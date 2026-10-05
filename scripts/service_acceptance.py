#!/usr/bin/env python3
"""service_acceptance - the 24-hour infrastructure acceptance check for restored unattended operation (repo 2.26).

    python scripts/service_acceptance.py --from 2026-10-06T00:00:00Z [--to ISO] [--now ISO] [--runs-json FILE]

Read-only. It is an infrastructure check, not a research criterion, and its verdict is bound to its inputs: the
checker version, the repository commit, a hash of every record file it read, the Actions evidence (retrieval time,
count, completeness) and the window.

Verdicts (exit 0 pass, 1 fail, 2 invalid, 3 pending, 4 insufficient evidence):
  invalid       the window is shorter than 24 h or reversed - a short diagnostic never receives a restoration pass
  pending       the window, plus the last decision deadline inside it, has not ended on the evaluation clock
  insufficient  Actions run evidence is missing or incomplete, so initiation and interventions cannot be shown
  pass / fail   every target below met / at least one missed

Targets (stated before observing; unchanged from 2.25 except as noted):
  collection    >= 97% of the window's slot-to-slot intervals hold a PERSISTED, CRITICAL-SUCCESSFUL collector run
                record started without a person (2.26: a record with critical_ok false, a lost snapshot or a critical
                stage error does not count; optional-source degradation is reported as warnings); with 96 slots that
                is 95 intervals and at most 2 empty (2.25's prose said 3 - wrong). Longest interval without such a
                run <= 45 min.
  initiation    every counted run's lineage verified against the Actions run list: GitHub's schedule (event schedule
                on main), or a recovery chain whose root is a scheduled dispatcher run, or a root dispatcher run
                titled "(external)" created within 90 s after :12/:27/:42/:57 (the external timer's cadence -
                corroborating evidence, reported separately, since the owner's token cannot prove a timer).
                A root that is missing from the evidence is unknown and does not count.
  decisions     derived from the schedule, not from the records: every 4H range decision whose 75-minute run window
                ends inside the window is published eligibly; every PS1 decision whose 90-minute deadline ends inside
                it is executed, a recorded non-rebalance, or not expected under the lifecycle; no decision has more
                than one execution. Empty expected sets cannot pass a valid 24 h window (there are always six).
  persistence   every collector run of main in the window that concluded is joined to a stored record; a run with no
                record (a failed push, an uploaded artifact) is a persistence failure, and data restored later
                (data/restored/) never counts as on-time collection.
  backlog       no matured, eligible RC1D forecast unscored beyond the monitor's lag at the window's end.
  people        no run of the critical chain (collector, dispatcher, range, streams, scoring) in the window started by a
                person or by a chain a person started, and none whose initiation is unknown (it cannot prove the
                absence of a person). Runs from before 2.26 carry no lineage in their titles; records still name
                their root, and an owner dispatcher run without the "(external)" title is unknown, not a person.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cadence                    # noqa: E402
import provenance                 # noqa: E402
from watchdog import load_runs    # noqa: E402

VERSION = "acceptance-2.0.0"
UTC = dt.timezone.utc
MIN_WINDOW_H = 24
TARGETS = {"interval_share": 0.97, "longest_gap_min": 45}
RANGE_GRACE_MIN = 75
PS1_DEADLINE_MIN = 90
TIMER_MINUTES = (12, 27, 42, 57)
TIMER_TOLERANCE_S = 90
CRITICAL = {"collect.yml": "collector", "recovery.yml": "dispatcher", "range.yml": "range",
            "research-streams.yml": "streams", "range-score.yml": "scoring"}
BOT = provenance.BOT
INPUTS = ("state/range_attempts.jsonl", "state/range_publications.jsonl", "streams/ps1/decisions.jsonl",
          "streams/ps1/executions.jsonl", "streams/ps1/runs.jsonl", "streams/ps1/lifecycle.jsonl",
          "streams/ps1/launch.json", "state/forecast_manifest.json", "registry/scores.jsonl", "cadence.json")


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if isinstance(s, str) and s else None


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else None


def rows(path):
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


# ------------------------------------------------------------------------------------------- Actions evidence
def fetch_runs(repo, token, start, end, opener=None):
    """Every run created in [start - 1 h, end + 3 h], all workflows, complete pagination; (runs, complete)."""
    opener = opener or urllib.request.urlopen
    q = f"created={iso(start - dt.timedelta(hours=1))}..{iso(end + dt.timedelta(hours=3))}"
    out, page, total = [], 1, None
    while True:
        url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}&{q}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
        with opener(req, timeout=30) as r:
            body = json.loads(r.read())
        total = body.get("total_count", total)
        batch = body.get("workflow_runs", [])
        out += [{k: x.get(k) for k in ("id", "event", "status", "conclusion", "created_at", "updated_at",
                                       "display_title", "head_branch", "path", "name")}
                | {"actor": (x.get("actor") or {}).get("login"), "triggering_actor": (x.get("triggering_actor") or {}).get("login")}
                for x in batch]
        if len(batch) < 100 or page >= 40:
            break
        page += 1
    return out, total is not None and len(out) >= total


def wf_of(run):
    path = run.get("path") or ""
    return path.rsplit("/", 1)[-1].split("@")[0]


def on_timer(created):
    return created is not None and any(
        0 <= (created - created.replace(minute=m, second=0, microsecond=0)).total_seconds() <= TIMER_TOLERANCE_S
        for m in TIMER_MINUTES)


def classify(run, by_id, depth=0, origin=None):
    """Initiation of one Actions run: verified | timer-corroborated | declared-external | human | unknown.
    `origin` is the lineage a stored record carries, used when the run's title predates 2.26 and names none."""
    if run is None or depth > 4:
        return "unknown"
    if run.get("head_branch") not in (None, "main"):
        return "unknown"
    ev, trig = run.get("event"), run.get("triggering_actor")
    if ev == "schedule":
        return "verified"
    if ev == "workflow_run":
        return "verified" if trig == BOT else "unknown"   # chained after a run; its parent is checked separately
    if ev != "workflow_dispatch":
        return "human" if ev in ("push", "pull_request") else "unknown"
    if trig == BOT:
        import recovery
        origin = recovery.via(run.get("display_title")) or origin
        r = provenance.root({"source": "recovery", "origin": origin}) if origin else {"run": None, "label": "unknown"}
        if r["label"] == "human":
            return "human"
        root_run = by_id.get(str(r["run"])) if r["run"] else None
        if root_run is None:
            return "unknown"
        return classify(root_run, by_id, depth + 1, origin=f"{r['run']}:{r['label']}")
    if wf_of(run) == "recovery.yml":
        titled = (run.get("display_title") or "").endswith("(external)")
        declared = titled or (origin or "").split(":")[1:2] == ["external"]
        if declared:
            return "timer-corroborated" if on_timer(parse(run.get("created_at"))) else "declared-external"
        if run.get("display_title") == "Recovery dispatcher":
            # before 2.26 the title did not say whether the input declared "external": not a person shown, not proof
            return "unknown"
    return "human"


UNATTENDED = ("verified", "timer-corroborated")


# ------------------------------------------------------------------------------------------- decisions
def range_decisions(base, start, end):
    attempts = [a for a in rows(Path(base) / "state/range_attempts.jsonl")
                if isinstance(a.get("run"), dict) and a["run"].get("production")]
    eligible = {p.get("attempt") for p in rows(Path(base) / "state/range_publications.jsonl") if p.get("eligible") is True}
    out, d = {}, start.replace(minute=0, second=0, microsecond=0)
    while d.hour % 4:
        d += dt.timedelta(hours=1)
    while d + dt.timedelta(minutes=RANGE_GRACE_MIN) <= end:
        if d >= start:
            mine = [a for a in attempts if a.get("decision_utc") == iso(d)]
            if any(a.get("attempt") in eligible for a in mine):
                out[iso(d)] = "published"
            elif mine:
                out[iso(d)] = f"missed: {mine[-1].get('state')}"
            else:
                out[iso(d)] = "missed: absent"
        d += dt.timedelta(hours=4)
    return out


def ps1_decisions(base, start, end):
    import health
    states, info = health.ps1_decisions(base, end)
    if not info.get("launched"):
        return {}, {}
    keep = {k: v for k, v in states.items() if start <= parse(k) and parse(k) + dt.timedelta(minutes=PS1_DEADLINE_MIN) <= end}
    execs = {}
    for r in rows(Path(base) / "streams/ps1/executions.jsonl"):
        if r.get("execution_id") or r.get("fill_time_ms"):
            execs.setdefault(r.get("decision_id"), set()).add(r.get("execution_id") or r.get("fill_time_ms"))
    dup = {k: len(execs.get(f"ps1-{parse(k):%Y%m%dT%H%MZ}", ())) for k in keep}
    return keep, {k: n for k, n in dup.items() if n > 1}


def ps1_ok(state):
    return state == "executed" or state.startswith("not expected") or not (
        state.startswith("missed") or state.startswith("pending") or state in ("rebalance",))


# ------------------------------------------------------------------------------------------- measure
def digest(base, files):
    h = hashlib.sha256()
    for rel in files:
        p = Path(base) / rel
        h.update(rel.encode() + b"\0" + (p.read_bytes() if p.exists() else b"<absent>") + b"\0")
    return h.hexdigest()


def measure(base, start, end, now, runs=None, complete=False, retrieved=None):
    base = Path(base)
    doc = {"checker": VERSION, "window": [iso(start), iso(end)], "evaluated_utc": iso(now), "targets": TARGETS}
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=base, capture_output=True, text=True).stdout.strip() or None
    except OSError:
        commit = None
    run_files = sorted(str(p.relative_to(base)) for p in (base / "data/runs").glob("*.jsonl")) if (base / "data/runs").exists() else []
    doc["inputs"] = {"commit": commit, "files_sha256": digest(base, list(INPUTS) + run_files),
                     "actions": {"runs": len(runs or []), "complete": bool(runs is not None and complete),
                                 "retrieved_utc": retrieved}}
    hours = (end - start).total_seconds() / 3600
    if hours < MIN_WINDOW_H:
        doc["verdict"] = "invalid"
        doc["reason"] = f"window {hours:.2f} h < {MIN_WINDOW_H} h: diagnostics only, never a restoration pass"
        return doc
    by_id = {str(r["id"]): r for r in runs or []}
    # collection
    a, b = int(start.timestamp() * 1000), int(end.timestamp() * 1000)
    recs = [r for r in load_runs(base) if a <= r["t"] < b and cadence.is_routine(r)]
    periods = cadence.load(base)
    buckets = cadence.slot_buckets(periods, a, b)
    counted, initiations, critical_fail, degraded = [], {}, [], 0
    for r in recs:
        crit, probs = cadence.failure_summary(r)
        run = by_id.get(str(r.get("run_id")))
        init = classify(run, by_id, origin=(r.get("provenance") or {}).get("origin")) if runs is not None else "unknown"
        if run is None and runs is not None:
            init = "unknown"
        initiations[init] = initiations.get(init, 0) + 1
        if crit:
            critical_fail.append(r.get("run_id"))
            continue
        degraded += bool(probs)
        if init in UNATTENDED:
            counted.append(r["t"])
    covered = sum(1 for s, e in buckets if any(s <= t < e for t in counted))
    edges = [a] + sorted(counted) + [b]
    gap = max(y - x for x, y in zip(edges, edges[1:])) / 60000
    share = covered / len(buckets) if buckets else 0.0
    doc["collection"] = {"intervals": len(buckets), "intervals_with_unattended_critical_success": covered,
                         "share": round(share, 4), "allowed_empty": int(len(buckets) * (1 - TARGETS["interval_share"])),
                         "longest_gap_min": round(gap, 1), "records": len(recs), "by_initiation": initiations,
                         "critical_failures": critical_fail, "degraded_optional_records": degraded}
    # persistence: concluded collector runs of main with no stored record
    stored = {str(r.get("run_id")) for r in load_runs(base)}
    col_runs = [x for x in runs or [] if wf_of(x) == "collect.yml" and x.get("head_branch") == "main"
                and start <= (parse(x.get("created_at")) or start) < end and x.get("status") == "completed"
                and x.get("conclusion") not in ("cancelled", "skipped")]
    lost = [x["id"] for x in col_runs if str(x["id"]) not in stored and not (x.get("conclusion") == "success"
                                                                           and "recovery" in (x.get("display_title") or ""))]
    yielded = [x["id"] for x in col_runs if str(x["id"]) not in stored and x["id"] not in lost]
    doc["persistence"] = {"concluded_collector_runs": len(col_runs), "without_stored_record": lost,
                          "recovery_runs_that_yielded_or_stored_nothing": yielded,
                          "restored_later_not_counted": sorted(p.name for p in (base / "data/restored").glob("collector-*"))
                          if (base / "data/restored").exists() else []}
    # decisions
    horizon = min(end, now)                       # a decision whose deadline is still ahead is not judged yet
    rd = range_decisions(base, start, horizon)
    pd, dup = ps1_decisions(base, start, horizon)
    doc["decisions"] = {"range": rd, "ps1": pd, "ps1_duplicate_executions": dup}
    # backlog at the window's end
    import range_monitor
    _, minfo = range_monitor.check(base, end)
    doc["scoring_backlog"] = {h: len(v) for h, v in (minfo.get("scoring_backlog") or {}).items() if v}
    # people across the critical chain
    chain = [x for x in runs or [] if wf_of(x) in CRITICAL and x.get("head_branch") == "main"
             and start <= (parse(x.get("created_at")) or start) < end]
    kinds = {}
    people = []
    for x in chain:
        k = classify(x, by_id)
        kinds[k] = kinds.get(k, 0) + 1
        if k in ("human", "declared-external"):
            people.append({"run": x["id"], "workflow": CRITICAL[wf_of(x)], "initiation": k})
    unknown = [x["id"] for x in chain if classify(x, by_id) == "unknown"]
    doc["chain"] = {"runs": len(chain), "by_initiation": kinds, "person_or_unverified_external": people,
                    "lineage_unknown": unknown}
    checks = {
        "collection_intervals": share >= TARGETS["interval_share"],
        "longest_gap": gap <= TARGETS["longest_gap_min"],
        "range_decisions_published": bool(rd) and all(v == "published" for v in rd.values()),
        "ps1_decisions_resolved": all(ps1_ok(v) for v in pd.values()) and not dup,
        "no_persistence_failures": not lost,
        "scoring_backlog_empty": not doc["scoring_backlog"],
        "no_person_in_chain": not people,
        "chain_lineage_known": not unknown,          # unknown initiation cannot prove that no person intervened
    }
    doc["checks"] = checks
    last_deadline = end + dt.timedelta(minutes=PS1_DEADLINE_MIN)
    if now < end:
        doc["verdict"] = "pending"
        doc["reason"] = f"window ends {iso(end)}; evaluate after it (values above are partial)"
    elif runs is None or not complete:
        doc["verdict"] = "insufficient"
        doc["reason"] = "Actions run evidence missing or incomplete: initiation and interventions cannot be shown"
    else:
        doc["verdict"] = "pass" if all(checks.values()) else "fail"
    doc["note"] = (f"decisions due before {iso(end)} only; data restored after the fact never counts; "
                   f"a pass says nothing about the original scheduler's root cause (re-evaluate after {iso(last_deadline)} "
                   "if a PS1 deadline straddles the end)")
    return doc


def main(argv):
    if "--from" not in argv:
        print(__doc__)
        return 2
    start = parse(argv[argv.index("--from") + 1])
    end = parse(argv[argv.index("--to") + 1]) if "--to" in argv else start + dt.timedelta(hours=MIN_WINDOW_H)
    now = parse(argv[argv.index("--now") + 1]) if "--now" in argv else dt.datetime.now(UTC)
    if start is None or end is None or end <= start:
        print(json.dumps({"checker": VERSION, "verdict": "invalid", "reason": "window missing or reversed"}))
        return 2
    runs, complete, retrieved = None, False, None
    if "--runs-json" in argv:
        doc = json.loads(Path(argv[argv.index("--runs-json") + 1]).read_text())
        runs, complete, retrieved = doc["runs"], bool(doc.get("complete")), doc.get("retrieved_utc")
    elif (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")) and os.environ.get("GITHUB_REPOSITORY"):
        retrieved = iso(dt.datetime.now(UTC))
        runs, complete = fetch_runs(os.environ["GITHUB_REPOSITORY"], os.environ.get("GITHUB_TOKEN") or os.environ["GH_TOKEN"],
                                    start, end)
    doc = measure(ROOT, start, end, now, runs, complete, retrieved)
    print(json.dumps(doc, indent=1, sort_keys=True))
    return {"pass": 0, "fail": 1, "invalid": 2, "pending": 3, "insufficient": 4}[doc["verdict"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
