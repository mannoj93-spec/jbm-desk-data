"""Repo 2.27: the October 5 runner-assignment disruption and the reviewer's success/coverage counterexamples.

Execution stages from real job metadata (runner_id 0, no steps, cancelled), recovery that is neither suppressed by
dead attempts nor storming, success-only yield coverage with durable receipts, health and watchdog that keep data
freshness, activity and the 45-minute acceptance target apart, and monitors that could not execute."""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk"), str(ROOT / "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cadence                    # noqa: E402
import execution as X             # noqa: E402
import health as H                # noqa: E402
import recovery as R              # noqa: E402
import watchdog                   # noqa: E402

UTC = dt.timezone.utc
FIX = json.loads((ROOT / "regression/fixtures/actions_2026-10-05/collector_jobs.json").read_text())
Q = [7, 22, 37, 52]
MS = lambda t: int(t.timestamp() * 1000)            # noqa: E731


def t(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def gh(created, status="completed", conclusion="success", title="Collector", event="schedule"):
    return {"id": abs(hash((created, status, conclusion, title))) % 10**9, "event": event, "status": status,
            "head_branch": "main", "conclusion": conclusion if status == "completed" else None,
            "created_at": created, "updated_at": created, "display_title": title}


def rec(at, ok=True, trigger="schedule", **kw):
    r = {"t": MS(t(at)), "mode": "routine", "trigger": trigger, "runner": "github", "critical_ok": ok,
         "run_id": str(MS(t(at))), "errors": {} if ok else {"snap": "boom"}, "code_version": "test"}
    r.update(kw)
    return r


class StageTests(unittest.TestCase):
    def test_real_no_runner_job_is_never_started_not_a_persistence_loss(self):
        st = X.stages(FIX["37360591638_run"], FIX["37360591638"])
        self.assertEqual((st["runner_assigned"], st["steps_executed"], st["phase"]), (False, False, "never-started"))
        self.assertEqual(st["conclusion"], "failure")                  # the run said failure; nothing executed
        ok = X.stages(FIX["37357926760_run"], FIX["37357926760"], record=rec("2026-10-05T18:42:24Z"))
        self.assertEqual(ok["phase"], "persisted-success")

    def test_stage_facts_stay_unknown_without_evidence_and_queue_age_is_measured(self):
        run = gh("2026-10-05T19:49:29Z", status="pending")
        st = X.stages(run, None, now=t("2026-10-05T20:13:56Z"))
        self.assertEqual((st["runner_assigned"], st["steps_executed"], st["phase"]), (None, None, "queued"))
        self.assertEqual(st["queue_age_min"], 24.4)
        self.assertEqual(X.stages(gh("2026-10-05T19:00:00Z", conclusion="failure"), None)["phase"], "unknown")
        ran_nothing = [{"runner_id": 5, "steps": [{"name": "x", "conclusion": "skipped", "started_at": None}]}]
        self.assertEqual(X.stages(gh("2026-10-05T19:00:00Z", conclusion="failure"), ran_nothing)["phase"],
                         "failed-before-execution")
        self.assertEqual(X.stages(gh("2026-10-05T19:00:00Z", conclusion="failure"), FIX["37357926760"])["phase"],
                         "executed-no-output")
        self.assertEqual(X.stages(gh("2026-10-05T19:00:00Z"), FIX["37357926760"], record=rec("2026-10-05T19:02:00Z", ok=False))
                         ["phase"], "critical-failure")


class RecoveryRetryTests(unittest.TestCase):
    def plan(self, now, **runs):
        return [w for w, _, _ in R.plan(t(now), runs, minutes=Q)]

    def test_dead_native_attempts_do_not_suppress_recovery(self):
        # Oct 5: native runs were created but never received a runner (conclusion failure / cancelled)
        for dead in (gh("2026-10-05T19:03:19Z", conclusion="failure"), gh("2026-10-05T19:03:19Z", conclusion="cancelled"),
                     gh("2026-10-05T19:03:19Z", status="queued")):
            now = "2026-10-05T19:27:00Z" if dead["status"] == "queued" else "2026-10-05T19:12:00Z"
            self.assertIn("collector", self.plan(now, collector=[dead]), dead)

    def test_young_queued_or_running_attempts_suppress_duplicates(self):
        for live in (gh("2026-10-05T19:09:00Z", status="queued"), gh("2026-10-05T19:09:00Z", status="in_progress"),
                     gh("2026-10-05T19:09:00Z")):
            self.assertNotIn("collector", self.plan("2026-10-05T19:12:00Z", collector=[live]), live)

    def test_retries_are_capped_per_slot_and_range_per_decision(self):
        key = "2026-10-05T19:07:00Z"
        mine = [gh("2026-10-05T19:12:30Z", conclusion="failure", title=f"Collector recovery {key} via 1:external",
                   event="workflow_dispatch"),
                gh("2026-10-05T19:13:30Z", conclusion="failure", title=f"Collector recovery {key} via 2:external",
                   event="workflow_dispatch")]
        self.assertNotIn("collector", self.plan("2026-10-05T19:16:00Z", collector=mine))
        stuck = gh("2026-10-05T20:13:31Z", status="pending", title="Range forecasts")
        self.assertNotIn("range", self.plan("2026-10-05T20:20:00Z", range=[stuck]))      # 6.5 min: let it start
        self.assertIn("range", self.plan("2026-10-05T20:27:00Z", range=[stuck]))         # 13.5 min queued: retry
        self.assertNotIn("range", self.plan("2026-10-05T20:46:00Z", range=[stuck]))      # past the deadline: missed

    def test_streams_fall_back_when_the_range_run_is_stuck_in_the_queue(self):
        stuck = gh("2026-10-05T20:13:31Z", status="pending", title="Range forecasts")
        self.assertIn("streams", self.plan("2026-10-05T20:57:00Z", range=[stuck]))

    def test_the_planner_only_dispatches(self):
        src = (ROOT / "recovery.py").read_text()
        for verb in ("/cancel", "/rerun", "force-cancel"):
            self.assertNotIn(verb, src)


class YieldTests(unittest.TestCase):
    def test_only_a_critical_success_covers_and_the_receipt_names_it(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "data/runs"
            p.mkdir(parents=True)
            slot = t("2026-10-05T18:37:00Z")
            (p / "2026-10.jsonl").write_text(json.dumps(rec("2026-10-05T18:39:00Z", ok=False)) + "\n")
            self.assertFalse(R.covered(d, slot))                       # 2.26: True
            good = rec("2026-10-05T18:42:24Z")
            with open(p / "2026-10.jsonl", "a") as f:
                f.write(json.dumps(good) + "\n")
            self.assertEqual(R.covering(d, slot)["t"], good["t"])
            rc = R.yield_receipt(slot, good, env={"GITHUB_RUN_ID": "77", "GITHUB_REF_NAME": "main"},
                                 now=t("2026-10-05T18:45:00Z"))
            run = {"id": 77, "head_branch": "main", "display_title": f"Collector recovery {R.iso(slot)} via 1:external"}
            self.assertEqual(R.valid_yield(rc, [good], run), (True, "verified"))
            self.assertFalse(R.valid_yield(rc, [good], dict(run, id=78))[0])
            self.assertFalse(R.valid_yield(rc, [good], dict(run, head_branch=None))[0])
            self.assertFalse(R.valid_yield(dict(rc, checked_utc="2026-10-05T18:40:00Z"), [good], run)[0])
            self.assertFalse(R.valid_yield({"schema": "x"}, [good], run)[0])

    def test_the_collector_workflow_records_and_persists_the_receipt(self):
        text = (ROOT / ".github/workflows/collect.yml").read_text()
        self.assertIn('python recovery.py covered --slot "$DESK_DISPATCH_SLOT" --receipt', text)
        self.assertIn("run: bash scripts/commit_push.sh state/recovery_yields.jsonl", text)
        writers = json.loads((ROOT / "scripts/writers.json").read_text())
        self.assertIn("state/recovery_yields.jsonl", writers["writers"]["collector"]["allow"])


class SharedSuccessTests(unittest.TestCase):
    def test_one_definition_used_by_coverage(self):
        self.assertTrue(cadence.critical_success(rec("2026-10-05T18:00:00Z")))
        self.assertFalse(cadence.critical_success(rec("2026-10-05T18:00:00Z", ok=False)))
        self.assertFalse(cadence.critical_success({"t": 1, "mode": "routine"}))           # unstated is not success
        self.assertTrue(cadence.critical_success(rec("2026-10-05T18:00:00Z", snap={"books_ok": 16, "books": 17,
                                                                                  "failed": {"kraken": "502"}})))
        runs = [rec(f"2026-10-05T{h:02d}:{m:02d}:00Z", ok=False) for h in range(18, 20) for m in (8, 23, 38, 53)]
        cov = cadence.coverage([(0, Q, "")], runs, MS(t("2026-10-05T18:07:00Z")), MS(t("2026-10-05T20:07:00Z")))
        self.assertEqual(cov["intervals_with_automated_run"], cov["intervals"])           # activity: all
        self.assertEqual(cov["intervals_with_successful_automated_run"], 0)               # success: none (2.26: all)
        self.assertEqual(cov["automated_critical_failures"], 8)


class HealthAndWatchdogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "data/runs").mkdir(parents=True)
        (self.d / "cadence.json").write_text(json.dumps({"periods": [{"from": "2026-09-23T16:06:13Z", "minutes": Q}]}))

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, *rows):
        with open(self.d / "data/runs/2026-10.jsonl", "a") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")

    def test_fresh_failure_is_failing_and_stale_data_is_not_made_fresh_by_activity(self):
        self.put(rec("2026-10-05T18:27:35Z"), rec("2026-10-05T18:42:24Z", ok=False))
        s = H.source(self.d, MS(t("2026-10-05T18:50:00Z")), 90)["service"]
        self.assertEqual((s["state"], s["data_state"], s["last_activity_result"]), ("failing", "fresh", "critical failure"))
        self.assertEqual(s["last_success_utc"], "2026-10-05T18:27:35Z")
        self.put(rec("2026-10-05T19:59:00Z", ok=False))
        s = H.source(self.d, MS(t("2026-10-05T20:00:00Z")), 90)["service"]
        self.assertEqual((s["state"], s["data_state"]), ("stale", "stale"))              # activity 1 min ago
        self.assertTrue(s["acceptance_target"]["breached_now"])
        self.assertEqual(s["acceptance_target"]["max_gap_min"], 45)

    def test_acceptance_target_is_reported_apart_from_the_watchdog_limit(self):
        self.put(rec("2026-10-05T18:42:24Z"))
        at = MS(t("2026-10-05T19:40:00Z"))                              # 57.6 min: inside 90, past 45
        s = H.source(self.d, at, 90)["service"]
        self.assertEqual((s["state"], s["acceptance_target"]["breached_now"]), ("healthy", True))
        code, msg = watchdog.check(self.d, at)[:2]
        self.assertEqual(code, 0)
        self.assertTrue(any("45-minute restoration acceptance target is breached" in w
                            for w in watchdog.check(self.d, at).warnings))
        code, msg = watchdog.check(self.d, MS(t("2026-10-05T20:13:56Z")))[:2]
        self.assertEqual(code, 1)
        self.assertIn("may not have executed (no runner)", msg)

    def test_stale_report_is_not_called_scheduler_silence(self):
        doc = H.evaluate(self.d, now_ms=MS(t("2026-10-05T20:00:00Z")), stale_min=90)
        self.assertNotIn("has been silent", doc["freshness_rule"])
        self.assertIn("may not have executed (no runner)", doc["freshness_rule"])

    def test_monitor_that_never_received_a_runner_could_not_execute(self):
        class Resp:
            def __init__(self, body):
                self.body = body

            def read(self):
                return self.body

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        def opener(req, timeout=None):
            u = req.full_url
            if "/jobs" in u:
                jobs = FIX["37364503243"] if "/runs/2/" in u else FIX["37357926760"]
                return Resp(json.dumps({"jobs": jobs}).encode())
            rid = 2 if "watchdog" in u else 3
            return Resp(json.dumps({"workflow_runs": [{"id": rid, "status": "completed", "conclusion": "failure",
                                                       "created_at": "2026-10-05T19:57:31Z",
                                                       "updated_at": "2026-10-05T20:12:33Z"}]}).encode())
        m = H.monitors(t("2026-10-05T20:15:00Z"), "tok", "o/r", opener)
        self.assertEqual(m["workflows"]["watchdog.yml"]["last_executed"], False)
        self.assertEqual(m["workflows"]["watchdog.yml"]["last_execution"], "no runner")
        # 2.28: the other run's jobs (a collector job standing in) ran setup steps but no range check step; 2.27 called
        # that "check executed" and a detection (review counterexample 5) - it detected nothing
        self.assertEqual(m["workflows"]["range-monitor.yml"]["last_check"], "failed before checking")
        self.assertEqual(m["could_not_execute"], ["range-monitor.yml", "watchdog.yml"])
        self.assertEqual(m["problems_detected_by"], [])

    def test_unknown_ps1_action_is_an_invalid_problem_state(self):
        base = self.d
        (base / "streams/ps1").mkdir(parents=True)
        (base / "streams/ps1/launch.json").write_text(json.dumps({"first_decision_utc": "2026-10-05T16:00:00Z",
                                                                   "protocol_sha256": "k"}))
        (base / "streams/ps1/decisions.jsonl").write_text(json.dumps({"decision_id": "ps1-20261005T1600Z",
                                                                      "action": "corrupt"}) + "\n")
        states, _ = H.ps1_decisions(base, t("2026-10-05T18:00:00Z"))
        self.assertTrue(states["2026-10-05T16:00:00Z"].startswith("invalid: unrecognized action"))
        inc = H.incidents({"source": {"gaps": []}, "decisions": {"range": {}, "ps1": states}})
        self.assertEqual(len(inc), 1)


if __name__ == "__main__":
    unittest.main()
