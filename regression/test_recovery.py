"""Recovery dispatcher (repo 2.25): dropped and delayed native triggers, queue contention, racing native and recovery
starts, failed dispatches, an unavailable Actions API, missed forecast deadlines, provenance and the separation of
native cadence from automated service continuity. Every input is an isolated fixture; nothing calls GitHub."""
import datetime as dt
import io
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cadence      # noqa: E402
import provenance   # noqa: E402
import recovery as R  # noqa: E402
import storage      # noqa: E402
import watchdog     # noqa: E402

UTC = dt.timezone.utc
Q = [7, 22, 37, 52]


def t(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def gh(created, event="schedule", status="completed", conclusion="success", title=None, updated=None, name=""):
    return {"id": random.randint(1, 10**9), "event": event, "status": status,
            "conclusion": conclusion if status == "completed" else None, "created_at": created,
            "updated_at": updated or created, "display_title": title or name}


class PlanTests(unittest.TestCase):
    def plan(self, now, **runs):
        return R.plan(t(now), runs, minutes=Q)

    def keys(self, items):
        return [(w, k) for w, k, _ in items]

    def test_collector_due_only_when_no_run_since_the_slot(self):
        now = "2026-10-04T12:12:00Z"     # slot 12:07, grace 4 min
        self.assertIn(("collector", "2026-10-04T12:07:00Z"), self.keys(self.plan(now)))
        for covered in (gh("2026-10-04T12:09:00Z"),                                   # native, late
                        gh("2026-10-04T12:10:00Z", status="queued"),                  # queued behind repo-write
                        gh("2026-10-04T12:08:00Z", event="workflow_dispatch")):       # a person's run
            self.assertNotIn("collector", [w for w, _, _ in self.plan(now, collector=[covered])])
        cancelled = gh("2026-10-04T12:09:00Z", conclusion="cancelled")
        self.assertIn("collector", [w for w, _, _ in self.plan(now, collector=[cancelled])])
        # inside the grace period the native start still has time
        self.assertNotIn("collector", [w for w, _, _ in self.plan("2026-10-04T12:10:00Z",
                                                                  collector=[gh("2026-10-04T11:54:00Z")])])

    def test_one_recovery_dispatch_per_slot(self):
        mine = gh("2026-10-04T12:12:30Z", event="workflow_dispatch", title=R.title("Collector", "2026-10-04T12:07:00Z"),
                  conclusion="cancelled")
        self.assertNotIn("collector", [w for w, _, _ in self.plan("2026-10-04T12:14:00Z", collector=[mine])])

    def test_range_window_is_derived_from_the_freshness_limit(self):
        self.assertNotIn("range", [w for w, _, _ in self.plan("2026-10-04T12:05:00Z")])     # native :02 + grace
        self.assertIn(("range", "2026-10-04T12:00:00Z"), self.keys(self.plan("2026-10-04T12:12:00Z")))
        self.assertIn(("range", "2026-10-04T12:00:00Z"), self.keys(self.plan("2026-10-04T12:45:00Z")))
        # past the last dispatch time a late forecast would be refused; the decision stays missed, nothing is sent
        self.assertNotIn("range", [w for w, _, _ in self.plan("2026-10-04T12:46:00Z")])
        self.assertLess(R.RANGE_LAST_DISPATCH_MIN + 15, 60 + 1)

    def test_range_covered_by_any_live_run_and_retried_only_after_failures(self):
        now = "2026-10-04T12:27:00Z"
        for run in (gh("2026-10-04T12:03:00Z", status="in_progress"), gh("2026-10-04T12:03:00Z")):
            self.assertNotIn("range", [w for w, _, _ in self.plan(now, range=[run])])
        failed = gh("2026-10-04T12:03:00Z", conclusion="failure")
        self.assertIn("range", [w for w, _, _ in self.plan(now, range=[failed])])
        k = "2026-10-04T12:00:00Z"
        two = [failed] + [gh(f"2026-10-04T12:1{i}:00Z", event="workflow_dispatch", conclusion="failure",
                             title=R.title("Range forecasts", k)) for i in range(2)]
        self.assertNotIn("range", [w for w, _, _ in self.plan(now, range=two)])                # bounded at two

    def test_streams_follow_the_range_run_and_respect_the_ps1_deadline(self):
        rr = [gh("2026-10-04T12:13:00Z", updated="2026-10-04T12:16:00Z")]
        self.assertNotIn("streams", [w for w, _, _ in self.plan("2026-10-04T12:17:00Z", range=rr)])   # chain's turn
        self.assertIn("streams", [w for w, _, _ in self.plan("2026-10-04T12:27:00Z", range=rr)])
        chained = gh("2026-10-04T12:16:20Z", event="workflow_run")
        self.assertNotIn("streams", [w for w, _, _ in self.plan("2026-10-04T12:27:00Z", range=rr, streams=[chained])])
        self.assertIn("streams", [w for w, _, _ in self.plan("2026-10-04T12:57:00Z")])          # no range run: +50
        self.assertNotIn("streams", [w for w, _, _ in self.plan("2026-10-04T13:16:00Z")])       # past +75

    def test_scoring_after_seventy_minutes(self):
        self.assertNotIn("scoring", [w for w, _, _ in self.plan("2026-10-04T12:42:00Z", scoring=[gh("2026-10-04T11:41:00Z")])])
        self.assertIn(("scoring", "2026-10-04T12:00:00Z"),
                      self.keys(self.plan("2026-10-04T12:57:00Z", scoring=[gh("2026-10-04T11:41:00Z")])))

    def test_a_day_with_dropped_and_late_native_starts(self):
        """Simulate 24 h of 15-minute dispatcher invocations while the native schedule drops 90% of its runs and
        starts the rest 0-40 min late; a run exists only after its dispatch or native creation."""
        rng = random.Random(7)
        start = t("2026-10-04T00:00:00Z")
        runs = {k: [] for k in R.WORKFLOWS}
        native = []
        for h in range(24):
            for m in Q:
                if rng.random() < 0.1:
                    native.append(("collector", start + dt.timedelta(hours=h, minutes=m + rng.randint(0, 40))))
            if h % 4 == 0 and rng.random() < 0.1:
                native.append(("range", start + dt.timedelta(hours=h, minutes=2 + rng.randint(0, 200))))
        dispatched = []
        for i in range(24 * 4):
            now = start + dt.timedelta(minutes=12 + 15 * i)
            for w, c in [x for x in native if x[1] <= now]:
                runs[w].append(gh(R.iso(c), updated=R.iso(c + dt.timedelta(minutes=2))))
                native.remove((w, c))
            for w, key, _ in R.plan(now, runs, minutes=Q):
                dispatched.append((w, key, now))
                name = R.WORKFLOWS[w][1]
                runs[w].append(gh(R.iso(now + dt.timedelta(seconds=20)), event="workflow_dispatch",
                                  title=R.title(name, key), updated=R.iso(now + dt.timedelta(minutes=3))))
        keys = [(w, k) for w, k, _ in dispatched]
        self.assertEqual(len(keys), len(set(keys)), "a key was dispatched twice")
        created = sorted(R.created(r) for r in runs["collector"])
        gaps = [(b - a).total_seconds() / 60 for a, b in zip(created, created[1:])]
        self.assertLessEqual(max(gaps), 30)                                   # every slot started within its slot
        for h in range(0, 24, 4):
            d = start + dt.timedelta(hours=h)
            first = min(R.created(r) for r in runs["range"] if R.created(r) >= d)
            self.assertLess((first - d).total_seconds() / 60, R.RANGE_LAST_DISPATCH_MIN + 1)
        self.assertLessEqual(max(sum(1 for w, _, n in dispatched if n == x) for _, _, x in dispatched), 4)


class Opener:
    """Stand-in for urllib's opener: GET lists, POST dispatches; records every request."""
    def __init__(self, list_status=200, post_status=204, fail_first=0):
        self.calls, self.list_status, self.post_status, self.fail_first = [], list_status, post_status, fail_first

    def __call__(self, req, timeout=None):
        self.calls.append((req.get_method(), req.full_url, req.data))
        if req.get_method() == "POST":
            if self.fail_first:
                self.fail_first -= 1
                raise urllib.error.HTTPError(req.full_url, 502, "bad gateway", {}, None)
            if self.post_status >= 400:
                raise urllib.error.HTTPError(req.full_url, self.post_status, "x", {}, None)
            return Resp(self.post_status, b"")
        if self.list_status >= 400:
            raise urllib.error.HTTPError(req.full_url, self.list_status, "x", {}, None)
        return Resp(200, json.dumps({"workflow_runs": []}).encode())


class Resp(io.BytesIO):
    def __init__(self, status, body):
        super().__init__(body)
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class ExecutorTests(unittest.TestCase):
    def setUp(self):
        self._sleep, R._sleep = R._sleep, (lambda s: None)

    def tearDown(self):
        R._sleep = self._sleep

    def test_dispatch_sends_recovery_inputs_to_main(self):
        o = Opener()
        res = R.dispatch("o/r", "tok", [("range", "2026-10-04T12:00:00Z", "why")], "123:external", opener=o)
        self.assertTrue(res[0]["ok"])
        method, url, data = o.calls[0]
        self.assertTrue(url.endswith("/actions/workflows/range.yml/dispatches"))
        self.assertEqual(json.loads(data), {"ref": "main", "inputs": {"trigger": "recovery", "slot": "2026-10-04T12:00:00Z",
                                                                       "origin": "123:external"}})

    def test_permission_failure_and_server_errors_are_reported_not_looped(self):
        res = R.dispatch("o/r", "tok", [("collector", "k", "why")], "1:x", opener=Opener(post_status=403))
        self.assertEqual(res[0], {"workflow": "collect.yml", "slot": "k", "reason": "why", "ok": False, "status": 403,
                                  "error": "HTTP 403"})
        o = Opener(fail_first=1)
        self.assertTrue(R.dispatch("o/r", "tok", [("collector", "k", "w")], "1:x", opener=o)[0]["ok"])   # one retry
        o = Opener(fail_first=5)
        res = R.dispatch("o/r", "tok", [("collector", "k", "w")], "1:x", opener=o)
        self.assertFalse(res[0]["ok"])
        self.assertEqual(len(o.calls), 2)                                                               # bounded

    def test_unavailable_actions_api_dispatches_nothing(self):
        o = Opener(list_status=503)
        with self.assertRaises(RuntimeError):
            R.list_runs("o/r", "tok", opener=o)
        self.assertFalse(any(m == "POST" for m, _, _ in o.calls))

    def test_cli_without_a_token_refuses(self):
        env = {k: v for k, v in os.environ.items() if k not in ("GITHUB_TOKEN",)}
        r = subprocess.run([sys.executable, str(ROOT / "recovery.py"), "dispatch"], env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


class YieldAndProvenanceTests(unittest.TestCase):
    def test_recovery_collector_yields_when_its_slot_was_collected(self):
        with tempfile.TemporaryDirectory() as d:
            slot = t("2026-10-04T12:07:00Z")
            self.assertFalse(R.covered(d, slot))
            storage.append_unique(Path(d) / "data/runs/2026-10.jsonl",
                                  [{"t": int(slot.timestamp() * 1000) + 120_000, "mode": "routine", "trigger": "schedule"}],
                                  lambda r: r["t"])
            self.assertTrue(R.covered(d, slot))
            self.assertFalse(R.covered(d, slot + dt.timedelta(minutes=15)))

    def test_provenance_labels(self):
        bot = provenance.BOT
        self.assertEqual(provenance.source({"GITHUB_EVENT_NAME": "schedule"}), "native-schedule")
        self.assertEqual(provenance.source({"GITHUB_EVENT_NAME": "workflow_dispatch", "DESK_DISPATCH_TRIGGER": "recovery",
                                            "GITHUB_TRIGGERING_ACTOR": bot}), "recovery")
        # a person typing "recovery" is still a person
        self.assertEqual(provenance.source({"GITHUB_EVENT_NAME": "workflow_dispatch", "DESK_DISPATCH_TRIGGER": "recovery",
                                            "GITHUB_TRIGGERING_ACTOR": "mannoj93-spec"}), "human")
        rec = provenance.record({"GITHUB_EVENT_NAME": "workflow_dispatch", "DESK_DISPATCH_TRIGGER": "recovery",
                                 "GITHUB_TRIGGERING_ACTOR": "mannoj93-spec", "DESK_DISPATCH_SLOT": "s"})
        self.assertEqual((rec["source"], rec["declared"], rec["slot"]), ("human", "recovery", "s"))
        self.assertEqual(provenance.source({"GITHUB_EVENT_NAME": "workflow_run"}), "chained")
        self.assertEqual(R.origin_label({"GITHUB_EVENT_NAME": "workflow_dispatch", "DESK_DISPATCH_TRIGGER": "external",
                                         "GITHUB_RUN_ID": "9"}), "9:external")
        self.assertEqual(R.origin_label({"GITHUB_EVENT_NAME": "schedule", "GITHUB_RUN_ID": "9"}), "9:native-schedule")


M = 60_000


def rec(t_ms, source):
    trig = {"native-schedule": "schedule"}.get(source, "workflow_dispatch")
    r = {"t": t_ms, "mode": "routine", "runner": "github", "trigger": trig, "critical_ok": True, "errors": {},
         "series": {}, "snap": {"books_ok": 2, "books": 2}, "code_version": "test"}
    if source != "native-schedule":
        r["provenance"] = {"source": source}
    return r


class ServiceVersusNativeTests(unittest.TestCase):
    T = int(t("2026-10-04T00:07:00Z").timestamp() * 1000)

    def check(self, runs, now):
        with tempfile.TemporaryDirectory() as d:
            storage.append_unique(Path(d) / "data/runs/2026-10.jsonl", runs, lambda r: r["t"])
            return watchdog.check(d, now, 90)

    def test_recovery_keeps_service_but_never_hides_a_native_silence(self):
        runs = [rec(self.T, "native-schedule")] + [rec(self.T + i * 15 * M, "recovery") for i in range(1, 20)]
        res = self.check(runs, self.T + 19 * 15 * M + 5 * M)
        self.assertEqual(res[0], 0)
        self.assertIn("recovery dispatcher", res[1])
        self.assertTrue(any(w.startswith("native schedule silent") for w in res.warnings))
        self.assertTrue(any("recovered native gap" not in w for w in res.warnings))

    def test_a_persons_runs_never_count_as_service(self):
        runs = [rec(self.T, "native-schedule")] + [rec(self.T + i * 15 * M, "human") for i in range(1, 12)]
        res = self.check(runs, self.T + 12 * 15 * M)
        self.assertEqual(res[0], 1)
        self.assertIn("stale", res[1])

    def test_coverage_measures_and_counts_by_source(self):
        periods = [(0, Q, "")]
        a = self.T - 7 * M
        runs = [rec(self.T, "native-schedule"), rec(self.T + 15 * M + 3 * M, "recovery"), rec(self.T + 30 * M, "human"),
                rec(self.T + 75 * M, "recovery")]
        c = cadence.coverage(periods, runs, a, a + 2 * 60 * M)
        self.assertEqual(c["expected_slots"], 8)
        self.assertEqual(c["runs_by_source"], {"native-schedule": 1, "recovery": 2, "human": 1})
        self.assertEqual(c["automated_runs"], 3)
        self.assertEqual(c["intervals_with_automated_run"], 3)
        self.assertEqual(c["longest_automated_gap_min"], 57.0)

    def test_health_records_a_service_gap_separately_from_the_native_gap(self):
        import health as H
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "cadence.json").write_text(json.dumps({"periods": [{"from": "2026-09-23T16:06:13Z", "minutes": Q}]}))
            runs = [rec(self.T, "native-schedule"), rec(self.T + 15 * M, "recovery"), rec(self.T + 200 * M, "recovery")]
            storage.append_unique(base / "data/runs/2026-10.jsonl", runs, lambda r: r["t"])
            src = H.source(base, self.T + 210 * M, 90)
            self.assertEqual(src["state"], "stale")                      # native: silent for 210 min
            self.assertEqual(src["service"]["state"], "healthy")         # automated: last run 10 min ago
            self.assertEqual(len(src["service"]["gaps"]), 1)             # 15 -> 200 min stays visible
            self.assertEqual(src["coverage_24h"]["runs_by_source"], {"native-schedule": 1, "recovery": 2})
            kinds = [i["kind"] for i in H.incidents({"source": src, "decisions": {"range": {}, "ps1": {}}})]
            self.assertEqual(sorted(kinds), ["collector_gap", "service_gap"])   # native ongoing; service recovered


class WiringTests(unittest.TestCase):
    WF = ROOT / ".github/workflows"

    def test_targets_accept_recovery_inputs_and_name_runs_as_the_planner_expects(self):
        for key, (wf, name) in R.WORKFLOWS.items():
            text = (self.WF / wf).read_text()
            for inp in ("trigger:", "slot:", "origin:"):
                self.assertIn(f"      {inp}", text, f"{wf} {inp}")
            self.assertIn(f"run-name: ${{{{ inputs.trigger == 'recovery' && format('{name} recovery {{0}}', inputs.slot) || '' }}}}",
                          text)
            self.assertEqual(R.title(name, "K"), f"{name} recovery K")
            for env in ("DESK_DISPATCH_TRIGGER", "DESK_DISPATCH_SLOT", "DESK_DISPATCH_ORIGIN"):
                self.assertIn(env, text, f"{wf} {env}")

    def test_collector_recovery_has_its_own_group_and_yields(self):
        text = (self.WF / "collect.yml").read_text()
        self.assertIn("(inputs.trigger == 'recovery' && 'recovery')", text)
        self.assertIn("python recovery.py covered --slot", text)
        for step in ("Collect", "Record operational health", "Persist completed series and failure diagnostics"):
            block = text.split(f"- name: {step}\n", 1)[1].split("\n      - name:", 1)[0]
            self.assertIn("steps.yield.outputs.covered != 'true'", block, step)

    def test_dispatcher_permissions_are_minimal(self):
        text = (self.WF / "recovery.yml").read_text()
        perms = text.split("permissions:\n", 1)[1].split("\n\n", 1)[0].split("\n# ", 1)[0]
        self.assertEqual(re.findall(r"^  ([a-z-]+): (\w+)", perms, re.M), [("contents", "read"), ("actions", "write")])
        self.assertNotIn("DESK_DEPLOY_KEY", text)
        self.assertNotIn("commit_push", text)
        self.assertIn("cancel-in-progress: false", text)


class DispatcherMonitorTests(unittest.TestCase):
    def test_a_silent_dispatcher_is_reported_stale_and_an_unreachable_api_unknown(self):
        import health as H
        now = t("2026-10-04T13:00:00Z")
        def opener(req, timeout=None):
            runs = [{"event": "workflow_dispatch", "conclusion": "success", "created_at": "2026-10-04T12:00:00Z"}]
            return Resp(200, json.dumps({"workflow_runs": runs if "recovery.yml" in req.full_url else []}).encode())
        mon = H.monitors(now, "tok", "o/r", opener)
        self.assertEqual(mon["workflows"]["recovery.yml"]["state"], "stale")       # 60 min > 45
        self.assertEqual(mon["dispatcher_state"], "stale")
        def down(req, timeout=None):
            raise urllib.error.URLError("unreachable")
        self.assertEqual(H.monitors(now, "tok", "o/r", down)["dispatcher_state"], "unknown")


class AcceptanceCheckTests(unittest.TestCase):
    """scripts/service_acceptance.py: measured values against targets stated in advance; a partial window is pending."""
    def run_check(self, runs, now, rng=None, ps1=None):
        sys.path.insert(0, str(ROOT / "scripts"))
        import service_acceptance as A
        from unittest import mock
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / "cadence.json").write_text(json.dumps({"periods": [{"from": "2026-09-23T16:06:13Z", "minutes": Q}]}))
            storage.append_unique(base / "data/runs/2026-10.jsonl", runs, lambda r: r["t"])
            with mock.patch.object(A.health, "range_decisions", return_value=(rng or {}, {"scoring_backlog": {}})), \
                    mock.patch.object(A.health, "ps1_decisions", return_value=(ps1 or {}, {})):
                return A.measure(base, t("2026-10-05T00:00:00Z"), t("2026-10-06T00:00:00Z"), t(now))

    def test_full_automated_day_passes_and_partial_window_is_pending(self):
        T = int(t("2026-10-05T00:07:00Z").timestamp() * 1000)
        runs = [rec(T + i * 15 * M + 60_000, "recovery" if i % 3 else "native-schedule") for i in range(96)]
        dec = {f"2026-10-05T{h:02d}:00:00Z": "published" for h in range(0, 24, 4)}
        ps1 = {k: "executed" for k in dec}
        doc = self.run_check(runs, "2026-10-06T00:05:00Z", dec, ps1)
        self.assertEqual(doc["verdict"], "pass", doc["checks"])
        self.assertEqual(doc["collection"]["runs_by_source"], {"native-schedule": 32, "recovery": 64})
        self.assertEqual(self.run_check(runs[:40], "2026-10-05T10:00:00Z", dec, ps1)["verdict"], "pending")

    def test_a_gap_a_missed_decision_or_a_persons_run_fails(self):
        T = int(t("2026-10-05T00:07:00Z").timestamp() * 1000)
        runs = [rec(T + i * 15 * M + 60_000, "recovery") for i in range(96) if not 40 <= i < 44]
        doc = self.run_check(runs, "2026-10-06T00:05:00Z", {"2026-10-05T04:00:00Z": "missed: skipped"})
        self.assertEqual(doc["verdict"], "fail")
        self.assertFalse(doc["checks"]["longest_automated_gap"])
        self.assertFalse(doc["checks"]["range_decisions_published"])
        runs = [rec(T + i * 15 * M + 60_000, "recovery") for i in range(96)] + [rec(T + 5 * M, "human")]
        self.assertFalse(self.run_check(runs, "2026-10-06T00:05:00Z")["checks"]["no_person_started_runs"])


class ChainTests(unittest.TestCase):
    """2.25.1: production showed no workflow_run event after a token-dispatched range run (Oct 4 20:47Z), so a
    recovery range run dispatches the streams itself."""
    def test_range_workflow_chains_streams_only_for_recovery_runs(self):
        text = (ROOT / ".github/workflows/range.yml").read_text()
        self.assertIn("  actions: write", text.split("jobs:", 1)[0])
        step = text.split("- name: Start the research streams for this decision (recovery runs only)\n", 1)[1].split("\n      - name:", 1)[0]
        self.assertIn("if: always() && inputs.trigger == 'recovery'", step)
        self.assertIn('python recovery.py chain --slot "$DESK_DISPATCH_SLOT"', step)

    def test_chain_dispatches_streams_with_recovery_inputs(self):
        o = Opener()
        res = R.dispatch("o/r", "tok", [("streams", "2026-10-04T20:00:00Z", "chained")], "9:range-recovery", opener=o)
        self.assertTrue(res[0]["ok"])
        _, url, data = o.calls[0]
        self.assertTrue(url.endswith("/actions/workflows/research-streams.yml/dispatches"))
        self.assertEqual(json.loads(data)["inputs"], {"trigger": "recovery", "slot": "2026-10-04T20:00:00Z",
                                                      "origin": "9:range-recovery"})


if __name__ == "__main__":
    unittest.main()
