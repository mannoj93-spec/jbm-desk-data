#!/usr/bin/env python3
"""Operational tests (crypto-desk 12.3, repo 2.18): the run lifecycle log, status outcomes for failures before
forecasting, the range-stream monitor (12.3: current-availability policy, incident lifetime, sparse inputs), hourly
maturity scoring, scoring from explicit initial states (12.3), and the release version parser.
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
        self.assertEqual(st["generated_utc"], "2026-09-26T09:00:00.000Z")          # milliseconds since 12.3
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
                {"run_id": "36229141684", "event": "schedule", "created_utc": "2026-09-26T08:14:00Z", "conclusion": "failure"}]
        problems, _ = MON.check(self.r.base, T(9, 40), runs)
        self.assertEqual([p for p in problems if p.startswith("actions:")],
                         ["actions: range.yml run 555 (2026-09-26T16:02:00Z) concluded failure with no record in the repository"
                          " (no later scheduled run has succeeded)"])

    def test_failure_recorded_in_the_deployment_log_is_acknowledged(self):
        # Sep 26: run 36241307098 failed before the run log existed; every monitor run then failed on it (12.2.1).
        self.status_at(T(9, 30))
        run = [{"run_id": "36241307098", "event": "schedule", "created_utc": "2026-09-26T12:14:41Z", "conclusion": "failure"},
               {"run_id": "36254628462", "event": "schedule", "created_utc": "2026-09-26T16:14:02Z", "conclusion": "success"}]
        problems, _ = MON.check(self.r.base, T(9, 40), run)
        self.assertEqual(len([p for p in problems if p.startswith("actions:")]), 1)          # unrecorded: alarm
        (self.r.base / "desk/deployments.jsonl").write_text(json.dumps(
            {"revision": "2.16", "event": "scheduled run failed before forecasting", "run_id": "36241307098",
             "decision_utc": "2026-09-26T12:00:00Z"}) + "\n")
        problems, info = MON.check(self.r.base, T(9, 40), run)
        self.assertEqual([p for p in problems if p.startswith("actions:")], [])              # recorded: acknowledged
        self.assertEqual(info["acknowledged_runs"], ["36241307098"])
        problems, _ = MON.check(self.r.base, T(13, 30), run[:1])
        self.assertTrue(any("run 36241307098 failed before forecasting" in p for p in problems), problems)
        run.append({"run_id": "999", "event": "schedule", "created_utc": "2026-09-26T20:14:00Z", "conclusion": "failure"})
        problems, _ = MON.check(self.r.base, T(9, 40), run)
        self.assertEqual(len([p for p in problems if p.startswith("actions:")]), 1)          # a new one still alarms
        self.assertIn("run 999", [p for p in problems if p.startswith("actions:")][0])

    # 12.3 (repo 2.18): current-availability policy on the monitor's clock, and Actions incident lifetime.
    def corrupt_latest(self, fid):
        m = self.r.manifest()
        path = self.r.base / m[fid]["frozen"]
        path.write_bytes(path.read_bytes().replace(b'"reference_price":', b'"reference_price":1', 1))

    def test_integrity_failed_current_alerts_despite_publications(self):
        # Reproduction (Sep 28): corrupting the latest 4h frozen file made status integrity-failed; 12.2.1's check()
        # returned no problems because publications, runs and freshness were all fine.
        self.corrupt_latest(IDS8[0])
        self.status_at(T(9, 30))
        st = json.loads((self.r.base / "reports/range_status.json").read_text())
        self.assertEqual(st["current"]["4h"]["state"], "integrity-failed")
        self.assertEqual(len(self.r.pubs()), 2)                           # both publications eligible
        problems, info = MON.check(self.r.base, T(9, 40))
        self.assertEqual([p for p in problems if p.startswith("current: 4h integrity-failed")].__len__(), 1, problems)
        self.assertEqual(info["current_states"]["4h"], "integrity-failed")
        problems, _ = MON.check(self.r.base, T(8, 30))                   # no grace for integrity, even in the run window
        self.assertTrue(any(p.startswith("current: 4h integrity-failed") for p in problems), problems)

    def test_expired_cached_status_cannot_imply_health(self):
        self.status_at(T(9, 30))
        st = json.loads((self.r.base / "reports/range_status.json").read_text())
        self.assertEqual({c["state"] for c in st["current"].values()}, {"valid-current"})
        self.assertEqual(MON.check(self.r.base, T(9, 40))[0], [])
        # Same file, read after 4h's valid_until and after status_expires_utc (13:15Z) - freshness alone passes at 11:30
        st["generated_utc"] = "2026-09-26T13:00:00.000Z"                  # a fresh-looking stamp on a stale view
        (self.r.base / "reports/range_status.json").write_text(json.dumps(st))
        problems, _ = MON.check(self.r.base, T(13, 20))
        self.assertFalse(any(p.startswith("freshness:") for p in problems))
        self.assertTrue(any(p.startswith("current: status expired") for p in problems), problems)
        self.assertTrue(any(p.startswith("current: 4h ") and "expired at" in p for p in problems), problems)

    def test_transition_is_info_persistent_is_a_problem(self):
        self.r.drop(IDS8)                                                 # the 08:00Z batch never published
        self.status_at(T(8, 30))                                          # 04:00Z batch still valid: healthy
        self.assertEqual([p for p in MON.check(self.r.base, T(8, 40))[0] if p.startswith("current:")], [])
        self.status_at(T(9, 20))                                          # 04:00Z valid until 09:15 -> stale
        st = json.loads((self.r.base / "reports/range_status.json").read_text())
        self.assertEqual(st["current"]["4h"]["state"], "stale")
        problems, _ = MON.check(self.r.base, T(9, 25))                   # outside 08:00 + 75 min: persistent
        self.assertTrue(any(p.startswith("current: 4h stale") for p in problems), problems)
        # a missing current state inside its run window is a publication transition, reported in info
        st = RR.status(self.r.base, T(9, 20))
        st["generated_utc"], st["status_expires_utc"] = "2026-09-26T12:10:00.000Z", "2026-09-26T16:00:00Z"
        st["current"]["4h"] = {"state": "missing", "id": None, "reason": "no forecast available"}
        (self.r.base / "reports/range_status.json").write_text(json.dumps(st))
        problems, info = MON.check(self.r.base, T(12, 20))
        self.assertFalse(any(p.startswith("current: 4h") for p in problems), problems)
        self.assertEqual(info["current_transition"]["4h"], "missing")
        problems, _ = MON.check(self.r.base, T(13, 20))                  # same file past 12:00 + 75 min
        self.assertTrue(any(p.startswith("current: 4h missing") for p in problems), problems)

    def test_incident_lifetime(self):
        self.status_at(T(9, 30))
        sched = lambda rid, t, c: {"run_id": rid, "event": "schedule", "created_utc": t, "conclusion": c}  # noqa: E731
        old = sched("111", "2026-09-25T12:14:00Z", "failure")             # unrecorded, 21 h before the check
        ok = [sched("112", "2026-09-25T16:14:00Z", "success"), sched("113", "2026-09-26T08:14:00Z", "success")]
        problems, info = MON.check(self.r.base, T(9, 40), [old] + ok)
        self.assertEqual([p for p in problems if p.startswith("actions:")], [])   # resolved and out of window
        self.assertEqual(info["historical_failures"], ["111"])                    # evidence kept
        # out of window but never recovered: an ongoing outage stays active
        problems, _ = MON.check(self.r.base, T(9, 40), [old])
        self.assertTrue(any("run 111" in p and "no later scheduled run has succeeded" in p for p in problems), problems)
        # recent unknown failure alerts even with a later success
        recent = sched("114", "2026-09-26T04:14:00Z", "failure")
        problems, _ = MON.check(self.r.base, T(9, 40), [recent] + ok)
        self.assertEqual([p for p in problems if p.startswith("actions:")],
                         ["actions: range.yml run 114 (2026-09-26T04:14:00Z) concluded failure with no record in the repository"])
        # acknowledgment never hides an ongoing outage: an acknowledged failure that is the latest run alarms
        (self.r.base / "desk/deployments.jsonl").write_text(json.dumps({"run_id": "115"}) + "\n")
        latest = sched("115", "2026-09-26T09:14:00Z", "failure")
        problems, info = MON.check(self.r.base, T(9, 40), ok + [latest])
        self.assertEqual(info["acknowledged_runs"], ["115"])
        self.assertTrue(any("latest scheduled range.yml run 115" in p for p in problems), problems)
        # the legacy Sep 26 incident: acknowledged and recovered, so neither an alarm nor lost
        (self.r.base / "desk/deployments.jsonl").write_text(json.dumps({"run_id": "36241307098"}) + "\n")
        legacy = sched("36241307098", "2026-09-26T12:14:41Z", "failure")
        later = sched("36361801280", "2026-09-28T00:14:00Z", "success")
        problems, info = MON.check(self.r.base, T(9, 40), [legacy, later])
        self.assertEqual(([p for p in problems if p.startswith("actions:")], info["acknowledged_runs"]),
                         ([], ["36241307098"]))

    def test_sparse_checkout_covers_every_input(self):
        wf = (DESK.parent / ".github/workflows/range-monitor.yml").read_text()
        block = wf.split("sparse-checkout: |", 1)[1].split("sparse-checkout-cone-mode", 1)[0]
        paths = [x.strip() for x in block.splitlines() if x.strip()]
        self.assertIn("desk/range_monitor.py", paths)
        for need in MON.INPUTS:
            self.assertTrue(any(need == p or need.startswith(p.rstrip("/") + "/") for p in paths), need)
        src = (DESK / "range_monitor.py").read_text()
        for lit in [x.split('"')[0] for x in src.split('base / "')[1:]]:    # every path the code opens is listed
            self.assertIn(lit, MON.INPUTS)
        self.assertNotIn("import range_", src)                           # independent of the forecasting code

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
        self.assertEqual(st["scoring"]["4h"]["scoring-failed"], 1)                   # 12.4 name: a failed attempt
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


@unittest.skipUnless(REPO, "needs the repository and the fixture")
class TestScoringStates(unittest.TestCase):
    """12.3 (repo 2.18): scoring from explicit initial states on the immutable fixture, never on a copy of the growing
    production registry. Each test names its starting state; expectations check complete returned records."""

    def setUp(self):
        import scoring
        self.S, self.r = scoring, Repo()
        self.ALL = IDS4 + IDS8

    def tearDown(self):
        self.r.close()

    @staticmethod
    def fetch(s, e):
        return [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]

    def run_at(self, t):
        _, new, pending, alerts = self.S.score_registry(self.r.base, MS(t), "t", fetch=self.fetch, only_prefix="range-rc1d-")
        return new, pending, alerts

    def rows(self):
        p = self.r.base / "registry/scores.jsonl"
        return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []

    def assert_complete(self, rec):
        m = self.r.manifest()[rec["id"]]
        doc = self.r.doc(rec["id"])
        self.assertEqual(rec["status"], "scored")
        self.assertEqual(rec["forecast_sha256"], m["sha256"])
        self.assertEqual((rec["start"], rec["horizon"]), (MS(RR._t(doc["start_utc"])), MS(RR._t(doc["horizon_utc"]))))
        self.assertEqual(rec["publication"]["attempt"], m["attempt"])
        self.assertEqual({e["loss_basis"] for e in rec["events"]}, {"point (desk/range_contract.py)"})
        ev = json.loads((self.r.base / rec["evidence"]).read_text())
        self.assertEqual((self.S.digest(ev), ev["forecast_sha256"]), (rec["evidence_sha256"], rec["forecast_sha256"]))

    def assert_unique(self):
        keys = [(r["id"], r["forecast_sha256"]) for r in self.rows()]
        self.assertEqual(len(keys), len(set(keys)))

    def test_unscored_to_fully_scored(self):
        self.assertEqual(self.rows(), [])                                      # initial state: no scores
        new, pending, _ = self.run_at(T(12, 0, d=29))                          # every window matured
        self.assertEqual((sorted(x["id"] for x in new), pending), (sorted(self.ALL), 0))
        for rec in new:
            self.assert_complete(rec)
        self.assert_unique()

    def test_partial_then_remaining(self):
        new, pending, _ = self.run_at(T(8, 25))                                # 04:00Z 4h matured at 08:25
        self.assertEqual([x["id"] for x in new], [IDS4[0]])
        self.assertEqual(pending, 5)
        new, _, _ = self.run_at(T(4, 30, d=27))                                # + 08:00Z 4h and 04:00Z 24h
        self.assertEqual(sorted(x["id"] for x in new), sorted([IDS8[0], IDS4[1]]))
        before = (self.r.base / "registry/scores.jsonl").read_bytes()
        new, pending, _ = self.run_at(T(12, 0, d=29))                          # the rest, and only the rest
        self.assertEqual(sorted(x["id"] for x in new), sorted([IDS8[1], IDS4[2], IDS8[2]]))
        self.assertEqual(pending, 0)
        self.assertTrue((self.r.base / "registry/scores.jsonl").read_bytes().startswith(before))   # history kept
        for rec in self.rows():
            self.assert_complete(rec)
        self.assert_unique()

    def test_fully_scored_state_adds_nothing(self):
        """The state that broke the 2.17 preflight: all three 04:00Z horizons already scored."""
        self.run_at(T(12, 0, d=29))
        before = (self.r.base / "registry/scores.jsonl").read_bytes()
        for t in (T(12, 0, d=29), T(13, 0, d=29), T(0, 0, d=30)):               # repeated scoring
            new, pending, alerts = self.run_at(t)
            self.assertEqual((new, pending, alerts), ([], 0, []))
        self.assertEqual((self.r.base / "registry/scores.jsonl").read_bytes(), before)
        self.assertEqual(len(self.rows()), 6)
        self.assert_unique()

    def test_repeated_scoring_at_one_instant(self):
        a, _, _ = self.run_at(T(4, 30, d=27))
        b, _, _ = self.run_at(T(4, 30, d=27))
        self.assertEqual((len(a), b), (3, []))
        self.assertEqual(len(self.rows()), 3)
        self.assert_unique()

    def test_additional_batch_after_full_scoring(self):
        self.run_at(T(12, 0, d=29))
        before = (self.r.base / "registry/scores.jsonl").read_bytes()
        prepared = T(12, 4, d=29)
        ids = self.r.add_batch(T(12, 0, d=29), prepared, MS(prepared) + 60_000, MS(prepared) + 120_000)
        new, pending, _ = self.run_at(T(12, 0, d=29))                          # the new batch has not started
        self.assertEqual((new, pending), ([], 3))
        new, pending, _ = self.run_at(T(16, 30, d=29))                         # its 4h matured; 24h and 72h wait
        self.assertEqual(([x["id"] for x in new], pending), ([ids[0]], 2))
        self.assert_complete(new[0])
        self.assertTrue((self.r.base / "registry/scores.jsonl").read_bytes().startswith(before))
        self.assertEqual(len(self.rows()), 7)
        self.assert_unique()


@unittest.skipUnless(REPO, "needs the repository and the fixture")
class TestScoringStatesAndEvidence(unittest.TestCase):
    """12.4: awaiting maturity, ready for the next scheduled scorer, overdue and scoring failed are distinct; only
    overdue and failed are backlog. The evidence block reports paired differences, widths and dependence, and
    withholds uncertainty below the pre-declared block count."""

    def setUp(self):
        self.r = Repo()
        (self.r.base / "reports").mkdir()
        import range_job as J
        self.J = J

    def tearDown(self):
        self.r.close()

    @staticmethod
    def fetch(s, e):
        return [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]

    def test_states_across_time(self):
        end4 = RR._t(self.r.doc(IDS4[0])["horizon_utc"])               # 08:20; mature 08:25
        at = lambda minutes: RR.status(self.r.base, end4 + dt.timedelta(minutes=minutes))["scoring"]["4h"]   # noqa: E731
        self.assertEqual(at(4)["waiting-maturity"], 2)
        x = at(5 + 60)                                                   # matured an hour ago, not yet attempted
        self.assertEqual((x["ready"], x["overdue"], x["backlog"]), (1, 0, []))
        x = at(5 + RR.SCORE_OVERDUE_MIN + 1)                             # the scorer has not taken it
        self.assertEqual((x["ready"], x["overdue"], [b["state"] for b in x["backlog"]]), (0, 1, ["overdue"]))
        import scoring
        def partial(s, e):
            return scoring.check_bars(self.fetch(s, e)[:-1], s, e)
        self.J.score(self.r.base, end4 + dt.timedelta(minutes=10), fetch=partial)
        x = at(11)
        self.assertEqual((x["scoring-failed"], x["ready"], [b["state"] for b in x["backlog"]]), (1, 0, ["scoring-failed"]))
        self.J.score(self.r.base, end4 + dt.timedelta(minutes=70), fetch=self.fetch)
        x = at(71)
        self.assertEqual((x["scored"], x["scoring-failed"], x["backlog"]), (1, 0, []))

    def test_evidence_block(self):
        import scoring
        scoring.score_registry(self.r.base, MS(T(12, 0, d=29)), "t", fetch=self.fetch, only_prefix="range-rc1d-")
        st = RR.status(self.r.base, T(12, 0, d=29))
        ev = st["evaluation"]
        self.assertEqual(ev["method"], RR.EVAL_VERSION)
        e = ev["horizons"]["4h"]
        self.assertEqual(e["n"], 2)
        self.assertEqual(e["b2_better"] + e["ties"] + e["b2_worse"], 2)
        self.assertAlmostEqual(e["diff_mean"], round(e["mae_b2"] - e["mae_b0"], 5), places=4)
        self.assertTrue(0 < e["width_b2"] and 0 < e["width_b0"])
        self.assertIsNone(e["diff_mean_ci95"])
        self.assertIn("unavailable", e["uncertainty"])                  # 2 decisions: no block, no interval
        # 12.4.6 / repo 2.23: overlap is described from the actual registered windows, not a theoretical count
        w72 = ev["horizons"]["72h"]["window_overlap"]
        self.assertEqual((w72["windows"], w72["overlapping_another"], w72["largest_disjoint_subset"]), (2, 2, 1))
        self.assertIn("2 of 2 overlap another", ev["horizons"]["72h"]["windows"])
        self.assertEqual(e["window_overlap"]["windows"], 2)
        self.assertIn("ln range", e["metric"])
        md = RR.markdown(st)
        for want in ("Range scoring", "Range monitor", "## Current availability", "## Evidence (descriptive)",
                     "B2 better/tie/worse", "## Recent decisions (history)", "the weekly report only summarises"):
            self.assertIn(want, md)

    def test_interval_reported_only_with_enough_blocks(self):
        d = [(-0.05 if i % 3 else 0.02) for i in range(RR.EVAL_BLOCK * RR.EVAL_MIN_BLOCKS)]
        lo, hi = RR._bootstrap_mean(d, RR.EVAL_BLOCK, 400, RR.EVAL_SEED)
        self.assertTrue(lo <= sum(d) / len(d) <= hi)
        self.assertEqual(RR._bootstrap_mean(d, RR.EVAL_BLOCK, 400, RR.EVAL_SEED), [lo, hi])   # deterministic


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
