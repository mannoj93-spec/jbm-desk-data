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

    def test_native_silence_stays_in_the_report_and_gets_no_incident_row_of_its_own(self):
        # Repo 2.30.9: the native schedule is the secondary trigger. A silence is still measured and listed in the
        # report at every evaluation, but it is no longer one incident row per silence.
        during = T0 + dt.timedelta(hours=13)
        d1 = self.ev(during)
        self.assertEqual(d1["source"]["state"], "stale")
        self.assertIsNone(d1["source"]["gaps"][-1]["end_utc"])
        self.assertEqual([r for r in H.record(self.b.d, d1) if r["kind"] == "collector_gap"], [])
        self.b.runs([T0 + dt.timedelta(hours=13, minutes=27)])
        d2 = self.ev(T0 + dt.timedelta(hours=13, minutes=40))
        self.assertEqual(d2["source"]["state"], "healthy")
        self.assertEqual(d2["source"]["gaps"][0]["end_utc"], "2026-10-03T13:27:00Z")     # stays visible after recovery
        self.assertEqual([r for r in H.record(self.b.d, d2) if r["kind"] == "collector_gap"], [])
        self.assertIn("1 silence(s) over 90 min", H.markdown(d2))

    def test_native_schedule_is_summarized_once_per_closed_day(self):
        self.b.runs([T0 + dt.timedelta(hours=13, minutes=27)])                 # one native start after a 147-min silence
        same_day = self.ev(T0 + dt.timedelta(hours=14))
        self.assertEqual(same_day["source"]["native_daily"], [])               # the day has not closed: no summary yet
        self.assertEqual([r for r in H.record(self.b.d, same_day) if r["kind"] == "native_schedule_day"], [])
        nxt = T0 + dt.timedelta(days=1, hours=2)
        d = self.ev(nxt)
        day = d["source"]["native_daily"]
        self.assertEqual([(x["day"], x["native_runs"], x["automated_runs"], x["native_gaps_over_limit"]) for x in day],
                         [("2026-10-03", 46, 46, 1)])
        self.assertEqual(day[0]["longest_native_silence_min"], 633.0)          # 13:27 to midnight: day edges count
        new = [r for r in H.record(self.b.d, d) if r["kind"] == "native_schedule_day"]
        self.assertEqual([(r["start_utc"], r["end_utc"], r["status"], r["native_runs"], r["recorded_after_end"]) for r in new],
                         [("2026-10-03T00:00:00Z", "2026-10-04T00:00:00Z", "summary", 46, True)])
        again = H.record(self.b.d, self.ev(nxt + dt.timedelta(hours=3)))       # recorded once, never again
        self.assertEqual([r for r in again if r["kind"] == "native_schedule_day"], [])
        self.assertIn("2026-10-03 46 of 46 automated runs", H.markdown(d))

    def test_malformed_lines_are_counted_not_dropped_silently(self):
        clean = self.ev(T0 + dt.timedelta(hours=11))
        self.assertEqual(clean["integrity"]["malformed_lines"], {})
        self.assertIn("no malformed lines", H.markdown(clean))
        p = Path(self.b.d) / "state/incidents.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('{"kind": "service_gap", "subject": "x", "start_utc": "a", "end_utc": "b"}\n{"kind": "torn\n[1, 2]\n\n')
        d = self.ev(T0 + dt.timedelta(hours=11))
        self.assertEqual(d["integrity"]["malformed_lines"], {"state/incidents.jsonl": 2})   # torn line and a non-object; blank is nothing
        self.assertIn("MALFORMED LINES SKIPPED - state/incidents.jsonl 2", H.markdown(d))
        self.assertEqual(len(H.rows(p)), 1)
        p.write_text('{"kind": "service_gap", "subject": "x", "start_utc": "a", "end_utc": "b"}\n')
        self.assertEqual(self.ev(T0 + dt.timedelta(hours=11))["integrity"]["malformed_lines"], {})

    def test_timer_token_expiry_is_unrecorded_until_the_operator_records_it(self):
        now = T0 + dt.timedelta(hours=11)
        d = self.ev(now)
        self.assertEqual(d["timer_token"]["state"], "unrecorded")
        self.assertIn("expiry not recorded", H.markdown(d))
        decl = Path(self.b.d) / "docs/acceptance/timer.json"
        decl.parent.mkdir(parents=True, exist_ok=True)
        for expires, state in [("2027-10-05T00:00:00Z", "ok"), ("2026-10-20T00:00:00Z", "expiring"),
                               ("2026-10-03T11:00:00Z", "expired"), ("2026-10-01T00:00:00Z", "expired")]:
            decl.write_text(json.dumps({"token": {"expires_utc": expires, "recorded": "test"}}))
            self.assertEqual(self.ev(now)["timer_token"]["state"], state, expires)
        for bad in [{"token": {"expires_utc": "soon"}}, {"token": {"expires_utc": None}}, {"token": "x"}, {}]:
            decl.write_text(json.dumps(bad))
            self.assertEqual(self.ev(now)["timer_token"]["state"], "unrecorded", bad)   # unreadable is never 'ok'
        decl.write_text(json.dumps({"token": {"expires_utc": "2026-10-20T00:00:00Z"}}))
        self.assertIn("expiring; expires 2026-10-20T00:00:00Z", H.markdown(self.ev(now)))

    def test_timer_check_fails_on_a_silent_or_unreadable_primary_trigger(self):
        now = dt.datetime(2026, 10, 5, 20, 20, tzinfo=dt.timezone.utc)
        def opener_for(created):
            class Resp:
                def __enter__(self_): return self_
                def __exit__(self_, *a): return False
                def read(self_): return json.dumps({"workflow_runs": [
                    {"event": "workflow_dispatch", "display_title": "Recovery dispatcher (external)", "created_at": c}
                    for c in created]}).encode()
            return lambda req, timeout=20: Resp()
        arriving = [f"2026-10-05T{h:02d}:{m:02d}:05Z" for h in range(17, 21) for m in (12, 27, 42, 57) if (h, m) <= (20, 12)]
        code, msg = H.timer_check("tok", "o/r", now, opener_for(arriving))
        self.assertEqual(code, 0); self.assertIn("external timer arriving", msg)
        code, msg = H.timer_check("tok", "o/r", now, opener_for(arriving[:-4]))          # nothing for over 45 minutes
        self.assertEqual(code, 1); self.assertIn("external timer silent", msg)
        self.assertEqual(H.timer_check("tok", "o/r", now, opener_for([]))[0], 1)         # never arrived
        self.assertEqual(H.timer_check(None, "o/r", now)[0], 1)                          # unknown is not arriving
        def broken(req, timeout=20): raise OSError("down")
        code, msg = H.timer_check("tok", "o/r", now, broken)
        self.assertEqual(code, 1); self.assertIn("unknown", msg)

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

    def test_a_late_stale_skip_is_still_a_missed_decision_and_recorded_once(self):
        # Oct 3 production sequence: 12:00Z had no record during the silence; a scheduled run delivered ~3 h late
        # refused the stale bar and recorded "skipped". The decision stays missed and is recorded once.
        during = T0 + dt.timedelta(hours=14)                     # both deadlines passed, collector still silent
        first = [r for r in H.record(self.b.d, self.ev(during)) if r["subject"] == "2026-10-03T12:00:00Z"]
        self.assertEqual([r["kind"] for r in first], ["range_decision", "ps1_decision"])
        with open(self.b.d / "state/range_attempts.jsonl", "a") as f:
            f.write(json.dumps({"decision_utc": "2026-10-03T12:00:00Z", "state": "skipped",
                                "reason": "stale decision (2.99h > 1.0h)",
                                "run": {"production": True}}) + "\n")
        later = self.ev(T0 + dt.timedelta(hours=15))
        self.assertTrue(later["decisions"]["range"]["2026-10-03T12:00:00Z"].startswith("missed: skipped"))
        self.assertIn("2026-10-03T12:00:00Z", [r["subject"] for r in H.incidents(later) if r["kind"] == "range_decision"])
        self.assertEqual([r for r in H.record(self.b.d, later) if r["subject"] == "2026-10-03T12:00:00Z"], [])

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


class MonitorHeartbeatTests(unittest.TestCase):
    """2.26: a monitor that ran on time and failed is a fresh heartbeat with a detected problem, not silence."""
    def test_recent_failed_check_with_an_old_success(self):
        now = dt.datetime(2026, 10, 5, 7, 0, tzinfo=UTC)
        runs = [{"id": 2, "status": "completed", "conclusion": "failure", "created_at": "2026-10-05T06:01:00Z",
                 "updated_at": "2026-10-05T06:01:40Z"},
                {"id": 1, "status": "completed", "conclusion": "success", "created_at": "2026-10-04T18:00:00Z",
                 "updated_at": "2026-10-04T18:00:30Z"}]
        e, _ = H.heartbeat(runs, now, 510)
        self.assertEqual((e["state"], e["last_result"], e["last_run_id"]), ("fresh", "failure", 2))
        self.assertEqual(e["last_success_utc"], "2026-10-04T18:00:00Z")      # still reported, separately
        late = dt.datetime(2026, 10, 5, 16, 0, tzinfo=UTC)
        self.assertEqual(H.heartbeat(runs, late, 510)[0]["state"], "stale")     # silence is still silence
        self.assertEqual(H.heartbeat([], now, 510)[0]["state"], "unknown")
        running = [{"id": 3, "status": "in_progress", "created_at": "2026-10-05T06:59:00Z"}]
        self.assertEqual(H.heartbeat(running, now, 510)[0]["state"], "unknown")  # a start is not a completed check


if __name__ == "__main__":
    unittest.main()

class RecoveryCheckTests(unittest.TestCase):
    def test_recovery_check_evidence_is_separate_from_overall_run_failure(self):
        from unittest.mock import patch
        runs=[{'id':1,'head_branch':'main','status':'completed','conclusion':'failure','updated_at':'2026-10-27T12:02:00Z'},
              {'id':2,'head_branch':'main','status':'in_progress','updated_at':'2026-10-27T12:10:00Z'},
              {'id':3,'head_branch':'pr','status':'completed','updated_at':'2026-10-27T12:11:00Z'}]
        jobs=[{'name':name,'runner_id':42,'steps':[{'name':step,'started_at':'2026-10-27T12:01:00Z',
                'completed_at':'2026-10-27T12:02:00Z','conclusion':result}]} for name,step,result in [
                ('service-watch','Collector service continuity','success'),
                ('study-watch','Check study deadlines and collection gaps from current records','failure')]]
        with patch.object(H,'_get',return_value={'jobs':jobs}) as get:
            r=H.recovery_checks(runs,H.parse('2026-10-27T12:15:00Z'),'t','o/r',None)
            self.assertIn('/runs/1/jobs',get.call_args.args[0])
            self.assertEqual(r['service-watch']['last_check'],'passed')
            self.assertEqual(r['study-watch']['last_check'],'check failed')
            self.assertEqual(r['study-watch']['state'],'fresh')
            stale=H.recovery_checks(runs,H.parse('2026-10-27T13:00:00Z'),'t','o/r',None)
            self.assertEqual(stale['service-watch']['state'],'stale')
            jobs[0]['steps']=[];jobs[0]['runner_id']=0
            unknown=H.recovery_checks(runs,H.parse('2026-10-27T12:15:00Z'),'t','o/r',None)
            self.assertEqual(unknown['service-watch']['last_check'],'no runner')
            self.assertIsNone(unknown['service-watch']['last_completed_utc'])
