"""Deribit BTC option book, schema 2 (collector 2.7).

Every run: one record in data/options/deribit_btc/YYYY-MM-DD.jsonl. Its rows keep exactly the
schema-1 columns (instrument, open interest, mark IV), so schema-1 readers keep working; schema 2
adds record-level fields (zero_oi, absent, past_expiry, underlying_v2, the quote panel ...).
Hourly (the first run in each UTC hour): one full quote record in
data/options/deribit_btc_quotes/YYYY-MM-DD.jsonl with bid, ask, mark, 24h volume and last price for
every instrument with open interest. Quotes are hourly, not every 15 minutes, to bound storage
(~74 KB per full record); open interest, mark IV and the panel stay at the collector cadence.

What each state means, so that nothing is confused with anything else:
  row present              the instrument had open interest > 0 in this run's summary
  name in `zero_oi`        listed in the summary with open interest exactly 0
  name in `absent`         active per the instrument list but not returned by the summary
  name in `past_expiry`    returned by the summary although its expiry time has passed
  bid/ask null             no resting bid/ask at the source (a missing quote, not a zero price)
  no record for the run    the collection failed; the run record says why
Volume is Deribit's rolling 24-hour volume at the time of the response. It is NOT the volume
traded in the 15 minutes between runs, and differencing it does not give interval volume
(trades leaving the 24-hour window are subtracted too).

Units: option prices (bid, ask, mark, last) in BTC per 1-BTC contract (Deribit options are
inverse); mark IV in percent; open interest and 24h volume in BTC contracts; volume_usd in USD.
The bounded quote panel adds Deribit's own greeks for a few liquid instruments; selection uses
Black-76 forward delta from mark IV with r = 0 (Deribit reports interest_rate 0 for options).
"""
import math
import re

SCHEMA = "deribit_options/2"
ROW_FIELDS = ["instrument", "open_interest_btc", "mark_iv", "bid_price_btc", "ask_price_btc", "mark_price_btc",
              "volume_24h_rolling_btc", "volume_24h_rolling_usd", "last_price_btc", "source_ts_offset_ms"]
PANEL_FIELDS = ["instrument", "timestamp", "best_bid_price", "best_bid_amount", "best_ask_price",
                "best_ask_amount", "mark_price", "mark_iv", "bid_iv", "ask_iv", "delta", "gamma", "vega", "theta",
                "underlying_price", "index_price", "open_interest"]
META_FIELDS = ["expiration_ms", "strike", "option_type", "creation_ms", "tick_size", "contract_size",
               "settlement_period", "min_trade_amount"]
PANEL_MAX = 12              # extra ticker requests per run (Deribit public credits refill ~20/s)
PANEL_BUDGET_S = 20
PANEL_TARGET_DAYS = (2, 7, 30)
NAME = re.compile(r"BTC-(\d{1,2}[A-Z]{3}\d{2})-(\d+(?:\.\d+)?)-([CP])")
DAY = 86_400_000


def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black76_delta(forward, strike, iv_pct, t_years, kind):
    """Forward (undiscounted) Black-76 delta; None when inputs cannot define it."""
    if not forward or not strike or not iv_pct or t_years <= 0 or forward <= 0 or strike <= 0:
        return None
    sigma = iv_pct / 100.0
    d1 = (math.log(forward / strike) + 0.5 * sigma * sigma * t_years) / (sigma * math.sqrt(t_years))
    return ncdf(d1) if kind == "C" else ncdf(d1) - 1.0


def refresh_meta(C, st, names):
    """Instrument metadata, refreshed once per UTC day or when the summary lists an unknown name.
    Returns (meta_dict, status, listing_change or None)."""
    cache = st.get("deribit_meta") or {}
    known = cache.get("instruments") or {}
    today = C.day(C.NOW)
    if cache.get("day") == today and all(n in known for n in names):
        return known, "cached", None
    js, err = C.get(f"{C.DERIBIT}/get_instruments?currency=BTC&kind=option&expired=false", tries=2, timeout=20)
    res = js.get("result") if isinstance(js, dict) else None
    if err or not isinstance(res, list) or not res:
        return known, f"refresh failed: {err or 'malformed get_instruments'}", None
    fresh = {}
    for x in res:
        name = x.get("instrument_name") if isinstance(x, dict) else None
        if not isinstance(name, str) or not NAME.fullmatch(name):
            continue
        fresh[name] = [x.get("expiration_timestamp"), C.f(x.get("strike")), x.get("option_type"),
                       x.get("creation_timestamp"), C.f(x.get("tick_size")), C.f(x.get("contract_size")),
                       x.get("settlement_period"), C.f(x.get("min_trade_amount"))]
    change = None
    if known:
        added, removed = sorted(set(fresh) - set(known)), sorted(set(known) - set(fresh))
        if added or removed:
            change = {"t": C.NOW, "schema": "deribit_option_listing/1", "source": "public/get_instruments",
                      "added": added,
                      "removed": [[n, "past_expiry" if (known[n][0] or 0) <= C.NOW else "delisted_or_inactive"]
                                  for n in removed],
                      "listed": len(fresh)}
    st["deribit_meta"] = {"t": C.NOW, "day": today, "fields": META_FIELDS, "instruments": fresh}
    return fresh, "refreshed", change


def collect(C, st):
    """Summary (one request) + metadata (at most one request) + quote panel (at most PANEL_MAX)."""
    js = C.need(C.get(f"{C.DERIBIT}/get_book_summary_by_currency?currency=BTC&kind=option", pause=0.2))
    res = js.get("result") if isinstance(js, dict) else None
    if not isinstance(res, list) or not res or not all(isinstance(x, dict) for x in res):
        raise ValueError("empty or malformed Deribit option summary")
    stamps = [int(C.f(x.get("creation_timestamp")) or 0) for x in res]
    t_event, t_event_min = max(stamps), min(s for s in stamps if s) if any(stamps) else 0
    rows, underlying, underlying_v2, zero, zero_names, excluded, past = [], {}, {}, 0, [], [], []
    listed = set()
    for x in res:
        name, oi = x.get("instrument_name"), C.f(x.get("open_interest"))
        if not isinstance(name, str) or not C.OPTION_NAME.fullmatch(name):
            excluded.append([str(name)[:40], "instrument name"])
            continue
        listed.add(name)
        if oi is None or oi < 0:
            excluded.append([name, "open_interest"])
            continue
        if oi == 0:
            zero += 1
            zero_names.append(name)
            continue
        iv, u = C.positive(x.get("mark_iv")), C.positive(x.get("underlying_price"))
        if iv is None or u is None:
            excluded.append([name, "mark_iv" if iv is None else "underlying_price"])
            continue
        ts = int(C.f(x.get("creation_timestamp")) or 0)
        rows.append([name, oi, iv, C.f(x.get("bid_price")), C.f(x.get("ask_price")), C.f(x.get("mark_price")),
                     C.f(x.get("volume")), C.f(x.get("volume_usd")), C.f(x.get("last")),
                     ts - t_event_min if ts else None])      # full row; the per-run record keeps rows[:3]
        exp = name.split("-")[1]
        underlying.setdefault(exp, u)
        underlying_v2.setdefault(exp, [x.get("underlying_index"), u, C.f(x.get("interest_rate"))])
    with_oi = len(rows) + len(excluded)
    if not rows or len(excluded) > C.FORWARD_MAX_INVALID * max(with_oi, 1):
        raise ValueError(f"{len(excluded)} of {with_oi} option rows invalid; snapshot not stored "
                         f"(first: {excluded[:3]})")
    rows.sort()
    zero_names.sort()
    meta, meta_status, change = refresh_meta(C, st, listed)
    absent = sorted(n for n, m in meta.items() if n not in listed and (m[0] or 0) > C.NOW)
    past = sorted(n for n in listed if n in meta and (meta[n][0] or 0) <= C.NOW)
    if change:
        C.append_rows("options/deribit_btc_listing", [change])
    panel, panel_status = quote_panel(C, rows, underlying, meta)
    status = "degraded" if excluded else "complete"
    delivery = next((C.f(x.get("estimated_delivery_price")) for x in res if x.get("estimated_delivery_price")), None)
    hour = C.NOW // (3_600_000)
    quotes_due = st.get("deribit_quotes_hour") != hour
    if quotes_due:
        C.append_rows("options/deribit_btc_quotes", [{
            "t": C.NOW, "t_event": t_event, "t_event_min": t_event_min, "schema": "deribit_option_quotes/1",
            "unit": "option prices in BTC per 1-BTC contract; bid/ask null = no resting order; volume is the "
                    "rolling 24h figure at t_event, not interval volume; source_ts_offset_ms is relative to "
                    "t_event_min", "fields": ROW_FIELDS, "rows": rows, "underlying_v2": underlying_v2,
            "estimated_delivery_price": delivery}], partition=C.day)
        st["deribit_quotes_hour"] = hour
    out = {"t": C.NOW, "t_event": t_event, "t_event_min": t_event_min, "status": status, "schema": SCHEMA,
           "unit": "open_interest in BTC (contracts of 1 BTC); mark_iv in % vol",
           "fields": ROW_FIELDS[:3], "rows": [r[:3] for r in rows], "underlying": underlying,
           "quotes_record": quotes_due,
           "underlying_fields": ["underlying_index", "underlying_price", "interest_rate"],
           "underlying_v2": underlying_v2, "estimated_delivery_price": delivery,
           "instruments": len(res), "zero_oi_omitted": zero, "zero_oi": zero_names, "excluded": excluded,
           "absent": absent, "past_expiry": past, "meta_status": meta_status, "meta_listed": len(meta),
           "panel_fields": PANEL_FIELDS, "panel": panel, "panel_status": panel_status}
    added = C.append_rows("options/deribit_btc", [out], partition=C.day)
    return {"added": added, "status": status, "instruments": len(res), "with_oi": len(rows),
            "excluded": len(excluded), "zero_oi": zero, "absent": len(absent), "past_expiry": len(past),
            "listing_change": bool(change), "meta": meta_status, "panel": panel_status,
            "total_oi_btc": round(sum(r[1] for r in rows), 1),
            "err": f"degraded: {len(excluded)} option rows excluded" if excluded else None}


def select_panel(rows, underlying, meta, now):
    """Up to PANEL_MAX liquid instruments: for the expiries nearest 2, 7 and 30 days, the call and
    put nearest 50 delta and the 25-delta call and put (Black-76 from mark IV). Deterministic."""
    by_exp = {}
    for r in rows:
        name, oi, iv = r[0], r[1], r[2]
        m = NAME.fullmatch(name)
        if not m or name not in meta or not meta[name][0]:
            continue
        exp_ms = meta[name][0]
        t_years = (exp_ms - now) / (365.0 * DAY)
        if t_years <= 1 / 365.0:
            continue
        delta = black76_delta(underlying.get(m.group(1)), float(m.group(2)), iv, t_years, m.group(3))
        if delta is not None:
            by_exp.setdefault(exp_ms, []).append((name, m.group(3), delta, oi))
    chosen, used = [], set()
    for days in PANEL_TARGET_DAYS:
        if not by_exp:
            break
        exp = min(by_exp, key=lambda e: (abs((e - now) / DAY - days), e))
        if exp in used:
            continue
        used.add(exp)
        cand = by_exp[exp]
        for kind, target in (("C", 0.5), ("P", -0.5), ("C", 0.25), ("P", -0.25)):
            pool = [c for c in cand if c[1] == kind and c[0] not in chosen]
            if pool:
                chosen.append(min(pool, key=lambda c: (abs(c[2] - target), -c[3], c[0]))[0])
    return chosen[:PANEL_MAX]


def quote_panel(C, rows, underlying, meta):
    names = select_panel(rows, underlying, meta, C.NOW)
    if not names:
        return [], "no instruments selectable (metadata missing)"
    start = C.time.monotonic()
    deadline = start + PANEL_BUDGET_S
    panel, errors = [], 0
    for name in names:
        if C.time.monotonic() >= deadline:
            errors += 1
            continue
        js, err = C.get(f"{C.DERIBIT}/ticker?instrument_name={name}", tries=1, pause=0.1, timeout=8, deadline=deadline)
        r = js.get("result") if isinstance(js, dict) else None
        if err or not isinstance(r, dict):
            errors += 1
            continue
        g = r.get("greeks") or {}
        panel.append([name, r.get("timestamp"), C.f(r.get("best_bid_price")), C.f(r.get("best_bid_amount")),
                      C.f(r.get("best_ask_price")), C.f(r.get("best_ask_amount")), C.f(r.get("mark_price")),
                      C.f(r.get("mark_iv")), C.f(r.get("bid_iv")), C.f(r.get("ask_iv")), C.f(g.get("delta")),
                      C.f(g.get("gamma")), C.f(g.get("vega")), C.f(g.get("theta")), C.f(r.get("underlying_price")),
                      C.f(r.get("index_price")), C.f(r.get("open_interest"))])
    status = f"{len(panel)}/{len(names)} tickers" + (f"; {errors} failed or out of time" if errors else "")
    return panel, status
