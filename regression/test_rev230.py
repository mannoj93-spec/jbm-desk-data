"""Repo 2.30 research-integrity repairs (Oct 19 2026 review, F2-F9 and sections 13-17).

Each test class reproduces a reviewed defect at the public entry point, then checks the repair and a valid control.
Every fixture is synthetic and offline: a fixture receipt is never a registry write, a fixture publication is never a
main-branch commit, a mock backend is never a live archive, and nothing here says a venue returned these values."""
import datetime as dt
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "regression"))

from lab.data import Store  # noqa: E402
from research_tools import evidence_contract as E  # noqa: E402
from research_tools import panel  # noqa: E402
import test_rev229 as R229  # noqa: E402

MIN = 60_000
H = 60 * MIN
T0 = R229.T0


def _write(base, rel, rows):
    p = Path(base) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def f2_base(tmp, snap_until=None, oi_until=None, perp_minutes=6 * 60, depth_shift_min=0):
    """write_base, then cut snapshots after snap_until and OI after oi_until (ms), keeping perp bars to perp_minutes."""
    base = R229.write_base(tmp, minutes=perp_minutes)
    sp = Path(base) / "data/snap/2026-10.jsonl"
    snaps = [json.loads(x) for x in sp.read_text().splitlines()]
    if depth_shift_min:
        for s in snaps:
            s["depth_binance_usdt"]["t_event"] = s["t"] + depth_shift_min * MIN
    if snap_until is not None:
        snaps = [s for s in snaps if s["t"] <= snap_until]
    _write(base, "data/snap/2026-10.jsonl", snaps)
    op = Path(base) / "data/series/binance_openInterestHist_5m/2026-10.jsonl"
    rows = [json.loads(x) for x in op.read_text().splitlines()]
    if oi_until is not None:
        rows = [r for r in rows if r["t"] <= oi_until]
    _write(base, "data/series/binance_openInterestHist_5m/2026-10.jsonl", rows)
    return base


# ------------------------------------------------------------------------------------------------- F2 panel
class F2PanelFreshnessTests(unittest.TestCase):
    def test_reviewed_failure_stale_snapshots_and_old_oi_are_not_usable(self):
        """05:00 decision: perp bars ending 04:45, depth/funding/basis from 00:07, OI ending 01:55 (panel-1.0.0 said ok)."""
        with tempfile.TemporaryDirectory() as tmp:
            base = f2_base(tmp, snap_until=T0 + 7 * MIN, oi_until=T0 + H + 55 * MIN)
            p = panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 5 * H, T0 + 5 * H + 1)
            r = p["rows"][0]
            self.assertEqual(r["t_utc"], "2026-10-12T05:00Z")
            self.assertEqual(r["fstate"]["flow_btc"], "ok")                       # the perp-only value stands
            self.assertTrue(r["fstate"]["flow_per_depth"].startswith("stale-depth"))
            self.assertNotIn("flow_per_depth", r["features"])
            self.assertTrue(r["state"]["funding_dispersion"].startswith("stale-funding"))
            self.assertTrue(r["state"]["spot_perp_basis"].startswith("stale-basis"))
            self.assertTrue(r["state"]["positioning_interaction"].startswith("stale-oi"))
            self.assertNotIn("d_oi_1h_pct", r["features"])
            self.assertEqual(r["inputs"]["sources"]["depth"]["state"], "stale")
            ok, why = panel.eligible(r, ["ret_1h_bp", "flow_per_depth", "d_oi_1h_pct"])
            self.assertFalse(ok)
            self.assertEqual(len(why), 3)

    def test_valid_aligned_inputs_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = panel.build(Store(f2_base(tmp), cutoff=T0 + 6 * H), T0 + 3 * H, T0 + 5 * H)
            oks = [r for r in p["rows"] if panel.eligible(r, ["flow_per_depth", "d_oi_1h_pct", "basis_bp",
                                                             "funding_dispersion_bp_8h"])[0]]
            self.assertEqual(len(oks), len(p["rows"]))
            for r in oks:
                w0, w1 = (E.instant(x) for x in r["inputs"]["oi_window_utc"])
                self.assertEqual((w1 - w0).total_seconds(), 3600)
                self.assertEqual(r["inputs"]["oi_stamp_utc"], r["inputs"]["oi_window_utc"][1])
                self.assertLessEqual(r["inputs"]["sources"]["oi"]["age_s"], panel.OI_MAX_AGE // 1000)

    def test_oi_and_price_refer_to_the_same_hour(self):
        """ret_1h_bp is the return over the OI hour, not over the latest perp hour."""
        with tempfile.TemporaryDirectory() as tmp:
            st = Store(f2_base(tmp), cutoff=T0 + 6 * H)
            r = panel.build(st, T0 + 4 * H, T0 + 4 * H + 1)["rows"][0]
            perp = st.bars("binance_klines_1m_BTCUSDT_perp")
            t_oi = E.instant(r["inputs"]["oi_stamp_utc"])
            t_oi = int(t_oi.timestamp() * 1000)
            want = 1e4 * math.log(perp[t_oi - MIN]["c"] / perp[t_oi - 60 * MIN]["o"])
            self.assertAlmostEqual(r["features"]["ret_1h_bp"], round(want, 3), places=3)
            vol = sum(perp[t_oi - k * MIN]["v"] for k in range(1, 61))
            self.assertIsNotNone(r["features"]["d_oi_per_volume"])
            self.assertGreater(vol, 0)

    def test_depth_far_from_the_flow_window_is_misaligned(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = f2_base(tmp, depth_shift_min=-25)                 # every depth measured 25 min before its slot
            r = panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 4 * H, T0 + 4 * H + 1)["rows"][0]
            self.assertTrue(r["fstate"]["flow_per_depth"].startswith(("misaligned-depth", "stale-depth")))
            self.assertNotIn("flow_per_depth", r["features"])

    def test_valid_zero_is_a_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = f2_base(tmp)
            sp = Path(base) / "data/snap/2026-10.jsonl"
            snaps = [json.loads(x) for x in sp.read_text().splitlines()]
            for s in snaps:
                for v in s["hl_predicted_fundings"]["venues"].values():
                    v["rate"] = 0.0
            _write(base, "data/snap/2026-10.jsonl", snaps)
            r = panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 4 * H, T0 + 4 * H + 1)["rows"][0]
            self.assertEqual((r["features"]["funding_mean_bp_8h"], r["fstate"]["funding_mean_bp_8h"]), (0.0, "ok"))

    def test_admitted_panel_is_not_silently_revised(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = f2_base(tmp)
            p1 = panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 3 * H, T0 + 5 * H)
            adm = panel.freeze(p1)
            self.assertTrue(panel.compare(adm, panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 3 * H, T0 + 5 * H))["identical"])
            sp = Path(base) / "data/snap/2026-10.jsonl"
            snaps = [json.loads(x) for x in sp.read_text().splitlines()]
            snaps[17]["depth_binance_usdt"]["bid_btc_25"] = 61.0                # a later correction of stored data
            _write(base, "data/snap/2026-10.jsonl", snaps)
            c = panel.compare(adm, panel.build(Store(base, cutoff=T0 + 6 * H), T0 + 3 * H, T0 + 5 * H))
            self.assertFalse(c["identical"])
            self.assertTrue(c["changed_rows"])
            self.assertIn("new panel version", c["rule"])
            self.assertEqual(adm["policy_sha256"], panel.policy_sha256())


if __name__ == "__main__":
    unittest.main()


# ------------------------------------------------------------------------------------------ F3 research API
from research_tools import research_api as RA  # noqa: E402
from research_tools.research_api import ResearchAPI, Refused, verify_results  # noqa: E402
from research_tools.search_ledger import FileAnchor, Ledger, LedgerCorrupt  # noqa: E402
import random  # noqa: E402

SPEC = dict(R229.SPEC)


def shifted_provider(mean=5.0, sd=2.0, n=6000, horizons=(60, 240), rolling_days=None):
    """Synthetic rows every 15 min with feature x ~ N(mean, sd); labels for each horizon, available t + h + 1 min.
    rolling_days emulates repo 2.29's rolling provider (ignores start)."""
    rnd = random.Random(23)
    rows, labels = [], {h: [] for h in horizons}
    for k in range(n):
        t = T0 + k * 15 * MIN
        x = rnd.gauss(mean, sd)
        rows.append({"t": t, "features": {"x": x}, "state": {"fam": "ok"}})
        for h in horizons:
            labels[h].append({"t": t, "state": "ok", "label_bp": 4 * (x - mean) + rnd.gauss(0, 10),
                              "label_available": t + (h + 1) * MIN})

    def provide(cutoff, start_ms=None, horizons=horizons):
        lo = cutoff - rolling_days * 24 * H if rolling_days else (start_ms if start_ms is not None else T0)
        return {"rows": [r for r in rows if lo <= r["t"] < cutoff],
                "labels": {h: [x for x in labels[h] if x["label_available"] <= cutoff and x["t"] >= lo]
                           for h in horizons if h in labels}}
    return provide


class _APIBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock = R229.Clock(T0 + 50 * H)
        self.actor = {"kind": "model", "id": "fixture-model", "version": "fixture-1", "training_cutoff": None}
        self.prov = shifted_provider()
        self.r = ResearchAPI(self.tmp.name, self.prov, "researcher", self.actor, self.clock)
        self.e = ResearchAPI(self.tmp.name, self.prov, "evaluator", {"kind": "system", "id": "evaluator"}, self.clock)
        self.r.open_experiment("X1", "SYN", E.epoch_ms(T0 + 48 * H), {"checkpoints_n": [20, 40]}, "req-open")

    def tearDown(self):
        self.tmp.cleanup()

    def transform(self, sd_override=None):
        rows = self.prov(T0 + 48 * H)["rows"]
        art = panel.fit_transform(rows, ["x"], T0 + 48 * H)
        if sd_override is not None:
            art = dict(art)
            art["params"] = {"x": dict(art["params"]["x"], sd=sd_override)}
            body = {k: v for k, v in art.items() if k != "sha256"}
            import hashlib as _h
            art["sha256"] = _h.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        return art


class F3ResearchAPITests(_APIBase):
    def test_transform_is_applied_and_changes_actions(self):
        """repo 2.29 scored raw x although the spec carried a standardising transform."""
        rows = self.prov(T0 + 48 * H)["rows"][:5]
        art = self.transform()
        spec = dict(SPEC, transform=art)
        raw = RA.actions(SPEC, rows)
        z = RA.actions(spec, rows)
        p = art["params"]["x"]
        want = []
        for r in rows:
            zz = (min(max(r["features"]["x"], p["lo"]), p["hi"]) - p["mean"]) / p["sd"]
            want.append(1 if zz > 0.5 else -1 if zz < -0.5 else 0)
        self.assertEqual(list(z.values()), want)
        self.assertEqual(set(raw.values()), {1})                          # mean 5: raw x is always "long"
        self.assertNotEqual(list(raw.values()), list(z.values()))

    def test_malformed_transforms_and_specs_are_refused(self):
        bad = [dict(SPEC, transform=self.transform(sd_override=0.0)),
               dict(SPEC, transform=dict(self.transform(), sha256="0" * 64)),
               dict(SPEC, transform={"schema": "panel-transform/1"}),
               dict(SPEC, rule=dict(SPEC["rule"], weights={"x": float("nan")})),
               dict(SPEC, rule=dict(SPEC["rule"], weights={"x": 1.0, "y": 2.0})),
               dict(SPEC, rule=dict(SPEC["rule"], long_above=-1.0, short_below=1.0)),
               dict(SPEC, horizon_min=61), dict(SPEC, features=["x", "x"]),
               dict(SPEC, rule=dict(SPEC["rule"], type="python"))]
        for i, s in enumerate(bad):
            self.assertTrue(RA.validate_spec(s), i)
            with self.assertRaises(Refused):
                self.r.register("X1", s, f"req-bad-{i}")
        rejects = [e for e in self.r.ledger.entries() if e["action"] == "reject"]
        self.assertEqual(len(rejects), len(bad))
        self.assertTrue(all(self.r.objects.has(e["objects"]["spec"]) for e in rejects))   # each attempt reproducible
        with self.assertRaises(Refused):
            self.r.register("X1", SPEC, "req-code", code_path=str(ROOT / "report.py"))

    def test_unauthorized_training_data_is_refused(self):
        rows = self.prov(T0 + 60 * H)["rows"]
        late = panel.fit_transform(rows, ["x"], T0 + 60 * H)                # fitted past the discovery cutoff
        with self.assertRaises(Refused):
            self.r.register("X1", dict(SPEC, transform=late), "req-late-fit")
        with self.assertRaises(Refused):
            self.r.run("X1", dict(SPEC, transform=late), E.epoch_ms(T0 + 40 * H), {}, "req-late-run")

    def test_candidate_edited_after_registration_is_refused(self):
        cand = self.r.register("X1", SPEC, "req-reg")
        p = Path(self.tmp.name) / "candidates" / f"X1-{cand['candidate_sha256'][:12]}.json"
        doc = json.loads(p.read_text())
        doc["spec"]["rule"]["weights"]["x"] = -1.0                          # old claimed hash kept
        p.write_text(json.dumps(doc))
        self.clock.t = T0 + 70 * H
        with self.assertRaises(Refused):
            self.e.evaluate("X1", cand["candidate_sha256"], "req-ev")
        p.unlink()                                                         # crash after the commit point: restored
        self.assertTrue(self.e.evaluate("X1", cand["candidate_sha256"], "req-ev2")["released"])
        orphan = dict(cand, candidate_sha256="ab" * 32)
        (Path(self.tmp.name) / "candidates" / f"X1-{'ab' * 6}.json").write_text(json.dumps(orphan))
        with self.assertRaisesRegex(Refused, "orphaned"):
            self.e.evaluate("X1", "ab" * 32, "req-orphan")

    def test_changed_code_needs_a_successor(self):
        cand = self.r.register("X1", SPEC, "req-reg")
        real = RA._code_objects
        try:
            RA._code_objects = lambda: {k: dict(v, sha256="0" * 64) for k, v in real().items()}
            self.clock.t = T0 + 70 * H
            with self.assertRaisesRegex(Refused, "successor"):
                self.e.evaluate("X1", cand["candidate_sha256"], "req-ev")
        finally:
            RA._code_objects = real

    def test_local_registration_time_is_not_prospective_and_anchoring_is(self):
        cand = self.r.register("X1", SPEC, "req-reg")
        self.clock.t = T0 + 70 * H
        out = self.e.evaluate("X1", cand["candidate_sha256"], "req-ev")
        self.assertIn("not externally anchored", out["evidence_class"])
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as priv:
            clock = R229.Clock(T0 + 50 * H)
            anchor = FileAnchor(Path(priv) / "anchor.jsonl")
            r = ResearchAPI(tmp, self.prov, "researcher", self.actor, clock)
            e = ResearchAPI(tmp, self.prov, "evaluator", {"kind": "system", "id": "ev"}, clock, anchor=anchor,
                            private_root=priv)
            r.open_experiment("X1", "SYN", E.epoch_ms(T0 + 48 * H), {"checkpoints_n": [20]}, "req-open")
            c = r.register("X1", SPEC, "req-reg")
            clock.t = T0 + 51 * H
            e.ledger.anchor_now(clock())                                    # the evaluator side anchors
            clock.t = T0 + 70 * H
            out = e.evaluate("X1", c["candidate_sha256"], "req-ev")
            self.assertIn("prospective confirmation", out["evidence_class"])
            self.assertEqual(out["released"][0]["confirmation_window"][0], E.iso(E.epoch_ms(T0 + 51 * H)))
            lp = Path(tmp) / "ledger.jsonl"
            lines = lp.read_text().splitlines()
            ev = json.loads(lines[1])                                     # forge an earlier registration time
            ev["t_utc"] = E.iso(E.epoch_ms(T0 + 40 * H))
            body = {k: v for k, v in ev.items() if k != "sha256"}
            ev["sha256"] = E.content_sha256(body)
            prev = ev["sha256"]
            fixed = [lines[0], E.canon(ev)]
            for x in lines[2:]:
                y = json.loads(x)
                y["prev_sha256"] = prev
                y["sha256"] = E.content_sha256({k: v for k, v in y.items() if k != "sha256"})
                prev = y["sha256"]
                fixed.append(E.canon(y))
            lp.write_text("\n".join(fixed) + "\n")                          # a fully re-hashed, consistent chain
            self.assertEqual(Ledger(lp).verify(), [])                       # unanchored: looks fine
            self.assertTrue(e.ledger.verify())                              # anchored: the rewrite is detected
            with self.assertRaises(Refused):
                e.evaluate("X1", c["candidate_sha256"], "req-ev-forged")

    def test_horizon_is_the_candidates_and_must_be_supplied(self):
        spec = dict(SPEC, horizon_min=240)
        cand = self.r.register("X1", spec, "req-reg240")
        self.clock.t = T0 + 90 * H
        out = self.e.evaluate("X1", cand["candidate_sha256"], "req-ev")
        self.assertIn("t + 240 min", out["released"][0]["membership_rule"])
        only60 = ResearchAPI(self.tmp.name, shifted_provider(horizons=(60,)), "evaluator",
                             {"kind": "system", "id": "evaluator"}, self.clock)
        with self.assertRaisesRegex(Refused, "horizon"):
            only60.evaluate("X1", cand["candidate_sha256"], "req-ev60")

    def test_checkpoint_membership_is_fixed_whatever_the_evaluation_time(self):
        """repo 2.29 released 46 scored observations under checkpoint 40."""
        shas = []
        for t_eval in (T0 + 62 * H, T0 + 75 * H, T0 + 120 * H):
            with tempfile.TemporaryDirectory() as tmp:
                clock = R229.Clock(T0 + 50 * H)
                r = ResearchAPI(tmp, self.prov, "researcher", self.actor, clock)
                e = ResearchAPI(tmp, self.prov, "evaluator", {"kind": "system", "id": "ev"}, clock)
                r.open_experiment("X1", "SYN", E.epoch_ms(T0 + 48 * H), {"checkpoints_n": [20, 40]}, "req-open")
                c = r.register("X1", SPEC, "req-reg")
                clock.t = t_eval
                out = e.evaluate("X1", c["candidate_sha256"], "req-ev")
                rel = {x["checkpoint_n"]: x for x in out["released"]}
                self.assertEqual(rel[20]["result"]["scored"], 20)
                if 40 in rel:
                    self.assertEqual(rel[40]["result"]["scored"], 40)
                shas.append(rel[20]["members_sha256"])
                again = e.evaluate("X1", c["candidate_sha256"], "req-ev-again")
                self.assertEqual(again["released"], [])                    # no extra look
                n = len([x for x in Path(tmp, "results", "X1.jsonl").read_text().splitlines() if x])
                self.assertEqual(n, len(rel))
                res = rel[20]["result"]
                self.assertEqual(res["scheduled"], res["missing_decision"] + res["abstain"] + res["taken"])
        self.assertEqual(len(set(shas)), 1)

    def test_confirmation_beyond_30_days_keeps_early_observations(self):
        cand = self.r.register("X1", SPEC, "req-reg")
        self.clock.t = T0 + 60 * H
        first = self.e.evaluate("X1", cand["candidate_sha256"], "req-ev1")["released"]
        self.assertEqual([x["checkpoint_n"] for x in first], [20])
        rolling = ResearchAPI(self.tmp.name, shifted_provider(rolling_days=30), "evaluator",
                              {"kind": "system", "id": "evaluator"}, self.clock)
        self.clock.t = T0 + 50 * H + 40 * 24 * H                           # day 40 of confirmation
        out = rolling.evaluate("X1", cand["candidate_sha256"], "req-ev2")
        rel = {x["checkpoint_n"]: x for x in out["released"]}
        self.assertEqual(rel[40]["confirmation_window"][0], cand["confirmation_starts_utc"])
        obs = RA.ObservationLog(self.tmp.name, "X1", cand["candidate_sha256"]).records()
        self.assertEqual(min(o["t"] for o in obs), T0 + 50 * H)            # the first day's decisions are kept
        self.assertEqual(rel[40]["result"]["scored"], 40)

    def test_ablation_counterexamples_and_configs_are_counted_search(self):
        spec = {"family": "SYN", "features": ["x", "x2"], "horizon_min": 60,
                "rule": {"type": "linear-score", "weights": {"x": 1.0, "x2": 0.5}, "bias": -5.0,
                         "long_above": 0.5, "short_below": -0.5}}
        prov = shifted_provider()

        def prov2(cutoff, start_ms=None, horizons=(60,)):
            d = prov(cutoff, start_ms, horizons)
            for r in d["rows"]:
                r["features"]["x2"] = r["features"]["x"] ** 2 / 10
            return d
        r = ResearchAPI(self.tmp.name, prov2, "researcher", self.actor, self.clock)
        abl = r.ablate("X1", spec, E.epoch_ms(T0 + 40 * H), "req-abl")
        self.assertEqual(sorted(abl), ["x", "x2"])
        packets = r.counterexamples("X1", spec, E.epoch_ms(T0 + 40 * H), "req-cx", k=3)
        self.assertEqual(len(packets), 3)
        self.assertTrue(all(p["action"] * p["outcome_bp"] <= 0 for p in packets))
        r.config("X1", {"kind": "prompt", "label": "v2", "text_sha256": "f" * 64}, "req-cfg")
        c = r.ledger.family_count("SYN")
        self.assertEqual((c["search_actions"]["ablation"], c["search_actions"]["counterexamples"],
                          c["search_actions"]["config"]), (2, 1, 1))


# --------------------------------------------------------------------------------------- F6 search ledger
class F6LedgerTests(_APIBase):
    def test_suffix_truncation_is_detected_against_the_anchor(self):
        with tempfile.TemporaryDirectory() as priv:
            L = Ledger(Path(self.tmp.name) / "ledger.jsonl", anchor=FileAnchor(Path(priv) / "a.jsonl"))
            for k in range(5):
                self.r.run("X1", SPEC, E.epoch_ms(T0 + 40 * H), {"max_rows": 10 + k}, f"req-{k}")
            L.anchor_now(self.clock())
            before = L.family_count("SYN")["runs_including_failures"]
            lp = Path(self.tmp.name) / "ledger.jsonl"
            lines = lp.read_text().splitlines()
            lp.write_text("\n".join(lines[:-4]) + "\n")                     # delete the last entries
            self.assertEqual(Ledger(lp).verify(), [])                       # 2.29: an intact-looking chain
            self.assertIn("unanchored", Ledger(lp).verify_report()["claim"])
            self.assertLess(Ledger(lp).family_count("SYN")["runs_including_failures"], before)
            self.assertTrue(any("suffix truncation" in p for p in L.verify()))
            with self.assertRaises(LedgerCorrupt):
                L.append("X1", self.actor, "note", {}, "req-after", self.clock())

    def test_conflicting_request_id_writes_no_candidate(self):
        self.r.ledger.append("X1", self.actor, "note", {"family": "SYN", "x": 1}, "req-reg", self.clock())
        n = len(self.r.ledger.entries())
        with self.assertRaises(Refused):
            self.r.register("X1", SPEC, "req-reg")
        self.assertFalse((Path(self.tmp.name) / "candidates").exists())   # 2.29 wrote the file first
        self.assertEqual(len(self.r.ledger.entries()), n)
        cand = self.r.register("X1", SPEC, "req-reg-ok")
        self.assertEqual(self.r.register("X1", SPEC, "req-reg-ok"), cand)  # a retry is idempotent
        self.assertEqual(self.r.ledger.family_count("SYN")["registered_candidates"], 1)

    def test_torn_final_line_is_repaired_and_recorded(self):
        self.r.run("X1", SPEC, E.epoch_ms(T0 + 40 * H), {}, "req-run")
        lp = Path(self.tmp.name) / "ledger.jsonl"
        with open(lp, "ab") as f:
            f.write(b'{"id": "S00009", "prev_sha')                         # a crash mid-write
        with self.assertRaises(LedgerCorrupt):
            self.r.ledger.entries()
        rep = self.r.ledger.repair(self.clock())
        self.assertEqual(rep["action"], "repair")
        self.assertEqual(self.r.ledger.verify(), [])
        self.assertTrue(list(Path(self.tmp.name).glob("ledger.jsonl.torn-*")))

    def test_simultaneous_appends_keep_one_chain(self):
        import multiprocessing as mp
        lp = str(Path(self.tmp.name) / "conc.jsonl")
        ctx = mp.get_context("fork")
        ps = [ctx.Process(target=_appender, args=(lp, w)) for w in range(4)]
        for p in ps:
            p.start()
        for p in ps:
            p.join(60)
        L = Ledger(lp)
        self.assertEqual(L.verify(), [])
        self.assertEqual(len(L.entries()), 4 * 15)

    def test_researcher_cannot_read_unreleased_results_through_a_separate_evaluator(self):
        if os.geteuid() != 0:
            self.skipTest("OS-user separation needs root to start a second user; boundary not tested here")
        import socket as _s
        import subprocess
        import pwd
        nobody = pwd.getpwnam("nobody")
        shared, priv = Path(self.tmp.name), Path(tempfile.mkdtemp())
        sock = str(Path(tempfile.mkdtemp()) / "ev.sock")
        os.chmod(Path(sock).parent, 0o755)
        cand = self.r.register("X1", SPEC, "req-reg")
        for d, _, fs in os.walk(shared):
            os.chmod(d, 0o777)
            for f in fs:
                os.chmod(os.path.join(d, f), 0o666)
        script = (f"import sys; sys.path[:0]=[{str(ROOT)!r},{str(ROOT / 'regression')!r}]\n"
                  "import test_rev230 as T, test_rev229 as R\n"
                  "from research_tools import evaluator_service as S\n"
                  f"svc=S.Service({str(shared)!r},{str(priv)!r},T.shifted_provider(),R.Clock(R.T0+70*R.H))\n"
                  f"S.serve(svc,{sock!r},max_requests=3)\n")
        srv = subprocess.Popen([sys.executable, "-c", script])
        try:
            for _ in range(100):
                if os.path.exists(sock):
                    break
                import time as _t
                _t.sleep(0.1)
            from research_tools import evaluator_service as S
            out = S.Client(sock).call({"op": "evaluate", "experiment": "X1", "candidate_sha256": cand["candidate_sha256"],
                                       "request_id": "req-svc-ev"})
            self.assertTrue(out["released"])
            probe = (f"import sys, json; sys.path[:0]=[{str(ROOT)!r}]\n"
                     "from research_tools import evaluator_service as S\n"
                     "try:\n"
                     f"    open({str(priv / 'results' / 'X1.jsonl')!r}).read(); print('READ')\n"
                     "except PermissionError:\n    print('DENIED')\n"
                     f"r=S.Client({sock!r}).call({{'op':'released','experiment':'X1','candidate_sha256':{cand['candidate_sha256']!r}}})\n"
                     "print(len(r['records']), all(x['released'] for x in r['records']))\n")

            def demote():
                os.setgid(nobody.pw_gid)
                os.setuid(nobody.pw_uid)
            p = subprocess.run([sys.executable, "-c", probe], preexec_fn=demote, capture_output=True, text=True,
                               timeout=60)
            self.assertEqual(p.returncode, 0, p.stderr)
            lines = p.stdout.split()
            self.assertEqual(lines[0], "DENIED")
            self.assertEqual(lines[-1], "True")
            S.Client(sock).call({"op": "anchor"})
            self.assertTrue((priv / "ledger-anchor.jsonl").exists())
        finally:
            srv.wait(30)
        del _s


def _appender(lp, w):
    L = Ledger(lp)
    for k in range(15):
        L.append("X", {"kind": "system", "id": f"w{w}"}, "note", {"k": k}, f"w{w}-{k}", "2026-10-12T00:00:00Z")


# ------------------------------------------------------------------------------------------ F4 DIR1 runner
from research_tools import directional as DIR  # noqa: E402
from research_tools import dir1_runner as RUN  # noqa: E402

PROTO = json.loads((ROOT / "research/registrations/dir1-prepared/protocol.json").read_text())


def fx_row(t, age_s=300, **feat):
    f = {"ret_1h_bp": 12.0, "flow_per_depth": 0.02, "d_oi_1h_pct": 0.1}
    f.update(feat)
    src = {s: {"age_s": age_s, "state": "ok"} for s in ("perp_window", "depth", "oi", "basis", "funding_estimate")}
    return {"t": t, "features": {k: v for k, v in f.items() if v is not None},
            "fstate": {k: ("ok" if v is not None else "source-missing") for k, v in f.items()},
            "inputs": {"sources": src}}


class FixedClock:
    def __init__(self, t):
        self.t = t

    def __call__(self):
        return E.epoch_ms(int(self.t))


def stat_art():
    a = {"schema": "directional-statistical/1", "features": ["ret_1h_bp"], "coef": [0.002], "intercept": 0.0,
         "train_cutoff_utc": E.iso(E.epoch_ms(T0))}
    a["sha256"] = E.content_sha256(a)
    return a


class F4RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = T0 + 4 * H
        self.clock = FixedClock(self.d + 30_000)
        self.rows = {self.d: fx_row(self.d), self.d + H: fx_row(self.d + H)}
        self.bars = R229.fixture_bars(14)
        self.proto = dict(PROTO, inference=dict(PROTO["inference"], timeout_s=1.0))

    def tearDown(self):
        self.tmp.cleanup()

    def runner(self, adapters=None, main=None, rows=None, instrument=None, mode="fixture", proto=None):
        main = main or RUN.FixtureMain(self.clock, delay_ms=60_000)
        ps = RUN.FixturePanelSource(rows if rows is not None else self.rows,
                                    instrument or PROTO["instrument"]["target"])
        ad = adapters if adapters is not None else {
            "baseline": RUN.CallableAdapter("baseline", DIR.baseline_arm(PROTO)),
            "statistical": RUN.CallableAdapter("statistical", DIR.statistical_arm(stat_art()))}
        return RUN.DIR1Runner(proto or self.proto, self.tmp.name, mode, ad, main, main, ps, self.clock)

    def test_reviewed_grade_defects_are_refused(self):
        """1.0.0: grade() returned 'graded' with no publication evidence, a wrong hash and p_up 2.0."""
        g = DIR.grade(PROTO, self.d, 2.0, None, self.bars, evaluation_cutoff_ms=T0 + 14 * H)
        self.assertEqual(g["state"], "refused")
        self.assertEqual(DIR.grade(PROTO, self.d, 0.6, None, self.bars, T0 + 14 * H)["state"], "refused")
        self.assertEqual(DIR.grade(PROTO, self.d, 0.6, {"class": "failed"}, self.bars, T0 + 14 * H)["state"], "refused")
        self.assertEqual(DIR.grade(PROTO, self.d, 0.6, {"class": "on-time", "published_utc": E.iso(E.epoch_ms(self.d))},
                                   self.bars)["state"], "refused")                    # no evaluation cutoff
        main = RUN.FixtureMain(self.clock)
        content = {"opportunity": "x", "p_up": 0.6}
        ev = main.publish(content)
        self.assertEqual(DIR.admit(PROTO, self.d, dict(content, p_up=0.7), ev, main)["class"], "failed")  # wrong hash
        self.assertEqual(DIR.admit(PROTO, self.d, content, {"kind": "git-commit", "ref": "nope"}, main)["class"], "failed")

    def test_malformed_outputs_never_raise_and_are_recorded(self):
        for raw in ("true", "42", "[1]", True, 42, [0.5], {"p_up": True}, {"p_up": 2.0}, {"p_up": float("nan")}, b"\xff"):
            p, why = DIR.parse_forecast(raw)
            self.assertIsNone(p, raw)
            self.assertTrue(why)
        r = DIR.infer(lambda f, k: ({"p_up": float("nan")}, 0.0), {}, PROTO, R229.Tick(T0))
        self.assertEqual(r["outcome"], "error")
        self.assertIn("NaN", r["attempts"][0]["raw_text"])

    def test_operational_entry_point_accounts_for_every_opportunity(self):
        rows = dict(self.rows)
        rows[self.d + 2 * H] = fx_row(self.d + 2 * H, flow_per_depth=None)          # missing input
        rows[self.d + 3 * H] = fx_row(self.d + 3 * H, age_s=1200)                   # stale input
        run = self.runner(rows=rows)
        for k in range(5):                                                         # k = 4: no row at all
            self.clock.t = self.d + k * H + 30_000
            run.run(self.d + k * H)
        self.clock.t = self.d + 5 * H + 30_000
        acct = run.reconcile(self.d, self.d + 6 * H, self.clock())                  # the 6th not run yet: expected
        self.assertEqual(acct["baseline"].get("expected"), 1)
        self.clock.t = self.d + 5 * H + 700_000
        acct = run.reconcile(self.d, self.d + 6 * H, self.clock())                  # past its deadline: missed
        for arm in ("baseline", "statistical", "frontier"):
            self.assertEqual(sum(acct[arm].values()), 6)
        self.assertEqual(acct["frontier"], {"inputs-unavailable": 5, "missed": 1})  # uncommissioned, still counted
        self.assertEqual(acct["baseline"].get("inputs-unavailable"), 3)
        out = run.grade_matured(self.bars, evaluation_cutoff_ms=self.d + 4 * H)     # outcomes not yet available
        self.assertEqual(out["graded"], 0)
        out = run.grade_matured(self.bars, evaluation_cutoff_ms=T0 + 14 * H)
        self.assertEqual(out["graded"], 4)                                         # 2 decisions x 2 arms
        self.assertEqual(run.results.verify(), [])
        g = run.results.records()[0]
        self.assertIn("price proxy", g["grade"]["price_basis"])
        self.assertTrue(g["fixture"])
        self.assertIsNone(g["grade"]["net_bp"] if g["grade"]["action"] else None)  # no funding supplied: not zero
        reasons = [e["data"].get("reasons") for e in run.log.events if e["state"] == "inputs-unavailable"
                   and e["arm"] == "baseline"]
        self.assertTrue(any("flow_per_depth" in " ".join(r or []) for r in reasons))
        self.assertTrue(any("1200 s old" in " ".join(r or []) for r in reasons))

    def test_wrong_instrument_and_unregistered_protocol_are_refused(self):
        run = self.runner(instrument="Binance spot BTCUSDT")
        run.run(self.d)
        self.assertEqual(run.log.state(DIR.opp_id(PROTO, self.d, "baseline")), "inputs-unavailable")
        with self.assertRaisesRegex(RUN.Refused, "fixture"):
            self.runner(mode="operational")
        ok = RUN.GitHubMainVerifier("o/r", gh=lambda a: {})
        op = RUN.DIR1Runner(self.proto, self.tmp.name + "/op", "operational",
                            {"baseline": RUN.CallableAdapter("baseline", DIR.baseline_arm(PROTO))}, ok, ok,
                            RUN.FixturePanelSource(self.rows), self.clock)
        with self.assertRaisesRegex(RUN.Refused, "prepared"):
            op.run(self.d)

    def test_publication_late_tampered_and_failed(self):
        late = self.runner(main=RUN.FixtureMain(self.clock, delay_ms=700_000))
        late.run(self.d)
        self.assertEqual(late.log.state(DIR.opp_id(PROTO, self.d, "baseline")), "publish-late")
        late.grade_matured(self.bars, T0 + 14 * H)
        self.assertEqual(late.results.records()[0]["grade"]["admission"], "late")
        for main in (RUN.FixtureMain(self.clock, tamper=True), RUN.FixtureMain(self.clock, fail=True)):
            with tempfile.TemporaryDirectory() as tmp:
                r = RUN.DIR1Runner(self.proto, tmp, "fixture",
                                   {"baseline": RUN.CallableAdapter("baseline", DIR.baseline_arm(PROTO))}, main, main,
                                   RUN.FixturePanelSource(self.rows), self.clock)
                r.run(self.d)
                self.assertEqual(r.log.state(DIR.opp_id(PROTO, self.d, "baseline")), "publish-failed")
                self.assertEqual(r.grade_matured(self.bars, T0 + 14 * H)["graded"], 0)

    def test_hung_model_call_is_cancelled_at_the_deadline(self):
        import time as _t
        fx = RUN.FixtureAdapter("frontier", [("sleep", 30), ("sleep", 30)])
        run = self.runner(adapters={"frontier": fx})
        t0 = _t.monotonic()
        run.run(self.d)
        took = _t.monotonic() - t0
        self.assertLess(took, 8)                                                   # 2 attempts x 1 s, not 60 s
        oid = DIR.opp_id(PROTO, self.d, "frontier")
        self.assertEqual(run.log.state(oid), "timeout")
        ev = run.log.history(oid)[-1]["data"]
        atts = run.objects.get(ev["attempts_object"])
        self.assertEqual([a["parse"][:7] for a in atts], ["timeout", "timeout"])
        self.assertTrue(all(a["cost_usd"] is None and "cancelled" in a["cost_state"] for a in atts))
        self.assertIsNone(ev["cost_usd"])                                           # unknown, not zero

    def test_first_valid_parse_with_malformed_outputs_through_the_runner(self):
        fx = RUN.FixtureAdapter("frontier", ["true", {"p_up": 0.61}, {"p_up": 0.9}])
        run = self.runner(adapters={"frontier": fx})
        run.run(self.d)
        oid = DIR.opp_id(PROTO, self.d, "frontier")
        fc = next(e for e in run.log.history(oid) if e["state"] == "forecast")["data"]
        self.assertEqual((fc["selected_attempt"], fc["p_up"], fc["n_attempts"]), (1, 0.61, 2))
        atts = run.objects.get(fc["attempts_object"])
        self.assertEqual(run.objects.get(atts[0]["raw_object"])["raw_text"], "true")

    def test_restart_and_duplicate_invocation(self):
        run = self.runner()
        run.run(self.d)
        n = len(run.log.events)
        run.run(self.d)                                                            # duplicate invocation
        self.assertEqual(len(run.log.events), n)
        again = self.runner()                                                      # a fresh process: reload
        self.assertEqual(len(again.log.events), n)
        oid = DIR.opp_id(PROTO, self.d + H, "baseline")
        again.log.add(oid, "baseline", "expected", E.epoch_ms(self.d + H), {"decision_t_utc": E.iso(E.epoch_ms(self.d + H)),
                                                                             "fixture": True})
        pk = again.objects.put({"features": {"ret_1h_bp": 4.0}})
        again.log.add(oid, "baseline", "inputs-ready", self.clock(), {"packet_object": pk, "fixture": True})
        again.log.add(oid, "baseline", "inference-started", self.clock(), {"packet_object": pk})   # then a crash
        self.clock.t = self.d + H + 30_000
        third = self.runner()
        third.run(self.d + H)
        h = third.log.history(oid)
        fc = next(e for e in h if e["state"] == "forecast")["data"]
        atts = third.objects.get(fc["attempts_object"])
        self.assertEqual(atts[0]["attempt"], "interrupted")
        self.assertEqual(len(atts), 2)                                              # max_attempts 2 kept
        with open(third.log.path, "ab") as f:
            f.write(b'{"opportunity": "torn')
        fourth = self.runner()
        self.assertTrue(fourth.log.recovered)
        p = third.log.path
        lines = p.read_text().splitlines()
        p.write_text("\n".join(lines[:2] + lines[3:]) + "\n")
        with self.assertRaises(RUN.LogCorrupt):
            self.runner()

    def test_github_main_verifier_uses_server_records_not_commit_dates(self):
        import base64 as b64
        content = {"opportunity": "o", "p_up": 0.6}
        sha = "a" * 40
        calls = []

        def gh(args):
            calls.append(args[0])
            a = args[0]
            if "/contents/" in a:
                return {"content": b64.b64encode(json.dumps(content).encode()).decode()}
            if "/compare/" in a:
                base, head = a.split("/compare/")[1].split("...")
                return {"status": "identical" if base == head or head in ("main", "c" * 40) else "behind"}
            if "/activity" in a:
                return [{"id": 1, "after": "b" * 40, "timestamp": "2026-10-12T04:00:30Z"},
                        {"id": 2, "after": "c" * 40, "timestamp": "2026-10-12T04:02:10Z"}]
            raise AssertionError(a)
        v = RUN.GitHubMainVerifier("o/r", gh=gh)
        ok, first, why, rc = v.verify({"kind": "git-commit", "ref": sha, "path": "streams/dir1/o.json",
                                       "published_utc": "2026-10-12T03:00:00Z"}, content)
        self.assertTrue(ok, why)
        self.assertEqual(first, "2026-10-12T04:02:10Z")                            # the push that contained it
        self.assertFalse(v.verify({"kind": "git-commit", "ref": sha, "path": "x"}, dict(content, p_up=0.7))[0])


# ------------------------------------------------------------------------------------------ F5 comparisons
class F5ComparisonTests(unittest.TestCase):
    def g(self, b, adm="on-time"):
        return {"state": "graded", "brier": b, "admission": adm, "action": 1, "utility_bp": 1.0, "net_bp": 0.5}

    def test_registered_primary_is_statistical_minus_baseline(self):
        graded = {"baseline": {1: self.g(0.25)}, "statistical": {1: self.g(0.16)}, "frontier": {1: self.g(0.36)}}
        c = DIR.compare_arms(graded, PROTO, schedule=[1])
        self.assertEqual(c["comparisons"]["primary"]["difference"], "statistical - baseline")
        self.assertAlmostEqual(c["comparisons"]["primary"]["mean_difference"], -0.09, places=9)
        rev = dict(reversed(list(graded.items())))
        self.assertEqual(DIR.compare_arms(rev, PROTO, [1])["comparisons"]["primary"], c["comparisons"]["primary"])
        self.assertIsNone(DIR.compare_arms(graded)["comparisons"])                 # no protocol: nothing invented

    def test_pair_specific_intersections_and_schedule_denominators(self):
        sched = [1, 2, 3, 4]
        graded = {"baseline": {1: self.g(0.25), 2: self.g(0.20), 3: self.g(0.30)},
                  "statistical": {1: self.g(0.16), 2: self.g(0.18), 3: self.g(0.10, adm="late")},
                  "frontier": {1: {"state": "timeout"}, 2: {"state": "error"}},
                  "challenger": {1: {"state": "error"}}}                            # a failed extra arm
        c = DIR.compare_arms(graded, PROTO, schedule=sched)
        pc = c["comparisons"]["primary"]
        self.assertEqual(pc["n_pair"], 2)                                          # the frontier failures erase nothing
        self.assertAlmostEqual(pc["mean_difference"], ((0.16 - 0.25) + (0.18 - 0.20)) / 2, places=9)
        self.assertEqual(pc["scheduled"], 4)
        self.assertEqual(pc["not_valid"], {"statistical": 2, "baseline": 1})       # late 3 and absent 4; absent 4
        self.assertEqual(c["opportunities"], 4)                                    # opportunity 4: every arm missing
        self.assertEqual(c["arms"]["baseline"]["states"]["missing"], 1)
        self.assertEqual(c["arms"]["statistical"]["graded_late"], 1)
        self.assertEqual(c["paired_intersection"], 0)

    def test_numeric_abstention_is_scored_for_quality_and_trades_nothing(self):
        bars = R229.fixture_bars(14)
        d = T0 + 4 * H
        adm = {"class": "on-time", "published_utc": E.iso(E.epoch_ms(d + 90_000))}
        g = DIR.grade(PROTO, d, 0.5, adm, bars, evaluation_cutoff_ms=T0 + 14 * H)
        self.assertEqual((g["state"], g["action"], g["net_bp"]), ("graded", 0, 0.0))
        self.assertIsNotNone(g["brier"])
        late = DIR.grade(PROTO, d, 0.5, dict(adm, published_utc=E.iso(E.epoch_ms(d + 20 * MIN))), bars, T0 + 14 * H)
        self.assertEqual(late["target_bp"], g["target_bp"])                       # the common target does not move
        self.assertNotEqual(late["entry_utc"], g["entry_utc"])                    # execution stays latency-aware
        fund = [{"t": T0 + 8 * H, "rate": 1e-4}]
        g2 = DIR.grade(PROTO, d, 0.8, adm, bars, T0 + 14 * H, funding=fund, inference_usd=0.01)
        self.assertEqual(g2["funding_bp"], 1.0)                                    # a long pays a positive rate
        self.assertEqual(g2["inference_usd"], 0.01)


# ------------------------------------------------------------------------------------------ F7 E1 acceptance
import gzip  # noqa: E402
import hashlib  # noqa: E402
from stream import pilot_acceptance as PA  # noqa: E402

CRIT = json.loads((ROOT / "stream/pilot_e1.json").read_text())
TCRIT = dict(CRIT, duration_days=1, evidence_target_shocks=2, shock_window_min=10)
S0 = T0 + 24 * H                                                           # pilot start: Oct 13 00:00


def _gz(rows):
    return gzip.compress(("\n".join(json.dumps(r, separators=(",", ":")) for r in rows) + "\n").encode(), 6, mtime=0)


def make_pilot(root, hours=3, shocks=(70, 140), faults=()):
    """A complete recorder directory for both scoped books over `hours` from S0 (plus one warm-up hour): raw book
    messages (a snapshot, then one delta per second), the 1-second samples the recorder would derive, clock samples
    every 10 minutes, mid-move triggers at the given minutes with captures, and a manifest of every partition."""
    root = Path(root)
    manifest = []

    def put(key, data):
        p = root / key
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        manifest.append({"key": key, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                         "uploaded_at": S0 + hours * H})
    for venue, inst in CRIT["scope"]["venues_instruments"]:
        ch = PA.BOOK_CHANNELS[venue].format(inst=inst)
        book = PA._new_book(venue, inst)
        cid = 0
        for h in range(-1, hours):
            hs = S0 + h * H
            day, hh = PA._day_hour(hs)
            raw, der = [], []
            for s in range(3600):
                t = hs + s * 1000
                k = (h + 1) * 3600 + s
                px = 80000.0 + (k % 7) * 0.5 + (40.0 if any(abs(k - (m + 60) * 60) < 2 for m in shocks) else 0.0)
                cid += 1
                if venue == "deribit":
                    data = {"instrument_name": inst if "wrong-id" not in faults else "ETH-PERPETUAL", "timestamp": t,
                            "change_id": cid, "bids": [["new", px - 0.5, 10.0]], "asks": [["new", px + 0.5, 10.0]]}
                    data["type" if cid == 1 else "prev_change_id"] = "snapshot" if cid == 1 else cid - 1
                    if cid > 1:
                        data["bids"] = [["delete", p_, 0] for p_ in list(book.bids)] + data["bids"]
                        data["asks"] = [["delete", p_, 0] for p_ in list(book.asks)] + data["asks"]
                    msg = {"jsonrpc": "2.0", "method": "subscription", "params": {"channel": ch, "data": data}}
                    book.apply(data)
                else:
                    data = {"s": inst, "u": cid, "b": [[str(px - 0.5), "10"]] + [[str(p_), "0"] for p_ in book.bids],
                            "a": [[str(px + 0.5), "10"]] + [[str(p_), "0"] for p_ in book.asks]}
                    msg = {"topic": ch, "type": "snapshot" if cid == 1 else "delta", "ts": t, "data": data}
                    book.apply(msg)
                raw.append({"r": t + 1, "m": json.dumps(msg)})
                top = book.top()
                mid = top[2] + (25.0 if "fabricated" in faults and venue == "bybit" and h == 1 else 0.0)
                der.append({"t": t + 5, "bid": top[0], "ask": top[1], "mid": mid, "book_ts": t,
                            "book_age_ms": 5 if not ("stale-bybit" in faults and venue == "bybit") else 5000})
            skip_raw = ("missing-raw" in faults and venue == "deribit" and h == 1)
            if "missing-day" in faults and h in (0, 1, 2) and venue == "deribit":
                continue
            rk = f"raw/{venue}/{ch}/{day}/{hh}.jsonl.gz"
            put(rk, _gz(raw))
            if skip_raw:
                (root / rk).unlink()
            if "corrupt-raw" in faults and venue == "deribit" and h == 1:
                (root / rk).write_bytes(_gz(raw[:-1]))
            put(f"derived/book1s/{venue}/{inst}/{day}/{hh}.jsonl.gz", _gz(der))
    for m in range(0, hours * 60, 10):
        t = S0 + m * 60_000
        day = PA._day_hour(t)[0]
        p = root / "derived/clock" / f"{day}.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        off = 400.0 if ("clock" in faults and m >= 60) else 4.0
        with open(p, "a") as f:
            f.write(json.dumps({"venue": "deribit", "t": t, "offset_ms": off, "rtt_ms": 20}) + "\n")
    for i, m in enumerate(shocks):
        t = S0 + m * 60_000
        day = PA._day_hour(t)[0]
        cap = f"{day}-trigger-{t}"
        with open(root / "derived/triggers" / f"{day}.jsonl" if (root / "derived/triggers").exists()
                  else (root / "derived/triggers").mkdir(parents=True) or root / "derived/triggers" / f"{day}.jsonl", "a") as f:
            f.write(json.dumps({"capture_id": cap, "kind": "trigger", "t": t,
                                "detail": {"key": "deribit:BTC-PERPETUAL"}}) + "\n")
        put(f"captures/{day}/{cap}.jsonl.gz", _gz([{"r": t, "m": "{}"}]))
    (root / "manifest").mkdir(exist_ok=True)
    (root / "manifest" / "2026-10-13.jsonl").write_text("".join(json.dumps(m) + "\n" for m in manifest))
    return root


class F7PilotAcceptanceTests(unittest.TestCase):
    def ev(self, faults=(), hours=3, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            make_pilot(tmp, hours=hours, faults=faults, **kw)
            return PA.evaluate(tmp, TCRIT, PA._iso(S0), PA._iso(S0 + hours * H), eligible_shocks=25)

    def test_complete_valid_control_passes_with_the_early_stop(self):
        r = self.ev()
        self.assertEqual(r["verdict"], "pass", r["findings"] + r["unverifiable"])
        self.assertEqual(r["shocks"]["eligible"], 2)
        self.assertEqual(r["stopped_early_utc"], PA._iso(S0 + 150 * 60_000))     # target reached: registered stop
        self.assertEqual(r["claimed_shocks_ignored"], 25)

    def test_reviewed_false_pass_cannot_pass(self):
        """1.0.0 passed partial days, a missing day, a missing raw object and a claimed 25 shocks."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for day in ("2026-10-12", "2026-10-14", "2026-10-15"):              # no 2026-10-13
                for venue, inst in CRIT["scope"]["venues_instruments"]:
                    p = root / "derived/book1s" / venue / inst / day / "00.jsonl.gz"
                    p.parent.mkdir(parents=True, exist_ok=True)
                    d0 = PA._ms(day + "T00:00:00Z")
                    n = 86400 if day == "2026-10-14" else 3600
                    p.write_bytes(_gz([{"t": d0 + s * 1000 + 3, "book_age_ms": 300} for s in range(n)]))
            (root / "manifest").mkdir()
            (root / "manifest/2026-10-14.jsonl").write_text(json.dumps({"key": "raw/deribit/x/2026-10-14/00.jsonl.gz",
                                                                       "bytes": 10, "sha256": "0" * 64}) + "\n")
            r = PA.evaluate(root, CRIT, "2026-10-12T00:00:00Z", "2026-10-16T00:00:00Z", eligible_shocks=25)
            self.assertEqual(r["verdict"], "fail")
            self.assertTrue(any("2026-10-13" in f for f in r["findings"]))
            self.assertEqual(r["shocks"]["eligible"], 0)
            self.assertEqual(r["partitions_verified"], 0)

    def test_each_defect_prevents_a_pass(self):
        for fault, needle in (("missing-raw", "missing"), ("corrupt-raw", "wrong-"), ("fabricated", "not reproducible"),
                              ("wrong-id", "another instrument"), ("clock", "clock offset"),
                              ("stale-bybit", "bybit/BTCUSDT")):
            r = self.ev(faults=(fault,))
            self.assertNotEqual(r["verdict"], "pass", fault)
            text = " ".join(r["findings"] + r["unverifiable"])
            self.assertIn(needle, text, fault)

    def test_missing_middle_hours_and_missing_recovery_history(self):
        r = self.ev(faults=("missing-day",), hours=4)
        self.assertEqual(r["verdict"], "fail")
        self.assertTrue(r["stop_conditions"])                                   # consecutive unverifiable partitions
        r2 = self.ev(shocks=(70, 175))                                          # the second shock's recovery is cut off
        self.assertEqual(r2["shocks"]["eligible"], 1)
        self.assertEqual(r2["verdict"], "inconclusive")

    def test_restore_through_the_backend_when_the_local_cache_is_gone(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as remote:
            root = make_pilot(tmp)
            for p in list(root.rglob("raw/**/*.gz")):
                dest = Path(remote) / p.relative_to(root)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(p.read_bytes())
                p.unlink()                                                      # local raw cache cleared

            class Backend:
                def get(self, key):
                    return (Path(remote) / key).read_bytes()
            r = PA.evaluate(root, TCRIT, PA._iso(S0), PA._iso(S0 + 3 * H), backend=Backend())
            self.assertEqual(r["verdict"], "pass", r["unverifiable"][:3])
            self.assertEqual(PA.evaluate(root, TCRIT, PA._iso(S0), PA._iso(S0 + 3 * H))["verdict"], "fail")

    def test_recorder_writes_clock_samples(self):
        from stream import service as SV
        from stream.storage import LocalStore
        with tempfile.TemporaryDirectory() as tmp:
            rec = SV.Recorder({}, LocalStore(tmp))
            c = SV.Connection("deribit", {"url": "wss://x", "channels": []}, rec, None)
            c.clock_sent = S0
            c.handle(json.dumps({"jsonrpc": "2.0", "id": 7, "result": S0 + 30}), S0 + 40)
            rec.store.flush()
            rows = rec.store.read(f"derived/clock/{PA._day_hour(S0)[0]}.jsonl")
            self.assertEqual((rows[0]["offset_ms"], rows[0]["rtt_ms"]), (10.0, 40))


# ------------------------------------------------------------------------------------------ F9 archive
from research_tools import archive_store as AS  # noqa: E402

RAW = json.dumps([[T0, "1", "2", "0.5", "1.5", "3", T0 + 59999, "4.5", 7, "1", "1.5", "0"]]).encode()
META = {"source": "binance", "url_or_channel": "fapi/v1/klines", "retrieved_utc": "2026-10-12T00:01:00Z",
        "event_utc": "2026-10-12T00:00:00Z", "parser": "parse_binance_klines", "parser_version": "1",
        "provenance": "original"}


class MockBackend:
    """A realistic in-memory object store with injectable faults. A mock is never a live archive."""
    def __init__(self, fault=None):
        self.objects, self.fault = {}, fault

    def put(self, key, data):
        if self.fault == "interrupt":
            self.objects[key] = data[: len(data) // 2]
            raise ConnectionResetError("upload interrupted")
        self.objects[key] = data

    def get(self, key):
        d = self.objects.get(key)
        if d is not None and self.fault == "wrong-size":
            return d[:-1]
        if d is not None and self.fault == "wrong-hash":
            return d[:5] + (b"X" if d[5:6] != b"X" else b"Y") + d[6:]
        return d


class F9ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock = FixedClock(T0 + 2 * MIN)

    def tearDown(self):
        self.tmp.cleanup()

    def store(self, backend=None, **kw):
        return AS.ArchiveStore(self.tmp.name, backend=backend, clock=self.clock, **kw)

    def test_raw_corruption_fails_even_when_the_parse_is_unchanged(self):
        """1.0.0: a whitespace change made verify() fail but replay() return ok."""
        a = self.store()
        line = a.put(RAW, META, AS.parse_binance_klines(RAW), parser=AS.parse_binance_klines)
        self.assertEqual(a.replay(line, AS.parse_binance_klines)["state"], "ok")
        p = Path(self.tmp.name) / line["key"]
        spaced = RAW.replace(b",", b", ")
        self.assertEqual(AS.parse_binance_klines(spaced), AS.parse_binance_klines(RAW))   # same rows
        p.write_bytes(spaced)
        self.assertEqual(a.replay(line, AS.parse_binance_klines)["state"], "integrity-failed")
        self.assertTrue(a.verify([line]))

    def test_repeated_put_verifies_the_existing_object(self):
        a = self.store()
        line = a.put(RAW, META)
        (Path(self.tmp.name) / line["key"]).write_bytes(b"not the bytes")
        line2 = a.put(RAW, META)
        self.assertEqual(line2["durability"]["local"]["state"], "written")
        self.assertEqual(a.verify([line2]), [])
        self.assertTrue(list((Path(self.tmp.name) / "quarantine").iterdir()))
        self.assertEqual(a.accounting(a.manifest.lines())["repeated_observations"], 1)
        self.assertEqual(a.accounting(a.manifest.lines())["unique_bytes"], len(RAW))

    def test_clock_separation_and_backend_durability(self):
        b = MockBackend()
        a = self.store(backend=b, backend_name="mock-s3")
        line = a.put(RAW, META, AS.parse_binance_klines(RAW))
        self.assertEqual((line["state"], line["durable_scope"]), ("durable", "backend"))
        self.assertEqual(line["first_durable_utc"], E.iso(self.clock()))
        self.assertNotEqual(line["first_durable_utc"], line["retrieved_utc"])
        self.assertNotEqual(line["retrieved_utc"], line["event_utc"])
        rec = a.put(RAW, dict(META, provenance="reconstructed"))
        self.assertEqual(rec["historical_availability"], "unknown (reconstructed)")
        self.assertEqual(a.manifest.verify(), [])

    def test_restore_from_the_backend_after_the_local_cache_is_cleared(self):
        b = MockBackend()
        a = self.store(backend=b)
        line = a.put(RAW, META, AS.parse_binance_klines(RAW), parser=AS.parse_binance_klines)
        import shutil
        shutil.rmtree(Path(self.tmp.name) / "objects")
        r = a.replay(line, AS.parse_binance_klines)
        self.assertEqual(r["state"], "ok")
        self.assertEqual(r["rows"], AS.parse_binance_klines(RAW))
        self.assertTrue((Path(self.tmp.name) / line["key"]).exists())            # restored and re-verified

    def test_interrupted_upload_wrong_size_wrong_hash_and_missing(self):
        for fault in ("interrupt", "wrong-size", "wrong-hash"):
            with tempfile.TemporaryDirectory() as tmp:
                a = AS.ArchiveStore(tmp, backend=MockBackend(fault), clock=self.clock)
                line = a.put(RAW, META, AS.parse_binance_klines(RAW))
                self.assertEqual(line["state"], "local-only", fault)
                self.assertEqual(line["durable_scope"], "local", fault)
                self.assertIn("error", line["durability"]["backend"], fault)
                (Path(tmp) / line["key"]).unlink()
                self.assertIn(a.replay(line, AS.parse_binance_klines)["state"], ("unavailable",), fault)

    def test_parser_identity_budget_and_retention(self):
        a = self.store(budget=AS.Budget(max_bytes_per_day=len(RAW) + 10))
        line = a.put(RAW, META, AS.parse_binance_klines(RAW), parser=AS.parse_binance_klines)

        def parse_binance_klines(raw):                                        # same name, different code
            return []
        self.assertEqual(a.replay(line, parse_binance_klines)["state"], "parser-mismatch")
        a.put(RAW, META)                                                     # a repeat stores nothing new
        with self.assertRaises(AS.BudgetExceeded):
            a.put(RAW + b" ", META)
        self.assertEqual(AS.ArchiveStore.retention_candidates(a.manifest.lines(), 1, "2026-10-20T00:00:00Z"), [])
