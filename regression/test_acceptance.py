"""service_acceptance 3.0 (repo 2.27). Reproduces the independent review's counterexamples against 2.26 - PS1 false passes
(launch removed, corrupt actions with no executions, fills after the window), timer-corroborated credited as
unattended, owner-actor workflow_run children unknown, a titled recovery run with no output exempted, verdicts not
bound to their evidence - and covers valid controls: a complete healthy day built on the REAL PS1 chain of
2026-10-04/05 (regression/fixtures/ps1_2026-10-05, verified by paper_ps1.verify_chain), legitimately unlaunched PS1,
recorded no-rebalance, operator pause, proven yields, no-runner cancellations, delayed timer delivery, offline replay
and a git cutoff that later repairs cannot cross. Collector, dispatcher and range records are synthetic."""
import copy
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk"), str(ROOT / "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)
import recovery as R              # noqa: E402
import service_acceptance as A   # noqa: E402

UTC = dt.timezone.utc
START = dt.datetime(2026, 10, 4, 18, 0, tzinfo=UTC)     # PS1 decisions 20:00 .. 16:00 inside, all really executed
END = START + dt.timedelta(hours=24)
AFTER = END + dt.timedelta(hours=3)
BOT = "github-actions[bot]"
OWNER = "mannoj93-spec"
FIX = ROOT / "regression/fixtures"
PS1_FIX = FIX / "ps1_2026-10-05"
ACT_FIX = FIX / "actions_2026-10-05"


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def ms(t):
    return int(t.timestamp() * 1000)


def jobs_ran(runner=1000003169):
    return [{"id": 1, "runner_id": runner, "status": "completed", "conclusion": "success",
             "steps": [{"number": 1, "name": "Set up job", "status": "completed", "conclusion": "success",
                        "started_at": "x", "completed_at": "x"}]}]


def jobs_no_runner():
    return json.loads((ACT_FIX / "collector_jobs.json").read_text())["37360591638"]   # real: runner_id 0, no steps


class World:
    """A complete healthy day: every slot collected (alternating native runs and recovery chains rooted in the external
    timer), six range decisions published, the six real PS1 decisions of the window executed, no backlog."""
    def __init__(self, d):
        self.d = Path(d)
        for sub in ("data/runs", "state", "registry", "reports", "desk/research/ps1", "streams"):
            (self.d / sub).mkdir(parents=True, exist_ok=True)
        (self.d / "cadence.json").write_text(json.dumps({"periods": [{"from": "2026-09-23T16:06:13Z", "minutes": [7, 22, 37, 52]}]}))
        (self.d / "desk/release.json").write_text(json.dumps({"range_stream_start_utc": "2026-09-26T04:00:00Z"}))
        shutil.copy(ROOT / "desk/research/ps1/protocol.json", self.d / "desk/research/ps1/protocol.json")
        shutil.copytree(PS1_FIX, self.d / "streams/ps1")
        self.runs, self.records, self.next_id, self.jobs, self.receipts = [], [], 1000, {}, []
        t = START + dt.timedelta(minutes=7)
        i = 0
        while t < END:
            if i % 2 == 0:
                self.collector(t + dt.timedelta(minutes=2), native=True)
            else:
                at = t + dt.timedelta(minutes=5, seconds=20)
                disp = self.run("recovery.yml", at, "workflow_dispatch", OWNER, title="Recovery dispatcher (external)")
                self.receipts.append({"executed_utc": iso(at - dt.timedelta(seconds=2)), "status": 204})
                self.collector(t + dt.timedelta(minutes=6), native=False, root=f"{disp['id']}:external")
            t += dt.timedelta(minutes=15)
            i += 1
        att, pubs = [], []
        d = START.replace(hour=20)
        while d + dt.timedelta(minutes=75) <= END:
            rr = self.run("range.yml", d + dt.timedelta(minutes=3), "schedule", OWNER)
            a = f"{iso(d)}#{rr['id']}"
            att.append({"attempt": a, "decision_utc": iso(d), "state": "published",
                        "run": {"production": True, "run_id": str(rr["id"]), "event": "schedule"}})
            pubs.append({"attempt": a, "eligible": True, "start_ms": ms(d + dt.timedelta(minutes=20))})
            d += dt.timedelta(hours=4)
        self.write("state/range_attempts.jsonl", att)
        self.write("state/range_publications.jsonl", pubs)
        (self.d / "state/forecast_manifest.json").write_text("{}")
        self.flush()

    def run(self, wf, created, event, trig, title=None, conclusion="success", branch="main", status="completed"):
        self.next_id += 1
        r = {"id": self.next_id, "run_attempt": 1, "event": event, "status": status,
             "conclusion": conclusion if status == "completed" else None,
             "created_at": iso(created), "updated_at": iso(created + dt.timedelta(minutes=2)),
             "display_title": title or {"collect.yml": "Collector", "range.yml": "Range forecasts",
                                        "recovery.yml": "Recovery dispatcher"}.get(wf, wf),
             "head_branch": branch, "path": f".github/workflows/{wf}", "actor": trig, "triggering_actor": trig}
        self.runs.append(r)
        return r

    def collector(self, t, native, root=None, critical=True, persist=True, slot=None, **extra):
        if native:
            r = self.run("collect.yml", t, "schedule", OWNER)
            prov = {"source": "native-schedule"}
        else:
            r = self.run("collect.yml", t, "workflow_dispatch", BOT,
                         title=f"Collector recovery {slot or iso(t - dt.timedelta(minutes=6))} via {root}")
            prov = {"source": "recovery", "origin": root}
        if persist:
            rec = {"t": ms(t), "mode": "routine", "runner": "github", "trigger": r["event"], "run_id": str(r["id"]),
                   "critical_ok": critical, "errors": {}, "series": {}, "snap": {"books_ok": 17, "books": 17},
                   "provenance": prov, "code_version": "test"}
            rec.update(extra)
            self.records.append(rec)
        self.jobs[str(r["id"])] = jobs_ran()
        return r

    def write(self, rel, rows):
        (self.d / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.d / rel).write_text("".join(json.dumps(r) + "\n" for r in rows))

    def flush(self):
        self.write("data/runs/2026-10.jsonl", self.records)

    def evidence(self):
        return {"schema": "actions-evidence/1", "repo": "o/r", "retrieved_utc": iso(AFTER), "query": {"created_from": "x"},
                "pages": [{"page": 1, "count": len(self.runs)}], "total_count": len(self.runs), "complete": True,
                "runs": copy.deepcopy(self.runs), "extra_runs": [], "jobs": copy.deepcopy(self.jobs),
                "jobs_requested": [], "jobs_complete": True}

    def receipts_doc(self):
        return {"provider": "test-timer", "executions": copy.deepcopy(self.receipts)}

    def measure(self, start=START, end=END, now=AFTER, ev="default", receipts="default", cutoff=None):
        ev = self.evidence() if ev == "default" else ev
        receipts = self.receipts_doc() if receipts == "default" else receipts
        return A.measure(self.d, start, end, now, ev, receipts, cutoff)


GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def commit_at(d, when, msg="c"):
    """Commit the whole fixture directory with committer time `when` (git history = repository availability)."""
    e = dict(GIT_ENV, GIT_AUTHOR_DATE=iso(when), GIT_COMMITTER_DATE=iso(when))
    if not (Path(d) / ".git").exists():
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, env=e, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", msg, "--allow-empty"], cwd=d, env=e, check=True, capture_output=True)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.w = World(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()


# ------------------------------------------------------------------------------------------- valid control
class HealthyDayTests(Base):
    def test_complete_healthy_day_on_the_real_ps1_chain_passes_with_its_numbers(self):
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "pass", (doc["checks"], doc.get("reason")))
        c = doc["collection"]
        self.assertEqual((c["intervals"], c["intervals_with_critical_success"], c["allowed_empty"]), (95, 95, 2))
        self.assertEqual(c["by_initiation"], {"verified": 48, "timer-receipt": 48})
        self.assertEqual(len(doc["decisions"]["range"]), 6)
        self.assertEqual(set(doc["decisions"]["ps1"].values()), {"executed"})
        self.assertEqual(len(doc["decisions"]["ps1"]), 6)
        self.assertEqual(doc["decisions"]["ps1_chain"], {"ok": True, "verified": 10, "physical_rows": 60})
        self.assertEqual(doc["unattended_certification"], "established")

    def test_short_window_is_invalid_and_before_the_cutoff_is_pending(self):
        self.assertEqual(self.w.measure(start=START + dt.timedelta(hours=1), end=START + dt.timedelta(hours=2))["verdict"],
                         "invalid")
        self.assertEqual(self.w.measure(now=END + dt.timedelta(minutes=30))["verdict"], "pending")   # cutoff end+120

    def test_missing_or_incomplete_actions_evidence_is_insufficient(self):
        self.assertEqual(self.w.measure(ev=None)["verdict"], "insufficient")
        ev = self.w.evidence()
        ev["complete"] = False
        self.assertEqual(self.w.measure(ev=ev)["verdict"], "insufficient")


# ------------------------------------------------------------------------------------------- PS1 (section 3)
class PS1Tests(Base):
    P = "streams/ps1"

    def rewrite(self, name, fn):
        path = self.w.d / self.P / name
        rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        path.write_text("".join(json.dumps(r) + "\n" for r in (fn(r) for r in rows) if r is not None))

    def ps1(self, start=START, end=END, git=False):
        h = A.History(self.w.d, "HEAD") if git else None
        return A.ps1_evaluate(self.w.d, start, end, end + dt.timedelta(hours=2), h)

    def test_reproduced_launch_removed_fails(self):
        (self.w.d / self.P / "launch.json").unlink()
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "fail")
        self.assertFalse(doc["checks"]["ps1_evidence_valid"])
        self.assertIn("no launch record", " ".join(doc["decisions"]["ps1_problems"]))

    def test_reproduced_corrupt_actions_without_executions_fail(self):
        (self.w.d / self.P / "executions.jsonl").write_text("")
        self.rewrite("decisions.jsonl", lambda r: dict(r, action="unrecognized-corrupt-action"))
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "fail")
        self.assertFalse(doc["checks"]["ps1_decisions_resolved"])
        self.assertTrue(all(v.startswith("invalid: unrecognized action") for v in doc["decisions"]["ps1"].values()))

    def test_reproduced_fills_after_the_window_fail(self):
        self.rewrite("executions.jsonl", lambda r: dict(r, fill_time_ms=ms(END) + 3_600_000))
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "fail")
        self.assertFalse(doc["checks"]["ps1_evidence_valid"])          # the chain no longer verifies
        self.assertTrue(all(v.startswith("missed") for v in doc["decisions"]["ps1"].values()))

    def test_legitimately_unlaunched_stream_expects_nothing(self):
        shutil.rmtree(self.w.d / self.P)
        out = self.ps1()
        self.assertEqual((out["status"], out["decisions"], out["evidence_ok"]), ("not launched", {}, True))
        self.assertEqual(self.w.measure()["verdict"], "pass")

    def test_historical_misses_and_missing_record_fail(self):
        out = self.ps1(START - dt.timedelta(hours=24), START)          # Oct 3 18:00 - Oct 4 18:00: the real misses
        self.assertEqual(out["decisions"]["2026-10-03T20:00:00Z"], "executed")
        self.assertEqual(out["decisions"]["2026-10-04T08:00:00Z"], "missed: decision processed after its deadline")
        later = self.ps1(START + dt.timedelta(hours=6), END + dt.timedelta(hours=6))   # includes Oct 5 20:00: no record
        self.assertEqual(later["decisions"]["2026-10-05T20:00:00Z"], "missed: no decision record")

    T20 = dt.datetime(2026, 10, 5, 20, tzinfo=UTC)

    def _add_decision(self, action, computed_after_min=10, **extra):
        t = self.T20
        row = {"decision_id": "ps1-20261005T2000Z", "decision_utc": iso(t), "action": action,
               "protocol_sha256": json.loads((self.w.d / self.P / "launch.json").read_text())["protocol_sha256"],
               "computed_end_ms": ms(t) + computed_after_min * 60_000}
        row.update(extra)
        with open(self.w.d / self.P / "decisions.jsonl", "a") as f:
            f.write(json.dumps(row) + "\n")

    def test_valid_no_rebalance_needs_valid_fields_and_repository_availability(self):
        win = (START + dt.timedelta(hours=6), END + dt.timedelta(hours=6))
        commit_at(self.w.d, self.T20 - dt.timedelta(hours=1), "before")
        self._add_decision("no-rebalance")
        commit_at(self.w.d, self.T20 + dt.timedelta(minutes=12), "recorded on time")
        st = self.ps1(*win, git=True)
        self.assertEqual(st["decisions"]["2026-10-05T20:00:00Z"], "no-rebalance (recorded)")
        self.assertTrue(st["evidence_ok"] and all(A.ps1_ok(v) for v in st["decisions"].values()))
        # without history its on-time availability is unestablished; never resolved
        self.assertFalse(A.ps1_ok(self.ps1(*win)["decisions"]["2026-10-05T20:00:00Z"]))

    def test_reviewer_bare_or_late_no_rebalance_does_not_resolve(self):
        win = (START + dt.timedelta(hours=6), END + dt.timedelta(hours=6))
        commit_at(self.w.d, self.T20 - dt.timedelta(hours=1), "before")
        self._add_decision("no-rebalance", protocol_sha256=None)                  # bare row (review finding 4)
        commit_at(self.w.d, self.T20 + dt.timedelta(minutes=12))
        self.assertEqual(self.ps1(*win, git=True)["decisions"]["2026-10-05T20:00:00Z"],
                         "missed: no-rebalance record invalid or after the deadline")
        self.tearDown(); self.setUp()
        commit_at(self.w.d, self.T20 - dt.timedelta(hours=1), "before")
        self._add_decision("no-rebalance")
        commit_at(self.w.d, self.T20 + dt.timedelta(hours=3), "written after the deadline")
        self.assertEqual(self.ps1(*win, git=True)["decisions"]["2026-10-05T20:00:00Z"],
                         "unresolved: no-rebalance not in the repository before the deadline")
        self.tearDown(); self.setUp()
        self._add_decision("bogus")
        self.assertFalse(A.ps1_ok(self.ps1(*win)["decisions"]["2026-10-05T20:00:00Z"]))
        self.tearDown(); self.setUp()
        self._add_decision("no-rebalance", computed_after_min=120)
        self.assertEqual(self.ps1(*win)["decisions"]["2026-10-05T20:00:00Z"],
                         "missed: no-rebalance record invalid or after the deadline")

    def _pause(self, t, by="operator", frm="active", state="paused"):
        key = json.loads((self.w.d / self.P / "launch.json").read_text())["protocol_sha256"]
        with open(self.w.d / self.P / "lifecycle.jsonl", "a") as f:
            f.write(json.dumps({"key": key, "state": state, "by": by, "t_ms": t, "from": frm}) + "\n")

    def test_operator_pause_is_not_expected_but_a_job_pause_is(self):
        win = (START + dt.timedelta(hours=6), END + dt.timedelta(hours=6))
        commit_at(self.w.d, self.T20 - dt.timedelta(hours=2), "before")
        t = ms(self.T20 - dt.timedelta(hours=1))
        self._pause(t)
        commit_at(self.w.d, self.T20 - dt.timedelta(minutes=50), "operator pause")
        self.assertEqual(self.ps1(*win, git=True)["decisions"]["2026-10-05T20:00:00Z"],
                         "not expected (lifecycle paused by operator)")
        self.rewrite("lifecycle.jsonl", lambda r: dict(r, by="job") if r.get("t_ms") == t else r)
        commit_at(self.w.d, self.T20 - dt.timedelta(minutes=49), "job pause")
        self.assertEqual(self.ps1(*win, git=True)["decisions"]["2026-10-05T20:00:00Z"], "missed: no decision record")

    def test_reviewer_backdated_or_invalid_lifecycle_rows_excuse_nothing(self):
        # review finding 3: strip the window's PS1 records, then add a pause dated before the window
        for name in ("decisions.jsonl", "executions.jsonl", "execution_states.jsonl", "confirmations.jsonl"):
            keep = START.strftime("%Y%m%dT%H%MZ")
            self.rewrite(name, lambda r: r if str(r.get("decision_id") or (r.get("snapshot") or {}).get("decision_id")
                                                   or "")[4:] < keep else None)
        (self.w.d / self.P / "execution_states.jsonl").write_text(
            "".join(l + "\n" for l in (self.w.d / self.P / "execution_states.jsonl").read_text().splitlines()))
        commit_at(self.w.d, START - dt.timedelta(hours=2), "window records missing")
        self.assertEqual(self.w.measure()["verdict"], "fail")
        self._pause(ms(START) - 1)                                     # backdated, committed after the deadlines
        commit_at(self.w.d, END + dt.timedelta(hours=1), "backdated pause")
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "fail", doc["decisions"]["ps1"])
        self.assertTrue(all(v.startswith(("unresolved", "missed")) for v in doc["decisions"]["ps1"].values()))
        self.tearDown(); self.setUp()
        self._pause(ms(START) - 1, by=None, frm=None, state="terminated")         # no actor, no transition
        out = self.ps1()
        self.assertIn("lifecycle row 2: unknown actor None", " ".join(out["problems"]))
        self.assertFalse(out["evidence_ok"])

    def test_off_schedule_decision_ids_are_problems(self):
        with open(self.w.d / self.P / "decisions.jsonl", "a") as f:
            f.write(json.dumps({"decision_id": "ps1-20261005T0100Z", "action": "garbage"}) + "\n")
        self.assertIn("not a scheduled 4H decision", " ".join(self.ps1()["problems"]))

    def test_invalid_chain_and_duplicate_execution_fail(self):
        self.rewrite("executions.jsonl", lambda r: dict(r, cash_after=r["cash_after"] + 1)
                     if r.get("decision_id") == "ps1-20261005T0800Z" else r)
        self.assertFalse(self.ps1()["evidence_ok"])
        self.tearDown(); self.setUp()
        rows = [json.loads(l) for l in (self.w.d / self.P / "executions.jsonl").read_text().splitlines()]
        dup = [dict(r, execution_id=r["execution_id"] + "-dup") for r in rows if r["decision_id"] == "ps1-20261005T0800Z"]
        with open(self.w.d / self.P / "executions.jsonl", "a") as f:
            f.write("".join(json.dumps(r) + "\n" for r in dup))
        out = self.ps1()
        self.assertFalse(out["evidence_ok"])
        self.assertEqual(self.w.measure()["verdict"], "fail")

    def test_contradictory_launch_fails(self):
        p = self.w.d / self.P / "launch.json"
        p.write_text(json.dumps(dict(json.loads(p.read_text()), first_decision_utc="2026-10-04T20:00:00Z")))
        self.assertIn("launch record contradicts the earliest verified execution", self.ps1()["problems"])


# ------------------------------------------------------------------------------------------- lineage (section 4)
def real_runs():
    return [json.loads(l) for l in (ACT_FIX / "lineage_runs.jsonl").read_text().splitlines() if l.strip()]


class LineageTests(unittest.TestCase):
    def test_real_owner_actor_streams_child_resolves_to_its_native_range_parent(self):
        runs = real_runs()
        L = A.Lineage(runs)
        child = [r for r in runs if r["id"] == 37339803624][0]
        label, why = L.classify(child)
        self.assertEqual(label, "verified", why)                       # 2.26: unknown
        self.assertIn("37339238832", why)                              # not the bot-started recovery range run
        rec = [r for r in runs if r["id"] == 37339631785][0]
        self.assertEqual(L.classify(rec)[0], "timer-corroborated")     # owner external root, no provider receipt

    def test_named_parent_wins_and_must_verify(self):
        runs = real_runs()
        child = dict([r for r in runs if r["id"] == 37339803624][0],
                     display_title="Research streams after run 37339238832 attempt 1")
        self.assertEqual(A.Lineage(runs + [child]).classify(child)[0], "verified")
        bad = dict(child, display_title="Research streams after run 37339008552 attempt 1")     # bot-started range
        self.assertEqual(A.Lineage(runs).classify(bad)[0], "timer-corroborated")      # its own chain, not "verified"
        missing = dict(child, display_title="Research streams after run 99 attempt 1")
        self.assertEqual(A.Lineage(runs).classify(missing)[0], "unknown")

    def test_bot_child_without_parent_and_human_parent(self):
        orphan = {"id": 5, "event": "workflow_run", "status": "completed", "created_at": "2026-10-05T16:18:23Z",
                  "head_branch": "main", "path": ".github/workflows/research-streams.yml", "triggering_actor": BOT,
                  "display_title": "Research streams"}
        self.assertEqual(A.Lineage([orphan]).classify(orphan)[0], "unknown")        # 2.26: verified by actor alone
        parent = {"id": 4, "event": "workflow_dispatch", "status": "completed", "created_at": "2026-10-05T16:10:00Z",
                  "updated_at": "2026-10-05T16:17:00Z", "head_branch": "main", "path": ".github/workflows/range.yml",
                  "triggering_actor": OWNER, "display_title": "Range forecasts"}
        child = dict(orphan, display_title="Research streams after run 4 attempt 1", triggering_actor=OWNER)
        self.assertEqual(A.Lineage([parent, child]).classify(child)[0], "human")

    def test_unknown_branch_is_not_main(self):
        r = {"id": 7, "event": "schedule", "head_branch": None, "path": ".github/workflows/collect.yml"}
        self.assertEqual(A.Lineage([r]).classify(r)[0], "unknown")
        self.assertEqual(A.Lineage([dict(r, head_branch="dev")]).classify(dict(r, head_branch="dev"))[0], "unknown")

    def test_multihop_recovery_and_parent_outside_the_window(self):
        runs = real_runs()
        streams = [r for r in runs if r["id"] == 37339631785][0]
        no_parent = [r for r in runs if r["id"] != 37339008552]
        self.assertEqual(A.Lineage(no_parent).classify(streams)[0], "unknown")     # named intermediate parent missing
        sched_root = dict([r for r in runs if r["id"] == 37338966228][0], event="schedule", triggering_actor=OWNER,
                          display_title="Recovery dispatcher")
        runs2 = [sched_root if r["id"] == 37338966228 else r for r in runs]
        self.assertEqual(A.Lineage(runs2).classify(streams)[0], "verified")
        # the root outside the window comes in through extra_runs (complete_evidence) and still resolves
        ev = {"runs": [r for r in runs2 if r["id"] != 37338966228], "extra_runs": [sched_root]}
        self.assertEqual(A.Lineage(ev["runs"] + ev["extra_runs"]).classify(streams)[0], "verified")

    def test_delayed_timer_delivery_and_a_manual_dispatch_timed_like_the_timer(self):
        d = {"id": 9, "event": "workflow_dispatch", "status": "completed", "created_at": "2026-10-05T16:13:20Z",
             "head_branch": "main", "path": ".github/workflows/recovery.yml", "triggering_actor": OWNER,
             "display_title": "Recovery dispatcher (external)"}
        self.assertEqual(A.Lineage([d]).classify(d)[0], "timer-corroborated")      # 80 s late: still on the cadence
        rc = {"provider": "t", "executions": [{"executed_utc": "2026-10-05T16:13:18Z", "status": 204}]}
        self.assertEqual(A.Lineage([d], rc).classify(d)[0], "timer-receipt")
        # a person submitting the same inputs at :12:30 looks identical without a receipt - never strict
        m = dict(d, id=10, created_at="2026-10-05T16:12:30Z")
        lab = A.Lineage([d, m], rc).classify(m)[0]
        self.assertEqual(lab, "timer-corroborated")
        self.assertNotIn(lab, A.STRICT)
        self.assertEqual(A.Lineage([dict(d, created_at="2026-10-05T16:05:00Z")]).classify(
            dict(d, created_at="2026-10-05T16:05:00Z"))[0], "declared-external")

    def test_timer_corroboration_alone_is_insufficient_for_certification(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            doc = w.measure(receipts=None)
            self.assertEqual((doc["service_verdict"], doc["verdict"]), ("pass", "insufficient"))
            self.assertEqual(doc["unattended_certification"], "insufficient evidence")
            self.assertEqual(doc["collection"]["by_initiation"], {"verified": 48, "timer-corroborated": 48})

    def test_person_started_dispatcher_taints_its_children(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = World(tmp)
            disp = w.run("recovery.yml", START + dt.timedelta(hours=3, minutes=33), "workflow_dispatch", OWNER)
            w.run("research-streams.yml", START + dt.timedelta(hours=3, minutes=40), "workflow_dispatch", BOT,
                  title=f"Research streams recovery x via {disp['id']}:human")
            w.run("range.yml", START + dt.timedelta(hours=8, minutes=10), "workflow_dispatch", OWNER)
            doc = w.measure()
            people = doc["chain"]["person_or_unverified_external"]
            self.assertEqual(sorted(p["workflow"] for p in people), ["range", "streams"])
            self.assertEqual([u["workflow"] for u in doc["chain"]["lineage_unknown"]], ["dispatcher"])
            self.assertEqual(doc["verdict"], "fail")


# ------------------------------------------------------------------------------------------- execution (section 5)
class ExecutionTests(Base):
    def test_no_runner_cancellation_is_a_missed_execution_not_a_persistence_loss(self):
        r = self.w.run("collect.yml", START + dt.timedelta(hours=2, minutes=8), "schedule", OWNER, conclusion="failure")
        self.w.jobs[str(r["id"])] = jobs_no_runner()
        doc = self.w.measure()
        self.assertEqual(doc["execution"]["never_executed"], [r["id"]])
        self.assertEqual(doc["execution"]["executed_without_stored_output"], [])
        self.assertTrue(doc["checks"]["no_lost_output"])

    def test_executed_run_without_output_and_unproven_titled_recovery_fail(self):
        r = self.w.run("collect.yml", START + dt.timedelta(hours=2, minutes=8), "schedule", OWNER, conclusion="failure")
        self.w.jobs[str(r["id"])] = jobs_ran()
        doc = self.w.measure()
        self.assertEqual(doc["execution"]["executed_without_stored_output"], [r["id"]])
        self.assertFalse(doc["checks"]["no_lost_output"])
        self.tearDown(); self.setUp()
        x = self.w.collector(START + dt.timedelta(hours=2, minutes=13), native=False, root="1:external", persist=False,
                             slot=iso(START + dt.timedelta(hours=2, minutes=7)))
        doc = self.w.measure()                                         # 2.26 exempted it for its title
        self.assertEqual(doc["execution"]["executed_without_stored_output"], [x["id"]])
        self.assertEqual(doc["verdict"], "fail")

    def test_jobs_missing_for_an_unrecorded_run_is_insufficient(self):
        r = self.w.run("collect.yml", START + dt.timedelta(hours=2, minutes=8), "schedule", OWNER, conclusion="failure")
        doc = self.w.measure()
        self.assertEqual(doc["execution"]["stage_unknown"], [r["id"]])
        self.assertEqual(doc["verdict"], "insufficient")

    def test_real_proven_yield_passes_and_a_receipt_on_a_failed_record_does_not(self):
        slot = START + dt.timedelta(hours=2, minutes=7)
        cover = [r for r in self.w.records if r["t"] >= ms(slot)][0]
        x = self.w.collector(slot + dt.timedelta(minutes=8), native=False, root="1:external", persist=False, slot=iso(slot))
        rc = R.yield_receipt(slot, cover, env={"GITHUB_RUN_ID": str(x["id"]), "GITHUB_RUN_ATTEMPT": "1",
                                               "GITHUB_REF_NAME": "main"}, now=slot + dt.timedelta(minutes=9))
        self.w.write("state/recovery_yields.jsonl", [rc])
        doc = self.w.measure()
        self.assertEqual(doc["execution"]["valid_yield_receipts"], 1)
        self.assertTrue(doc["checks"]["no_lost_output"], doc["execution"])
        cover["critical_ok"] = False                                    # the covering record was not a success
        self.w.flush()
        self.assertEqual(R.valid_yield(rc, self.w.records)[1], "covering record differs from the one the receipt names")
        self.assertEqual(self.w.measure()["execution"]["executed_without_stored_output"], [x["id"]])

    def test_pre_receipt_yield_proven_by_retained_job_evidence(self):
        # real shape: run 37344766414 (Oct 5 16:57Z) - yield step success, Collect skipped, no record, no receipt
        slot = START + dt.timedelta(hours=2, minutes=7)
        cover = [r for r in self.w.records if r["t"] >= ms(slot)][0]
        x = self.w.collector(slot + dt.timedelta(minutes=8), native=False, root="1:external", persist=False, slot=iso(slot))
        done = iso(slot + dt.timedelta(minutes=9))
        self.w.jobs[str(x["id"])] = [{"id": 2, "runner_id": 7, "steps": [
            {"name": A.YIELD_STEP, "conclusion": "success", "started_at": done, "completed_at": done},
            {"name": "Collect", "conclusion": "skipped", "started_at": None, "completed_at": None}]}]
        doc = self.w.measure()
        self.assertEqual(doc["execution"]["yields_proven_by_job_evidence"], 1)
        self.assertTrue(doc["checks"]["no_lost_output"])
        cover["critical_ok"] = False                                    # 2.26's covered() accepted a failed record
        self.w.flush()
        self.assertEqual(self.w.measure()["execution"]["executed_without_stored_output"], [x["id"]])

    def test_failed_critical_records_never_cover(self):
        for r in self.w.records:
            r["critical_ok"] = False
        self.w.flush()
        doc = self.w.measure()
        self.assertEqual(doc["collection"]["intervals_with_critical_success"], 0)
        self.assertEqual(len(doc["collection"]["critical_failures"]), 96)
        self.assertEqual(doc["verdict"], "fail")
        self.assertFalse(R.covered(self.w.d, START))

    def test_optional_degradation_is_a_warning_and_racing_duplicates_count_once(self):
        for r in self.w.records[::3]:
            r["snap"] = {"books_ok": 16, "books": 17, "failed": {"kraken": "HTTP 502"}}
        self.w.collector(START + dt.timedelta(hours=1, minutes=10), native=False, root="1:external")  # a racing duplicate
        self.w.records.sort(key=lambda r: r["t"])
        self.w.flush()
        doc = self.w.measure()
        self.assertEqual(doc["collection"]["degraded_optional_records"], 32)
        self.assertEqual(doc["collection"]["intervals_with_critical_success"], 95)


# ------------------------------------------------------------------------------------------- binding (section 6)
class BindingTests(Base):
    def test_a_material_actions_change_changes_the_digest_and_the_verdict(self):
        a = self.w.measure()
        ev = self.w.evidence()
        d = [r for r in ev["runs"] if r["display_title"] == "Recovery dispatcher (external)"][0]
        d["display_title"] = "Recovery dispatcher"                     # reviewer: external -> untitled
        b = self.w.measure(ev=ev)
        self.assertNotEqual(a["inputs"]["actions"]["sha256"], b["inputs"]["actions"]["sha256"])
        self.assertEqual((a["verdict"], b["verdict"]), ("pass", "fail"))

    def test_a_material_input_change_changes_its_file_digest(self):
        a = self.w.measure()["inputs"]["files_sha256"]
        p = self.w.d / "desk/research/ps1/protocol.json"
        p.write_text(p.read_text() + " ")
        doc = self.w.measure()
        self.assertNotEqual(a["desk/research/ps1/protocol.json"], doc["inputs"]["files_sha256"]["desk/research/ps1/protocol.json"])
        self.assertFalse(doc["checks"]["ps1_evidence_valid"])

    def test_offline_replay_reproduces_the_verdict(self):
        ev = self.w.evidence()
        one = self.w.measure(ev=json.loads(json.dumps(ev)))
        two = self.w.measure(ev=json.loads(json.dumps(ev)))
        for k in ("verdict", "checks", "collection", "decisions", "inputs"):
            self.assertEqual(one[k], two[k], k)

    def test_repairs_committed_after_the_cutoff_cannot_improve_the_window(self):
        d = self.w.d
        removed = [self.w.records.pop(40) for _ in range(3)]            # three intervals empty
        self.w.flush()
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")

        def commit(when, msg):
            e = dict(env, GIT_AUTHOR_DATE=iso(when), GIT_COMMITTER_DATE=iso(when))
            subprocess.run(["git", "add", "-A"], cwd=d, env=e, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", msg], cwd=d, env=e, check=True, capture_output=True)
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        commit(END + dt.timedelta(minutes=30), "on time")
        before = self.w.measure()
        self.assertEqual(before["verdict"], "fail")
        self.w.records = sorted(self.w.records + removed, key=lambda r: r["t"])   # a later "repair"
        self.w.flush()
        commit(END + dt.timedelta(hours=5), "repair after the cutoff")
        after = self.w.measure(now=END + dt.timedelta(hours=6))
        self.assertEqual(before["collection"], after["collection"])
        self.assertEqual(after["verdict"], "fail")
        self.assertEqual(before["inputs"]["repository"]["commit"], after["inputs"]["repository"]["commit"])


# ------------------------------------------------------------------------------------------- independent review (2.27)
class ReviewFindingTests(Base):
    """Counterexamples from an independent adversarial review of acceptance-3.0.0 before release, each now refused."""

    def test_a_rerun_is_a_persons_start_whatever_its_event(self):
        ev = self.w.evidence()
        for r in ev["runs"]:
            if r["path"].endswith("collect.yml") and r["event"] == "schedule":
                r.update(run_attempt=2, triggering_actor="someone-else")
        doc = self.w.measure(ev=ev)
        self.assertEqual(doc["verdict"], "fail")
        self.assertEqual(doc["collection"]["by_initiation"].get("human"), 48)
        ev = self.w.evidence()
        for r in ev["runs"]:
            if r["display_title"] == "Recovery dispatcher (external)":
                r.update(run_attempt=2)
        self.assertEqual(self.w.measure(ev=ev)["verdict"], "fail")
        parent = {"id": 4, "run_attempt": 2, "event": "schedule", "status": "completed", "head_branch": "main",
                  "created_at": "2026-10-05T16:14:07Z", "updated_at": "2026-10-05T16:18:20Z",
                  "path": ".github/workflows/range.yml", "triggering_actor": OWNER}
        child = {"id": 5, "event": "workflow_run", "status": "completed", "head_branch": "main",
                 "created_at": "2026-10-05T16:18:23Z", "path": ".github/workflows/research-streams.yml",
                 "triggering_actor": OWNER, "display_title": "Research streams after run 4 attempt 1"}
        self.assertEqual(A.Lineage([parent, child]).classify(child)[0], "unknown")   # attempt 1's start unverifiable

    def test_records_must_belong_to_the_collector_run_they_name(self):
        rng = [r for r in self.w.runs if r["path"].endswith("range.yml")][0]
        native = [r for r in self.w.records if r["trigger"] == "schedule"]
        for r in native:
            r["run_id"] = str(rng["id"])
        self.w.flush()
        ev = self.w.evidence()
        ev["runs"] = [r for r in ev["runs"] if not (r["path"].endswith("collect.yml") and r["event"] == "schedule")]
        doc = self.w.measure(ev=ev)
        self.assertEqual(doc["verdict"], "fail")
        self.assertEqual(len(doc["collection"]["records_not_bound_to_their_run"]), 48)
        self.tearDown(); self.setUp()
        one = str(self.w.runs[0]["id"])                                  # every record names one scheduled run
        for r in self.w.records:
            r["run_id"] = one
        self.w.flush()
        self.assertEqual(self.w.measure()["verdict"], "fail")

    def test_a_receipt_written_outside_its_run_or_contradicted_by_its_jobs_is_not_a_yield(self):
        slot = START + dt.timedelta(hours=2, minutes=7)
        cover = [r for r in self.w.records if r["t"] >= ms(slot)][0]
        x = self.w.collector(slot + dt.timedelta(minutes=8), native=False, root="1:external", persist=False, slot=iso(slot))
        env = {"GITHUB_RUN_ID": str(x["id"]), "GITHUB_REF_NAME": "main"}
        late = R.yield_receipt(slot, cover, env=env, now=slot + dt.timedelta(hours=6))        # after the run ended
        self.w.write("state/recovery_yields.jsonl", [late])
        self.assertEqual(self.w.measure()["execution"]["executed_without_stored_output"], [x["id"]])
        ok = R.yield_receipt(slot, cover, env=env, now=slot + dt.timedelta(minutes=9))
        self.w.write("state/recovery_yields.jsonl", [ok])
        self.w.jobs[str(x["id"])] = [{"id": 3, "runner_id": 7, "steps": [
            {"name": A.YIELD_STEP, "conclusion": "skipped", "started_at": None},
            {"name": "Collect", "conclusion": "success", "started_at": "x", "completed_at": "x"}]}]
        self.assertEqual(self.w.measure()["execution"]["executed_without_stored_output"], [x["id"]])

    def test_decisions_are_included_by_deadline(self):
        # window [Oct 4 20:30, Oct 5 20:30): the Oct 4 20:00 decisions (deadlines 21:15 and 21:30) are inside it
        s0 = START + dt.timedelta(hours=2, minutes=30)
        rd = A.range_decisions(self.w.d, s0, s0 + dt.timedelta(hours=24))
        self.assertIn("2026-10-04T20:00:00Z", rd)
        p1 = A.ps1_evaluate(self.w.d, s0, s0 + dt.timedelta(hours=24), s0 + dt.timedelta(hours=26))
        self.assertIn("2026-10-04T20:00:00Z", p1["decisions"])

    def test_a_range_decision_published_by_a_person_does_not_count(self):
        att = [json.loads(l) for l in (self.w.d / "state/range_attempts.jsonl").read_text().splitlines()]
        rid = att[2]["run"]["run_id"]
        ev = self.w.evidence()
        for r in ev["runs"]:
            if str(r["id"]) == rid:
                r.update(event="workflow_dispatch")
        doc = self.w.measure(ev=ev)
        self.assertEqual(doc["decisions"]["range"][att[2]["decision_utc"]], "published by a run that is human")
        self.assertFalse(doc["checks"]["range_decisions_published"])

    def test_cutoff_is_bounded_and_the_code_digest_covers_storage(self):
        self.assertEqual(self.w.measure(cutoff=END + dt.timedelta(days=30))["verdict"], "invalid")
        self.assertIn("storage.py", self.w.measure()["code_sha256"])
        self.assertIn("desk/research/ps1/protocol.json", self.w.measure()["code_sha256"])

    def test_malformed_evidence_is_insufficient_not_a_crash(self):
        with open(self.w.d / "data/runs/2026-10.jsonl", "a") as f:
            f.write("{not json\n")
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "insufficient")
        self.assertIn("malformed evidence", doc["reason"])
        self.tearDown(); self.setUp()
        self.w.records[5]["provenance"] = "a string"
        self.w.flush()
        self.assertIn(self.w.measure()["verdict"], ("pass", "fail", "insufficient"))
        ev = self.w.evidence()
        del ev["runs"][3]["id"]
        self.assertEqual(self.w.measure(ev=ev)["verdict"], "insufficient")


if __name__ == "__main__":
    unittest.main()
