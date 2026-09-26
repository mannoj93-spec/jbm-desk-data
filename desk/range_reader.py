#!/usr/bin/env python3
"""range_reader — the deterministic contract for reading the desk's registered range forecasts.

Version reader-12.2.0 (crypto-desk 12.2, repo 2.17). Stdlib only. Used by range_job.py (to write
reports/range_status.json) and by a desk thread (on a clone, or through that JSON).

read_current(base, now, horizon) is an AS-OF read: it resolves the manifest - never raw registry/ files - and
considers only records AVAILABLE at `now` (decision, preparation, registration and publication confirmation
all at or before now), newest decision first. It verifies the frozen bytes against their hash, the schema and
the strict RC1D checks (range_contract.validate_rc1d) and applies the shared eligibility rule
(range_contract.eligibility). A record not yet confirmed whose window has not started is not available and is
skipped; an integrity failure is reported, never skipped around. A window may start after `now`.

States:
  valid-current     the newest available forecast, eligible, and now < valid_until_utc
  stale             the newest available eligible forecast has expired (a newer decision was due) or ended
  missing           no RC1D forecast available at `now` (or only legacy/test records)
  unregistered      a source file exists for the latest decision with no manifest entry
  ineligible        the newest available record can never be eligible: late registration, late or absent
                    publication confirmation by its window start
  integrity-failed  manifest, frozen bytes, schema, instrument, contract or strict RC1D checks do not verify
  unavailable       (revalidate only) a cached result applied to a time before that record was available

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
import range_ops as OPS          # noqa: E402

VERSION = "reader-12.2.0"
UTC = dt.timezone.utc
PREFIX = "range-rc1d-"
LEGACY = "range-b2-"
INSTRUMENT = "BTCUSDT perp, Binance last price"
GRACE_MIN = 75            # after a 4H close, the previous decision's forecast stays current this long
HORIZONS = ("4h", "24h", "72h")
MATURITY_BUFFER_MIN = 5   # scoring.MATURITY_BUFFER_MS: a window is scorable this long after it ends
SCORING_LOG = "state/range_scoring.jsonl"


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
    now_ms = C.ms(now)
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
    decided = []                                        # (decision, id) for ids whose decision is <= now
    for fid in manifest:
        if isinstance(fid, str) and fid.startswith(stem):
            try:
                d = dt.datetime.strptime(fid[len(stem):], "%Y%m%dT%H%MZ").replace(tzinfo=UTC)
            except ValueError:
                return dict(out, state="integrity-failed", id=fid, reason="manifest id is not a decision stamp")
            if d <= now:
                decided.append((d, fid))
    latest_expected = max(acceptable_decisions(now))
    orphan = base / "registry" / f"{stem}{latest_expected:%Y%m%dT%H%MZ}.json"
    if orphan.exists() and orphan.name[:-5] not in manifest:
        return dict(out, state="unregistered", id=orphan.name[:-5],
                    reason="source file for the latest decision has no manifest entry; not a registered forecast")
    pending = []
    for _, fid in sorted(decided, reverse=True):
        entry = manifest[fid]
        if not isinstance(entry, dict) or not isinstance(entry.get("registered"), int) \
                or isinstance(entry.get("registered"), bool):
            return dict(out, state="integrity-failed", id=fid, reason="manifest entry or registration time malformed")
        if entry["registered"] > now_ms:
            continue                                    # registered later: did not exist at `now`
        attempt = entry.get("attempt")
        pub = pubs.get(attempt) if isinstance(attempt, str) else None
        try:
            doc = _verify(base, fid, entry, contract, pub)
            start, end, decision = _t(doc["start_utc"]), _t(doc["horizon_utc"]), _t(doc["decision_utc"])
            state, why = C.eligibility(C.ms(start), entry, pub, now_ms)
            avail = C.available_ms(doc, entry, pub if state == "eligible" else None)
        except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
            return dict(out, state="integrity-failed", id=fid, reason=str(exc))
        if avail > now_ms or state == "pending":
            pending.append(fid)                         # prepared/registered but not yet published at `now`
            continue
        ev = {e["name"][:2]: e for e in doc["events"]}
        b2, b0 = ev["B2"], ev["B0"]
        ref = doc["reference_price"]
        pts = {k: round(ref * (2.718281828459045 ** b2[k] - 1), 1) for k in ("point", "q10", "q50", "q90")}
        until = expiry(decision, end)
        res = dict(out, id=fid, decision_utc=doc["decision_utc"], start_utc=doc["start_utc"], end_utc=doc["horizon_utc"],
                   point_lr=b2["point"], q_lr=[b2["q10"], b2["q50"], b2["q90"]], b0_point_lr=b0["point"],
                   reference_price=ref, points_at_decision_close=pts, frozen_sha256=entry["sha256"],
                   registered_ms=entry["registered"], attempt=attempt, available_ms=avail,
                   available_from_utc=C.iso(C.from_ms(-(-avail // 1000) * 1000)), valid_until_utc=C.iso(until))
        if pending:
            res["newer_pending"] = pending
        if state != "eligible":
            return _timed(dict(res, state="ineligible", reason=why), now)
        return revalidate(dict(res, state="valid-current", reason="eligible and current"), now)
    why = f"no {PREFIX}* forecast available at {C.iso(now)}"
    if pending:
        why += f" ({', '.join(pending)} registered, publication not yet confirmed)"
    legacy = sorted(fid for fid in manifest if isinstance(fid, str) and fid.startswith(f"{LEGACY}{horizon}-"))
    if legacy:
        why += f" (legacy 2.14 records exist, latest {legacy[-1]}; different contract)"
    return dict(out, state="missing", reason=why, **({"newer_pending": pending} if pending else {}))


def _timed(res, now):
    """Time-dependent fields, recomputed against the consumer's clock."""
    start, end = _t(res["start_utc"]), _t(res["end_utc"])
    elapsed = min(1.0, max(0.0, (now - start).total_seconds() / (end - start).total_seconds()))
    return dict(res, now_utc=C.iso(now), elapsed_fraction=round(elapsed, 4))


def revalidate(res: dict, now: dt.datetime) -> dict:
    """Apply the reader's freshness rule to a (possibly cached) result at `now`. A cached valid-current result
    agrees with a fresh read of the same forecast at every instant: current while now < valid_until_utc,
    stale from then on, and `unavailable` before the record existed (available_ms: decision, preparation,
    registration and confirmation). It can never upgrade another state (a cached `missing` may have been
    superseded)."""
    if res.get("state") != "valid-current" or not res.get("valid_until_utc"):
        return res
    until = _t(res["valid_until_utc"])
    res = _timed(res, now)
    avail = res.get("available_ms")
    if isinstance(avail, int) and C.ms(now) < avail:          # lower bound: the record did not exist yet
        return dict({k: v for k, v in res.items() if k != "label"}, state="unavailable", remaining=None,
                    reason=f"not available before {res.get('available_from_utc')}; re-read at this time")
    if res["state"] == "valid-current" and now < until:
        label = (f"{res['id']} - full-window range forecast for [{res['start_utc']}, {res['end_utc']}) "
                 f"({res['elapsed_fraction']:.0%} elapsed; not a remaining-range forecast), contract {res['contract']}")
        return dict(res, label=label, remaining=None)
    reason = "window ended" if now >= _t(res["end_utc"]) else \
        f"expired at {res['valid_until_utc']} (a newer decision was due; no newer forecast is current)"
    return dict({k: v for k, v in res.items() if k != "label"}, state="stale", reason=reason, remaining=None)


def _outcome(recs, scores, life=None, due=True):
    """Outcome of one decision from its production attempt rows (latest state wins) and, when no attempt was
    recorded, the run lifecycle log (state/range_runs.jsonl): a known failure before forecasting is reported
    with its stage and reason and is never replaced by a generic `in-progress` or `missing`."""
    final = recs[-1].get("state") if recs else None
    ids = next((r.get("ids") for r in reversed(recs) if isinstance(r.get("ids"), list)), None) or []
    if final is None:
        if life:
            if life["state"] == "running":
                return ("running" if not due else "failed"), (life["reason"] if not due else
                        f"run {life['run_id']} started but recorded no terminal outcome ({life['reason']})"), ids
            if life["state"] == "skipped":
                return "skipped", life.get("reason"), ids
            return "failed", f"run {life['run_id']}: {life.get('reason')}", ids
        if not due:
            return "not-started", "no run has recorded anything for this decision yet", ids
        return "missing", "no production attempt or run record (run absent, or it failed before persisting)", ids
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


def _scoring_log(base):
    """Latest scoring attempt per id from state/range_scoring.jsonl (written by range_job.py score)."""
    out = {}
    try:
        for r in _rows(Path(base) / SCORING_LOG):
            if isinstance(r, dict) and isinstance(r.get("id"), str):
                out[r["id"]] = r
    except (ValueError, OSError):
        pass
    return out


def scoring_states(base, now, docs, scores, problems) -> dict:
    """Per-horizon scoring pipeline states for registered RC1D forecasts available at `now`:
    waiting-maturity (window not ended + buffer), waiting-observations (matured; the last scoring attempt
    found observations incomplete, conflicting or unavailable), ready (matured, eligible, not yet attempted
    or attempt pending), scored, ineligible (never scored: late registration or publication, unconfirmed,
    integrity failure). `backlog` = ready + waiting-observations, oldest end first; a mature 4h backlog is
    shown on its own, never hidden behind an unfinished 72h window."""
    now_ms = C.ms(now)
    log = _scoring_log(base)
    out = {h: {"waiting-maturity": 0, "waiting-observations": 0, "ready": 0, "scored": 0, "ineligible": 0,
               "backlog": []} for h in HORIZONS}
    for fid, item in sorted(docs.items()):
        h = fid[len(PREFIX):].split("-")[0]
        if h not in out:
            continue
        sc = scores.get(fid) or {}
        if item is None:
            out[h]["ineligible"] += 1
            continue
        doc, entry, pub = item
        try:
            start, end = C.ms(_t(doc["start_utc"])), C.ms(_t(doc["horizon_utc"]))
            if entry["registered"] > now_ms:
                continue
            elig, _ = C.eligibility(start, entry, pub, now_ms)
        except (KeyError, TypeError, ValueError) as exc:
            problems.append(f"scoring state {fid}: {exc}")
            continue
        if sc.get("status") == "scored":
            state = "scored"
        elif sc.get("status") or elig in ("late-registration", "late-publication") or \
                (elig == "unconfirmed" and end <= now_ms):
            state = "ineligible"
        elif end + MATURITY_BUFFER_MIN * 60_000 > now_ms:
            state = "waiting-maturity"
        elif (log.get(fid) or {}).get("outcome") == "unscorable":
            state = "waiting-observations"
        else:
            state = "ready"
        out[h][state] += 1
        if state in ("ready", "waiting-observations"):
            out[h]["backlog"].append({"id": fid, "matured_utc": C.iso(C.from_ms(end + MATURITY_BUFFER_MIN * 60_000)),
                                      "state": state, "last_attempt": log.get(fid)})
    return out


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
    runs, runs_bad = OPS.rows(base)
    if runs_bad:
        problems.append(f"range_runs.jsonl: {runs_bad} malformed row(s) ignored")
    prod_runs = [r for r in runs if r.get("event") in ("schedule", "workflow_dispatch")]
    starts = [release.get("range_stream_start_utc")] if release.get("range_stream_start_utc") else []
    starts += [min(by_dec)] if by_dec else []
    rows, counts = [], {}
    latest = boundary(now)
    in_grace = now - latest < dt.timedelta(minutes=GRACE_MIN)
    last_due = latest - dt.timedelta(hours=4) if in_grace else latest
    if starts:
        d = _t(min(starts))
        while d <= last_due:
            outcome, why, ids = _outcome(by_dec.get(C.iso(d), []), scores, OPS.decision_view(prod_runs, C.iso(d)))
            counts[outcome] = counts.get(outcome, 0) + 1
            rows.append({"decision_utc": C.iso(d), "outcome": outcome, "reason": why, "ids": ids})
            d += dt.timedelta(hours=4)
    current_decision = None
    if in_grace:
        recs = by_dec.get(C.iso(latest), [])
        outcome, why, ids = _outcome(recs, scores, OPS.decision_view(prod_runs, C.iso(latest)), due=False)
        current_decision = {"decision_utc": C.iso(latest), "grace_until_utc": C.iso(latest + dt.timedelta(minutes=GRACE_MIN)),
                            "outcome": outcome, "reason": why, "ids": ids}
    orphans = sorted(p.name for p in (base / "registry").glob(f"{PREFIX}*.json") if p.name[:-5] not in manifest)
    pubs = pubs_bad[0]
    docs = {}
    for fid, e in manifest.items():
        if isinstance(fid, str) and fid.startswith(PREFIX):
            try:
                att = e.get("attempt") if isinstance(e, dict) else None
                docs[fid] = (_verify(base, fid, e, C.contract_id("RC1D"), pubs.get(att) if isinstance(att, str) else None),
                             e, pubs.get(att) if isinstance(att, str) else None)
            except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
                problems.append(f"{fid}: {exc}")
                docs[fid] = None
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
    scoring = scoring_states(base, now, docs, scores, problems)
    valid_untils = [_t(c["valid_until_utc"]) for c in current.values() if c.get("state") == "valid-current"]
    expires = min(valid_untils + [latest + dt.timedelta(hours=4, minutes=GRACE_MIN)])
    return {"generated_utc": C.iso(now), "status_expires_utc": C.iso(expires),
            "freshness_rule": "This file describes the stream as of generated_utc. After status_expires_utc it cannot "
                              "tell you what is current; before then, re-check every current[h] on your own clock with "
                              "range_reader.revalidate (valid only while now < valid_until_utc).",
            "reader": VERSION, "contract": C.contract_id("RC1D"),
            "release": {k: release.get(k) for k in ("package", "repo_revision", "contract", "release_sha256")},
            "current": current, "scored": scored, "due_decisions": len(rows), "expected_decisions": len(rows),
            "current_decision": current_decision, "outcomes": counts, "recent": rows[-18:], "scoring": scoring,
            "runs_recorded": len(runs),
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
             f"**Expires {st.get('status_expires_utc')}**: after that this page cannot say what is current; before "
             "then re-check each row's valid-until on your own clock. "
             "Machine-readable twin: `reports/range_status.json`. Scores: `registry/scores.jsonl` (hourly scoring).", "",
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
    sc = st.get("scoring") or {}
    if sc:
        lines += ["Scoring pipeline (RC1D):", "", "| horizon | waiting maturity | waiting observations | ready | scored | ineligible |",
                  "|---|---|---|---|---|---|"]
        lines += [f"| {h} | {x['waiting-maturity']} | {x['waiting-observations']} | {x['ready']} | {x['scored']} | {x['ineligible']} |"
                  for h, x in sc.items()]
        lines.append("")
    if st["recent"]:
        lines += ["| decision | outcome | reason |", "|---|---|---|"]
        lines += [f"| {r['decision_utc']} | {r['outcome']} | {r['reason']} |" for r in st["recent"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else DESK.parent
    now = _t(sys.argv[2]) if len(sys.argv) > 2 else dt.datetime.now(UTC).replace(microsecond=0)
    print(json.dumps({h: read_current(base, now, h) for h in HORIZONS}, indent=1))
