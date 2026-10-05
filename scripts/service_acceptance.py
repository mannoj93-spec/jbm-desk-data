#!/usr/bin/env python3
"""service_acceptance - the 24-hour infrastructure acceptance check for restored unattended operation (repo 2.27).

    python scripts/service_acceptance.py --from ISO [--to ISO] [--cutoff ISO] [--now ISO]
           [--actions-evidence FILE | (fetch with GITHUB_TOKEN/GH_TOKEN + GITHUB_REPOSITORY) [--save-evidence FILE]]
           [--timer-receipts FILE] [--commit SHA]

Read-only. An infrastructure check, not a research criterion. acceptance-3.0.0 (repo 2.27) replaces 2.0.0 after an
independent review reproduced false passes (PS1, lineage, yields) and unbound inputs.

Four clocks are kept apart:
  window      [--from, --to): the service period measured (>= 24 h, else invalid)
  deadlines   per decision: a 4H range decision's 75-minute run window, a PS1 decision's 90-minute execution
              deadline. A decision is judged only if its deadline falls inside the window (deadline-based inclusion)
  cutoff      the evidence-availability cutoff (default: window end + 120 min). Repository evidence is read AS OF
              THE LAST COMMIT ON THE EVALUATED BRANCH WHOSE COMMITTER TIME IS <= THE CUTOFF (git), so a fill,
              confirmation, record, receipt or score written later cannot repair the window. Committer time is not
              push time; that limit is stated in the output. Outside a git checkout availability is "unestablished".
  evaluation  --now (default: the clock). Before the cutoff the verdict is pending.

Verdicts (exit 0 pass, 1 fail, 2 invalid, 3 pending, 4 insufficient evidence):
  invalid       window shorter than 24 h or reversed
  pending       the evaluation clock is before the cutoff
  insufficient  Actions evidence (runs, pagination, needed job/step evidence, out-of-window parents) is missing or
                incomplete; or every service target passed but strict unattended certification is not established
                (see initiation) - then service_verdict is "pass" and the reason says what evidence is missing
  pass / fail   every target met / at least one missed

Targets (stated before observing; unchanged in substance since 2.25):
  collection    >= 97% of the window's slot-to-slot intervals hold a persisted run record that is a CRITICAL SUCCESS
                (cadence.critical_success - the shared definition) from a run whose initiation is not a person;
                longest interval without one <= 45 min (the acceptance target; the 90-minute watchdog limit is a
                different rule). Optional-source degradation is a warning.
  execution     every collector run of main created in the window is classified by stage (execution.py):
                persisted-success, critical-failure, yielded (only with a valid durable yield receipt naming the
                slot, the run and the already-persisted covering record, or - for runs before receipts - equivalent
                retained job evidence: the yield step succeeded, Collect was skipped and a critical-success record at
                or after the slot was stored before the yield step finished), never-started / failed-before-execution
                (a missed execution: no observation existed, so it is not a persistence loss; its slot still counts
                against collection), executed-no-output (executed, nothing stored, no valid receipt: an output or
                persistence failure) or unknown (no job evidence: insufficient). A successful run with no record and
                no valid receipt is unproven missing output, whatever its title says.
  initiation    lineage from Actions metadata, never from actor identity alone:
                  verified            GitHub's schedule on main; a workflow_run child whose named parent run (2.27
                                      titles; earlier runs: the unique completed parent workflow run on main within
                                      180 s before it) verifies, taking the parent's initiation; a recovery chain
                                      whose root (and named intermediate parent) resolve to a verified root
                  timer-receipt       an external-titled dispatcher run matched one-to-one to an independent timer
                                      provider receipt (--timer-receipts, bound by hash)
                  timer-corroborated  external-titled and within 90 s after :12/:27/:42/:57 but no receipt: the
                                      owner's credential cannot exclude a person submitting the same inputs then
                  declared-external   external-titled off the timer
                  human / unknown     a person's start, or lineage that cannot be resolved (missing parent or root,
                                      branch not main or not stated, conflicting evidence)
                Service continuity counts verified, timer-receipt and timer-corroborated; strict unattended
                certification counts only verified and timer-receipt. Any human or declared-external run in the
                critical chain (collector, dispatcher, range, streams, scoring), or any unknown one, fails.
  decisions     derived from the schedule, never from the records present: every 4H range decision is published
                eligibly; PS1 (only after its launch, validated - see ps1_evaluate) is executed once by a verified
                chain execution filled before its deadline, or a recorded no-rebalance, or not expected under an
                operator pause/termination at that time. Unknown actions, invalid chains, duplicates, late fills and
                missing or contradictory launch evidence fail.
  backlog       no matured, eligible RC1D forecast unscored beyond the monitor's lag at the window's end.
Evidence binding: the output carries the checker version and the sha256 of its own code and helper modules, the
evaluated commit, the sha256 of every consulted repository file at that commit, and the sha256 of the normalized
Actions evidence (query bounds, pagination, runs, out-of-window parents, jobs/steps) and of any timer receipts.
--save-evidence writes that Actions evidence; --actions-evidence replays it offline with --commit, reproducing the
verdict without querying mutable state. Data restored later (data/restored/) never counts as on-time.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cadence                    # noqa: E402
import execution                  # noqa: E402
import provenance                 # noqa: E402
import recovery                   # noqa: E402
from watchdog import load_runs    # noqa: E402

VERSION = "acceptance-3.0.0"
UTC = dt.timezone.utc
MIN_WINDOW_H = 24
TARGETS = {"interval_share": 0.97, "longest_gap_min": 45}
RANGE_GRACE_MIN = 75
PS1_DEADLINE_MIN = 90
CUTOFF_GRACE_MIN = 120            # default evidence-availability cutoff after the window end
TIMER_MINUTES = (12, 27, 42, 57)
TIMER_TOLERANCE_S = 90
RECEIPT_TOLERANCE_S = 30
PARENT_INFER_S = 180
CRITICAL = {"collect.yml": "collector", "recovery.yml": "dispatcher", "range.yml": "range",
            "research-streams.yml": "streams", "range-score.yml": "scoring"}
BOT = provenance.BOT
CONTINUITY = ("verified", "timer-receipt", "timer-corroborated")
STRICT = ("verified", "timer-receipt")
UNATTENDED = STRICT                       # 2.26 counted timer-corroborated here; 2.27 does not
RUN_KEYS = ("id", "run_attempt", "event", "status", "conclusion", "created_at", "updated_at", "run_started_at",
            "display_title", "head_branch", "head_sha", "path", "name")
CONSULTED = ("cadence.json", "desk/release.json", "desk/deployments.jsonl", "state/range_attempts.jsonl",
             "state/range_runs.jsonl", "state/range_publications.jsonl", "state/forecast_manifest.json",
             "reports/range_status.json", "registry/scores.jsonl", "state/recovery_yields.jsonl",
             "desk/research/ps1/protocol.json", "data/restored/receipts.jsonl")
CONSULTED_TREES = ("data/runs", "streams/ps1")
CODE = ("scripts/service_acceptance.py", "cadence.py", "execution.py", "provenance.py", "recovery.py", "watchdog.py",
        "health.py", "desk/paper_ps1.py", "desk/range_monitor.py", "desk/stream_util.py")


def parse(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if isinstance(s, str) and s else None
    except ValueError:
        return None


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else None


def ms(t):
    return int(t.timestamp() * 1000)


def rows(path):
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        if line.strip():
            try:
                r = json.loads(line)
            except ValueError:
                out.append({"_malformed": line[:80]})
                continue
            out.append(r if isinstance(r, dict) else {"_malformed": str(r)[:80]})
    return out


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canonical_sha(obj):
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


# ------------------------------------------------------------------------------------------- Actions evidence
def normalize_run(x):
    r = {k: x.get(k) for k in RUN_KEYS}
    for k in ("actor", "triggering_actor"):
        v = x.get(k)
        r[k] = v.get("login") if isinstance(v, dict) else v
    return r


def normalize_job(j):
    return {"id": j.get("id"), "run_id": j.get("run_id"), "run_attempt": j.get("run_attempt"), "name": j.get("name"),
            "status": j.get("status"), "conclusion": j.get("conclusion"), "created_at": j.get("created_at"),
            "started_at": j.get("started_at"), "completed_at": j.get("completed_at"), "runner_id": j.get("runner_id"),
            "steps": [{k: s.get(k) for k in ("number", "name", "status", "conclusion", "started_at", "completed_at")}
                      for s in j.get("steps") or []]}


def _get(url, token, opener):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                                               "X-GitHub-Api-Version": "2022-11-28"})
    with (opener or urllib.request.urlopen)(req, timeout=30) as r:
        return json.loads(r.read())


def fetch_evidence(repo, token, start, end, now=None, opener=None):
    """Actions evidence for [start, end): every run created in [start - 6 h, end + 3 h] (all workflows, complete
    pagination recorded page by page). Parents, roots and jobs are added by complete_evidence()."""
    lo, hi = start - dt.timedelta(hours=6), end + dt.timedelta(hours=3)
    q = f"created={iso(lo)}..{iso(hi)}"
    runs, pages, total, page = [], [], None, 1
    while True:
        body = _get(f"https://api.github.com/repos/{repo}/actions/runs?per_page=100&page={page}&{q}", token, opener)
        batch = body.get("workflow_runs") or []
        total = body.get("total_count", total)
        pages.append({"page": page, "count": len(batch), "total_count": body.get("total_count")})
        runs += [normalize_run(x) for x in batch]
        if len(batch) < 100 or page >= 40:
            break
        page += 1
    ids = [r["id"] for r in runs]
    return {"schema": "actions-evidence/1", "repo": repo, "retrieved_utc": iso(now or dt.datetime.now(UTC)),
            "query": {"created_from": iso(lo), "created_to": iso(hi), "per_page": 100, "branch": None},
            "pages": pages, "total_count": total,
            "complete": total is not None and len(runs) >= total and len(set(ids)) == len(ids),
            "runs": runs, "extra_runs": [], "jobs": {}, "jobs_requested": [], "jobs_complete": True}


def complete_evidence(ev, need_runs, need_jobs, token, opener=None):
    """Fetch named runs absent from the listing (parents, roots outside the window) and the jobs of the named runs.
    Failures are recorded, never filled in."""
    have = {str(r["id"]) for r in ev["runs"] + ev["extra_runs"]}
    for rid in sorted(set(map(str, need_runs)) - have):
        try:
            ev["extra_runs"].append(dict(normalize_run(_get(
                f"https://api.github.com/repos/{ev['repo']}/actions/runs/{rid}", token, opener)), fetched_individually=True))
        except Exception as exc:                                  # noqa: BLE001 - recorded as missing
            ev.setdefault("missing_runs", []).append({"id": rid, "error": type(exc).__name__})
    for rid in sorted(set(map(str, need_jobs)) - set(ev["jobs"])):
        ev["jobs_requested"].append(rid)
        try:
            body = _get(f"https://api.github.com/repos/{ev['repo']}/actions/runs/{rid}/jobs?per_page=50&filter=all",
                        token, opener)
            ev["jobs"][rid] = [normalize_job(j) for j in body.get("jobs") or []]
        except Exception:                                         # noqa: BLE001 - recorded as incomplete
            ev["jobs_complete"] = False
    return ev


def wf_of(run):
    path = (run or {}).get("path") or ""
    return path.rsplit("/", 1)[-1].split("@")[0]


def on_timer(created):
    return created is not None and any(
        0 <= (created - created.replace(minute=m, second=0, microsecond=0)).total_seconds() <= TIMER_TOLERANCE_S
        for m in TIMER_MINUTES)


# ------------------------------------------------------------------------------------------- lineage
class Lineage:
    """Initiation of Actions runs from normalized evidence (see the module docstring)."""

    def __init__(self, runs, receipts=None):
        self.by_id = {str(r["id"]): r for r in runs}
        self.runs = runs
        self.memo = {}
        self.receipt_match = self._match_receipts(receipts)

    def _match_receipts(self, receipts):
        """{dispatcher run id: receipt index}: external-titled dispatcher runs matched one-to-one to timer receipts."""
        if not receipts:
            return {}
        exe = [(i, parse(e.get("executed_utc"))) for i, e in enumerate(receipts.get("executions") or [])
               if isinstance(e, dict) and e.get("status") in (200, 201, 204)]
        exe = [(i, t) for i, t in exe if t]
        disp = sorted((r for r in self.runs if wf_of(r) == "recovery.yml" and r.get("event") == "workflow_dispatch"
                       and (r.get("display_title") or "").endswith("(external)")), key=lambda r: r.get("created_at") or "")
        used, out = set(), {}
        for r in disp:
            c = parse(r.get("created_at"))
            best = [(abs((c - t).total_seconds()), i) for i, t in exe if i not in used
                    and -5 <= (c - t).total_seconds() <= RECEIPT_TOLERANCE_S] if c else []
            if best:
                _, i = min(best)
                used.add(i)
                out[str(r["id"])] = i
        return out

    def parent_of(self, run):
        """(parent run, method) for a workflow_run child, or (None, reason)."""
        named = provenance.workflow_run_parent(run.get("display_title"))
        allowed = provenance.WORKFLOW_RUN_PARENTS.get(wf_of(run), ())
        c = parse(run.get("created_at"))
        if named:
            p = self.by_id.get(named[0])
            if p is None:
                return None, f"named parent {named[0]} not in the evidence"
            if wf_of(p) not in allowed:
                return None, f"named parent {named[0]} is {wf_of(p)}, not a parent workflow of {wf_of(run)}"
            pu = parse(p.get("updated_at"))
            if p.get("status") != "completed" or pu is None or c is None or pu > c + dt.timedelta(seconds=60):
                return None, f"named parent {named[0]} had not completed before the child started"
            if p.get("run_attempt") not in (None, named[1]):
                # a rerun replaces the run's metadata with its latest attempt; the child names the attempt it followed
                return p, f"named parent {named[0]} attempt {named[1]} (evidence shows attempt {p.get('run_attempt')})"
            return p, "named by the run (event payload)"
        if c is None:
            return None, "child has no creation time"
        # a run started with the workflow token (github-actions[bot] dispatch) raises no workflow_run event, so it
        # cannot be the parent
        cands = [p for p in self.runs if wf_of(p) in allowed and p.get("status") == "completed"
                 and p.get("head_branch") == "main" and parse(p.get("updated_at"))
                 and not (p.get("event") == "workflow_dispatch" and p.get("triggering_actor") == BOT)
                 and 0 <= (c - parse(p.get("updated_at"))).total_seconds() <= PARENT_INFER_S]
        if len(cands) == 1:
            return cands[0], ("inferred: the only completed parent-workflow run on main able to raise workflow_run "
                              "within 180 s (title predates 2.27)")
        return None, (f"{len(cands)} candidate parents within {PARENT_INFER_S} s" if cands else "no parent run found")

    def classify(self, run, origin=None, depth=0):
        """(label, why)."""
        if run is None:
            return "unknown", "run not in the evidence"
        key = (str(run.get("id")), origin)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = ("unknown", "cycle")
        out = self._classify(run, origin, depth)
        self.memo[key] = out
        return out

    def _classify(self, run, origin, depth):
        if depth > 6:
            return "unknown", "lineage deeper than 6 hops"
        branch = run.get("head_branch")
        if branch != "main":
            return "unknown", f"branch {branch!r} is not main" if branch else "branch not stated"
        ev, trig = run.get("event"), run.get("triggering_actor")
        if ev == "schedule":
            return "verified", "GitHub schedule on main"
        if ev == "workflow_run":
            parent, how = self.parent_of(run)
            if parent is None:
                return "unknown", f"workflow_run: {how}"
            label, why = self.classify(parent, depth=depth + 1)
            return label, f"workflow_run after {parent['id']} ({how}); parent {why}"
        if ev == "workflow_dispatch" and trig == BOT:
            org = recovery.via(run.get("display_title")) or origin
            r = provenance.root({"source": "recovery", "origin": org}) if org else {"run": None, "label": "unknown"}
            if r["label"] == "human":
                return "human", f"recovery chain declared started by a person ({org})"
            if not r["run"]:
                return "unknown", "bot dispatch without a resolvable origin"
            root_run = self.by_id.get(str(r["run"]))
            if root_run is None:
                return "unknown", f"root {r['run']} not in the evidence"
            if r.get("parent") and str(r["parent"]) != str(r["run"]):
                par = self.by_id.get(str(r["parent"]))
                if par is None:
                    return "unknown", f"named parent {r['parent']} not in the evidence"
                pr = provenance.root({"source": "recovery", "origin": recovery.via(par.get("display_title")) or ""})
                if str(pr.get("run")) != str(r["run"]):
                    return "unknown", f"parent {r['parent']} does not belong to root {r['run']}"
            label, why = self.classify(root_run, origin=f"{r['run']}:{r['label']}", depth=depth + 1)
            return label, f"recovery chain rooted at {r['run']}: {why}"
        if ev == "workflow_dispatch" and wf_of(run) == "recovery.yml":
            titled = (run.get("display_title") or "").endswith("(external)")
            declared = titled or (origin or "").split(":")[1:2] == ["external"]
            if declared:
                if str(run["id"]) in self.receipt_match:
                    return "timer-receipt", "external dispatch matched to a timer provider receipt"
                if on_timer(parse(run.get("created_at"))):
                    return "timer-corroborated", "external-titled on the timer cadence; no provider receipt"
                return "declared-external", "external-titled off the timer cadence"
            if run.get("display_title") == "Recovery dispatcher":
                return "unknown", "untitled owner dispatcher run (before 2.26 titles, or a person without inputs)"
        if ev in ("workflow_dispatch", "push", "pull_request"):
            return "human", f"{ev} by {trig}"
        return "unknown", f"event {ev}"


# ------------------------------------------------------------------------------------------- repository snapshot
def git(base, *args):
    r = subprocess.run(["git", *args], cwd=base, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def snapshot(base, cutoff, commit=None):
    """(directory, info): the consulted repository files as of the cutoff. In a git checkout: the last first-parent
    commit of HEAD (or --commit) with committer time <= cutoff, extracted to a temporary directory. Otherwise the
    working tree, with availability at the cutoff unestablished."""
    base = Path(base)
    head = commit or "HEAD"
    out = git(base, "rev-list", "-1", "--first-parent", f"--before={iso(cutoff)}", head) if (base / ".git").exists() else None
    if not out:
        return base, {"commit": None, "method": "working tree (not a git checkout): availability at the cutoff is "
                                                "not established"}
    sha = out.decode().strip()
    ctime = (git(base, "show", "-s", "--format=%cI", sha) or b"").decode().strip()
    listed = (git(base, "ls-tree", "-r", "--name-only", sha) or b"").decode().splitlines()
    want = [p for p in listed if p in CONSULTED or p.startswith(tuple(t + "/" for t in CONSULTED_TREES))]
    tmp = Path(tempfile.mkdtemp(prefix="acceptance-"))
    for p in want:
        data = git(base, "show", f"{sha}:{p}")
        if data is not None:
            (tmp / p).parent.mkdir(parents=True, exist_ok=True)
            (tmp / p).write_bytes(data)
    return tmp, {"commit": sha, "commit_time": ctime,
                 "method": "last first-parent commit with committer time <= cutoff (committer time, not push time)"}


def consulted_files(snap):
    snap = Path(snap)
    files = [p for p in CONSULTED]
    for t in CONSULTED_TREES:
        if (snap / t).exists():
            files += sorted(str(p.relative_to(snap)) for p in (snap / t).rglob("*") if p.is_file())
    return {f: (sha256_bytes((snap / f).read_bytes()) if (snap / f).exists() else "absent") for f in sorted(set(files))}


def code_digest():
    return {f: (sha256_bytes((ROOT / f).read_bytes()) if (ROOT / f).exists() else "absent") for f in CODE}


# ------------------------------------------------------------------------------------------- decisions
def range_decisions(base, start, end):
    """Expected 4H decisions whose 75-minute run window ends inside [start, end]: published eligibly or missed."""
    attempts = [a for a in rows(Path(base) / "state/range_attempts.jsonl")
                if isinstance(a.get("run"), dict) and a["run"].get("production")]
    eligible = {p.get("attempt") for p in rows(Path(base) / "state/range_publications.jsonl") if p.get("eligible") is True}
    out, d = {}, start.replace(minute=0, second=0, microsecond=0)
    while d.hour % 4 or d < start:
        d += dt.timedelta(hours=1)
    while d + dt.timedelta(minutes=RANGE_GRACE_MIN) <= end:
        mine = [a for a in attempts if a.get("decision_utc") == iso(d)]
        if any(a.get("attempt") in eligible for a in mine):
            out[iso(d)] = "published"
        elif mine:
            out[iso(d)] = f"missed: {mine[-1].get('state')}"
        else:
            out[iso(d)] = "missed: absent"
        d += dt.timedelta(hours=4)
    return out


PS1_VALID = ("executed", "no-rebalance (recorded)")


def ps1_ok(state):
    """Explicit valid outcomes only (2.27; 2.26 accepted anything not on a rejection list)."""
    return state in PS1_VALID or state.startswith("not expected (lifecycle ")


def _lifecycle_at(life, t_ms):
    state, by = "proposed", None
    for r in life:
        if isinstance(r.get("t_ms"), int) and r["t_ms"] <= t_ms:
            state, by = r.get("state"), r.get("by")
    return state, by


def ps1_evaluate(base, start, end, cutoff):
    """PS1 expected decisions and their validated outcomes. Returns {status, evidence_ok, problems, decisions,
    duplicates, chain}. Launch, protocol and lifecycle evidence are validated before deciding whether PS1 is expected;
    the expected set comes from the launch and the schedule, never from the outcome rows present."""
    import paper_ps1 as P
    base = Path(base)
    root = base / P.ROOT
    problems = []
    proto = base / "desk/research/ps1/protocol.json"
    if not proto.exists() or sha256_bytes(proto.read_bytes()) != P.PROTOCOL_SHA256:
        problems.append("protocol file absent or differs from the frozen PS1 protocol")
    max_delay = PS1_DEADLINE_MIN
    life = sorted((r for r in rows(root / "lifecycle.jsonl") if r.get("key") == P.PROTOCOL_SHA256),
                  key=lambda r: r.get("t_ms") if isinstance(r.get("t_ms"), int) else -1)
    cut = ms(cutoff)
    life = [r for r in life if isinstance(r.get("t_ms"), int) and r["t_ms"] <= cut]
    decs = {}
    for r in rows(root / "decisions.jsonl"):
        if "_malformed" in r or not isinstance(r.get("decision_id"), str):
            problems.append("malformed decision row")
            continue
        decs.setdefault(r["decision_id"], r)                      # first write wins, as in paper_ps1.decisions
    activity = bool(decs) or bool(rows(root / "executions.jsonl")) or bool(rows(root / "execution_states.jsonl")) \
        or any(r.get("state") in ("active", "paused", "terminated", "archived") for r in life)
    launch_path = root / "launch.json"
    launch = None
    if launch_path.exists():
        try:
            launch = json.loads(launch_path.read_text())
        except ValueError:
            problems.append("launch record is not valid JSON")
        if launch is not None and (not isinstance(launch, dict) or parse(launch.get("first_decision_utc")) is None
                                   or launch.get("protocol_sha256") != P.PROTOCOL_SHA256):
            problems.append("launch record malformed or under another protocol")
            launch = None
    chain = P.verify_chain(base) if activity else {"ok": True, "verified": [], "rows": [], "failures": [],
                                                    "exclusions": [], "ledger_rows": {"physical": 0}}
    if chain["failures"]:
        problems += [f"chain: {f['reason']}" for f in chain["failures"][:5]]
    if launch is None and not launch_path.exists():
        if activity:
            problems.append("no launch record although the stream has decisions, executions or an active lifecycle")
            status = "invalid"
        else:
            return {"status": "not launched", "evidence_ok": not problems, "problems": problems, "decisions": {},
                    "duplicates": {}, "chain": {"ok": True, "verified": 0}}
    else:
        want = P.expected_launch(chain)
        if launch is not None and (want is None or any(launch.get(k) != want[k] for k in
                                                      ("first_decision_utc", "first_execution_ms", "protocol_sha256"))):
            problems.append("launch record contradicts the earliest verified execution")
        status = "launched" if launch is not None else "invalid"
    first = parse((launch or {}).get("first_decision_utc"))
    # verified executions by decision, with their fill and completion times
    by_dec = {}
    for r in chain["rows"]:
        by_dec.setdefault(r.get("decision_id"), {}).setdefault(r.get("execution_id"), []).append(r)
    final_t = {eid: st[-1].get("t_ms") for eid, st in P.exec_states(base).items() if st}
    out, dup = {}, {}
    if first is not None:
        t = first
        while t + dt.timedelta(minutes=max_delay) <= end:
            if t >= start:
                did, k = f"ps1-{t:%Y%m%dT%H%MZ}", iso(t)
                deadline = ms(t) + max_delay * 60_000
                st, by = _lifecycle_at(life, ms(t))
                execs = {eid: rs for eid, rs in by_dec.get(did, {}).items()
                         if all(isinstance(r.get("fill_time_ms"), int) and r["fill_time_ms"] <= deadline for r in rs)
                         and isinstance(final_t.get(eid), int) and final_t[eid] <= cut}
                late = set(by_dec.get(did, {})) - set(execs)
                d = decs.get(did)
                if len(by_dec.get(did, {})) > 1:
                    dup[k] = len(by_dec[did])
                if st in ("terminated", "archived") or (st == "paused" and by == "operator"):
                    s = f"not expected (lifecycle {st}{' by ' + by if by else ''})"
                elif d is None:
                    s = "missed: no decision record"
                elif d.get("action") == "rebalance":
                    s = ("executed" if len(execs) == 1 else
                         "invalid: duplicate execution" if len(execs) > 1 else
                         "missed: filled after the deadline or the cutoff" if late else
                         "missed: not executed by the deadline")
                elif d.get("action") == "no-rebalance":
                    ok_t = isinstance(d.get("computed_end_ms"), int) and d["computed_end_ms"] <= deadline
                    s = ("invalid: execution of a no-rebalance decision" if by_dec.get(did) else
                         "no-rebalance (recorded)" if ok_t else "missed: no-rebalance recorded after the deadline")
                elif d.get("action") == "missed":
                    s = "missed: decision processed after its deadline"
                else:
                    s = f"invalid: unrecognized action {str(d.get('action'))[:40]!r}"
                out[k] = s
            t += dt.timedelta(hours=4)
    if status == "launched" and first is not None and first >= end:
        status = "launched after the window"
    return {"status": status, "evidence_ok": not problems, "problems": problems, "decisions": out, "duplicates": dup,
            "chain": {"ok": chain["ok"], "verified": len(chain["verified"]),
                      "physical_rows": (chain.get("ledger_rows") or {}).get("physical")}}


YIELD_STEP = "Recovery yields when its slot is already collected"


def job_yield(run, jobs, records):
    """Equivalent retained job evidence of a legitimate yield, for runs before yield receipts (2.27): the yield step
    succeeded, the Collect step was skipped, and a CRITICALLY SUCCESSFUL record at or after the run's titled slot was
    already stored when the yield step finished. Returns the receipt-like proof or None."""
    title = (run or {}).get("display_title") or ""
    if not title.startswith("Collector recovery ") or not jobs:
        return None
    slot = parse(title.split(" ")[2]) if len(title.split(" ")) > 2 else None
    steps = {s.get("name"): s for j in jobs for s in j.get("steps") or []}
    y, c = steps.get(YIELD_STEP), steps.get("Collect")
    done = parse((y or {}).get("completed_at"))
    if slot is None or not y or y.get("conclusion") != "success" or (c or {}).get("conclusion") != "skipped" or done is None:
        return None
    cover = [r for r in records if cadence.critical_success(r) and ms(slot) <= r["t"] <= ms(done)]
    if not cover:
        return None
    return {"schema": "job-evidence-yield", "slot": iso(slot), "run_id": str(run["id"]),
            "covering": {"run_id": str(cover[0].get("run_id")), "t": cover[0]["t"]}, "checked_utc": iso(done)}


# ------------------------------------------------------------------------------------------- measure
def needs(base, start, end, ev):
    """(run ids to fetch individually, run ids whose jobs are needed) for complete evidence."""
    runs = ev["runs"] + ev["extra_runs"]
    have = {str(r["id"]) for r in runs}
    need_runs = set()
    for r in runs:
        org = recovery.via(r.get("display_title"))
        if org:
            rt = provenance.root({"source": "recovery", "origin": org})
            for x in (rt.get("run"), rt.get("parent")):
                if x and str(x) not in have:
                    need_runs.add(str(x))
        par = provenance.workflow_run_parent(r.get("display_title"))
        if par and par[0] not in have:
            need_runs.add(par[0])
    stored = {str(r.get("run_id")) for r in load_runs(base)}
    need_jobs = {str(r["id"]) for r in runs if wf_of(r) == "collect.yml" and r.get("head_branch") == "main"
                 and start <= (parse(r.get("created_at")) or start) < end and str(r["id"]) not in stored
                 and r.get("status") == "completed"}
    return need_runs, need_jobs


def measure(base, start, end, now, evidence=None, receipts=None, cutoff=None, commit=None):
    cutoff = cutoff or end + dt.timedelta(minutes=CUTOFF_GRACE_MIN)
    doc = {"checker": VERSION, "code_sha256": code_digest(),
           "clocks": {"window": [iso(start), iso(end)], "evidence_cutoff_utc": iso(cutoff), "evaluated_utc": iso(now),
                      "deadlines": {"range_run_window_min": RANGE_GRACE_MIN, "ps1_execution_min": PS1_DEADLINE_MIN,
                                    "inclusion": "a decision is judged when its deadline falls inside the window"}},
           "targets": TARGETS}
    hours = (end - start).total_seconds() / 3600
    if hours < MIN_WINDOW_H:
        doc.update(verdict="invalid", reason=f"window {hours:.2f} h < {MIN_WINDOW_H} h: diagnostics only, never a pass")
        return doc
    if cutoff < end:
        doc.update(verdict="invalid", reason="evidence cutoff before the window end")
        return doc
    snap, sinfo = snapshot(base, cutoff, commit)
    try:
        return _measure(doc, snap, sinfo, start, end, now, evidence, receipts, cutoff)
    finally:
        if snap != Path(base):
            shutil.rmtree(snap, ignore_errors=True)


def _measure(doc, base, sinfo, start, end, now, ev, receipts, cutoff):
    doc["inputs"] = {"repository": sinfo, "files_sha256": consulted_files(base),
                     "actions": None if ev is None else {
                         "sha256": canonical_sha(ev), "retrieved_utc": ev.get("retrieved_utc"), "query": ev.get("query"),
                         "runs": len(ev.get("runs") or []), "extra_runs": len(ev.get("extra_runs") or []),
                         "complete": bool(ev.get("complete")), "jobs_complete": bool(ev.get("jobs_complete")),
                         "missing_runs": ev.get("missing_runs") or []},
                     "timer_receipts": None if receipts is None else {"sha256": canonical_sha(receipts),
                                                                      "provider": receipts.get("provider"),
                                                                      "executions": len(receipts.get("executions") or [])}}
    runs = (ev["runs"] + ev["extra_runs"]) if ev else []
    L = Lineage(runs, receipts)
    by_id = L.by_id
    a, b = ms(start), ms(end)
    all_recs = load_runs(base)
    recs = [r for r in all_recs if a <= r["t"] < b and cadence.is_routine(r)]
    buckets = cadence.slot_buckets(cadence.load(base), a, b)
    cont, strict, inits, crit_fail, degraded = [], [], {}, [], 0
    for r in recs:
        run = by_id.get(str(r.get("run_id")))
        label, _ = L.classify(run, origin=(r.get("provenance") or {}).get("origin")) if ev else ("unknown", "")
        inits[label] = inits.get(label, 0) + 1
        if not cadence.critical_success(r):
            crit_fail.append(r.get("run_id"))
            continue
        degraded += bool(cadence.failure_summary(r)[1])
        if label in CONTINUITY:
            cont.append(r["t"])
        if label in STRICT:
            strict.append(r["t"])

    def cover(ts):
        held = sum(1 for s, e in buckets if any(s <= t < e for t in ts))
        edges = [a] + sorted(ts) + [b]
        return held, round(max(y - x for x, y in zip(edges, edges[1:])) / 60000, 1), (held / len(buckets) if buckets else 0.0)
    held, gap, share = cover(cont)
    s_held, s_gap, s_share = cover(strict)
    doc["collection"] = {"intervals": len(buckets), "intervals_with_critical_success": held, "share": round(share, 4),
                         "allowed_empty": int(len(buckets) * (1 - TARGETS["interval_share"])),
                         "longest_gap_min": gap, "records": len(recs), "by_initiation": inits,
                         "critical_failures": crit_fail, "degraded_optional_records": degraded,
                         "strict": {"intervals_with_critical_success": s_held, "share": round(s_share, 4),
                                    "longest_gap_min": s_gap},
                         "rule": "continuity counts verified, timer-receipt and timer-corroborated starts; strict "
                                 "counts verified and timer-receipt only"}
    # execution stages of every collector run of main created in the window
    yields = [y for y in rows(base / "state/recovery_yields.jsonl") if "_malformed" not in y]
    stored = {str(r.get("run_id")): r for r in all_recs}
    col = [x for x in runs if wf_of(x) == "collect.yml" and x.get("head_branch") == "main"
           and start <= (parse(x.get("created_at")) or start) < end]
    phases, never, lost, unknown_stage, open_runs, proven_by_jobs = {}, [], [], [], [], 0
    for x in col:
        rid = str(x["id"])
        rc = None
        for y in yields:
            if str(y.get("run_id")) == rid and recovery.valid_yield(y, all_recs, x)[0]:
                rc = y
        jobs = (ev.get("jobs") or {}).get(rid) if ev else None
        if rc is None and rid not in stored:
            rc = job_yield(x, jobs, all_recs)
            proven_by_jobs += rc is not None
        st = execution.stages(x, jobs, stored.get(rid), rc, now)
        phases[st["phase"]] = phases.get(st["phase"], 0) + 1
        if st["phase"] in execution.NOT_EXECUTED:
            never.append(x["id"])
        elif st["phase"] == "executed-no-output":
            lost.append(x["id"])
        elif st["phase"] in ("queued", "in-progress"):
            open_runs.append(x["id"])
        elif st["phase"] == "unknown":
            unknown_stage.append(x["id"])
    doc["execution"] = {"collector_runs": len(col), "by_phase": phases, "never_executed": never,
                        "executed_without_stored_output": lost, "stage_unknown": unknown_stage,
                        "not_finished_at_evaluation": open_runs, "valid_yield_receipts": phases.get("yielded", 0) - proven_by_jobs,
                        "yields_proven_by_job_evidence": proven_by_jobs,
                        "restored_later_not_counted": sorted(p.name for p in (base / "data/restored").glob("collector-*"))
                        if (base / "data/restored").exists() else [],
                        "rule": "never-started / failed-before-execution = missed execution (no observation existed); "
                                "executed-no-output = output or persistence failure; a yield needs a valid receipt"}
    rd = range_decisions(base, start, end)
    p1 = ps1_evaluate(base, start, end, cutoff)
    doc["decisions"] = {"range": rd, "ps1": p1["decisions"], "ps1_status": p1["status"], "ps1_problems": p1["problems"],
                        "ps1_duplicate_executions": p1["duplicates"], "ps1_chain": p1["chain"]}
    import range_monitor
    _, minfo = range_monitor.check(base, end)
    doc["scoring_backlog"] = {h: len(v) for h, v in (minfo.get("scoring_backlog") or {}).items() if v}
    chain = [x for x in runs if wf_of(x) in CRITICAL and start <= (parse(x.get("created_at")) or start) < end
             and x.get("head_branch") == "main"]
    kinds, people, unknown, tc = {}, [], [], 0
    for x in chain:
        k, why = L.classify(x)
        kinds[k] = kinds.get(k, 0) + 1
        if k in ("human", "declared-external"):
            people.append({"run": x["id"], "workflow": CRITICAL[wf_of(x)], "initiation": k})
        elif k == "unknown":
            unknown.append({"run": x["id"], "workflow": CRITICAL[wf_of(x)], "why": why})
        tc += k == "timer-corroborated"
    off_main = [x["id"] for x in runs if wf_of(x) in CRITICAL and start <= (parse(x.get("created_at")) or start) < end
                and x.get("head_branch") != "main"]
    doc["chain"] = {"runs": len(chain), "by_initiation": kinds, "person_or_unverified_external": people,
                    "lineage_unknown": unknown, "not_main_ignored": off_main}
    checks = {
        "collection_intervals": share >= TARGETS["interval_share"],
        "longest_gap": gap <= TARGETS["longest_gap_min"],
        "range_decisions_published": bool(rd) and all(v == "published" for v in rd.values()),
        "ps1_evidence_valid": p1["evidence_ok"] and not p1["status"].startswith("invalid"),
        "ps1_decisions_resolved": all(ps1_ok(v) for v in p1["decisions"].values()) and not p1["duplicates"],
        "no_lost_output": not lost,
        "scoring_backlog_empty": not doc["scoring_backlog"],
        "no_person_in_chain": not people,
        "chain_lineage_known": not unknown,
    }
    doc["checks"] = checks
    service = "pass" if all(checks.values()) else "fail"
    strict_ok = s_share >= TARGETS["interval_share"] and s_gap <= TARGETS["longest_gap_min"] and tc == 0
    doc["service_verdict"] = service
    doc["unattended_certification"] = ("established" if strict_ok and service == "pass" else
                                       "not applicable (service failed)" if service == "fail" else
                                       "insufficient evidence")
    if now < cutoff:
        doc.update(verdict="pending", reason=f"evidence cutoff {iso(cutoff)} not reached; values are partial")
    elif ev is None or not ev.get("complete") or ev.get("missing_runs"):
        doc.update(verdict="insufficient", reason="Actions run evidence missing, incomplete or missing named parents/roots")
    elif not ev.get("jobs_complete") or unknown_stage:
        doc.update(verdict="insufficient", reason="job/step evidence missing for collector runs without a stored record")
    elif service == "fail":
        doc.update(verdict="fail")
    elif not strict_ok:
        doc.update(verdict="insufficient",
                   reason=f"service targets met, but strict unattended certification is not established: {tc} critical-"
                          "chain run(s) are only timer-corroborated (owner credential; no independent provider "
                          "receipt) - supply --timer-receipts from the timer provider to bind them")
    else:
        doc.update(verdict="pass")
    doc["note"] = ("restored data never counts; a pass says nothing about the original native-schedule root cause; "
                   "repository availability is committer time at the cutoff, not push time")
    return doc


def main(argv):
    def arg(k):
        return argv[argv.index(k) + 1] if k in argv else None
    if "--from" not in argv:
        print(__doc__)
        return 2
    start = parse(arg("--from"))
    end = parse(arg("--to")) if arg("--to") else (start and start + dt.timedelta(hours=MIN_WINDOW_H))
    now = parse(arg("--now")) if arg("--now") else dt.datetime.now(UTC)
    cutoff = parse(arg("--cutoff")) if arg("--cutoff") else (end and end + dt.timedelta(minutes=CUTOFF_GRACE_MIN))
    if start is None or end is None or end <= start:
        print(json.dumps({"checker": VERSION, "verdict": "invalid", "reason": "window missing or reversed"}))
        return 2
    receipts = json.loads(Path(arg("--timer-receipts")).read_text()) if arg("--timer-receipts") else None
    ev = None
    if arg("--actions-evidence"):
        ev = json.loads(Path(arg("--actions-evidence")).read_text())
    elif (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")) and os.environ.get("GITHUB_REPOSITORY"):
        token = os.environ.get("GITHUB_TOKEN") or os.environ["GH_TOKEN"]
        ev = fetch_evidence(os.environ["GITHUB_REPOSITORY"], token, start, end)
        snap, _ = snapshot(ROOT, min(cutoff, now), arg("--commit"))
        try:
            for _ in range(3):                                    # roots of roots: bounded
                need_runs, need_jobs = needs(snap, start, end, ev)
                complete_evidence(ev, need_runs, need_jobs, token)
        finally:
            if snap != ROOT:
                shutil.rmtree(snap, ignore_errors=True)
        if arg("--save-evidence"):
            Path(arg("--save-evidence")).write_text(json.dumps(ev, indent=1, sort_keys=True) + "\n")
    doc = measure(ROOT, start, end, now, ev, receipts, cutoff, arg("--commit"))
    print(json.dumps(doc, indent=1, sort_keys=True))
    return {"pass": 0, "fail": 1, "invalid": 2, "pending": 3, "insufficient": 4}[doc["verdict"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
