"""Tests for the research lab (lab/): point-in-time access, outcome labels (entry at availability,
maturity, horizon boundaries, costs, funding), episode collapse, controls, registration and the
exploratory/evaluation split, status rules, idempotent persistence, module behaviour on missing
inputs (explicit unavailable / insufficient states), late observations, the streaming-dependent
module E, evidence cards and proposals, the skill-evaluation harness, and an end-to-end run with
error isolation. Offline; synthetic data in temporary directories.
"""
import gzip
import io
import json
import math
import os
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from lab import evidence, experiments, outcomes, skill_eval, stats
from lab.common import H, MINUTE, PROCESSING_LATENCY_MS
from lab.data import Store
from lab.events import collapse, event_record
from lab.modules import deleveraging, flow_absorption, liquidity, twap
from lab.run import Lab, main as lab_main

T0 = 1_790_121_600_000                     # 2026-09-23 00:00 UTC
FIX = Path(__file__).resolve().parent / "fixtures"


def bars_from(prices, start=T0, avail_lag=0):
    """{t: bar} with o=previous close, c=price; highs/lows bracket both."""
    out, prev = {}, prices[0]
    for i, p in enumerate(prices):
        t = start + i * MINUTE
        out[t] = {"t": t, "o": prev, "h": max(prev, p) * 1.0001, "l": min(prev, p) * 0.9999, "c": p, "v": 10.0,
                  "tbv": 5.0, "avail": t + MINUTE + avail_lag}
        prev = p
    return out


def ev(t, direction=1, group="test", avail=None, det="d"):
    return event_record(det, "v1", t, t, avail if avail is not None else t, direction, group, {}, "h", "prospective: x",
                        {}, {}, "code")


class OutcomeTests(unittest.TestCase):
    def test_entry_at_first_bar_after_availability(self):
        b = bars_from([100 + i for i in range(200)])
        lab = outcomes.label(T0 + 10 * MINUTE + 1, 1, b, T0 + 10 * H, horizons=(30,))
        self.assertEqual(lab[30]["entry_t"], T0 + 11 * MINUTE)          # never the bar the decision was made in
        self.assertEqual(lab[30]["entry_px"], b[T0 + 11 * MINUTE]["o"])
        self.assertEqual(lab[30]["exit_px"], b[T0 + 41 * MINUTE]["o"])
        exact = outcomes.label(T0 + 10 * MINUTE, 1, b, T0 + 10 * H, horizons=(30,))
        self.assertEqual(exact[30]["entry_t"], T0 + 10 * MINUTE)

    def test_maturity_and_incomplete(self):
        b = bars_from([100.0] * 100)
        lab = outcomes.label(T0, 1, b, now=T0 + 30 * MINUTE, horizons=(30, 60))
        self.assertEqual(lab[30]["status"], "immature")                  # exit bar not closed at `now`
        lab = outcomes.label(T0, 1, b, now=T0 + 99 * MINUTE, horizons=(30, 60, 240))
        self.assertEqual(lab[30]["status"], "complete")
        self.assertEqual(lab[240]["status"], "immature")                 # beyond the latest stored bar
        del b[T0 + 15 * MINUTE]
        lab = outcomes.label(T0, 1, b, now=T0 + 99 * MINUTE, horizons=(30,))
        self.assertEqual(lab[30], {"status": "incomplete", "missing": 1})  # never interpolated

    def test_horizon_boundary_uses_exit_open(self):
        prices = [100.0] * 31 + [200.0] * 30
        b = bars_from(prices)
        lab = outcomes.label(T0, 1, b, T0 + 2 * H, horizons=(30,))
        self.assertAlmostEqual(lab[30]["ret"], 0.0)                      # the jump happens in the exit bar itself
        self.assertLess(lab[30]["mfe"], 0.001)                            # and is outside the horizon window

    def test_costs_direction_and_funding(self):
        b = bars_from([100.0] * 600)
        fund = [(T0 + 4 * H, 0.0001)]                                     # longs pay 1 bp at 04:00
        long = outcomes.label(T0, 1, b, T0 + 10 * H, horizons=(480,), funding=fund, half_spread=1.0)[480]
        short = outcomes.label(T0, -1, b, T0 + 10 * H, horizons=(480,), funding=fund, half_spread=1.0)[480]
        base = (2 * 5.0 + 2 * 1.0 + 2 * 1.0) / 1e4
        self.assertAlmostEqual(long["ret_net"], -base - 0.0001)
        self.assertAlmostEqual(short["ret_net"], -base + 0.0001)
        early = outcomes.label(T0, 1, b, T0 + 10 * H, horizons=(60,), funding=fund)[60]
        self.assertEqual(early["costs"]["funding_pnl"], 0)               # settlement outside (entry, exit]

    def test_mae_mfe_signs(self):
        b = bars_from([100, 101, 99, 102, 100] + [100] * 40)
        lg = outcomes.label(T0, 1, b, T0 + 2 * H, horizons=(30,))[30]
        sh = outcomes.label(T0, -1, b, T0 + 2 * H, horizons=(30,))[30]
        self.assertGreater(lg["mfe"], 0)
        self.assertLess(lg["mae"], 0)
        self.assertAlmostEqual(lg["mfe"], -sh["mae"])

    def test_half_spread_staleness(self):
        snaps = [{"t": T0, "depth_binance_usdt": {"st": "ok", "best_bid": 99.99, "best_ask": 100.01}}]
        hs, src = outcomes.half_spread_bp(snaps, T0 + 5 * MINUTE)
        self.assertEqual(src, "snapshot")
        self.assertAlmostEqual(hs, 1.0, places=6)
        self.assertEqual(outcomes.half_spread_bp(snaps, T0 + 20 * MINUTE)[1], "default")


class EventTests(unittest.TestCase):
    def test_available_before_event_rejected(self):
        with self.assertRaises(ValueError):
            event_record("d", "v1", T0, T0, T0 - 1, 1, "g", {}, "h", "b", {}, {}, "c")

    def test_collapse_is_causal_and_counts_once(self):
        es = [ev(T0 + k * 10 * MINUTE) for k in range(4)] + [ev(T0 + 3 * H)] + [ev(T0 + 5 * MINUTE, -1)]
        heads = collapse(es, 30 * MINUTE)
        self.assertEqual(len(heads), 3)                                  # chain of 4, one isolated, one opposite side
        chain = next(h for h in heads if h["t_event"] == T0 and h["direction"] == 1)
        self.assertEqual(chain["episode_size"], 4)

    def test_nonoverlap(self):
        items = [{"t": T0 + k * 10 * MINUTE, "y": 1} for k in range(10)]
        self.assertEqual(len(stats.nonoverlap(items, 30 * MINUTE)), 4)

    def test_bootstrap_deterministic_and_needs_days(self):
        a = [(T0 + d * 86_400_000, 0.01) for d in range(5)]
        b = [(T0 + d * 86_400_000, 0.0) for d in range(5)]
        self.assertEqual(stats.block_bootstrap_diff(a, b), stats.block_bootstrap_diff(a, b))
        self.assertIsNone(stats.block_bootstrap_diff(a[:1], b[:1]))


class StoreTests(unittest.TestCase):
    def test_point_in_time_and_first_observation(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "data/prices/binance_klines_1m_BTCUSDT_perp")
            p.mkdir(parents=True)
            fields = ["t", "o", "h", "l", "c", "v", "qv", "n", "tbv", "tbqv"]
            first = {"t": T0, "t_last": T0 + MINUTE, "fields": fields, "observed_at": T0 + 5 * MINUTE,
                     "bars": [[T0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [T0 + MINUTE, 2, 2, 2, 2, 1, 1, 1, 1, 1]]}
            late = {"t": T0 + MINUTE, "t_last": T0 + 2 * MINUTE, "fields": fields, "observed_at": T0 + 20 * MINUTE,
                    "bars": [[T0 + MINUTE, 9, 9, 9, 9, 1, 1, 1, 1, 1], [T0 + 2 * MINUTE, 3, 3, 3, 3, 1, 1, 1, 1, 1]]}
            (p / "2026-09.jsonl").write_text(json.dumps(first) + "\n" + json.dumps(late) + "\n")
            b = Store(d, cutoff=T0 + 10 * MINUTE).bars("binance_klines_1m_BTCUSDT_perp")
            self.assertEqual(sorted(b), [T0, T0 + MINUTE])                # the late batch is invisible at the cutoff
            b = Store(d, cutoff=T0 + 30 * MINUTE).bars("binance_klines_1m_BTCUSDT_perp")
            self.assertEqual(b[T0 + MINUTE]["o"], 2)                      # first observation wins
            self.assertEqual(b[T0 + 2 * MINUTE]["avail"], T0 + 20 * MINUTE)


class FakeStore:
    def __init__(self, **kw):
        self.kw = kw

    def __getattr__(self, name):
        return lambda *a, **k: self.kw.get(name, [] if name not in ("bars",) else {})


class FakeLab:
    def __init__(self, now, store, write=False, base=None):
        self.now, self.store, self.write, self.base = now, store, write, base
        self.code, self.history, self.history_sha = "code", {}, {}


class ModuleTests(unittest.TestCase):
    def test_deleveraging_ignores_late_revisions(self):
        # 8 days of small buckets, then one bucket whose orders arrive in two waves
        orders = []
        for k in range(8 * 288):
            t = T0 + k * 5 * MINUTE
            orders.append({"t": t, "posSide": "long", "btc": 0.1, "bkPx": 100_000, "avail": t + 60_000})
        tb = T0 + 8 * 288 * 5 * MINUTE
        orders.append({"t": tb, "posSide": "long", "btc": 0.05, "bkPx": 100_000, "avail": tb + 60_000})
        orders.append({"t": tb + 1000, "posSide": "long", "btc": 50, "bkPx": 100_000, "avail": tb + 6 * H})
        store = FakeStore(liq_orders=orders, okx_insurance=[], bars={})
        res = deleveraging.run(FakeLab(tb + 7 * H, store), {})
        evs = [e for e in res["passes"][0]["events"] if e["t_event"] == tb + 5 * MINUTE]
        self.assertEqual(evs, [])                                         # decided at first sight: small bucket
        self.assertEqual(res["passes"][0]["state"], "insufficient_data")  # no insurance rows: stated, not faked

    def test_twap_uses_only_price_known_at_first_seen(self):
        b = bars_from([100.0] * 60 + [1_000_000.0] * 60)
        seen = T0 + 30 * MINUTE
        rec = {"t": seen, "observed_at": seen, "requests": [{"kind": "twap", "status": "ok", "user": "0xa",
               "twap_history": [{"state": {"coin": "BTC", "side": "B", "sz": "20", "timestamp": T0, "minutes": 60},
                                 "status": {"status": "activated"}, "twapId": 7}]}]}
        store = FakeStore(hl_enrich=[rec], bars=b)
        res = twap.run(FakeLab(T0 + 3 * H, store), {"min_notional_usd": 1e6})
        self.assertEqual(res["passes"][0]["events"], [])                  # 20 BTC x 100 < 1e6: the later price is unseen
        res = twap.run(FakeLab(T0 + 3 * H, store), {"min_notional_usd": 1000})
        e = res["passes"][0]["events"][0]
        self.assertEqual(e["t_event"], seen)
        self.assertEqual(e["t_available"], seen + PROCESSING_LATENCY_MS)
        self.assertEqual(res["passes"][0]["state"], "insufficient_data")

    def test_flow_absorption_threshold_uses_past_only(self):
        rng = random.Random(1)
        prices, p = [], 100.0
        for _ in range(9 * 1440):
            p *= math.exp(rng.gauss(0, 0.0005))
            prices.append(p)
        b = bars_from(prices)
        for t, bar in b.items():
            bar["tbv"] = bar["v"] * rng.uniform(0.3, 0.7)
        evs, ctl, cov = flow_absorption.build(b, {}, min(b), max(b) + MINUTE, {"flow_quantile": 0.99, "weak_max": 0.5,
                                              "strong_min": 1.5}, "prospective: x")
        self.assertTrue(evs)
        self.assertTrue(all(e["t_available"] >= e["t_event"] + PROCESSING_LATENCY_MS for e in evs))
        first_allowed = min(b) + 7 * 86_400_000
        self.assertTrue(all(e["t_event"] >= first_allowed - 86_400_000 for e in evs))
        # changing a FUTURE bar must not change any earlier event
        cut = evs[len(evs) // 2]["t_event"]
        b2 = {t: dict(v) for t, v in b.items()}
        for t in b2:
            if t > cut + 10 * MINUTE:
                b2[t]["tbv"] = b2[t]["v"]
        evs2, _, _ = flow_absorption.build(b2, {}, min(b2), max(b2) + MINUTE, {"flow_quantile": 0.99, "weak_max": 0.5,
                                           "strong_min": 1.5}, "prospective: x")
        key = lambda es: [(e["t_event"], e["group"], e["features"]["flow_norm"]) for e in es if e["t_event"] <= cut]
        self.assertEqual(key(evs), key(evs2))


class OptionsQualityTests(unittest.TestCase):
    def test_stale_and_missing_quotes_excluded(self):
        from lab.modules import options_disagreement as f
        fields = ["instrument", "timestamp", "best_bid_price", "best_ask_price", "mark_price"]
        rec = {"t_event": T0, "panel_fields": fields, "panel": [
            ["A", T0 - 5_000, 0.010, 0.011, 0.0105],       # fresh, tight: kept
            ["B", T0 - 120_000, 0.010, 0.011, 0.0105],     # stale ticker: excluded
            ["C", T0, None, 0.011, 0.0105],                # no bid (missing quote, not zero): excluded
            ["D", T0, 0.005, 0.020, 0.0105]]}              # spread > 10% of mark: excluded
        self.assertEqual(f.panel_quality(rec), {"panel_ok": 1, "panel_excluded": 3})

    def test_delta_convention_and_interpolation(self):
        from lab.modules import options_disagreement as f
        self.assertAlmostEqual(f.delta(100.0, 100.0, 50.0, 0.25, "C") - f.delta(100.0, 100.0, 50.0, 0.25, "P"), 1.0)
        self.assertIsNone(f.interp([(0.2, 1.0), (0.4, 2.0)], 0.5))    # no extrapolation


def write_book1s(root, venue, inst, rows):
    by = {}
    for r in rows:
        import datetime as dt
        d = dt.datetime.fromtimestamp(r["t"] / 1000, dt.timezone.utc)
        by.setdefault((d.strftime("%Y-%m-%d"), d.strftime("%H")), []).append(r)
    for (day, hour), rs in by.items():
        p = Path(root, "derived/book1s", venue, inst, day, f"{hour}.jsonl.gz")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(gzip.compress(("\n".join(json.dumps(r) for r in rs) + "\n").encode()))


class LiquidityTests(unittest.TestCase):
    def sample(self, t, bid_d, ask_d):
        return {"t": t, "bid": 99.99, "ask": 100.01, "mid": 100.0, "bid_depth_10bp": bid_d, "ask_depth_10bp": ask_d}

    def test_unavailable_without_stream(self):
        with patch.dict(os.environ, {"STREAM_DATA_DIR": ""}):
            res = liquidity.run(FakeLab(T0, FakeStore(bars={})), {"shock_frac": 0.3, "recover_frac": 0.8, "recovery_s": 60})
        self.assertEqual(res["passes"][0]["state"], "unavailable")
        self.assertEqual(res["passes"][0]["events"], [])

    def test_shock_slow_fast_and_gap_skip(self):
        rows = [self.sample(T0 + s * 1000, 10.0, 10.0) for s in range(3600)]
        for s in range(2000, 2070):                                     # slow: stays depleted for 70 s (bid side)
            rows[s] = self.sample(T0 + s * 1000, 1.0, 4.0)
        for s in range(2500, 2505):                                     # fast: refills within 5 s (ask side)
            rows[s] = self.sample(T0 + s * 1000, 5.0, 0.5)
        rows = [r for i, r in enumerate(rows) if not (3000 <= i < 3010)]  # missing seconds
        rows[2990 - 0] = self.sample(T0 + 2990 * 1000, 1.0, 1.0)          # shock right before the hole
        params = {"shock_frac": 0.3, "recover_frac": 0.8, "recovery_s": 60}
        smp = {r["t"]: r for r in rows}
        evs, ctl, cov = liquidity.build(smp, [], params, "code")
        by_start = {e["t_first_observed"] // 1000 - T0 // 1000: e for e in evs}
        self.assertEqual(sorted(by_start), [2000, 2061, 2500])
        self.assertEqual((by_start[2000]["group"], by_start[2000]["direction"]), ("slow", -1))
        self.assertEqual(by_start[2000]["t_event"], T0 + 2060 * 1000)   # decided after the recovery window
        self.assertEqual((by_start[2500]["group"], by_start[2500]["direction"]), ("fast", 1))
        self.assertEqual(len(collapse(evs, 15 * MINUTE)), 2)            # the 2061 re-fire joins the 2000 episode
        self.assertEqual(cov["skipped_coverage"], 1)                     # missing seconds: skipped, not zero depth
        evs2, _, cov2 = liquidity.build(smp, [(T0 + 2400 * 1000, T0 + 2600 * 1000)], params, "code")
        self.assertEqual(cov2["skipped_gap"], 1)
        self.assertNotIn(T0 + 2500 * 1000, [e["t_first_observed"] for e in evs2])   # overlaps the recorded gap

    def test_reads_partitions_from_stream_dir(self):
        with tempfile.TemporaryDirectory() as d:
            write_book1s(d, "bybit", "BTCUSDT", [self.sample(T0 + s * 1000, 10.0, 10.0) for s in range(120)])
            Path(d, "derived/gaps").mkdir(parents=True)
            Path(d, "derived/gaps/2026-09-23.jsonl").write_text(json.dumps(
                {"venue": "bybit", "instrument": "BTCUSDT", "start": T0, "end": T0 + 5000, "reason": "x"}) + "\n")
            with patch.dict(os.environ, {"STREAM_DATA_DIR": d}):
                res = liquidity.run(FakeLab(T0 + H, FakeStore(bars={})), {"shock_frac": 0.3, "recover_frac": 0.8,
                                                                        "recovery_s": 60})
            p = res["passes"][0]
            self.assertEqual(p["coverage"]["samples"], 120)
            self.assertEqual(p["coverage"]["recorded_gaps"], 1)
            self.assertEqual(p["state"], "insufficient_data")


def design(ref="reference", sign=1, preds=()):
    return {"id": "T1", "version": 1, "module": "m", "family": "F", "question": "q?",
            "variants": [{"name": "v", "params": {}}], "primary_variant": "v",
            "outcome": {"metric": "ret_net", "horizons_min": [30], "primary_horizon": 30},
            "comparison": {"test_group": "test", "reference_group": ref, "hypothesised_sign": sign},
            "baseline_predictors": list(preds), "collapse_ms": 30 * MINUTE, "min_independent_episodes": 4,
            "_sha256": "x" * 64, "_file": "lab/designs/T1.json"}


class ExperimentTests(unittest.TestCase):
    def labelled(self, n_days, test_y, ref_y, start=T0):
        out = []
        for d in range(n_days):
            t = start + d * 86_400_000
            for g, y in (("test", test_y), ("reference", ref_y)):
                e = ev(t + (0 if g == "test" else H), 1, g)
                out.append((e, {30: {"status": "complete", "ret_net": y + 0.0001 * (d % 3)}}))
        return out

    def test_evaluation_excludes_pre_registration_and_vice_versa(self):
        lab = self.labelled(10, 0.01, 0.0)
        reg = T0 + 5 * 86_400_000
        d = design()
        ex = experiments.summarize(lab, d, reg, "exploratory")["30"]
        evl = experiments.summarize(lab, d, reg, "evaluation")["30"]
        self.assertEqual(ex["independent_test_episodes"], 5)
        self.assertEqual(evl["independent_test_episodes"], 5)
        self.assertEqual(experiments.summarize(lab, d, None, "evaluation")["30"]["independent_test_episodes"], 0)

    def test_status_rules(self):
        d = design()
        lab = self.labelled(10, 0.01, 0.0)
        s = experiments.summarize(lab, d, T0, "evaluation")
        self.assertEqual(experiments.status(d, s)[0], "supported")
        s = experiments.summarize(self.labelled(10, -0.01, 0.0), d, T0, "evaluation")
        self.assertEqual(experiments.status(d, s)[0], "retired")
        s = experiments.summarize(self.labelled(3, 0.01, 0.0), d, T0, "evaluation")
        self.assertEqual(experiments.status(d, s)[0], "under prospective evaluation")
        self.assertEqual(experiments.status(d, None)[0], "exploratory")
        self.assertEqual(experiments.status(d, s, superseded=True)[0], "retired")

    def test_control_reference_uses_test_direction_mix(self):
        d = design(ref="control")
        rows = []
        for k in range(6):
            t = T0 + k * 86_400_000
            rows.append((ev(t, -1, "test"), {30: {"status": "complete", "ret_net": 0.002}}))
            rows.append((ev(t + H, 1, "control_long"), {30: {"status": "complete", "ret_net": 0.005}}))
            rows.append((ev(t + H, -1, "control_short"), {30: {"status": "complete", "ret_net": -0.007}}))
        s = experiments.summarize(rows, d, None, "exploratory")["30"]
        self.assertEqual(s["test_share_long"], 0.0)
        self.assertAlmostEqual(s["reference"]["mean"], -0.007)          # short-oriented reference for a short test

    def test_register_never_rewrites(self):
        with tempfile.TemporaryDirectory() as dd:
            d = design()
            self.assertEqual(experiments.register(dd, [d], T0)["T1"], T0)
            self.assertEqual(experiments.register(dd, [d], T0 + H)["T1"], T0)
            d2 = dict(d, _sha256="y" * 64)
            self.assertEqual(experiments.register(dd, [d2], T0 + H)["T1"], T0 + H)   # a changed design is new

    def test_run_design_persist_idempotent(self):
        class Mod:
            @staticmethod
            def run(lab, params):
                b = bars_from([100.0 + 0.01 * i for i in range(3000)])
                es = [ev(T0 + k * H, 1, "test") for k in range(1, 40)] + [ev(T0 + k * H + 30 * MINUTE, 1, "reference")
                                                                           for k in range(1, 40)]
                return {"passes": [{"basis": "prospective", "events": es, "controls": [], "bars": b,
                                    "coverage": {}, "state": "available", "reasons": []}]}
        with tempfile.TemporaryDirectory() as dd:
            lab = FakeLab(T0 + 60 * H, FakeStore(), write=True, base=dd)
            res, led = experiments.run_design(lab, design(), Mod, T0)
            lines = lambda: sum(len(p.read_text().splitlines()) for p in Path(dd).rglob("*.jsonl"))
            n1 = lines()
            experiments.run_design(lab, design(), Mod, T0)
            self.assertEqual(n1, lines())
            outs = [json.loads(l) for p in Path(dd, "research/outcomes").rglob("*.jsonl") for l in p.read_text().splitlines()]
            self.assertTrue(outs and all(o["label"]["status"] == "complete" for o in outs))
            self.assertEqual(len(led), 1)
            self.assertIn(res["status"], ("supported", "under prospective evaluation", "retired"))


class EvidenceAndSkillEvalTests(unittest.TestCase):
    def test_no_proposal_unless_supported(self):
        cards = [{"design": "X", "status": "exploratory", "status_reason": "no evaluation episodes yet",
                  "passes": {"prospective": {"reasons": ["2 days of data"]}}}]
        text = evidence.skill_proposals(cards, T0)
        self.assertIn("No change is proposed", text)
        self.assertNotIn("Proposed text", text)

    def test_overclaim_detection_and_negation(self):
        cards = {"A1-flow-absorption": {"design": "A1-flow-absorption", "module": "flow_absorption", "status": "exploratory"},
                 "G1-alt-stress-propagation": {"design": "G1-alt-stress-propagation", "module": "cross_asset",
                                               "status": "exploratory"}}
        f = skill_eval.evidence_audit("Flow absorption is a demonstrated edge. Alt stress propagation is not yet supported.",
                                      cards)
        over = [x for x in f if x["kind"] == "overclaim"]
        self.assertEqual([x["design"] for x in over], ["A1-flow-absorption"])

    def test_fixture_evaluation_and_privacy(self):
        base = FIX / "skill_eval"
        cases = json.loads((Path(__file__).resolve().parents[1] / "lab/skill_eval_cases.json").read_text())["cases"]
        r = skill_eval.evaluate(base / "current", base / "revision", cases, skill_eval.load_cards(base / "cards"))
        self.assertEqual(r["cases"]["regressions"], ["decision-status-taxonomy"])
        self.assertEqual(len(r["evidence_audit"]["revision_overclaims"]), 1)
        self.assertEqual(r, skill_eval.evaluate(base / "current", base / "revision", cases,
                                                skill_eval.load_cards(base / "cards")))   # deterministic
        repo = Path(__file__).resolve().parents[1]
        with patch("sys.stderr", io.StringIO()):
            self.assertEqual(skill_eval.main(["--current", str(base / "current"), "--revision", str(base / "revision"),
                                              "--out", str(repo / "private-out")]), 2)
        self.assertFalse((repo / "private-out").exists())

    def test_live_without_key_is_not_run(self):
        base = FIX / "skill_eval"
        with tempfile.TemporaryDirectory() as out, patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}), \
                patch("sys.stdout", io.StringIO()):
            skill_eval.main(["--current", str(base / "current"), "--revision", str(base / "revision"), "--out", out,
                             "--base", str(base / "cards"), "--live", "--model", "m"])
            r = json.loads(next(Path(out).glob("*.json")).read_text())
        self.assertTrue(r["live"]["status"].startswith("live evaluation not run"))
        self.assertNotIn("results", r["live"])

    def test_live_with_fake_transport(self):
        class Resp(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False
        calls = []

        def opener(req, timeout=0):
            calls.append(json.loads(req.data))
            return Resp(json.dumps({"content": [{"type": "text", "text": "Insufficient data: too few episodes."}]}).encode())
        cases = [{"id": "c", "prompt": "Is this an edge?", "response_must": ["insufficient"]}]
        out = skill_eval.live(cases, "CUR", "REV", "m", "k", opener)
        self.assertTrue(out["c"]["current"]["pass"] and out["c"]["revision"]["pass"])
        self.assertEqual([c["system"] for c in calls], ["CUR", "REV"])


class EndToEndTests(unittest.TestCase):
    def test_run_isolates_module_errors_and_writes_reports(self):
        repo = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            Path(d, "lab/designs").mkdir(parents=True)
            for f in (repo / "lab/designs").glob("*.json"):
                Path(d, "lab/designs", f.name).write_bytes(f.read_bytes())
            bad = json.loads(Path(d, "lab/designs/H1-deleveraging-stress.json").read_text())
            bad.update(id="Z9-broken", module="no_such_module")
            Path(d, "lab/designs/Z9-broken.json").write_text(json.dumps(bad))
            with patch("sys.stdout", io.StringIO()), patch.dict(os.environ, {"STREAM_DATA_DIR": ""}):
                rc = lab_main(["update", "--base", d, "--now", str(T0)])
            self.assertEqual(rc, 1)                                       # an error is surfaced...
            cards = {p.stem: json.loads(p.read_text()) for p in Path(d, "research/evidence/cards").glob("*.json")}
            self.assertEqual(len(cards), 9)                               # ...and every other design still reported
            self.assertEqual(cards["Z9-broken"]["status"], "error")
            self.assertEqual(cards["E1-liquidity-recovery"]["passes"]["prospective"]["state"], "unavailable")
            self.assertTrue(all(c["status"] in ("exploratory", "error") for c in cards.values()))
            self.assertIn("No change is proposed", Path(d, "reports/skill_proposals.md").read_text())
            self.assertTrue(Path(d, "state/lab_registered.json").exists())


if __name__ == "__main__":
    unittest.main()
