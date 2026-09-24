"""Tests for the streaming collector (stream/): frames and handshake, order-book continuity (gaps,
duplicates, out-of-order, resync), the rolling pre/post buffer, gzip-member storage, retention,
the durable-upload cycle under failure, the S3 SigV4 signer (vectors cross-checked with botocore
1.35.0), reconnect/backoff with gap records, and the heartbeat check. Offline: a local socket
server and scripted fake transports stand in for the venues.
"""
import base64
import gzip
import hashlib
import json
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path

from stream import check_heartbeat, service, storage, wsclient
from stream.books import BybitBook, DeribitBook, HyperliquidBook

T0 = 1_790_184_200_000                                    # 2026-09-23 17:23:20 UTC


class FrameTests(unittest.TestCase):
    def pair(self):
        a, b = socket.socketpair()
        ws = wsclient.WebSocket("ws://x/")
        ws.sock = a
        return ws, a, b

    def test_text_fragmented_ping_and_close(self):
        ws, a, b = self.pair()
        try:
            b.sendall(wsclient.encode_frame(wsclient.OP_TEXT, b'{"a":1}', mask=False))
            b.sendall(wsclient.encode_frame(wsclient.OP_PING, b"hb", mask=False))
            b.sendall(wsclient.encode_frame(wsclient.OP_TEXT, b"frag-", mask=False, fin=False))
            b.sendall(wsclient.encode_frame(wsclient.OP_CONT, b"ment", mask=False))
            self.assertEqual(ws.recv(1), '{"a":1}')
            self.assertEqual(ws.recv(1), "frag-ment")                 # ping answered in between
            b.settimeout(1)
            fin, op, data = wsclient.read_frame(b)                   # client's pong, masked
            self.assertEqual((fin, op, data), (True, wsclient.OP_PONG, b"hb"))
            self.assertIsNone(ws.recv(0.05))                         # nothing pending: None, not an error
            b.sendall(wsclient.encode_frame(wsclient.OP_CLOSE, b"", mask=False))
            with self.assertRaises(wsclient.WSClosed):
                ws.recv(1)
        finally:
            a.close(), b.close()

    def test_lengths_126_and_127(self):
        ws, a, b = self.pair()
        try:
            for n in (200, 70_000):
                payload = ("x" * n).encode()
                threading.Thread(target=b.sendall, args=(wsclient.encode_frame(wsclient.OP_TEXT, payload, mask=False),)).start()
                self.assertEqual(len(ws.recv(2)), n)
        finally:
            a.close(), b.close()

    def test_oversize_frame_rejected(self):
        ws, a, b = self.pair()
        try:
            b.sendall(bytes([0x81, 127]) + (wsclient.MAX_MESSAGE + 1).to_bytes(8, "big"))
            with self.assertRaises(wsclient.WSClosed):
                ws.recv(1)
        finally:
            a.close(), b.close()

    def test_handshake_against_local_server(self):
        srv = socket.socket()
        srv.bind(("127.0.0.1", 0))
        srv.listen(1)
        port = srv.getsockname()[1]

        def serve():
            c, _ = srv.accept()
            req = b""
            while b"\r\n\r\n" not in req:
                req += c.recv(4096)
            key = [l.split(b": ")[1] for l in req.split(b"\r\n") if l.lower().startswith(b"sec-websocket-key")][0].decode()
            acc = base64.b64encode(hashlib.sha1((key + wsclient.GUID).encode()).digest()).decode()
            c.sendall(f"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                      f"Sec-WebSocket-Accept: {acc}\r\n\r\n".encode())
            fin, op, data = wsclient.read_frame(c)
            c.sendall(wsclient.encode_frame(wsclient.OP_TEXT, b"echo:" + data, mask=False))
            time.sleep(0.2)
            c.close()
        th = threading.Thread(target=serve)
        th.start()
        ws = wsclient.WebSocket(f"ws://127.0.0.1:{port}/ws", timeout=5, proxy="").connect()
        ws.send_text("hi")
        self.assertEqual(ws.recv(2), "echo:hi")
        with self.assertRaises(wsclient.WSClosed):
            ws.recv(2)                                                 # peer closed: an error, never silence
        ws.close()
        th.join()
        srv.close()


class BookTests(unittest.TestCase):
    def test_deribit_snapshot_changes_gap_duplicate(self):
        b = DeribitBook("BTC-PERPETUAL")
        self.assertEqual(b.apply({"type": "change", "prev_change_id": 5, "change_id": 6, "timestamp": 1,
                                  "bids": [], "asks": []}), "ignored_until_snapshot")
        self.assertEqual(b.apply({"type": "snapshot", "change_id": 10, "timestamp": 2,
                                  "bids": [["new", 100.0, 5], ["new", 99.5, 3]], "asks": [["new", 100.5, 4]]}), "applied")
        self.assertEqual(b.top()[:3], (100.0, 100.5, 100.25))
        self.assertEqual(b.apply({"type": "change", "prev_change_id": 10, "change_id": 11, "timestamp": 3,
                                  "bids": [["delete", 100.0, 0]], "asks": []}), "applied")
        self.assertEqual(b.top()[0], 99.5)
        self.assertEqual(b.apply({"type": "change", "prev_change_id": 9, "change_id": 10, "timestamp": 4,
                                  "bids": [], "asks": []}), "duplicate_or_stale")
        self.assertTrue(b.valid)
        self.assertEqual(b.apply({"type": "change", "prev_change_id": 13, "change_id": 14, "timestamp": 5,
                                  "bids": [], "asks": []}), "gap")
        self.assertFalse(b.valid)
        self.assertIsNone(b.top())                                     # invalid book is never sampled
        self.assertEqual(len(b.gaps), 1)
        self.assertEqual(b.apply({"type": "snapshot", "change_id": 20, "timestamp": 6,
                                  "bids": [["new", 101.0, 1]], "asks": [["new", 101.5, 1]]}), "applied")   # resync
        self.assertTrue(b.valid)

    def test_bybit_sequence(self):
        b = BybitBook("BTCUSDT")
        snap = {"type": "snapshot", "ts": 1, "data": {"s": "BTCUSDT", "u": 100, "b": [["100", "2"]], "a": [["101", "3"]]}}
        self.assertEqual(b.apply(snap), "applied")
        self.assertEqual(b.apply({"type": "delta", "ts": 2, "data": {"u": 101, "b": [["100", "0"]], "a": []}}), "applied")
        self.assertIsNone(b.top())                                     # one-sided book is unusable
        self.assertEqual(b.apply({"type": "delta", "ts": 3, "data": {"u": 101, "b": [["99", "1"]], "a": []}}),
                         "duplicate_or_stale")
        self.assertEqual(b.apply({"type": "delta", "ts": 4, "data": {"u": 102, "b": [["99", "1"]], "a": []}}), "applied")
        self.assertEqual(b.apply({"type": "delta", "ts": 5, "data": {"u": 104, "b": [], "a": []}}), "gap")
        self.assertFalse(b.valid)
        self.assertEqual(b.apply({"type": "delta", "ts": 6, "data": {"u": 105, "b": [], "a": []}}), "ignored_until_snapshot")
        self.assertEqual(b.apply({"type": "delta", "ts": 7, "data": {"u": 1, "b": [["98", "1"]], "a": [["99", "1"]]}}),
                         "applied")                                    # u == 1: service restart resets the book
        self.assertEqual(b.top()[:2], (98.0, 99.0))

    def test_crossed_book_unusable(self):
        b = BybitBook("BTCUSDT")
        b.apply({"type": "snapshot", "ts": 1, "data": {"u": 5, "b": [["101", "1"]], "a": [["100", "1"]]}})
        self.assertIsNone(b.top())

    def test_hyperliquid_stale_and_silence(self):
        b = HyperliquidBook("BTC", max_gap_ms=15000)
        lv = [[{"px": "100", "sz": "1"}], [{"px": "101", "sz": "2"}]]
        self.assertEqual(b.apply({"time": 1000, "levels": lv}), "applied")
        self.assertEqual(b.apply({"time": 1000, "levels": lv}), "duplicate_or_stale")
        self.assertEqual(b.apply({"time": 900, "levels": lv}), "duplicate_or_stale")
        self.assertEqual(b.apply({"time": 6400, "levels": lv}), "applied")   # measured cadence: no gap
        self.assertEqual(b.gaps, [])
        b.apply({"time": 30000, "levels": lv})
        self.assertEqual(len(b.gaps), 1)

    def test_depth_band(self):
        b = BybitBook("X")
        b.apply({"type": "snapshot", "ts": 1, "data": {"u": 1, "b": [["100", "1"], ["99.95", "2"], ["99", "9"]],
                                                          "a": [["100.1", "3"], ["101", "9"]]}})
        bid, ask, mid, bd, ad = b.top(band_bp=10)
        self.assertEqual((bd, ad), (3.0, 3.0))                         # levels beyond 10 bp of mid excluded


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = storage.LocalStore(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_gzip_members_survive_append_and_truncated_tail(self):
        key = "raw/v/c/2026-09-23/18.jsonl.gz"
        self.store.append(key, {"i": 1})
        self.store.flush()
        self.store.append(key, {"i": 2})
        self.store.flush()
        self.assertEqual([r["i"] for r in self.store.read(key)], [1, 2])
        p = self.store.path(key)
        good = p.read_bytes()
        p.write_bytes(good + gzip.compress(b'{"i":3}\n')[:14])         # crash mid-member
        with gzip.open(p) as fh:
            with self.assertRaises(EOFError):
                fh.read()
        rows = []
        with gzip.open(p) as fh:                                      # earlier members still readable
            try:
                for line in fh:
                    rows.append(json.loads(line))
            except EOFError:
                pass
        self.assertEqual([r["i"] for r in rows], [1, 2])

    def test_closed_partitions_and_retention_only_after_upload(self):
        for day, hour in (("2026-09-10", "05"), ("2026-09-23", "16"), ("2026-09-23", "17")):
            self.store.append(f"raw/v/c/{day}/{hour}.jsonl.gz", {"x": 1})
        self.store.flush()
        closed = self.store.closed_partitions(T0)                      # now = 17:23 -> hour 17 still open
        self.assertIn("raw/v/c/2026-09-10/05.jsonl.gz", closed)
        self.assertIn("raw/v/c/2026-09-23/16.jsonl.gz", closed)
        self.assertNotIn("raw/v/c/2026-09-23/17.jsonl.gz", closed)
        self.assertEqual(self.store.retention(T0, 7, 30, uploaded=set()), [])          # never delete an unuploaded copy
        self.assertEqual(self.store.retention(T0, 7, 30, uploaded={"raw/v/c/2026-09-10/05.jsonl.gz"}),
                         ["raw/v/c/2026-09-10/05.jsonl.gz"])

    def test_sigv4_matches_botocore_vectors(self):
        # Signatures produced by botocore 1.35.0 S3SigV4Auth for the same inputs (2026-09-23 cross-check).
        vectors = [
            ("PUT", "https://acct.r2.cloudflarestorage.com/bucket/jbm-stream/raw/bybit/orderbook.50.BTCUSDT/2026-09-23/19.jsonl.gz",
             b"hello world", "b1ab7fe10b30cba8a5cd86f81e55c197e784169e147420bd69f1b75727c641c4"),
            ("HEAD", "https://acct.r2.cloudflarestorage.com/bucket/jbm-stream/raw/bybit/orderbook.50.BTCUSDT/2026-09-23/19.jsonl.gz",
             b"", "1ee12f90028660435482133bac17d5b6965d040564a67286c5da2f2092c3eb7e"),
            ("PUT", "https://s3.eu-west-1.amazonaws.com/bkt/p/derived/gaps/2026-09-23.jsonl", b"hello world",
             "96c62b5931972a42a619da07077bfa05607af6bdb66f7b4dad91c9ac2ab4458b"),
            ("HEAD", "https://s3.eu-west-1.amazonaws.com/bkt/p/derived/gaps/2026-09-23.jsonl", b"",
             "9acf349c8a7055ba29ef9a656e2bdfad00c1cd283eddd29e910f70826aee5ce1")]
        for method, url, payload, sig in vectors:
            h = storage.sigv4_headers(method, url, "auto", "AKIDEXAMPLE", "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY",
                                      hashlib.sha256(payload).hexdigest(), "20260923T190000Z")
            self.assertTrue(h["Authorization"].endswith("Signature=" + sig), method + url)

    def test_backend_requires_credentials_from_environment(self):
        cfg = {"storage": {"backend": "s3", "s3": {"endpoint": "https://e", "bucket": "b", "access_key_env": "NOPE_K_1",
                                                    "secret_key_env": "NOPE_S_1"}}}
        with self.assertRaises(RuntimeError):
            storage.backend_from_config(cfg)
        self.assertIsNone(storage.backend_from_config({"storage": {"backend": "none"}}))


class FakeBackend:
    def __init__(self, fail_keys=(), short=False):
        self.objects, self.fail_keys, self.short = {}, set(fail_keys), short

    def put(self, key, data):
        if key in self.fail_keys:
            raise OSError("network down")
        self.objects[key] = data[:-1] if self.short else data

    def size(self, key):
        return len(self.objects[key])


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = storage.LocalStore(self.tmp.name)
        self.rec = service.Recorder({"buffer": {"pre_seconds": 10, "post_seconds": 5}}, self.store)

    def tearDown(self):
        self.tmp.cleanup()

    def test_capture_has_pre_and_post_window_only(self):
        for i in range(30):                                            # one message per second
            self.rec.raw("v", "c", T0 + i * 1000, f'{{"i":{i}}}')
        cid = self.rec.capture("trigger", T0 + 29_000, {"k": 4})
        for i in range(30, 40):
            self.rec.raw("v", "c", T0 + i * 1000, f'{{"i":{i}}}')
        self.store.flush()
        got = [json.loads(r["m"])["i"] for r in self.store.read(f"captures/{cid[:10]}/{cid}.jsonl.gz")]
        self.assertEqual(got, list(range(19, 35)))                     # 10 s before (inclusive) .. 5 s after
        trig = self.store.read(f"derived/triggers/{cid[:10]}.jsonl")
        self.assertEqual(trig[0]["kind"], "trigger")

    def test_buffer_byte_cap_counts_drops(self):
        rec = service.Recorder({"buffer": {"pre_seconds": 1000, "max_bytes": 50}}, self.store)
        for i in range(10):
            rec.raw("v", "c", T0 + i, "x" * 20)
        self.assertLessEqual(rec.buf_bytes, 50)
        self.assertGreater(rec.counters["buffer_overflow_drops"], 0)   # overflow is exposed, not silent

    def test_stale_book_not_sampled(self):
        b = BybitBook("BTCUSDT")
        b.apply({"type": "snapshot", "ts": T0, "data": {"u": 5, "b": [["100", "1"]], "a": [["101", "1"]]}})
        self.assertIsNotNone(self.rec.sample(b, T0 + 1000))
        self.assertIsNone(self.rec.sample(b, T0 + 60_000))
        self.assertEqual(self.rec.counters["stale_book_skips:bybit"], 1)

    def test_upload_cycle_failure_is_counted_and_retried(self):
        for hour in ("15", "16"):
            self.store.append(f"raw/v/c/2026-09-23/{hour}.jsonl.gz", {"h": hour})
        self.store.flush()
        uploaded = set()
        be = FakeBackend(fail_keys={"raw/v/c/2026-09-23/15.jsonl.gz"})
        service.upload_cycle(self.store, be, self.rec, uploaded, T0, {})
        self.assertEqual(uploaded, {"raw/v/c/2026-09-23/16.jsonl.gz"})
        self.assertEqual(self.rec.counters["upload_failures:OSError"], 1)
        be.fail_keys = set()
        service.upload_cycle(self.store, be, self.rec, uploaded, T0, {})
        self.assertEqual(len(uploaded), 2)
        self.store.flush()
        man = self.store.read("manifest/2026-09-23.jsonl")
        self.assertEqual(sorted(m["key"] for m in man), sorted(uploaded))
        self.assertTrue(all(len(m["sha256"]) == 64 for m in man))

    def test_upload_size_mismatch_not_marked(self):
        self.store.append("raw/v/c/2026-09-23/15.jsonl.gz", {"h": 1})
        self.store.flush()
        uploaded = set()
        service.upload_cycle(self.store, FakeBackend(short=True), self.rec, uploaded, T0, {})
        self.assertEqual(uploaded, set())
        self.assertEqual(self.rec.counters["upload_failures:OSError"], 1)

    def test_no_backend_never_deletes_unless_opted_in(self):
        self.store.append("raw/v/c/2026-09-01/15.jsonl.gz", {"h": 1})
        self.store.flush()
        uploaded = set()
        service.upload_cycle(self.store, None, self.rec, uploaded, T0, {"retention_days_raw_local": 7})
        self.assertTrue(self.store.path("raw/v/c/2026-09-01/15.jsonl.gz").exists())
        service.upload_cycle(self.store, None, self.rec, uploaded, T0,
                             {"retention_days_raw_local": 7, "local_only_deletion": True})
        self.assertFalse(self.store.path("raw/v/c/2026-09-01/15.jsonl.gz").exists())

    def test_open_capture_not_uploaded(self):
        cid = self.rec.capture("control", T0 - 7200_000, {})
        self.rec.captures[cid] = T0 + 10**9                            # still open
        self.store.flush()
        uploaded = set()
        service.upload_cycle(self.store, FakeBackend(), self.rec, uploaded, T0, {})
        self.assertNotIn(f"captures/{cid[:10]}/{cid}.jsonl.gz", uploaded)


class FakeWS:
    """Scripted transport: each connect() takes the next script; a script is a list of messages
    (str) and ends by raising WSClosed (disconnect) unless it is the last one, which then idles."""
    def __init__(self, scripts, sent):
        self.scripts, self.sent = scripts, sent

    def __call__(self, url, timeout=10):
        return self

    def connect(self):
        if not self.scripts:
            raise OSError("refused")
        self.cur = list(self.scripts.pop(0))
        self.last = not self.scripts
        return self

    def send_text(self, text):
        self.sent.append(json.loads(text))

    def recv(self, timeout=None):
        if self.cur:
            return self.cur.pop(0)
        if self.last:
            time.sleep(0.01)
            return None
        raise wsclient.WSClosed("scripted disconnect")

    def close(self):
        pass


def bybit(kind, u, b=(), a=(), ts=T0):
    return json.dumps({"topic": "orderbook.50.BTCUSDT", "type": kind, "ts": ts,
                       "data": {"s": "BTCUSDT", "u": u, "b": [list(x) for x in b], "a": [list(x) for x in a]}})


class ConnectionTests(unittest.TestCase):
    def run_conn(self, venue, vcfg, scripts, secs=0.6):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        store = storage.LocalStore(tmp.name)
        rec = service.Recorder({}, store)
        stop = threading.Event()
        sent = []
        c = service.Connection(venue, vcfg, rec, stop, stall_s=30)
        c.ws_factory = FakeWS(scripts, sent)
        c.backoff = 0.01
        orig_wait = stop.wait
        stop.wait = lambda s: orig_wait(min(s, 0.02))                  # compress backoff for the test
        c.start()
        time.sleep(secs)
        stop.set()
        c.join(2)
        store.flush()
        return c, rec, store, sent

    def test_bybit_gap_resubscribes_and_disconnect_recorded(self):
        vcfg = {"url": "wss://x", "topics": ["orderbook.50.BTCUSDT", "publicTrade.BTCUSDT"]}
        trade = lambda i, T: json.dumps({"topic": "publicTrade.BTCUSDT", "ts": T, "data": [{"i": i, "T": T, "s": "BTCUSDT"}]})
        scripts = [[bybit("snapshot", 10, [("100", "1")], [("101", "1")]), bybit("delta", 11, [("100", "2")]),
                    bybit("delta", 13), trade("a", T0 + 5), trade("a", T0 + 5), trade("b", T0 + 1)],
                   [bybit("snapshot", 50, [("100", "1")], [("101", "1")])]]
        c, rec, store, sent = self.run_conn("bybit", vcfg, scripts)
        self.assertIn({"op": "unsubscribe", "args": ["orderbook.50.BTCUSDT"]}, sent)
        self.assertEqual(sum(1 for m in sent if m.get("op") == "subscribe" and m["args"] == vcfg["topics"]), 2)
        self.assertEqual(rec.counters["duplicates:bybit"], 1)
        self.assertEqual(rec.counters["out_of_order:bybit"], 1)
        # A gap is filed under the UTC day of its own time: the update-id jump carries the message
        # time (T0's day), the disconnect the wall clock. Read both days, so the test does not depend
        # on the date it runs (it only passed on 2026-09-23 before 2.9).
        days = {storage.hour_key(T0)[0], storage.hour_key(int(time.time() * 1000))[0]}
        gaps = [g for day in sorted(days) if store.path(f"derived/gaps/{day}.jsonl").exists()
                for g in store.read(f"derived/gaps/{day}.jsonl")]
        reasons = [g["reason"] for g in gaps]
        self.assertTrue(any("update id jump 11 -> 13" in r for r in reasons))
        self.assertIn("disconnected", reasons)
        self.assertTrue(c.books["BTCUSDT"].valid)                     # resynchronised from the new snapshot
        self.assertEqual(c.reconnects, 1)

    def test_deribit_heartbeat_reply_and_resync(self):
        vcfg = {"url": "wss://x", "channels": ["book.BTC-PERPETUAL.100ms"]}
        ch = "book.BTC-PERPETUAL.100ms"
        msg = lambda d: json.dumps({"jsonrpc": "2.0", "method": "subscription", "params": {"channel": ch, "data": d}})
        base = {"instrument_name": "BTC-PERPETUAL", "timestamp": T0}
        scripts = [[msg({**base, "type": "snapshot", "change_id": 1, "bids": [["new", 100.0, 1]], "asks": [["new", 101.0, 1]]}),
                    json.dumps({"jsonrpc": "2.0", "method": "heartbeat", "params": {"type": "test_request"}}),
                    msg({**base, "type": "change", "prev_change_id": 5, "change_id": 6, "bids": [], "asks": []}),
                    msg({**base, "type": "snapshot", "change_id": 7, "bids": [["new", 100.0, 1]], "asks": [["new", 101.0, 1]]})]]
        c, rec, store, sent = self.run_conn("deribit", vcfg, scripts, secs=0.3)
        methods = [m.get("method") for m in sent]
        self.assertEqual(methods[:2], ["public/set_heartbeat", "public/subscribe"])
        self.assertIn("public/test", methods)
        self.assertIn("public/unsubscribe", methods)
        self.assertTrue(c.books["BTC-PERPETUAL"].valid)

    def test_refused_connections_back_off_without_crashing(self):
        c, rec, store, sent = self.run_conn("hyperliquid", {"url": "wss://x", "subscriptions": []}, [], secs=0.3)
        self.assertGreaterEqual(rec.counters["reconnects:hyperliquid"], 2)
        self.assertFalse(c.connected)


class TriggerAndHeartbeatTests(unittest.TestCase):
    def test_trigger_warmup_fire_and_cooldown(self):
        tr = service.Triggers({"triggers": {"mid_move_sigma": 4, "window_s": 10, "cooldown_s": 900}})
        import random
        rng = random.Random(3)
        mid, fired = 100.0, []
        for i in range(700):
            mid *= 1 + rng.gauss(0, 0.0001)
            fired.append(tr.update("k", T0 + i * 1000, mid))
        self.assertFalse(any(fired))
        self.assertIsNotNone(tr.update("k", T0 + 700_000, mid * 1.01))
        self.assertIsNone(tr.update("k", T0 + 701_000, mid * 1.02))   # cooldown

    def test_heartbeat_check(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(check_heartbeat.check(d)["ok"])
            Path(d, "heartbeat.json").write_text(json.dumps({"t": T0, "connections": {
                "bybit": {"connected": True, "last_msg": T0 - 1000}, "hyperliquid": {"connected": False, "last_msg": T0 - 500_000}}}))
            v = check_heartbeat.check(d, now_ms=T0 + 5000)
            self.assertFalse(v["ok"])
            self.assertTrue(any("hyperliquid" in r for r in v["reasons"]))
            self.assertFalse(check_heartbeat.check(d, now_ms=T0 + 600_000)["ok"])

    def test_restart_gap_written(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Path(d, "c.json")
            cfg.write_text(json.dumps({"data_dir": d, "venues": {}}))
            Path(d, "state.json").write_text(json.dumps({"heartbeat": T0}))
            service.main(["--config", str(cfg), "--duration", "1"])
            gaps = [json.loads(l) for f in Path(d, "derived/gaps").glob("*.jsonl") for l in f.read_text().splitlines()]
            self.assertEqual(gaps[0]["reason"], "service not running (restart)")
            self.assertEqual(gaps[0]["start"], T0)


if __name__ == "__main__":
    unittest.main()
