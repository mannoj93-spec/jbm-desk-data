#!/usr/bin/env python3
"""range_contract — the one forecast contract shared by evaluation, registration, reading and scoring.

Version contract-12.0.0 (crypto-desk package 12.0, repo revision 2.15). Stdlib only. `range_model.py`
stays byte-frozen (O21 spec ae6aa254…); this module defines how its features, fits and losses are used.

Two contracts, one implementation:
  RC1   the contract O21 evaluated: decision at a 4H close D; target window [D, D+h); inputs closed or
        available at or before D; point = the OLS fitted value p (B2) or b0 (B0) in ln(lr) units; losses on
        the point. Historical performance claims (baserates R1-R2) belong to RC1 only.
  RC1D  the automated prospective variant: same inputs, fit and point rule, but the window starts at
        S = the first 5-minute boundary at least LEAD_MIN minutes after the forecast was prepared, and the
        calendar terms (weekend shares, release count) describe [S, S+h) - the window actually scored.
        RC1D has no historical evaluation; it earns its own record from registered forecasts.

Common to both:
  target     ln(max high / min low) over the window, Binance BTCUSDT perp, last price. Evaluation reads 4H
             bars (RC1 windows are 4H-aligned); scoring reads 1m bars; on aligned windows the two agree.
  point      ln(lr) = p (never the residual-median-adjusted value). Registered as `point` = exp(p).
  quantiles  exp(p + fit-residual 10/50/90 quantiles), sorted. q50 is NOT the loss-bearing point.
  baseline   B0 on the same window, point b0, quantiles from B0's fit-period residuals.
  coherence  none applied. A 24h point below the 4h point (or 72h below 24h) is reported as a diagnostic.
             `range_model.forecast_now`'s coherence raise is not part of any contract.
  losses     abs_error_log_lr = |ln point - ln realized|; qlike on range^2 with the point; pinball on the
             three quantiles; covered_80 = q10 <= realized <= q90. One function, `losses`, for all paths.
  splits     a row belongs to a period only if its decision AND its target maturity fall inside it.
"""
from __future__ import annotations

import bisect
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

import range_model as R

VERSION = "contract-12.0.0"
UTC = dt.timezone.utc
HOURS = {"4h": 4, "24h": 24, "72h": 72}
SELECTED = {"4h": "B2", "24h": "B2", "72h": "B2"}       # O21 selection, frozen
LEAD_MIN = 5            # RC1D: window starts >= 5 minutes after preparation (time to publish durably)
MIN_MARGIN_S = 120      # freezing is refused when the window starts within two minutes
ROUND = 12              # registry rounding in lr units (relative error < 1e-9 at lr >= 0.001)
PARITY_TOL = 1e-8       # |difference| allowed between paths in ln(lr) and loss units after rounding

CONTRACTS = {
    "RC1": {"window": "decision", "evaluated": "O21 (Sep 26 2026), reanalysis 12.0"},
    "RC1D": {"window": f"first 5-minute boundary >= preparation + {LEAD_MIN} min", "evaluated": "none (prospective only)"},
}
_COMMON = {
    "target": "ln(max high / min low) over [start, end); Binance BTCUSDT perp last price",
    "input_cutoff": "4H bars with close <= decision; DVOL candles with available_at <= decision (stale > 6h = missing); calendar as retained (no schedule vintages)",
    "features": "range_model.features_at at the decision; Saturday/Sunday time shares and release count over [start, end)",
    "point": "ln(lr) = OLS fitted value p (B2) or b0 (B0); registered as point = exp(p)",
    "quantiles": "exp(point + fit-residual 10/50/90 quantiles), sorted",
    "baseline": "B0 persistence on the same window",
    "coherence": "none applied; violations reported",
    "losses": "abs_error_log_lr and qlike on the point; pinball and covered_80 on the quantiles",
    "splits": "decision >= period start and target maturity <= period end",
    "model_spec_sha256": "ae6aa254c786d2dd6045fab098c4237dbe8bcc07d6626d20617366d386ff687d",
    "selected": SELECTED,
}


def spec(contract: str) -> dict:
    if contract not in CONTRACTS:
        raise ValueError(f"unknown contract {contract!r}")
    return dict(_COMMON, id=contract, version=VERSION, **CONTRACTS[contract])


def contract_id(contract: str) -> str:
    """The identifier written into every forecast: contract name, implementation version, spec hash prefix."""
    return f"{contract}/{VERSION}/{sha256_json(spec(contract))[:12]}"


def sha256_json(obj) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def ms(t: dt.datetime) -> int:
    return int(t.timestamp() * 1000)


def from_ms(x: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(x / 1000, tz=UTC)


# --------------------------------------------------------------------------------------------
# Windows and calendar terms
# --------------------------------------------------------------------------------------------
def window(contract: str, decision: dt.datetime, horizon: str, prepared: dt.datetime | None = None):
    """(start, end) of the target window."""
    if contract == "RC1":
        start = decision
    elif contract == "RC1D":
        if prepared is None:
            raise ValueError("RC1D needs the preparation time")
        earliest = prepared + dt.timedelta(minutes=LEAD_MIN)
        step = 300
        start = from_ms(-(-ms(earliest) // (step * 1000)) * step * 1000)
    else:
        raise ValueError(contract)
    return start, start + dt.timedelta(hours=HOURS[horizon])


def _day_overlap(start: dt.datetime, end: dt.datetime, weekday: int) -> float:
    total, day = 0.0, dt.datetime(start.year, start.month, start.day, tzinfo=UTC)
    while day < end:
        nxt = day + dt.timedelta(days=1)
        if day.weekday() == weekday:
            total += (min(end, nxt) - max(start, day)).total_seconds()
        day = nxt
    return total


def calendar_terms(start: dt.datetime, end: dt.datetime, releases: list) -> dict:
    """Weekend time shares and scheduled-release count over [start, end). On a 4H-aligned window these equal
    range_model.features_at's bar-count shares exactly (every 4H bar lies inside one UTC day)."""
    span = (end - start).total_seconds()
    return {"sat_share": _day_overlap(start, end, 5) / span, "sun_share": _day_overlap(start, end, 6) / span,
            "releases": bisect.bisect_left(releases, end) - bisect.bisect_left(releases, start)}


def decision_row(history: list, releases: list, dvol_rows, horizon: str, start: dt.datetime, end: dt.datetime):
    """Features at the close of history[-1] with calendar terms for the window actually targeted."""
    series = R.dvol_series(dvol_rows) if dvol_rows else None
    row = R.features_at(history[-R.WARMUP:], releases, series, horizon)
    if row is None:
        return None
    row = dict(row, **calendar_terms(start, end, releases))
    row["start_utc"], row["end_utc"] = iso(start), iso(end)
    return row


# --------------------------------------------------------------------------------------------
# Point, quantiles, events
# --------------------------------------------------------------------------------------------
def values(fit_h: dict, b0_resid_q: list, row: dict) -> dict:
    """{"B2": {"point", "q"}, "B0": {...}} in ln(lr) units. The point is never adjusted."""
    missing = [t for t in R.MODEL_TERMS[fit_h["model"]] if row.get(t) is None]
    if missing:
        raise ValueError(f"inputs missing at the decision: {missing}")
    p = R.predict({"model": fit_h["model"], "beta": fit_h["beta"]}, row)
    return {fit_h["model"]: {"point": p, "q": sorted(p + r for r in fit_h["resid_q"])},
            "B0": {"point": row["b0"], "q": sorted(row["b0"] + r for r in b0_resid_q)}}


def event(name: str, v: dict) -> dict:
    """A registry `range` event in lr units (ln(high/low)), rounded to ROUND decimals."""
    q = [round(math.exp(x), ROUND) for x in v["q"]]
    return {"name": name, "type": "range", "point": round(math.exp(v["point"]), ROUND),
            "q10": q[0], "q50": q[1], "q90": q[2]}


def coherence_violations(points: dict) -> list:
    """Horizon pairs whose ln(lr) points violate nesting (24h < 4h, 72h < 24h). Diagnostic only."""
    out = []
    for a, b in (("4h", "24h"), ("24h", "72h")):
        if a in points and b in points and points[b] < points[a]:
            out.append(f"{b}<{a}")
    return out


# --------------------------------------------------------------------------------------------
# Losses (the single implementation used by evaluation and by scoring.py)
# --------------------------------------------------------------------------------------------
def realized_lr(bars) -> float:
    """ln(max high / min low) from bars given as dicts (high/low) or tuples (t, high, low, close)."""
    hi = max(b["high"] if isinstance(b, dict) else b[1] for b in bars)
    lo = min(b["low"] if isinstance(b, dict) else b[2] for b in bars)
    return math.log(hi / lo)


def losses(point_lr: float, q_lr: list, realized: float) -> dict:
    """All losses of one range event. Inputs in lr units (ln(high/low)); realized > 0 required for the
    log losses (a zero range is recorded with None log losses, never dropped)."""
    out = {"realized_ln_range": round(realized, ROUND), "covered_80": q_lr[0] <= realized <= q_lr[2],
           "pinball": {f"q{k}": round(max(a * (realized - v), (a - 1) * (realized - v)), ROUND)
                       for k, a, v in ((10, .1, q_lr[0]), (50, .5, q_lr[1]), (90, .9, q_lr[2]))},
           "abs_error_lr": round(abs(point_lr - realized), ROUND)}
    if realized > 0:
        x = (realized / point_lr) ** 2
        out.update(abs_error_log_lr=round(abs(math.log(point_lr) - math.log(realized)), ROUND),
                   qlike=round(x - math.log(x) - 1, ROUND))
    else:
        out.update(abs_error_log_lr=None, qlike=None)
    return out


# --------------------------------------------------------------------------------------------
# Fit validation
# --------------------------------------------------------------------------------------------
class FitInvalid(ValueError):
    pass


def calendar_prefix_sha(path: Path, until: dt.datetime) -> str:
    """Hash of the calendar rows released before `until` (a refreshed calendar that only adds later events
    keeps a fit reusable)."""
    rows = [line for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line and not line.startswith("#") and not line.startswith("release_utc")]
    keep = [r for r in rows if r[:20] < iso(until)]
    return hashlib.sha256("\n".join(keep).encode()).hexdigest()


def validate_fit(doc: dict, month_start: dt.datetime, calendar_path: Path, spec_sha: str) -> None:
    """Refuse a fit whose identity, shape or values do not match what this contract expects."""
    def need(cond, msg):
        if not cond:
            raise FitInvalid(msg)

    def finite(xs):
        return all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in xs)

    need(isinstance(doc, dict), "fit is not an object")
    need(doc.get("month") == f"{month_start:%Y-%m}", f"month {doc.get('month')!r} != {month_start:%Y-%m}")
    need(doc.get("refit_utc") == iso(month_start), "refit_utc is not the month start")
    need(doc.get("spec_sha256") == spec_sha, "fit belongs to a different model specification")
    need(doc.get("range_model") == R.VERSION, f"fit range_model {doc.get('range_model')!r} != {R.VERSION}")
    need(doc.get("last_bar") == iso(month_start - dt.timedelta(hours=4)), "training cutoff is not the last bar before the month")
    fits, b0q = doc.get("fits"), doc.get("b0_resid_q")
    need(isinstance(fits, dict) and set(fits) == set(SELECTED), "fits must cover exactly 4h, 24h, 72h")
    need(isinstance(b0q, dict) and set(b0q) == set(SELECTED), "b0_resid_q must cover exactly 4h, 24h, 72h")
    for h, model in SELECTED.items():
        f = fits[h]
        terms = ["const", *R.MODEL_TERMS[model]]
        need(f.get("model") == model, f"{h}: model {f.get('model')!r} != {model}")
        need(list(f.get("terms", [])) == terms, f"{h}: terms not in the specified order")
        beta = f.get("beta")
        need(isinstance(beta, list) and len(beta) == len(terms) and finite(beta), f"{h}: coefficients malformed")
        dropped = f.get("dropped_terms", [])
        need(set(dropped) <= set(terms[1:]) and all(beta[terms.index(t)] == 0 for t in dropped), f"{h}: dropped terms inconsistent")
        need(isinstance(f.get("n"), int) and f["n"] >= 200, f"{h}: training n missing or < 200")
        need(f.get("refit_utc") == iso(month_start), f"{h}: refit time differs from the month start")
        rq = f.get("resid_q")
        need(isinstance(rq, list) and len(rq) == 3 and finite(rq) and rq[0] <= rq[1] <= rq[2], f"{h}: residual quantiles malformed")
        bq = b0q[h]
        need(isinstance(bq, list) and len(bq) == 3 and finite(bq) and bq[0] <= bq[1] <= bq[2], f"{h}: B0 residual quantiles malformed")
    cal_now = hashlib.sha256(Path(calendar_path).read_bytes()).hexdigest()
    if doc.get("calendar_sha256") != cal_now:
        need(doc.get("calendar_prefix_sha256") == calendar_prefix_sha(calendar_path, month_start),
             "calendar changed before the fit's cutoff (or the fit records no calendar prefix)")
    data = doc.get("data") or {}
    need(data.get("klines_worst_state") == "ok" or data.get("supplied") or data.get("chain"),
         "fit history not recorded as ok")
    need(data.get("dvol_state") in ("ok", None) or data.get("dvol_override"), "fit DVOL state not ok and no override recorded")


# --------------------------------------------------------------------------------------------
# Input admissibility (explicit, executable overrides)
# --------------------------------------------------------------------------------------------
OVERRIDES = {
    # name: (loader state it admits, condition, what is recorded)
    "dvol_incomplete_live": "live DVOL window 'incomplete' is admitted only if the candle feeding the decision "
                            "(available_at <= decision, within 6h) is present and no row is malformed or conflicting; "
                            "missing hours are recorded as exclusions",
    "dvol_incomplete_history": "refit DVOL history 'incomplete' is admitted; training rows whose DVOL is missing "
                               "are excluded from B2 (not imputed) and the missing hours are recorded",
}


def admit_dvol(state: str, rows: list, decision: dt.datetime, report: dict, purpose: str) -> dict:
    """Return the admissibility record or raise. `purpose` is 'live' or 'history'."""
    if state == "ok":
        return {"state": "ok", "override": None, "excluded_hours": 0}
    if state in ("malformed", "retrieval_error", "revised", "missing") or (report or {}).get("conflicts"):
        raise ValueError(f"DVOL {state} is not admissible ({purpose})")
    if state == "incomplete":
        if purpose == "live":
            series = R.dvol_series(rows) if rows else None
            if not series or R.dvol_as_of(series, decision) is None:
                raise ValueError("DVOL incomplete and the decision candle is missing")
            return {"state": state, "override": "dvol_incomplete_live", "excluded_hours": report.get("missing_hours")}
        return {"state": state, "override": "dvol_incomplete_history", "excluded_hours": report.get("missing_hours")}
    raise ValueError(f"unknown DVOL state {state!r}")


# --------------------------------------------------------------------------------------------
# Evaluation (RC1): maturity-bounded splits, walk-forward monthly refits, one loss function
# --------------------------------------------------------------------------------------------
PERIODS = {"fit_end": "2024-09-23T00:00:00Z", "validation": ("2024-09-23T00:00:00Z", "2025-09-23T00:00:00Z"),
           "holdout": ("2025-09-23T00:00:00Z", "2026-09-23T00:00:00Z")}


def in_period(row: dict, start: str, end: str) -> bool:
    """Decision inside [start, end) and target matured by end (the outcome never enters a later period)."""
    return (start <= row["decision_utc"] < end and row.get("y") is not None
            and row["target_close_utc"] is not None and row["target_close_utc"] <= end)


def walk_forward(rows: list, model: str, start: str, end: str, b0q_rows=None) -> list:
    """RC1 forecasts for rows in the period. Monthly expanding refits use every target that matured before
    the month began - including earlier outcomes from the evaluated period itself (walk-forward, not a
    never-fitted period)."""
    ev = [r for r in rows if in_period(r, start, end)]
    if model != "B0":
        ev = [r for r in ev if R.usable(r, model)]
    out, fits = [], {}
    for r in ev:
        t = R._t(r["decision_utc"])
        m0 = dt.datetime(t.year, t.month, 1, tzinfo=UTC)
        if model == "B0":
            if m0 not in fits:
                prior = [x["y"] - x["b0"] for x in rows if x.get("y") is not None and x["target_close_utc"] is not None
                         and x["target_close_utc"] <= iso(m0)]
                fits[m0] = R._quantiles(prior) if len(prior) >= 200 else None
            rq = fits[m0]
            p = r["b0"]
            q = sorted(p + x for x in rq) if rq else None
        else:
            if m0 not in fits:
                fits[m0] = R.fit(rows, model, m0)
            fm = fits[m0]
            if fm is None:
                continue
            p = R.predict(fm, r)
            q = sorted(p + x for x in fm["resid_q"])
        out.append({"decision_utc": r["decision_utc"], "target_close_utc": r["target_close_utc"], "y": r["y"],
                    "point": p, "q": q, "refit_utc": iso(m0)})
    return out


def loss_rows(fc: list) -> list:
    """Per-row losses through `losses`, in lr units (the same call scoring.py makes)."""
    out = []
    for r in fc:
        realized = math.exp(r["y"])
        q = [math.exp(x) for x in r["q"]] if r["q"] else [math.exp(r["point"])] * 3
        out.append(dict(r, **losses(math.exp(r["point"]), q, realized)))
    return out


def holm(pvalues: dict) -> dict:
    """Holm-Bonferroni adjusted p-values for a family {name: p}."""
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m, running, out = len(items), 0.0, {}
    for i, (k, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        out[k] = running
    return out
