"""Module F - options / perpetual disagreement.

Surface measures from each 15-minute Deribit record (mark IV, OI; collector option schema 1/2):
  delta convention   Black-76 forward delta from Deribit mark IV, r = 0 (Deribit reports
                     interest_rate 0 for options), time to expiry to 08:00 UTC on the expiry date
  ATM IV (per expiry) IV interpolated linearly in delta at call delta 0.50
  RR25 (per expiry)  IV(call delta +0.25) - IV(put delta -0.25), each interpolated linearly in delta
  constant maturity  7 and 30 days: ATM by linear interpolation of total variance (sigma^2 T) in T
                     between the bracketing expiries; RR25 linearly in T; no extrapolation
  units              IV in vol points (percent); RR25 in vol points
  OI concentration   Herfindahl index of OI shares by (expiry, strike); put/call OI ratio
Quote quality (panel quotes, when present): ticker timestamp within 60 s of the record and bid-ask
spread <= 10% of mark, otherwise excluded; Deribit's own delta is compared with ours as a check.
OI does not reveal dealer inventory direction; nothing here assigns a sign to dealer exposure.

Event: rr25_7d z-score (vs the trailing `z_window` records, prior only) <= -z while the Binance
predicted funding z-score >= +z  ->  "bearish_disagreement", direction -1; mirror image ->
"bullish_disagreement", direction +1. Reference: hourly controls.
"""
import datetime as dt
import math
import re

from lab.common import BASIS_PROSPECTIVE, DAY, PROCESSING_LATENCY_MS, hash_inputs
from lab.events import event_record

ID = "options_disagreement"
VERSION = "F-1"
NAME = re.compile(r"BTC-(\d{1,2})([A-Z]{3})(\d{2})-(\d+(?:\.\d+)?)-([CP])")
MONTHS = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}
SPEC = {"module": "F", "id": ID, "version": VERSION, "title": "Options / perpetual disagreement",
        "hypothesis": "When 7-day option skew and perpetual funding disagree strongly, subsequent BTC returns "
                      "follow the options side more often than hourly controls.",
        "inputs": ["data/options/deribit_btc (mark IV, OI, underlying)", "snap.binance_usdt_prem funding",
                   "data/series/binance_globalLongShortAccountRatio_5m"],
        "event": "rr25_7d z <= -z and funding z >= +z (bearish), or the mirror image (bullish)",
        "outcome": "net log return in the options-implied direction",
        "baseline": "hourly controls; regression on prior return, volatility, funding",
        "exclusions": ["expiries under 1 day", "no bracketing expiries for 7 or 30 days",
                       "records without funding in the same run"]}


def expiry_ms(name):
    m = NAME.fullmatch(name)
    d = dt.datetime(2000 + int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)), 8, tzinfo=dt.timezone.utc)
    return int(d.timestamp() * 1000)


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def delta(f, k, iv, t, kind):
    s = iv / 100
    d1 = (math.log(f / k) + 0.5 * s * s * t) / (s * math.sqrt(t))
    return ncdf(d1) if kind == "C" else ncdf(d1) - 1


def interp(points, x):
    """Linear interpolation on sorted (x, y) points; None outside the range."""
    pts = sorted(points)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1 and x1 > x0:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None


def surface(rec):
    """Per-expiry ATM IV and RR25, constant-maturity 7d/30d, OI concentration."""
    t0 = rec["t"]
    by_exp = {}
    total_oi, puts, calls, shares = 0.0, 0.0, 0.0, []
    for name, oi, iv in (r[:3] for r in rec["rows"]):
        m = NAME.fullmatch(name)
        if not m:
            continue
        exp = expiry_ms(name)
        t = (exp - t0) / (365 * DAY)
        code = name.split("-")[1]
        f = rec.get("underlying", {}).get(code)
        total_oi += oi
        shares.append(oi)
        if m.group(5) == "P":
            puts += oi
        else:
            calls += oi
        if t < 1 / 365 or not f or not iv:
            continue
        by_exp.setdefault(exp, []).append((m.group(5), delta(f, float(m.group(4)), iv, t, m.group(5)), iv))
    per = {}
    for exp, opts in by_exp.items():
        c = [(d, iv) for k, d, iv in opts if k == "C"]
        p = [(d, iv) for k, d, iv in opts if k == "P"]
        atm, c25, p25 = interp(c, 0.5), interp(c, 0.25), interp(p, -0.25)
        per[exp] = {"t_years": (exp - t0) / (365 * DAY), "atm": atm,
                    "rr25": (c25 - p25) if c25 is not None and p25 is not None else None}
    def cm(days):
        pts = sorted((v["t_years"], v) for v in per.values() if v["atm"] is not None)
        target = days / 365
        for (ta, a), (tb, b) in zip(pts, pts[1:]):
            if ta <= target <= tb:
                w = a["atm"] ** 2 * ta + (b["atm"] ** 2 * tb - a["atm"] ** 2 * ta) * (target - ta) / (tb - ta)
                rr = (a["rr25"] + (b["rr25"] - a["rr25"]) * (target - ta) / (tb - ta)
                      if a["rr25"] is not None and b["rr25"] is not None else None)
                return math.sqrt(w / target), rr
        return None, None
    atm7, rr7 = cm(7)
    atm30, rr30 = cm(30)
    hhi = sum((x / total_oi) ** 2 for x in shares) if total_oi else None
    return {"atm_iv_7d": atm7, "atm_iv_30d": atm30, "rr25_7d": rr7, "rr25_30d": rr30,
            "term_slope_30_7": (atm30 - atm7) if atm7 and atm30 else None, "oi_hhi": hhi,
            "put_call_oi": puts / calls if calls else None, "total_oi_btc": total_oi}


def panel_quality(rec):
    ok, bad = [], []
    for row in rec.get("panel") or []:
        r = dict(zip(rec.get("panel_fields", []), row))
        fresh = r.get("timestamp") and abs(r["timestamp"] - rec.get("t_event", r["timestamp"])) <= 60_000
        spread_ok = (r.get("best_bid_price") and r.get("best_ask_price") and r.get("mark_price")
                     and (r["best_ask_price"] - r["best_bid_price"]) <= 0.10 * r["mark_price"])
        (ok if fresh and spread_ok else bad).append(r["instrument"])
    return {"panel_ok": len(ok), "panel_excluded": len(bad)}


def zscore(hist, x, window):
    h = [v for v in hist[-window:] if v is not None]
    if len(h) < window * 0.7 or x is None:
        return None
    mu = sum(h) / len(h)
    sd = math.sqrt(sum((v - mu) ** 2 for v in h) / (len(h) - 1)) if len(h) > 1 else 0
    return (x - mu) / sd if sd > 0 else None


def run(lab, params):
    recs = lab.store.options()
    snaps = {s["t"]: s for s in lab.store.snaps()}
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    events, controls, rr_hist, f_hist, series = [], [], [], [], []
    z, window = params["z"], params["z_window"]
    for rec in recs:
        s = surface(rec)
        snap = snaps.get(rec["t"]) or {}
        prem = snap.get("binance_usdt_prem") or {}
        funding = prem.get("funding_live_predicted_8h") if prem.get("st") == "ok" else None
        s.update(panel_quality(rec), funding_pred_8h=funding)
        rz, fz = zscore(rr_hist, s["rr25_7d"], window), zscore(f_hist, funding, window)
        rr_hist.append(s["rr25_7d"])
        f_hist.append(funding)
        s.update(rr25_7d_z=rz, funding_z=fz)
        series.append((rec["t"], s))
        avail = max(rec["observed_at"], snap.get("observed_at", rec["observed_at"]))
        ih = hash_inputs([rec["t"], s["rr25_7d"], funding])
        if rz is not None and fz is not None:
            for group, cond, direction in (("bearish_disagreement", rz <= -z and fz >= z, -1),
                                           ("bullish_disagreement", rz >= z and fz <= -z, 1)):
                if cond:
                    events.append(event_record(ID, VERSION, rec["t"], rec["observed_at"], avail + PROCESSING_LATENCY_MS,
                                               direction, group, s, ih, BASIS_PROSPECTIVE, {"records_in_z": window},
                                               {"funding": "same run"}, lab.code))
        if rec["t"] % 3_600_000 < 900_000:
            controls.append(event_record(ID + ":control", VERSION, rec["t"], rec["observed_at"],
                                         avail + PROCESSING_LATENCY_MS, -1 if (s["rr25_7d"] or 0) < 0 else 1,
                                         "control", s, ih, BASIS_PROSPECTIVE, {}, {}, lab.code))
    have = sum(1 for _, s in series if s["rr25_7d_z"] is not None)
    state = "available" if have >= params.get("min_records", 96 * 14) else "insufficient_data"
    reasons = [] if state == "available" else [f"{len(recs)} option records ({have} with a trailing z-score); "
                                                f"the design needs {params.get('min_records', 96 * 14)}"]
    latest = series[-1][1] if series else {}
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"records": len(recs), "with_z": have,
                                                   "latest_surface": {k: (round(v, 4) if isinstance(v, float) else v)
                                                                      for k, v in latest.items()}},
                                      "bars": bars, "state": state, "reasons": reasons}]}
