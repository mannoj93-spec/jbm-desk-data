"""Research-integrity regressions for lab-2.1 (CHANGELOG 2.9), reviewed code c9fff86 (2.8).

  1  a checkpoint verdict comes from a precisely bounded, recorded dataset   CheckpointTests
  2  options history features obey their own availability                   OptionsAvailabilityTests
  3  one baseline per outcome horizon                                       HorizonBaselineTests

Tests whose names end in `_common_api` drive only interfaces that exist in both 2.8 and 2.9
(experiments.run_design, options_disagreement.run, Baseline(...).predict) and fail on the reviewed
code; the others pin the new checkpoint/baseline interfaces. Offline; synthetic data only, in
temporary directories.
"""
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lab import evidence, experiments, outcomes
from lab import baseline as baseline_mod
from lab.asof import ASSUMED_PROCESSING_MS
from lab.baseline import Baseline
from lab.common import H, MINUTE
from lab.events import event_record
from lab.modules import options_disagreement

T0 = 1_790_121_600_000                     # 2026-09-23 00:00 UTC
DAY = 86_400_000
NEW_API = hasattr(experiments, "checkpoint_sample")


def mk(t, d, group, avail=None):
    avail = avail if avail is not None else t + MINUTE
    return event_record("d", "v", t, t, avail, d, group, {"severity": 1.0}, "h", "as-of replay: test", {}, {}, "c",
                        t_inputs=avail - ASSUMED_PROCESSING_MS)


def feats(t, d):
    """Deterministic, non-collinear baseline features for a decision at t."""
    a = ((t // MINUTE) * 2654435761) % 1000 / 1000
    b = ((t // MINUTE) * 40503) % 997 / 997
    c = ((t // MINUTE) * 69069) % 991 / 991
    return {"prior_ret_60m_aligned": d * (0.004 * a - 0.001), "prior_rv_60m": 0.002 + 0.003 * b,
            "funding_aligned": d * 0.0001 * (c - 0.5)}


class Harness:
    """run_design with outcome labels and baseline features supplied by functions (patched), so the
    evaluation logic is exercised on exactly specified outcomes."""
    def __init__(self, base, design, y_of, status_of=None):
        self.base, self.design, self.y_of = Path(base), design, y_of
        self.status_of = status_of or (lambda t, d, h: "complete")

    def label(self, t_available, direction, bars, now, horizons=(60,), funding=(), half_spread=None):
        entry = -(-t_available // MINUTE) * MINUTE
        out = {}
        for h in horizons:
            end = entry + h * MINUTE
            if end + MINUTE > now:
                out[h] = {"status": "immature"}
            elif self.status_of(t_available, direction, h) != "complete":
                out[h] = {"status": "incomplete", "missing": 1}
            else:
                out[h] = {"status": "complete", "entry_t": entry, "exit_t": end, "label_available": end + MINUTE,
                          "ret_net": self.y_of(t_available, direction, h)}
        return out

    def run(self, now, events, controls, run_state=None, registered=T0 - DAY, variants_at=None):
        evs = [e for e in events if e["t_available"] <= now]
        ctl = [c for c in controls if c["t_available"] <= now]

        class Mod:
            @staticmethod
            def run(lab, params):
                return {"passes": [{"basis": "prospective", "events": [dict(e) for e in evs],
                                    "controls": [dict(c) for c in ctl], "bars": {now - MINUTE: {}}, "coverage": {},
                                    "state": "available", "reasons": []}]}
        store = type("S", (), {"funding_events": lambda s: [], "funding_known": lambda s: [], "snaps": lambda s: []})()
        lab = type("L", (), {"now": now, "write": True, "base": self.base, "code": "c", "store": store})()
        kw = {"run_state": run_state}
        if variants_at is not None:
            kw["variants_at"] = variants_at
        with patch.object(outcomes, "label", self.label), \
                patch.object(experiments, "features_at", lambda bars, kf, t, d: feats(t, d)):
            res, _ = experiments.run_design(lab, self.design, Mod, {"registered": registered}, 1, **kw)
        return res


def design(horizons=(60,), primary=60, ref="control", min_n=100, blocks=20, did="T", version="ev-t"):
    return {"id": did, "version": 2, "module": "flow_absorption", "family": "F", "question": "q",
            "variants": [{"name": "v", "params": {}}], "primary_variant": "v",
            "outcome": {"metric": "ret_net", "horizons_min": list(horizons), "primary_horizon": primary},
            "comparison": {"test_group": "test", "reference_group": ref, "hypothesised_sign": 1},
            "collapse_ms": 0, "min_retained_observations": min_n, "min_dependence_blocks": blocks,
            "_sha256": "x", "_file": "lab/designs/T.json", "_version": version, "_components": {}}


# ---- issue 1 ---------------------------------------------------------------------------------------
def scenario(n_first=100, n_later=100):
    """The review's reproduction: 100 short test decisions (-2%), then 100 long ones (+3%); controls
    every 2 hours whose long outcome is -5% and short outcome -0.1%."""
    first = [mk(T0 + i * 6 * H + H, -1, "test") for i in range(n_first)]
    later = [mk(T0 + (n_first + i) * 6 * H + H, 1, "test") for i in range(n_later)]
    controls = [mk(T0 + day * DAY + hh * H, 1, "control") for day in range(-5, 60) for hh in range(0, 24, 2)]
    tests = {e["t_available"]: e for e in first + later}

    def y(t_available, d, h):
        k = (t_available // H) % 5
        if t_available in tests:
            return (-0.02 if d < 0 else 0.03) + 0.0002 * k
        return (-0.05 + 0.0001 * k) if d > 0 else (-0.001 - 0.0001 * k)
    return first, later, controls, y


def labelled_rows(events, controls, y, now, horizons=(60,), status_of=None, registered=True):
    """What run_design labels, built directly (for the checkpoint interfaces)."""
    h_ = Harness(".", None, y, status_of)
    rows = []
    for e in events:
        e = dict(e, t_persisted=e.get("t_persisted", e["t_available"]))
        rows.append((e, h_.label(e["t_available"], e["direction"], None, now, horizons), feats(e["t_available"], e["direction"])))
    for c in controls:
        for g, d, sfx in (("control_long", 1, "L"), ("control_short", -1, "S")):
            cc = dict(c, group=g, direction=d, event_id=c["event_id"] + sfx)
            rows.append((cc, h_.label(c["t_available"], d, None, now, horizons), feats(c["t_available"], d)))
    return rows


class CheckpointTests(unittest.TestCase):
    now1 = T0 + 600 * H                                 # after the first 100 labels, before the later ones

    def test_appended_observations_do_not_change_the_n100_verdict_common_api(self):
        first, later, controls, y = scenario()
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            a = Harness(d1, design(), y)
            r1 = a.run(self.now1, first + later, controls)
            r2 = a.run(T0 + 1300 * H, first + later, controls, run_state={"last_cutoff": self.now1})
            fresh = Harness(d2, design(), y).run(T0 + 1300 * H, first + later, controls)
        self.assertEqual(r1["status"], "retired", r1["status_reason"])
        self.assertEqual(r2["status"], "retired", r2["status_reason"])          # 2.8: "supported"
        self.assertEqual(fresh["status"], "retired", fresh["status_reason"])    # even without a record

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_record_is_unchanged_and_no_drift_when_observations_are_appended(self):
        first, later, controls, y = scenario()
        with tempfile.TemporaryDirectory() as d:
            a = Harness(d, design(), y)
            a.run(self.now1, first + later, controls)
            path = Path(d, "research/v2/T/ev-t/checkpoints.jsonl")
            before = path.read_bytes()
            r2 = a.run(T0 + 1300 * H, first + later, controls, run_state={"last_cutoff": self.now1})
            self.assertTrue(path.read_bytes().startswith(before))                # historical bytes preserved
            rec = json.loads(before.splitlines()[0])
            self.assertEqual((rec["look"], rec["n"], rec["verdict"]), (1, 100, "retired"))
            self.assertTrue(experiments.verify_checkpoint(rec))
            self.assertEqual(r2["checkpoints"]["records"][0]["manifest_sha256"], rec["manifest_sha256"])
            self.assertEqual(r2["checkpoints"]["drift"], [])
            self.assertEqual(rec["manifest"]["p_long"], 0.0)
            self.assertLessEqual(max(r["known_at"] for r in rec["manifest"]["test"] + rec["manifest"]["reference"]),
                                 rec["cutoff"])

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_later_direction_severity_outcome_and_control_changes_cannot_alter_it(self):
        first, later, controls, y = scenario()
        now = T0 + 1300 * H
        d = design()
        base_rows = labelled_rows(first + later, controls, y, now)
        s0 = experiments.checkpoint_sample(base_rows, d, {"registered": T0 - DAY}, 100)
        cut = s0["cutoff"]
        m0 = experiments.manifest_sha(experiments.build_manifest(d, s0, baseline_mod.build(base_rows, [60])[60], 1))

        def after(rows, fn):
            out = []
            for e, lab, bf in copy.deepcopy(rows):
                v = lab.get(60) or {}
                if v.get("label_available", 0) > cut:
                    fn(e, lab, bf)
                out.append((e, lab, bf))
            return out

        def flip(e, lab, bf):
            e["direction"] = -e["direction"]

        def sev(e, lab, bf):
            e["features"]["severity"] = 99.0

        def out_(e, lab, bf):
            lab[60]["ret_net"] = 5.0

        def ctl(e, lab, bf):
            if e["group"].startswith("control"):
                lab[60]["ret_net"] = -9.0
                bf["prior_ret_60m_aligned"] = 3.0
        for fn in (flip, sev, out_, ctl):
            rows = after(base_rows, fn)
            s = experiments.checkpoint_sample(rows, d, {"registered": T0 - DAY}, 100)
            m = experiments.build_manifest(d, s, baseline_mod.build(rows, [60])[60], 1)
            self.assertEqual(experiments.manifest_sha(m), m0, fn.__name__)
        # appended later controls never enter either
        more = controls + [mk(T0 + 58 * DAY + k * MINUTE * 7, 1, "control") for k in range(50)]
        rows = labelled_rows(first + later, more, y, now)
        s = experiments.checkpoint_sample(rows, d, {"registered": T0 - DAY}, 100)
        self.assertEqual(experiments.manifest_sha(experiments.build_manifest(d, s, baseline_mod.build(rows, [60])[60], 1)), m0)

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_delayed_outcomes_and_exact_cutoff_boundaries(self):
        first, later, controls, y = scenario(30, 0)
        d, reg, now = design(min_n=20, blocks=4), {"registered": T0 - DAY}, T0 + 400 * H
        rows = labelled_rows(first, controls, y, now)
        s = experiments.checkpoint_sample(rows, d, reg, 20)
        tests = sorted((r for r in rows if r[0]["group"] == "test"), key=lambda r: r[0]["t_event"])
        self.assertEqual(s["cutoff"], tests[19][1][60]["label_available"])     # the 20th label, known exactly then
        self.assertEqual(len(s["test"]), 20)
        # one earlier outcome is delayed (its bars arrived late): the cutoff moves to the 21st label
        # and the delayed observation is not in the sample even though it entered earlier
        tests[4][1][60]["label_available"] = now - MINUTE
        s2 = experiments.checkpoint_sample(rows, d, reg, 20)
        self.assertEqual(s2["cutoff"], tests[20][1][60]["label_available"])
        keys = {r["decision_key"] for r in s2["test"]}
        self.assertNotIn(tests[4][0]["decision_key"], keys)
        self.assertIn(tests[20][0]["decision_key"], keys)
        # a decision frozen only after its outcome was known becomes known when it was frozen
        tests[4][1][60]["label_available"] = tests[4][1][60]["exit_t"] + MINUTE
        tests[0][0]["t_persisted"] = tests[19][1][60]["label_available"] + 1
        s3 = experiments.checkpoint_sample(rows, d, reg, 20)
        self.assertEqual(s3["cutoff"], tests[0][0]["t_persisted"])
        # immature labels do not count; with 19 known the look is pending
        rows19 = labelled_rows(first[:19], controls, y, now)
        p = experiments.checkpoint_sample(rows19, d, reg, 20)
        self.assertEqual((p["pending"], p["retained"], p["need"]), (True, 19, 20))
        # quality window: only labels that ended by the cutoff; an incomplete one inside it counts
        rows_q = labelled_rows(first, controls, y, now, status_of=lambda t, dd, h: "incomplete" if t == first[2]["t_available"] else "complete")
        q = experiments.checkpoint_sample(rows_q, d, reg, 20)["quality"]
        self.assertEqual((q["labels_ended_by_cutoff"], q["complete_and_known"]), (21, 20))

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_later_checkpoints_evaluate_their_own_additional_observations(self):
        first, later, controls, y = scenario(40, 0)
        d = design(min_n=20, blocks=4)
        with tempfile.TemporaryDirectory() as dd:
            a = Harness(dd, d, y)
            r = a.run(T0 + 21 * 6 * H, first, controls)               # 20 known -> look 1 only
            self.assertEqual([x["look"] for x in r["checkpoints"]["records"]], [1])
            self.assertIsNone(r["checkpoints"]["pending"])                   # terminal: nothing further pending
            path = Path(dd, "research/v2/T/ev-t/checkpoints.jsonl")
            first_bytes = path.read_bytes()
            r = a.run(T0 + 41 * 6 * H, first, controls, run_state={"last_cutoff": T0 + 21 * 6 * H})
            recs = r["checkpoints"]["records"]
            self.assertEqual(path.read_bytes(), first_bytes)
        # look 1 retired the version (wrong side): a terminal verdict, so no later look is computed
        self.assertEqual(recs[0]["verdict"], "retired")
        self.assertEqual(len(recs), 1)
        # a version whose effect does not settle continues to its next look on its own data
        def y2(t, dd_, h):
            if (t // H) % 24 in (1, 7, 13, 19) and dd_ < 0:           # test decisions: noisy, no effect
                return -0.001 + (0.004 if (t // H) % 2 else -0.004) * (1 if (t // DAY) % 2 else -1)
            return -0.001 if dd_ < 0 else -0.05
        with tempfile.TemporaryDirectory() as dd:
            a = Harness(dd, d, y2)
            r1 = a.run(T0 + 21 * 6 * H, first, controls)
            self.assertEqual(r1["checkpoints"]["records"][0]["verdict"], "not_met")
            self.assertEqual(r1["checkpoints"]["pending"], {"look": 2, "need": 30, "retained": 21})
            a.run(T0 + 31 * 6 * H, first, controls, run_state={"last_cutoff": T0 + 21 * 6 * H})
            r = a.run(T0 + 41 * 6 * H, first, controls, run_state={"last_cutoff": T0 + 31 * 6 * H})
            recs = r["checkpoints"]["records"]
            lines = Path(dd, "research/v2/T/ev-t/checkpoints.jsonl").read_text().splitlines()
        self.assertEqual([x["look"] for x in recs], [1, 2, 3])
        self.assertEqual([x["n"] for x in recs], [20, 30, 40])
        self.assertTrue(recs[0]["cutoff"] < recs[1]["cutoff"] < recs[2]["cutoff"])
        k1 = {x["key"] for x in recs[0]["manifest"]["test"]}
        k2 = {x["key"] for x in recs[1]["manifest"]["test"]}
        self.assertTrue(k1 < k2 and len(k2 - k1) == 10)
        self.assertEqual(len(lines), 3)

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_repeat_runs_are_idempotent_and_multiplicity_is_bounded_by_the_cutoff(self):
        first, later, controls, y = scenario(30, 0)
        d = design(min_n=20, blocks=4)
        seen = []

        def variants_at(t):
            seen.append(t)
            return 3 if t < T0 + 10 * DAY else 50
        with tempfile.TemporaryDirectory() as dd:
            a = Harness(dd, d, y)
            a.run(T0 + 200 * H, first, controls, variants_at=variants_at)
            snap = {p: p.read_bytes() for p in Path(dd).rglob("*.jsonl")}
            a.run(T0 + 200 * H, first, controls, run_state={"last_cutoff": T0 + 200 * H}, variants_at=variants_at)
            self.assertEqual(snap, {p: p.read_bytes() for p in Path(dd).rglob("*.jsonl")})
            rec = experiments.load_checkpoints(dd, d)[1]
        self.assertEqual(seen[0], rec["cutoff"])
        self.assertEqual(rec["manifest"]["criteria"]["n_variants"], 3)

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_drift_is_reported_never_rewritten_and_a_new_version_keeps_the_old_record(self):
        first, later, controls, y = scenario(30, 0)
        d = design(min_n=20, blocks=4)
        with tempfile.TemporaryDirectory() as dd:
            a = Harness(dd, d, y)
            a.run(T0 + 200 * H, first, controls)
            rec = experiments.load_checkpoints(dd, d)[1]
            a.y_of = lambda t, dd_, h: y(t, dd_, h) + (0.5 if t == first[0]["t_available"] else 0)   # a revised past outcome
            r = a.run(T0 + 210 * H, first, controls, run_state={"last_cutoff": T0 + 200 * H})
            self.assertEqual(r["checkpoints"]["records"][0]["manifest_sha256"], rec["manifest_sha256"])
            self.assertEqual(len(r["checkpoints"]["drift"]), 1)
            d2 = design(min_n=20, blocks=4, version="ev-corrected")
            Harness(dd, d2, a.y_of).run(T0 + 210 * H, first, controls)
            self.assertEqual(experiments.load_checkpoints(dd, d)[1], rec)          # old evidence intact
            self.assertIn(1, experiments.load_checkpoints(dd, d2))

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_verification_and_skill_proposals_use_recorded_checkpoints(self):
        def ysup(t, dd_, h):
            k = (t // H) % 5
            if (t // H) % 6 == 1:
                return 0.01 + 0.0003 * k
            return (-0.001 + 0.0001 * k) if dd_ > 0 else (-0.001 - 0.0001 * k)
        first, later, controls, _ = scenario(30, 0)
        first = [mk(e["t_event"], 1, "test") for e in first]
        d = design(min_n=20, blocks=4)
        with tempfile.TemporaryDirectory() as dd:
            res = Harness(dd, d, ysup).run(T0 + 200 * H, first, controls)
        self.assertEqual(res["status"], "supported", res["status_reason"])
        rec = res["checkpoints"]["records"][0]
        self.assertTrue(experiments.verify_checkpoint(rec))
        dd_ = dict(d, _file="lab/designs/T.json")
        card = {"design": "T", "evaluation_version": "ev-t", "status": "supported", "status_reason": "x",
                "condition": "q?", "registered_at": "2026-09-22", "primary_horizon_min": 60, "passes": {},
                "contradictory_evidence": [], "checkpoints": evidence.checkpoint_view(dd_, res),
                "research_integrity": res.get("integrity")}          # 2.12: bar-based, "not_required"
        text = evidence.skill_proposals([card], T0)
        self.assertIn(rec["manifest_sha256"], text)
        iv = rec["checks"]["effect_adjusted"]["interval"]
        self.assertIn(f"{iv[0] * 1e4:+.1f} bp", text)
        bad = copy.deepcopy(res)
        bad["checkpoints"]["records"][0]["manifest"]["test"][0]["y"] += 1.0          # tampered evidence
        self.assertFalse(experiments.verify_checkpoint(bad["checkpoints"]["records"][0]))
        self.assertEqual(experiments.status(d, bad["checkpoints"]["records"], None)[0], "blocked")
        card_bad = dict(card, checkpoints=evidence.checkpoint_view(dd_, bad))
        text = evidence.skill_proposals([card_bad], T0)
        self.assertIn("No change is proposed", text)
        self.assertIn("proposal withheld", text)


class KnowledgeOrderTests(unittest.TestCase):
    """Things decided or stored after a cutoff cannot reach back into it (review of the first 2.9 draft)."""
    def test_later_known_decision_cannot_displace_a_known_episode_head(self):
        from lab.events import collapse, collapse_as_known
        key = lambda e: (e["detector"], e["direction"])
        a = dict(mk(T0 + 50 * MINUTE, 1, "test"), t_persisted=T0 + H)
        c = dict(mk(T0 + 110 * MINUTE, 1, "test"), t_persisted=T0 + H)
        same = [dict(a), dict(c), dict(mk(T0 + 80 * MINUTE, 1, "test"), t_persisted=T0 + H)]
        self.assertEqual([e["event_id"] for e in collapse_as_known([dict(x) for x in same], 30 * MINUTE, key,
                                                                    lambda e: e["t_persisted"])],
                         [e["event_id"] for e in collapse([dict(x) for x in same], 30 * MINUTE, key)])
        late = dict(mk(T0 + 40 * MINUTE, 1, "test", avail=T0 + 90 * MINUTE), t_persisted=T0 + 7 * H)
        bridge = dict(mk(T0 + 80 * MINUTE, 1, "test"), t_persisted=T0 + 7 * H)
        heads = collapse_as_known([dict(a), dict(c), late, bridge], 30 * MINUTE, key, lambda e: e["t_persisted"])
        self.assertEqual({e["event_id"] for e in heads}, {a["event_id"], c["event_id"]})   # 2.9 draft: late became head

    def test_checkpoint_sample_ignores_a_decision_frozen_after_the_cutoff(self):
        d = design(min_n=10, blocks=1)
        d["collapse_ms"] = 30 * MINUTE
        base = [mk(T0 + i * 6 * H + H, 1, "test") for i in range(9)]
        a = mk(T0 + 59 * H + 50 * MINUTE, 1, "test")
        a2 = mk(T0 + 58 * H, 1, "test")
        b = mk(T0 + 59 * H + 40 * MINUTE, 1, "test", avail=T0 + 60 * H + 30 * MINUTE)     # inputs late, frozen later
        controls = [mk(T0 + dd * DAY + hh * H, 1, "control") for dd in range(-3, 4) for hh in range(0, 24, 2)]
        y = lambda t, dd, h: 0.001 * ((t // H) % 7) * dd

        class LateBars(Harness):                     # a2's bars arrive only at T0+61h
            def label(self, t_available, direction, bars, now, horizons=(60,), funding=(), half_spread=None):
                out = super().label(t_available, direction, bars, now, horizons, funding, half_spread)
                if t_available == a2["t_available"] and out[60]["status"] == "complete":
                    if now < T0 + 61 * H:
                        out[60] = {"status": "incomplete", "missing": 1}
                    else:
                        out[60]["label_available"] = T0 + 61 * H
                return out
        out = []
        for extra in ([], [b]):
            with tempfile.TemporaryDirectory() as tmp:
                hz, rs = LateBars(tmp, d, y), None
                for k in range(1, 12):
                    now = T0 + k * 6 * H
                    res = hz.run(now, base + [a, a2] + extra, controls, run_state=rs)
                    rs = {"last_cutoff": now}
                rec = res["checkpoints"]["records"][0]
                out.append((rec["cutoff"], rec["manifest_sha256"]))
        self.assertEqual(out[0], out[1])

    def test_option_controls_do_not_depend_on_snapshot_timing(self):
        recs = [{"t": T0 + i * 15 * MINUTE, "observed_at": T0 + i * 15 * MINUTE + MINUTE, "rows": []} for i in range(8)]

        def controls(snaps):
            store = type("S", (), {"options": lambda s: recs, "snaps": lambda s: snaps, "bars": lambda s, n: {}})()
            lab = type("L", (), {"store": store, "code": "c"})()
            with patch.object(options_disagreement, "surface", lambda r: {"rr25_7d": 1.0}), \
                    patch.object(options_disagreement, "panel_quality", lambda r: {"rr25_7d_quotes": "unknown"}):
                p = options_disagreement.run(lab, {"z": 2, "z_window": 4, "min_records": 1})["passes"][0]
            return [(c["t_event"], c["t_available"]) for c in p["controls"]]
        snap = lambda seen: [{"t": T0 + H, "observed_at": seen, "binance_usdt_prem": {"st": "ok",
                                                                                      "funding_live_predicted_8h": 1e-4}}]
        ref = controls([])
        self.assertEqual(len(ref), 2)
        for seen in (T0 + H + 5 * MINUTE, T0 + 2 * H + 10 * MINUTE):      # on time; 70 minutes late
            self.assertEqual(controls(snap(seen)), ref)                  # 2.9 draft: moved, then dropped

    def test_first_freeze_wins_and_merge_keeps_it(self):
        import io
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        import merge_research
        d = design()
        rel = "research/v2/T/ev-t/events/2026-09.jsonl"
        first = json.dumps({"decision_key": "k1", "group": "test", "t_persisted": 1000}, sort_keys=True)
        second = json.dumps({"decision_key": "k1", "group": "test_ineligible", "t_persisted": 2000}, sort_keys=True)
        with tempfile.TemporaryDirectory() as inc, tempfile.TemporaryDirectory() as repo:
            for b_ in (inc, repo):
                Path(b_, rel).parent.mkdir(parents=True)
            Path(repo, rel).write_text(first + "\n")
            Path(inc, rel).write_text(second + "\n")
            with patch("sys.stdout", io.StringIO()):
                merge_research.main(inc, repo)
            self.assertEqual(Path(repo, rel).read_text(), first + "\n")
            Path(repo, rel).write_text(first + "\n" + second + "\n")   # even a duplicate line cannot override
            self.assertEqual(experiments.load_frozen(repo, d)["k1"]["t_persisted"], 1000)

    def test_verification_rejects_an_inconsistent_record_even_with_a_matching_hash(self):
        def ysup(t, dd_, h):
            return 0.01 + 0.0003 * ((t // H) % 5) if (t // H) % 6 == 1 else -0.001
        first = [mk(T0 + i * 6 * H + H, 1, "test") for i in range(30)]
        controls = [mk(T0 + day * DAY + hh * H, 1, "control") for day in range(-5, 10) for hh in range(0, 24, 2)]
        d = design(min_n=20, blocks=4)
        with tempfile.TemporaryDirectory() as dd:
            rec = Harness(dd, d, ysup).run(T0 + 200 * H, first, controls)["checkpoints"]["records"][0]
        self.assertTrue(experiments.verify_checkpoint(rec, d))
        for edit in (lambda r: r["manifest"]["test"].pop(),                       # fewer rows than n
                     lambda r: r["manifest"]["criteria"].update(n_variants=1, adjusted_alpha=0.5),
                     lambda r: r["manifest"]["reference"][0].update(known_at=r["cutoff"] + 1)):
            bad = copy.deepcopy(rec)
            edit(bad)
            bad["manifest_sha256"] = experiments.manifest_sha(bad["manifest"])     # hash recomputed
            self.assertFalse(experiments.verify_checkpoint(bad, d))
        self.assertFalse(experiments.verify_checkpoint(rec, dict(d, min_retained_observations=30)))

    def test_multiplicity_counts_only_versions_registered_by_the_cutoff(self):
        from lab import run as run_mod
        d1 = dict(design(did="A"), family="F", _version="ev-1")
        d2 = dict(design(did="B"), family="F", _version="ev-2", variants=[{"name": "x"}, {"name": "y"}])
        with tempfile.TemporaryDirectory() as base:
            f = run_mod.family_variants_at(base, [d1, d2], {"A": {"registered": 100}, "B": {"registered": 500}})["F"]
        self.assertEqual((f(99), f(100), f(499), f(500)), (0, 1, 1, 3))


class CheckpointMergeTests(unittest.TestCase):
    def test_merge_keeps_the_first_record_of_a_look(self):
        import io
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        import merge_research
        rel = "research/v2/T/ev-t/checkpoints.jsonl"
        with tempfile.TemporaryDirectory() as inc, tempfile.TemporaryDirectory() as repo:
            for b in (inc, repo):
                Path(b, rel).parent.mkdir(parents=True)
            Path(repo, rel).write_text('{"look":1,"verdict":"not_met","completed_at":1}\n')
            Path(inc, rel).write_text('{"look":1,"verdict":"supported","completed_at":2}\n'
                                      '{"look":2,"verdict":"not_met","completed_at":3}\n')
            with patch("sys.stdout", io.StringIO()), patch("sys.stderr", io.StringIO()):
                rc = merge_research.main(inc, repo)
            # 2.11: an incoming batch computed against a different look-1 record is rejected whole
            self.assertEqual(rc, 3)
            self.assertEqual(Path(repo, rel).read_text(), '{"look":1,"verdict":"not_met","completed_at":1}\n')
            look2 = '{"look":2,"verdict":"not_met","completed_at":3,"design":"T","version":"ev-t"}'
            Path(inc, rel).write_text('{"look":1,"verdict":"not_met","completed_at":1}\n' + look2 + "\n")
            if hasattr(merge_research, "publication_problems"):          # 2.12: publication metadata required
                from publication_fixture import batch_metadata
                batch_metadata(inc, 3, {"T": "ev-t"})
            with patch("sys.stdout", io.StringIO()):
                self.assertEqual(merge_research.main(inc, repo), 0)
            self.assertEqual(Path(repo, rel).read_text(), '{"look":1,"verdict":"not_met","completed_at":1}\n'
                                                          + look2 + "\n")


class LabelAvailabilityTests(unittest.TestCase):
    def bars(self, start, n, lag=0):
        return {start + i * MINUTE: {"t": start + i * MINUTE, "o": 100.0, "h": 100.1, "l": 99.9, "c": 100.0,
                                     "avail": start + (i + 1) * MINUTE + lag} for i in range(n)}

    def test_label_available_covers_late_bars_and_attributed_funding(self):
        t0 = T0 + 7 * H + 30 * MINUTE                               # 07:30; the 60-minute label spans 08:00
        b = self.bars(t0 - 5 * MINUTE, 200)
        now = t0 + 190 * MINUTE
        lab = outcomes.label(t0, 1, b, now, (60,), funding=[(T0, 1e-4, T0 + 7 * MINUTE)])[60]
        self.assertEqual(lab["status"], "immature")                 # 08:00 settlement not stored yet
        f = [(T0, 1e-4, T0 + 7 * MINUTE), (T0 + 8 * H + 4, 5e-4, T0 + 8 * H + 40 * MINUTE)]
        lab = outcomes.label(t0, 1, b, now, (60,), funding=f)[60]
        self.assertEqual(lab["status"], "complete")
        self.assertEqual(lab["label_available"], T0 + 8 * H + 40 * MINUTE)   # the settlement's availability
        self.assertAlmostEqual(lab["costs"]["funding_pnl"], -5e-4)
        b[t0 + 10 * MINUTE]["avail"] = t0 + 150 * MINUTE              # one bar stored late
        self.assertEqual(outcomes.label(t0, 1, b, now, (60,), funding=f)[60]["label_available"], t0 + 150 * MINUTE)

    def test_half_spread_uses_only_observed_snapshots(self):
        snaps = [{"t": T0, "observed_at": T0 + 5 * MINUTE,
                  "depth_binance_usdt": {"st": "ok", "best_bid": 99.0, "best_ask": 101.0}}]
        self.assertEqual(outcomes.half_spread_bp(snaps, T0 + 2 * MINUTE)[1], "default")
        self.assertEqual(outcomes.half_spread_bp(snaps, T0 + 5 * MINUTE)[1], "snapshot")


# ---- issue 2 ---------------------------------------------------------------------------------------
FIELDS = ["instrument", "timestamp", "best_bid_price", "best_bid_amount", "best_ask_price", "best_ask_amount",
          "mark_price", "mark_iv", "bid_iv", "ask_iv", "delta"]
T_EVT = T0 + 9 * H + 45 * MINUTE                   # the 09:45 record; its inputs are complete at 09:47


class OptionsAvailabilityTests(unittest.TestCase):
    """Record K-1 (09:30) has its funding snapshot observed only at 10:00."""
    def build(self, f_prev=0.0001, prev_snap_at=T0 + 10 * H, cur_snap_at=T_EVT + 2 * MINUTE, prev_status="ok",
              extra_missing=0, late_record=False, next_record=True):
        recs, snaps = [], []
        ks = list(range(-35, 2 if next_record else 1))
        for k in ks:
            t = T_EVT + k * 15 * MINUTE
            rr = -5.0 if k == 0 else 0.1 * (k % 3)
            rows = [["BTC-30SEP26-90000-C", 10.0, 50.0 + rr / 2], ["BTC-30SEP26-70000-P", 10.0, 50.0 - rr / 2]]
            recs.append({"t": t, "t_event": t, "observed_at": t + MINUTE, "rows": rows, "underlying": {"30SEP26": 8e4},
                         "panel_fields": FIELDS,
                         "panel": [["BTC-30SEP26-90000-C", t - 1000, 0.010, 5, 0.011, 5, 0.0105, 50.0, 49.0, 51.0, 0.25],
                                   ["BTC-30SEP26-70000-P", t - 1000, 0.010, 5, 0.011, 5, 0.0105, 55.0, 54.0, 56.0, -0.25]]})
            fund, seen, st = 0.0001 * (k % 3), t + MINUTE, "ok"
            if k == -1:
                fund, seen, st = f_prev, prev_snap_at, prev_status
            if k == 0:
                fund, seen = 0.01, cur_snap_at
            if -1 - extra_missing <= k < -1:
                st = "error"
            snaps.append({"t": t, "observed_at": seen, "binance_usdt_prem": {"st": st, "funding_live_predicted_8h": fund}})
        if late_record:                              # a 09:37 record collected only at 11:00
            t = T_EVT - 8 * MINUTE
            recs.append(dict(recs[-3], t=t, t_event=t, observed_at=T0 + 11 * H))
            recs.sort(key=lambda r: r["t"])
        return recs, snaps

    def module_run(self, policy="qualified", **kw):
        recs, snaps = self.build(**kw)

        class S:
            def options(self):
                return recs

            def snaps(self):
                return snaps

            def bars(self, name):
                return {}
        lab = type("L", (), {"store": S(), "code": "c"})()
        with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rows"][0][2] - rec["rows"][1][2]}):
            p = options_disagreement.run(lab, {"z": 2.0, "z_window": 30, "min_records": 10, "quote_policy": policy})["passes"][0]
        return p

    @staticmethod
    def at(p, t, kind="events"):
        return [e for e in p[kind] if e["t_event"] == t]

    @staticmethod
    def essence(evs):
        return [(e["group"], e["direction"], e["t_available"], e["features"]) for e in evs]

    def test_future_funding_cannot_change_the_0945_event_common_api(self):
        for policy in ("qualified", "mark_only"):
            small = self.module_run(policy, f_prev=0.0001)
            huge = self.module_run(policy, f_prev=0.5)             # available only at 10:00
            a, b = self.at(small, T_EVT), self.at(huge, T_EVT)
            self.assertEqual(len(a), 1, policy)
            self.assertEqual(self.essence(a), self.essence(b), policy)   # existence, direction, features, eligibility
            self.assertEqual(a[0]["t_inputs"], T_EVT + 2 * MINUTE)

    def test_value_becomes_usable_for_later_decisions(self):
        small, huge = self.module_run(f_prev=0.0001), self.module_run(f_prev=0.5)
        c1 = self.at(small, T_EVT + 15 * MINUTE, "controls")[0]["features"]["funding_z"]
        c2 = self.at(huge, T_EVT + 15 * MINUTE, "controls")[0]["features"]["funding_z"]
        self.assertIsNotNone(c1)
        self.assertNotEqual(c1, c2)                                 # the 10:00 decision may use it

    def test_exact_cutoff_boundary_common_api(self):
        edge = T_EVT + 2 * MINUTE                                   # the event's t_inputs
        on = [self.module_run(f_prev=f, prev_snap_at=edge) for f in (0.0001, 0.5)]
        after = [self.module_run(f_prev=f, prev_snap_at=edge + 1) for f in (0.0001, 0.5)]
        self.assertNotEqual(self.essence(self.at(on[0], T_EVT)), self.essence(self.at(on[1], T_EVT)))   # known at t_inputs
        self.assertEqual(self.essence(self.at(after[0], T_EVT)), self.essence(self.at(after[1], T_EVT)))

    def test_missing_funding_stays_unknown(self):
        p = self.module_run(prev_status="error")
        ev = self.at(p, T_EVT)
        self.assertEqual(len(ev), 1)                                # 29 of 30 known: coverage met
        sparse = self.module_run(prev_status="error", extra_missing=9)      # 10 of 30 missing: below 70%
        self.assertEqual(self.at(sparse, T_EVT), [])
        c = [e for e in sparse["controls"] if e["features"]["funding_pred_8h"] is None]
        self.assertTrue(c)                                          # never filled

    def test_delayed_current_snapshot_moves_the_decision_and_then_uses_known_history(self):
        a = self.module_run(f_prev=0.0001, cur_snap_at=T0 + 10 * H + 5 * MINUTE)
        b = self.module_run(f_prev=0.5, cur_snap_at=T0 + 10 * H + 5 * MINUTE)
        self.assertEqual(self.at(a, T_EVT)[0]["t_inputs"], T0 + 10 * H + 5 * MINUTE)
        self.assertNotEqual(self.essence(self.at(a, T_EVT)), self.essence(self.at(b, T_EVT)))

    def test_later_arrivals_do_not_revise_the_event(self):
        base = self.at(self.module_run(next_record=False), T_EVT)
        self.assertEqual(self.essence(self.at(self.module_run(late_record=True), T_EVT)), self.essence(base))
        self.assertEqual(self.essence(self.at(self.module_run(next_record=True), T_EVT)), self.essence(base))


# ---- issue 3 ---------------------------------------------------------------------------------------
SLOPE = {30: 2.0, 60: -3.0, 240: 0.5, 480: 1.0}


def horizon_y(t_available, d, h):
    """Outcomes whose dependence on the prior return differs by horizon (tests and controls alike)."""
    f = feats(t_available, d)
    return SLOPE[h] * f["prior_ret_60m_aligned"] + 0.00001 * ((t_available // MINUTE) % 3 - 1)


class HorizonBaselineTests(unittest.TestCase):
    H4 = (30, 60, 240, 480)

    def data(self):
        tests = [mk(T0 + i * 6 * H + H, 1, "test") for i in range(80)]
        controls = [mk(T0 + day * DAY + hh * H, 1, "control") for day in range(-5, 25) for hh in range(0, 24, 2)]
        return tests, controls

    def test_each_horizon_is_predicted_by_its_own_baseline_common_api(self):
        tests, controls = self.data()
        with tempfile.TemporaryDirectory() as dd:
            res = Harness(dd, design(self.H4, 60, ref="control", min_n=100), horizon_y).run(T0 + 30 * DAY, tests, controls)
        ev = res["variants"][0]["passes"][0]["phases"]["evaluation"]
        for h in (30, 60, 240):
            b = ev[str(h)]["baseline"]
            self.assertEqual(b["identifiable_share_test"], 1.0, h)
            self.assertLess(abs(b["test_residual"]["mean"]), 2e-5, h)   # 2.8: a 60-minute model mis-predicts 30/240

    def test_missing_horizon_data_stays_unidentifiable_common_api(self):
        tests, controls = self.data()
        ctl_t = {c["t_available"] for c in controls}
        status = lambda t, d, h: "incomplete" if (h == 480 and t in ctl_t) else "complete"
        with tempfile.TemporaryDirectory() as dd:
            res = Harness(dd, design(self.H4, 60, ref="control", min_n=100), horizon_y, status).run(T0 + 30 * DAY, tests, controls)
        b = res["variants"][0]["passes"][0]["phases"]["evaluation"]["480"]["baseline"]
        self.assertEqual(b["identifiable_share_test"], 0.0)              # 2.8: borrowed the 60-minute model
        self.assertIsNone(b["residual_diff"]["adjusted"])

    def test_future_controls_cannot_alter_an_earlier_prediction_common_api(self):
        day = T0 + 10 * DAY
        rows = []
        for k in range(60):
            t = T0 + k * 2 * H
            f = feats(t, 1)
            rows.append(dict(f, entry_t=t, exit_t=t + 60 * MINUTE, label_available=t + 61 * MINUTE,
                             y=-3.0 * f["prior_ret_60m_aligned"]))
        obs = dict(feats(day + H, 1), entry_t=day + H, exit_t=day + 2 * H)
        p0 = Baseline(rows).predict(obs)[0]
        # a control that ended before the day but whose label was only available after it (late bars)
        late = [dict(r, y=5.0, label_available=day + H) for r in rows[:30]]
        late = [dict(r, entry_t=day - 3 * H + i * MINUTE, exit_t=day - 2 * H + i * MINUTE) for i, r in enumerate(late)]
        self.assertAlmostEqual(Baseline(rows + late).predict(obs)[0], p0, places=12)

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_training_rows_are_same_horizon_and_known_before_the_bound(self):
        tests, controls = self.data()
        rows = labelled_rows(tests, controls, horizon_y, T0 + 30 * DAY, self.H4)
        bl = baseline_mod.build(rows, self.H4)
        day = T0 + 3 * DAY
        for h in (30, 60, 240):
            tr, bound = bl[h].training(day)
            self.assertTrue(tr and all(r["_known"] <= day for r in tr))
            self.assertTrue(all(r["exit_t"] - r["entry_t"] == h * MINUTE for r in tr))
            self.assertEqual(bl[h].describe()["horizon_min"], h)
            cut = day - 6 * H
            tr2, b2 = bl[h].training(day, cut)
            self.assertEqual(b2, cut)
            self.assertTrue(all(r["_known"] <= cut for r in tr2) and len(tr2) < len(tr))
            edge = [r for r in bl[h].rows if r["_known"] == day]
            self.assertTrue(all(r in tr for r in edge))                     # known exactly at the bound: usable
        with self.assertRaises(ValueError):                                 # one model for many horizons is refused
            experiments.summarize(rows, design(self.H4, 60), {"registered": T0 - DAY}, "evaluation", {},
                                  Baseline([]), 1)

    @unittest.skipUnless(NEW_API, "2.9 interface")
    def test_primary_horizon_promotion_uses_its_own_baseline(self):
        tests, controls = self.data()
        ctl_t = {c["t_available"] for c in controls}
        d = design(self.H4, 30, ref="control", min_n=20, blocks=4)
        rows = labelled_rows(tests, controls, horizon_y, T0 + 30 * DAY, self.H4)
        bl = baseline_mod.build(rows, self.H4)
        s = experiments.checkpoint_sample(rows, d, {"registered": T0 - DAY}, 20)
        m = experiments.build_manifest(d, s, bl[30], 1)
        self.assertEqual(m["baseline"]["horizon_min"], 30)
        r0 = s["test"][0]
        self.assertEqual(m["test"][0]["prediction"], bl[30].predict(r0, cutoff=s["cutoff"])[0])
        self.assertNotEqual(m["test"][0]["prediction"], bl[60].predict(r0, cutoff=s["cutoff"])[0])
        # the primary horizon's controls are missing: blocked, never rescued by the 60-minute model
        status = lambda t, dd, h: "incomplete" if (h == 30 and t in ctl_t) else "complete"
        rows = labelled_rows(tests, controls, horizon_y, T0 + 30 * DAY, self.H4, status)
        with tempfile.TemporaryDirectory() as dd:
            lab = type("L", (), {"base": dd, "now": T0 + 30 * DAY})()
            recs, pending, _ = experiments.checkpoints(lab, d, rows, {"registered": T0 - DAY},
                                                       baseline_mod.build(rows, self.H4), lambda t: 1, write=False)
        self.assertFalse(recs[0]["checks"]["baseline_identifiable"]["ok"])
        self.assertEqual(recs[0]["checks"]["baseline_identifiable"]["horizon_min"], 30)
        self.assertNotEqual(recs[0]["verdict"], "supported")


if __name__ == "__main__":
    unittest.main()
