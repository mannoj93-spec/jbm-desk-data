#!/usr/bin/env python3
"""range_ops — operational lifecycle log of the range stream's runs (crypto-desk 12.2, repo 2.17).

Stdlib only and independent of the forecasting modules, so it still works when the desk's test suite fails.
Every scheduled or manual run of .github/workflows/range.yml appends rows to state/range_runs.jsonl:

  {"run_id", "decision_utc", "code_commit", "event", "stage", "outcome", "t", "reason"}

  stage    run (start/finish) | preflight (offline tests, release check) | refit | forecast (retrieval and
           registration; per-attempt detail stays in state/range_attempts.jsonl) | publish | confirm
  outcome  started | success | failure | skipped | cancelled   (per stage)
           published | skipped | failed | incomplete          (stage "run" terminal row, from `finish`)

This log is evidence of what the runner did. It never creates a forecast, an attempt or a window: a run that
fails before forecasting has lifecycle rows and nothing in the registry.

  python desk/range_ops.py start                         # decision = the 4H close this run is for
  python desk/range_ops.py record preflight=failure refit=skipped [--log FILE]
  python desk/range_ops.py finish
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

VERSION = "ops-12.2.0"
UTC = dt.timezone.utc
RUNS = "state/range_runs.jsonl"
STAGES = ("preflight", "refit", "forecast", "publish", "confirm")
OUTCOMES = ("success", "failure", "skipped", "cancelled")


def iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def boundary(now: dt.datetime) -> dt.datetime:
    return now.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=now.hour % 4)


def rows(base) -> tuple:
    """(rows, malformed count). Malformed lines are counted, never used and never fatal."""
    out, bad = [], 0
    try:
        text = (Path(base) / RUNS).read_text()
    except FileNotFoundError:
        return [], 0
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except ValueError:
            bad += 1
            continue
        if isinstance(r, dict) and isinstance(r.get("run_id"), str) and isinstance(r.get("decision_utc"), str) \
                and r.get("stage") in ("run",) + STAGES and isinstance(r.get("outcome"), str):
            out.append(r)
        else:
            bad += 1
    return out, bad


def _append(base, row):
    path = Path(base) / RUNS
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def _run_env():
    return {"run_id": os.environ.get("GITHUB_RUN_ID", "local"), "code_commit": os.environ.get("GITHUB_SHA"),
            "event": os.environ.get("GITHUB_EVENT_NAME", "local")}


def _decision_for(base, run_id, now):
    for r in reversed(rows(base)[0]):
        if r["run_id"] == run_id and r["stage"] == "run" and r["outcome"] == "started":
            return r["decision_utc"]
    return iso(boundary(now))


def start(base, now=None, env=None):
    now = now or dt.datetime.now(UTC)
    env = env or _run_env()
    row = dict(env, decision_utc=iso(boundary(now)), stage="run", outcome="started", t=iso(now), reason=None,
               ops=VERSION)
    _append(base, row)
    return row


def failure_reason(log_text: str) -> str | None:
    """The first few FAIL/ERROR lines of a unittest log, or the last non-empty line."""
    hits = [x.strip() for x in log_text.splitlines() if re.match(r"^(FAIL|ERROR):|^release check:|Error", x.strip())]
    if hits:
        return "; ".join(hits[:3])[:400]
    tail = [x.strip() for x in log_text.splitlines() if x.strip()]
    return tail[-1][:400] if tail else None


def record(base, outcomes: dict, now=None, env=None, reason=None):
    """One row per stage outcome (GitHub `steps.<id>.outcome`: success, failure, skipped, cancelled)."""
    now = now or dt.datetime.now(UTC)
    env = env or _run_env()
    dec = _decision_for(base, env["run_id"], now)
    out = []
    for stage, outcome in outcomes.items():
        if stage not in STAGES or outcome not in OUTCOMES:
            raise ValueError(f"unknown stage/outcome {stage}={outcome}")
        row = dict(env, decision_utc=dec, stage=stage, outcome=outcome, t=iso(now),
                   reason=reason if outcome == "failure" else None, ops=VERSION)
        _append(base, row)
        out.append(row)
    return out


def terminal(stage_rows: list, attempts: list) -> tuple:
    """(outcome, reason) of a run from its stage rows and its decision's attempt rows."""
    last = {}
    for r in stage_rows:
        last[r["stage"]] = r
    failed = [s for s in STAGES if last.get(s, {}).get("outcome") in ("failure", "cancelled")]
    if failed:
        s = failed[0]
        return "failed", f"{s} {last[s]['outcome']}" + (f": {last[s]['reason']}" if last[s].get("reason") else "")
    if last.get("confirm", {}).get("outcome") == "success":
        return "published", "published and confirmed"
    final = attempts[-1].get("state") if attempts else None
    if final == "skipped":
        return "skipped", attempts[-1].get("reason") or "forecast skipped"
    if not last:
        return "incomplete", "no stage recorded"
    return "incomplete", "run ended without a confirmed publication"


def finish(base, now=None, env=None):
    now = now or dt.datetime.now(UTC)
    env = env or _run_env()
    dec = _decision_for(base, env["run_id"], now)
    mine = [r for r in rows(base)[0] if r["run_id"] == env["run_id"] and r["stage"] != "run"]
    attempts = []
    try:
        for line in (Path(base) / "state/range_attempts.jsonl").read_text().splitlines():
            try:
                a = json.loads(line)
            except ValueError:
                continue
            if isinstance(a, dict) and a.get("decision_utc") == dec and \
                    isinstance(a.get("run"), dict) and a["run"].get("run_id") == env["run_id"]:
                attempts.append(a)
    except FileNotFoundError:
        pass
    outcome, why = terminal(mine, attempts)
    row = dict(env, decision_utc=dec, stage="run", outcome=outcome, t=iso(now), reason=why, ops=VERSION)
    _append(base, row)
    return row


def decision_view(runs: list, decision: str) -> dict | None:
    """What the lifecycle log says about one decision: the latest run's latest row wins; a terminal row
    overrides started. None when no run recorded anything for this decision."""
    mine = [r for r in runs if r["decision_utc"] == decision]
    if not mine:
        return None
    latest_run = mine[-1]["run_id"]
    rr = [r for r in mine if r["run_id"] == latest_run]
    term = [r for r in rr if r["stage"] == "run" and r["outcome"] != "started"]
    if term:
        return {"run_id": latest_run, "state": term[-1]["outcome"], "reason": term[-1].get("reason"), "t": term[-1]["t"]}
    fails = [r for r in rr if r["outcome"] in ("failure", "cancelled")]
    if fails:
        f = fails[0]
        return {"run_id": latest_run, "state": "failed", "reason": f"{f['stage']} {f['outcome']}"
                + (f": {f['reason']}" if f.get("reason") else ""), "t": f["t"]}
    return {"run_id": latest_run, "state": "running", "reason": f"last stage {rr[-1]['stage']} {rr[-1]['outcome']}",
            "t": rr[-1]["t"]}


def main(argv):
    base = Path(os.environ.get("RANGE_BASE", Path(__file__).resolve().parent.parent))
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "start":
        print(json.dumps(start(base)))
    elif cmd == "record":
        log = None
        pairs = {}
        args = argv[2:]
        i = 0
        while i < len(args):
            if args[i] == "--log":
                log = args[i + 1]
                i += 2
                continue
            k, _, v = args[i].partition("=")
            pairs[k] = v or "skipped"
            i += 1
        reason = None
        if log and Path(log).exists():
            reason = failure_reason(Path(log).read_text(errors="replace"))
        for r in record(base, pairs, reason=reason):
            print(json.dumps(r))
    elif cmd == "finish":
        print(json.dumps(finish(base)))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
