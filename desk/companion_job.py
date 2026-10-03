#!/usr/bin/env python3
"""companion_job — prospective B1 companion forecasts beside the RC1D stream (repo 2.20, stream rc1d-b1).

Why: RC1D registers B2 (HAR/calendar + DVOL) and B0 (persistence) only, and its validator expects exactly those
model identities, so B2-vs-B0 cannot say how much of B2's accuracy comes from DVOL. B1 is B2 without the DVOL term
(range_model.MODEL_TERMS["B1"], the model O21 evaluated as the middle step). This job registers a B1 point and
interval for every RC1D decision and horizon, on the SAME decision, input snapshot, calendar terms and target
window, in a separate registry, and never touches registry/, the manifest or the RC1D contract.

  fit       once per month, after the RC1D refit for that month exists: fit B1 per horizon on the retained
            history chain, using only targets that closed at or before the month start (R.fit's cutoff) -
            the same information cutoff as the month's B2 fit. streams/rc1d-b1/fits/YYYY-MM.json.
  forecast  for the latest 4H decision: read the registered RC1D records (verified), take the features their
            bundle froze for each window, compute B1, and register it - only while at least MIN_MARGIN_S remain
            before the window start. Too late = missed, recorded as missed, never computed later.
  confirm   after the workflow pushed: verify each new companion file on origin/main by hash; eligible only if
            prepared and confirmed before the window start (the RC1D rule, range_contract.eligibility).
  score     when the RC1D record for the same window is scored, apply range_contract.losses to the B1 point
            with the realized range that record carries (identical window, identical loss function).
  report    reports/companion_b1.{json,md}: B2 vs B1 beside B2 vs B0 on the same paired set (rc1d-eval-1 rules).

1.1.0 (repo 2.21): confirmations carry an integrity binding (forecast hash, decision time, version, input snapshot,
contract, confirmation time and commit); scoring and reporting verify it and exclude anything changed, recording the
failure and leaving the original in place; the stream has an explicit lifecycle (streams/rc1d-b1/lifecycle.jsonl):
termination is the operator's, stops new forecasts at once, and never deletes history. Forecast values, fits, the
loss function and the evaluation method are unchanged.

1.3.0 (repo 2.23): a missing binding no longer grants legacy status. Only the three confirmations written by
companion-1.0.0 before bindings existed (LEGACY_UNBOUND: ids, row hashes and registry hashes as first committed in
4ffe647d, 2026-10-01T00:23:06Z) verify without one, and only while byte-identical to that history; any other
confirmation with an absent, null, malformed or inconsistent binding fails consumption. Report clocks are named
(generated, processed, observation cutoff, latest outcome-window end); see report_clocks().

Stdlib only. Network: git only (confirmation). Records: streams/rc1d-b1/.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import os
import sys
from pathlib import Path

DESK = Path(__file__).resolve().parent
CODE = DESK.parent
BASE = Path(os.environ.get("JBM_DESK_BASE") or CODE)  # records root ($JBM_DESK_BASE in tests)
for p in (str(DESK), str(CODE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import range_model as R          # noqa: E402
import range_contract as C       # noqa: E402
import stream_util as U          # noqa: E402

VERSION = "companion-1.3.0"
STREAM = "rc1d-b1"
MODEL = "B1"
ROOT = "streams/rc1d-b1"
FORECASTS, REGISTRY, ATTEMPTS = f"{ROOT}/forecasts", f"{ROOT}/registry.jsonl", f"{ROOT}/attempts.jsonl"
CONFIRMS, SCORES, FITS = f"{ROOT}/confirmations.jsonl", f"{ROOT}/scores.jsonl", f"{ROOT}/fits"
ID_PREFIX = "rc1d-b1-"
RC1D_PREFIX = "range-rc1d-"
HORIZONS = ("4h", "24h", "72h")
MIN_MARGIN_S = C.MIN_MARGIN_S            # 120 s, the RC1D freezing margin
EVAL_METHOD = "companion-eval-1 (2026-09-30): rc1d-eval-1 applied to B2 vs B1 on eligible paired windows"
LIFECYCLE_KEY = "rc1d-b1/companion-1"       # the stream; it has been active since its first registration (2026-10-01)
LIFECYCLE_DEFAULT = "active"


def _say(msg):
    import os
    if not os.environ.get("RANGE_JOB_QUIET"):
        print(msg)


def _attempt(base, row):
    U.append(Path(base) / ATTEMPTS, row, key=lambda r: (r["id"], r["state"], r["t_ms"]))
    _say(f"companion {row['id']}: {row['state']}" + (f" ({row['reason']})" if row.get("reason") else ""))


def lifecycle(base) -> tuple:
    rows = U.lifecycle_rows(base, ROOT, LIFECYCLE_KEY)
    return U.lifecycle_state(base, ROOT, LIFECYCLE_KEY, LIFECYCLE_DEFAULT), (rows[-1] if rows else None)


def terminated_ms(base):
    """When the operator terminated the stream (lifecycle row time, or the marker file's recorded time), else None."""
    for r in U.lifecycle_rows(base, ROOT, LIFECYCLE_KEY):
        if r.get("state") == "terminated":
            return r["t_ms"]
    marker = Path(base) / ROOT / "terminated.json"
    if marker.exists():                                # a marker without a time: forecasting already refuses, so
        try:                                           # nothing registered after it exists to exclude
            t = json.loads(marker.read_text()).get("t_ms")
            return int(t) if isinstance(t, int) else None
        except (ValueError, AttributeError):
            return None
    return None


def operator_lifecycle(new: str, reason: str, base=BASE) -> dict:
    return U.transition(base, ROOT, LIFECYCLE_KEY, new, by="operator", reason=reason, default=LIFECYCLE_DEFAULT)


# --------------------------------------------------------------------------------------------
# Integrity binding
# --------------------------------------------------------------------------------------------
def binding(reg: dict, cdoc: dict, confirmed_ms: int, commit: str) -> dict:
    return {"record_sha256": reg["sha256"], "id": reg["id"], "decision_utc": reg["decision_utc"],
            "prepared_ms": reg["prepared_ms"], "start_ms": reg["start_ms"],
            "version": {"stream": cdoc.get("stream"), "job": cdoc.get("version"), "model": cdoc.get("model"),
                        "fit": cdoc.get("fit")},
            "input_snapshot": {"rc1d_id": cdoc.get("rc1d_id"), "rc1d_frozen_sha256": cdoc.get("rc1d_frozen_sha256"),
                               "snapshot_hash": cdoc.get("snapshot_hash")},
            "contract": cdoc.get("contract"), "confirmed_ms": confirmed_ms, "commit": commit}


# The genuine unbound cohort: confirmations written by companion-1.0.0 before bindings existed, pinned to their
# first committed bytes (commit 4ffe647df588861c33bcd3e2431794b9c77f9341, streams/rc1d-b1/confirmations.jsonl lines
# 1-3; U.sha of each row equals the sha256 of its canonical line). id -> (confirmation row sha, registry forecast sha).
LEGACY_UNBOUND = {
    "rc1d-b1-4h-20261001T0000Z": ("4f28e567660b7435bf3ac7b411a6d7e7677c14cc10a8af7a0b0dbd77d7621d2f",
                                  "c0ccdd023f0ec0108215cad8a955e1f26054aea0f52a90b7de54fc8c1ae361df"),
    "rc1d-b1-24h-20261001T0000Z": ("5c7c4e2d846604520872b0f413dcf08b4c7d1a457af917649558e26bbfc3a9f2",
                                   "b68df6a9253bb7fa48524e0b5b700fa417afb38ba692c6ba2e822576427e5f03"),
    "rc1d-b1-72h-20261001T0000Z": ("9b59270d1c971d24ce5ae9552bd41ef96200c6a5f97df924a7faefec70fdd702",
                                   "cc5149aa1277a229860efb30324f904b2716d8c6714fc644140e86d6b6aed057"),
}
LEGACY_LIMITATION = ("legacy confirmation (companion-1.0.0, before integrity bindings): verified against its pinned "
                     "first-committed bytes and the registry hash; its confirmation time carries no binding of its own")


def verify(base, reg: dict, conf: dict) -> tuple:
    """(ok, reason, forecast doc). The forecast bytes must hash to the registry row; every confirmation must carry
    a well-formed binding that matches the record, except the pinned legacy cohort (LEGACY_UNBOUND), which must be
    byte-identical to its first committed row and name the pinned registry hash and the 1.0.0 identity. A version
    label alone, or a binding stripped from a modern confirmation, never grants legacy status."""
    base = Path(base)
    path = base / reg["path"]
    if not path.exists():
        return False, "forecast file missing", None
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != reg["sha256"]:
        return False, "forecast file changed after registration", None
    cdoc = json.loads(raw)
    if cdoc.get("id") != reg["id"] or cdoc.get("rc1d_id") != reg["rc1d_id"] or cdoc.get("decision_utc") != reg["decision_utc"]:
        return False, "forecast identity differs from the registry row", None
    eligible = reg["prepared_ms"] < reg["start_ms"] and conf.get("confirmed_ms", 1 << 62) < reg["start_ms"]
    if conf.get("start_ms") != reg["start_ms"] or bool(conf.get("eligible")) != eligible:
        return False, "confirmation times or eligibility differ from the registry row", None
    has_b, has_h = "binding" in conf, "binding_sha256" in conf
    if not has_b and not has_h:
        pin = LEGACY_UNBOUND.get(reg["id"])
        if pin is None:
            return False, "confirmation binding missing (only the pinned companion-1.0.0 cohort is unbound)", None
        if U.sha(conf) != pin[0]:
            return False, "unbound legacy confirmation differs from its first committed bytes", None
        if reg["sha256"] != pin[1] or reg.get("job") != "companion-1.0.0" or cdoc.get("version") != "companion-1.0.0":
            return False, "unbound legacy confirmation does not match its pinned registry identity", None
        return True, LEGACY_LIMITATION, cdoc
    b = conf.get("binding")
    if not isinstance(b, dict) or not isinstance(conf.get("binding_sha256"), str):
        return False, "confirmation binding missing, null or malformed", None
    if conf.get("binding_sha256") != U.sha(b):
        return False, "confirmation binding altered", None
    want = binding(reg, cdoc, conf.get("confirmed_ms"), conf.get("commit"))
    for k in want:
        if want[k] != b.get(k):
            return False, f"record differs from its confirmation binding ({k})", None
    return True, "verified", cdoc


# --------------------------------------------------------------------------------------------
# Monthly fit
# --------------------------------------------------------------------------------------------
def fit_path(base, month: str) -> Path:
    return Path(base) / FITS / f"{month}.json"


def build_fit(bars, dvol, releases, m0: dt.datetime) -> dict:
    """B1 per horizon on rows whose targets closed at or before m0. Pure. Raises on any input after m0."""
    late = [b["open_utc"] for b in bars if R._t(b["open_utc"]) >= m0]
    if late:
        raise ValueError(f"fit input at or after the month start: {late[:2]}")
    panel = R.build_panel(bars, releases, dvol)
    fits = {}
    for h in HORIZONS:
        fm = R.fit(panel[h], MODEL, m0)
        if fm is None:
            raise RuntimeError(f"companion fit {h}: too few rows")
        used = [r for r in panel[h] if R.usable(r, MODEL) and r["target_close_utc"] <= U.iso(m0)]
        fits[h] = {"model": MODEL, "beta": fm["beta"], "terms": list(fm["terms"]), "n": fm["n"],
                   "dropped_terms": fm["dropped_terms"], "resid_q": fm["resid_q"], "refit_utc": fm["refit_utc"],
                   "last_target_close_utc": max(r["target_close_utc"] for r in used)}
    return fits


def fit(base=BASE, now=None) -> Path | None:
    """Validate or build this month's companion fit. Refuses (returns None) until the RC1D fit for the month
    exists, so both models see the same retained history chain."""
    import range_job as J
    now = now or dt.datetime.now(U.UTC)
    m0 = dt.datetime(now.year, now.month, 1, tzinfo=U.UTC)
    month = f"{m0:%Y-%m}"
    path = fit_path(base, month)
    if path.exists():
        validate_fit(json.loads(path.read_text()), m0)
        _say(f"companion fit {month}: exists and validates")
        return path
    b2 = J.fit_path(m0.date(), base)
    if not b2.exists():
        _say(f"companion fit {month}: waiting for the RC1D fit {b2.name}")
        return None
    J.load_fit(base, m0)                                   # the B2 fit must itself validate
    releases, cal_sha = J.calendar()
    bars, dvol, links = J.history_chain(base)
    bars = [b for b in bars if R._t(b["open_utc"]) < m0]
    dvol = [r for r in dvol if R._t(r["open_utc"]) < m0]
    times = [R._t(b["open_utc"]) for b in bars]
    gaps = sum(1 for a, b in zip(times, times[1:]) if b - a != dt.timedelta(hours=4))
    if gaps or times[-1] != m0 - dt.timedelta(hours=4):
        raise RuntimeError(f"companion fit: history not contiguous to {month} (gaps={gaps}, last={times[-1]})")
    doc = {"stream": STREAM, "version": VERSION, "month": month, "refit_utc": U.iso(m0), "model": MODEL,
           "range_model": R.VERSION, "fits": build_fit(bars, dvol, releases, m0), "calendar_sha256": cal_sha,
           "chain": links, "bars": len(bars), "last_bar": bars[-1]["open_utc"],
           "rc1d_fit_sha256": U.file_sha(b2), "built_ms": U.clock_ms(),
           "cutoff_rule": "R.fit: rows whose target closed at or before refit_utc (the month's B2 fit uses the same rule)"}
    validate_fit(doc, m0)
    from storage import atomic_bytes
    atomic_bytes(path, (json.dumps(doc, indent=1, sort_keys=True) + "\n").encode())
    _say(f"companion fit {month}: written (n={ {h: f['n'] for h, f in doc['fits'].items()} })")
    return path


def validate_fit(doc: dict, m0: dt.datetime) -> None:
    if doc.get("month") != f"{m0:%Y-%m}" or doc.get("model") != MODEL or doc.get("refit_utc") != U.iso(m0):
        raise ValueError("companion fit: month, model or refit time mismatch")
    for h in HORIZONS:
        f = (doc.get("fits") or {}).get(h) or {}
        if f.get("model") != MODEL or tuple(f.get("terms", ())) != ("const",) + R.MODEL_TERMS[MODEL]:
            raise ValueError(f"companion fit {h}: terms are not B1's")
        if not f.get("last_target_close_utc") or f["last_target_close_utc"] > U.iso(m0):
            raise ValueError(f"companion fit {h}: a training target closed after the month start")
        if len(f.get("beta", [])) != len(R.MODEL_TERMS[MODEL]) + 1 or len(f.get("resid_q", [])) != 3:
            raise ValueError(f"companion fit {h}: malformed coefficients")


# --------------------------------------------------------------------------------------------
# Forecast
# --------------------------------------------------------------------------------------------
def companion_id(h: str, decision: dt.datetime) -> str:
    return f"{ID_PREFIX}{h}-{decision:%Y%m%dT%H%MZ}"


def values(fit_h: dict, features: dict) -> dict:
    """B1 point (ln lr) and residual-quantile interval from the features the RC1D bundle froze for the window."""
    missing = [t for t in R.MODEL_TERMS[MODEL] if features.get(t) is None]
    if missing:
        raise ValueError(f"features missing: {missing}")
    p = R.predict({"model": MODEL, "beta": fit_h["beta"]}, features)
    return {"point": p, "q": sorted(p + r for r in fit_h["resid_q"])}


def registered(base) -> dict:
    return {r["id"]: r for r in U.rows(Path(base) / REGISTRY)}


def forecast(base=BASE, now=None, clock=U.clock_ms, run=None) -> list:
    """Register B1 companions for the latest decision's RC1D records. Returns the ids registered now."""
    base = Path(base)
    now = now or dt.datetime.now(U.UTC)
    run = run or U.run_meta()
    st, last = lifecycle(base)
    if not (st in ("approved", "active") or (st == "paused" and (last or {}).get("by") == "job")):
        _say(f"companion forecast refused: lifecycle {st}")
        return []
    decision = U.boundary(now)
    done = registered(base)
    closed = {r["id"] for r in U.rows(base / ATTEMPTS) if r["state"] in ("missed", "abandoned", "refused")}
    out = []
    for h in HORIZONS:
        cid, rid = companion_id(h, decision), f"{RC1D_PREFIX}{h}-{decision:%Y%m%dT%H%MZ}"
        if cid in done or cid in closed:            # a missed companion stays missed; retries add nothing
            continue
        t0 = clock()
        base_row = {"id": cid, "rc1d_id": rid, "decision_utc": U.iso(decision), "t_ms": t0, "job": VERSION, "run": run}
        try:
            doc, entry, _ = U.rc1d_record(base, rid)
            bundle = U.rc1d_bundle(base, doc)
        except (U.RecordUnavailable, OSError, ValueError) as exc:
            _attempt(base, dict(base_row, state="missed", code="rc1d-unavailable", reason=f"RC1D record unavailable: {exc}"[:300]))
            continue
        start_ms = U.ms(U.parse(doc["start_utc"]))
        if start_ms - t0 < MIN_MARGIN_S * 1000:
            gap = (start_ms - t0) / 1000
            where = f"{gap:.0f}s before the window start" if gap >= 0 else f"{-gap:.0f}s after the window start"
            _attempt(base, dict(base_row, state="missed", code="late", start_ms=start_ms,
                                reason=f"reached {where} (margin {MIN_MARGIN_S}s); not computed - a late companion is never registered"))
            continue
        month = f"{decision:%Y-%m}"
        fpath = fit_path(base, month)
        try:
            fdoc = json.loads(fpath.read_text())
            validate_fit(fdoc, dt.datetime(decision.year, decision.month, 1, tzinfo=U.UTC))
            v = values(fdoc["fits"][h], bundle["features"][h])
        except (OSError, ValueError, KeyError) as exc:
            _attempt(base, dict(base_row, state="missed", code="no-fit", start_ms=start_ms, reason=f"no usable companion fit/features: {exc}"[:300]))
            continue
        prepared = clock()
        q = [round(math.exp(x), C.ROUND) for x in v["q"]]
        fdoc_raw = fpath.read_bytes()
        cdoc = {"id": cid, "stream": STREAM, "version": VERSION, "model": f"B1 HAR/calendar ({R.VERSION} terms, no DVOL)",
                "rc1d_id": rid, "rc1d_frozen_sha256": entry["sha256"], "decision_utc": doc["decision_utc"],
                "snapshot_hash": doc["snapshot_hash"], "contract": entry.get("contract") or doc.get("contract"),
                "start_utc": doc["start_utc"], "horizon_utc": doc["horizon_utc"],
                "instrument": doc["instrument"], "fit": {"month": month, "sha256": hashlib.sha256(fdoc_raw).hexdigest()},
                "point": round(math.exp(v["point"]), C.ROUND), "q10": q[0], "q50": q[1], "q90": q[2],
                "made_utc": U.iso_ms(prepared),
                "note": "Companion benchmark: same decision, snapshot, calendar terms and window as the RC1D record. "
                        "point = exp(OLS fit value) in ln(high/low) units, loss-bearing; q = point x exp(residual "
                        "quantiles). Not part of contract RC1D; not a direction, probability or position size."}
        from storage import atomic_bytes
        raw = U.canonical(cdoc) + b"\n"
        rel = f"{FORECASTS}/{cid}.json"
        if (base / rel).exists():
            _attempt(base, dict(base_row, state="refused", code="orphan-file", reason="file exists without a registry row; not overwritten"))
            continue
        atomic_bytes(base / rel, raw)
        frozen = clock()
        if start_ms - frozen < MIN_MARGIN_S * 1000:
            (base / rel).unlink()
            _attempt(base, dict(base_row, state="abandoned", code="late", start_ms=start_ms, reason="freezing margin passed during preparation"))
            continue
        U.append(base / REGISTRY, {"id": cid, "rc1d_id": rid, "path": rel, "sha256": hashlib.sha256(raw).hexdigest(),
                                   "prepared_ms": prepared, "frozen_ms": frozen, "start_ms": start_ms,
                                   "decision_utc": doc["decision_utc"], "horizon": h, "job": VERSION, "run": run},
                 key=lambda r: (r["id"],))
        _attempt(base, dict(base_row, state="frozen", start_ms=start_ms, t_ms=frozen))
        out.append(cid)
    return out


def confirm(base=BASE, clock=U.clock_ms, remote=U.remote_sha) -> list:
    """Confirm each frozen, unconfirmed companion on origin/main by hash. Eligibility is fixed at the first
    confirmation: prepared and confirmed strictly before the window start."""
    base = Path(base)
    have = {r["id"] for r in U.rows(base / CONFIRMS)}
    out = []
    for cid, r in registered(base).items():
        if cid in have:
            continue
        commit, got = remote(r["path"])
        t = clock()
        if got != r["sha256"]:
            _say(f"companion confirm: {cid} not on the remote yet")
            continue
        try:
            cdoc = json.loads((base / r["path"]).read_bytes())
        except (OSError, ValueError):
            continue
        b = binding(r, cdoc, t, commit)
        row = {"id": cid, "commit": commit, "confirmed_ms": t, "start_ms": r["start_ms"],
               "eligible": r["prepared_ms"] < r["start_ms"] and t < r["start_ms"],
               "method": "git fetch origin; file sha256 matches the registry row; bound",
               "binding": b, "binding_sha256": U.sha(b)}
        U.append(base / CONFIRMS, row, key=lambda x: (x["id"],))
        out.append(row)
    return out


# --------------------------------------------------------------------------------------------
# Scoring and report
# --------------------------------------------------------------------------------------------
def _rc1d_scores(base) -> dict:
    out = {}
    for r in U.rows(Path(base) / "registry/scores.jsonl"):
        if str(r.get("id", "")).startswith(RC1D_PREFIX) and r.get("id") not in out:
            out[r["id"]] = r
    return out


class Unscored(Exception):
    """The RC1D window has no score row yet (an expected state, not an integrity failure)."""


def rc1d_outcome(base, rid: str, scores: dict) -> dict:
    """The realized range and B2/B0 losses of one RC1D window, verified against original records: the score row
    names the manifest's frozen forecast, its evidence file hashes to the hash recorded at scoring, the realized
    range recomputes from that evidence, and the B2/B0 losses recompute from the frozen forecast. Raises
    Unscored when there is no score row, U.RecordUnavailable on any mismatch."""
    from storage import digest
    s = scores.get(rid)
    if not s or s.get("status") not in (None, "scored"):
        raise Unscored(rid)
    doc, entry, _ = U.rc1d_record(base, rid)
    if s.get("forecast_sha256") != entry.get("sha256"):
        raise U.RecordUnavailable(f"{rid}: score row names another forecast")
    ev_path = Path(base) / str(s.get("evidence", ""))
    if not s.get("evidence") or not ev_path.is_file():
        raise U.RecordUnavailable(f"{rid}: score evidence missing")
    raw = ev_path.read_bytes()
    ev = json.loads(raw)
    if s.get("evidence_sha256") not in (hashlib.sha256(raw).hexdigest(), digest(ev)):
        raise U.RecordUnavailable(f"{rid}: score evidence does not hash to the recorded value")
    realized = C.realized_lr(ev["price_bars"])
    events = s.get("events") or []
    if len(events) != len(doc.get("events") or []):
        raise U.RecordUnavailable(f"{rid}: score events do not match the forecast")
    errs = {}
    for e, se in zip(doc["events"], events):
        L = C.losses(e["point"], [e["q10"], e["q50"], e["q90"]], realized)
        if se.get("realized_ln_range") != L["realized_ln_range"] or se.get("abs_error_log_lr") != L["abs_error_log_lr"]:
            raise U.RecordUnavailable(f"{rid}: score row differs from the losses its evidence reproduces")
        errs[str(e.get("name", ""))[:2]] = L["abs_error_log_lr"]
        carried = L["realized_ln_range"]                # the realized range as the record carries it (rounded)
    if "B2" not in errs or "B0" not in errs:
        raise U.RecordUnavailable(f"{rid}: B2 or B0 event missing")
    return {"realized": carried, "B2": errs["B2"], "B0": errs["B0"],
            "eligible": bool((s.get("publication") or {}).get("eligible")), "score_sha256": U.sha(s),
            "scored_ms": s.get("scored")}


def verified_pair(base, cid: str, reg: dict, conf: dict | None, scores: dict) -> dict:
    """The one consumption path for a companion: forecast + confirmation (verify), the RC1D outcome
    (rc1d_outcome), and the B1 loss recomputed from both. Returns {state, ...}: 'ok' (with companion_eligible),
    'unscored', or 'integrity' (reason)."""
    if conf is None:
        return {"state": "integrity", "reason": "confirmation missing"}
    ok, why, cdoc = verify(base, reg, conf)
    if not ok:
        return {"state": "integrity", "reason": why}
    try:
        out = rc1d_outcome(base, reg["rc1d_id"], scores)
    except Unscored:
        return {"state": "unscored"}
    except (U.RecordUnavailable, OSError, ValueError, KeyError) as exc:
        return {"state": "integrity", "reason": f"RC1D outcome: {exc}"}
    loss = C.losses(cdoc["point"], [cdoc["q10"], cdoc["q50"], cdoc["q90"]], out["realized"])
    return {"state": "ok", "verification": why, "cdoc": cdoc, "outcome": out, "B1": loss,
            "companion_eligible": bool(conf.get("eligible")),
            "start_ms": reg["start_ms"], "end_ms": U.ms(U.parse(cdoc["horizon_utc"])),
            "inputs_sha256": U.sha({"forecast_sha256": reg["sha256"], "rc1d_score_sha256": out["score_sha256"],
                                    "realized_ln_range": out["realized"]})}


def _score_matches(row: dict, vp: dict) -> bool:
    return (row.get("inputs_sha256") in (None, vp["inputs_sha256"])
            and row.get("realized_ln_range") == vp["outcome"]["realized"]
            and (row.get("B1") or {}).get("abs_error_log_lr") == vp["B1"]["abs_error_log_lr"]
            and row.get("B2_abs_error_log_lr") == vp["outcome"]["B2"]
            and row.get("B0_abs_error_log_lr") == vp["outcome"]["B0"])


def score(base=BASE, now_ms=None) -> dict:
    """Score confirmed companions whose RC1D twin is scored, through verified_pair. Returns
    {'scored': [...], 'integrity': [...], 'unscored': n}."""
    base = Path(base)
    have = {r["id"] for r in U.rows(base / SCORES)}
    conf = {}
    for r in U.rows(base / CONFIRMS):
        conf.setdefault(r["id"], r)
    rc = _rc1d_scores(base)
    out = {"scored": [], "integrity": [], "unscored": 0}
    t_end = terminated_ms(base)
    for cid, reg in registered(base).items():
        if cid in have or cid not in conf:
            continue
        if t_end is not None and reg["frozen_ms"] >= t_end:
            continue                                   # registered at or after termination: never scored
        vp = verified_pair(base, cid, reg, conf[cid], rc)
        if vp["state"] == "unscored":
            out["unscored"] += 1
            continue
        if vp["state"] == "integrity":
            U.integrity_failure(base, ROOT, f"companion {cid}", vp["reason"], expected=reg["sha256"])
            out["integrity"].append({"id": cid, "reason": vp["reason"]})
            continue
        o = vp["outcome"]
        row = {"id": cid, "rc1d_id": reg["rc1d_id"], "decision_utc": reg["decision_utc"], "horizon": reg["horizon"],
               "companion_eligible": conf[cid]["eligible"], "rc1d_eligible": o["eligible"],
               "realized_ln_range": o["realized"], "B1": vp["B1"],
               "B2_abs_error_log_lr": o["B2"], "B0_abs_error_log_lr": o["B0"],
               "loss_function": "range_contract.losses (the RC1D scorer's function)", "job": VERSION,
               "forecast_sha256": reg["sha256"], "rc1d_score_sha256": o["score_sha256"],
               "inputs_sha256": vp["inputs_sha256"], "verification": vp["verification"]}
        U.append(base / SCORES, row, key=lambda x: (x["id"],))
        out["scored"].append(row)
    return out


def disjoint_windows(windows: list) -> int:
    """Largest set of pairwise non-overlapping [start, end) windows - range_reader's shared implementation."""
    import range_reader as RR
    return RR.disjoint_windows(windows)


def overlapping_windows(windows: list) -> int:
    """Windows overlapping at least one other - range_reader's shared implementation."""
    import range_reader as RR
    return RR.overlapping_windows(windows)


REPORT_CLOCKS = {
    "generated_utc": "when this report file was written",
    "processed_utc": "latest scoring time of an included pair (processing, not observation)",
    "source_cutoff_utc": "latest market observation the figures depend on: the latest outcome-window end of an included "
                         "verified pair (repo 2.23; 2.20-2.22 put the scoring time here)",
    "outcome_window_end_utc": "the same window end, named; null with no included pair (expected before maturity)"}
COMPARISONS = (("B2_vs_B1", "B2", "B1"), ("B2_vs_B0", "B2", "B0"), ("B1_vs_B0", "B1", "B0"))
WITHHELD = "withheld: integrity failure in this horizon (records preserved; see integrity_failures)"


def evaluation(base=BASE) -> dict:
    """Per horizon, through verified_pair only: RC1D windows scored, companions missing/late/unscored/excluded,
    actual-window overlap, and paired differences on the eligible verified pairs (rc1d-eval-1 block rules).
    A horizon with any integrity failure withholds every performance figure; counts stay visible."""
    import range_reader as RR
    base = Path(base)
    rc = _rc1d_scores(base)
    reg = registered(base)
    conf = {}
    for r in U.rows(base / CONFIRMS):
        conf.setdefault(r["id"], r)
    cached = {}
    for r in U.rows(base / SCORES):
        cached.setdefault(r["id"], r)
    first = min((r["decision_utc"] for r in reg.values()), default=None)
    out, failures, cutoff, window_end = {}, [], 0, 0
    for h in HORIZONS:
        rids = sorted(k for k in rc if k.startswith(f"{RC1D_PREFIX}{h}-") and first
                      and k[len(RC1D_PREFIX) + len(h) + 1:] >= U.parse(first).strftime("%Y%m%dT%H%MZ"))
        pairs, cnt = [], {"rc1d_scored_since_start": len(rids), "rc1d_not_eligible": 0, "missing_companion": 0,
                          "late_companion": 0, "unscored": 0, "excluded_integrity": 0}
        for rid in rids:
            cid = ID_PREFIX + rid[len(RC1D_PREFIX):]
            if cid not in reg:
                cnt["missing_companion"] += 1
                continue
            vp = verified_pair(base, cid, reg[cid], conf.get(cid), rc)
            if vp["state"] == "integrity":
                cnt["excluded_integrity"] += 1
                failures.append({"id": cid, "reason": vp["reason"]})
                U.integrity_failure(base, ROOT, f"companion {cid}", vp["reason"], expected=reg[cid]["sha256"])
                continue
            if vp["state"] == "ok" and not vp["companion_eligible"]:
                cnt["late_companion"] += 1
                continue
            if vp["state"] == "unscored":
                cnt["unscored"] += 1
                continue
            if not vp["outcome"]["eligible"]:
                cnt["rc1d_not_eligible"] += 1
                continue
            row = cached.get(cid)
            if row is None:
                cnt["unscored"] += 1
                continue
            if not _score_matches(row, vp):
                cnt["excluded_integrity"] += 1
                failures.append({"id": cid, "reason": "cached score differs from its verified inputs"})
                U.integrity_failure(base, ROOT, f"companion {cid}", "cached score differs from its verified inputs",
                                    expected=vp["inputs_sha256"], found=row.get("inputs_sha256"))
                continue
            cutoff = max(cutoff, vp["outcome"]["scored_ms"] or 0)
            window_end = max(window_end, vp["end_ms"] or 0)
            pairs.append({"decision_utc": reg[cid]["decision_utc"], "B2": vp["outcome"]["B2"], "B1": vp["B1"]["abs_error_log_lr"],
                          "B0": vp["outcome"]["B0"], "window": (vp["start_ms"], vp["end_ms"])})
        wins = [p["window"] for p in pairs]
        entry = dict(cnt, paired=len(pairs),
                     windows={"verified_pairs": len(pairs), "largest_disjoint_subset": disjoint_windows(wins),
                              "overlapping_another": overlapping_windows(wins),
                              "basis": "actual [start, end) windows of the verified pairs; all valid pairs stay in the "
                                       "registered analysis - the disjoint count describes dependence, it selects nothing"},
                     overlap_warning=(f"{overlapping_windows(wins)} of {len(pairs)} windows overlap another; the largest "
                                      f"disjoint subset has {disjoint_windows(wins)}") if overlapping_windows(wins) else None,
                     metric="absolute error of ln range (log units); a negative difference favours the first model")
        if cnt["excluded_integrity"]:
            for name, _, _ in COMPARISONS:
                entry[name] = {"withheld": WITHHELD}
            out[h] = entry
            continue
        for name, a, b in COMPARISONS:
            d = [p[a] - p[b] for p in pairs]
            n = len(d)
            if not n:
                entry[name] = {"first": a, "second": b, "n": 0}
                continue
            blocks = n // RR.EVAL_BLOCK
            e = {"first": a, "second": b, "n": n, "diff_mean": round(sum(d) / n, 5),
                 "diff_median": round(RR._quantile(d, 0.5), 5),
                 "first_better": sum(x < -1e-12 for x in d), "ties": sum(abs(x) <= 1e-12 for x in d),
                 "first_worse": sum(x > 1e-12 for x in d), "resampling_blocks": blocks}
            mi, mj = sum(p[a] for p in pairs) / n, sum(p[b] for p in pairs) / n
            sd = math.sqrt(sum((x - sum(d) / n) ** 2 for x in d) / (n - 1)) if n > 1 else None
            e["effect"] = {"mae_first": round(mi, 5), "mae_second": round(mj, 5),
                           "relative_mae_reduction": round(1 - mi / mj, 4) if mj > 0 else None,
                           "standardized_mean_diff": round(sum(d) / n / sd, 4) if sd else None}
            if blocks >= RR.EVAL_MIN_BLOCKS:
                e["diff_mean_ci95"] = [round(x, 5) for x in RR._bootstrap_mean(d, RR.EVAL_BLOCK, RR.EVAL_RESAMPLES, RR.EVAL_SEED)]
            else:
                e["diff_mean_ci95"] = None
                e["uncertainty"] = f"unavailable: {blocks} complete resampling block(s) of {RR.EVAL_BLOCK}; needs {RR.EVAL_MIN_BLOCKS}"
            entry[name] = e
        out[h] = entry
    return {"method": EVAL_METHOD, "schema": "companion-eval-2", "stream_start_decision_utc": first, "horizons": out,
            "integrity_failures_now": failures, "processed_ms": cutoff or None,
            "outcome_window_end_ms": window_end or None,
            "uncertainty_method": f"moving-block bootstrap of paired differences, blocks of {RR.EVAL_BLOCK} decisions "
                                  f"(a resampling device for dependence, not a measured effective sample size), "
                                  f"{RR.EVAL_RESAMPLES} resamples, seed {RR.EVAL_SEED}, 95% interval; reported only from "
                                  f"{RR.EVAL_MIN_BLOCKS} blocks",
            "baselines": {"B2_vs_B1": "does DVOL add to HAR/calendar", "B2_vs_B0": "B2 vs persistence on the same windows",
                          "B1_vs_B0": "HAR/calendar vs persistence"},
            "note": "Descriptive. B2 vs B0 here is restricted to windows with an eligible companion, so it can differ "
                    "from reports/range_status.json (all eligible RC1D windows). Overlapping windows are dependent."}


def report(base=BASE, now_ms=None) -> dict:
    base = Path(base)
    now_ms = now_ms or U.clock_ms()
    ev = evaluation(base)
    att = U.rows(base / ATTEMPTS)
    missed = {}
    for r in att:
        if r["state"] in ("missed", "abandoned", "refused"):
            key = r.get("code") or r["state"]
            missed[key] = missed.get(key, 0) + 1
    life, last = lifecycle(base)
    integrity = U.rows(base / ROOT / "integrity.jsonl")
    hz = ev["horizons"].values()
    ok = not ev["integrity_failures_now"]
    any_ci = any((e.get("B2_vs_B1") or {}).get("diff_mean_ci95") for e in hz)
    any_pair = any(e.get("paired") for e in hz)
    klass = ("unavailable" if not ok else "retired" if life in ("terminated", "archived") else
             "exploratory" if any_ci else "descriptive" if any_pair else "unavailable")
    confs = {}
    for r in U.rows(base / CONFIRMS):
        confs.setdefault(r["id"], r)
    iso = lambda ms: U.iso_ms(ms) if ms else None                                      # noqa: E731
    doc = {"report": "companion_b1", "schema": "companion-report-3", "generated_utc": U.iso_ms(now_ms),
           "processed_utc": iso(ev["processed_ms"]),
           "source_cutoff_utc": iso(ev["outcome_window_end_ms"]),
           "outcome_window_end_utc": iso(ev["outcome_window_end_ms"]),
           "clocks": REPORT_CLOCKS,
           "stream": STREAM, "job": VERSION, "evaluation": ev,
           "lifecycle": {"state": life, "last": last, "authority": "termination and archiving: operator only"},
           "integrity": {"ok": ok, "failures_now": ev["integrity_failures_now"], "recorded_failures": len(integrity)},
           "evidence_class": klass,
           "evidence_class_rule": "no pre-registered success threshold exists for the companion, so its ceiling is "
                                  "'exploratory' (an interval with no decision rule); 'descriptive' below the block minimum; "
                                  "'unavailable' with no scored pair or any integrity failure; 'retired' once terminated",
           "registered": len(registered(base)), "confirmed": len(confs),
           "eligible": sum(1 for r in confs.values() if r.get("eligible")), "not_registered_by_reason": missed,
           "status": "prospective record only; descriptive until rc1d-eval-1 block minimums are met"}
    from storage import atomic_bytes
    atomic_bytes(base / "reports/companion_b1.json", (json.dumps(doc, indent=1, sort_keys=True) + "\n").encode())
    atomic_bytes(base / "reports/companion_b1.md", markdown(doc).encode())
    return doc


def markdown(doc: dict) -> str:
    ev = doc["evaluation"]
    lines = [f"# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)", "",
             f"Generated {doc['generated_utc']} by {doc['job']}; observation cutoff (latest included outcome-window end) "
             f"{doc['source_cutoff_utc'] or '—'}; last scored {doc['processed_utc'] or '—'}. "
             f"Stream start: {ev['stream_start_decision_utc'] or 'not started'}. "
             f"Registered {doc['registered']}, confirmed {doc['confirmed']}, eligible {doc['eligible']}. "
             f"Lifecycle {doc['lifecycle']['state']}. Evidence class: **{doc['evidence_class']}**. "
             f"Integrity: {'ok' if doc['integrity']['ok'] else 'FAILED - affected horizons withheld'} "
             f"({doc['integrity']['recorded_failures']} recorded failure rows).", "",
             "> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says "
             "nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.", "",
             "| horizon | RC1D scored | paired | largest disjoint subset | overlapping | missing | late | unscored | excluded (integrity) | B2−B1 mean | median | B2 better/tie/worse | rel. MAE reduction | standardized | 95% (resampling blocks) | B2−B0 mean | B1−B0 mean |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for h, e in ev["horizons"].items():
        a, b, c = e.get("B2_vs_B1", {}), e.get("B2_vs_B0", {}), e.get("B1_vs_B0", {})
        w = e["windows"]
        if a.get("withheld"):
            perf = "withheld | — | — | — | — | — | — | —"
        else:
            ci = a.get("diff_mean_ci95")
            eff = a.get("effect") or {}
            perf = (f"{a.get('diff_mean', '—')} | {a.get('diff_median', '—')} | "
                    f"{a.get('first_better', '—')}/{a.get('ties', '—')}/{a.get('first_worse', '—')} | "
                    f"{eff.get('relative_mae_reduction', '—')} | {eff.get('standardized_mean_diff', '—')} | "
                    f"{ci if ci else 'unavailable'} ({a.get('resampling_blocks', 0)}) | {b.get('diff_mean', '—')} | {c.get('diff_mean', '—')}")
        lines.append(f"| {h} | {e['rc1d_scored_since_start']} | {e['paired']} | {w['largest_disjoint_subset']} | {w['overlapping_another']} | "
                     f"{e['missing_companion']} | {e['late_companion']} | {e['unscored']} | {e['excluded_integrity']} | {perf} |")
    warn = [f"{h}: {e['overlap_warning']}" for h, e in ev["horizons"].items() if e.get("overlap_warning")]
    if warn:
        lines += ["", "Overlap (from actual windows): " + "; ".join(warn) + "."]
    if doc["not_registered_by_reason"]:
        lines += ["", "Not registered, by reason: " + "; ".join(f"{k} ({v})" for k, v in sorted(doc["not_registered_by_reason"].items()))]
    lines += ["", f"Method: {ev['method']}. Uncertainty: {ev.get('uncertainty_method')}. {ev['note']}",
              f"Evidence class rule: {doc['evidence_class_rule']}.", ""]
    return "\n".join(lines)


def main(argv) -> int:
    cmd = argv[1] if len(argv) > 1 else ""
    try:
        if cmd == "fit":
            p = fit()
            res = {"outcome": "fit ready" if p else "waiting for the RC1D fit", "class": "done" if p else "expected"}
        elif cmd == "forecast":
            st, last = lifecycle(BASE)
            ids = forecast()
            res = {"outcome": f"registered {len(ids)}" if ids else (f"refused: lifecycle {st}" if st not in ("approved", "active") else "none registered"),
                   "class": "done" if ids else "expected", "ids": ids}
        elif cmd == "confirm":
            rows = confirm()
            res = {"outcome": f"confirmed {len(rows)}", "class": "done" if rows else "expected"}
        elif cmd == "score":
            r = score()
            if r["integrity"]:
                res = {"outcome": "integrity failure", "class": "error", "failures": r["integrity"],
                       "scored": len(r["scored"])}
            else:
                res = {"outcome": f"scored {len(r['scored'])}" if r["scored"] else "no newly matured companion",
                       "class": "done" if r["scored"] else "expected", "unscored": r["unscored"]}
        elif cmd == "report":
            doc = report()
            res = {"outcome": f"report: {doc['evidence_class']}", "class": "done" if doc["integrity"]["ok"] else "error",
                   "integrity": doc["integrity"]["failures_now"]}
        elif cmd == "lifecycle" and len(argv) >= 4:
            row = operator_lifecycle(argv[2], " ".join(argv[3:]))
            res = {"outcome": f"lifecycle {row['state']}", "class": "done"}
        else:
            print("usage: companion_job.py fit|forecast|confirm|score|report | lifecycle <state> <reason>")
            return 2
    except (U.LifecycleError, RuntimeError, ValueError, OSError) as exc:
        res = {"outcome": f"failed: {exc}"[:300], "class": "error"}
    res["job"] = VERSION
    return U.emit(res)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
