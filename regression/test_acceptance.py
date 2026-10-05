"""service_acceptance 2.0 (repo 2.26): reproduces the 2.25 gate's three defects - a one-hour window could pass, records
with critical_ok false were credited, and only collector records were checked for people - and covers a complete
healthy 24 h fixture, short and unfinished windows, missing evidence, failed critical collection, optional-source
degradation, persistence failures, unknown lineage and intervention anywhere in the critical chain. Synthetic."""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk"), str(ROOT / "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)
import service_acceptance as A   # noqa: E402

UTC = dt.timezone.utc
START = dt.datetime(2026, 10, 6, 0, 0, tzinfo=UTC)
END = START + dt.timedelta(hours=24)
AFTER = END + dt.timedelta(hours=2)
KEY = "d0e8c837be9c3a1e51c8a4836d44e73851f488305b2748cb770f35ff1d909952"
BOT = "github-actions[bot]"
OWNER = "mannoj93-spec"


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def ms(t):
    return int(t.timestamp() * 1000)


class World:
    """A complete healthy day: every slot collected (alternating native and recovery chains rooted in the external
    timer), six range decisions published, six PS1 decisions executed once, no backlog."""
    def __init__(self, d):
        self.d = Path(d)
        for sub in ("data/runs", "state", "registry", "reports", "desk/research/ps1", "streams/ps1"):
            (self.d / sub).mkdir(parents=True, exist_ok=True)
        (self.d / "cadence.json").write_text(json.dumps({"periods": [{"from": "2026-09-23T16:06:13Z", "minutes": [7, 22, 37, 52]}]}))
        (self.d / "desk/release.json").write_text(json.dumps({"range_stream_start_utc": "2026-09-26T04:00:00Z"}))
        (self.d / "desk/research/ps1/protocol.json").write_text(json.dumps({"execution": {"max_delay_min": 90}}))
        (self.d / "streams/ps1/launch.json").write_text(json.dumps({"first_decision_utc": "2026-10-03T00:00:00Z",
                                                                     "protocol_sha256": KEY}))
        self.write("streams/ps1/lifecycle.jsonl", [{"key": KEY, "state": "active", "by": "job", "t_ms": 1}])
        self.runs, self.records, self.next_id = [], [], 1000
        t = START + dt.timedelta(minutes=7)
        i = 0
        while t < END:
            if i % 2 == 0:
                self.collector(t + dt.timedelta(minutes=2), native=True)
            else:
                disp = self.run("recovery.yml", t + dt.timedelta(minutes=5, seconds=20), "workflow_dispatch", OWNER,
                                title="Recovery dispatcher (external)")
                self.collector(t + dt.timedelta(minutes=6), native=False, root=f"{disp['id']}:external")
            t += dt.timedelta(minutes=15)
            i += 1
        att, pubs, dec, ex = [], [], [], []
        d = START
        while d < END:
            a = f"{iso(d)}#{self.next_id}"
            self.run("range.yml", d + dt.timedelta(minutes=3), "schedule", OWNER)
            att.append({"attempt": a, "decision_utc": iso(d), "state": "published", "run": {"production": True}})
            pubs.append({"attempt": a, "eligible": True, "start_ms": ms(d + dt.timedelta(minutes=20))})
            did = f"ps1-{d:%Y%m%dT%H%MZ}"
            dec.append({"decision_id": did, "action": "rebalance"})
            ex += [{"decision_id": did, "fill_time_ms": ms(d + dt.timedelta(minutes=12)), "arm": arm} for arm in ("A", "B")]
            d += dt.timedelta(hours=4)
        self.write("state/range_attempts.jsonl", att)
        self.write("state/range_publications.jsonl", pubs)
        self.write("streams/ps1/decisions.jsonl", dec)
        self.write("streams/ps1/executions.jsonl", ex)
        (self.d / "state/forecast_manifest.json").write_text("{}")
        self.flush()

    def run(self, wf, created, event, trig, title=None, conclusion="success", branch="main"):
        self.next_id += 1
        r = {"id": self.next_id, "event": event, "status": "completed", "conclusion": conclusion,
             "created_at": iso(created), "updated_at": iso(created + dt.timedelta(minutes=2)),
             "display_title": title or wf, "head_branch": branch, "path": f".github/workflows/{wf}",
             "actor": trig, "triggering_actor": trig}
        self.runs.append(r)
        return r

    def collector(self, t, native, root=None, critical=True, persist=True, **extra):
        if native:
            r = self.run("collect.yml", t, "schedule", OWNER)
            prov = {"source": "native-schedule"}
        else:
            r = self.run("collect.yml", t, "workflow_dispatch", BOT, title=f"Collector recovery x via {root}")
            prov = {"source": "recovery", "origin": root}
        if persist:
            rec = {"t": ms(t), "mode": "routine", "runner": "github", "trigger": r["event"], "run_id": str(r["id"]),
                   "critical_ok": critical, "errors": {}, "series": {}, "snap": {"books_ok": 17, "books": 17},
                   "provenance": prov, "code_version": "test"}
            rec.update(extra)
            self.records.append(rec)
        return r

    def write(self, rel, rows):
        (self.d / rel).write_text("".join(json.dumps(r) + "\n" for r in rows))

    def flush(self):
        self.write("data/runs/2026-10.jsonl", self.records)

    def measure(self, start=START, end=END, now=AFTER, runs="all", complete=True):
        return A.measure(self.d, start, end, now, self.runs if runs == "all" else runs, complete, "2026-10-07T02:00:00Z")


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.w = World(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_complete_healthy_day_passes_with_its_numbers(self):
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "pass", doc["checks"])
        c = doc["collection"]
        self.assertEqual((c["intervals"], c["intervals_with_unattended_critical_success"], c["allowed_empty"]), (95, 95, 2))
        self.assertEqual(c["by_initiation"], {"verified": 48, "timer-corroborated": 48})
        self.assertEqual(len(doc["decisions"]["range"]), 6)
        self.assertEqual(len(doc["decisions"]["ps1"]), 6)
        self.assertEqual(doc["inputs"]["actions"]["complete"], True)
        self.assertEqual(len(doc["inputs"]["files_sha256"]), 64)

    def test_reproduced_short_window_is_invalid_and_unfinished_is_pending(self):
        self.assertEqual(self.w.measure(start=START + dt.timedelta(hours=1), end=START + dt.timedelta(hours=2))["verdict"],
                         "invalid")
        self.assertEqual(self.w.measure(now=END - dt.timedelta(minutes=1))["verdict"], "pending")

    def test_missing_or_incomplete_actions_evidence_is_insufficient(self):
        self.assertEqual(self.w.measure(runs=None)["verdict"], "insufficient")
        self.assertEqual(self.w.measure(complete=False)["verdict"], "insufficient")

    def test_reproduced_failed_critical_collection_is_not_credited(self):
        for r in self.w.records:
            r["critical_ok"] = False
            r["snap"] = {"books_ok": 0, "books": 17}
        self.w.flush()
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "fail")
        self.assertEqual(doc["collection"]["intervals_with_unattended_critical_success"], 0)
        self.assertEqual(len(doc["collection"]["critical_failures"]), 96)

    def test_optional_degradation_is_a_warning_not_a_failure(self):
        for r in self.w.records[::3]:
            r["snap"] = {"books_ok": 16, "books": 17, "failed": {"kraken": "HTTP 502"}}
        self.w.flush()
        doc = self.w.measure()
        self.assertEqual(doc["verdict"], "pass", doc["checks"])
        self.assertEqual(doc["collection"]["degraded_optional_records"], 32)

    def test_empty_decision_evidence_fails(self):
        self.w.write("state/range_attempts.jsonl", [])
        doc = self.w.measure()
        self.assertFalse(doc["checks"]["range_decisions_published"])
        self.assertTrue(all(v == "missed: absent" for v in doc["decisions"]["range"].values()))
        self.assertEqual(len(doc["decisions"]["range"]), 6)               # expected from the schedule, not the records

    def test_reproduced_manual_intervention_outside_the_collector_fails(self):
        self.w.run("range.yml", START + dt.timedelta(hours=8, minutes=10), "workflow_dispatch", OWNER)
        doc = self.w.measure()
        self.assertFalse(doc["checks"]["no_person_in_chain"])
        self.assertEqual(doc["chain"]["person_or_unverified_external"][0]["workflow"], "range")

    def test_person_started_dispatcher_taints_its_children(self):
        disp = self.w.run("recovery.yml", START + dt.timedelta(hours=3, minutes=33), "workflow_dispatch", OWNER)
        self.w.run("research-streams.yml", START + dt.timedelta(hours=3, minutes=40), "workflow_dispatch", BOT,
                   title=f"Research streams recovery x via {disp['id']}:human")
        people = self.w.measure()["chain"]["person_or_unverified_external"]
        self.assertEqual(sorted(p["workflow"] for p in people), ["dispatcher", "streams"])

    def test_off_timer_external_dispatch_is_unverified(self):
        self.w.run("recovery.yml", START + dt.timedelta(hours=5, minutes=3), "workflow_dispatch", OWNER,
                   title="Recovery dispatcher (external)")
        doc = self.w.measure()
        self.assertIn({"run": self.w.next_id, "workflow": "dispatcher", "initiation": "declared-external"},
                      doc["chain"]["person_or_unverified_external"])

    def test_failed_push_is_a_persistence_failure_and_unknown_lineage_is_not_counted(self):
        self.w.collector(START + dt.timedelta(hours=2, minutes=10), native=True, persist=False)
        self.w.runs[-1]["conclusion"] = "failure"
        doc = self.w.measure()
        self.assertEqual(doc["persistence"]["without_stored_record"], [self.w.next_id])
        self.assertFalse(doc["checks"]["no_persistence_failures"])
        # a recovery record whose root dispatcher run is not in the evidence counts as unknown
        lost_root = [r for r in self.w.runs if r["display_title"] == "Recovery dispatcher (external)"][0]
        self.w.runs.remove(lost_root)
        self.assertEqual(self.w.measure()["collection"]["by_initiation"].get("unknown"), 1)

    def test_duplicate_ps1_execution_fails(self):
        ex = (self.w.d / "streams/ps1/executions.jsonl").read_text()
        (self.w.d / "streams/ps1/executions.jsonl").write_text(
            ex + json.dumps({"decision_id": "ps1-20261006T0800Z", "fill_time_ms": ms(START) + 99, "arm": "A"}) + "\n")
        doc = self.w.measure()
        self.assertEqual(doc["decisions"]["ps1_duplicate_executions"], {"2026-10-06T08:00:00Z": 2})
        self.assertFalse(doc["checks"]["ps1_decisions_resolved"])


if __name__ == "__main__":
    unittest.main()
