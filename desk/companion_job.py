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

Stdlib only. Network: git only (confirmation). Records: streams/rc1d-b1/.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

DESK = Path(__file__).resolve().parent
BASE = DESK.parent
for p in (str(DESK), str(BASE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import range_model as R          # noqa: E402
import range_contract as C       # noqa: E402
import stream_util as U          # noqa: E402

VERSION = "companion-1.0.0"
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


def _say(msg):
    import os
    if not os.environ.get("RANGE_JOB_QUIET"):
        print(msg)


def _attempt(base, row):
    U.append(Path(base) / ATTEMPTS, row, key=lambda r: (r["id"], r["state"], r["t_ms"]))
    _say(f"companion {row['id']}: {row['state']}" + (f" ({row['reason']})" if row.get("reason") else ""))


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
                "snapshot_hash": doc["snapshot_hash"], "start_utc": doc["start_utc"], "horizon_utc": doc["horizon_utc"],
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
        row = {"id": cid, "commit": commit, "confirmed_ms": t, "start_ms": r["start_ms"],
               "eligible": r["prepared_ms"] < r["start_ms"] and t < r["start_ms"],
               "method": "git fetch origin; file sha256 matches the registry row"}
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


def score(base=BASE, now_ms=None) -> list:
    """Score confirmed companions whose RC1D twin is scored; the realized range comes from that record."""
    base = Path(base)
    have = {r["id"] for r in U.rows(base / SCORES)}
    conf = {r["id"]: r for r in U.rows(base / CONFIRMS)}
    rc = _rc1d_scores(base)
    out = []
    for cid, reg in registered(base).items():
        if cid in have or cid not in conf:
            continue
        s = rc.get(reg["rc1d_id"])
        if not s:
            continue
        ev = {e.get("name", "")[:2]: e for e in s.get("events", []) if isinstance(e, dict)}
        realized = (ev.get("B2") or {}).get("realized_ln_range")
        if realized is None:
            continue
        cdoc = json.loads((base / reg["path"]).read_bytes())
        loss = C.losses(cdoc["point"], [cdoc["q10"], cdoc["q50"], cdoc["q90"]], realized)
        row = {"id": cid, "rc1d_id": reg["rc1d_id"], "decision_utc": reg["decision_utc"], "horizon": reg["horizon"],
               "companion_eligible": conf[cid]["eligible"],
               "rc1d_eligible": bool((s.get("publication") or {}).get("eligible")),
               "realized_ln_range": realized, "B1": loss,
               "B2_abs_error_log_lr": (ev.get("B2") or {}).get("abs_error_log_lr"),
               "B0_abs_error_log_lr": (ev.get("B0") or {}).get("abs_error_log_lr"),
               "loss_function": "range_contract.losses (the RC1D scorer's function)", "job": VERSION}
        U.append(base / SCORES, row, key=lambda x: (x["id"],))
        out.append(row)
    return out


def evaluation(base=BASE) -> dict:
    """Per horizon: RC1D windows scored, companions registered/eligible/missing, and paired B2-vs-B1 and
    B2-vs-B0 differences on the eligible pairs (rc1d-eval-1 block rules)."""
    import range_reader as RR
    base = Path(base)
    rc = _rc1d_scores(base)
    reg = registered(base)
    conf = {r["id"]: r for r in U.rows(base / CONFIRMS)}
    sc = {r["id"]: r for r in U.rows(base / SCORES)}
    first = min((r["decision_utc"] for r in reg.values()), default=None)
    out = {}
    for h in HORIZONS:
        rc_h = {k: v for k, v in rc.items() if k.startswith(f"{RC1D_PREFIX}{h}-")
                and (v.get("publication") or {}).get("eligible") and first and k[len(RC1D_PREFIX) + len(h) + 1:] >=
                U.parse(first).strftime("%Y%m%dT%H%MZ")}
        pairs, missing, late = [], 0, 0
        for rid in sorted(rc_h):
            cid = ID_PREFIX + rid[len(RC1D_PREFIX):]
            if cid not in reg:
                missing += 1
                continue
            if not (conf.get(cid) or {}).get("eligible"):
                late += 1
                continue
            s = sc.get(cid)
            if not s or s["B1"].get("abs_error_log_lr") is None or s.get("B2_abs_error_log_lr") is None:
                continue
            pairs.append((s["decision_utc"], s["B2_abs_error_log_lr"], s["B1"]["abs_error_log_lr"], s["B0_abs_error_log_lr"]))
        entry = {"rc1d_scored_eligible_since_start": len(rc_h), "paired": len(pairs), "missing_companion": missing,
                 "late_companion": late,
                 "metric": "absolute error of ln range (log units); negative difference favours B2"}
        for name, j in (("B2_vs_B1", 2), ("B2_vs_B0", 3)):
            d = [p[1] - p[j] for p in pairs]
            n = len(d)
            if not n:
                entry[name] = {"n": 0}
                continue
            blocks = n // RR.EVAL_BLOCK
            e = {"n": n, "diff_mean": round(sum(d) / n, 5), "diff_median": round(RR._quantile(d, 0.5), 5),
                 "b2_better": sum(x < -1e-12 for x in d), "ties": sum(abs(x) <= 1e-12 for x in d),
                 "b2_worse": sum(x > 1e-12 for x in d), "blocks": blocks}
            if blocks >= RR.EVAL_MIN_BLOCKS:
                e["diff_mean_ci95"] = [round(x, 5) for x in RR._bootstrap_mean(d, RR.EVAL_BLOCK, RR.EVAL_RESAMPLES, RR.EVAL_SEED)]
            else:
                e["diff_mean_ci95"] = None
                e["uncertainty"] = f"unavailable: {blocks} complete block(s) of {RR.EVAL_BLOCK}; needs {RR.EVAL_MIN_BLOCKS}"
            entry[name] = e
        out[h] = entry
    return {"method": EVAL_METHOD, "stream_start_decision_utc": first, "horizons": out,
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
    doc = {"generated_utc": U.iso_ms(now_ms), "stream": STREAM, "job": VERSION, "evaluation": ev,
           "registered": len(registered(base)), "confirmed": len(U.rows(base / CONFIRMS)),
           "eligible": sum(1 for r in U.rows(base / CONFIRMS) if r["eligible"]), "not_registered_by_reason": missed,
           "status": "prospective record only; descriptive until rc1d-eval-1 block minimums are met"}
    from storage import atomic_bytes
    atomic_bytes(base / "reports/companion_b1.json", (json.dumps(doc, indent=1, sort_keys=True) + "\n").encode())
    atomic_bytes(base / "reports/companion_b1.md", markdown(doc).encode())
    return doc


def markdown(doc: dict) -> str:
    ev = doc["evaluation"]
    lines = [f"# RC1D companion benchmark: B2 vs B1 (HAR/calendar without DVOL)", "",
             f"Generated {doc['generated_utc']} by {doc['job']}. Stream start: {ev['stream_start_decision_utc'] or 'not started'}. "
             f"Registered {doc['registered']}, confirmed {doc['confirmed']}, eligible {doc['eligible']}.", "",
             "> Descriptive forecast-accuracy evidence only. It says whether DVOL adds to B1's range forecast; it says "
             "nothing about direction, sizing or trading returns. Late or missing companions stay late or missing.", "",
             "| horizon | RC1D scored (eligible) | paired | missing | late | B2−B1 mean | median | B2 better/tie/worse | 95% (blocks) | B2−B0 mean (same windows) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for h, e in ev["horizons"].items():
        a, b = e.get("B2_vs_B1", {}), e.get("B2_vs_B0", {})
        ci = a.get("diff_mean_ci95")
        lines.append(f"| {h} | {e['rc1d_scored_eligible_since_start']} | {e['paired']} | {e['missing_companion']} | "
                     f"{e['late_companion']} | {a.get('diff_mean', '—')} | {a.get('diff_median', '—')} | "
                     f"{a.get('b2_better', '—')}/{a.get('ties', '—')}/{a.get('b2_worse', '—')} | "
                     f"{ci if ci else 'unavailable'} ({a.get('blocks', 0)}) | {b.get('diff_mean', '—')} |")
    if doc["not_registered_by_reason"]:
        lines += ["", "Not registered, by reason: " + "; ".join(f"{k} ({v})" for k, v in sorted(doc["not_registered_by_reason"].items()))]
    lines += ["", f"Method: {ev['method']}. {ev['note']}", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fit":
        fit()
    elif cmd == "forecast":
        forecast()
    elif cmd == "confirm":
        confirm()
    elif cmd == "score":
        score()
    elif cmd == "report":
        report()
    else:
        raise SystemExit("usage: companion_job.py fit|forecast|confirm|score|report")
