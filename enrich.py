"""Optional research enrichment (collector 2.7), run after the forward books.

Nothing here is on the critical path: it runs last, inside its own stage limit, every source is
isolated, and a failure is recorded in the run record without affecting what was already saved.

1. One-minute price bars (schema.PRICE_SERIES), checkpointed like the history series: every run
   stores the closed minutes since the last stored one (at most MAX_PAGES pages per series per
   run) as ONE batch record in data/prices/<name>/YYYY-MM.jsonl: {"t": first bar, "t_last": last
   bar, "fields": [...], "bars": [[t, o, h, l, c, ...], ...]}. A bar is stored only after it closes;
   it is available no earlier than the batch's observed_at. Readers deduplicate bars by open time,
   first observation wins (research.Ctx.prices).
2. OKX insurance fund for the BTC-USDT swap family: the latest balance row each run, plus every
   liquidation deposit, bankruptcy loss and ADL row since the last one stored. Rows are stored as
   OKX returns them (type, amt, balance, adlType, decRate, maxBal ...). OKX publishes a
   regular_update row about once a minute; only the latest one per run is kept.
"""
SERIES_URL = {
    "binance_klines_1m_BTCUSDT_perp": "/fapi/v1/klines?symbol=BTCUSDT&interval=1m",
    "binance_markklines_1m_BTCUSDT_perp": "/fapi/v1/markPriceKlines?symbol=BTCUSDT&interval=1m",
    "binance_klines_1m_BTCUSDT_spot": "/api/v3/klines?symbol=BTCUSDT&interval=1m",
    "binance_klines_1m_ETHUSDT_perp": "/fapi/v1/klines?symbol=ETHUSDT&interval=1m",
    "binance_klines_1m_SOLUSDT_perp": "/fapi/v1/klines?symbol=SOLUSDT&interval=1m",
}
MAX_PAGES = 2               # 3000 minutes per series per run: two days of catch-up after an outage
FIRST_RUN_MINUTES = 1500
BAR_FIELDS = ["t", "o", "h", "l", "c", "v", "qv", "n", "tbv", "tbqv"]
MARK_FIELDS = ["t", "o", "h", "l", "c"]
INSURANCE_TYPES = ("liquidation_balance_deposit", "bankruptcy_loss", "adl")
MINUTE = 60_000


def parse_kline(C, k, mark):
    """Binance kline row -> stored fields; None when malformed (the page is then rejected)."""
    try:
        t = int(k[0])
        o, h, l, c = (C.f(k[i]) for i in (1, 2, 3, 4))
        if None in (o, h, l, c) or min(o, h, l, c) <= 0 or h < max(o, c, l) or l > min(o, c):
            return None
        if mark:
            return t, {"o": o, "h": h, "l": l, "c": c}
        vals = {"v": C.f(k[5]), "qv": C.f(k[7]), "n": int(k[8]), "tbv": C.f(k[9]), "tbqv": C.f(k[10])}
        if any(v is None or v < 0 for v in vals.values()):
            return None
        return t, dict(o=o, h=h, l=l, c=c, **vals)
    except (TypeError, ValueError, IndexError):
        return None


def klines(C, st, name):
    ck = st.setdefault("series", {})
    last = ck.get(name)
    closed_before = C.NOW // MINUTE * MINUTE           # a bar opening at T is closed once T + 1m <= NOW
    start = (last + MINUTE) if last else closed_before - FIRST_RUN_MINUTES * MINUTE
    rows, pages, err = [], 0, None
    mark = "markklines" in name
    while start < closed_before and pages < MAX_PAGES:
        js, err = C.get(f"{C.BN}{SERIES_URL[name]}&startTime={start}&endTime={closed_before - 1}&limit=1500",
                        pause=0.2)
        pages += 1
        if err:
            break
        if not isinstance(js, list):
            err = "not a list"
            break
        page = []
        for k in js:
            parsed = parse_kline(C, k, mark)
            if parsed is None:
                err = "malformed kline"
                break
            t, fields = parsed
            if t + MINUTE <= closed_before and t >= start:
                page.append([t] + [fields[k] for k in (MARK_FIELDS if mark else BAR_FIELDS)[1:]])
        if err or not page:
            break
        stamps = [r[0] for r in page]
        if stamps != sorted(set(stamps)):
            err = "unordered or duplicate klines"
            break
        rows.extend(page)
        start = stamps[-1] + MINUTE
    added = 0
    if rows:
        from schema import PRICE_SERIES
        instrument, price_type, _ = PRICE_SERIES[name]
        batch = {"t": rows[0][0], "t_last": rows[-1][0], "schema": "price_bars/1", "series": name,
                 "instrument": instrument, "price_type": price_type, "interval_ms": MINUTE,
                 "fields": MARK_FIELDS if mark else BAR_FIELDS, "bars": rows, "n": len(rows), "r": C.NOW}
        added = len(rows) if C.append_rows(f"prices/{name}", [batch], key=lambda r: (r["t"], r["t_last"])) else 0
        ck[name] = max(last or 0, rows[-1][0])
    gaps = sum(1 for a, b in zip(rows, rows[1:]) if b[0] - a[0] != MINUTE)
    behind = (closed_before - (ck.get(name) or closed_before) - MINUTE) // MINUTE if ck.get(name) else None
    return {"added": added, "pages": pages, "gaps_in_batch": gaps, "minutes_behind": behind, "err": err}


def insurance(C, st):
    base = f"{C.OKX}/public/insurance-fund?instType=SWAP&instFamily=BTC-USDT"
    js = C.need(C.get(base + "&limit=1"))             # newest row of any type (normally regular_update)
    data = (js.get("data") or [{}])[0] if isinstance(js, dict) else {}
    details = data.get("details") if isinstance(data, dict) else None
    if not isinstance(details, list) or not details:
        raise ValueError("insurance fund: no regular_update row")
    rows = [{"t": int(details[0]["ts"]), "type": details[0].get("type"), "d": details[0]}]
    last = st.setdefault("okx_insurance_last", {})
    errors = {}
    for kind in INSURANCE_TYPES:
        js, err = C.get(base + f"&type={kind}&limit=100", pause=0.2)
        if err:
            errors[kind] = err
            continue
        det = ((js.get("data") or [{}])[0] or {}).get("details") if isinstance(js, dict) else None
        if not isinstance(det, list):
            errors[kind] = "malformed"
            continue
        newer = [d for d in det if int(d.get("ts", 0)) > last.get(kind, 0)]
        rows.extend({"t": int(d["ts"]), "type": kind, "d": d} for d in newer)
        if det:
            last[kind] = max(last.get(kind, 0), max(int(d.get("ts", 0)) for d in det))
    for r in rows:
        r.update(inst_family="BTC-USDT", inst_type="SWAP", pool_total=data.get("total"))
    added = C.append_rows("okx_insurance", rows, key=lambda r: (r["t"], r["type"], r["d"].get("amt"), r["d"].get("balance")))
    return {"added": added, "rows": len(rows), "err": "; ".join(f"{k}: {v}" for k, v in errors.items()) or None}


def collect(C, st):
    out = {}
    for name in SERIES_URL:
        try:
            out[name] = klines(C, st, name)
        except Exception as exc:
            out[name] = {"added": 0, "err": f"{type(exc).__name__}: {str(exc)[:120]}"}
    try:
        out["okx_insurance"] = insurance(C, st)
    except Exception as exc:
        out["okx_insurance"] = {"added": 0, "err": f"{type(exc).__name__}: {str(exc)[:120]}"}
    return out
