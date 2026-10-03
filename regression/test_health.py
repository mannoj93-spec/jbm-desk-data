"""Operational health (repo 2.24): gaps stay visible after recovery, incidents are recorded once, monitoring
can be stale or unknown, missed work is never completed by later data, and the check mutates no research state."""
import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)
import health as H   # noqa: E402

UTC = dt.timezone.utc
T0 = dt.datetime(2026, 10, 3, 0, 0, tzinfo=UTC)
MS = lambda t: int(t.timestamp() * 1000)          # noqa: E731
KEY = "d0e8c837be9c3a1e51c8a4836d44e73851f488305b2748cb770f35ff1d909952"


def run(t, trigger="schedule"):
    return {"t": MS(t), "mode": "routine", "trigger": trigger, "runner": "github", "critical_ok": True,
            "code_version": "test"}


class Base:
    def __init__(self, d):
        self.d = Path(d)
        for sub in ("data/runs", "state", "reports", "streams/ps1", "desk/research/ps1", "registry"):
            (self.d / sub).mkdir(parents=True, exist_ok=True)
        (self.d / "desk/release.json").write_text(json.dumps({"range_stream_start_utc": "2026-10-03T00:00:00Z"}))
        (self.d / "desk/research/ps1/protocol.json").write_text(json.dumps({"execution": {"max_delay_min": 90}}))
        (self.d / "streams/ps1/launch.json").write_text(json.dumps({"first_decision_utc": "2026-10-03T00:00:00Z",
                                                                     "protocol_sha256": KEY}))
        self.write("streams/ps1/lifecycle.jsonl", [{"key": KEY, "state": "active", "by": "job", "t_ms": MS(T0) + 1_200_000}])
        self.write("streams/ps1/executions.jsonl",
                   [{"decision_id": "ps1-20261003T0000Z", "fill_time_ms": MS(T0) + 1_225_000}])
        self.write("streams/ps1/decisions.jsonl", [{"decision_id": "ps1-20261003T0000Z", "action": "rebalance"}])
        self.write("state/range_attempts.jsonl",
                   [{"decision_utc": "2026-10-03T00:00:00Z", "state": "published", "run": {"production": True}}])
        (self.d / "reports/paper_ps1.json").write_text(json.dumps({"generated_utc": "2026-10-03T01:00:00.000Z",
                                                                   "coverage": 1.0, "scheduled_decisions": 1}))
        (self.d / "reports/range_status.json").write_text(json.dumps({
            "generated_utc": "2026-10-03T08:10:00Z", "status_expires_utc": "2026-10-03T09:20:00Z",
            "current": {"4h": {"state": "valid-current", "id": "x", "valid_until_utc": "2026-10-03T12:20:00Z"}}}))

    def write(self, rel, rows):
        (self.d / rel).write_text("".join(json.dumps(r) + "\n" for r in rows))

    def runs(self, times, trigger="schedule"):
        p = self.d / "data/runs/2026-10.jsonl"
        with open(p, "a") as f:
            for t in times:
                f.write(json.dumps(run(t, trigger)) + "\n")

    def snapshot(self):
        return {str(p.relative_to(self.d)): p.read_bytes() for p in self.d.rglob("*") if p.is_file()}


def every(start, end, minutes=15):
    out, t = [], start
    while t <= end:
        out.append(t)
        t += dt.timedelta(minutes=minutes)
    return out


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.b = Base(self.tmp.name)
        self.b.runs(every(T0, T0 + dt.timedelta(hours=11, minutes=4)))

    def tearDown(self):
        self.tmp.cleanup()

    def ev(self, at, **kw):
        return H.evaluate(self.b.d, now_ms=MS(at), stale_min=90, **kw)

    def test_ongoing_gap_then_recovery_recorded_once_each(self):
        during = T0 + dt.timedelta(hours=13)
        d1 = self.ev(during)
        self.assertEqual(d1["source"]["state"], "stale")
        self.assertIsNone(d1["source"]["gaps"][-1]["end_utc"])
        new = H.record(self.b.d, d1)
        self.assertEqual([r["status"] for r in new if r["kind"] == "collector_gap"], ["ongoing"])
        self.assertEqual([r for r in H.record(self.b.d, self.ev(during + dt.timedelta(minutes=10))) if r["kind"] == "collector_gap"], [])
        self.b.runs([T0 + dt.timedelta(hours=13, minutes=27)])
        after = T0 + dt.timedelta(hours=13, minutes=40)
        d2 = self.ev(after)
        self.assertEqual(d2["source"]["state"], "healthy")
        self.assertEqual(d2["source"]["gaps"][0]["end_utc"], "2026-10-03T13:27:00Z")     # stays visible after recovery
        new = [r for r in H.record(self.b.d, d2) if r["kind"] == "collector_gap"]
        self.assertEqual((len(new), new[0]["status"], new[0]["recorded_after_end"]), (1, "resolved", True))
        self.assertEqual(new[0]["first_recorded_utc"], "2026-10-03T13:40:00Z")            # detection != event time
        self.assertEqual(new[0]["start_utc"], "2026-10-03T11:00:00Z")          # last scheduled record before the gap
        self.assertEqual([r for r in H.record(self.b.d, self.ev(after + dt.timedelta(minutes=15))) if r["kind"] == "collector_gap"], [])

    def test_manual_runs_do_not_close_a_scheduled_gap(self):
        self.b.runs([T0 + dt.timedelta(hours=12, minutes=30)], trigger="workflow_dispatch")
        d = self.ev(T0 + dt.timedelta(hours=13))
        self.assertEqual(d["source"]["state"], "stale")
        self.assertEqual(d["source"]["manual_runs_since"], 1)

    def test_missed_decisions_stay_missed_when_later_data_arrives(self):
        self.b.runs(every(T0 + dt.timedelta(hours=13, minutes=27), T0 + dt.timedelta(hours=16)))
        later = T0 + dt.timedelta(hours=16)
        # recovered price bars for the gap land after the decision; they create no decision or attempt
        (self.b.d / "data/prices").mkdir(parents=True)
        (self.b.d / "data/prices/bars.jsonl").write_text(json.dumps({"observed_at": MS(later), "bars": [[MS(T0) + 43_200_000, 1, 1, 1, 1]]}) + "\n")
        d = self.ev(later)
        self.assertEqual(d["decisions"]["range"]["2026-10-03T12:00:00Z"], "absent")
        self.assertEqual(d["decisions"]["ps1"]["2026-10-03T12:00:00Z"], "missed: no decision record (run absent)")
        self.assertEqual(d["decisions"]["ps1"]["2026-10-03T00:00:00Z"], "executed")
        cov = d["ps1_coverage"]
        self.assertEqual(cov["report_coverage"], 1.0)                                      # as of its own generation
        self.assertIn("2026-10-03T12:00:00Z", [x["decision_utc"] for x in cov["not_covered"]])
        self.assertNotIn("2026-10-03T00:00:00Z", [x["decision_utc"] for x in cov["not_covered"]])

    def test_a_decision_inside_its_deadline_is_pending_not_missed(self):
        d = self.ev(T0 + dt.timedelta(hours=4, minutes=30))
        self.assertEqual(d["decisions"]["ps1"]["2026-10-03T04:00:00Z"], "pending")
        self.assertFalse(any(r["subject"] == "2026-10-03T04:00:00Z" for r in H.incidents(d)))

    def test_operator_pause_makes_later_decisions_not_expected(self):
        self.b.write("streams/ps1/lifecycle.jsonl", [{"key": KEY, "state": "active", "by": "job", "t_ms": MS(T0) + 1_200_000},
                                                     {"key": KEY, "state": "paused", "by": "operator", "t_ms": MS(T0) + 7_200_000}])
        d = self.ev(T0 + dt.timedelta(hours=9))
        self.assertTrue(d["decisions"]["ps1"]["2026-10-03T04:00:00Z"].startswith("not expected (lifecycle paused by operator"))

    def test_expired_forecasts_on_the_check_clock(self):
        a = self.ev(T0 + dt.timedelta(hours=10))["availability"]
        self.assertEqual(a["status"], "expired")
        self.assertEqual(a["horizons"]["4h"]["state_now"], "expired on this clock")
        a = self.ev(T0 + dt.timedelta(hours=9))["availability"]
        self.assertEqual((a["status"], a["horizons"]["4h"]["state_now"]), ("within expiry", "valid-current"))

    def test_monitoring_unknown_without_token_and_stale_when_old(self):
        self.assertEqual(self.ev(T0 + dt.timedelta(hours=11))["monitors"]["state"], "unknown")

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
            started = "2026-10-03T08:17:00Z" if "watchdog" in req.full_url else "2026-10-03T09:53:00Z"
            return Resp(json.dumps({"workflow_runs": [{"run_started_at": started, "conclusion": "success"}]}).encode())
        m = self.ev(T0 + dt.timedelta(hours=11), token="t", repo="o/r", opener=opener)["monitors"]
        self.assertEqual(m["workflows"]["watchdog.yml"]["state"], "stale")                 # an old success is not health
        self.assertEqual(m["workflows"]["range-monitor.yml"]["state"], "fresh")
        self.assertEqual(m["state"], "stale")
        self.assertEqual(m["newest_scheduled_start_utc"], "2026-10-03T09:53:00Z")

    def test_read_only_evaluation_and_bounded_record_writes(self):
        before = self.b.snapshot()
        self.ev(T0 + dt.timedelta(hours=13))
        self.assertEqual(self.b.snapshot(), before)
        H.record(self.b.d, self.ev(T0 + dt.timedelta(hours=13)))
        after = self.b.snapshot()
        changed = {k for k in after if before.get(k) != after[k]}
        self.assertEqual(changed, {"reports/health.json", "reports/health.md", "state/incidents.jsonl"})


if __name__ == "__main__":
    unittest.main()
