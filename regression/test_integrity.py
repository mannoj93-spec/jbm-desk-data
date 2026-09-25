"""Research-integrity regressions for lab-2.0 (CHANGELOG 2.8). Each class reproduces a finding of
the review of 2.7 (commit 900d0b1) and pins the corrected behaviour:

  2  outcome independence and sample counting          OverlapTests
  3  point-in-time feature availability                AvailabilityTests, FreezeTests
  4  evaluation versions and promotion                 VersionTests
  5  transfer and liquidation attribution              AttributionTests
  6  streaming timing tolerance                        StreamTimingTests
  7  option quote quality                              OptionQualityTests
  8  report provenance and non-rewinding persistence   PersistenceTests

Offline; synthetic data lives only in temporary directories.
"""
import gzip
import io
import json
import math
import os
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from lab import experiments, hlevidence, outcomes, stats, versioning
from lab.asof import ASSUMED_PROCESSING_MS, LATE_INPUT_MAX_MS
from lab.baseline import Baseline
from lab.common import H, MINUTE
from lab.events import event_record
from lab.modules import accounts, cross_asset, flow_absorption, liq_exposure, liquidity, options_disagreement
from stream import service, storage
from stream.books import BybitBook

ROOT = Path(__file__).resolve().parents[1]
T0 = 1_790_121_600_000                     # 2026-09-23 00:00 UTC
DAY = 86_400_000


def bars(prices, start=T0, lag=0, tbv_share=0.5):
    out, prev = {}, prices[0]
    for i, p in enumerate(prices):
        t = start + i * MINUTE
        out[t] = {"t": t, "o": prev, "h": max(prev, p) * 1.0001, "l": min(prev, p) * 0.9999, "c": p, "v": 10.0,
                  "tbv": 10.0 * tbv_share, "avail": t + MINUTE + lag}
        prev = p
    return out


def walk(n, seed, sd=0.0005, start=100.0):
    rng, p, out = random.Random(seed), start, []
    for _ in range(n):
        p *= math.exp(rng.gauss(0, sd))
        out.append(p)
    return out


def ev(t_event, direction, group, t_available, det="d"):
    return event_record(det, "v", t_event, t_event, t_available, direction, group, {"severity": 1.0}, "h",
                        "as-of replay: test", {}, {}, "c", t_inputs=t_available - ASSUMED_PROCESSING_MS)


def labelled(events, b, now, horizons=(30, 60, 240, 480)):
    return [(e, outcomes.label(e["t_available"], e["direction"], b, now, horizons), None) for e in events]


def design(horizons=(30, 60, 240, 480), ref="reference"):
    return {"id": "T", "version": 2, "module": "flow_absorption", "family": "F", "question": "q",
            "variants": [{"name": "v", "params": {}}], "primary_variant": "v",
            "outcome": {"metric": "ret_net", "horizons_min": list(horizons), "primary_horizon": horizons[0]},
            "comparison": {"test_group": "test", "reference_group": ref, "hypothesised_sign": 1},
            "collapse_ms": 0, "min_retained_observations": 100, "min_dependence_blocks": 20,
            "_sha256": "x", "_file": "lab/designs/T.json", "_version": "ev-t", "_components": {}}


def counts(rows, d, horizon):
    s = experiments.summarize(rows, d, None, "reanalysis", {}, {}, 1)
    return s[str(horizon)]["counts"]["test"]


# ---- 2. outcome independence ---------------------------------------------------------------------
class OverlapTests(unittest.TestCase):
    def setUp(self):
        self.b = bars(walk(3000, 1))
        self.now = T0 + 2900 * MINUTE

    def test_identical_entry_counts_once(self):
        # two events an hour apart whose inputs arrive together -> same executable bar
        avail = T0 + 2 * H + 30_000
        rows = labelled([ev(T0, 1, "test", avail), ev(T0 + H, 1, "test", avail)], self.b, self.now)
        for h in (30, 60, 240, 480):
            c = counts(rows, design(), h)
            self.assertEqual((c["scorable"], c["retained"], c["dropped_overlap"]), (2, 1, 1), h)

    def test_partial_overlap_and_touching_boundaries_per_horizon(self):
        a = T0 + 60_000
        rows = labelled([ev(T0, 1, "test", a), ev(T0 + 45 * MINUTE, 1, "test", a + 45 * MINUTE)], self.b, self.now)
        got = {h: counts(rows, design(), h)["retained"] for h in (30, 60, 240, 480)}
        self.assertEqual(got, {30: 2, 60: 1, 240: 1, 480: 1})
        touch = labelled([ev(T0, 1, "test", a), ev(T0 + 30 * MINUTE, 1, "test", a + 30 * MINUTE)], self.b, self.now)
        self.assertEqual(counts(touch, design(), 30)["retained"], 2)       # exit == next entry: both kept
        self.assertEqual(counts(touch, design(), 60)["retained"], 1)

    def test_catch_up_after_outage_collapses_to_one_entry(self):
        # an outage: 12 five-minute decisions whose inputs all arrive in one catch-up batch
        catch_up = T0 + 3 * H
        rows = labelled([ev(T0 + k * 5 * MINUTE, 1, "test", catch_up) for k in range(12)], self.b, self.now)
        for h in (30, 60, 240, 480):
            self.assertEqual(counts(rows, design(), h)["retained"], 1)

    def test_delayed_batch_uses_actual_entry(self):
        on_time = labelled([ev(T0, 1, "test", T0 + 60_000)], self.b, self.now)[0][1][30]
        late = labelled([ev(T0, 1, "test", T0 + 20 * MINUTE)], self.b, self.now)[0][1][30]
        self.assertEqual(late["entry_t"] - on_time["entry_t"], 19 * MINUTE)

    def test_opposite_directions_at_one_entry_are_not_two_observations(self):
        a = T0 + 60_000
        rows = labelled([ev(T0, 1, "test", a), ev(T0, -1, "test", a)], self.b, self.now)
        self.assertEqual(counts(rows, design(), 60)["retained"], 1)

    def test_cross_group_overlap_shares_a_dependence_block(self):
        a = T0 + 60_000
        rows = labelled([ev(T0, 1, "test", a), ev(T0 + 10 * MINUTE, 1, "reference", a + 10 * MINUTE),
                         ev(T0 + 3 * DAY // 2, 1, "test", T0 + 3 * DAY // 2 + 60_000)], self.b, T0 + 2 * DAY + H)
        s = experiments.summarize(rows, design(), None, "reanalysis", {}, {}, 1)["60"]
        test_blocks = {r["block"] for r in s["_test"]}
        ref_blocks = {r["block"] for r in s["_ref"]}
        self.assertEqual(len(test_blocks), 2)
        self.assertTrue(ref_blocks <= test_blocks)                      # the overlapping reference joined a test block
        self.assertEqual(s["counts"]["dependence_blocks"], 2)

    def test_selection_ignores_outcomes(self):
        a = T0 + 60_000
        evs = [ev(T0, 1, "test", a), ev(T0 + 10 * MINUTE, 1, "test", a + 10 * MINUTE)]
        rows = labelled(evs, self.b, self.now)
        kept = experiments.summarize(rows, design(), None, "reanalysis", {}, {}, 1)["60"]["_test"]
        rows[0][1][60]["ret_net"], rows[1][1][60]["ret_net"] = -1.0, 1.0      # outcomes cannot change selection
        kept2 = experiments.summarize(rows, design(), None, "reanalysis", {}, {}, 1)["60"]["_test"]
        self.assertEqual([r["event_id"] for r in kept], [r["event_id"] for r in kept2])

    def test_counts_are_kept_separately(self):
        a = T0 + H + 60_000
        rows = labelled([ev(T0, 1, "test", a), ev(T0 + H, 1, "test", a)], self.b, self.now)
        c = experiments.summarize(rows, design(), None, "reanalysis", {"test": 5}, {}, 1)["60"]["counts"]
        self.assertEqual({k: c["test"][k] for k in ("firings", "episodes", "scorable", "retained", "blocks")},
                         {"firings": 5, "episodes": 2, "scorable": 2, "retained": 1, "blocks": 1})


# ---- 3. point-in-time availability ---------------------------------------------------------------
def three_assets(n=2 * 1440, shock_at=1500):
    data = {a: bars(walk(n, seed)) for a, seed in (("BTC", 11), ("ETH", 12), ("SOL", 13))}
    eth = data["ETH"]
    for k in range(5):                                                   # a sharp ETH drop in one window
        t = T0 + (shock_at + k) * MINUTE
        eth[t]["c"] = eth[t]["o"] * 0.996
        eth[t]["l"] = eth[t]["c"] * 0.9999
        if t + MINUTE in eth:
            eth[t + MINUTE]["o"] = eth[t]["c"]
    return data


class AvailabilityTests(unittest.TestCase):
    params = {"k_sigma": 3.0}

    def events(self, data):
        ev_, _, cov, _ = cross_asset.build(data, "as-of replay: test", self.params, "c", [])
        return {e["decision_key"]: e for e in ev_ if e["features"].get("alt") == "ETH"}, cov

    def test_delayed_prior_bar_delays_cross_asset_event(self):
        base, _ = self.events(three_assets())
        self.assertTrue(base)
        key, e0 = next(iter(base.items()))
        data = three_assets()
        prior = e0["t_event"] - 40 * MINUTE                               # inside the prior-60-minute sigma window
        data["BTC"][prior]["avail"] = e0["t_event"] + 49 * MINUTE
        got, _ = self.events(data)
        e1 = got[key]
        self.assertGreaterEqual(e1["t_inputs"], data["BTC"][prior]["avail"])
        self.assertGreaterEqual(e1["t_available"], data["BTC"][prior]["avail"] + ASSUMED_PROCESSING_MS)
        self.assertEqual(e1["features"], e0["features"])                 # values unchanged, only timing

    def test_very_late_prior_bar_excludes_event(self):
        base, _ = self.events(three_assets())
        key, e0 = next(iter(base.items()))
        data = three_assets()
        data["SOL"][e0["t_event"] - 30 * MINUTE]["avail"] = e0["t_event"] + LATE_INPUT_MAX_MS + H
        got, cov = self.events(data)
        self.assertNotIn(key, got)
        self.assertGreater(cov["late_inputs"], 0)

    def test_optional_funding_only_if_known(self):
        data = three_assets()
        base, _ = self.events(data)
        key, e0 = next(iter(base.items()))
        early = (e0["t_event"] - 2 * H, 0.0001, e0["t_event"] - 2 * H)
        late = (e0["t_event"] - H, 0.0009, e0["t_event"] + 5 * H)      # settled before, published after
        ev_, _, _, _ = cross_asset.build(data, "as-of replay: test", self.params, "c", [early, late])
        got = {e["decision_key"]: e for e in ev_}[key]
        self.assertEqual(got["features"]["funding_last"], 0.0001)

    def flow_setup(self):
        rng = random.Random(1)
        perp = bars(walk(9 * 1440, 1))
        spot = bars(walk(9 * 1440, 2))
        for bb in (perp, spot):
            for b in bb.values():
                b["tbv"] = b["v"] * rng.uniform(0.3, 0.7)
        return perp, spot

    def flow(self, perp, spot, funding=()):
        p = {"flow_quantile": 0.99, "weak_max": 0.5, "strong_min": 1.5}
        evs, ctl, cov = flow_absorption.build(perp, spot, min(perp), max(perp) + MINUTE, p, "as-of replay: test",
                                              (), funding, "c")
        return {e["decision_key"]: e for e in evs}, cov

    def test_flow_absorption_prior_bar_and_optional_spot(self):
        perp, spot = self.flow_setup()
        base, _ = self.flow(perp, spot)
        key, e0 = sorted(base.items(), key=lambda kv: kv[1]["t_event"])[len(base) // 2]
        self.assertIsNotNone(e0["features"]["spot_flow_norm"])
        perp2 = {t: dict(b) for t, b in perp.items()}
        perp2[e0["t_event"] - 30 * MINUTE]["avail"] = e0["t_event"] + 20 * MINUTE    # a prior bar arrives late
        got, _ = self.flow(perp2, spot)
        self.assertGreaterEqual(got[key]["t_available"], e0["t_event"] + 20 * MINUTE + ASSUMED_PROCESSING_MS)
        self.assertEqual(got[key]["features"]["flow_norm"], e0["features"]["flow_norm"])
        spot2 = {t: dict(b) for t, b in spot.items()}
        spot2[e0["t_event"] - MINUTE]["avail"] = e0["t_event"] + 3 * H                 # optional spot is late
        got, cov = self.flow(perp, spot2)
        self.assertIsNone(got[key]["features"]["spot_flow_norm"])
        self.assertEqual(got[key]["quality"]["spot"], "late")
        self.assertEqual(got[key]["t_available"], e0["t_available"])                   # optional input never delays

    def test_hl_liquidation_exposure_waits_for_the_mark(self):
        rec = {"t": T0, "observed_at": T0 + 60_000, "policy": "hl-sample-v2", "address_of": {"F0": "0xa"},
               "positions": [["F0", "BTC", 1.0, 100.0, 99.0, "cross", 10, 5e6, 0, 0, 0, 40]]}
        snap = {"t": T0, "observed_at": T0 + 10 * MINUTE, "oi": {"hyperliquid": {"st": "ok", "mark": 100.0}}}

        class S:
            def hl_accounts(self):
                return [rec]

            def snaps(self):
                return [snap]

            def bars(self, name):
                return {}

            def hl_enrich(self):
                return []
        lab = type("L", (), {"store": S(), "code": "c"})()
        res = liq_exposure.run(lab, {"distance_pct": 2.0, "min_notional_usd": 1e6})
        e = res["passes"][0]["events"][0]
        self.assertEqual(e["t_inputs"], snap["observed_at"])


class FreezeTests(unittest.TestCase):
    """Appending future or late data cannot silently alter an already frozen decision."""
    def run_twice(self, first_group, second_group, second_extra=()):
        b = bars([100.0 + 0.01 * i for i in range(3000)])
        state = {"calls": 0}

        class Mod:
            @staticmethod
            def run(lab, params):
                state["calls"] += 1
                g = first_group if state["calls"] == 1 else second_group
                es = [ev(T0 + 5 * H, 1, g, T0 + 5 * H + 60_000)]
                if state["calls"] > 1:
                    es += list(second_extra)
                return {"passes": [{"basis": "prospective", "events": es, "controls": [], "bars": b,
                                    "coverage": {}, "state": "available", "reasons": []}]}
        d = design(horizons=(30,))
        with tempfile.TemporaryDirectory() as dd:
            lab = type("L", (), {"now": T0 + 10 * H, "write": True, "base": Path(dd), "code": "c",
                                 "store": type("S", (), {"funding_events": lambda s: [], "funding_known": lambda s: [],
                                                         "snaps": lambda s: []})()})()
            experiments.run_design(lab, d, Mod, {"registered": T0}, 1)
            lab.now = T0 + 20 * H
            res, _ = experiments.run_design(lab, d, Mod, {"registered": T0}, 1, run_state={"last_cutoff": T0 + 10 * H})
        return res["variants"][0]["passes"][0]

    def test_frozen_decision_survives_recomputation(self):
        p = self.run_twice("test", "reference")
        self.assertEqual(p["freeze_audit"]["revised_since_frozen"], 1)
        ev_ = p["phases"]["evaluation"]["30"]["counts"]
        self.assertEqual((ev_["test"]["episodes"], ev_["reference"]["episodes"]), (1, 0))

    def test_late_replay_is_not_evaluation_evidence(self):
        late = ev(T0 + 7 * H, 1, "test", T0 + 7 * H + 60_000)            # decided before the previous run's cutoff
        p = self.run_twice("test", "test", [late])
        self.assertEqual(p["freeze_audit"]["late_replay"], 1)
        self.assertEqual(p["phases"]["evaluation"]["30"]["counts"]["test"]["episodes"], 1)


# ---- 4. versions ---------------------------------------------------------------------------------
class VersionTests(unittest.TestCase):
    def copy(self, d):
        for rel in ["lab", "schema.py", "enrich.py", "hlsample.py", "optionsbook.py", "stream"]:
            src = ROOT / rel
            if src.is_dir():
                shutil.copytree(src, Path(d, rel), ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy(src, Path(d, rel))

    def version(self, base, name="A1-flow-absorption"):
        d = experiments.load_design(Path(base, "lab/designs", name + ".json"))
        return versioning.version_id(versioning.components(base, d))

    def test_semantic_code_change_starts_new_version_but_docs_and_data_do_not(self):
        with tempfile.TemporaryDirectory() as d:
            self.copy(d)
            v0 = self.version(d)
            p = Path(d, "lab/modules/flow_absorption.py")
            src = p.read_text()
            p.write_text(src.replace('"""Module A - flow absorption.', '"""Module A - flow absorption (edited doc).', 1)
                         .replace("\nimport math\n", "\n# a comment\nimport math\n", 1))
            self.assertEqual(self.version(d), v0)                        # docstring + comment edit
            Path(d, "data").mkdir()
            Path(d, "data/new.jsonl").write_text("{}\n")                 # data commit
            Path(d, "README.md").write_text("docs")
            self.assertEqual(self.version(d), v0)
            p.write_text(p.read_text().replace("STEP = 5 * MINUTE", "STEP = 10 * MINUTE"))
            self.assertNotEqual(self.version(d), v0)                     # detector logic changed
            p.write_text(src)
            Path(d, "lab/outcomes.py").write_text(Path(d, "lab/outcomes.py").read_text()
                                                  .replace('"taker_fee_bp_per_side": 5.0', '"taker_fee_bp_per_side": 4.0'))
            self.assertNotEqual(self.version(d), v0)                     # cost convention changed
            shutil.copy(ROOT / "lab/outcomes.py", Path(d, "lab/outcomes.py"))
            h = Path(d, "hlsample.py")
            h.write_text(h.read_text().replace("FIXED_N = 100", "FIXED_N = 90"))
            self.assertEqual(self.version(d), v0)                        # module A does not read the HL sample
            self.assertNotEqual(self.version(d, "B1-underwater-adds"),
                                self.version(str(ROOT), "B1-underwater-adds"))   # module B does

    def test_new_version_keeps_old_evidence_accessible(self):
        from lab import evidence
        with tempfile.TemporaryDirectory() as d:
            c1 = {"design": "T", "evaluation_version": "ev-1", "status": "exploratory", "superseded_versions": []}
            evidence.write_cards(d, [c1], T0)
            c2 = {"design": "T", "evaluation_version": "ev-2", "status": "exploratory", "superseded_versions": ["ev-1"]}
            evidence.write_cards(d, [c2], T0 + H)
            self.assertTrue(Path(d, "research/evidence/v2/T@ev-1.json").exists())
            idx = json.loads(Path(d, "research/evidence/index.json").read_text())["designs"]["T"]
            self.assertEqual(idx["current"], "ev-2")
            self.assertEqual(idx["versions"]["ev-1"]["status"], "retired (superseded)")

    def test_every_design_has_a_baseline_and_promotion_counts(self):
        for p in experiments.design_files(ROOT):
            d = json.loads(p.read_text())
            self.assertEqual(d["baseline"]["predictors"], ["prior_ret_60m_aligned", "prior_rv_60m", "funding_aligned"])
            self.assertGreaterEqual(d["min_retained_observations"], 100)
            self.assertGreaterEqual(d["min_dependence_blocks"], 20)


# ---- 5. attribution --------------------------------------------------------------------------------
ACC = ["account_id", "state", "reason", "clearinghouse_time_offset_ms", "account_value", "total_ntl_pos",
       "total_margin_used", "total_raw_usd", "cross_account_value", "cross_maintenance_margin_used", "withdrawable",
       "n_positions", "other_n", "other_long_ntl", "other_short_ntl", "other_margin_used", "other_unrealized_pnl"]


def acct_rec(t, szi):
    return {"t": t, "observed_at": t + 60_000, "address_of": {"F0": "0xa"}, "account_fields": ACC,
            "accounts": [["F0", "ok_btc", None, 0, 1e6, 0, 0, 0, 1e6, 1e4, 0, 1, 0, 0, 0, 0, 0]],
            "positions": [["F0", "BTC", szi, 100.0, 50.0, "cross", 5, 1e5, -3e4, 1e4, 0, 40]] if szi else [],
            "flat": [] if szi else [["F0", 0, 1e6, 1e6]], "policy": "hl-sample-v2"}


class HLStore:
    def __init__(self, recs, enrich):
        self.recs, self.enrich = recs, enrich

    def hl_accounts(self):
        return self.recs

    def hl_enrich(self):
        return self.enrich


def check(kind, start, end, status="ok", ledger=(), fills=(), truncated=False, seen=None):
    return {"t": end, "observed_at": seen or end + 60_000, "requests": [
        {"kind": kind, "user": "0xa", "window": [start, end], "status": status, "truncated_at_source": truncated,
         "ledger": list(ledger), "fills": list(fills)}]}


class AttributionTests(unittest.TestCase):
    def transitions(self, enrich):
        recs = [acct_rec(T0 + 60 * MINUTE, 1.0), acct_rec(T0 + 75 * MINUTE, 2.0)]
        return accounts.transitions(HLStore(recs, enrich))[0]

    def test_earlier_deposit_in_the_query_window_does_not_confirm_the_transition(self):
        dep = [T0 + 5 * MINUTE, "deposit", {"type": "deposit", "usdc": "1000"}]
        tr = self.transitions([check("ledger", T0, T0 + 80 * MINUTE, ledger=[dep])])
        self.assertEqual(tr["transfer"], "none_observed")

    def test_in_window_transfer_is_confirmed_and_boundaries(self):
        inside = [T0 + 70 * MINUTE, "withdraw", {"type": "withdraw"}]
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, ledger=[inside])])["transfer"],
                         "confirmed")
        at_t0 = [T0 + 60 * MINUTE, "deposit", {"type": "deposit"}]            # (t0, t1]: t0 belongs before
        at_t1 = [T0 + 75 * MINUTE, "deposit", {"type": "deposit"}]
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, ledger=[at_t0])])["transfer"],
                         "none_observed")
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, ledger=[at_t1])])["transfer"],
                         "confirmed")
        spot = [T0 + 70 * MINUTE, "send", {"type": "send", "sourceDex": "spot", "destinationDex": "spot"}]
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, ledger=[spot])])["transfer"],
                         "none_observed")

    def test_incomplete_coverage_stays_unknown(self):
        self.assertEqual(self.transitions([])["transfer"], "unchecked")
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, truncated=True)])["transfer"], "partial")
        self.assertEqual(self.transitions([check("ledger", T0 + 65 * MINUTE, T0 + 80 * MINUTE)])["transfer"], "partial")
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, status="failed")])["transfer"], "failed")
        self.assertEqual(self.transitions([check("ledger", T0, T0 + 80 * MINUTE, status="not_attempted")])["transfer"],
                         "not_attempted")

    def test_knowledge_at_decision_versus_later_confirmation(self):
        inside = [T0 + 70 * MINUTE, "withdraw", {"type": "withdraw"}]
        tr = self.transitions([check("ledger", T0, T0 + 80 * MINUTE, ledger=[inside], seen=T0 + 5 * H)])
        self.assertEqual((tr["transfer_at_decision"], tr["transfer"]), ("unchecked", "confirmed"))

    def exit_kind(self, enrich, szi=1.0):
        cs = hlevidence.checks(HLStore([], enrich))
        return hlevidence.position_exit(cs, "0xa", T0 + 60 * MINUTE, T0 + 75 * MINUTE, szi)["kind"]

    def fill(self, t, coin, direction, liq=None):
        return [t, coin, 100.0, 1.0, "A", direction, 1.0, 0.0, True, 0.1, 1, None, liq]

    def test_position_specific_liquidation(self):
        w = (T0, T0 + 80 * MINUTE)
        early = [T0 + 5 * MINUTE, "liquidation", {"type": "liquidation", "liquidatedPositions": [{"coin": "BTC", "szi": "1"}]}]
        self.assertEqual(self.exit_kind([check("ledger", *w, ledger=[early])]), "evidence_unchecked")
        eth = [T0 + 70 * MINUTE, "liquidation", {"type": "liquidation", "liquidatedPositions": [{"coin": "ETH", "szi": "3"}]}]
        self.assertEqual(self.exit_kind([check("ledger", *w, ledger=[eth])]), "evidence_unchecked")
        btc = [T0 + 70 * MINUTE, "liquidation", {"type": "liquidation", "liquidatedPositions": [{"coin": "BTC", "szi": "1"}]}]
        self.assertEqual(self.exit_kind([check("ledger", *w, ledger=[btc])]), "confirmed_liquidation")
        anon = [T0 + 70 * MINUTE, "liquidation", {"type": "liquidation"}]
        self.assertEqual(self.exit_kind([check("ledger", *w, ledger=[anon])]), "account_liquidation_unattributed")

    def test_fills_must_match_coin_side_and_account(self):
        w = (T0, T0 + 80 * MINUTE)
        eth_close = self.fill(T0 + 70 * MINUTE, "ETH", "Close Long")
        self.assertEqual(self.exit_kind([check("fills", *w, fills=[eth_close])]), "unclassified")
        short_close = self.fill(T0 + 70 * MINUTE, "BTC", "Close Short")
        self.assertEqual(self.exit_kind([check("fills", *w, fills=[short_close])]), "unclassified")
        other = self.fill(T0 + 70 * MINUTE, "BTC", "Close Long", {"liquidatedUser": "0xother"})
        self.assertEqual(self.exit_kind([check("fills", *w, fills=[other])]), "voluntary_exit")
        mine = self.fill(T0 + 70 * MINUTE, "BTC", "Close Long", {"liquidatedUser": "0xa"})
        self.assertEqual(self.exit_kind([check("fills", *w, fills=[mine])]), "confirmed_liquidation")
        self.assertEqual(self.exit_kind([check("fills", *w, truncated=True)]), "evidence_partial")


# ---- 6. streaming timing -------------------------------------------------------------------------
class StreamTimingTests(unittest.TestCase):
    params = {"shock_frac": 0.3, "recover_frac": 0.8, "recovery_s": 60}

    def record(self, root, jitter, drop=(), stale=(), dup=False):
        """Drive Recorder.sample with a real BybitBook for 2 hours of seconds, then read back through
        the module: Recorder -> LocalStore partitions -> liquidity.run."""
        store = storage.LocalStore(root)
        rec = service.Recorder({"sample_max_age_ms": 20000}, store)
        book = BybitBook("BTCUSDT")
        rng = random.Random(5)
        for s in range(7200):
            depth = 10.0
            if 4000 <= s < 4070:
                bid, ask = 1.0, 4.0                                     # slow recovery shock
            elif 5000 <= s < 5005:
                bid, ask = 5.0, 0.5                                     # fast recovery shock
            else:
                bid, ask = depth, depth
            t = T0 + s * 1000 + (rng.choice(jitter) if jitter else 0)
            if s in drop:
                continue
            book.apply({"type": "snapshot", "ts": t - (5000 if s in stale else 50),
                        "data": {"u": s + 1, "b": [["100.00", str(bid)]], "a": [["100.01", str(ask)]]}})
            rec.sample(book, t)
            if dup and s % 97 == 0:
                rec.sample(book, t + 3)
        store.flush()
        with patch.dict(os.environ, {"STREAM_DATA_DIR": root}):
            lab = type("L", (), {"code": "c", "store": type("S", (), {"bars": lambda s, n: {}})()})()
            return liquidity.run(lab, self.params)["passes"][0]

    def summary(self, p):
        return (sorted((e["t_event"], e["group"], e["direction"]) for e in p["events"]),
                sorted(c["t_event"] for c in p["controls"]))

    def test_jitter_keeps_the_same_shocks_and_controls(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            exact = self.summary(self.record(a, None))
            jittered_pass = self.record(b, [1, 2, -2, 3], dup=True)
        self.assertEqual(len(exact[0]), 3)                              # slow, its re-fire, fast
        self.assertEqual(len(exact[1]), 1)                              # the 01:00 control
        self.assertEqual(self.summary(jittered_pass), exact)
        self.assertGreater(jittered_pass["coverage"]["duplicates"], 0)

    def test_missing_and_stale_seconds_still_fail_coverage(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            missing = self.record(a, [1, 2], drop={4030})
            stale = self.record(b, [1, 2], stale={4030})
        for p in (missing, stale):
            self.assertNotIn("slow", [e["group"] for e in p["events"] if e["t_event"] == T0 + 4060 * 1000])
            self.assertGreaterEqual(p["coverage"]["skipped_coverage"], 1)
        self.assertEqual(stale["coverage"]["stale"], 1)

    def test_sequence_gap_fails_coverage(self):
        with tempfile.TemporaryDirectory() as a:
            Path(a, "derived/gaps").mkdir(parents=True)
            Path(a, "derived/gaps/2026-09-23.jsonl").write_text(json.dumps(
                {"venue": "bybit", "instrument": "BTCUSDT", "start": T0 + 4990 * 1000, "end": None,
                 "reason": "update id jump"}) + "\n")
            p = self.record(a, [1])
        self.assertNotIn(T0 + 5060 * 1000, [e["t_event"] for e in p["events"]])
        self.assertEqual(p["coverage"]["skipped_gap"], 1)

    def test_availability_never_precedes_the_samples(self):
        with tempfile.TemporaryDirectory() as a:
            p = self.record(a, [2])
        for e in p["events"]:
            self.assertGreaterEqual(e["t_inputs"], e["t_event"] + 2 + liquidity.FLUSH_ASSUMED_MS)


# ---- 7. option quote quality ---------------------------------------------------------------------
class OptionQualityTests(unittest.TestCase):
    FIELDS = ["instrument", "timestamp", "best_bid_price", "best_bid_amount", "best_ask_price", "best_ask_amount",
              "mark_price", "mark_iv", "bid_iv", "ask_iv", "delta"]

    def rec(self, call, put):
        return {"t": T0, "t_event": T0, "panel_fields": self.FIELDS,
                "panel": [["BTC-30SEP26-90000-C"] + call, ["BTC-30SEP26-70000-P"] + put]}

    good = [T0 - 1000, 0.010, 5, 0.011, 5, 0.0105, 50.0, 49.0, 51.0, 0.25]
    goodp = [T0 - 1000, 0.010, 5, 0.011, 5, 0.0105, 55.0, 54.0, 56.0, -0.25]

    def test_each_failure_mode_disqualifies_the_signal(self):
        f = options_disagreement.panel_quality
        self.assertEqual(f(self.rec(self.good, self.goodp))["rr25_7d_quotes"], "qualified")
        cases = {"stale": [T0 - 120_000] + self.good[1:],
                 "crossed": [T0, 0.012, 5, 0.011, 5, 0.0105, 50.0, 49.0, 51.0, 0.25],
                 "one_sided_or_missing": [T0, 0.0, 0, 0.011, 5, 0.0105, 50.0, 49.0, 51.0, 0.25],
                 "wide": [T0, 0.008, 5, 0.012, 5, 0.0105, 50.0, 49.0, 51.0, 0.25],
                 "mark_outside_quotes": [T0, 0.010, 5, 0.011, 5, 0.0105, 60.0, 49.0, 51.0, 0.25]}
        for reason, call in cases.items():
            q = f(self.rec(call, self.goodp))
            self.assertEqual(q["rr25_7d_quotes"], "failed", reason)
            self.assertIn(reason, q["rr25_7d_quote_reason"])

    def test_unobserved_quality_is_unknown_not_failed(self):
        q = options_disagreement.panel_quality({"t": T0, "panel_fields": self.FIELDS, "panel": []})
        self.assertEqual(q["rr25_7d_quotes"], "unknown")
        q = options_disagreement.panel_quality(self.rec(self.good, [T0, 0.01, 5, 0.011, 5, 0.0105, 50.0, 49, 51, -0.5]))
        self.assertEqual(q["rr25_7d_quotes"], "unknown")               # the 25-delta put was not in the panel

    def module_run(self, panel_call, policy="qualified"):
        recs, snaps = [], []
        for k in range(40):
            t = T0 + k * 15 * MINUTE
            rr = -5.0 if k == 39 else 0.1 * (k % 3)
            rows = [["BTC-30SEP26-90000-C", 10.0, 50.0 + rr / 2], ["BTC-30SEP26-70000-P", 10.0, 50.0 - rr / 2],
                    ["BTC-30SEP26-80000-C", 10.0, 50.0], ["BTC-30SEP26-80000-P", 10.0, 50.0]]
            recs.append({"t": t, "t_event": t, "observed_at": t + 60_000, "rows": rows,
                         "underlying": {"30SEP26": 80000.0}, "panel_fields": self.FIELDS,
                         "panel": [["BTC-30SEP26-90000-C", t + (panel_call[0] - T0)] + panel_call[1:],
                                   ["BTC-30SEP26-70000-P", t - 1000] + self.goodp[1:]]})
            fund = 0.0001 * (k % 3) if k < 39 else 0.01
            snaps.append({"t": t, "observed_at": t + 60_000,
                          "binance_usdt_prem": {"st": "ok", "funding_live_predicted_8h": fund}})

        class S:
            def options(self):
                return recs

            def snaps(self):
                return snaps

            def bars(self, name):
                return {}
        lab = type("L", (), {"store": S(), "code": "c"})()
        return options_disagreement.run(lab, {"z": 2.0, "z_window": 30, "min_records": 10, "quote_policy": policy})

    def test_quality_changes_eligibility_not_just_a_counter(self):
        with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rows"][0][2] - rec["rows"][1][2]}):
            ok = self.module_run(self.good)["passes"][0]["events"]
            bad = self.module_run([T0 - 3 * H] + self.good[1:])["passes"][0]["events"]
            mark_only = self.module_run([T0 - 3 * H] + self.good[1:], "mark_only")["passes"][0]["events"]
        self.assertEqual([e["group"] for e in ok], ["bearish_disagreement"])
        self.assertEqual([e["group"] for e in bad], ["bearish_disagreement_ineligible"])
        self.assertEqual([e["group"] for e in mark_only], ["bearish_disagreement"])  # separately labelled variant
        self.assertEqual(bad[0]["features"]["rr25_7d"], ok[0]["features"]["rr25_7d"])   # descriptive surface kept

    def test_primary_design_excludes_ineligible_and_markonly_is_descriptive(self):
        d = json.loads((ROOT / "lab/designs/F1-options-perp-disagreement.json").read_text())
        self.assertEqual(d["comparison"]["test_group"], ["bearish_disagreement", "bullish_disagreement"])
        primary = next(v for v in d["variants"] if v["name"] == d["primary_variant"])
        self.assertEqual(primary["params"]["quote_policy"], "qualified")
        self.assertTrue(next(v for v in d["variants"] if v["params"]["quote_policy"] == "mark_only")["descriptive"])

    def test_zero_oi_is_distinct_from_missing(self):
        rec = {"t": T0, "rows": [["BTC-30SEP26-80000-C", 0.0, 50.0]], "underlying": {"30SEP26": 80000.0}}
        s = options_disagreement.surface(rec)
        self.assertEqual(s["total_oi_btc"], 0.0)                       # zero is a value
        self.assertIsNone(options_disagreement.surface({"t": T0, "rows": [], "underlying": {}})["oi_hhi"])


# ---- 8. reports and persistence ------------------------------------------------------------------
class PersistenceTests(unittest.TestCase):
    def test_merge_never_rewinds_newer_content(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import merge_research
        with tempfile.TemporaryDirectory() as inc, tempfile.TemporaryDirectory() as repo:
            for base, cutoff, gen in ((inc, "2026-09-23 10:00Z", "2026-09-23 12:00Z"),
                                      (repo, "2026-09-23 11:00Z", "2026-09-23 11:30Z")):
                Path(base, "reports").mkdir()
                Path(base, "reports/latest.md").write_text(f"Generated {gen} by x. Input cutoff: {cutoff} (y).\n")
                Path(base, "research/v2/ledger").mkdir(parents=True)
                Path(base, "state").mkdir()
            Path(repo, "research/v2/ledger/2026-09.jsonl").write_text('{"a":1}\n')
            Path(inc, "research/v2/ledger/2026-09.jsonl").write_text('{"a":1}\n{"b":2}\n')
            Path(repo, "state/lab_registrations.json").write_text(json.dumps({"T@ev-1": {"registered": 1}}))
            Path(inc, "state/lab_registrations.json").write_text(json.dumps({"T@ev-1": {"registered": 999},
                                                                             "T@ev-2": {"registered": 5}}))
            with patch("sys.stdout", io.StringIO()), patch("sys.stderr", io.StringIO()):
                self.assertEqual(merge_research.main(inc, repo), 4)       # 2.12: no publication metadata
            self.assertEqual(Path(repo, "research/v2/ledger/2026-09.jsonl").read_text(), '{"a":1}\n')
            sys.path.insert(0, str(ROOT / "regression"))
            from publication_fixture import valid_summary
            Path(inc, "lab-summary.json").write_text(json.dumps(valid_summary(5, {})))
            with patch("sys.stdout", io.StringIO()):
                self.assertEqual(merge_research.main(inc, repo), 0)
            self.assertIn("Input cutoff: 2026-09-23 11:00Z", Path(repo, "reports/latest.md").read_text())
            self.assertEqual(Path(repo, "research/v2/ledger/2026-09.jsonl").read_text(), '{"a":1}\n{"b":2}\n')
            reg = json.loads(Path(repo, "state/lab_registrations.json").read_text())
            self.assertEqual(reg, {"T@ev-1": {"registered": 1}, "T@ev-2": {"registered": 5}})

    def test_coverage_refresh_states_provenance_and_has_no_side_effects(self):
        import report
        with tempfile.TemporaryDirectory() as d:
            Path(d, "data/runs").mkdir(parents=True)
            Path(d, "data/runs/2026-09.jsonl").write_text(json.dumps(
                {"t": T0, "observed_at": T0 + 90_000, "code_version": "collector-2.7-2026-09-23", "mode": "routine"}) + "\n")
            shutil.copy(ROOT / "cadence.json", Path(d, "cadence.json"))
            text = report.build(Path(d), T0 + H, 7, coverage_only=True)
            self.assertIn("Input cutoff: 2026-09-23 00:01Z", text)
            self.assertIn(report.REPORT_VERSION, text)                    # the running report version
            self.assertIn("Not run in the coverage refresh", text)
            self.assertFalse(Path(d, "registry").exists())


if __name__ == "__main__":
    unittest.main()
