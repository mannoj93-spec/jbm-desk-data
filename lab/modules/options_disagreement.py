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
Two different products, never mixed (lab-2.0):
  DESCRIPTIVE SURFACE  the measures above, from Deribit MARK IV of every instrument with OI. Mark IV
                       is Deribit's model value; it exists without any resting order, so it is a
                       description of the venue's surface, not a tradable price. Always reported,
                       with that limitation named.
  QUOTE-QUALIFIED SIGNAL  an event counts as quote-qualified only if the executable quotes behind
                       the measure it uses were checked and passed. rr25_7d uses the 25-delta call
                       and put of the expiries around 7 days; the collector's 12-ticker panel
                       samples the expiry nearest 7 days at +-25 delta (and 50 delta). Eligibility:
                         qualified  that expiry's 25-delta call AND put panel quotes both pass: ticker
                                    time within 60 s of the record, two-sided (bid and ask > 0 with
                                    size), not crossed, spread <= 10% of mid, expiry > 1 day away,
                                    and mark IV inside [bid IV, ask IV]
                         failed     at least one of them was observed and failed (reason recorded)
                         unknown    the panel was absent, failed, or did not include them. Quote
                                    quality that was never observed stays unknown; it is not failed.
Instruments outside the panel are not invalidated: the panel only QUALIFIES the signal. Zero open
interest is listed by the collector separately from absent instruments and never read as missing.
OI does not reveal dealer inventory direction; nothing here assigns a sign to dealer exposure.

Event: rr25_7d z-score (vs the trailing `z_window` records, prior only) <= -z while the Binance
predicted funding z-score >= +z  ->  "bearish_disagreement", direction -1; mirror image ->
"bullish_disagreement", direction +1. Reference: hourly controls, one per UTC hour of option-record
availability (lab/controls.py; F-3); funding is never required for a control.
Params: quote_policy "qualified" (default: events that are not quote-qualified are regrouped as
<group>_ineligible, visible but outside the test group) or "mark_only" (a separately labelled,
descriptive variant that evaluates mark-IV events regardless of quotes).
As-of (lab/asof.py): an event's inputs are the option record and the same run's funding snapshot
(t_inputs = the later of their observed_at); a control's only input is the option record, so a late
or missing snapshot never moves a control. The z-score window is the last
`window` earlier option records that had been observed by t_inputs; within it each historical
funding value counts only if ITS snapshot was observed by t_inputs (separate availability per
feature, lab-2.1). Anything not yet available is missing (never filled) and the 70% coverage rule
applies. Funding without a snapshot observed_at is unknown.
"""
import datetime as dt
import math
import re

from lab import controls as controls_mod
from lab.asof import decide
from lab.common import BASIS_PROSPECTIVE, DAY, hash_inputs
from lab.events import event_record

ID = "options_disagreement"
VERSION = "F-3"
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


def quote_check(r, t_ref):
    """None if the quote passes, else the reason. `r` is one panel row as a dict."""
    bid, ask, mid_mark = r.get("best_bid_price"), r.get("best_ask_price"), r.get("mark_price")
    if r.get("timestamp") is None or abs(r["timestamp"] - t_ref) > 60_000:
        return "stale"
    if not bid or not ask or not r.get("best_bid_amount") or not r.get("best_ask_amount"):
        return "one_sided_or_missing"
    if bid >= ask:
        return "crossed"
    if (ask - bid) > 0.10 * ((ask + bid) / 2):
        return "wide"
    exp = expiry_ms(r["instrument"])
    if exp is None or exp - t_ref <= DAY:
        return "expiring"
    biv, aiv, miv = r.get("bid_iv"), r.get("ask_iv"), r.get("mark_iv")
    if biv and aiv and miv and not (biv <= miv <= aiv):
        return "mark_outside_quotes"
    return None


def panel_quality(rec):
    """Counts by outcome plus the eligibility of the rr25_7d signal (qualified / failed / unknown)."""
    t_ref = rec.get("t_event") or rec["t"]
    rows = [dict(zip(rec.get("panel_fields", []), row)) for row in rec.get("panel") or []]
    reasons = {}
    for r in rows:
        why = quote_check(r, t_ref)
        reasons[why or "ok"] = reasons.get(why or "ok", 0) + 1
    out = {"panel_ok": reasons.get("ok", 0), "panel_excluded": sum(v for k, v in reasons.items() if k != "ok"),
           "panel_reasons": reasons}
    # the rr25_7d instruments: the panel expiry nearest 7 days, its call and put nearest |delta| 0.25
    cand = [r for r in rows if expiry_ms(r["instrument"]) and r.get("delta") is not None]
    if not cand:
        out.update(rr25_7d_quotes="unknown", rr25_7d_quote_reason="panel absent or without greeks")
        return out
    exp7 = min({expiry_ms(r["instrument"]) for r in cand}, key=lambda e: abs((e - t_ref) / DAY - 7))
    legs = []
    for kind, target in (("C", 0.25), ("P", -0.25)):
        pool = [r for r in cand if expiry_ms(r["instrument"]) == exp7 and r["instrument"].endswith("-" + kind)
                and abs(r["delta"] - target) <= 0.12]
        legs.append(min(pool, key=lambda r: abs(r["delta"] - target)) if pool else None)
    if any(l is None for l in legs):
        out.update(rr25_7d_quotes="unknown", rr25_7d_quote_reason="25-delta call/put of the ~7d expiry not in panel")
        return out
    fails = [f"{l['instrument']}: {quote_check(l, t_ref)}" for l in legs if quote_check(l, t_ref)]
    out.update(rr25_7d_quotes="failed" if fails else "qualified", rr25_7d_quote_reason="; ".join(fails) or None)
    return out


def zscore(hist, x, window):
    """z of x against the last `window` entries of hist (None entries are missing; >= 70% needed)."""
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
    policy = params.get("quote_policy", "qualified")
    events, cands, series = [], [], []
    hist = []           # earlier records: (t, rr25_7d, rr available at, funding, funding available at)
    z, window = params["z"], params["z_window"]
    elig = {"qualified": 0, "failed": 0, "unknown": 0}
    def zs(t_cut, rr, fund):
        """(rr z, funding z) as of t_cut. Window = the last `window` earlier option records
        (record-time order) already observed by t_cut - the record list exactly as it stood then, so
        a record collected later can neither enter nor shift it. Within it a funding value counts
        only if ITS snapshot was observed by t_cut; otherwise it is missing (never filled) and the
        70% coverage rule decides. A value that arrives later is used by later decisions."""
        prior = [h for h in hist if h[2] <= t_cut][-window:]
        return (zscore([h[1] for h in prior], rr, window),
                zscore([h[3] if h[4] is not None and h[4] <= t_cut else None for h in prior], fund, window))

    for rec in recs:
        s = surface(rec)
        snap = snaps.get(rec["t"]) or {}
        prem = snap.get("binance_usdt_prem") or {}
        f_avail = snap.get("observed_at")                # funding is known when ITS snapshot was observed
        funding = prem.get("funding_live_predicted_8h") if prem.get("st") == "ok" and f_avail is not None else None
        s.update(panel_quality(rec), funding_pred_8h=funding)
        # an event needs funding, so its inputs are complete when both the option record and the
        # funding snapshot are observed
        t_inputs = max(rec["observed_at"], f_avail) if funding is not None else rec["observed_at"]
        rz, fz = zs(t_inputs, s["rr25_7d"], funding)
        s.update(rr25_7d_z=rz, funding_z=fz, surface_basis="descriptive: Deribit mark IV")
        series.append((rec["t"], s))
        ih = hash_inputs([rec["t"], s["rr25_7d"], funding])
        avail, excluded = decide(rec["t"], t_inputs)
        if not excluded and rz is not None and fz is not None:
            for group, cond, direction in (("bearish_disagreement", rz <= -z and fz >= z, -1),
                                           ("bullish_disagreement", rz >= z and fz <= -z, 1)):
                if cond:
                    elig[s["rr25_7d_quotes"]] += 1
                    g = group if policy == "mark_only" or s["rr25_7d_quotes"] == "qualified" else group + "_ineligible"
                    events.append(event_record(ID, VERSION, rec["t"], rec["observed_at"], avail,
                                               direction, g, dict(s, severity=abs(rz)), ih, BASIS_PROSPECTIVE,
                                               {"records_in_z": window},
                                               {"funding": "same run", "quote_policy": policy,
                                                "rr25_7d_quotes": s["rr25_7d_quotes"]}, lab.code, t_inputs=t_inputs))
        # Control candidate: its only required input is the option record, so a funding snapshot
        # arriving later (or never) cannot move, delay or exclude it, and no signal is needed.
        # Its descriptive features are as of its own availability. One per hour: lab/controls.py.
        t_ctl = rec["observed_at"]
        f_ctl = funding if funding is not None and f_avail <= t_ctl else None
        crz, cfz = zs(t_ctl, s["rr25_7d"], f_ctl)

        def build(avail, rec=rec, s=dict(s), f_ctl=f_ctl, crz=crz, cfz=cfz, t_ctl=t_ctl):
            return event_record(ID + ":control", VERSION, rec["t"], rec["observed_at"], avail,
                                -1 if (s["rr25_7d"] or 0) < 0 else 1, "control",
                                dict(s, funding_pred_8h=f_ctl, rr25_7d_z=crz, funding_z=cfz),
                                hash_inputs([rec["t"], s["rr25_7d"]]), BASIS_PROSPECTIVE, {}, {}, lab.code,
                                t_inputs=t_ctl)
        cands.append(controls_mod.candidate(rec["t"], rec["t"], rec["observed_at"], t_ctl, build))
        hist.append((rec["t"], s["rr25_7d"], rec["observed_at"], funding, f_avail if funding is not None else None))
    controls, comparison = controls_mod.apply(lab, cands, min((r["observed_at"] for r in recs), default=None))
    have = sum(1 for _, s in series if s["rr25_7d_z"] is not None)
    state = "available" if have >= params.get("min_records", 96 * 14) else "insufficient_data"
    reasons = [] if state == "available" else [f"{len(recs)} option records ({have} with a trailing z-score); "
                                                f"the design needs {params.get('min_records', 96 * 14)}"]
    latest = series[-1][1] if series else {}
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"records": len(recs), "with_z": have, "quote_policy": policy,
                                                   "event_quote_eligibility": elig, "comparison": comparison,
                                                   "latest_surface": {k: (round(v, 4) if isinstance(v, float) else v)
                                                                      for k, v in latest.items()}},
                                      "bars": bars, "state": state, "reasons": reasons}]}
