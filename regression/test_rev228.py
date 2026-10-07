"""Repo 2.28: monitor check-step evidence and external-timer arrivals.

- A monitor run whose setup ran but whose check never ran (checkout failed, check skipped) did NOT execute its check;
  2.27 read any executed step as "check executed" (independent review counterexample 5).
- A failed check step detects a problem only when the job carries a finding annotation; an exit-code annotation alone
  is "check failed" (a crash cannot be excluded).
- External-timer arrivals (the designated primary trigger) are reported apart from the native dispatcher and service
  health, on the REAL dispatcher runs of 2026-10-06/07 (regression/fixtures/actions_2026-10-07): the 15:12 and 16:57
  opportunities had no arrival while the native dispatcher stayed fresh.
"""
import datetime as dt
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import execution as X   # noqa: E402
import health as H      # noqa: E402

UTC = dt.timezone.utc
FIX = ROOT / "regression/fixtures/actions_2026-10-07/recovery_runs.json"
CHECK = H.CHECK_STEPS["range-monitor.yml"]


def step(name, conclusion, started=True, status="completed"):
    return {"name": name, "status": status, "conclusion": conclusion,
            "started_at": "2026-10-07T12:00:00Z" if started else None,
            "completed_at": "2026-10-07T12:00:05Z" if started else None}


def job(*steps, runner=7):
    return [{"id": 99, "runner_id": runner, "status": "completed", "steps": list(steps)}]


class CheckOutcomeTests(unittest.TestCase):
    def test_review_counterexample_setup_ok_checkout_failed_check_skipped(self):
        jobs = job(step("Set up job", "success"), step("Check out", "failure"),
                   step(CHECK, "skipped", started=False), step("Complete job", "success"))
        self.assertTrue(X.steps_executed(jobs))                       # what 2.27 read as "check executed"
        self.assertEqual(X.check_outcome(jobs, CHECK), ("failed before checking", False))

    def test_outcome_table(self):
        ok = step("Set up job", "success")
        cases = [
            (job(ok, step(CHECK, "success")), None, ("passed", True)),
            (job(ok, step(CHECK, "failure")), ["Decision 2026-10-07T12:00Z missed"], ("found a problem", True)),
            (job(ok, step(CHECK, "failure")), ["Process completed with exit code 1."], ("check failed", True)),
            (job(ok, step(CHECK, "failure")), None, ("check failed", True)),
            (job(ok, step(CHECK, "skipped", started=False)), None, ("check skipped", False)),
            (job(ok, step(CHECK, None, status="in_progress")), None, ("running", True)),
            (job(ok), None, ("failed before checking", False)),           # job ended before the step existed
            ([{"id": 1, "runner_id": 0, "steps": []}], None, ("no runner", False)),
            (None, None, ("unknown", None)),
        ]
        for jobs, notes, want in cases:
            self.assertEqual(X.check_outcome(jobs, CHECK, notes), want, (jobs, notes))


class Resp:
    def __init__(self, body):
        self.body = json.dumps(body).encode()

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class MonitorExecutionTests(unittest.TestCase):
    def opener(self, jobs, annotations):
        def op(req, timeout=None):
            u = req.full_url
            if "/annotations" in u:
                return Resp(annotations)
            if "/jobs" in u:
                return Resp({"jobs": jobs})
            if "recovery.yml" in u:
                return Resp({"workflow_runs": []})
            return Resp({"workflow_runs": [{"id": 5, "status": "completed", "conclusion": "failure",
                                            "created_at": "2026-10-07T12:00:00Z", "updated_at": "2026-10-07T12:01:00Z"}]})
        return op

    def test_skipped_check_detects_nothing(self):
        jobs = job(step("Set up job", "success"), step("Check out", "failure"), step(CHECK, "skipped", started=False))
        e = H.execution(5, "tok", "o/r", self.opener(jobs, []), "range-monitor.yml")
        self.assertEqual((e["last_executed"], e["last_check"]), (False, "failed before checking"))
        m = H.monitors(dt.datetime(2026, 10, 7, 12, 5, tzinfo=UTC), "tok", "o/r", self.opener(jobs, []))
        self.assertEqual(m["problems_detected_by"], [])
        self.assertIn("range-monitor.yml", m["could_not_execute"])

    def test_finding_annotation_is_a_detection_exit_code_is_not(self):
        jobs = job(step("Set up job", "success"), step(CHECK, "failure"))
        found = [{"annotation_level": "failure", "message": "Range decision 2026-10-07T08:00Z: no confirmation row"},
                 {"annotation_level": "failure", "message": "Process completed with exit code 1."}]
        e = H.execution(5, "tok", "o/r", self.opener(jobs, found), "range-monitor.yml")
        self.assertEqual((e["last_executed"], e["last_check"]), (True, "found a problem"))
        self.assertIn("no confirmation row", e["last_execution"])
        crash = [{"annotation_level": "failure", "message": "Process completed with exit code 1."}]
        e = H.execution(5, "tok", "o/r", self.opener(jobs, crash), "range-monitor.yml")
        self.assertEqual((e["last_executed"], e["last_check"]), (True, "check failed"))
        m = H.monitors(dt.datetime(2026, 10, 7, 12, 5, tzinfo=UTC), "tok", "o/r", self.opener(jobs, crash))
        self.assertEqual(m["problems_detected_by"], [])


class ExternalTimerTests(unittest.TestCase):
    RUNS = json.loads(FIX.read_text())
    NOW = dt.datetime(2026, 10, 7, 19, 30, tzinfo=UTC)

    def test_real_oct7_absences_with_a_healthy_native_dispatcher(self):
        ext = [r for r in self.RUNS if r["event"] == "workflow_dispatch"]
        t = H.external_timer(ext, self.NOW)
        self.assertEqual(t["absent"], ["2026-10-07T15:12:00Z", "2026-10-07T16:57:00Z"])
        self.assertEqual((t["opportunities"], t["on_time"], t["delayed"]), (96, 94, []))
        self.assertEqual(t["on_time_max_lag_s"], 66)                   # 16:13:06 for the 16:12 opportunity
        self.assertEqual(t["state"], "gaps")
        native = [r for r in self.RUNS if r["event"] == "schedule"]
        self.assertEqual(H.heartbeat(native, self.NOW, H.DISPATCHER[1])[0]["state"], "fresh")

    def test_missing_external_is_visible_while_native_and_service_are_healthy(self):
        def op(req, timeout=None):
            u = req.full_url
            if "recovery.yml" in u and "event=workflow_dispatch" in u:
                return Resp({"workflow_runs": [r for r in self.RUNS if r["event"] == "workflow_dispatch"]})
            if "recovery.yml" in u:
                return Resp({"workflow_runs": self.RUNS[:30]})
            return Resp({"workflow_runs": [{"id": 5, "status": "completed", "conclusion": "success",
                                            "created_at": "2026-10-07T19:00:00Z", "updated_at": "2026-10-07T19:01:00Z"}]})
        m = H.monitors(self.NOW, "tok", "o/r", op)
        self.assertEqual(m["workflows"]["recovery.yml"]["native"]["state"], "fresh")
        self.assertEqual(m["external_timer"]["absent"], ["2026-10-07T15:12:00Z", "2026-10-07T16:57:00Z"])
        self.assertEqual(m["external_timer"]["state"], "gaps")

    def test_silent_timer_and_arrivals_only_rule(self):
        t = H.external_timer([], self.NOW)
        self.assertEqual((t["state"], t["on_time"], len(t["absent"])), ("silent", 0, 96))
        self.assertIn("provider's execution history", t["rule"])
        late = [{"event": "workflow_dispatch", "display_title": "Recovery dispatcher (external)",
                 "created_at": "2026-10-07T18:14:00Z"}]
        t = H.external_timer(late, self.NOW, hours=2)
        self.assertEqual(t["delayed"], [{"slot": "2026-10-07T18:12:00Z", "lag_s": 120}])
        manual = [dict(late[0], display_title="Recovery dispatcher")]   # a native-titled dispatch is not the timer
        self.assertEqual(H.external_timer(manual, self.NOW, hours=2)["delayed"], [])


class FeasibilityWarmupTests(unittest.TestCase):
    def test_threshold_counts_usable_records_not_raw_acquisition(self):
        import feasibility as F
        r = ["1347 option records (859 with a trailing z-score); the design needs 1344"]
        self.assertEqual(F.warmup_counts(r), (859.0, 1344.0, "option records with a trailing z-score", 1347.0))
        r = ["1291 snapshot transitions for the fixed cohort; the design needs 1344"]
        self.assertEqual(F.warmup_counts(r), (1291.0, 1344.0, "snapshot transitions for the fixed cohort", None))
        self.assertIsNone(F.warmup_counts(["streaming service not deployed"]))


if __name__ == "__main__":
    unittest.main()
