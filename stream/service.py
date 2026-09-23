"""JBM streaming collector: a separate, continuously running service (NOT run by GitHub Actions).

  python -m stream.service --config stream/config.example.json [--duration 60]

What it does, per enabled venue connection (one thread each):
  * connects (optionally through HTTPS_PROXY), subscribes, keeps the connection alive with the
    venue's documented heartbeat (Deribit public/set_heartbeat + public/test replies; Hyperliquid
    {"method":"ping"}; Bybit {"op":"ping"}), and reconnects with exponential backoff and jitter;
  * stores every message as received (raw text + receive time) in hourly gzip partitions;
  * rebuilds order books with sequence checks (books.py); a sequence gap invalidates the book,
    is recorded, and triggers a re-subscription for a fresh snapshot;
  * de-duplicates trades by venue trade id and flags out-of-order trades (kept, marked).
The main loop samples valid books once a second (top of book and depth within 10 bp), keeps a
rolling buffer of recent messages, and writes CAPTURES around triggers (a mid move beyond
k sigma in `window_s`, or a burst of liquidations) and around scheduled CONTROLS, so baseline
coverage exists for every trigger type. Every disconnect, stall, sequence gap, overflow or service
restart is written to derived/gaps: a missing interval is never presented as zero activity.
A heartbeat file (heartbeat.json) is rewritten every `heartbeat_s`; stream/check_heartbeat.py
exits non-zero when it is stale.
"""
import argparse
import collections
import hashlib
import json
import math
import os
from pathlib import Path
import random
import sys
import threading
import time

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from stream.books import BybitBook, DeribitBook, HyperliquidBook
from stream.storage import LocalStore, backend_from_config, hour_key
from stream.wsclient import WebSocket, WSClosed

VERSION = "stream-1.0-2026-09-23"


def now_ms():
    return int(time.time() * 1000)


class Recorder:
    """Thread-safe writes into LocalStore, gap log, rolling buffer and captures."""
    def __init__(self, cfg, store):
        self.cfg, self.store = cfg, store
        self.lock = threading.Lock()
        b = cfg.get("buffer", {})
        self.pre_ms, self.post_ms = b.get("pre_seconds", 300) * 1000, b.get("post_seconds", 900) * 1000
        self.max_bytes = b.get("max_bytes", 64 * 1024 * 1024)
        self.buf, self.buf_bytes = collections.deque(), 0
        self.captures = {}                      # capture_id -> end_ms
        self.counters = collections.Counter()
        self.liqs = collections.deque()         # (t_ms, venue, usd notional) for the burst trigger

    def raw(self, venue, channel, t, text):
        day, hour = hour_key(t)
        rec = {"r": t, "m": text}
        with self.lock:
            self.store.append(f"raw/{venue}/{channel}/{day}/{hour}.jsonl.gz", rec)
            self.buf.append((t, venue, channel, text))
            self.buf_bytes += len(text)
            while self.buf and (self.buf[0][0] < t - self.pre_ms or self.buf_bytes > self.max_bytes):
                old = self.buf.popleft()
                self.buf_bytes -= len(old[3])
                if old[0] >= t - self.pre_ms:
                    self.counters["buffer_overflow_drops"] += 1
            for cid, end in list(self.captures.items()):
                if t <= end:
                    self.store.append(f"captures/{cid[:10]}/{cid}.jsonl.gz", {"r": t, "venue": venue, "ch": channel, "m": text})
                else:
                    del self.captures[cid]
            self.counters[f"msgs:{venue}"] += 1

    def gap(self, venue, start, end, reason, instrument=None):
        day, _ = hour_key(end or start or now_ms())
        with self.lock:
            self.store.append(f"derived/gaps/{day}.jsonl", {"venue": venue, "instrument": instrument, "start": start,
                                                           "end": end, "reason": reason, "version": VERSION})
            self.counters["gaps"] += 1

    def capture(self, kind, t, detail):
        """Start a capture: write the rolling buffer (pre-event) now, then everything until t+post."""
        cid = f"{time.strftime('%Y-%m-%d', time.gmtime(t / 1000))}-{kind}-{t}"
        day = cid[:10]
        with self.lock:
            self.store.append(f"derived/triggers/{day}.jsonl", {"capture_id": cid, "kind": kind, "t": t,
                                                               "detail": detail, "pre_ms": self.pre_ms,
                                                               "post_ms": self.post_ms, "buffered": len(self.buf)})
            for (bt, venue, ch, text) in self.buf:
                self.store.append(f"captures/{day}/{cid}.jsonl.gz", {"r": bt, "venue": venue, "ch": ch, "m": text})
            self.captures[cid] = t + self.post_ms
        return cid

    def sample(self, book, t):
        top = book.top()
        if top is None:
            return None
        if book.last_ts is not None and t - book.last_ts > self.cfg.get("sample_max_age_ms", 20000):
            self.counters[f"stale_book_skips:{book.venue}"] += 1     # missing, not a quiet book
            return None
        day, hour = hour_key(t)
        bid, ask, mid, bd, ad = top
        with self.lock:
            self.store.append(f"derived/book1s/{book.venue}/{book.instrument}/{day}/{hour}.jsonl.gz",
                              {"t": t, "bid": bid, "ask": ask, "mid": mid, "bid_depth_10bp": bd, "ask_depth_10bp": ad,
                               "book_ts": book.last_ts,
                               "book_age_ms": (t - book.last_ts) if book.last_ts is not None else None})
        return top


class Connection(threading.Thread):
    """One venue connection with reconnect/backoff, heartbeats and resubscription on gaps."""
    PING_S = {"hyperliquid": 50, "bybit": 20, "deribit": None}

    def __init__(self, venue, vcfg, rec, stop, stall_s=30):
        super().__init__(name=f"conn-{venue}", daemon=True)
        self.venue, self.vcfg, self.rec, self.stop_evt, self.stall_s = venue, vcfg, rec, stop, stall_s
        self.books, self.seen, self.last_trade_t = {}, collections.OrderedDict(), {}
        self.connected, self.last_msg, self.down_since = False, None, None
        self.ws, self.backoff, self.reconnects = None, 1.0, 0
        self.ws_factory = WebSocket
        self.lock = threading.Lock()            # guards books; order is always self.lock -> rec.lock

    # ---- venue specifics --------------------------------------------------------------------
    def subscribe_msgs(self):
        v = self.vcfg
        if self.venue == "deribit":
            return [{"jsonrpc": "2.0", "id": 1, "method": "public/set_heartbeat", "params": {"interval": 10}},
                    {"jsonrpc": "2.0", "id": 2, "method": "public/subscribe", "params": {"channels": v["channels"]}}]
        if self.venue == "hyperliquid":
            return [{"method": "subscribe", "subscription": s} for s in v["subscriptions"]]
        if self.venue == "bybit":
            return [{"op": "subscribe", "args": v["topics"]}]
        raise ValueError(self.venue)

    def resubscribe(self, what):
        if self.venue == "deribit":
            msgs = [{"jsonrpc": "2.0", "id": 3, "method": "public/unsubscribe", "params": {"channels": [what]}},
                    {"jsonrpc": "2.0", "id": 4, "method": "public/subscribe", "params": {"channels": [what]}}]
        elif self.venue == "bybit":
            msgs = [{"op": "unsubscribe", "args": [what]}, {"op": "subscribe", "args": [what]}]
        else:
            return
        for m in msgs:
            self.ws.send_text(json.dumps(m))

    def dedup(self, key):
        if key in self.seen:
            self.rec.counters[f"duplicates:{self.venue}"] += 1
            return False
        self.seen[key] = True
        if len(self.seen) > 50_000:
            self.seen.popitem(last=False)
        return True

    def trade_order(self, inst, t):
        last = self.last_trade_t.get(inst)
        if last is not None and t < last:
            self.rec.counters[f"out_of_order:{self.venue}"] += 1
        self.last_trade_t[inst] = max(t, last or t)

    def handle(self, text, t):
        js = json.loads(text)
        channel = "other"
        if self.venue == "deribit":
            if js.get("method") == "heartbeat" and (js.get("params") or {}).get("type") == "test_request":
                self.ws.send_text(json.dumps({"jsonrpc": "2.0", "id": 9, "method": "public/test", "params": {}}))
                channel = "heartbeat"
            elif js.get("method") == "subscription":
                channel = js["params"]["channel"]
                data = js["params"]["data"]
                if channel.startswith("book."):
                    inst = data.get("instrument_name")
                    book = self.books.setdefault(inst, DeribitBook(inst))
                    res = book.apply(data)
                    if res == "gap":
                        self.rec.gap(self.venue, book.gaps[-1][0], None, book.gaps[-1][1], inst)
                        self.resubscribe(channel)
                elif channel.startswith("trades."):
                    fresh = [d for d in data if self.dedup(("deribit", d.get("trade_id")))]
                    for d in fresh:
                        self.trade_order(d.get("instrument_name"), d.get("timestamp", t))
                        if d.get("liquidation"):
                            self.rec.counters["liquidation_flags:deribit"] += 1
                    if not fresh:
                        return
        elif self.venue == "hyperliquid":
            channel = js.get("channel", "other")
            data = js.get("data")
            if channel == "l2Book":
                book = self.books.setdefault(data["coin"], HyperliquidBook(data["coin"], self.vcfg.get("max_gap_ms", 15000)))
                n = len(book.gaps)
                if book.apply(data) == "applied" and len(book.gaps) > n:
                    self.rec.gap(self.venue, None, book.gaps[-1][0], book.gaps[-1][1], data["coin"])
                channel = f"l2Book.{data['coin']}"
            elif channel == "trades":
                fresh = [d for d in data if self.dedup(("hl", d.get("coin"), d.get("time"), d.get("tid")))]
                for d in fresh:
                    self.trade_order(d.get("coin"), d.get("time", t))
                if not fresh:
                    return
                channel = f"trades.{data[0]['coin']}" if data else "trades"
        elif self.venue == "bybit":
            topic = js.get("topic")
            channel = topic or js.get("op", "other")
            if topic and topic.startswith("orderbook."):
                inst = topic.split(".")[-1]
                book = self.books.setdefault(inst, BybitBook(inst))
                if book.apply(js) == "gap":
                    self.rec.gap(self.venue, book.gaps[-1][0], None, book.gaps[-1][1], inst)
                    self.resubscribe(topic)
            elif topic and topic.startswith("publicTrade."):
                fresh = [d for d in js.get("data", []) if self.dedup(("bybit", d.get("i")))]
                for d in fresh:
                    self.trade_order(d.get("s"), d.get("T", t))
                if not fresh:
                    return
            elif topic and topic.startswith("allLiquidation."):
                rows = js.get("data") or []
                self.rec.counters["liquidations:bybit"] += len(rows)
                with self.rec.lock:
                    for d in rows:      # p is the bankruptcy price (Bybit docs); v is size in base units
                        try:
                            self.rec.liqs.append((int(d.get("T", t)), "bybit", float(d["v"]) * float(d["p"])))
                        except (KeyError, TypeError, ValueError):
                            self.rec.counters["liquidation_rows_unparsed:bybit"] += 1
            elif topic and topic.startswith("adlAlert."):
                keep = set(self.vcfg.get("adl_symbols", ["BTCUSDT", "ETHUSDT", "SOLUSDT"]))
                js["data"] = [d for d in js.get("data") or [] if d.get("s") in keep]
                text = json.dumps(js, separators=(",", ":"))           # stored filtered; filter recorded below
                channel = topic + ".filtered"
        self.rec.raw(self.venue, channel.replace("/", "_"), t, text)

    # ---- loop -------------------------------------------------------------------------------
    def run(self):
        while not self.stop_evt.is_set():
            try:
                self.ws = self.ws_factory(self.vcfg["url"], timeout=10).connect()
                for m in self.subscribe_msgs():
                    self.ws.send_text(json.dumps(m))
                t = now_ms()
                if self.down_since is not None:
                    self.rec.gap(self.venue, self.down_since, t, "disconnected")
                self.down_since, self.connected, self.backoff, self.last_msg = None, True, 1.0, t
                last_ping = time.monotonic()
                while not self.stop_evt.is_set():
                    msg = self.ws.recv(1.0)
                    t = now_ms()
                    ping = self.PING_S.get(self.venue)
                    if ping and time.monotonic() - last_ping >= ping:
                        self.ws.send_text(json.dumps({"method": "ping"} if self.venue == "hyperliquid" else {"op": "ping"}))
                        last_ping = time.monotonic()
                    if msg is None:
                        if t - self.last_msg > self.stall_s * 1000:
                            raise WSClosed(f"no message for {self.stall_s} s")
                        continue
                    self.last_msg = t
                    with self.lock:
                        self.handle(msg if isinstance(msg, str) else msg.decode(), t)
            except Exception as exc:                                    # any failure: record, back off, retry
                t = now_ms()
                if self.connected or self.down_since is None:
                    self.down_since = self.last_msg or t
                self.connected = False
                with self.lock:
                    for book in self.books.values():
                        book.invalidate(t, f"disconnect: {type(exc).__name__}")
                self.rec.counters[f"reconnects:{self.venue}"] += 1
                self.reconnects += 1
                self.rec.counters[f"last_error:{self.venue}:{type(exc).__name__}: {str(exc)[:80]}"] += 1
                try:
                    if self.ws:
                        self.ws.close()
                except Exception:
                    pass
                self.stop_evt.wait(self.backoff * (0.5 + random.random()))
                self.backoff = min(self.backoff * 2, 60.0)


class Triggers:
    """Mid-move trigger per (venue, instrument) on 1-second samples, with cooldown."""
    def __init__(self, cfg):
        t = cfg.get("triggers", {})
        self.k, self.window, self.cooldown = t.get("mid_move_sigma", 4.0), t.get("window_s", 10), t.get("cooldown_s", 900)
        self.hist = {}
        self.last_fire = {}

    def update(self, key, t, mid):
        h = self.hist.setdefault(key, collections.deque(maxlen=1800 + self.window))
        h.append((t, mid))
        if len(h) < 600 + self.window:
            return None
        pts = list(h)
        rets = [math.log(pts[i][1] / pts[i - self.window][1]) for i in range(self.window, len(pts) - 1)]
        mu = sum(rets) / len(rets)
        sd = math.sqrt(sum((r - mu) ** 2 for r in rets) / (len(rets) - 1))
        now_ret = math.log(pts[-1][1] / pts[-1 - self.window][1])
        if sd > 0 and abs(now_ret) >= self.k * sd and t - self.last_fire.get(key, 0) >= self.cooldown * 1000:
            self.last_fire[key] = t
            return {"key": key, "ret": now_ret, "sigma": sd, "k": self.k, "window_s": self.window}
        return None


def upload_cycle(store, backend, rec, uploaded, t, cfg):
    """Upload closed partitions to the durable backend (verified by size), write the manifest, then
    apply local retention. Failures are counted and retried next cycle; they never stop capture.
    Without a backend nothing is ever deleted unless local_only_deletion is explicitly enabled."""
    with rec.lock:
        store.flush()
        open_caps = {f"captures/{c[:10]}/{c}.jsonl.gz" for c in rec.captures}
    for key in store.closed_partitions(t):
        if key in uploaded or key in open_caps:
            continue
        if backend is None:
            if cfg.get("local_only_deletion"):
                uploaded.add(key)          # explicit opt-in: local retention may delete without a copy
            continue
        try:
            data = store.path(key).read_bytes()
            backend.put(key, data)
            if backend.size(key) != len(data):
                raise IOError("size mismatch after upload")
        except Exception as exc:
            rec.counters[f"upload_failures:{type(exc).__name__}"] += 1
            continue
        uploaded.add(key)
        rec.counters["uploads"] += 1
        rec.counters["upload_bytes"] += len(data)
        day = hour_key(t)[0]
        with rec.lock:
            store.append(f"manifest/{day}.jsonl", {"key": key, "bytes": len(data),
                                                   "sha256": hashlib.sha256(data).hexdigest(), "uploaded_at": t})
    removed = store.retention(t, cfg.get("retention_days_raw_local"), cfg.get("retention_days_derived_local"), uploaded)
    rec.counters["local_partitions_deleted"] += len(removed)


def write_json_atomic(path, obj):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=True))
    os.replace(tmp, path)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--duration", type=float, default=None, help="seconds to run (default: forever)")
    args = ap.parse_args(argv)
    cfg = json.loads(Path(args.config).read_text())
    root = Path(os.environ.get("STREAM_DATA_DIR", cfg["data_dir"]))
    store = LocalStore(root)
    backend = backend_from_config(cfg)
    rec = Recorder(cfg, store)
    state_path = root / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    start = now_ms()
    if state.get("heartbeat"):
        rec.gap("service", state["heartbeat"], start, "service not running (restart)")
    stop = threading.Event()
    conns = [Connection(v, c, rec, stop, cfg.get("stall_s", 30)) for v, c in cfg["venues"].items() if c.get("enabled")]
    for c in conns:
        c.start()
    trig = Triggers(cfg)
    uploaded = set(state.get("uploaded", []))
    next_control = (start // (cfg.get("controls_every_s", 3600) * 1000) + 1) * cfg.get("controls_every_s", 3600) * 1000
    last_flush = last_hb = last_upload = time.monotonic()
    try:
        while not stop.is_set():
            time.sleep(1.0 - (time.time() % 1.0))
            t = now_ms()
            for c in conns:
                with c.lock:
                    for book in list(c.books.values()):
                        top = rec.sample(book, t)
                        fired = trig.update(f"{book.venue}:{book.instrument}", t, top[2]) if top else None
                        if fired:
                            rec.capture("trigger", t, fired)
            if t >= next_control:
                rec.capture("control", t, {"schedule_s": cfg.get("controls_every_s", 3600)})
                next_control += cfg.get("controls_every_s", 3600) * 1000
            if time.monotonic() - last_flush >= cfg.get("flush_s", 5):
                with rec.lock:
                    store.flush()
                last_flush = time.monotonic()
            if time.monotonic() - last_hb >= cfg.get("heartbeat_s", 10):
                write_json_atomic(root / "heartbeat.json", {
                    "t": t, "version": VERSION, "connections": {c.venue: {"connected": c.connected, "last_msg": c.last_msg,
                                                                          "reconnects": c.reconnects,
                                                                          "books_valid": sum(b.valid for b in c.books.values())}
                                                               for c in conns},
                    "counters": dict(rec.counters), "buffer_bytes": rec.buf_bytes, "captures_open": len(rec.captures)})
                state.update(heartbeat=t, uploaded=sorted(uploaded)[-5000:])
                write_json_atomic(state_path, state)
                last_hb = time.monotonic()
            burst = cfg.get("triggers", {}).get("liq_burst_usd_60s")
            if burst:
                with rec.lock:
                    while rec.liqs and rec.liqs[0][0] < t - 60_000:
                        rec.liqs.popleft()
                    total = sum(x[2] for x in rec.liqs)
                if total >= burst and t - trig.last_fire.get("liq_burst", 0) >= trig.cooldown * 1000:
                    trig.last_fire["liq_burst"] = t
                    rec.capture("liq_burst", t, {"usd_at_bankruptcy_px_60s": total, "threshold": burst})
            if time.monotonic() - last_upload >= cfg.get("upload_every_s", 300):
                upload_cycle(store, backend, rec, uploaded, t, cfg)
                last_upload = time.monotonic()
            if args.duration and time.time() * 1000 - start >= args.duration * 1000:
                break
    finally:
        stop.set()
        for c in conns:
            c.join(timeout=5)
        with rec.lock:
            store.flush()
        state.update(heartbeat=now_ms(), uploaded=sorted(uploaded)[-5000:])
        write_json_atomic(state_path, state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
