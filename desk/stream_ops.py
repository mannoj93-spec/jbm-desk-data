#!/usr/bin/env python3
"""stream_ops — stage log and verdict for the research-streams workflow (repo 2.21, stream-ops-1.0.0).

Every workflow stage runs through `run`, which records one row in streams/ops/stages-YYYY-MM.jsonl:
run id and attempt, stage, required/optional, started and completed times, status (completed, failed, skipped),
exit code, the error tail, each declared artifact (exists, sha256) and, for test stages, the test counts.
`verdict` reads this run's rows and exits non-zero unless every expected required stage completed with its
artifacts and the persist step succeeded. A skipped optional stage is labelled, never counted as success of a
required output. Nothing here changes what a stage computes.

  stream_ops.py run --stage NAME (--required|--optional) [--artifact PATH]... [--needs STAGE]... [--tests] [--semantic] -- CMD...
  stream_ops.py verdict --expect A,B,C [--persist-outcome OUTCOME] [--check-persisted PATH]... [--branch main]

1.1.0 (repo 2.22): a stage's command may print one line `OUTCOME {json}` (desk/stream_util.emit) with class done,
expected or error; class error fails the stage even when the command exits 0, and --semantic makes a missing
OUTCOME line a failure. The verdict re-checks every recorded artifact (still present, same sha256) and, with
--check-persisted, that the intended record paths are committed and the commit is on origin/<branch>.
  stream_ops.py counts < unittest-output     (prints the parsed test counts)
Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

VERSION = "stream-ops-1.1.0"
DESK = Path(__file__).resolve().parent
BASE = Path(os.environ.get("JBM_DESK_BASE") or DESK.parent)
ROOT = "streams/ops"


def _now_ms() -> int:
    return int(time.time() * 1000)


def log_path(base, t_ms=None) -> Path:
    t = time.gmtime((t_ms or _now_ms()) / 1000)
    return Path(base) / ROOT / f"stages-{t.tm_year:04d}-{t.tm_mon:02d}.jsonl"


def run_identity(env=None) -> dict:
    env = os.environ if env is None else env
    return {"run_id": env.get("GITHUB_RUN_ID", "local"), "run_attempt": env.get("GITHUB_RUN_ATTEMPT", "1"),
            "event": env.get("GITHUB_EVENT_NAME", "local"), "triggering_run": env.get("TRIGGERING_RUN_ID") or None,
            "code_commit": env.get("GITHUB_SHA", "local")}


def _append(path: Path, row: dict) -> None:
    sys.path.insert(0, str(DESK)); sys.path.insert(0, str(BASE))
    from storage import append_unique
    append_unique(path, [row], key=lambda r: (r["run_id"], r["run_attempt"], r["stage"], r["started_ms"]))


def rows_for_run(base, ident: dict) -> list:
    out = []
    for p in sorted((Path(base) / ROOT).glob("stages-*.jsonl")):
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("run_id") == ident["run_id"] and str(r.get("run_attempt")) == str(ident["run_attempt"]):
                    out.append(r)
    return out


# --------------------------------------------------------------------------------------------
# Test counts: executed, passed, failed, skipped and unavailable are reported separately.
# unittest's "Ran N" includes skipped tests; executed = ran - skipped.
# --------------------------------------------------------------------------------------------
def parse_counts(text: str) -> dict:
    m = re.search(r"^Ran (\d+) tests? in", text, re.M)
    if not m:
        return {"ran": None, "executed": None, "passed": None, "failed": None, "errors": None, "skipped": None,
                "unavailable": "test output not found (the suite did not run or could not be loaded)"}
    ran = int(m.group(1))
    tail = text[m.end():]
    def k(name):
        mm = re.search(rf"{name}=(\d+)", tail)
        return int(mm.group(1)) if mm else 0
    failed, errors, skipped = k("failures"), k("errors"), k("skipped")
    xf, xs = k("expected failures"), k("unexpected successes")
    executed = ran - skipped
    return {"ran": ran, "executed": executed, "passed": executed - failed - errors - xf - xs, "failed": failed,
            "errors": errors, "skipped": skipped, "expected_failures": xf, "unexpected_successes": xs,
            "unavailable": None, "ok": bool(re.search(r"^OK\b", tail, re.M))}


def _artifacts(base, paths, since_ms=None) -> list:
    """Each declared artifact: exists, written during this stage (mtime at or after its start), sha256."""
    out = []
    for p in paths:
        f = Path(base) / p
        ok = f.is_file()
        fresh = ok and (since_ms is None or f.stat().st_mtime * 1000 >= since_ms - 1000)
        out.append({"path": p, "exists": ok, "written_this_stage": fresh,
                    "sha256": hashlib.sha256(f.read_bytes()).hexdigest() if ok else None})
    return out


def parse_outcome(text: str):
    """The last `OUTCOME {json}` line a command printed, or None."""
    found = None
    for line in text.splitlines():
        if line.startswith("OUTCOME "):
            try:
                found = json.loads(line[len("OUTCOME "):])
            except ValueError:
                found = {"class": "error", "outcome": "unparseable OUTCOME line"}
    return found


def run_stage(base, stage: str, required: bool, cmd: list, artifacts=(), needs=(), tests=False,
              ident=None, runner=subprocess.run, semantic=False) -> dict:
    base = Path(base)
    ident = ident or run_identity()
    started = _now_ms()
    row = dict(ident, stage=stage, required=required, started_ms=started, job=VERSION, command=" ".join(cmd)[:300])
    done = {r["stage"]: r for r in rows_for_run(base, ident)}
    unmet = [n for n in needs if (done.get(n) or {}).get("status") != "completed"]
    if unmet:
        row.update(status="skipped", completed_ms=_now_ms(), exit_code=None,
                   error=f"not run: needed stage(s) {', '.join(unmet)} did not complete", artifacts=_artifacts(base, artifacts))
        _append(log_path(base, started), row)
        print(f"[{stage}] skipped: {row['error']}")
        return row
    try:
        p = runner(cmd, cwd=str(base), capture_output=True, text=True)
        out, err, code = p.stdout or "", p.stderr or "", p.returncode
    except (OSError, ValueError) as exc:
        out, err, code = "", f"{type(exc).__name__}: {exc}", 127
    sys.stdout.write(out)
    sys.stderr.write(err)
    arts = _artifacts(base, artifacts, started)
    missing = [a["path"] for a in arts if not (a["exists"] and a["written_this_stage"])]
    status, error = "completed", None
    outcome = parse_outcome(out)
    if code != 0:
        status, error = "failed", (((outcome or {}).get("outcome") or "") + " " + (err.strip() or out.strip())[-400:]).strip() or f"exit {code}"
    elif outcome is not None and outcome.get("class") not in ("done", "expected"):
        status, error = "failed", f"semantic outcome: {outcome.get('outcome')} (class {outcome.get('class')})"
    elif semantic and outcome is None:
        status, error = "failed", "no machine-readable OUTCOME line"
    elif missing:
        status, error = "failed", f"missing artifact(s) (absent or not written by this stage): {', '.join(missing)}"
    row.update(status=status, completed_ms=_now_ms(), exit_code=code, error=error, artifacts=arts, outcome=outcome)
    if tests:
        row["tests"] = parse_counts(err + "\n" + out)
        if status == "completed" and row["tests"]["ran"] is None:
            row.update(status="failed", error="test counts unavailable")
    _append(log_path(base, started), row)
    print(f"[{stage}] {status}" + (f": {error}" if error else ""))
    return row


def check_persisted(base, paths: list, branch: str = "main", runner=subprocess.run) -> list:
    """Problems with persistence of the intended records: uncommitted changes under `paths`, or a HEAD that is
    not on origin/<branch> after a fetch."""
    base = Path(base)
    probs = []
    st = runner(["git", "status", "--porcelain", "--"] + list(paths), cwd=str(base), capture_output=True, text=True)
    if st.returncode != 0:
        return [f"git status failed: {st.stderr.strip()[:200]}"]
    if st.stdout.strip():
        probs.append("records not committed: " + "; ".join(st.stdout.strip().splitlines()[:5]))
    f = runner(["git", "fetch", "--quiet", "origin", branch], cwd=str(base), capture_output=True, text=True)
    if f.returncode != 0:
        return probs + [f"git fetch failed: {f.stderr.strip()[:200]}"]
    a = runner(["git", "merge-base", "--is-ancestor", "HEAD", f"origin/{branch}"], cwd=str(base), capture_output=True, text=True)
    if a.returncode != 0:
        probs.append(f"this run's commit is not on origin/{branch}")
    return probs


def verdict(base, expect: list, persist_outcome=None, ident=None, persisted=None, branch="main",
            runner=subprocess.run) -> dict:
    ident = ident or run_identity()
    base = Path(base)
    rows = {}
    for r in rows_for_run(base, ident):
        rows[r["stage"]] = r                              # last row for a stage in this attempt wins
    problems, optional = [], []
    for st in expect:
        r = rows.get(st)
        if r is None:
            problems.append(f"{st}: not run")
            continue
        if r["required"] and r["status"] != "completed":
            problems.append(f"{st}: {r['status']} ({r.get('error')})")
        elif not r["required"] and r["status"] != "completed":
            optional.append(f"{st}: optional, {r['status']} ({r.get('error')})")
    for st, r in rows.items():
        if st not in expect and r["required"] and r["status"] != "completed":
            problems.append(f"{st}: {r['status']} ({r.get('error')})")
    for st, r in rows.items():                             # final gate: artifacts still present and unchanged
        if r["status"] != "completed":
            continue
        for a in r.get("artifacts") or []:
            f = base / a["path"]
            now_sha = hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None
            if now_sha != a.get("sha256"):
                msg = f"{st}: artifact {a['path']} {'missing' if now_sha is None else 'changed'} after the stage completed"
                (problems if r["required"] else optional).append(msg)
    if persisted:
        problems += [f"persist: {p}" for p in check_persisted(base, persisted, branch, runner)]
    if persist_outcome is not None and persist_outcome != "success":
        problems.append(f"persist: {persist_outcome} (records not confirmed on the remote)")
    status = "failed" if problems else ("completed with optional stages not completed" if optional else "completed")
    starts = [v["started_ms"] for v in rows.values()]
    ends = [v.get("completed_ms") or v["started_ms"] for v in rows.values()]
    doc = {"run": ident, "status": status, "required_problems": problems, "optional_not_completed": optional,
           "logged_span_s": round((max(ends) - min(starts)) / 1000, 1) if rows else None,
           "stages": {k: {"required": v["required"], "status": v["status"], "error": v.get("error"),
                          "outcome": v.get("outcome"),
                          "artifacts": v.get("artifacts"), "tests": v.get("tests"),
                          "started_ms": v["started_ms"], "completed_ms": v.get("completed_ms")} for k, v in rows.items()},
           "job": VERSION}
    summ = os.environ.get("GITHUB_STEP_SUMMARY")
    if summ:
        with open(summ, "a") as fh:
            fh.write(f"## Research streams: {status}\n\n| stage | required | status | error |\n|---|---|---|---|\n")
            for k, v in doc["stages"].items():
                fh.write(f"| {k} | {v['required']} | {v['status']} | {(v['error'] or '')[:120]} |\n")
            for p in problems + optional:
                fh.write(f"\n- {p}")
            fh.write("\n")
    return doc


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "run":
        cmd = argv[argv.index("--") + 1:] if "--" in argv else []
        ap = argparse.ArgumentParser(prog="stream_ops.py run")
        ap.add_argument("--stage", required=True)
        g = ap.add_mutually_exclusive_group(required=True)
        g.add_argument("--required", action="store_true")
        g.add_argument("--optional", action="store_true")
        ap.add_argument("--artifact", action="append", default=[])
        ap.add_argument("--needs", action="append", default=[])
        ap.add_argument("--tests", action="store_true")
        ap.add_argument("--semantic", action="store_true")
        a = ap.parse_args(argv[1:argv.index("--")] if "--" in argv else argv[1:])
        if not cmd:
            ap.error("a command after -- is required")
        if cmd[0] == "python":
            cmd[0] = sys.executable
        r = run_stage(BASE, a.stage, a.required, cmd, a.artifact, a.needs, a.tests, semantic=a.semantic)
        return 0 if r["status"] == "completed" else 1
    if argv and argv[0] == "verdict":
        ap = argparse.ArgumentParser(prog="stream_ops.py verdict")
        ap.add_argument("--expect", required=True)
        ap.add_argument("--persist-outcome")
        ap.add_argument("--check-persisted", action="append", default=[])
        ap.add_argument("--branch", default="main")
        a = ap.parse_args(argv[1:])
        doc = verdict(BASE, [x for x in a.expect.split(",") if x], a.persist_outcome, persisted=a.check_persisted,
                      branch=a.branch)
        print(json.dumps({k: doc[k] for k in ("status", "required_problems", "optional_not_completed", "logged_span_s")}, indent=1))
        return 1 if doc["status"] == "failed" else 0
    if argv and argv[0] == "counts":
        print(json.dumps(parse_counts(sys.stdin.read())))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
