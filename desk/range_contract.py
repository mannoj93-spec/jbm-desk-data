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
import re
from pathlib import Path

import range_model as R

VERSION = "contract-12.1.0"            # this module's implementation version
CONTRACT_VERSION = "contract-12.0.0"   # the contract's semantic version: unchanged since 12.0, so contract ids
                                       # (and every registered record) stay valid across implementation fixes
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
    return dict(_COMMON, id=contract, version=CONTRACT_VERSION, **CONTRACTS[contract])


def contract_id(contract: str) -> str:
    """The identifier written into every forecast: contract name, implementation version, spec hash prefix."""
    return f"{contract}/{CONTRACT_VERSION}/{sha256_json(spec(contract))[:12]}"


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
    # Contract compatibility (12.1): a fit names the contract it was built under; RC1 and RC1D share one fit
    # procedure, so either is accepted. Pre-12.0 rule: a fit with no contract field is accepted only if it was
    # written by range-job-11.2.0 (the September 2026 fit, built by the same range_model.fit with these terms).
    if "contract" in doc:
        need(doc["contract"] in FIT_COMPATIBLE, f"fit contract {doc['contract']!r} is not compatible with {sorted(FIT_COMPATIBLE)}")
    else:
        need(doc.get("job") == "range-job-11.2.0", "fit has no contract field and is not the known pre-12.0 fit")


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


# --------------------------------------------------------------------------------------------
# Strict RC1D record validation (12.1): the reading, status and scoring boundary. Never raises.
# --------------------------------------------------------------------------------------------
FIT_COMPATIBLE = {contract_id("RC1"), contract_id("RC1D")}
READ_COMPATIBLE = {contract_id("RC1D")}
MAX_START_DELAY_MIN = 70        # decision -> window start: a run <= 60 min late + 5 min lead + 5-minute rounding
_HEX64 = frozenset("0123456789abcdef")


def _hex64(x):
    return isinstance(x, str) and len(x) == 64 and set(x) <= _HEX64


def _num01(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and 0 < x < 1


def _parse(s):
    try:
        return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except (TypeError, ValueError):
        return None


def validate_rc1d(doc, fid=None, entry=None, publication=None, contracts=None) -> list:
    """Semantic checks a hash cannot give: an empty list means the record is a well-formed RC1D forecast.
    Legacy records (range-b2-*, other streams) are not RC1D and are not checked here."""
    errs = []
    if not isinstance(doc, dict):
        return ["document is not an object"]
    fid = fid if fid is not None else doc.get("id")
    m = re.fullmatch(r"range-rc1d-(4h|24h|72h)-(\d{8}T\d{4}Z)", fid if isinstance(fid, str) else "")
    if not m or doc.get("id") != fid:
        return [f"id {fid!r} is not range-rc1d-<4h|24h|72h>-<YYYYmmddTHHMMZ> or differs from the document"]
    h, stamp = m.groups()
    if doc.get("contract") not in (contracts or READ_COMPATIBLE):
        errs.append(f"contract {doc.get('contract')!r} not in {sorted(contracts or READ_COMPATIBLE)}")
    if doc.get("instrument") != "BTCUSDT perp, Binance last price":
        errs.append("instrument mismatch")
    d, s, e, made = (_parse(doc.get(k)) for k in ("decision_utc", "start_utc", "horizon_utc", "made_utc"))
    if None in (d, s, e, made):
        return errs + ["decision/start/horizon/made timestamps missing or malformed"]
    if f"{d:%Y%m%dT%H%MZ}" != stamp:
        errs.append("decision does not match the id")
    if d.minute or d.second or d.hour % 4:
        errs.append("decision is not a 4H close")
    if e - s != dt.timedelta(hours=HOURS[h]):
        errs.append(f"window spans {(e - s).total_seconds() / 3600:g}h, not {h}")
    delay = (s - d).total_seconds() / 60
    if not LEAD_MIN <= delay <= MAX_START_DELAY_MIN or s.minute % 5 or s.second:
        errs.append(f"window start {delay:g} min after the decision (allowed {LEAD_MIN}-{MAX_START_DELAY_MIN}, 5-minute aligned)")
    if not d <= made <= s - dt.timedelta(minutes=LEAD_MIN):
        errs.append("preparation time outside [decision, start - lead]")
    ref = doc.get("reference_price")
    if not (isinstance(ref, (int, float)) and not isinstance(ref, bool) and math.isfinite(ref) and ref > 0):
        errs.append("reference_price not finite and positive")
    if not _hex64(doc.get("input_bundle")) or doc.get("snapshot_hash") != doc.get("input_bundle"):
        errs.append("input_bundle missing, malformed, or different from snapshot_hash")
    evs = doc.get("events")
    if not isinstance(evs, list) or len(evs) != 2:
        errs.append("events must be exactly the B2 and B0 range events")
    else:
        names = []
        for ev in evs:
            if not isinstance(ev, dict) or ev.get("type") != "range" or not isinstance(ev.get("name"), str):
                errs.append("an event is not a named range event")
                continue
            names.append(ev["name"][:2])
            vals = [ev.get(k) for k in ("point", "q10", "q50", "q90")]
            if not all(_num01(v) for v in vals):
                errs.append(f"{ev['name'][:2]}: point and q10/q50/q90 must be finite, in (0, 1)")
            elif not vals[1] <= vals[2] <= vals[3]:
                errs.append(f"{ev['name'][:2]}: quantiles not ordered")
        if sorted(names) != ["B0", "B2"]:
            errs.append(f"events are {names}, not one B2 and one B0")
    if entry is not None:
        if not isinstance(entry, dict):
            errs.append("manifest entry is not an object")
        else:
            if entry.get("id", fid) != fid or entry.get("source") != f"registry/{fid}.json":
                errs.append("manifest id/source inconsistent with the record")
            if not _hex64(entry.get("sha256")) or entry.get("frozen") != f"registry/frozen/{entry.get('sha256')}.json":
                errs.append("manifest hash/frozen path malformed")
            reg = entry.get("registered")
            if not isinstance(reg, int) or isinstance(reg, bool):
                errs.append("registration time missing or malformed")     # lateness is eligibility, not validity
            if not isinstance(entry.get("attempt"), str):
                errs.append("manifest entry has no attempt")
    if publication is not None:
        if not isinstance(publication, dict):
            errs.append("publication record is not an object")
        else:
            conf, ids = publication.get("confirmed"), publication.get("ids")
            if not isinstance(conf, int) or isinstance(conf, bool):
                errs.append("publication confirmation time missing or malformed")
            if not isinstance(ids, list) or fid not in ids:
                errs.append("publication record does not list this forecast")
            if publication.get("start_ms") != ms(s):
                errs.append("publication record's window start differs from the record")
    return errs

