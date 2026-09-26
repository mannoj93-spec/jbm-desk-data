#!/usr/bin/env python3
"""range_reader — the deterministic contract for reading the desk's registered range forecasts.

Version reader-12.0.0 (crypto-desk 12.0, repo 2.15). Stdlib only. Used by range_job.py (to write
reports/range_status.json) and by a desk thread (on a clone, or through that JSON).

read_current(base, now, horizon) resolves the manifest - never raw registry/ files - verifies the frozen
bytes against their hash and the schema, and checks instrument, contract, decision alignment, window,
freshness, and prospective eligibility (local freeze and remote confirmation both before the window start).

States:
  valid-current     the forecast for the latest expected decision, eligible, window not ended
  stale             the newest eligible forecast is for an older decision or its window has ended
  missing           no forecast registered for the stream (or only legacy/test records)
  unregistered      a source file exists for the latest decision with no manifest entry
  ineligible        registered but not (yet) prospectively eligible: publication unconfirmed or late
  integrity-failed  frozen bytes, schema, instrument or contract do not verify

A valid-current forecast is a forecast of the FULL window [start, end). Once the window has started it is
never a forecast of the remaining range; `label` says so and `remaining` is always None.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

DESK = Path(__file__).resolve().parent
for p in (str(DESK), str(DESK.parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

import range_contract as C      # noqa: E402

VERSION = "reader-12.0.0"
UTC = dt.timezone.utc
PREFIX = "range-rc1d-"
LEGACY = "range-b2-"
INSTRUMENT = "BTCUSDT perp, Binance last price"
GRACE_MIN = 75            # after a 4H close, the previous decision's forecast stays current this long
HORIZONS = ("4h", "24h", "72h")


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def _rows(path):
    try:
        return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    except FileNotFoundError:
        return []


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def boundary(now):
    return now.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=now.hour % 4)


def acceptable_decisions(now):
    e = boundary(now)
    return {e, e - dt.timedelta(hours=4)} if now - e < dt.timedelta(minutes=GRACE_MIN) else {e}


def _verify(base, fid, entry, expected_contract):
    """Frozen bytes -> document, or raise ValueError with the reason."""
    from schema import validate
    path = Path(base) / entry["frozen"]
    if path.resolve().parent != (Path(base) / "registry/frozen").resolve():
        raise ValueError("frozen path outside registry/frozen")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise ValueError("frozen bytes do not match the manifest hash")
    doc = json.loads(raw)
    errors = validate(doc)
    if errors or doc.get("id") != fid:
        raise ValueError(f"schema: {errors or 'id mismatch'}")
    if doc.get("instrument") != INSTRUMENT:
        raise ValueError("instrument mismatch")
    if doc.get("contract") != expected_contract:
        raise ValueError(f"contract {doc.get('contract')!r} != {expected_contract!r}")
    d = _t(doc["decision_utc"])
    if d.minute or d.second or d.hour % 4:
        raise ValueError("decision is not a 4H close")
    return doc


def read_current(base, now: dt.datetime, horizon: str, contract: str | None = None) -> dict:
    """`base` is a repository checkout (its schema.py validates the frozen documents)."""
    base = Path(base)
    if str(base) not in sys.path:
        sys.path.append(str(base))
    contract = contract or C.contract_id("RC1D")
    manifest = _read_json(base / "state/forecast_manifest.json", {})
    pubs = {}
    for r in _rows(base / "state/range_publications.jsonl"):
        pubs.setdefault(r["attempt"], r)
    stem = f"{PREFIX}{horizon}-"
    mine = sorted((fid for fid in manifest if fid.startswith(stem)), reverse=True)
    out = {"reader": VERSION, "horizon": horizon, "now_utc": C.iso(now), "contract": contract, "id": None,
           "remaining": None}
    latest_expected = max(acceptable_decisions(now))
    orphan = base / "registry" / f"{stem}{latest_expected:%Y%m%dT%H%MZ}.json"
    if orphan.exists() and orphan.name[:-5] not in manifest:
        return dict(out, state="unregistered", id=orphan.name[:-5],
                    reason="source file for the latest decision has no manifest entry; not a registered forecast")
    if not mine:
        legacy = sorted(fid for fid in manifest if fid.startswith(f"{LEGACY}{horizon}-"))
        why = f"no {PREFIX}* registration" + (f" (legacy 2.14 records exist, latest {legacy[-1]}; different contract)" if legacy else "")
        return dict(out, state="missing", reason=why)
    fid = mine[0]
    entry = manifest[fid]
    try:
        doc = _verify(base, fid, entry, contract)
    except (ValueError, OSError, KeyError) as exc:
        return dict(out, state="integrity-failed", id=fid, reason=str(exc))
    start, end, decision = _t(doc["start_utc"]), _t(doc["horizon_utc"]), _t(doc["decision_utc"])
    b2 = next(e for e in doc["events"] if e["name"].startswith("B2"))
    b0 = next(e for e in doc["events"] if e["name"].startswith("B0"))
    span = (end - start).total_seconds()
    elapsed = min(1.0, max(0.0, (now - start).total_seconds() / span))
    ref = doc["reference_price"]
    pts = {k: round(ref * (2.718281828459045 ** b2[k] - 1), 1) for k in ("point", "q10", "q50", "q90")}
    res = dict(out, id=fid, decision_utc=doc["decision_utc"], start_utc=doc["start_utc"], end_utc=doc["horizon_utc"],
               elapsed_fraction=round(elapsed, 4), point_lr=b2["point"], q_lr=[b2["q10"], b2["q50"], b2["q90"]],
               b0_point_lr=b0["point"], reference_price=ref, points_at_decision_close=pts,
               frozen_sha256=entry["sha256"], registered_ms=entry["registered"], attempt=entry.get("attempt"))
    pub = pubs.get(entry.get("attempt"))
    if entry["registered"] >= C.ms(start):
        return dict(res, state="ineligible", reason="registered at or after the window start")
    if pub is None:
        return dict(res, state="ineligible",
                    reason="publication not confirmed" + ("" if now < start else " before the window start"))
    if pub["confirmed"] >= C.ms(start):
        return dict(res, state="ineligible", reason="published after the window start")
    if decision not in acceptable_decisions(now) or now >= end:
        return dict(res, state="stale", reason=("window ended" if now >= end else f"newer decision expected ({C.iso(latest_expected)})"))
    label = (f"{fid} - full-window range forecast for [{doc['start_utc']}, {doc['horizon_utc']}) "
             f"({elapsed:.0%} elapsed; not a remaining-range forecast), contract {contract}")
    return dict(res, state="valid-current", reason="eligible and current", label=label,
                valid_until_utc=C.iso(min(end, max(acceptable_decisions(now)) + dt.timedelta(hours=4, minutes=GRACE_MIN))))


def status(base, now: dt.datetime) -> dict:
    """Reconcile expected 4H decisions with what happened to each; the compact surface a thread reads."""
    base = Path(base)
    manifest = _read_json(base / "state/forecast_manifest.json", {})
    attempts = _rows(base / "state/range_attempts.jsonl")
    pubs = {}
    for r in _rows(base / "state/range_publications.jsonl"):
        pubs.setdefault(r["attempt"], r)
    scores = {r["id"]: r for r in _rows(base / "registry/scores.jsonl")}
    release = _read_json(DESK / "release.json", {})
    prod = [a for a in attempts if (a.get("run") or {}).get("production")]
    by_dec = {}
    for a in prod:
        by_dec.setdefault(a["decision_utc"], []).append(a)
    starts = [release.get("range_stream_start_utc")] if release.get("range_stream_start_utc") else []
    starts += [min(by_dec)] if by_dec else []
    rows, counts = [], {}
    if starts:
        d, last = _t(min(starts)), boundary(now)
        if now - last < dt.timedelta(minutes=GRACE_MIN):
            last -= dt.timedelta(hours=4)          # the current close's run may still be in progress
        while d <= last:
            ds = C.iso(d)
            recs = by_dec.get(ds, [])
            final = recs[-1]["state"] if recs else None
            ids = next((r.get("ids") for r in reversed(recs) if r.get("ids")), None) or []
            if final is None:
                outcome, why = "missing", "no production attempt recorded (run absent, or it failed before persisting)"
            elif final in ("skipped",):
                outcome, why = "skipped", recs[-1].get("reason")
            elif final in ("failed", "abandoned"):
                outcome, why = final, recs[-1].get("reason")
            elif final in ("prepared",):
                outcome, why = "failed", "prepared but never frozen"
            elif final in ("frozen",):
                outcome, why = "registered-pending", "frozen; publication confirmation pending"
            elif final in ("unconfirmed", "published-late"):
                outcome, why = "late/ineligible", recs[-1].get("reason") or final
            elif final == "published":
                sc = [scores.get(i, {}).get("status") for i in ids]
                if all(s == "scored" for s in sc):
                    outcome, why = "scored", "all horizons scored"
                elif any(s and s != "scored" for s in sc):
                    outcome, why = "late/ineligible", "; ".join(sorted({s for s in sc if s and s != 'scored'}))
                else:
                    outcome, why = "registered-pending", f"eligible; {sum(s == 'scored' for s in sc)}/3 scored"
            else:
                outcome, why = "failed", f"unknown state {final}"
            counts[outcome] = counts.get(outcome, 0) + 1
            rows.append({"decision_utc": ds, "outcome": outcome, "reason": why, "ids": ids})
            d += dt.timedelta(hours=4)
    orphans = sorted(p.name for p in (base / "registry").glob(f"{PREFIX}*.json")
                     if p.name[:-5] not in manifest)
    integrity = []
    for fid, e in manifest.items():
        if fid.startswith(PREFIX):
            try:
                _verify(base, fid, e, C.contract_id("RC1D"))
            except (ValueError, OSError, KeyError) as exc:
                integrity.append(f"{fid}: {exc}")
    current = {h: read_current(base, now, h) for h in HORIZONS}
    stats = {}
    for fid, r in scores.items():
        if not fid.startswith(PREFIX) or r.get("status") != "scored":
            continue
        h = fid[len(PREFIX):].split("-")[0]
        ev = {e["name"].split(" ")[0]: e for e in r.get("events", [])}
        if ev.get("B2", {}).get("abs_error_log_lr") is None or ev.get("B0", {}).get("abs_error_log_lr") is None:
            continue
        s = stats.setdefault(h, {"n": 0, "b2": 0.0, "b0": 0.0, "c2": 0, "c0": 0})
        s["n"] += 1; s["b2"] += ev["B2"]["abs_error_log_lr"]; s["b0"] += ev["B0"]["abs_error_log_lr"]
        s["c2"] += bool(ev["B2"]["covered_80"]); s["c0"] += bool(ev["B0"]["covered_80"])
    scored = {h: {"n": s["n"], "mae_b2": round(s["b2"] / s["n"], 5), "mae_b0": round(s["b0"] / s["n"], 5),
                  "skill": round(1 - s["b2"] / s["b0"], 4) if s["b0"] else None,
                  "coverage_b2": round(s["c2"] / s["n"], 3), "coverage_b0": round(s["c0"] / s["n"], 3)}
              for h, s in stats.items()}
    return {"generated_utc": C.iso(now), "reader": VERSION, "contract": C.contract_id("RC1D"),
            "release": {k: release.get(k) for k in ("package", "repo_revision", "contract", "release_sha256")},
            "current": current, "scored": scored, "expected_decisions": len(rows), "outcomes": counts, "recent": rows[-18:],
            "non_production_attempts": len(attempts) - len(prod), "orphans": orphans, "integrity_failures": integrity,
            "legacy_2_14_registrations": sorted(fid for fid in manifest if fid.startswith(LEGACY)),
            "note": "Generated file: re-derive freshness against your own clock (current[h].valid_until_utc). "
                    "A green workflow is not a registration; only state valid-current is citable."}


def markdown(st: dict) -> str:
    lines = ["# Range forecasts - status", "",
             f"Generated {st['generated_utc']} by {st['reader']}; contract `{st['contract']}`. "
             "Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (weekly report).", "",
             "| horizon | state | id | window | reason |", "|---|---|---|---|---|"]
    for h, c in st["current"].items():
        win = f"{c.get('start_utc', '—')} → {c.get('end_utc', '—')}"
        lines.append(f"| {h} | {c['state']} | {c.get('id') or '—'} | {win} | {c.get('reason', '')} |")
    lines += ["", f"Expected production decisions: {st['expected_decisions']}; outcomes: "
              + (", ".join(f"{k} {v}" for k, v in sorted(st['outcomes'].items())) or "none yet") + ".",
              f"Non-production attempts (tests, local runs): {st['non_production_attempts']}. "
              f"Orphan source files: {len(st['orphans'])}. Integrity failures: {len(st['integrity_failures'])}. "
              f"Legacy 2.14 registrations (q50-scored, pre-contract): {len(st['legacy_2_14_registrations'])}.", ""]
    lines += ["Prospective scores (RC1D, losses on the registered point; windows overlap within a horizon, so "
              "independent n is far below the count; below ~100 independent windows nothing is eligible for "
              "forecast status):", "", "| horizon | scored | MAE B2 | MAE B0 | skill | coverage B2 | coverage B0 |",
              "|---|---|---|---|---|---|---|"]
    for h in HORIZONS:
        s = st["scored"].get(h)
        lines.append(f"| {h} | 0 | — | — | — | — | — |" if not s else
                     f"| {h} | {s['n']} | {s['mae_b2']} | {s['mae_b0']} | {s['skill']:.1%} | {s['coverage_b2']:.0%} | {s['coverage_b0']:.0%} |")
    lines.append("")
    if st["recent"]:
        lines += ["| decision | outcome | reason |", "|---|---|---|"]
        lines += [f"| {r['decision_utc']} | {r['outcome']} | {r['reason']} |" for r in st["recent"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else DESK.parent
    now = _t(sys.argv[2]) if len(sys.argv) > 2 else dt.datetime.now(UTC).replace(microsecond=0)
    print(json.dumps({h: read_current(base, now, h) for h in HORIZONS}, indent=1))
