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

VERSION = "reader-12.1.0"
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
    except ValueError as exc:                      # malformed JSON is reported, never silently defaulted
        raise ValueError(f"{Path(path).name}: malformed JSON ({exc})") from exc


def _rows(path):
    try:
        return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    except FileNotFoundError:
        return []
    except ValueError as exc:
        raise ValueError(f"{Path(path).name}: malformed JSON line ({exc})") from exc


def _publications(base):
    """{attempt: first confirmation}; rows that are not objects with an attempt are reported, not used."""
    pubs, bad = {}, 0
    for r in _rows(Path(base) / "state/range_publications.jsonl"):
        if isinstance(r, dict) and isinstance(r.get("attempt"), str):
            pubs.setdefault(r["attempt"], r)
        else:
            bad += 1
    return pubs, bad


def expiry(decision: dt.datetime, end: dt.datetime) -> dt.datetime:
    """Latest instant a forecast can be current: its decision stays acceptable until decision + 4h + grace
    (a missed next run), and never past its window end. An upper bound: a newer forecast supersedes it sooner."""
    return min(end, decision + dt.timedelta(hours=4, minutes=GRACE_MIN))


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def boundary(now):
    return now.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=now.hour % 4)


def acceptable_decisions(now):
    e = boundary(now)
    return {e, e - dt.timedelta(hours=4)} if now - e < dt.timedelta(minutes=GRACE_MIN) else {e}


def _verify(base, fid, entry, expected_contract, publication=None):
    """Frozen bytes -> document, or raise ValueError with the reason."""
    from schema import validate
    if not isinstance(entry, dict) or not isinstance(entry.get("frozen"), str):
        raise ValueError("manifest entry malformed")
    path = Path(base) / entry["frozen"]
    if path.resolve().parent != (Path(base) / "registry/frozen").resolve():
        raise ValueError("frozen path outside registry/frozen")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise ValueError("frozen bytes do not match the manifest hash")
    doc = json.loads(raw)
    errors = validate(doc)
    if errors or not isinstance(doc, dict) or doc.get("id") != fid:
        raise ValueError(f"schema: {errors or 'id mismatch'}")
    strict = C.validate_rc1d(doc, fid, entry, publication, {expected_contract})
    if strict:
        raise ValueError("RC1D: " + "; ".join(strict))
    return doc


def read_current(base, now: dt.datetime, horizon: str, contract: str | None = None) -> dict:
    """`base` is a repository checkout (its schema.py validates the frozen documents). Never raises: any
    malformed manifest, publication record or document is `integrity-failed` with its reason."""
    base = Path(base)
    if str(base) not in sys.path:
        sys.path.append(str(base))
    contract = contract or C.contract_id("RC1D")
    out = {"reader": VERSION, "horizon": horizon, "now_utc": C.iso(now), "contract": contract, "id": None,
           "remaining": None}
    try:
        manifest = _read_json(base / "state/forecast_manifest.json", {})
        if not isinstance(manifest, dict):
            raise ValueError("forecast_manifest.json is not an object")
        pubs, _ = _publications(base)
    except (ValueError, OSError) as exc:
        return dict(out, state="integrity-failed", reason=str(exc))
    stem = f"{PREFIX}{horizon}-"
    mine = sorted((fid for fid in manifest if isinstance(fid, str) and fid.startswith(stem)), reverse=True)
    latest_expected = max(acceptable_decisions(now))
    orphan = base / "registry" / f"{stem}{latest_expected:%Y%m%dT%H%MZ}.json"
    if orphan.exists() and orphan.name[:-5] not in manifest:
        return dict(out, state="unregistered", id=orphan.name[:-5],
                    reason="source file for the latest decision has no manifest entry; not a registered forecast")
    if not mine:
        legacy = sorted(fid for fid in manifest if isinstance(fid, str) and fid.startswith(f"{LEGACY}{horizon}-"))
        why = f"no {PREFIX}* registration" + (f" (legacy 2.14 records exist, latest {legacy[-1]}; different contract)" if legacy else "")
        return dict(out, state="missing", reason=why)
    fid = mine[0]
    entry = manifest[fid]
    pub = pubs.get(entry.get("attempt")) if isinstance(entry, dict) else None
    try:
        doc = _verify(base, fid, entry, contract, pub)
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
        return dict(out, state="integrity-failed", id=fid, reason=str(exc))
    start, end, decision = _t(doc["start_utc"]), _t(doc["horizon_utc"]), _t(doc["decision_utc"])
    ev = {e["name"][:2]: e for e in doc["events"]}
    b2, b0 = ev["B2"], ev["B0"]
    ref = doc["reference_price"]
    pts = {k: round(ref * (2.718281828459045 ** b2[k] - 1), 1) for k in ("point", "q10", "q50", "q90")}
    until = expiry(decision, end)
    res = dict(out, id=fid, decision_utc=doc["decision_utc"], start_utc=doc["start_utc"], end_utc=doc["horizon_utc"],
               point_lr=b2["point"], q_lr=[b2["q10"], b2["q50"], b2["q90"]], b0_point_lr=b0["point"],
               reference_price=ref, points_at_decision_close=pts, frozen_sha256=entry["sha256"],
               registered_ms=entry["registered"], attempt=entry.get("attempt"), valid_until_utc=C.iso(until))
    if pub is None:
        return _timed(dict(res, state="ineligible",
                           reason="publication not confirmed" + ("" if now < start else " before the window start")), now)
    if pub["confirmed"] >= C.ms(start):
        return _timed(dict(res, state="ineligible", reason="published after the window start"), now)
    return revalidate(dict(res, state="valid-current", reason="eligible and current"), now)


def _timed(res, now):
    """Time-dependent fields, recomputed against the consumer's clock."""
    start, end = _t(res["start_utc"]), _t(res["end_utc"])
    elapsed = min(1.0, max(0.0, (now - start).total_seconds() / (end - start).total_seconds()))
    return dict(res, now_utc=C.iso(now), elapsed_fraction=round(elapsed, 4))


def revalidate(res: dict, now: dt.datetime) -> dict:
    """Apply the reader's freshness rule to a (possibly cached) result at `now`. A cached valid-current result
    agrees with a fresh read of the same forecast at every instant: current while now < valid_until_utc,
    stale from then on. It can never upgrade another state (a cached `missing` may have been superseded)."""
    if res.get("state") != "valid-current" or not res.get("valid_until_utc"):
        return res
    until = _t(res["valid_until_utc"])
    res = _timed(res, now)
    if res["state"] == "valid-current" and now < until:
        label = (f"{res['id']} - full-window range forecast for [{res['start_utc']}, {res['end_utc']}) "
                 f"({res['elapsed_fraction']:.0%} elapsed; not a remaining-range forecast), contract {res['contract']}")
        return dict(res, label=label, remaining=None)
    reason = "window ended" if now >= _t(res["end_utc"]) else \
        f"expired at {res['valid_until_utc']} (a newer decision was due; no newer forecast is current)"
    return dict({k: v for k, v in res.items() if k != "label"}, state="stale", reason=reason, remaining=None)


def _outcome(recs, scores):
    """Outcome of one decision from its production attempt rows (latest state wins)."""
    final = recs[-1].get("state") if recs else None
    ids = next((r.get("ids") for r in reversed(recs) if isinstance(r.get("ids"), list)), None) or []
    if final is None:
        return "missing", "no production attempt recorded (run absent, or it failed before persisting)", ids
    if final == "skipped":
        return "skipped", recs[-1].get("reason"), ids
    if final in ("failed", "abandoned"):
        return final, recs[-1].get("reason"), ids
    if final == "prepared":
        return "failed", "prepared but never frozen", ids
    if final == "frozen":
        return "registered-pending", "frozen; publication confirmation pending", ids
    if final in ("unconfirmed", "published-late"):
        return "late/ineligible", recs[-1].get("reason") or final, ids
    if final == "published":
        sc = [(scores.get(i) or {}).get("status") for i in ids]
        if sc and all(x == "scored" for x in sc):
            return "scored", "all horizons scored", ids
        if any(x and x != "scored" for x in sc):
            return "late/ineligible", "; ".join(sorted({x for x in sc if x and x != "scored"})), ids
        return "registered-pending", f"eligible; {sum(x == 'scored' for x in sc)}/3 scored", ids
    return "failed", f"unknown state {final}", ids


def status(base, now: dt.datetime) -> dict:
    """Reconcile 4H decisions with what happened to each; the compact surface a thread reads. Never raises:
    a malformed input file is reported under `integrity_failures` and the rest of the report is still built.
    Decisions are split into `due` (their run window has passed: counted in `outcomes`) and `current`
    (the latest close, still inside its run grace period: reported, never counted as missing)."""
    base = Path(base)
    problems = []

    def load(fn, *args):
        try:
            return fn(*args)
        except (ValueError, OSError) as exc:
            problems.append(str(exc))
            return None
    manifest = load(_read_json, base / "state/forecast_manifest.json", {})
    if not isinstance(manifest, dict):
        problems.append("forecast_manifest.json is not an object") if manifest is not None else None
        manifest = {}
    attempts = [a for a in (load(_rows, base / "state/range_attempts.jsonl") or []) if isinstance(a, dict)]
    pubs_bad = load(_publications, base) or ({}, 0)
    if pubs_bad[1]:
        problems.append(f"range_publications.jsonl: {pubs_bad[1]} malformed row(s) ignored")
    scores = {r["id"]: r for r in (load(_rows, base / "registry/scores.jsonl") or [])
              if isinstance(r, dict) and isinstance(r.get("id"), str)}
    release = load(_read_json, DESK / "release.json", {}) or {}
    prod = [a for a in attempts if isinstance(a.get("run"), dict) and a["run"].get("production")
            and isinstance(a.get("decision_utc"), str)]
    by_dec = {}
    for a in prod:
        by_dec.setdefault(a["decision_utc"], []).append(a)
    starts = [release.get("range_stream_start_utc")] if release.get("range_stream_start_utc") else []
    starts += [min(by_dec)] if by_dec else []
    rows, counts = [], {}
    latest = boundary(now)
    in_grace = now - latest < dt.timedelta(minutes=GRACE_MIN)
    last_due = latest - dt.timedelta(hours=4) if in_grace else latest
    if starts:
        d = _t(min(starts))
        while d <= last_due:
            outcome, why, ids = _outcome(by_dec.get(C.iso(d), []), scores)
            counts[outcome] = counts.get(outcome, 0) + 1
            rows.append({"decision_utc": C.iso(d), "outcome": outcome, "reason": why, "ids": ids})
            d += dt.timedelta(hours=4)
    current_decision = None
    if in_grace:
        recs = by_dec.get(C.iso(latest), [])
        outcome, why, ids = _outcome(recs, scores)
        current_decision = {"decision_utc": C.iso(latest), "grace_until_utc": C.iso(latest + dt.timedelta(minutes=GRACE_MIN)),
                            "outcome": "in-progress" if not recs else outcome,
                            "reason": "run window still open; not yet due" if not recs else why, "ids": ids}
    orphans = sorted(p.name for p in (base / "registry").glob(f"{PREFIX}*.json") if p.name[:-5] not in manifest)
    pubs = pubs_bad[0]
    for fid, e in manifest.items():
        if isinstance(fid, str) and fid.startswith(PREFIX):
            try:
                _verify(base, fid, e, C.contract_id("RC1D"), pubs.get(e.get("attempt")) if isinstance(e, dict) else None)
            except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
                problems.append(f"{fid}: {exc}")
    current = {h: read_current(base, now, h) for h in HORIZONS}
    stats = {}
    for fid, r in scores.items():
        if not fid.startswith(PREFIX) or r.get("status") != "scored":
            continue
        try:
            h = fid[len(PREFIX):].split("-")[0]
            ev = {e["name"].split(" ")[0]: e for e in r.get("events", [])}
            if ev.get("B2", {}).get("abs_error_log_lr") is None or ev.get("B0", {}).get("abs_error_log_lr") is None:
                continue
            st_ = stats.setdefault(h, {"n": 0, "b2": 0.0, "b0": 0.0, "c2": 0, "c0": 0})
            st_["n"] += 1; st_["b2"] += ev["B2"]["abs_error_log_lr"]; st_["b0"] += ev["B0"]["abs_error_log_lr"]
            st_["c2"] += bool(ev["B2"]["covered_80"]); st_["c0"] += bool(ev["B0"]["covered_80"])
        except (KeyError, TypeError, AttributeError) as exc:
            problems.append(f"scores {fid}: malformed ({exc})")
    scored = {h: {"n": x["n"], "mae_b2": round(x["b2"] / x["n"], 5), "mae_b0": round(x["b0"] / x["n"], 5),
                  "skill": round(1 - x["b2"] / x["b0"], 4) if x["b0"] else None,
                  "coverage_b2": round(x["c2"] / x["n"], 3), "coverage_b0": round(x["c0"] / x["n"], 3)}
              for h, x in stats.items()}
    return {"generated_utc": C.iso(now), "reader": VERSION, "contract": C.contract_id("RC1D"),
            "release": {k: release.get(k) for k in ("package", "repo_revision", "contract", "release_sha256")},
            "current": current, "scored": scored, "due_decisions": len(rows), "expected_decisions": len(rows),
            "current_decision": current_decision, "outcomes": counts, "recent": rows[-18:],
            "non_production_attempts": len(attempts) - len(prod), "orphans": orphans, "integrity_failures": problems,
            "legacy_2_14_registrations": sorted(f for f in manifest if isinstance(f, str) and f.startswith(LEGACY)),
            "note": "Generated file. Freshness is the reader's rule applied to your own clock: a valid-current entry "
                    "is current only while now < current[h].valid_until_utc (range_reader.revalidate); recompute "
                    "elapsed_fraction from start/end. Only valid-current is citable, as a full-window forecast. "
                    "A green workflow is not a registration. Publication confirmation uses the runner's clock "
                    "after a remote fetch."}


def markdown(st: dict) -> str:
    lines = ["# Range forecasts - status", "",
             f"Generated {st['generated_utc']} by {st['reader']}; contract `{st['contract']}`. "
             "Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (weekly report).", "",
             "| horizon | state | id | window | valid until | reason |", "|---|---|---|---|---|---|"]
    for h, c in st["current"].items():
        win = f"{c.get('start_utc', '—')} → {c.get('end_utc', '—')}"
        lines.append(f"| {h} | {c['state']} | {c.get('id') or '—'} | {win} | {c.get('valid_until_utc') or '—'} | {c.get('reason', '')} |")
    cd = st.get("current_decision")
    lines += ["", (f"Current decision {cd['decision_utc']}: {cd['outcome']} ({cd['reason']}). " if cd else "")
              + f"Due production decisions: {st['due_decisions']}; outcomes: "
              + (", ".join(f"{k} {v}" for k, v in sorted(st['outcomes'].items())) or "none yet") + ".",
              f"Non-production attempts (tests, local runs): {st['non_production_attempts']}. "
              f"Orphan source files: {len(st['orphans'])}. Integrity failures: {len(st['integrity_failures'])}. "
              f"Legacy 2.14 registrations (q50-scored, pre-contract): {len(st['legacy_2_14_registrations'])}.",
              "Valid-current rows are current only until their valid_until_utc (see the JSON twin).", ""]
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
