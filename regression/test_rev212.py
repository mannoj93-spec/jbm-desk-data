"""Regressions for revision 2.12, reviewed at commit b4db7d0 (2.11 / lab-2.2).

  1  an evaluation whose required input integrity fails (or is incomplete) publishes no checkpoint,
     verdict, frozen decision, watermark or skill proposal - in the lab and again at the merge
                                                   BoundaryTests, RecoveryTests, FailureModeTests,
                                                   PublicationGateTests
  2  merge equality is canonical JSON: formatting never conflicts, real differences always do
                                                   CanonicalMergeTests

The end-to-end tests drive the REAL pipeline: lab.run.main (argument parsing, registration,
controls.apply with stored selections, experiments.run_design with its checkpoint evaluation and
verification, evidence cards, reports and proposals, the run-state watermark) on a disposable
repository, then the persist job's merge (scripts/merge_research.py) from a copy of the compute
outputs into that repository, exactly as .github/workflows/research.yml hands them over. Only the
inputs are synthetic: the design file, a module that turns a fixed list of observations into
candidates for controls.apply, and outcome labels / baseline features given by functions. The
verdict, the integrity result, checkpoint verification and proposal eligibility are never
patched. Tests named `*_common_api` use only interfaces present in 2.11 and fail on b4db7d0;
`*_preserved` tests use the same interfaces and pass on both (behaviour that must not change: a
valid run still reaches a supported 100/20 checkpoint, the stored winner of a competing writer is
what labels, baseline and checkpoint reference rows use, real differences still conflict).
"""
import copy
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from lab import controls, evidence, experiments, outcomes
from lab import run as run_mod
from lab.common import H, MINUTE

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_rev29 as r29                                    # noqa: E402  (mk, design, Harness, scenario)
from publication_fixture import batch_metadata             # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import merge_research                                      # noqa: E402

T0, DAY = r29.T0, r29.DAY
NEW = hasattr(experiments, "input_integrity")
new_only = unittest.skipUnless(NEW, "2.12 interface")
DID, VER = "C9-synthetic", "ev-rev212test"
KEY = f"{DID}@{VER}"
MOD = "lab_rev212_synthetic_module"
ARTIFACT = ("research/v2", "research/evidence/v2", "research/evidence/index.json", "reports/research.md",
            "reports/skill_proposals.md", "state/lab_registrations.json", "state/lab_run_state.json")


def the_design(module="liq_exposure"):
    d = r29.design(min_n=100, blocks=20, did=DID, version=VER)       # the normal 100 / 20 minimums
    d["module"] = module
    return d


class World:
    """Fixed synthetic observations: 160 long test decisions every 6 h from T0+1h, controls every
    2 h; `noise(i)` sets the first 100 test outcomes (tests 100+ are +2%)."""
    def __init__(self, noise=lambda i: 0.01):
        self.tests = [r29.mk(T0 + i * 6 * H + H, 1, "test") for i in range(160)]
        self.ctimes = [T0 + day * DAY + hh * H for day in range(-5, 45) for hh in range(0, 24, 2)]
        idx = {e["t_available"]: i for i, e in enumerate(self.tests)}
        self.tamper = None
        self.variants = None                     # override the design's variants (error-path tests)

        def y(t, d, h):
            k = (t // H) % 5
            if t in idx:
                return (noise(idx[t]) if idx[t] < 100 else 0.02) + 0.0003 * k
            return (-0.001 + 0.0001 * k) if d > 0 else (-0.001 - 0.0001 * k)
        self.harness = r29.Harness(".", None, y)

    def module(self):
        world = self

        def run(lab, params):
            if params.get("raise"):
                raise RuntimeError("synthetic failure in a later variant")
            now = lab.now
            cands = [controls.candidate(str(t), t, t, t, (lambda avail, t=t: r29.mk(t, 1, "control", avail)))
                     for t in world.ctimes if t <= now]
            ctl, diag = controls.apply(lab, cands, T0 - 5 * DAY)
            if world.tamper:
                ctl = world.tamper(ctl)
            return {"passes": [{"basis": "prospective", "events": [dict(e) for e in world.tests if e["t_available"] <= now],
                                "controls": ctl, "bars": {now - MINUTE: {}}, "coverage": {"comparison": diag},
                                "state": "available", "reasons": []}]}
        return types.SimpleNamespace(ID=DID, VERSION="synthetic-1", run=run)


def stored_record(t, t_persisted):
    """A stored selection exactly as controls.apply writes one."""
    avail = t + MINUTE
    rec = r29.mk(t, 1, "control", avail)
    rec.update(control_policy=controls.POLICY, control_hour=t // H * H, control_key=str(t), t_persisted=t_persisted,
               hour_closed_at_selection=True, hour_closed_at_previous_run=False)
    return rec


def seed_controls(repo, world, upto, skip=(), extra=()):
    """Valid stored selections (persisted 5 minutes after their decision) for every control whose
    persistence falls by `upto`, as an hourly lab would have left them; plus `extra` records."""
    d = the_design()
    have = controls.load_selections(repo, d)
    recs = [stored_record(t, t + MINUTE + 5 * MINUTE) for t in world.ctimes
            if t + 6 * MINUTE <= upto and t // H * H not in have and t not in skip]
    controls.persist_selections(repo, d, recs + list(extra))


def new_repo(tmp):
    repo = Path(tmp, "repo")
    (repo / "state").mkdir(parents=True)
    (repo / "state/lab_registrations.json").write_text(json.dumps(
        {KEY: {"design": DID, "version": VER, "registered": T0 - DAY, "design_sha256": "x", "components": {},
               "lab_version": "synthetic"}}))
    return repo


def lab_run(base, now, world, module="liq_exposure", args=("--write-past",)):
    """lab.run.main on `base` at cutoff `now`, as the research workflow runs it (stdout = summary)."""
    def load(p):
        d = the_design(module)
        if world.variants:
            d["variants"] = world.variants
        return d
    with patch.dict(run_mod.MODULES, {module: MOD}), patch.dict(sys.modules, {MOD: world.module()}), \
            patch.object(experiments, "design_files", lambda base: [Path("lab/designs/synthetic.json")]), \
            patch.object(experiments, "load_design", load), \
            patch.object(experiments, "attach_version", lambda base, d: d), \
            patch.object(outcomes, "label", world.harness.label), \
            patch.object(experiments, "features_at", lambda bars, kf, t, d: r29.feats(t, d)), \
            patch("sys.stdout", io.StringIO()) as out, patch("sys.stderr", io.StringIO()) as err:
        rc = run_mod.main(["update", "--base", str(base), "--now", str(now), *args])
    return rc, out.getvalue(), err.getvalue()


def compute(tmp, repo, now, world, tag, module="liq_exposure"):
    """The compute job: a checkout copy, the lab, and the artifact handed to the persist job."""
    work = Path(tmp, f"compute-{tag}")
    shutil.copytree(repo, work)
    rc, out, err = lab_run(work, now, world, module)
    inc = Path(tmp, f"incoming-{tag}")
    inc.mkdir()
    for rel in ARTIFACT:
        src = work / rel
        if src.is_dir():
            shutil.copytree(src, inc / rel)
        elif src.exists():
            (inc / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, inc / rel)
    (inc / "lab-summary.json").write_text(out)
    return rc, err, inc


def merge(inc, repo):
    with patch("sys.stdout", io.StringIO()), patch("sys.stderr", io.StringIO()) as err:
        rc = merge_research.main(inc, repo)
    return rc, err.getvalue()


def publish(tmp, repo, now, world, tag, module="liq_exposure"):
    rc, err, inc = compute(tmp, repo, now, world, tag, module)
    mrc, merr = merge(inc, repo)
    return rc, err, inc, mrc, merr


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in Path(root).rglob("*") if p.is_file()}


def card_of(repo):
    p = Path(repo, f"research/evidence/v2/{KEY}.json")
    return json.loads(p.read_text()) if p.exists() else None


def cps_of(repo):
    return experiments.load_checkpoints(repo, the_design())


def watermark(repo):
    p = Path(repo, "state/lab_run_state.json")
    return (json.loads(p.read_text()).get(KEY) or {}).get("last_cutoff") if p.exists() else None


class BoundaryTests(unittest.TestCase):
    """The review's reproduction: a stored control persisted 1 ms before its own decision, at the run
    where checkpoint 1 (n = 100, 20 blocks) would complete as supported."""
    NOW_A, NOW_B = T0 + 400 * H, T0 + 700 * H

    def scenario(self, tmp, malformed=True):
        world = World()
        repo = new_repo(tmp)
        seed_controls(repo, world, self.NOW_A - H)
        a = publish(tmp, repo, self.NOW_A, world, "a")                    # valid run: look 1 pending
        bad_t = T0 + 500 * H                                             # an even hour inside (A, B]
        extra = [dict(stored_record(bad_t, bad_t + MINUTE), t_persisted=bad_t + MINUTE - 1)] if malformed else []
        seed_controls(repo, world, self.NOW_B - H, skip=(bad_t,), extra=extra)
        return world, repo, a

    def test_competing_writer_winner_is_what_the_checkpoint_uses_preserved(self):
        """Another writer stored hour 20:00 from a later observation (:20); this run's own candidate
        (:00) loses. The recorded checkpoint's reference rows, the labels and the baseline all use the
        stored winner."""
        with tempfile.TemporaryDirectory() as tmp:
            world = World()
            repo = new_repo(tmp)
            seed_controls(repo, world, self.NOW_A - H)
            publish(tmp, repo, self.NOW_A, world, "a")
            t = T0 + 520 * H
            win = r29.mk(t + 20 * MINUTE, 1, "control", t + 21 * MINUTE)
            win.update(control_policy=controls.POLICY, control_hour=t, control_key=str(t + 20 * MINUTE),
                       t_persisted=t + 26 * MINUTE, hour_closed_at_selection=True, hour_closed_at_previous_run=False)
            other = controls.load_selections(repo, the_design())
            self.assertNotIn(t, other)
            controls.persist_selections(repo, the_design(), [win])
            seed_controls(repo, world, self.NOW_B - H)
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual((rc, mrc), (0, 0), err + merr)
            rec = cps_of(repo)[1]
            stored = controls.load_selections(repo, the_design())
            self.assertEqual(stored[t]["t_event"], t + 20 * MINUTE)
            ref_times = {r["t_event"] for r in rec["manifest"]["reference"]}
            self.assertIn(t + 20 * MINUTE, ref_times)                     # the winner, not the :00 proposal
            self.assertNotIn(t, ref_times)
            by_t = {s_["t_event"]: s_ for s_ in stored.values()}
            for r in rec["manifest"]["reference"]:                       # every reference row is a stored record,
                self.assertIn(r["t_event"], by_t)                        # known only once it was stored
                self.assertGreaterEqual(r["known_at"], by_t[r["t_event"]]["t_persisted"])
            if NEW:
                agree = card_of(repo)["research_integrity"]["evidence_agreement"]
                self.assertEqual(agree["mismatches"], [])
                self.assertGreater(agree["checked"], 300)

    def test_valid_control_run_does_reach_a_supported_checkpoint_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:            # the fixture is real: without the bad record
            world, repo, a = self.scenario(tmp, malformed=False)
            self.assertEqual((a[0], a[3]), (0, 0), a[1] + a[4])
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual((rc, mrc), (0, 0), err + merr)
            rec = cps_of(repo)[1]
            self.assertEqual((rec["n"], rec["verdict"]), (100, "supported"))
            self.assertTrue(experiments.verify_checkpoint(rec, the_design()))
            self.assertIn(f"## {DID} @ {VER}", Path(repo, "reports/skill_proposals.md").read_text())

    def test_integrity_failure_at_the_boundary_publishes_nothing_it_would_have_promoted_common_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            world, repo, a = self.scenario(tmp)
            self.assertEqual((a[0], a[3]), (0, 0), a[1] + a[4])
            before_ckpt = Path(repo, f"research/v2/{DID}/{VER}/checkpoints.jsonl")
            self.assertFalse(before_ckpt.exists())
            events_before = {k: v for k, v in snapshot(repo).items() if "/events/" in k or "/outcomes/" in k}
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual(rc, 1)                                             # the lab reports the failure
            self.assertIn("RESEARCH INTEGRITY FAILURE", err)
            # nothing promoted, anywhere: lab output and published repository
            for root in (inc, repo):
                self.assertEqual(experiments.load_checkpoints(root, the_design()), {}, root)   # 2.11: look 1 supported
                card = card_of(root)
                self.assertNotEqual(card["status"], "supported")                              # 2.11: supported
                self.assertNotIn(f"## {DID} @ {VER}", Path(root, "reports/skill_proposals.md").read_text())
            self.assertEqual(watermark(repo), self.NOW_A)                                     # 2.11: advanced to B
            self.assertEqual({k: v for k, v in snapshot(repo).items() if "/events/" in k or "/outcomes/" in k},
                             events_before)                                                    # nothing frozen by B
            # the stored records are never rewritten: the malformed one stays, withheld
            bad = controls.load_selections(repo, the_design())[T0 + 500 * H]
            self.assertEqual(bad["t_persisted"], bad["t_available"] - 1)
            if NEW:
                self.assertEqual(mrc, 0, merr)                                  # the blocked diagnostics publish
                card = card_of(repo)
                self.assertEqual(card["status"], "blocked")
                self.assertIn("research integrity failed", card["status_reason"])
                self.assertIn("persisted before its own decision", card["status_reason"])
                self.assertEqual(card["research_integrity"]["status"], "failed")
                self.assertFalse(card["publication"]["evaluation_valid"])
                self.assertFalse(card["publication"]["proposal_eligible"])
                self.assertEqual(card["attempt"]["cutoff_ms"], self.NOW_B)
                self.assertEqual(card["last_valid_result"]["cutoff_ms"], self.NOW_A)          # last valid kept
                self.assertEqual(card["last_valid_result"]["status"], "under prospective evaluation")
                summ = json.loads(Path(inc, "lab-summary.json").read_text())["designs"][DID]
                self.assertEqual((summ["version"], summ["cutoff_ms"], summ["validation"]["status"]),
                                 (VER, self.NOW_B, "failed"))
                self.assertTrue(any("persisted before its own decision" in r for r in summ["validation"]["reasons"]))
                text = Path(repo, "reports/research.md").read_text()
                self.assertIn("LATEST ATTEMPT BLOCKED", text)
                self.assertIn("| FAILED | BLOCKED |", text)
                self.assertIn("proposal suppressed", Path(repo, "reports/skill_proposals.md").read_text())
                idx = json.loads(Path(repo, "research/evidence/index.json").read_text())["designs"][DID]["versions"][VER]
                self.assertEqual((idx["status"], idx["evaluation_valid"]), ("blocked", False))

    @new_only
    def test_a_tampered_handoff_cannot_publish_the_promotion(self):
        """Defence in depth: the 2.11 outputs of the same run (supported look, supported card,
        proposal, advanced watermark) injected into the 2.12 artifact are refused whole."""
        with tempfile.TemporaryDirectory() as tmp:
            world, repo, _ = self.scenario(tmp)
            rc, err, inc = compute(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual(rc, 1)
            with tempfile.TemporaryDirectory() as tmp2:                 # the same run without the bad record
                w2, repo2, _ = self.scenario(tmp2, malformed=False)
                _, _, good = compute(tmp2, repo2, self.NOW_B, w2, "b")
                rel = f"research/v2/{DID}/{VER}/checkpoints.jsonl"
                supported_row = Path(good, rel).read_text()
                good_card = Path(good, f"research/evidence/v2/{KEY}.json").read_text()
                good_props = Path(good, "reports/skill_proposals.md").read_text()
            before = snapshot(repo)
            for name, mutate in (
                    ("checkpoint", lambda d: Path(d, rel).write_text(supported_row)),
                    ("card", lambda d: Path(d, f"research/evidence/v2/{KEY}.json").write_text(good_card)),
                    ("proposal", lambda d: Path(d, "reports/skill_proposals.md").write_text(good_props)),
                    ("watermark", lambda d: Path(d, "state/lab_run_state.json").write_text(
                        json.dumps({KEY: {"last_cutoff": self.NOW_B, "runs": 2}})))):
                d = Path(tmp, f"tampered-{name}")
                shutil.copytree(inc, d)
                mutate(d)
                mrc, merr = merge(d, repo)
                self.assertEqual(mrc, 4, name)
                self.assertIn("PUBLICATION BLOCKED", merr)
                self.assertEqual(snapshot(repo), before, name)             # no partial mutation


class RecoveryTests(unittest.TestCase):
    """Look 1 (n=100) is recorded as not_met; at look 2 (n=150) a stored winner persisted after the
    cutoff blocks the run; a later valid run completes look 2 from the same observations."""
    NOW_A, NOW_B, NOW_C = T0 + 700 * H, T0 + 1000 * H, T0 + 1003 * H

    def test_a_later_valid_retry_completes_the_unconsumed_look_common_api(self):
        world = World(noise=lambda i: 0.0005 + 0.008 * (1 if (i // 4) % 2 else -1))
        with tempfile.TemporaryDirectory() as tmp:
            repo = new_repo(tmp)
            seed_controls(repo, world, self.NOW_A - H)
            rc, err, _, mrc, merr = publish(tmp, repo, self.NOW_A, world, "a")
            self.assertEqual((rc, mrc), (0, 0), err + merr)
            path = Path(repo, f"research/v2/{DID}/{VER}/checkpoints.jsonl")
            look1 = path.read_bytes()
            self.assertEqual([(r["look"], r["verdict"]) for r in cps_of(repo).values()], [(1, "not_met")])
            fut_t = T0 + 900 * H
            winner = stored_record(fut_t, self.NOW_B + 2 * H)            # a concurrent writer's later clock
            seed_controls(repo, world, self.NOW_B - H, skip=(fut_t,), extra=[winner])
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual(rc, 1)
            self.assertEqual(path.read_bytes(), look1)                          # 2.11: look 2 recorded here
            self.assertNotIn(2, experiments.load_checkpoints(inc, the_design()))
            self.assertEqual(watermark(repo), self.NOW_A)                       # 2.11: advanced to B
            seed_controls(repo, world, self.NOW_C - H)
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_C, world, "c")
            self.assertEqual((rc, mrc), (0, 0), err + merr)
            self.assertTrue(path.read_bytes().startswith(look1))                # history byte-identical
            recs = cps_of(repo)
            self.assertEqual([(k, r["verdict"]) for k, r in sorted(recs.items())], [(1, "not_met"), (2, "supported")])
            self.assertEqual(recs[2]["completed_at"], self.NOW_C)
            self.assertTrue(experiments.verify_checkpoint(recs[2], the_design()))
            self.assertEqual(watermark(repo), self.NOW_C)
            exp = [json.loads(l) for p in sorted(Path(repo, "research/v2/experiments").glob("*.jsonl"))
                   for l in p.read_text().splitlines()]
            audit = [r for r in exp if r["t"] == self.NOW_C][0]["variants"][0]["passes"][0]["freeze_audit"]
            self.assertEqual(audit["late_replay"], 0)        # the tests B saw are new at C, not late replays
            seen_by_b = [e for e in world.tests if self.NOW_A < e["t_available"] <= self.NOW_B]
            self.assertEqual(audit["new"], len([e for e in world.tests if self.NOW_A < e["t_available"] <= self.NOW_C]))
            self.assertGreater(len(seen_by_b), 30)      # decisions B computed but, blocked, did not freeze
            self.assertIn(f"## {DID} @ {VER}", Path(repo, "reports/skill_proposals.md").read_text())


class FailureModeTests(unittest.TestCase):
    """Each required-integrity failure blocks the evaluation through lab.run.main."""
    NOW_A, NOW_B = T0 + 400 * H, T0 + 700 * H

    def run_b(self, extra=(), skip=(), tamper=None, module="liq_exposure"):
        world = World()
        with tempfile.TemporaryDirectory() as tmp:
            repo = new_repo(tmp)
            seed_controls(repo, world, self.NOW_A - H)
            publish(tmp, repo, self.NOW_A, world, "a", module)
            seed_controls(repo, world, self.NOW_B - H, skip=skip, extra=extra)
            world.tamper = tamper
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b", module)
            return rc, err, card_of(repo), cps_of(repo), json.loads(Path(inc, "lab-summary.json").read_text()), mrc, merr

    def test_malformed_timing_fields_block_common_api(self):
        t = T0 + 500 * H
        for field, value in (("t_inputs", None), ("t_available", str(t + MINUTE)), ("t_event", t + 5 * H)):
            rec = dict(stored_record(t, t + 6 * MINUTE), **{field: value})
            rc, err, card, cps, summ, mrc, merr = self.run_b(extra=[rec], skip=(t,))
            self.assertEqual(rc, 1, field)
            self.assertEqual(cps, {}, field)
            self.assertNotEqual(card["status"], "supported", field)
            if NEW:
                self.assertEqual(card["research_integrity"]["status"], "failed", field)
                self.assertIn("malformed", card["status_reason"], field)

    def test_a_future_persisted_winner_blocks_common_api(self):
        t = T0 + 500 * H
        rc, err, card, cps, summ, mrc, merr = self.run_b(extra=[stored_record(t, self.NOW_B + H)], skip=(t,))
        self.assertEqual(rc, 1)
        self.assertEqual(cps, {})
        self.assertNotEqual(card["status"], "supported")
        if NEW:
            self.assertIn("persisted after this cutoff", card["status_reason"])

    def test_labelled_controls_that_differ_from_the_stored_winners_block_common_api(self):
        def tamper(ctl):                        # a module that alters a control after selection
            out = [dict(c) for c in ctl]
            out[3]["features"] = {"severity": 7.0}
            return out
        rc, err, card, cps, summ, mrc, merr = self.run_b(tamper=tamper)
        self.assertEqual(rc, 1)
        self.assertEqual(cps, {})
        self.assertNotEqual(card["status"], "supported")
        if NEW:
            self.assertIn("is not the selection it came from", card["status_reason"])
            self.assertEqual(len(summ["designs"][DID]["integrity"]["evidence_agreement"]["mismatches"]), 1)

    @new_only
    def test_missing_required_validation_blocks(self):
        def drop(ctl):
            return ctl
        world = World()
        mod = world.module()
        orig = mod.run

        def no_diag(lab, params):                 # a hourly-control design that reports no diagnostics
            out = orig(lab, params)
            out["passes"][0]["coverage"] = {}
            return out
        mod.run = no_diag
        with tempfile.TemporaryDirectory() as tmp:
            repo = new_repo(tmp)
            seed_controls(repo, world, self.NOW_B - H)
            with patch.object(World, "module", lambda self: mod):
                rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual(rc, 1)
            card = card_of(repo)
            self.assertEqual(card["research_integrity"]["status"], "incomplete")
            self.assertEqual(card["status"], "blocked")
            self.assertEqual(cps_of(repo), {})

    @new_only
    def test_bar_based_designs_are_not_required_to_have_hourly_controls(self):
        world = World()
        with tempfile.TemporaryDirectory() as tmp:
            repo = new_repo(tmp)
            mod = world.module()

            def bar_based(lab, params):          # controls at bar closes, no collection-time policy
                out = {"passes": [{"basis": "prospective",
                                   "events": [dict(e) for e in world.tests if e["t_available"] <= lab.now],
                                   "controls": [r29.mk(t, 1, "control") for t in world.ctimes if t + MINUTE <= lab.now],
                                   "bars": {lab.now - MINUTE: {}}, "coverage": {}, "state": "available", "reasons": []}]}
                return out
            mod.run = bar_based
            with patch.object(World, "module", lambda self: mod):
                rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b", module="flow_absorption")
            self.assertEqual((rc, mrc), (0, 0), err + merr)
            card = card_of(repo)
            self.assertEqual(card["research_integrity"]["status"], "not_required")
            self.assertTrue(card["publication"]["evaluation_valid"])
            self.assertIn(1, cps_of(repo))                                  # evaluated as before


class PublicationGateTests(unittest.TestCase):
    """The persist job refuses research outputs whose publication metadata is missing, stale or
    contradictory - before any mutation."""
    NOW = T0 + 700 * H

    def valid_batch(self, tmp):
        world = World()
        repo = new_repo(tmp)
        seed_controls(repo, world, self.NOW - H)
        rc, err, inc = compute(tmp, repo, self.NOW, world, "x")
        self.assertEqual(rc, 0, err)
        return repo, inc

    @new_only
    def test_missing_stale_or_contradictory_metadata_blocks_the_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, inc = self.valid_batch(tmp)
            before = snapshot(repo)
            summ = json.loads(Path(inc, "lab-summary.json").read_text())

            def with_summary(s):
                return lambda d: Path(d, "lab-summary.json").write_text(json.dumps(s))
            stale = copy.deepcopy(summ)
            stale["cutoff_ms"] -= 6 * H
            for e in stale["designs"].values():
                e["cutoff_ms"] = e["publication"]["cutoff_ms"] = stale["cutoff_ms"]
            no_integ = copy.deepcopy(summ)
            no_integ["designs"][DID]["integrity"] = None
            flipped = copy.deepcopy(summ)
            flipped["designs"][DID]["validation"]["status"] = "failed"
            flipped["designs"][DID]["integrity"]["status"] = "failed"
            flipped["designs"][DID]["publication"]["validation"]["status"] = "failed"
            other_version = copy.deepcopy(summ)
            other_version["designs"][DID]["version"] = "ev-other"
            other_version["designs"][DID]["publication"]["evaluation_version"] = "ev-other"
            cases = {"missing": lambda d: Path(d, "lab-summary.json").unlink(),
                     "unreadable": lambda d: Path(d, "lab-summary.json").write_text("not json"),
                     "old schema": with_summary(dict(summ, schema="lab_summary/1")),
                     "stale cutoff": with_summary(stale),
                     "missing required integrity": with_summary(no_integ),
                     "contradictory validation": with_summary(flipped),
                     "different version": with_summary(other_version)}
            for name, mutate in cases.items():
                d = Path(tmp, f"case-{name}")
                shutil.copytree(inc, d)
                mutate(d)
                mrc, merr = merge(d, repo)
                self.assertEqual(mrc, 4, name)
                self.assertEqual(snapshot(repo), before, name)
            mrc, merr = merge(inc, repo)                                  # the genuine batch publishes
            self.assertEqual(mrc, 0, merr)
            self.assertIn(1, cps_of(repo))


class CanonicalMergeTests(unittest.TestCase):
    REL = f"research/v2/{DID}/{VER}"
    WIN = {"control_policy": controls.POLICY, "control_hour": T0, "t_event": T0 + 20 * MINUTE,
           "features": {"a": 1, "b": {"x": [1, 2], "y": "s"}}, "t_persisted": T0 + H}

    def files(self, tmp, repo_lines, inc_lines, name="controls/2026-09.jsonl", summary=True):
        repo, inc = Path(tmp, "repo"), Path(tmp, "inc")
        for b, lines in ((repo, repo_lines), (inc, inc_lines)):
            p = b / self.REL / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("".join(l + "\n" for l in lines))
        if summary:
            batch_metadata(inc, T0 + 2 * H, {DID: VER})
        return repo, inc, repo / self.REL / name

    def test_equivalent_formatting_merges_without_duplicates_or_rewrites_common_api(self):
        compact = json.dumps(self.WIN, sort_keys=True, separators=(",", ":"))
        spaced = json.dumps(self.WIN, indent=None)                          # different whitespace
        reordered = json.dumps({"features": {"b": {"y": "s", "x": [1, 2]}, "a": 1}, "t_persisted": T0 + H,
                                "t_event": T0 + 20 * MINUTE, "control_hour": T0,
                                "control_policy": controls.POLICY})          # nested key order
        for inc_line in (spaced, reordered, " " + compact + "  "):
            with tempfile.TemporaryDirectory() as tmp:
                repo, inc, p = self.files(tmp, [compact], [inc_line])
                before = p.read_bytes()
                rc, err = merge(inc, repo)
                self.assertEqual(rc, 0, err)                               # 2.11: RECONCILIATION CONFLICT, exit 3
                self.assertEqual(p.read_bytes(), before)                   # original bytes, no duplicate

    def test_equivalent_checkpoint_records_merge_and_unkeyed_rows_are_not_duplicated_common_api(self):
        rec = {"look": 1, "design": DID, "version": VER, "verdict": "not_met", "completed_at": T0,
               "checks": {"blocks": {"ok": True, "value": 20}}}
        a = json.dumps(rec, sort_keys=True)
        b = json.dumps({"checks": {"blocks": {"value": 20, "ok": True}}, "verdict": "not_met", "look": 1,
                        "completed_at": T0, "version": VER, "design": DID}, separators=(", ", ": "))
        with tempfile.TemporaryDirectory() as tmp:
            repo, inc, p = self.files(tmp, [a], [b], name="checkpoints.jsonl")
            rc, err = merge(inc, repo)
            self.assertEqual(rc, 0, err)
            self.assertEqual(p.read_text(), a + "\n")
        with tempfile.TemporaryDirectory() as tmp:                         # unkeyed append-only log
            repo, inc = Path(tmp, "repo"), Path(tmp, "inc")
            for base, line in ((repo, '{"t":1,"x":{"a":1,"b":2}}'), (inc, '{"x": {"b": 2, "a": 1}, "t": 1}')):
                Path(base, "research/v2/ledger").mkdir(parents=True)
                Path(base, "research/v2/ledger/2026-09.jsonl").write_text(line + "\n")
            batch_metadata(inc, T0, {})
            self.assertEqual(merge(inc, repo)[0], 0)
            self.assertEqual(Path(repo, "research/v2/ledger/2026-09.jsonl").read_text(), '{"t":1,"x":{"a":1,"b":2}}\n')

    def test_real_differences_still_conflict_without_partial_mutation_preserved(self):
        compact = json.dumps(self.WIN, sort_keys=True)
        changes = {"value": dict(self.WIN, t_event=T0 + 10 * MINUTE),
                   "array order": dict(self.WIN, features={"a": 1, "b": {"x": [2, 1], "y": "s"}}),
                   "string vs number": dict(self.WIN, t_persisted=str(T0 + H)),
                   "int vs float": dict(self.WIN, t_persisted=float(T0 + H)),
                   "extra metadata": dict(self.WIN, note="x"),
                   "missing metadata": {k: v for k, v in self.WIN.items() if k != "t_persisted"}}
        for name, rec in changes.items():
            with tempfile.TemporaryDirectory() as tmp:
                repo, inc, p = self.files(tmp, [compact], [json.dumps(rec)])
                Path(inc, "research/evidence/v2/x.json").write_text('{"generated_at": "2099-01-01T00:00Z"}')
                before = snapshot(repo)
                rc, err = merge(inc, repo)
                self.assertEqual(rc, 3, name)
                self.assertIn("RECONCILIATION CONFLICT", err)
                self.assertEqual(snapshot(repo), before, name)

    def test_legacy_duplicates_are_tolerated_but_cannot_be_exploited_common_api(self):
        a = json.dumps(self.WIN, sort_keys=True)
        b = json.dumps(dict(self.WIN, t_event=T0 + 30 * MINUTE), sort_keys=True)      # legacy loser
        new_hour = json.dumps(dict(self.WIN, control_hour=T0 + H, t_event=T0 + H + MINUTE), sort_keys=True)
        cases = {"verbatim legacy file plus a new hour": ([a, b, new_hour], 0),
                 "reformatted legacy file": ([json.dumps(json.loads(a)), json.dumps(json.loads(b), indent=None), new_hour], 0),
                 "batch whose first record is the legacy loser": ([b, new_hour], 3),
                 "legacy order reversed": ([b, a, new_hour], 3),
                 "a new third record for the key": ([a, b, json.dumps(dict(self.WIN, t_event=T0 + 40 * MINUTE))], 3)}
        for name, (lines, want) in cases.items():
            with tempfile.TemporaryDirectory() as tmp:
                repo, inc, p = self.files(tmp, [a, b], lines)
                rc, err = merge(inc, repo)
                self.assertEqual(rc, want, f"{name}: {err}")
                if want == 0:
                    self.assertEqual(p.read_text(), a + "\n" + b + "\n" + new_hour + "\n", name)

    @new_only
    def test_one_batch_cannot_carry_two_records_for_one_key(self):
        a = json.dumps(dict(self.WIN, control_hour=T0 + 5 * H), sort_keys=True)
        b = json.dumps(dict(self.WIN, control_hour=T0 + 5 * H, t_event=T0 + 5 * H + 9), sort_keys=True)
        with tempfile.TemporaryDirectory() as tmp:
            repo, inc, p = self.files(tmp, [], [a, b])
            self.assertEqual(merge(inc, repo)[0], 3)



class ReviewGapTests(unittest.TestCase):
    """Cases raised by the adversarial review of the first 2.12 draft."""
    NOW_A, NOW_B = T0 + 400 * H, T0 + 700 * H

    def test_an_error_in_a_later_variant_leaves_nothing_of_the_evaluation_common_api(self):
        world = World()
        world.variants = [{"name": "v", "params": {}}, {"name": "w", "params": {"raise": True}}]
        with tempfile.TemporaryDirectory() as tmp:
            repo = new_repo(tmp)
            seed_controls(repo, world, self.NOW_B - H)
            rc, err, inc, mrc, merr = publish(tmp, repo, self.NOW_B, world, "b")
            self.assertEqual(rc, 1)
            for root in (Path(tmp, "compute-b"), repo):            # 2.11: supported look 1 + decisions stored
                self.assertEqual(experiments.load_checkpoints(root, the_design()), {}, root)
                self.assertEqual([k for k in snapshot(root) if "/events/" in k or "/outcomes/" in k], [], root)
            self.assertEqual(card_of(repo)["status"], "error")
            self.assertIsNone(watermark(repo))
            if NEW:
                self.assertEqual(mrc, 0, merr)                    # the error card still publishes

    @new_only
    def test_a_read_only_replay_fails_the_same_malformed_record_and_writes_its_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            world, repo, _ = BoundaryTests().scenario(tmp)
            before = snapshot(repo)
            path = Path(tmp, "summary.json")
            rc, out, err = lab_run(repo, self.NOW_B, world, args=("--summary", str(path)))    # no --write-past
            self.assertEqual(rc, 1)
            self.assertEqual(snapshot(repo), before)                     # read-only: nothing written
            self.assertEqual(path.read_text(), out)                      # --summary == stdout
            e = json.loads(out)["designs"][DID]
            self.assertEqual(e["validation"]["status"], "failed")
            self.assertFalse(e["publication"]["proposal_eligible"])
            self.assertEqual(e["status"], "blocked")

    @new_only
    def test_a_partial_artifact_cannot_leave_older_promotion_outputs_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            world, repo, _ = BoundaryTests().scenario(tmp)
            rc, err, inc = compute(tmp, repo, self.NOW_B, world, "b")
            before = snapshot(repo)
            for rel in ("reports/skill_proposals.md", "reports/research.md", "research/evidence/index.json",
                        f"research/evidence/v2/{KEY}.json"):
                d = Path(tmp, "partial-" + rel.replace("/", "_"))
                shutil.copytree(inc, d)
                Path(d, rel).unlink()
                mrc, merr = merge(d, repo)
                self.assertEqual(mrc, 4, rel)
                self.assertIn("missing from the batch", merr)
                self.assertEqual(snapshot(repo), before, rel)

    @new_only
    def test_controls_without_a_comparison_window_are_incomplete(self):
        lab = types.SimpleNamespace(write=False, control_context=None, base=".")
        ctl = dict(r29.mk(T0, 1, "control"), control_policy=controls.POLICY, control_hour=T0, group="control_long")
        p = {"coverage": {"comparison": {"policy": controls.POLICY, "window": None}}, "controls": [ctl]}
        got = experiments.input_integrity(lab, the_design(), p, [(ctl, {}, None)])
        self.assertEqual(got["status"], "incomplete")
        self.assertFalse(experiments.evaluation_allowed(got))
        p["controls"], empty = [], experiments.input_integrity(lab, the_design(), dict(p, controls=[]), [])
        self.assertEqual(empty["status"], "passed")                     # nothing to validate: no controls at all

    @new_only
    def test_unreadable_or_out_of_range_rows_block_with_a_named_reason(self):
        rel = f"research/v2/{DID}/{VER}/outcomes/2026-09.jsonl"
        for name, line in (("not json", "{oops"), ("not an object", "[1, 2]"), ("duplicate key", '{"a": 1, "a": 2}'),
                           ("overflow", '{"a": 1e400}')):
            with tempfile.TemporaryDirectory() as tmp:
                repo, inc = Path(tmp, "repo"), Path(tmp, "inc")
                repo.mkdir()
                batch_metadata(inc, T0, {DID: VER})
                Path(inc, rel).parent.mkdir(parents=True)
                Path(inc, rel).write_text(line + "\n")
                mrc, merr = merge(inc, repo)
                self.assertEqual(mrc, 4, name)
                self.assertIn("unreadable record", merr, name)
        self.assertNotEqual(merge_research.canon('{"a": 1.0}'), merge_research.canon('{"a": 1}'))
        self.assertNotEqual(merge_research.canon('{"a": -0.0}'), merge_research.canon('{"a": 0.0}'))
        self.assertNotEqual(merge_research.canon('{"a": true}'), merge_research.canon('{"a": 1}'))
        self.assertEqual(merge_research.canon('{"a": "\\u00e9"}'), merge_research.canon('{"a": "\u00e9"}'))


if __name__ == "__main__":
    unittest.main()
