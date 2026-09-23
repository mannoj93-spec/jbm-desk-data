#!/usr/bin/env python3
"""JBM desk collector v2 -- stdlib only.

Keeps what the venues forget, in three shapes:

  1. History series (Binance positioning / OI / taker / funding, OKX mark, index,
     funding and account ratio, Deribit DVOL). Checkpointed: every run fetches every
     CLOSED interval since the last stored one, so 5m history survives even though the
     job runs hourly (runbook D: one snapshot an hour does not preserve 5m history).
  2. OKX forced-flow feed. Individual orders, deduplicated, each stamped with the run
     that first saw it -- which is what lets report.py measure how much an hour's total
     revises after the hour closes. Once a day the feed is paged to its boundary (O14).
  3. Snapshot of current-only data: OI on every book, funding fields by name, depth,
     Coinbase premium components, Bitfinex margin positions.
  4. Forward-only books no source retains (runbook F requirement 50): Deribit per-strike
     option open interest with mark IV, and the Hyperliquid position map (top accounts by
     account value -> BTC positions with liquidation price and leverage type).

Nothing is derived here beyond unit conversion that the runbook fixes per venue.
Everything else is computed at read time by versioned code (report.py or a skill thread).

Usage:
  python collector.py              # hourly run
  python collector.py --backfill   # page every history series back to its source boundary
Exit code 0 always, unless the critical Binance share series failed (then 2) --
the workflow commits first and fails afterwards so GitHub emails the owner.
"""
import gzip, json, math, os, re, sys, time, urllib.request, urllib.error, datetime as dt
from storage import atomic_json, read_json, append_unique
from registration import register as register_content
from schema import SERIES_KIND

CODE_VERSION = "collector-2.4-2026-09-23"
UA = {"User-Agent": "jbm-desk-collector/2.0", "Accept": "application/json"}
BASE = os.environ.get("OUT_DIR", os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(BASE, "state", "checkpoints.json")
BN = "https://www.binance.com"          # fapi.binance.com returns 451 from US datacenters
OKX = "https://www.okx.com/api/v5"
H = 3_600_000
M5 = 300_000
BACKFILL = "--backfill" in sys.argv
NOW = int(time.time() * 1000)
# Run-wide network budget. The workflow kills the job at 30 minutes; persistence runs after this
# process exits, so every request must stop well before that. A simulated all-venue outage took
# 285 minutes under 2.3 (576 requests, each waiting its full timeout). After the deadline, get()
# returns an error without a request, so each remaining stage fails fast and the run record is
# still written. Override with COLLECTOR_BUDGET_S.
RUN_BUDGET_S = int(os.environ.get("COLLECTOR_BUDGET_S", 20 * 60))
DEADLINE = time.time() + RUN_BUDGET_S
RUN = {"code_version": CODE_VERSION, "t_ret": NOW, "mode": "backfill" if BACKFILL else "hourly",
       "runner": "github" if os.environ.get("GITHUB_ACTIONS") else os.environ.get("RUNNER_LABEL", "local"),
       "series": {}, "liq": {}, "snap": {}, "errors": {}}


def iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def month(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m")


# ------------------------------------------------------------------ HTTP
def get(url, body=None, tries=4, pause=0.0, timeout=25, deadline=None):
    """Returns (json, None) or (None, reason). A 200 carrying an error body is a failure (M-19).
    No request starts after the run deadline (or the caller's earlier `deadline`), and no request
    or retry pause runs past it: the socket timeout is capped by the time remaining."""
    last = None
    stop = min(DEADLINE, deadline) if deadline else DEADLINE
    for i in range(tries):
        if pause:
            time.sleep(min(pause, max(0.0, stop - time.time())))
        remaining = stop - time.time()
        if remaining < 1:
            return None, (last + "; " if last else "") + "deadline reached"
        try:
            data = json.dumps(body).encode() if body is not None else None
            hdr = dict(UA)
            if data:
                hdr["Content-Type"] = "application/json"
            req = urllib.request.Request(url, data=data, headers=hdr)
            with urllib.request.urlopen(req, timeout=min(timeout, remaining)) as r:
                js = json.loads(r.read().decode())
            err = body_error(js)
            if err:
                return None, err
            return js, None
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (400, 401, 403, 404, 451):
                # Keep the venue's own reason (e.g. Bitget 40309 "symbol has been removed").
                try:
                    detail = body_error(json.loads(e.read().decode()))
                except Exception:
                    detail = None
                return None, last + (f" ({detail})" if detail else "")   # not transient
        except Exception as e:
            last = type(e).__name__ + ": " + str(e)[:80]
        if i + 1 < tries:
            time.sleep(min(2 + 3 * i, max(0.0, stop - time.time())))
    return None, last or "failed"


def body_error(js):
    if isinstance(js, dict):
        if "code" in js and isinstance(js.get("code"), int) and js["code"] < 0:
            return f"binance code {js['code']}: {js.get('msg', '')[:60]}"          # Binance
        c = js.get("code")
        if isinstance(c, str) and c not in ("0", "00000", "200000"):
            return f"code {c}: {str(js.get('msg', ''))[:60]}"                    # OKX/Bitget/KuCoin
        if js.get("status") == "error":
            return f"status error: {str(js.get('err_msg', ''))[:60]}"            # HTX
        if "error" in js and js["error"]:
            return f"error: {str(js['error'])[:60]}"                             # Deribit
    return None


def f(x):
    try:
        value = float(x)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ storage
def load_state():
    st = read_json(STATE, {"series": {}, "liq_last_ts": None})
    if not isinstance(st, dict) or not isinstance(st.get("series"), dict):
        raise ValueError("invalid checkpoints; restore state rather than discarding it")
    return st


def save_state(st):
    atomic_json(STATE, st)


def day(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d")


def append_rows(rel_dir, rows, partition=month):
    """Monthly files by default; large forward-only books use daily files (partition=day)
    so an hourly commit rewrites a small file."""
    by_month = {}
    for row in rows:
        row = dict(row, code_version=CODE_VERSION, code_commit=os.environ.get("GITHUB_SHA", "local"), observed_at=int(time.time()*1000))
        by_month.setdefault(partition(row["t"]), []).append(row)
    def key(row):
        if rel_dir == "liq/orders":
            return (row["t"], row.get("posSide"), row.get("side"), row.get("sz_contracts"), row.get("bkPx"))
        return (row["t"], row.get("sym"))
    return sum(append_unique(os.path.join(BASE, "data", rel_dir, m + ".jsonl"), rs, key)
               for m, rs in by_month.items())


# ------------------------------------------------------------------ 1. history series
def binance_futures_data(name, ep, period, fields, ckpt):
    """Stage the entire backward fetch; failed pages never advance a checkpoint."""
    step = M5 if period == "5m" else H
    interval = SERIES_KIND.get(name, "interval") == "interval"
    # Interval rows (taker volume) exist once their interval closes; snapshot rows (ratios, OI)
    # describe their stamp and are published about five minutes after it.
    closed_before = NOW - (step if interval else M5)
    # Measured 2026-09-22: the taker endpoint filters endTime on the interval CLOSE, the
    # snapshot endpoints on the stamp. Paging with endTime = oldest - 1 therefore dropped one
    # taker row per 500-row page (17 x 5m gaps, 1 x 1h gap, each exactly 500 rows apart).
    page_overlap = step - 1 if interval else -1
    base = f"{BN}/futures/data/{ep}?symbol=BTCUSDT&period={period}&limit=500"
    out, end, calls, complete, err = {}, NOW, 0, False, None
    while calls < 40:
        js, err = get(f"{base}&endTime={end}", pause=3.1)
        calls += 1
        if err:
            # Only the measured old-history 400 is a boundary, and only in backfill. 2.2 appends the
            # venue's reason to 4xx errors ("HTTP 400 (binance code -1130 ...)"), so match the prefix.
            if not ckpt and out and err.startswith("HTTP 400"):
                err, complete = None, True
            break
        if not isinstance(js, list):
            err = "invalid history response shape"
            break
        if not js:
            if ckpt and (not out or min(out) > ckpt + step):
                err = "source boundary before checkpoint; run --backfill and review coverage gaps"
            else:
                complete = True
            break
        try:
            stamps = [int(x["timestamp"]) for x in js]
            if min(stamps) >= end and calls > 1:
                raise ValueError("pagination made no progress")
            for x, t in zip(js, stamps):
                if t % step:
                    raise ValueError("misaligned history timestamp")
                if t > closed_before or (ckpt and t <= ckpt):
                    continue
                values = {k: f(x.get(k)) for k in fields}
                if any(v is None for v in values.values()):
                    raise ValueError("missing/non-finite required history field")
                if t in out and out[t]["f"] != values:
                    raise ValueError("conflicting duplicate history row")
                out[t] = {"t": t, "f": values, "r": NOW}
            if ckpt and min(stamps) <= ckpt:
                complete = True
                break
            end = min(stamps) + page_overlap
        except (KeyError, TypeError, ValueError) as exc:
            err = str(exc)
            break
    if not complete:
        return [], err or "history page cap reached before checkpoint/boundary", calls
    if ckpt and not out and closed_before - ckpt >= 2 * step:
        return [], "history did not advance despite overdue intervals", calls
    ts = sorted(out)
    all_ts = ([ckpt] if ckpt else []) + ts
    missing = sum(max(0, (b-a)//step-1) for a,b in zip(all_ts, all_ts[1:]))
    if missing:
        RUN["errors"][f"gap_{name}"] = f"{missing} absent intervals in source response; retained rows, review report and retry --backfill"
    return [out[t] for t in ts], None, calls


def binance_funding(ckpt):
    """Settled funding (not the live predicted premiumIndex value -- Defect 45)."""
    rows, err = [], None
    for sym in ("BTCUSDT", "BTCUSDC"):
        start = (ckpt or {}).get(sym) or NOW - 90 * 86_400_000
        js, e = get(f"{BN}/fapi/v1/fundingRate?symbol={sym}&startTime={start + 1}&limit=1000", pause=0.5)
        if e:
            err = f"{sym}: {e}"
            continue
        for x in js:
            rows.append({"t": int(x["fundingTime"]), "sym": sym, "f": {"funding_settled_8h": f(x["fundingRate"]),
                         "mark": f(x.get("markPrice"))}, "r": NOW})
    return rows, err


def okx_backward(path, parse, ckpt, max_pages, pause=0.12):
    out, after, pages = {}, None, 0
    stop_at = ckpt or 0
    while pages < max_pages:
        js, err = get(OKX + path + (f"&after={after}" if after else ""), pause=pause)
        pages += 1
        if err:
            return [], err, pages
        data = js.get("data") if isinstance(js, dict) else None
        if not isinstance(data, list):
            return [], "invalid OKX response", pages
        if not data:
            return sorted(out.values(), key=lambda r: r["t"]), None, pages
        try:
            # Pagination uses all timestamps, even forming candles rejected by parse.
            stamps = [int(x[0] if isinstance(x, list) else x["fundingTime"]) for x in data]
            oldest = min(stamps)
            if after is not None and oldest >= after:
                return [], "OKX pagination made no progress", pages
            for item in data:
                row = parse(item)
                if row is not None and stop_at < row["t"] < NOW:
                    if any(v is None for v in row["f"].values()):
                        return [], "missing required OKX field", pages
                    out[row["t"]] = row
            if oldest <= stop_at:
                return sorted(out.values(), key=lambda r: r["t"]), None, pages
            after = oldest
        except (KeyError, ValueError, TypeError, IndexError) as exc:
            return [], f"invalid OKX row: {exc}", pages
    return [], "OKX page cap reached before checkpoint/boundary", pages


def okx_candle(rec):
    if len(rec) < 6:
        raise ValueError("OKX candle missing confirmation flag")
    if rec[-1] != "1":        # confirm flag: '0' = forming bar, dropped (M-01)
        return None
    return {"t": int(rec[0]), "f": {"o": f(rec[1]), "h": f(rec[2]), "l": f(rec[3]), "c": f(rec[4])}, "r": NOW}


def okx_funding_rec(rec):
    return {"t": int(rec["fundingTime"]), "f": {"funding_settled_8h": f(rec.get("realizedRate") or rec.get("fundingRate")),
            "funding_rate_field": f(rec.get("fundingRate"))}, "r": NOW}


def deribit_dvol(ckpt):
    # One-day requests avoid oversized windows; exact grid validation detects truncation.
    start = ckpt + H if ckpt else ((NOW - 120 * 86_400_000) // H) * H
    stop = NOW // H * H
    rows = {}
    while start < stop:
        end = min(start + 24 * H, stop)
        js, err = get(f"https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC"
                      f"&start_timestamp={start}&end_timestamp={end-1}&resolution=3600", pause=0.2)
        if err:
            return [], err
        try:
            page = {}
            for item in js["result"]["data"]:
                t = int(item[0])
                if start <= t < end:
                    values = dict(zip(("o", "h", "l", "c"), (f(v) for v in item[1:5])))
                    if len(values) != 4 or any(v is None for v in values.values()):
                        raise ValueError("invalid DVOL value")
                    page[t] = {"t": t, "f": values, "r": NOW}
            if set(page) != set(range(start, end, H)):
                raise ValueError("incomplete DVOL day; checkpoint retained")
            rows.update(page)
        except (KeyError, TypeError, ValueError) as exc:
            return [], f"DVOL: {exc}"
        start = end
    return [rows[t] for t in sorted(rows)], None


def isolated(name, fn):
    """One series' failure (including an unexpected response shape) never stops the others."""
    try:
        return fn()
    except Exception as e:
        RUN["series"][name] = {"added": 0, "err": f"{type(e).__name__}: {str(e)[:120]}"}
        return None


def collect_series(st):
    ck = st.setdefault("series", {})
    ratio = ["longAccount", "shortAccount", "longShortRatio"]
    specs = [("globalLongShortAccountRatio", ratio), ("topLongShortAccountRatio", ratio),
             ("topLongShortPositionRatio", ratio), ("openInterestHist", ["sumOpenInterest", "sumOpenInterestValue"]),
             ("takerlongshortRatio", ["buySellRatio", "buyVol", "sellVol"])]
    critical_ok = True
    for ep, fields in specs:
        for period in ("5m", "1h"):
            name = f"binance_{ep}_{period}"
            def one(name=name, ep=ep, period=period, fields=fields):
                rows, err, calls = binance_futures_data(name, ep, period, fields, None if BACKFILL else ck.get(name))
                added = append_rows(f"series/{name}", rows) if rows else 0
                if rows:
                    ck[name] = max(ck.get(name) or 0, rows[-1]["t"])
                RUN["series"][name] = {"added": added, "calls": calls, "err": err,
                                       "first": iso(rows[0]["t"]) if rows else None, "last": iso(ck[name]) if name in ck else None}
                return err is None
            ok = isolated(name, one)
            if ep in ("globalLongShortAccountRatio", "topLongShortAccountRatio", "topLongShortPositionRatio") and not ok:
                critical_ok = False

    name = "binance_funding_settled"
    def funding():
        rows, err = binance_funding(None if BACKFILL else ck.get(name))
        rows = [r for r in rows if r["t"] <= NOW and (BACKFILL or r["t"] > (ck.get(name) or {}).get(r["sym"], 0))]
        if any(r["f"]["funding_settled_8h"] is None for r in rows):
            rows, err = [], "missing/non-finite settled funding value"
        added = append_rows(f"series/{name}", rows) if rows else 0
        if rows:
            ck.setdefault(name, {})
            for r in rows:
                ck[name][r["sym"]] = max(ck[name].get(r["sym"], 0), r["t"])
        RUN["series"][name] = {"added": added, "err": err}
    isolated(name, funding)

    okx_specs = [
        ("okx_mark_1h", "/market/history-mark-price-candles?instId=BTC-USDT-SWAP&bar=1H&limit=100", okx_candle),
        ("okx_index_1h", "/market/history-index-candles?instId=BTC-USDT&bar=1H&limit=100", okx_candle),
        ("okx_funding_settled", "/public/funding-rate-history?instId=BTC-USDT-SWAP&limit=100", okx_funding_rec),
    ]
    for name, path, parse in okx_specs:
        def okx_one(name=name, path=path, parse=parse):
            ckpt = NOW - 120 * 86_400_000 if BACKFILL or name not in ck else ck.get(name)
            rows, err, pages = okx_backward(path, parse, ckpt, max_pages=40 if BACKFILL or name not in ck else 5)
            added = append_rows(f"series/{name}", rows) if rows else 0
            if rows:
                ck[name] = max(ck.get(name) or 0, rows[-1]["t"])
            RUN["series"][name] = {"added": added, "pages": pages, "err": err}
        isolated(name, okx_one)

    name = "okx_acct_ratio_1h"
    def okx_ratio():
        js, err = get(f"{OKX}/rubik/stat/contracts/long-short-account-ratio?ccy=BTC&period=1H")
        rows = []
        if js:
            for t, v in js.get("data", []):
                t = int(t)
                # Snapshot stamped t (published before t+1h, measured); t+1h cut kept as the
                # conservative retrieval rule so each stored value is final.
                if t + H <= NOW and (BACKFILL or t > (ck.get(name) or 0)):
                    rows.append({"t": t, "f": {"longShortRatio": f(v)}, "r": NOW})
            rows.sort(key=lambda r: r["t"])
        if any(r["f"]["longShortRatio"] is None for r in rows):
            rows, err = [], "missing/non-finite account ratio"
        added = append_rows(f"series/{name}", rows) if rows else 0
        if rows:
            ck[name] = max(ck.get(name) or 0, rows[-1]["t"])
        RUN["series"][name] = {"added": added, "err": err}
    isolated(name, okx_ratio)

    name = "deribit_dvol_1h"
    def dvol():
        rows, err = deribit_dvol(None if BACKFILL else ck.get(name))
        added = append_rows(f"series/{name}", rows) if rows else 0
        if rows:
            ck[name] = max(ck.get(name) or 0, rows[-1]["t"])
        RUN["series"][name] = {"added": added, "err": err}
    isolated(name, dvol)
    return critical_ok


# ------------------------------------------------------------------ 2. forced flow
def liq_key(d):
    return f"{d['ts']}|{d.get('posSide')}|{d.get('side')}|{d.get('sz')}|{d.get('bkPx')}"


def collect_liq(st):
    """Page the OKX feed back to the last stored order minus a 6h re-capture window, so
    orders that appear late are caught and stamped with the run that first saw them.
    Once a day (00Z run) and on backfill, page to the boundary and record it (O14)."""
    seen_path = os.path.join(BASE, "state", "liq_recent_keys.json")
    seen = set(read_json(seen_path, []))
    last = st.get("liq_last_ts")
    probe = BACKFILL or dt.datetime.fromtimestamp(NOW / 1000, dt.timezone.utc).hour == 0 or last is None
    floor = 0 if probe else (last - 6 * H)
    url0 = f"{OKX}/public/liquidation-orders?instType=SWAP&uly=BTC-USDT&instId=BTC-USDT-SWAP&state=filled&limit=100"
    after, pages, err, got, oldest, newest = None, 0, None, [], None, None
    max_pages = 1500 if probe else 60
    while pages < max_pages:
        js, err = get(url0 + (f"&after={after}" if after else ""), pause=0.12)
        pages += 1
        if err:
            break
        det = [d for blk in (js.get("data") or []) for d in (blk.get("details") or [])]
        if not det:
            break
        ts = [int(d["ts"]) for d in det]
        got += det
        page_oldest = min(ts)
        if oldest is not None and page_oldest >= oldest:
            # A page holding only the boundary millisecond: step strictly past it.
            if after == oldest:
                err = "liquidation pagination made no progress"
                break
            after = oldest
            continue
        oldest = page_oldest if oldest is None else min(oldest, page_oldest)
        newest = max(ts) if newest is None else max(newest, max(ts))
        if page_oldest <= floor:
            break
        # `after` returns records strictly earlier than it. ~2% of stored timestamps carry two
        # orders (measured), so paging from the oldest ts itself could drop the second order of
        # a pair split across pages. Re-request the boundary millisecond; keys deduplicate it.
        after = page_oldest + 1
    if pages >= max_pages and (oldest is None or oldest > floor):
        err = err or "liquidation page cap reached before coverage boundary"
    if err:
        RUN["liq"] = {"pages": pages, "new": 0, "err": err, "probe": probe}
        return
    new = []
    for d in got:
        size, price = f(d.get("sz")), f(d.get("bkPx"))
        if size is None or size < 0 or price is None or price <= 0:
            raise ValueError("invalid liquidation size or price")
        k = liq_key(d)
        if k in seen:           # also drops the boundary order returned on two overlapping pages
            continue
        seen.add(k)
        new.append({"t": int(d["ts"]), "posSide": d.get("posSide"), "side": d.get("side"),
                    "sz_contracts": f(d.get("sz")), "btc": round((f(d.get("sz")) or 0) * 0.01, 6),
                    "bkPx": f(d.get("bkPx")), "first_seen": NOW, "bf": BACKFILL})
    added = append_rows("liq/orders", sorted(new, key=lambda r: r["t"])) if new else 0
    if newest:
        st["liq_last_ts"] = max(newest, last or 0)
    # keep keys for the re-capture window plus margin; older keys cannot reappear in a 6h window
    keep_after = (st.get("liq_last_ts") or NOW) - 30 * H
    seen = {k for k in seen if int(k.split("|")[0]) >= keep_after}
    os.makedirs(os.path.dirname(seen_path), exist_ok=True)
    atomic_json(seen_path, sorted(seen))
    RUN["liq"] = {"pages": pages, "orders_returned": len(got), "new": added, "err": err, "probe": probe,
                  "window_oldest": iso(oldest) if oldest else None, "window_newest": iso(newest) if newest else None,
                  "window_oldest_ms": oldest, "window_newest_ms": newest}
    if probe and oldest and not err:
        append_rows("liq/boundary", [{"t": NOW, "oldest": oldest, "oldest_iso": iso(oldest), "pages": pages,
                                      "retention_days": round((NOW - oldest) / 86_400_000, 2),
                                      "hit_page_cap": pages >= max_pages}])


# ------------------------------------------------------------------ 3. snapshot
def snap_source(name, fn):
    try:
        v = fn()
        if isinstance(v, tuple):          # (None, err)
            return {"st": "error", "err": v[1]}
        if "oi_btc" in v and (f(v["oi_btc"]) is None or v["oi_btc"] < 0):
            raise ValueError("missing/invalid normalized OI")
        v["st"] = "ok"
        v["t_ret"] = int(time.time() * 1000)
        return v
    except Exception as e:
        return {"st": "error", "err": type(e).__name__ + ": " + str(e)[:80]}


def need(js_err):
    js, err = js_err
    if err:
        raise RuntimeError(err)
    return js


def depth_bands(bids, asks, mult=1.0):
    bids = [(f(p), f(q) * mult) for p, q, *_ in bids]
    asks = [(f(p), f(q) * mult) for p, q, *_ in asks]
    bb, ba = max(p for p, _ in bids), min(p for p, _ in asks)
    mid = (bb + ba) / 2
    span_bid, span_ask = mid - min(p for p, _ in bids), max(p for p, _ in asks) - mid
    out = {"mid": mid, "best_bid": bb, "best_ask": ba, "span_bid_pts": round(span_bid, 1), "span_ask_pts": round(span_ask, 1)}
    for pts in (25, 50, 100, 200):
        out[f"bid_btc_{pts}"] = round(sum(q for p, q in bids if mid - p <= pts), 3) if span_bid >= pts else None
        out[f"ask_btc_{pts}"] = round(sum(q for p, q in asks if p - mid <= pts), 3) if span_ask >= pts else None
    return out                             # None = the book returned does not span the band (incomplete, not zero)


def snapshot():
    S = {}

    def bn_premium(sym, dapi=False):
        js = need(get(f"{BN}/{'dapi' if dapi else 'fapi'}/v1/premiumIndex?symbol={sym}"))
        x = js[0] if isinstance(js, list) else js
        return {"t_event": x["time"], "mark": f(x["markPrice"]), "index": f(x["indexPrice"]),
                "funding_live_predicted_8h": f(x["lastFundingRate"]), "interest_8h": f(x["interestRate"]),
                "next_settle": x["nextFundingTime"]}

    S["binance_usdt_prem"] = snap_source("", lambda: bn_premium("BTCUSDT"))
    S["binance_usdc_prem"] = snap_source("", lambda: bn_premium("BTCUSDC"))
    S["binance_coinm_prem"] = snap_source("", lambda: bn_premium("BTCUSD_PERP", dapi=True))

    oi = {}

    def bn_oi(sym):
        js = need(get(f"{BN}/fapi/v1/openInterest?symbol={sym}"))
        return {"t_event": js["time"], "raw": f(js["openInterest"]), "unit": "BTC", "oi_btc": f(js["openInterest"])}

    def bn_coinm():
        js = need(get(f"{BN}/dapi/v1/openInterest?symbol=BTCUSD_PERP"))
        mk = S["binance_coinm_prem"].get("mark")
        c = f(js["openInterest"])
        return {"t_event": js["time"], "raw": c, "unit": "contracts x $100, inverse", "mark": mk,
                "oi_btc": round(c * 100 / mk, 3) if mk else None, "inverse": True}

    oi["binance_BTCUSDT"] = snap_source("", lambda: bn_oi("BTCUSDT"))
    oi["binance_BTCUSDC"] = snap_source("", lambda: bn_oi("BTCUSDC"))
    oi["binance_BTCUSD_PERP"] = snap_source("", bn_coinm)

    def hyper():
        js = need(get("https://api.hyperliquid.xyz/info", body={"type": "metaAndAssetCtxs"}))
        uni = js[0]["universe"]
        i = next(k for k, u in enumerate(uni) if u["name"] == "BTC")
        c = js[1][i]
        return {"raw": f(c["openInterest"]), "unit": "BTC", "oi_btc": f(c["openInterest"]), "mark": f(c["markPx"]),
                "oracle": f(c["oraclePx"]), "cash_rate_1h": f(c["funding"]), "premium": f(c["premium"])}
    oi["hyperliquid"] = snap_source("", hyper)

    def hl_predicted():
        js = need(get("https://api.hyperliquid.xyz/info", body={"type": "predictedFundings"}))
        row = next(r for r in js if r[0] == "BTC")
        return {"venues": {v: {"rate": f(d.get("fundingRate")), "next": d.get("nextFundingTime"),
                               "interval_h": d.get("fundingIntervalHours")} for v, d in row[1] if d}}
    S["hl_predicted_fundings"] = snap_source("", hl_predicted)

    def bitget(sym, pt):
        js = need(get(f"https://api.bitget.com/api/v2/mix/market/open-interest?symbol={sym}&productType={pt}"))
        d = js["data"]
        amt = f(d["openInterestList"][0]["size"])
        out = {"t_event": int(d.get("ts") or js.get("requestTime") or 0), "raw": amt,
               "unit": "base coin (BTC)", "oi_btc": amt}
        fr = get(f"https://api.bitget.com/api/v2/mix/market/current-fund-rate?symbol={sym}&productType={pt}")[0]
        if fr and fr.get("data"):
            out["funding_live_predicted"] = f(fr["data"][0].get("fundingRate"))
            out["funding_interval_h"] = f(fr["data"][0].get("fundingRateInterval"))
        return out
    oi["bitget_USDT"] = snap_source("", lambda: bitget("BTCUSDT", "USDT-FUTURES"))
    # bitget_COIN retired 2026-09-23: Bitget answers 40309 "The symbol has been removed" for the
    # BTCUSD coin-margined perp; only dated coin futures (e.g. BTCUSDU26) remain listed.
    oi["bitget_USDC"] = snap_source("", lambda: bitget("BTCPERP", "USDC-FUTURES"))

    def okx_oi(inst):
        js = need(get(f"{OKX}/public/open-interest?instId={inst}"))
        d = js["data"][0]
        out = {"t_event": int(d["ts"]), "raw": f(d["oi"]), "oi_ccy": f(d.get("oiCcy")), "oi_usd": f(d.get("oiUsd")),
               "unit": "contracts; oiCcy is BTC", "oi_btc": f(d.get("oiCcy")), "inverse": inst.endswith("USD-SWAP")}
        fr = get(f"{OKX}/public/funding-rate?instId={inst}")[0]
        if fr and fr.get("data"):
            x = fr["data"][0]
            out["funding_current_period"] = f(x.get("fundingRate"))
            out["funding_method"] = x.get("method")
            out["next_settle"] = x.get("fundingTime")
        return out
    oi["okx_BTC-USDT-SWAP"] = snap_source("", lambda: okx_oi("BTC-USDT-SWAP"))
    oi["okx_BTC-USD-SWAP"] = snap_source("", lambda: okx_oi("BTC-USD-SWAP"))

    def gate():
        d = need(get("https://api.gateio.ws/api/v4/futures/usdt/contracts/BTC_USDT"))
        ps, qm = f(d["position_size"]), f(d["quanto_multiplier"])
        return {"raw": ps, "unit": "contracts x quanto_multiplier", "oi_btc": round(ps * qm, 3), "mark": f(d["mark_price"]),
                "index": f(d.get("index_price")), "funding_live_predicted": f(d.get("funding_rate")),
                "funding_interval_s": d.get("funding_interval"), "next_settle": d.get("funding_next_apply")}
    oi["gate"] = snap_source("", gate)

    def htx():
        js = need(get("https://api.hbdm.com/linear-swap-api/v1/swap_open_interest?contract_code=BTC-USDT"))
        d = js["data"][0]
        out = {"t_event": js.get("ts"), "raw": f(d["amount"]), "unit": "BTC", "oi_btc": f(d["amount"])}
        fr = get("https://api.hbdm.com/linear-swap-api/v1/swap_funding_rate?contract_code=BTC-USDT")[0]
        if fr and fr.get("data"):
            out["funding_live_predicted"] = f(fr["data"].get("funding_rate"))
        return out
    oi["htx"] = snap_source("", htx)

    def deribit():
        r = need(get("https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-PERPETUAL"))["result"]
        mk = f(r["mark_price"])
        return {"t_event": r["timestamp"], "raw": f(r["open_interest"]), "unit": "USD, inverse", "mark": mk,
                "index": f(r["index_price"]), "oi_btc": round(f(r["open_interest"]) / mk, 3), "inverse": True,
                "funding_current_live": f(r.get("current_funding")), "funding_8h_trailing": f(r.get("funding_8h"))}
    oi["deribit"] = snap_source("", deribit)

    def kucoin():
        d = need(get("https://api-futures.kucoin.com/api/v1/contracts/XBTUSDTM"))["data"]
        return {"raw": f(d["openInterest"]), "unit": "lots x 0.001 BTC", "oi_btc": round(f(d["openInterest"]) * 0.001, 3),
                "mark": f(d.get("markPrice")), "funding_current": f(d.get("fundingFeeRate")),
                "funding_predicted": f(d.get("predictedFundingFeeRate")), "funding_granularity_ms": d.get("fundingRateGranularity")}
    oi["kucoin"] = snap_source("", kucoin)

    def bingx():
        d = need(get("https://open-api.bingx.com/openApi/swap/v2/quote/openInterest?symbol=BTC-USDT"))["data"]
        p = need(get("https://open-api.bingx.com/openApi/swap/v2/quote/premiumIndex?symbol=BTC-USDT"))["data"]
        mk = f(p["markPrice"])
        return {"raw": f(d["openInterest"]), "unit": "USD", "mark": mk, "oi_btc": round(f(d["openInterest"]) / mk, 3),
                "funding_live_predicted": f(p.get("lastFundingRate")), "default_dropped": True}
    oi["bingx"] = snap_source("", bingx)

    def kraken():
        js = need(get("https://futures.kraken.com/derivatives/api/v3/tickers"))
        t = next(x for x in js["tickers"] if x.get("symbol") == "PF_XBTUSD")
        return {"raw": f(t.get("openInterest")), "unit": "BTC", "oi_btc": f(t.get("openInterest")),
                "mark": f(t.get("markPrice")), "funding_unreliable": f(t.get("fundingRate"))}
    oi["kraken"] = snap_source("", kraken)

    # bitmex retired 2026-09-23: XBTUSD and XBTUSDT settled Sep 16 (OI 0) and no XBT perpetual is
    # Open in /instrument/active (XBT_USDT Delisted; XBT_USDC Unlisted). Re-add if one relists.


    def dydx():
        m = need(get("https://indexer.dydx.trade/v4/perpetualMarkets?ticker=BTC-USD"))["markets"]["BTC-USD"]
        return {"raw": f(m["openInterest"]), "unit": "BTC", "oi_btc": f(m["openInterest"]),
                "oracle": f(m.get("oraclePrice")), "funding_next_1h": f(m.get("nextFundingRate"))}
    oi["dydx"] = snap_source("", dydx)

    def backpack():
        js = need(get("https://api.backpack.exchange/api/v1/openInterest?symbol=BTC_USDC_PERP"))
        x = js[0] if isinstance(js, list) else js
        return {"raw": f(x.get("openInterest")), "unit": "BTC", "oi_btc": f(x.get("openInterest"))}
    oi["backpack"] = snap_source("", backpack)

    def paradex():
        r = need(get("https://api.prod.paradex.trade/v1/markets/summary?market=BTC-USD-PERP"))["results"][0]
        return {"raw": f(r.get("open_interest")), "unit": "BTC", "oi_btc": f(r.get("open_interest")),
                "mark": f(r.get("mark_price")), "funding_current": f(r.get("funding_rate"))}
    oi["paradex"] = snap_source("", paradex)
    S["oi"] = oi

    def bn_depth():
        js = need(get(f"{BN}/fapi/v1/depth?symbol=BTCUSDT&limit=1000"))
        out = depth_bands(js["bids"], js["asks"])
        out["t_event"] = js.get("E") or js.get("T")
        return out
    S["depth_binance_usdt"] = snap_source("", bn_depth)

    def okx_depth():
        d = need(get(f"{OKX}/market/books?instId=BTC-USDT-SWAP&sz=400"))["data"][0]
        out = depth_bands(d["bids"], d["asks"], mult=0.01)
        out["t_event"] = int(d["ts"])
        return out
    S["depth_okx_usdt_swap"] = snap_source("", okx_depth)

    def cb_premium_parts():
        cb = need(get("https://api.exchange.coinbase.com/products/BTC-USD/ticker"))
        ut = need(get("https://api.exchange.coinbase.com/products/USDT-USD/ticker"))
        ok = need(get(f"{OKX}/market/ticker?instId=BTC-USDT"))["data"][0]
        bs = need(get(f"{BN}/api/v3/ticker/price?symbol=BTCUSDT"))
        return {"coinbase_btcusd": f(cb["price"]), "coinbase_btcusd_time": cb.get("time"),
                "coinbase_usdtusd": f(ut["price"]), "okx_spot_btcusdt": f(ok["last"]), "okx_spot_ts": int(ok["ts"]),
                "binance_spot_btcusdt": f(bs["price"])}
    S["premium_parts"] = snap_source("", cb_premium_parts)

    def bitfinex():
        lo = need(get("https://api-pub.bitfinex.com/v2/stats1/pos.size:1m:tBTCUSD:long/last"))
        sh = need(get("https://api-pub.bitfinex.com/v2/stats1/pos.size:1m:tBTCUSD:short/last"))
        return {"long_btc": f(lo[1]), "long_t": lo[0], "short_btc": f(sh[1]), "short_t": sh[0]}
    S["bitfinex_margin"] = snap_source("", bitfinex)
    return S


# ------------------------------------------------------------------ 4. forward-only books
DERIBIT = "https://www.deribit.com/api/v2/public"
HL_INFO = "https://api.hyperliquid.xyz/info"
HL_LEADERBOARD = "https://stats-data.hyperliquid.xyz/Mainnet/leaderboard"
HL_TOP_N = 200
HL_TOP_REFRESH = 6 * H
HL_BUDGET_S = 300           # a normal map takes ~70 s (200 calls at ~0.33 s)
HL_REQUEST_TIMEOUT_S = 10
HL_RATE_LIMIT_BACKOFF_S = 5


OPTION_NAME = re.compile(r"BTC-\d{1,2}[A-Z]{3}\d{2}-\d+(\.\d+)?-[CP]")
FORWARD_MAX_INVALID = 0.05          # more than 5% invalid option rows: the snapshot is not stored


def positive(x):
    v = f(x)
    return v if v is not None and v > 0 else None


def collect_deribit_options():
    """Per-strike BTC option open interest and mark IV (runbook F requirement 50; with mark IV
    it also preserves the published surface requirement 49 would otherwise reconstruct).
    One compact row per run in a daily file; instruments with zero OI are omitted and counted.
    An option with OI but a malformed name, missing mark IV or missing underlying is never stored
    as valid: it is excluded, named in `excluded`, and the snapshot is marked degraded."""
    js = need(get(f"{DERIBIT}/get_book_summary_by_currency?currency=BTC&kind=option", pause=0.2))
    res = js.get("result") if isinstance(js, dict) else None
    if not isinstance(res, list) or not res or not all(isinstance(x, dict) for x in res):
        raise ValueError("empty or malformed Deribit option summary")
    rows, underlying, zero, excluded = [], {}, 0, []
    for x in res:
        name, oi = x.get("instrument_name"), f(x.get("open_interest"))
        if not isinstance(name, str) or not OPTION_NAME.fullmatch(name):
            excluded.append([str(name)[:40], "instrument name"])
            continue
        if oi is None or oi < 0:
            excluded.append([name, "open_interest"])
            continue
        if oi == 0:
            zero += 1
            continue
        iv, u = positive(x.get("mark_iv")), positive(x.get("underlying_price"))
        if iv is None or u is None:
            excluded.append([name, "mark_iv" if iv is None else "underlying_price"])
            continue
        rows.append([name, oi, iv])
        underlying.setdefault(name.split("-")[1], u)
    with_oi = len(rows) + len(excluded)
    if not rows or len(excluded) > FORWARD_MAX_INVALID * max(with_oi, 1):
        raise ValueError(f"{len(excluded)} of {with_oi} option rows invalid; snapshot not stored "
                         f"(first: {excluded[:3]})")
    rows.sort()
    status = "degraded" if excluded else "complete"
    t_event = max(int(f(x.get("creation_timestamp")) or 0) for x in res)
    out = {"t": NOW, "t_event": t_event, "status": status,
           "unit": "open_interest in BTC (contracts of 1 BTC); mark_iv in % vol",
           "fields": ["instrument", "open_interest_btc", "mark_iv"], "rows": rows,
           "underlying": underlying, "instruments": len(res), "zero_oi_omitted": zero, "excluded": excluded}
    added = append_rows("options/deribit_btc", [out], partition=day)
    return {"added": added, "status": status, "instruments": len(res), "with_oi": len(rows),
            "excluded": len(excluded), "total_oi_btc": round(sum(r[1] for r in rows), 1),
            "err": f"degraded: {len(excluded)} option rows excluded" if excluded else None}


def hl_top_accounts(st, deadline=None):
    """Top accounts by account value, refreshed every six hours (the leaderboard is ~40 MB)."""
    cache = st.get("hl_top") or {}
    if cache.get("t") and NOW - cache["t"] < HL_TOP_REFRESH and len(cache.get("addresses", [])) >= HL_TOP_N // 2:
        return cache
    js = need(get(HL_LEADERBOARD, tries=2, timeout=60, deadline=deadline))
    rows = js.get("leaderboardRows") if isinstance(js, dict) else None
    if not isinstance(rows, list) or len(rows) < HL_TOP_N:
        raise ValueError("Hyperliquid leaderboard missing or short")
    ranked = sorted(((f(r.get("accountValue")) or 0.0, r.get("ethAddress")) for r in rows
                     if isinstance(r.get("ethAddress"), str)), reverse=True)[:HL_TOP_N]
    cache = {"t": NOW, "addresses": [a for _, a in ranked], "min_account_value": round(ranked[-1][0], 2),
             "rank_basis": "leaderboard accountValue, descending"}
    st["hl_top"] = cache
    return cache


HL_LEVERAGE_TYPES = ("cross", "isolated")


def hl_account(js):
    """Validate one clearinghouseState response. Returns (account_value, btc_positions) or raises.
    `{}` or any response without the documented structure is a failed account, never an empty one."""
    if not isinstance(js, dict):
        raise ValueError("not an object")
    summary, assets = js.get("marginSummary"), js.get("assetPositions")
    if not isinstance(summary, dict) or not isinstance(assets, list):
        raise ValueError("missing marginSummary/assetPositions")
    acct = f(summary.get("accountValue"))
    if acct is None or acct < 0:
        raise ValueError("invalid accountValue")
    positions = []
    for ap in assets:
        pos = ap.get("position") if isinstance(ap, dict) else None
        if not isinstance(pos, dict) or not isinstance(pos.get("coin"), str):
            raise ValueError("malformed asset position")
        if pos["coin"] != "BTC":
            continue
        lev = pos.get("leverage") if isinstance(pos.get("leverage"), dict) else {}
        szi, entry, value = f(pos.get("szi")), positive(pos.get("entryPx")), f(pos.get("positionValue"))
        liq = pos.get("liquidationPx")
        liq_px = None if liq is None else positive(liq)     # null is documented: no liquidation price
        if (not szi or entry is None or value is None or lev.get("type") not in HL_LEVERAGE_TYPES
                or positive(lev.get("value")) is None or (liq is not None and liq_px is None)):
            raise ValueError("malformed BTC position")
        positions.append([acct, szi, entry, liq_px, lev["type"], f(lev["value"]), value,
                          f(pos.get("unrealizedPnl")), f(pos.get("marginUsed"))])
    return acct, positions


def collect_hl_positions(st):
    """Hyperliquid position map: BTC positions of the top accounts with liquidation price and
    leverage type (runbook F requirement 50). Current-only at the source; forward-only here.
    Any failed or malformed account marks the snapshot degraded and names the address; half or
    more failing means the map is not stored."""
    started = time.time()
    deadline = started + HL_BUDGET_S
    top = hl_top_accounts(st, deadline)
    addresses = top["addresses"]
    reject_at = (len(addresses) + 1) // 2          # this many failures means the map is not stored
    positions, failed, stopped, rate_limited = [], [], None, 0
    for i, addr in enumerate(addresses):
        if len(failed) >= reject_at:
            stopped = "rejection inevitable"
        elif time.time() >= deadline:
            stopped = "deadline"
        if stopped:
            failed.extend([a, f"not attempted: {stopped}"] for a in addresses[i:])
            break
        js, err = get(HL_INFO, body={"type": "clearinghouseState", "user": addr}, tries=2, pause=0.05,
                      timeout=HL_REQUEST_TIMEOUT_S, deadline=deadline)
        if err and err.startswith("HTTP 429"):
            # Rate limited (seen live: 3 of 200 on a busy IP). Back off once, inside the budget.
            rate_limited += 1
            time.sleep(min(HL_RATE_LIMIT_BACKOFF_S, max(0.0, deadline - time.time())))
            js, err = get(HL_INFO, body={"type": "clearinghouseState", "user": addr}, tries=1,
                          timeout=HL_REQUEST_TIMEOUT_S, deadline=deadline)
        try:
            if err:
                raise ValueError(err)
            _, found = hl_account(js)
        except (ValueError, TypeError) as exc:
            failed.append([addr, str(exc)[:60]])
            continue
        positions.extend([addr] + p for p in found)
    elapsed = round(time.time() - started, 1)
    attempted = len(addresses) - sum(1 for _, why in failed if why.startswith("not attempted"))
    if len(failed) >= reject_at:
        raise RuntimeError(f"{len(failed)}/{len(addresses)} accounts failed or not attempted "
                           f"({attempted} attempted in {elapsed}s{'; stopped: ' + stopped if stopped else ''}); "
                           f"map not stored (first: {failed[:2]})")
    status = "degraded" if failed else "complete"
    out = {"t": NOW, "status": status, "accounts_ranked": len(addresses), "accounts_failed": len(failed),
           "failed": failed, "stopped": stopped, "elapsed_s": elapsed, "rate_limited": rate_limited, "ranked_at": top["t"], "min_account_value": top["min_account_value"],
           "rank_basis": top["rank_basis"],
           "fields": ["address", "account_value", "szi_btc", "entry_px", "liquidation_px", "leverage_type",
                      "leverage", "position_value", "unrealized_pnl", "margin_used"],
           "positions": positions}
    added = append_rows("hl_positions/btc", [out], partition=day)
    return {"added": added, "status": status, "positions": len(positions), "accounts_failed": len(failed),
            "stopped": stopped, "elapsed_s": elapsed, "rate_limited": rate_limited,
            "err": (f"degraded: {len(failed)}/{len(addresses)} accounts failed, malformed or not attempted"
                    + (f" (stopped: {stopped})" if stopped else "")) if failed else None}


def collect_forward(st):
    RUN["forward"] = {}
    for name, fn in (("deribit_options", collect_deribit_options), ("hl_positions", lambda: collect_hl_positions(st))):
        try:
            RUN["forward"][name] = fn()
        except Exception as e:
            RUN["forward"][name] = {"added": 0, "status": "failed", "err": f"{type(e).__name__}: {str(e)[:160]}"}


# ------------------------------------------------------------------ 5. registration clock
def register():
    new, errors = register_content(BASE, NOW)
    RUN["registered_new"] = new
    if errors:
        RUN["errors"]["register"] = "; ".join(errors)
        if "--register-only" in sys.argv:
            raise ValueError("; ".join(errors))


# ------------------------------------------------------------------ main
def main():
    if "--register-only" in sys.argv:          # forecast intake: stamp now, collect nothing
        register()
        if "--require" in sys.argv:
            required = sys.argv[sys.argv.index("--require") + 1]
            manifest = read_json(os.path.join(BASE, "state", "forecast_manifest.json"), {})
            entry = next((v for v in manifest.values() if v["source"] == required), None)
            if entry is None:
                raise ValueError("requested forecast was not frozen")
            from schema import ms
            frozen = read_json(os.path.join(BASE, entry["frozen"]))
            if entry["registered"] >= ms(frozen["start_utc"]):
                raise ValueError("registration missed start; choose a future start and new ID")
        for k in RUN.get("registered_new", []):
            print(f"registered {k} at {iso(NOW)}")
        if not RUN.get("registered_new"):
            print("nothing new to register")
        return
    try:
        register()
    except Exception as e:
        RUN["errors"]["register"] = type(e).__name__ + ": " + str(e)[:120]
    st = load_state()
    critical_ok = True
    try:
        critical_ok = collect_series(st)
    except Exception as e:
        RUN["errors"]["series"] = type(e).__name__ + ": " + str(e)[:120]
        critical_ok = False
    save_state(st)
    try:
        collect_liq(st)
    except Exception as e:
        RUN["errors"]["liq"] = type(e).__name__ + ": " + str(e)[:120]
    save_state(st)
    if not BACKFILL:
        try:
            S = snapshot()
            S["t"] = NOW
            S["code_version"] = CODE_VERSION
            S["runner"] = RUN["runner"]
            append_rows("snap", [S])
            books = S["oi"]
            RUN["snap"] = {"books_ok": sum(1 for v in books.values() if v.get("st") == "ok"), "books": len(books),
                           "failed": {k: v.get("err") for k, v in books.items() if v.get("st") != "ok"},
                           "other_failed": {k: v.get("err") for k, v in S.items()
                                            if isinstance(v, dict) and v.get("st") == "error"}}
        except Exception as e:
            RUN["errors"]["snap"] = type(e).__name__ + ": " + str(e)[:120]
        collect_forward(st)
        save_state(st)
    RUN["elapsed_s"] = round(time.time() - NOW / 1000, 1)
    RUN["critical_ok"] = critical_ok
    RUN["t"] = NOW
    append_rows("runs", [RUN])
    added = sum((v.get("added") or 0) for v in RUN["series"].values())
    print(f"{iso(NOW)} {CODE_VERSION} mode={RUN['mode']} series_rows+={added} liq_new={RUN['liq'].get('new')} "
          f"books={RUN['snap'].get('books_ok')}/{RUN['snap'].get('books')} "
          f"forward={ {k: v.get('err') or v.get('added') for k, v in RUN.get('forward', {}).items()} } critical_ok={critical_ok} "
          f"elapsed={RUN['elapsed_s']}s")
    if not critical_ok:
        sys.exit(2)


if __name__ == "__main__":
    main()
