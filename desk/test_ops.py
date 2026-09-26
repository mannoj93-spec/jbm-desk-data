#!/usr/bin/env python3
"""Operational tests (crypto-desk 12.2, repo 2.17): the run lifecycle log, status outcomes for failures before
forecasting, the range-stream monitor, hourly maturity scoring, and the release version parser.
Classes that need the repository (schema.py, scoring.py, the fixture) skip in the skill folder.
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_ops.py
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
sys.path[:0] = [str(DESK), str(DESK.parent)]

import range_ops as OPS            # noqa: E402

try:
    import range_reader as RR      # noqa: E402
    import range_monitor as MON    # noqa: E402
    import schema                  # noqa: E402,F401
    from test_asof import Repo, IDS4, IDS8, MS, FX   # noqa: E402
    REPO = FX.exists()
except ImportError:
    REPO = False

UTC = dt.timezone.utc
T = lambda h, m=0, s=0, d=26: dt.datetime(2026, 9, d, h, m, s, tzinfo=UTC)   # noqa: E731
ENV = lambda rid, ev="schedule": {"run_id": rid, "code_commit": "abc", "event": ev}  # noqa: E731


class TestLifecycleLog(unittest.TestCase):
    """Runs in the skill folder too: the lifecycle log is stdlib only."""

    def setUp(self):
        self.base = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_preflight_failure_is_terminal_and_explained(self):
        OPS.start(self.base, now=T(12, 2), env=ENV("r1"))
        log = "....\nFAIL: test_read_and_replay (__main__.TestLiveRecords.test_read_and_replay)\nRan 17 tests\n"
        OPS.record(self.base, {"preflight": "failure"}, now=T(12, 3), env=ENV("r1"), reason=OPS.failure_reason(log))
        OPS.record(self.base, {"refit": "skipped", "forecast": "skipped"}, now=T(12, 3), env=ENV("r1"))
        OPS.record(self.base, {"publish": "success", "confirm": "skipped"}, now=T(12, 4), env=ENV("r1"))
        end = OPS.finish(self.base, now=T(12, 4), env=ENV("r1"))
        self.assertEqual((end["decision_utc"], end["outcome"]), ("2026-09-26T12:00:00Z", "failed"))
        self.assertIn("preflight failure: FAIL: test_read_and_replay", end["reason"])
        v = OPS.decision_view(OPS.rows(self.base)[0], "2026-09-26T12:00:00Z")
        self.assertEqual(v["state"], "failed")

    def test_running_published_retry_and_malformed_rows(self):
        OPS.start(self.base, now=T(8, 2), env=ENV("a"))
        self.assertEqual(OPS.decision_view(OPS.rows(self.base)[0], "2026-09-26T08:00:00Z")["state"], "running")
        OPS.record(self.base, {"preflight": "success", "refit": "success", "forecast": "failure"}, now=T(8, 5), env=ENV("a"))
        OPS.finish(self.base, now=T(8, 6), env=ENV("a"))
        OPS.start(self.base, now=T(8, 20), env=ENV("b", "workflow_dispatch"))          # legitimate manual retry
        for st in ("preflight", "refit", "forecast", "publish", "confirm"):
            OPS.record(self.base, {st: "success"}, now=T(8, 22), env=ENV("b", "workflow_dispatch"))
        OPS.finish(self.base, now=T(8, 23), env=ENV("b", "workflow_dispatch"))
        with (self.base / OPS.RUNS).open("a") as f:
            f.write("{not json\n[1,2]\n")
        rows, bad = OPS.rows(self.base)
        self.assertEqual(bad, 2)
        v = OPS.decision_view(rows, "2026-09-26T08:00:00Z")
        self.assertEqual((v["run_id"], v["state"]), ("b", "published"))              # latest run's terminal row wins

    def test_unknown_stage_is_refused(self):
        OPS.start(self.base, now=T(8, 2), env=ENV("a"))
        with self.assertRaises(ValueError):
            OPS.record(self.base, {"deploy": "success"}, env=ENV("a"))

    def test_cli_works_without_the_forecasting_modules(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "desk").mkdir()
        shutil.copy(DESK / "range_ops.py", tmp / "desk/range_ops.py")
        (tmp / "desk/range_contract.py").write_text("this is not python(\n")         # a broken forecasting module
        env = dict(os.environ, RANGE_BASE=str(tmp), GITHUB_RUN_ID="9", GITHUB_EVENT_NAME="schedule")
        for args in (["start"], ["record", "preflight=failure"], ["finish"]):
            subprocess.run([sys.executable, str(tmp / "desk/range_ops.py")] + args, check=True, env=env,
                           capture_output=True)
        self.assertEqual(OPS.rows(tmp)[0][-1]["outcome"], "failed")
        shutil.rmtree(tmp)


@unittest.skipUnless(REPO, "needs the repository and its fixture")
class TestStatusOutcomes(unittest.TestCase):
    """Finding 3: a known failure before forecasting overrides generic in-progress/missing; no window is invented."""

    def setUp(self):
        self.r = Repo()

    def tearDown(self):
        self.r.close()

    def fail_preflight(self, decision_h, run="r12"):
        OPS.start(self.r.base, now=T(decision_h, 2), env=ENV(run))
        OPS.record(self.r.base, {"preflight": "failure"}, now=T(decision_h, 3), env=ENV(run), reason="FAIL: test_x")
        OPS.record(self.r.base, {"refit": "skipped", "forecast": "skipped", "publish": "success", "confirm": "skipped"},
                   now=T(decision_h, 3), env=ENV(run))
        OPS.finish(self.r.base, now=T(decision_h, 4), env=ENV(run))

    def test_current_and_due_failures(self):
        st = RR.status(self.r.base, T(12, 1))
        self.assertEqual(st["current_decision"]["outcome"], "not-started")
        OPS.start(self.r.base, now=T(12, 2), env=ENV("r12"))
        self.assertEqual(RR.status(self.r.base, T(12, 2, 30))["current_decision"]["outcome"], "running")
        self.fail_preflight(12)
        cur = RR.status(self.r.base, T(12, 10))["current_decision"]
        self.assertEqual(cur["outcome"], "failed")
        self.assertIn("preflight failure: FAIL: test_x", cur["reason"])
        due = {r["decision_utc"]: r for r in RR.status(self.r.base, T(13, 30))["recent"]}
        self.assertEqual(due["2026-09-26T12:00:00Z"]["outcome"], "failed")         # not "missing" after grace
        self.assertEqual(due["2026-09-26T12:00:00Z"]["ids"], [])                   # no forecast, no window
        self.assertNotIn("range-rc1d-4h-20260926T1200Z", json.loads((self.r.base / "state/forecast_manifest.json").read_text()))

    def test_missing_run_and_started_without_terminal(self):
        due = {r["decision_utc"]: r for r in RR.status(self.r.base, T(13, 30))["recent"]}
        self.assertEqual(due["2026-09-26T12:00:00Z"]["outcome"], "missing")
        OPS.start(self.r.base, now=T(12, 2), env=ENV("killed"))
        due = {r["decision_utc"]: r for r in RR.status(self.r.base, T(13, 30))["recent"]}
        self.assertEqual(due["2026-09-26T12:00:00Z"]["outcome"], "failed")
        self.assertIn("recorded no terminal outcome", due["2026-09-26T12:00:00Z"]["reason"])

    def test_status_expiry_is_explicit(self):
        st = RR.status(self.r.base, T(9))
        self.assertEqual(st["generated_utc"], "2026-09-26T09:00:00Z")
        self.assertEqual(st["status_expires_utc"], "2026-09-26T12:25:00Z")       # 08:00Z 4h valid until 12:25
        self.assertIn("own clock", st["freshness_rule"])
        self.assertIn("Expires 2026-09-26T12:25:00Z", RR.markdown(st))


@unittest.skipUnless(REPO, "needs the repository and its fixture")
class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.r = Repo()
        (self.r.base / "desk").mkdir()
        (self.r.base / "desk/release.json").write_text(json.dumps({"range_stream_start_utc": "2026-09-26T04:00:00Z"}))
        (self.r.base / "reports").mkdir()

    def tearDown(self):
        self.r.close()

    def status_at(self, t):
        (self.r.base / "reports/range_status.json").write_text(json.dumps(RR.status(self.r.base, t)))

    def test_healthy_then_failures(self):
        self.status_at(T(9, 30))
        problems, info = MON.check(self.r.base, T(9, 40))
        self.assertEqual(problems, [], problems)
        self.status_at(T(13, 20))
        problems, _ = MON.check(self.r.base, T(13, 30))
        self.assertTrue(any("2026-09-26T12:00:00Z: no attempt and no run record" in p for p in problems), problems)
        self.assertTrue(any(p.startswith("scoring: ") and "4h" in p for p in problems), problems)   # 04:00Z 4h matured 08:25
        OPS.start(self.r.base, now=T(12, 2), env=ENV("r12"))
        OPS.record(self.r.base, {"preflight": "failure"}, now=T(12, 3), env=ENV("r12"), reason="FAIL: test_x")
        OPS.finish(self.r.base, now=T(12, 4), env=ENV("r12"))
        problems, _ = MON.check(self.r.base, T(13, 30))
        self.assertTrue(any("run r12 produced no attempt (preflight failure: FAIL: test_x)" in p for p in problems), problems)

    def test_stale_status_publication_and_unrecorded_actions(self):
        self.status_at(T(9, 30))
        problems, _ = MON.check(self.r.base, T(19))
        self.assertTrue(any(p.startswith("freshness:") for p in problems))
        self.assertTrue(any(p.startswith("publication:") for p in problems))
        runs = [{"run_id": "555", "event": "schedule", "created_utc": "2026-09-26T16:02:00Z", "conclusion": "failure"},
                {"run_id": "36229141684", "event": "schedule", "created_utc": "x", "conclusion": "failure"}]
        problems, _ = MON.check(self.r.base, T(9, 40), runs)
        self.assertEqual([p for p in problems if p.startswith("actions:")],
                         ["actions: range.yml run 555 (2026-09-26T16:02:00Z) concluded failure with no record in the repository"])

    def test_monitor_runs_when_forecasting_code_is_broken(self):
        tmp = self.r.base
        shutil.copy(DESK / "range_monitor.py", tmp / "desk/range_monitor.py")
        (tmp / "desk/range_contract.py").write_text("broken(\n")
        (tmp / "desk/range_reader.py").write_text("broken(\n")
        self.status_at(T(13, 20))
        p = subprocess.run([sys.executable, str(tmp / "desk/range_monitor.py")], env=dict(os.environ, RANGE_BASE=str(tmp),
                           GITHUB_TOKEN=""), capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)                               # problems found (real clock), not a crash
        self.assertIn("::error::", p.stdout)
        self.assertNotIn("Traceback", p.stderr)


@unittest.skipUnless(REPO, "needs the repository and its fixture")
class TestHourlyScoring(unittest.TestCase):
    """Finding 4: maturity scoring independent of forecast generation; per-horizon states; idempotent; recovers."""

    def setUp(self):
        self.r = Repo()
        (self.r.base / "reports").mkdir()
        import range_job as J
        self.J = J
        self.calls = []

    def tearDown(self):
        self.r.close()

    def fetch(self, n_missing=0):
        def f(s, e):
            self.calls.append((s, e))
            bars = [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]
            if n_missing:
                import scoring
                return scoring.check_bars(bars[:-n_missing], s, e)          # raises Unscorable: incomplete coverage
            return bars
        return f

    def test_maturity_boundary_backlog_and_idempotency(self):
        end4 = RR._t(self.r.doc(IDS4[0])["horizon_utc"])                   # 08:20
        new, pending, _ = self.J.score(self.r.base, end4 + dt.timedelta(minutes=5) - dt.timedelta(seconds=1), fetch=self.fetch())
        self.assertEqual((len(new), self.calls), (0, []))
        st = RR.status(self.r.base, end4 + dt.timedelta(minutes=5))
        self.assertEqual(st["scoring"]["4h"]["ready"], 1)                          # mature 4h shown ...
        self.assertEqual(st["scoring"]["72h"]["waiting-maturity"], 2)               # ... beside unfinished 72h
        new, _, _ = self.J.score(self.r.base, end4 + dt.timedelta(minutes=5), fetch=self.fetch())
        self.assertEqual([x["id"] for x in new], [IDS4[0]])
        self.assertEqual(len(self.calls[0]) and (self.calls[0][1] - self.calls[0][0]) // 60_000, 240)
        rec = new[0]
        self.assertEqual((rec["status"], rec["events"][0]["loss_basis"]), ("scored", "point (desk/range_contract.py)"))
        self.assertTrue((self.r.base / rec["evidence"]).exists())
        again, _, _ = self.J.score(self.r.base, end4 + dt.timedelta(minutes=30), fetch=self.fetch())
        self.assertEqual(again, [])                                                  # idempotent by id and hash
        st = json.loads((self.r.base / "reports/range_status.json").read_text())
        self.assertEqual(st["scoring"]["4h"]["scored"], 1)

    def test_incomplete_coverage_waits_then_recovers(self):
        t = T(8, 30)
        new, pending, alerts = self.J.score(self.r.base, t, fetch=self.fetch(n_missing=1))
        self.assertEqual((new, pending), ([], 6))                  # 4h unscorable + five windows not yet mature
        self.assertTrue(any("incomplete price coverage: 239/240" in a for a in alerts), alerts)
        st = RR.status(self.r.base, t)
        self.assertEqual(st["scoring"]["4h"]["waiting-observations"], 1)
        self.assertIsNone(json.loads((self.r.base / "registry/scores.jsonl").read_text() or "null")
                          if (self.r.base / "registry/scores.jsonl").exists() else None)   # no loss fabricated
        new, _, _ = self.J.score(self.r.base, T(9, 30), fetch=self.fetch())
        self.assertEqual([x["id"] for x in new], [IDS4[0]])
        log = [json.loads(x) for x in (self.r.base / "state/range_scoring.jsonl").read_text().splitlines()]
        self.assertEqual([x["outcome"] for x in log], ["unscorable", "scored"])

    def test_scoring_while_forecasting_fails(self):
        OPS.start(self.r.base, now=T(12, 2), env=ENV("r12"))
        OPS.record(self.r.base, {"preflight": "failure"}, now=T(12, 3), env=ENV("r12"), reason="FAIL")
        OPS.finish(self.r.base, now=T(12, 4), env=ENV("r12"))
        new, _, _ = self.J.score(self.r.base, T(13), fetch=self.fetch())
        self.assertEqual(sorted(x["id"] for x in new), sorted([IDS4[0], IDS8[0]]))   # both matured 4h windows

    def test_other_streams_are_left_to_the_weekly_report(self):
        import scoring
        attempts = []
        scoring.score_registry(self.r.base, MS(T(13)), "t", fetch=self.fetch(), only_prefix="range-b2-", attempts=attempts)
        self.assertEqual(attempts, [])


class TestVersionParser(unittest.TestCase):
    def test_inline_comment_does_not_leak(self):
        import make_release as M
        tmp = Path(tempfile.mkdtemp())
        (tmp / "m.py").write_text('X = 1\nVERSION = "contract-9.9.9"            # this module\'s version\n')
        self.assertEqual(M._version(tmp / "m.py"), "contract-9.9.9")
        (tmp / "j.py").write_text("JOB_VERSION = 'range-job-1.0.0'  # c\n")
        self.assertEqual(M._version(tmp / "j.py"), "range-job-1.0.0")
        (tmp / "n.py").write_text('"""VERSION = "doc-string"""\nOTHER = 2\n')
        self.assertIsNone(M._version(tmp / "n.py"))
        for mod in ("range_contract.py", "range_reader.py", "range_ops.py"):
            v = M._version(DESK / mod)
            self.assertRegex(v, r"^[a-z-]+-\d+\.\d+\.\d+$", mod)
        shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=1)
