"""Options skew from the collector's Deribit captures (options-skew-0.1.0, repo 2.30; PREPARED - not an admitted panel
feature; brief section 14, family 6: skew change conditional on spot/perpetual disagreement).

Feasibility question: can the existing captures (data/options/deribit_btc_quotes, hourly, every listed BTC option)
support a continuous skew-change measure under fixed maturity, moneyness, quote-age and liquidity filters? This module
answers it with software, not a judgement: rr25_7d() computes a 7-day constant-maturity 25-delta risk reversal from
two-sided quotes, and feasibility() reports, over a date range of real captures, how often every filter is met and
which filter fails when it is not.

Frozen filters (FILTERS, hashed into every output):
  maturity      7-day constant maturity by total-variance interpolation between the two listed expiries bracketing
                7 days, each between 1 and 45 days out; no extrapolation
  moneyness     25-delta call and 25-delta put per expiry, delta from Black-76 on the expiry's own futures price
                (underlying_v2) with the option's mark IV; the nearest strike within 0.08 delta of 0.25
  quotes        both bid and ask present; quote-implied IVs from the bid/ask mid inverted with Black-76 on the
                futures price (prices are in BTC per contract: USD price = BTC price x futures price); mark IV is
                used for delta only
  liquidity     relative spread (ask - bid) / mid <= 0.25 and open interest >= 5 BTC
  quote age     capture observed_at - instrument timestamp (t_event_min + source_ts_offset_ms) <= 30 s
  pairing       skew change: two captures 50-70 minutes apart, both ok
Isolated gaps (fields the captures do not hold): no venue-published 25-delta risk reversal and no per-quote greeks
in the all-instrument capture (delta is model-derived from mark IV and stated so); the deribit_btc panel's greeks
cover only a near-the-money subset. These limit the measure; they do not block it.
Nothing here registers the feature; panel.py keeps options_disagreement gated until a registration freezes FILTERS.
"""
import datetime as dt
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "options-skew-0.1.0"
FILTERS = {"target_days": 7, "expiry_days": [1, 45], "delta": 0.25, "delta_tolerance": 0.08,
           "max_rel_spread": 0.25, "min_oi_btc": 5.0, "max_quote_age_ms": 30_000, "pair_minutes": [50, 70],
           "expiry_hour_utc": 8}
MONTHS = {m: i + 1 for i, m in enumerate(("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"))}


def filters_sha256():
    return E.content_sha256(FILTERS)


def _ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def expiry_ms(code):
    """'20OCT26' -> 08:00 UTC that day (Deribit expiry)."""
    d, mon, y = int(code[:-5]), MONTHS[code[-5:-2]], 2000 + int(code[-2:])
    return int(dt.datetime(y, mon, d, FILTERS["expiry_hour_utc"], tzinfo=dt.timezone.utc).timestamp() * 1000)


def black76(F, K, T, vol, call):
    if T <= 0 or vol <= 0:
        return max(0.0, (F - K) if call else (K - F))
    s = vol * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * s * s) / s
    d2 = d1 - s
    return F * _ncdf(d1) - K * _ncdf(d2) if call else K * _ncdf(-d2) - F * _ncdf(-d1)


def delta76(F, K, T, vol, call):
    s = vol * math.sqrt(T)
    d1 = (math.log(F / K) + 0.5 * s * s) / s
    return _ncdf(d1) if call else _ncdf(d1) - 1


def implied_vol(price_usd, F, K, T, call):
    lo, hi = 1e-4, 5.0
    intrinsic = max(0.0, (F - K) if call else (K - F))
    if price_usd <= intrinsic or price_usd >= (F if call else K):
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        if black76(F, K, T, mid, call) > price_usd:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def _quotes(cap):
    f = cap["fields"]
    ix = {k: i for i, k in enumerate(f)}
    for r in cap["rows"]:
        yield {k: r[i] for k, i in ix.items()}


def expiry_skew(cap, code, now_ms):
    """(state, {"T", "call_iv", "put_iv", ...}) for one expiry in one capture under FILTERS."""
    und = (cap.get("underlying_v2") or {}).get(code)
    F, fst = E.number(und[1] if und else None, "price")
    if fst != "ok":
        return "no-futures-price", None
    T = (expiry_ms(code) - now_ms) / (365.25 * 86_400_000)
    best = {True: None, False: None}
    why = {"no-two-sided": 0, "wide": 0, "low-oi": 0, "stale": 0}
    for q in _quotes(cap):
        parts = q["instrument"].split("-")
        if len(parts) != 4 or parts[1] != code:
            continue
        call = parts[3] == "C"
        K = float(parts[2])
        iv, ist = E.number(q.get("mark_iv"), "nonneg")
        if ist != "ok" or not iv:
            continue
        dlt = abs(delta76(F, K, T, iv / 100, call))
        if abs(dlt - FILTERS["delta"]) > FILTERS["delta_tolerance"]:
            continue
        bid, ask = q.get("bid_price_btc"), q.get("ask_price_btc")
        if bid is None or ask is None:
            why["no-two-sided"] += 1
            continue
        mid = (bid + ask) / 2
        if mid <= 0 or (ask - bid) / mid > FILTERS["max_rel_spread"]:
            why["wide"] += 1
            continue
        if (q.get("open_interest_btc") or 0) < FILTERS["min_oi_btc"]:
            why["low-oi"] += 1
            continue
        t_q = cap.get("t_event_min", cap["observed_at"]) + (q.get("source_ts_offset_ms") or 0)
        if cap["observed_at"] - t_q > FILTERS["max_quote_age_ms"]:
            why["stale"] += 1
            continue
        qiv = implied_vol(mid * F, F, K, T, call)
        if qiv is None:
            continue
        cand = (abs(dlt - FILTERS["delta"]), K, qiv, dlt)
        if best[call] is None or cand < best[call]:
            best[call] = cand
    if best[True] is None or best[False] is None:
        top = max(why, key=why.get) if any(why.values()) else "no-25-delta-strike"
        return top if any(why.values()) else "no-25-delta-strike", None
    return "ok", {"T": T, "call_iv": best[True][2], "put_iv": best[False][2], "call_K": best[True][1],
                  "put_K": best[False][1], "F": F}


def rr25_7d(cap):
    """(state, value) - the 7-day constant-maturity 25-delta risk reversal in vol points (call IV - put IV)."""
    now = cap["observed_at"]
    target = FILTERS["target_days"] / 365.25
    exps = []
    for code in (cap.get("underlying_v2") or {}):
        try:
            d = (expiry_ms(code) - now) / 86_400_000
        except (KeyError, ValueError):
            continue
        if FILTERS["expiry_days"][0] <= d <= FILTERS["expiry_days"][1]:
            exps.append((d, code))
    below = max((x for x in exps if x[0] <= FILTERS["target_days"]), default=None)
    above = min((x for x in exps if x[0] >= FILTERS["target_days"]), default=None)
    if below is None or above is None:
        return "no-bracketing-expiry", None
    s1, a = expiry_skew(cap, below[1], now)
    s2, b = expiry_skew(cap, above[1], now)
    if s1 != "ok" or s2 != "ok":
        return f"{below[1]}:{s1}|{above[1]}:{s2}", None
    out = {}
    for side in ("call_iv", "put_iv"):
        w1, w2 = a[side] ** 2 * a["T"], b[side] ** 2 * b["T"]
        if b["T"] == a["T"]:
            v = a[side]
        else:
            w = w1 + (w2 - w1) * (target - a["T"]) / (b["T"] - a["T"])
            v = math.sqrt(max(w, 0) / target)
        out[side] = v
    return "ok", round(100 * (out["call_iv"] - out["put_iv"]), 4)


def skew_changes(caps):
    """[(t_ms, state, change)] for consecutive captures 50-70 minutes apart."""
    pts = [(c["observed_at"],) + rr25_7d(c) for c in sorted(caps, key=lambda c: c["observed_at"])]
    out = []
    for (t0, s0, v0), (t1, s1, v1) in zip(pts, pts[1:]):
        gap = (t1 - t0) / 60_000
        if not FILTERS["pair_minutes"][0] <= gap <= FILTERS["pair_minutes"][1]:
            out.append((t1, f"unpaired ({gap:.0f} min apart)", None))
        elif s0 != "ok" or s1 != "ok":
            out.append((t1, "skew unavailable", None))
        else:
            out.append((t1, "ok", round(v1 - v0, 4)))
    return out


def feasibility(base, days):
    """Over real capture files: how often the 7d RR25 and its hourly change are computable, and why not."""
    caps = []
    for d in days:
        p = Path(base) / "data/options/deribit_btc_quotes" / f"{d}.jsonl"
        if p.exists():
            caps += [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    states = {}
    vals = []
    for c in caps:
        s, v = rr25_7d(c)
        k = s if s == "ok" else s.split("|")[0].split(":")[-1] if ":" in s else s
        states[k] = states.get(k, 0) + 1
        if v is not None:
            vals.append(v)
    ch = skew_changes(caps)
    okc = [x[2] for x in ch if x[1] == "ok"]
    return {"version": VERSION, "filters_sha256": filters_sha256(), "days": list(days), "captures": len(caps),
            "rr25_states": states, "rr25_ok_share": round(states.get("ok", 0) / len(caps), 4) if caps else None,
            "rr25_range_volpts": [min(vals), max(vals)] if vals else None,
            "hourly_changes": len(ch), "hourly_changes_ok": len(okc),
            "status": "prepared (feasibility measured; not registered, not a panel feature)"}
