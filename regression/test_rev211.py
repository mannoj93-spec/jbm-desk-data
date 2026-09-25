"""Regressions for revision 2.11: decision-time cutoffs and authoritative stored selections for the
hourly controls of modules B, C and F (lab/controls.py), reviewed at commit 8432df0 (2.10 / lab-2.2).

  1  a control is usable only once its DECISION (inputs + 60 s) is available by the cutoff; stored
     selections obey the same rule plus their persistence time          CutoffTests
  2  a writing run labels, trains and checkpoints with the STORED winner, not its own losing
     proposal; merges never publish evidence computed from a losing record  AuthorityTests
Tests named `*_common_api` drive only interfaces present in both versions (module.run,
persist_selections / load_selections, experiments.run_design) and fail on the reviewed code.
Concurrency is simulated by deterministic interleaving (context loaded, then another writer stores,
then this worker proposes). Write tests use temporary directories only.
"""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from lab import baseline as baseline_mod
from lab import controls, experiments
from lab.common import H, MINUTE
from lab.events import event_record
from lab.modules import liq_exposure, options_disagreement

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_rev210 as r210                                  # noqa: E402  (shared synthetic records)

ROOT = Path(__file__).resolve().parents[1]
T0, S = r210.T0, 1000
TEN = T0 + 10 * H
NEW = hasattr(controls, "ControlIntegrityError")
new_only = unittest.skipUnless(NEW, "2.11 interface")
MODS = {"liq_exposure": liq_exposure, "options_disagreement": options_disagreement}
DESIGN = {"id": "C1", "_version": "ev-t211"}


def run_module(module, runs, now, ctx=None, base=None, write=False, bars=None):
    lab = r210.lab_(runs, now, ctx, bars)
    lab.base, lab.write = base, write
    with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rr"]}), \
            patch.object(options_disagreement, "panel_quality", lambda rec: {"rr25_7d_quotes": "unknown"}):
        p = MODS[module].run(lab, r210.PARAMS[module])["passes"][0]
    return p["controls"], p["coverage"].get("comparison") or {}


def ctx_(frozen=None):
    return {"frozen": dict(frozen or {}), "last_cutoff": None, "new": [], "design": DESIGN}


def canon(r):
    return json.dumps(r, sort_keys=True)


class CutoffTests(unittest.TestCase):
    RUNS = [r210.run_(TEN - 90 * S, 60 * S)]                # source 09:58:30, inputs 09:59:30, decision 10:00:30

    def test_decision_after_cutoff_is_not_returned_common_api(self):
        for module in MODS:
            for now in (TEN, TEN + 30 * S - 1):                 # 10:00:00 and one millisecond before 10:00:30
                ctl, _ = run_module(module, self.RUNS, now)
                self.assertEqual(ctl, [], (module, now))        # 2.10: returned with a decision after the cutoff
            ctl, _ = run_module(module, self.RUNS, TEN + 30 * S)
            self.assertEqual([(c["control_hour"], c["t_available"]) for c in ctl], [(TEN - H, TEN + 30 * S)])
            ctl, _ = run_module(module, self.RUNS, TEN + 5 * MINUTE)
            self.assertEqual(len(ctl), 1)

    @new_only
    def test_pending_is_diagnosed_and_never_counted_as_selected_or_missing(self):
        _, d = run_module("liq_exposure", self.RUNS, TEN)
        self.assertEqual(d["pending_processing"], [[TEN - H, TEN + 30 * S]])
        self.assertEqual((d["pending_processing_closed_hours"], d["selected_closed"]), (1, 0))
        self.assertNotIn(TEN - H, dict(d["missing_closed_hours"]))
        self.assertEqual((d["closed_hours_with_candidates_but_no_control"], d["integrity_failures"]), ([], 0))

    def test_inputs_exactly_at_cutoff_are_pending_common_api(self):
        runs = [r210.run_(TEN - 60 * S, 60 * S)]                # inputs exactly 10:00:00
        self.assertEqual(run_module("options_disagreement", runs, TEN)[0], [])
        ctl, _ = run_module("options_disagreement", runs, TEN + 60 * S)
        self.assertEqual([c["control_hour"] for c in ctl], [TEN])

    def test_utc_midnight_keeps_the_input_hour_common_api(self):
        day = T0 + 24 * H
        runs = [r210.run_(day - 90 * S, 60 * S)]                # inputs 23:59:30, decision 00:00:30
        self.assertEqual(run_module("liq_exposure", runs, day)[0], [])
        ctl, _ = run_module("liq_exposure", runs, day + 30 * S)
        self.assertEqual((ctl[0]["t_inputs"] // H * H, ctl[0]["t_available"]), (day - H, day + 30 * S))

    @new_only
    def test_pending_becomes_selected_later_without_duplicates_or_new_hour(self):
        with tempfile.TemporaryDirectory() as base:
            c1 = ctx_()
            self.assertEqual(run_module("liq_exposure", self.RUNS, TEN, c1, base, True)[0], [])
            self.assertFalse(controls.controls_dir(base, DESIGN).exists())          # nothing frozen while pending
            c2 = ctx_(controls.load_selections(base, DESIGN))
            ctl, d = run_module("liq_exposure", self.RUNS, TEN + 5 * MINUTE, c2, base, True)
            self.assertEqual([c["control_hour"] for c in ctl], [TEN - H])
            self.assertEqual(d["proposals_accepted"], [TEN - H])
            f = controls.controls_dir(base, DESIGN) / "2026-09.jsonl"
            b1 = f.read_bytes()
            c3 = ctx_(controls.load_selections(base, DESIGN))
            ctl3, d3 = run_module("liq_exposure", self.RUNS, TEN + 2 * H, c3, base, True)
            self.assertEqual(f.read_bytes(), b1)
            self.assertEqual((canon(ctl3[0]), d3["proposals_accepted"]), (canon(ctl[0]), []))
            self.assertEqual(len(b1.splitlines()), 1)

    @new_only
    def test_stored_records_obey_the_same_cutoff_and_are_withheld_not_replaced(self):
        good, _ = run_module("liq_exposure", self.RUNS, TEN + 5 * MINUTE)
        rec = good[0]
        cases = {"t_persisted after cutoff (read-only, same identity -> provisional)": dict(rec, t_persisted=TEN + 3 * H),
                 "persisted before its own decision": dict(rec, t_persisted=TEN + 20 * S),
                 "missing t_available": {k: v for k, v in rec.items() if k != "t_available"},
                 "string time": dict(rec, t_inputs=str(rec["t_inputs"]))}
        for label, bad in cases.items():
            ctl, d = run_module("liq_exposure", self.RUNS, TEN + 5 * MINUTE, {"frozen": {TEN - H: bad}, "last_cutoff": None})
            if label.startswith("t_persisted after"):
                self.assertEqual(d["selection_states"], {"provisional": 1}, label)
                continue
            self.assertEqual(ctl, [], label)
            self.assertTrue(d["withheld_stored"], label)
            self.assertIsNot(ctl, bad)
        # a writing run with a winner persisted after its cutoff: withheld and an unresolved conflict
        with tempfile.TemporaryDirectory() as base:
            controls.persist_selections(base, DESIGN, [dict(rec, t_persisted=TEN + 3 * H)])
            ctl, d = run_module("liq_exposure", self.RUNS, TEN + 5 * MINUTE, ctx_(), base, True)
            self.assertEqual(ctl, [])
            self.assertEqual([h for h, _ in d["unresolved_conflicts"]], [TEN - H])
            self.assertGreaterEqual(d["integrity_failures"], 1)
            self.assertEqual(controls.load_selections(base, DESIGN)[TEN - H]["t_persisted"], TEN + 3 * H)   # untouched


def two_writers(base, stale=True):
    """Deterministic interleaving: worker B loads its (empty) context; writer A then stores the :20
    observation for 10:00; worker B then proposes the :10 observation (committed late)."""
    rec20, rec10 = r210.run_(TEN + 20 * MINUTE, 30 * S), r210.run_(TEN + 10 * MINUTE, 30 * S)
    ctx_b = ctx_()                                                           # B's snapshot: nothing stored
    run_module("liq_exposure", [rec20], TEN + 25 * MINUTE, ctx_(), base, True)   # writer A
    return rec10, rec20, ctx_b


class AuthorityTests(unittest.TestCase):
    def test_returned_control_is_the_stored_winner_common_api(self):
        with tempfile.TemporaryDirectory() as base:
            rec10, rec20, ctx_b = two_writers(base)
            ctl, _ = run_module("liq_exposure", [rec10, rec20], TEN + 40 * MINUTE, ctx_b, base, True)
            stored = controls.load_selections(base, DESIGN)
            self.assertEqual(stored[TEN]["t_event"], TEN + 20 * MINUTE)               # storage kept A
            self.assertEqual([canon(c) for c in ctl], [canon(stored[TEN])])          # 2.10 returned B's :10

    @new_only
    def test_context_diagnostics_and_repeated_calls_follow_the_winner(self):
        with tempfile.TemporaryDirectory() as base:
            rec10, rec20, ctx_b = two_writers(base)
            f = controls.controls_dir(base, DESIGN) / "2026-09.jsonl"
            b0 = f.read_bytes()
            ctl, d = run_module("liq_exposure", [rec10, rec20], TEN + 40 * MINUTE, ctx_b, base, True)
            self.assertEqual((d["proposals_accepted"], d["proposals_superseded"]), ([], [TEN]))
            self.assertTrue(d["used_equals_stored"])
            self.assertEqual(ctx_b["frozen"][TEN]["t_event"], TEN + 20 * MINUTE)     # refreshed context
            self.assertEqual(ctx_b["new"], [])                                        # not reported as newly frozen
            again, d2 = run_module("liq_exposure", [rec10, rec20], TEN + 50 * MINUTE, ctx_b, base, True)   # next variant
            self.assertEqual((canon(again[0]), d2["proposals_superseded"]), (canon(ctl[0]), []))
            stale = ctx_()                                                            # stale context again
            third, d3 = run_module("liq_exposure", [rec10, rec20], TEN + 55 * MINUTE, stale, base, True)
            self.assertEqual((canon(third[0]), d3["proposals_superseded"]), (canon(ctl[0]), [TEN]))
            self.assertEqual(f.read_bytes(), b0)                                      # winner metadata unchanged
            self.assertEqual(d["controls_fingerprint"], controls.fingerprint([controls.load_selections(base, DESIGN)[TEN]]))

    @new_only
    def test_multiple_proposals_accept_free_hours_and_yield_to_winners(self):
        with tempfile.TemporaryDirectory() as base:
            rec10, rec20, ctx_b = two_writers(base)
            others = [r210.run_(TEN + k * H + 20 * MINUTE, 30 * S) for k in (1, 2)]
            ctl, d = run_module("liq_exposure", [rec10, rec20] + others, TEN + 3 * H, ctx_b, base, True)
            self.assertEqual(d["proposals_superseded"], [TEN])
            self.assertEqual(d["proposals_accepted"], [TEN + H, TEN + 2 * H])
            stored = controls.load_selections(base, DESIGN)
            self.assertEqual([canon(c) for c in ctl], [canon(stored[h]) for h in sorted(stored)])

    @new_only
    def test_persistence_failure_fails_the_run_and_stores_nothing(self):
        with tempfile.TemporaryDirectory() as base:
            with patch.object(controls, "persist_selections", side_effect=OSError("disk full")):
                with self.assertRaises(OSError):
                    run_module("liq_exposure", [r210.run_(TEN + 20 * MINUTE)], TEN + H, ctx_(), base, True)
            self.assertFalse(controls.controls_dir(base, DESIGN).exists())
            with patch.object(controls, "persist_selections", return_value=0):          # write silently lost
                with self.assertRaises(controls.ControlIntegrityError):
                    run_module("liq_exposure", [r210.run_(TEN + 20 * MINUTE)], TEN + H, ctx_(), base, True)

    @new_only
    def test_the_writer_holds_the_scoped_lock_around_read_and_replace(self):
        calls = []
        real = controls.fcntl.flock
        with tempfile.TemporaryDirectory() as base, \
                patch.object(controls.fcntl, "flock", lambda fh, op: (calls.append(op), real(fh, op))), \
                patch.object(controls, "append_unique", lambda *a, **k: (calls.append("append"), 1)[1]):
            controls.persist_selections(base, DESIGN, [{"control_policy": controls.POLICY, "control_hour": TEN}])
        self.assertEqual(calls, [controls.fcntl.LOCK_EX, "append", controls.fcntl.LOCK_UN])

    @new_only
    def test_read_only_runs_never_write_and_mark_new_selections_provisional(self):
        with tempfile.TemporaryDirectory() as base:
            rec10, rec20, _ = two_writers(base)
            before = {p: p.read_bytes() for p in Path(base).rglob("*") if p.is_file()}
            ctl, d = run_module("liq_exposure", [rec10, rec20, r210.run_(TEN + H + 20 * MINUTE)], TEN + 2 * H + 5 * MINUTE,
                                {"frozen": controls.load_selections(base, DESIGN), "last_cutoff": None, "design": DESIGN},
                                base, write=False)
            self.assertEqual({p: p.read_bytes() for p in Path(base).rglob("*") if p.is_file()}, before)
            self.assertEqual(d["selection_states"], {"stored": 1, "provisional": 1})


class ReviewFindingTests(unittest.TestCase):
    """Low-severity findings of the adversarial review of the first 2.11 draft."""
    @new_only
    def test_future_and_nonexistent_hours_are_not_reported_as_withheld(self):
        runs = [r210.run_(TEN + k * H + 20 * MINUTE, 30 * S) for k in range(4)]
        later, _ = run_module("liq_exposure", runs, TEN + 4 * H)
        frozen = {c["control_hour"]: dict(c, t_persisted=TEN + 4 * H) for c in later}
        _, d = run_module("liq_exposure", runs[:2], TEN + H + 5 * MINUTE, {"frozen": frozen, "last_cutoff": None})
        self.assertEqual(d["withheld_stored"], [])            # 11:00-13:00 controls not reached at 11:05
        self.assertEqual(d["selection_states"], {"provisional": 1})
        # a closed hour with no record at this cutoff whose control was stored later: missing, not withheld
        early = [r210.run_(TEN - H + 20 * MINUTE, 30 * S)]
        _, d = run_module("liq_exposure", early, TEN + H + 5 * MINUTE, {"frozen": frozen, "last_cutoff": None})
        self.assertIn(TEN, dict(d["missing_closed_hours"]))
        self.assertNotIn(TEN, dict(d["withheld_stored"]))

    @new_only
    def test_a_stored_record_with_an_impossible_source_time_is_withheld(self):
        good, _ = run_module("liq_exposure", [r210.run_(TEN + 20 * MINUTE)], TEN + H)
        bad = dict(good[0], t_event=TEN + 5 * H)
        ctl, d = run_module("liq_exposure", [], TEN + H, {"frozen": {TEN: bad}, "last_cutoff": None})
        self.assertEqual(ctl, [])
        self.assertIn("malformed", dict(d.get("withheld_stored") or [[TEN, "malformed"]])[TEN])

    @new_only
    def test_merge_tolerates_a_legacy_duplicate_already_in_the_checkout(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import merge_research
        rel = f"research/v2/C1/{DESIGN['_version']}/checkpoints.jsonl"
        with tempfile.TemporaryDirectory() as inc, tempfile.TemporaryDirectory() as repo:
            for b_ in (inc, repo):
                Path(b_, rel).parent.mkdir(parents=True)
            Path(repo, rel).write_text('{"look":1,"v":"a"}\n{"look":1,"v":"b"}\n')
            Path(inc, rel).write_text('{"look":1,"v":"a"}\n{"look":1,"v":"b"}\n{"look":2,"v":"c"}\n')
            with patch("sys.stdout", io.StringIO()):
                self.assertEqual(merge_research.main(inc, repo), 0)


class FakeStore(r210.Store):
    def funding_known(self):
        return []

    def funding_events(self):
        return []


class EvaluationPathTests(unittest.TestCase):
    """The stored winner is what experiments.run_design labels, trains the baseline on and puts in
    the reference rows - checked on the lab's own label and summary objects."""
    def run_design(self, base, now, runs, ctx, bars):
        design = {"id": "C1", "version": 2, "module": "liq_exposure", "family": "C", "question": "q",
                  "variants": [{"name": "v", "params": r210.PARAMS["liq_exposure"]}], "primary_variant": "v",
                  "outcome": {"metric": "ret_net", "horizons_min": [60], "primary_horizon": 60},
                  "comparison": {"test_group": "long_cluster", "reference_group": "control", "hypothesised_sign": -1},
                  "collapse_ms": 0, "min_retained_observations": 100, "min_dependence_blocks": 20,
                  "_sha256": "x", "_file": "lab/designs/C1.json", "_version": DESIGN["_version"], "_components": {}}
        lab = type("L", (), {"now": now, "write": True, "base": Path(base), "code": "c", "control_context": ctx,
                             "store": FakeStore(runs, now, bars)})()
        captured = []
        orig = experiments.label_all

        def rec(*a, **k):
            out = orig(*a, **k)
            captured.append(out[0])
            return out
        with patch.object(experiments, "label_all", rec):
            res, _ = experiments.run_design(lab, design, liq_exposure, {"registered": T0 - H}, 1)
        return res, captured[0]

    def test_labels_baseline_and_reference_use_the_stored_winner_common_api(self):
        bars = {TEN + i * MINUTE: {"t": TEN + i * MINUTE, "o": 100.0 + (5.0 if i >= 15 else 0.0), "h": 106.0, "l": 99.0,
                                   "c": 100.0 + (5.0 if i >= 15 else 0.0), "tbv": 5.0, "v": 10.0,
                                   "avail": TEN + (i + 1) * MINUTE} for i in range(400)}
        with tempfile.TemporaryDirectory() as base:
            rec10, rec20, ctx_b = two_writers(base)
            res, labelled = self.run_design(base, TEN + 5 * H, [rec10, rec20], ctx_b, bars)
            winner = controls.load_selections(base, DESIGN)[TEN]
            ctl_rows = [(e, labs) for e, labs, _ in labelled if e["group"] == "control_long"]
            self.assertEqual([e["t_event"] for e, _ in ctl_rows], [TEN + 20 * MINUTE])      # 2.10: the :10 proposal
            entry = ctl_rows[0][1][60]["entry_t"]
            self.assertEqual(entry, -(-winner["t_available"] // MINUTE) * MINUTE)
            self.assertLess(abs(ctl_rows[0][1][60]["ret_net"]), 0.01)                      # :20 is after the jump
            bl = baseline_mod.build(labelled, [60])[60]
            self.assertTrue(all(r["entry_t"] == entry for r in bl.rows))
            ref = res["variants"][0]["passes"][0]["phases"]["evaluation"]["60"]["_ref"]
            self.assertEqual([r["entry_t"] for r in ref], [entry])
            if NEW:
                agree = controls.evidence_agreement(labelled, controls.load_selections(base, DESIGN))
                self.assertEqual((agree["checked"], agree["mismatches"]), (1, []))
                self.assertTrue(res["variants"][0]["passes"][0]["coverage"]["comparison"]["used_equals_stored"])


class MergeTests(unittest.TestCase):
    @new_only
    def test_merge_rejects_a_batch_computed_from_a_losing_selection(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import merge_research
        rel = f"research/v2/C1/{DESIGN['_version']}"
        win = {"control_policy": controls.POLICY, "control_hour": TEN, "t_event": TEN + 20 * MINUTE}
        lose = dict(win, t_event=TEN + 10 * MINUTE)
        with tempfile.TemporaryDirectory() as inc, tempfile.TemporaryDirectory() as repo:
            for b_, rec in ((repo, win), (inc, lose)):
                Path(b_, rel, "controls").mkdir(parents=True)
                Path(b_, rel, "controls", "2026-09.jsonl").write_text(json.dumps(rec, sort_keys=True) + "\n")
                Path(b_, "research/evidence/v2").mkdir(parents=True)
                Path(b_, "reports").mkdir()
            Path(repo, "research/evidence/v2/C1@x.json").write_text('{"generated_at": "2026-09-25T00:00Z", "v": "old"}')
            Path(inc, "research/evidence/v2/C1@x.json").write_text('{"generated_at": "2026-09-25T09:00Z", "v": "loser"}')
            Path(inc, rel, "checkpoints.jsonl").write_text('{"look":1,"verdict":"supported"}\n')
            Path(inc, "reports/research.md").write_text("Generated 2026-09-25 09:00Z loser\n")
            snap = {p: p.read_bytes() for p in Path(repo).rglob("*") if p.is_file()}
            with patch("sys.stdout", io.StringIO()), patch("sys.stderr", io.StringIO()) as err:
                self.assertEqual(merge_research.main(inc, repo), 3)
            self.assertIn("RECONCILIATION CONFLICT", err.getvalue())
            self.assertEqual({p: p.read_bytes() for p in Path(repo).rglob("*") if p.is_file()}, snap)
            Path(inc, rel, "controls", "2026-09.jsonl").write_text(json.dumps(win, sort_keys=True) + "\n")  # agrees
            with patch("sys.stdout", io.StringIO()):
                self.assertEqual(merge_research.main(inc, repo), 0)
            self.assertTrue(Path(repo, rel, "checkpoints.jsonl").exists())


class LabRunIntegrityTests(unittest.TestCase):
    @new_only
    def test_an_unresolved_conflict_fails_the_lab_run_and_is_reported(self):
        from lab import run as run_mod
        with tempfile.TemporaryDirectory() as base:
            Path(base, "lab/designs").mkdir(parents=True)
            Path(base, "lab/designs/C1-liquidation-cluster.json").write_bytes(
                (ROOT / "lab/designs/C1-liquidation-cluster.json").read_bytes())
            d = experiments.attach_version(base, experiments.load_design(Path(base, "lab/designs/C1-liquidation-cluster.json")))
            runs = [r210.run_(TEN + k * H + 20 * MINUTE, 30 * S) for k in range(3)]
            for sub, rows in (("data/hl_accounts", [a for a, _, _ in runs]), ("data/snap", [s for _, s, _ in runs])):
                Path(base, sub).mkdir(parents=True)
                Path(base, sub, "2026-09.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
            now = TEN + 3 * H
            probe, _ = run_module("liq_exposure", runs[:1], now)
            bad = dict(probe[0], t_persisted=now + H)                     # a winner stored "after" this cutoff
            controls.persist_selections(base, d, [bad])
            with patch("sys.stdout", io.StringIO()) as out, patch("sys.stderr", io.StringIO()) as err:
                rc = run_mod.main(["update", "--base", base, "--now", str(now), "--write-past"])
            self.assertEqual(rc, 1)
            self.assertIn("RESEARCH INTEGRITY FAILURE", err.getvalue())
            summary = json.loads(out.getvalue())
            self.assertFalse(summary["designs"]["C1-liquidation-cluster"]["integrity"]["ok"])
            self.assertIn("RESEARCH INTEGRITY FAILURE", Path(base, "reports/research.md").read_text())
            self.assertEqual(controls.load_selections(base, d)[TEN]["t_persisted"], now + H)     # not rewritten


if __name__ == "__main__":
    unittest.main()
