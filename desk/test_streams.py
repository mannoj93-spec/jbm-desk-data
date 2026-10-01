#!/usr/bin/env python3
"""Tests for the repo 2.20 prospective streams: the RC1D companion B1 (companion_job.py), the paper sizing
experiment PS1 (paper_ps1.py, desk/research/ps1/) and the read-only feasibility report (feasibility.py).

The consequential failure modes, one class each:
  TestLookAhead            future information entering a fit or a decision
  TestLateRegistration     a late companion accepted as prospective
  TestHindsightFills       an earlier or retrospective quote used as an executable fill
  TestJointMissingData     missing data producing a selective arm comparison
  TestAccounting           cost, turnover, sizing and portfolio-accounting errors
  TestRetries              retry duplication or inconsistent records
  TestIdentityPreserved    new code changing existing experiment identities or frozen outputs
  TestRC1DCompatibility    the RC1D stream, its validator, its reader and its scorer unaffected
Offline: fixtures are copied from the repository's own registered 2026-09-30T20:00Z RC1D batch; the network and
git are injected.
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import math
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
BASE = DESK.parent
for p in (str(DESK), str(BASE)):
    if p not in sys.path:
        sys.path.insert(0, p)
os.environ.setdefault("RANGE_JOB_QUIET", "1")

import companion_job as CJ       # noqa: E402
import paper_ps1 as P            # noqa: E402
import range_contract as C       # noqa: E402
import range_model as R          # noqa: E402
import stream_util as U          # noqa: E402

UTC = dt.timezone.utc
DEC = dt.datetime(2026, 9, 30, 20, 0, tzinfo=UTC)
IDS = [f"range-rc1d-{h}-20260930T2000Z" for h in ("4h", "24h", "72h")]
START_MS = U.ms(dt.datetime(2026, 9, 30, 20, 25, tzinfo=UTC))


def _have_fixture():
    try:
        m = json.loads((BASE / "state/forecast_manifest.json").read_text())
        return all(i in m for i in IDS)
    except (OSError, ValueError):
        return False


def make_base(tmp: Path) -> Path:
    """A minimal repository copy: the 2026-09-30T20:00Z RC1D batch (manifest entries, frozen bytes, bundle,
    publication row) plus the modules the reader imports."""
    m = json.loads((BASE / "state/forecast_manifest.json").read_text())
    sub = {i: m[i] for i in IDS}
    (tmp / "state").mkdir(parents=True)
    (tmp / "state/forecast_manifest.json").write_text(json.dumps(sub))
    pubs = [l for l in (BASE / "state/range_publications.jsonl").read_text().splitlines() if IDS[0] in l]
    (tmp / "state/range_publications.jsonl").write_text("\n".join(pubs) + "\n")
    for e in sub.values():
        dst = tmp / e["frozen"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(BASE / e["frozen"], dst)
    doc = json.loads((BASE / sub[IDS[0]]["frozen"]).read_bytes())
    b = f"desk/inputs/2026-09/{doc['input_bundle']}.json.gz"
    (tmp / b).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(BASE / b, tmp / b)
    U.transition(tmp, P.ROOT, P.PROTOCOL_SHA256, "approved", by="operator", reason="test fixture: protocol approved")
    return tmp


def synthetic_fit(month="2026-09"):
    """A valid B1 companion fit document (coefficients from a small synthetic panel - shape, not quality)."""
    import random
    rnd = random.Random(7)
    bars, t, px = [], dt.datetime(2026, 1, 1, tzinfo=UTC), 80000.0
    for _ in range(900):
        o = px
        c = o * math.exp(rnd.gauss(0, 0.008))
        h, l = max(o, c) * (1 + abs(rnd.gauss(0, 0.004))), min(o, c) * (1 - abs(rnd.gauss(0, 0.004)))
        bars.append({"open_utc": U.iso(t), "close_utc": U.iso(t + dt.timedelta(hours=4)), "open": o, "high": h, "low": l, "close": c})
        t += dt.timedelta(hours=4)
        px = c
    m0 = U.parse(bars[-1]["close_utc"])
    fits = CJ.build_fit(bars, [], [], m0)
    return {"month": month, "model": "B1", "refit_utc": f"{month}-01T00:00:00Z", "fits":
            {h: dict(f, last_target_close_utc=f"{month}-01T00:00:00Z", refit_utc=f"{month}-01T00:00:00Z") for h, f in fits.items()}}


class Clock:
    def __init__(self, t_ms):
        self.t = t_ms

    def __call__(self):
        self.t += 7
        return self.t


def book(bid=83000.0, ask=83000.5, size=5.0, levels=20):
    return {"bids": [[f"{bid - i:.2f}", f"{size}"] for i in range(levels)],
            "asks": [[f"{ask + i:.2f}", f"{size}"] for i in range(levels)]}


def quote_fetcher(clock, bid=83000.0, ask=83000.5, sent_offset_ms=0, retrieval=None):
    def fetch(url, clock=clock):
        s = clock() + sent_offset_ms
        q = dict(book(bid, ask), source=url, t_sent_ms=s, t_received_ms=s + 300, http_date=None, http_date_ms=None,
                 last_update_id=1, raw_sha256="x", retrieval=retrieval or "live request (not a retrospective quote)")
        return q
    return fetch


def proto_for_tests():
    proto = P.load_protocol()
    proto = copy.deepcopy(proto)
    proto["start"]["not_before_utc"] = "2026-09-01T00:00:00Z"
    return proto


# =============================================================================================
@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestLookAhead(unittest.TestCase):
    def test_calibration_refuses_inputs_after_cutoff(self):
        sys.path.insert(0, str(DESK / "research/ps1"))
        import calibrate as K
        bars = [{"open_utc": "2026-09-22T20:00:00Z", "close_utc": "2026-09-23T00:00:01Z", "open": 1, "high": 1, "low": 1, "close": 1}]
        with self.assertRaises(ValueError):
            K.compute(bars, [], [])

    def test_companion_fit_refuses_bars_at_or_after_month_start(self):
        fit = synthetic_fit()
        self.assertTrue(all(f["last_target_close_utc"] <= "2026-09-01T00:00:00Z" for f in fit["fits"].values()))
        with self.assertRaises(ValueError):
            CJ.build_fit([{"open_utc": "2026-10-01T00:00:00Z", "close_utc": "2026-10-01T04:00:00Z",
                           "open": 1, "high": 1, "low": 1, "close": 1}], [], [], dt.datetime(2026, 10, 1, tzinfo=UTC))

    def test_fit_validation_rejects_a_future_training_target(self):
        fit = synthetic_fit()
        fit["fits"]["24h"]["last_target_close_utc"] = "2026-09-01T04:00:00Z"
        with self.assertRaises(ValueError):
            CJ.validate_fit(fit, dt.datetime(2026, 9, 1, tzinfo=UTC))

    def test_paper_weights_use_only_the_bundle_that_ends_at_the_decision(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            doc, _, _ = U.rc1d_record(base, IDS[0])
            bundle = U.rc1d_bundle(base, doc)
            self.assertEqual(bundle["bars"][-1]["close_utc"], "2026-09-30T20:00:00Z")
            rec = P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=Clock(START_MS + 60000), proto=proto_for_tests(),
                           run={"event": "test"})
            self.assertEqual(rec["action"], "rebalance")
            self.assertAlmostEqual(rec["sd_park_42"], P.sd_park(bundle["bars"]), places=15)
            self.assertLessEqual(max(b["close_utc"] for b in bundle["bars"]), rec["decision_utc"])


# =============================================================================================
@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestLateRegistration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = make_base(Path(self.tmp.name))
        f = CJ.fit_path(self.base, "2026-09")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(synthetic_fit()))

    def tearDown(self):
        self.tmp.cleanup()

    def test_inside_the_margin_nothing_is_computed_or_registered(self):
        out = CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=24), clock=Clock(START_MS - 90_000), run={})
        self.assertEqual(out, [])
        self.assertFalse((self.base / CJ.FORECASTS).exists())
        states = {r["state"] for r in U.rows(self.base / CJ.ATTEMPTS)}
        self.assertEqual(states, {"missed"})
        again = CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        self.assertEqual(again, [])                      # a missed companion is never registered on a later run
        self.assertEqual(len(U.rows(self.base / CJ.ATTEMPTS)), 3)

    def test_on_time_then_confirmed_late_is_ineligible(self):
        out = CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        self.assertEqual(len(out), 3)
        reg = CJ.registered(self.base)
        remote = lambda path: ("c0ffee", reg[Path(path).stem]["sha256"])       # noqa: E731
        rows = CJ.confirm(self.base, clock=Clock(START_MS + 1000), remote=remote)
        self.assertTrue(rows and not any(r["eligible"] for r in rows))

    def test_on_time_and_confirmed_before_start_is_eligible(self):
        CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        reg = CJ.registered(self.base)
        rows = CJ.confirm(self.base, clock=Clock(START_MS - 300_000), remote=lambda p: ("c", reg[Path(p).stem]["sha256"]))
        self.assertTrue(all(r["eligible"] for r in rows))

    def test_a_remote_mismatch_is_not_confirmed(self):
        CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        self.assertEqual(CJ.confirm(self.base, clock=Clock(START_MS - 300_000), remote=lambda p: ("c", "0" * 64)), [])

    def test_late_companions_are_excluded_from_pairs(self):
        CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        reg = CJ.registered(self.base)
        CJ.confirm(self.base, clock=Clock(START_MS + 1000), remote=lambda p: ("c", reg[Path(p).stem]["sha256"]))
        score = {"id": IDS[0], "publication": {"eligible": True}, "events": [
            {"name": "B2 range model", "realized_ln_range": 0.01, "abs_error_log_lr": 0.2},
            {"name": "B0 persistence baseline", "realized_ln_range": 0.01, "abs_error_log_lr": 0.3}]}
        (self.base / "registry").mkdir(exist_ok=True)
        (self.base / "registry/scores.jsonl").write_text(json.dumps(score) + "\n")
        CJ.score(self.base)
        ev = CJ.evaluation(self.base)["horizons"]["4h"]
        self.assertEqual((ev["paired"], ev["late_companion"]), (0, 1))

    def test_companion_values_use_the_frozen_window_features(self):
        doc, _, _ = U.rc1d_record(self.base, IDS[1])
        feats = U.rc1d_bundle(self.base, doc)["features"]["24h"]
        self.assertEqual((feats["start_utc"], feats["end_utc"]), (doc["start_utc"], doc["horizon_utc"]))
        v = CJ.values(synthetic_fit()["fits"]["24h"], feats)
        self.assertTrue(math.isfinite(v["point"]))


# =============================================================================================
class TestHindsightFills(unittest.TestCase):
    def test_quote_requested_before_executable_is_rejected(self):
        q = dict(book(), t_sent_ms=1000, t_received_ms=1300, retrieval="live request (not a retrospective quote)",
                 source="https://www.binance.com/api/v3/depth?symbol=BTCUSDT&limit=20", last_update_id=7, http_date_ms=None)
        self.assertEqual(P.eligible_quote(q, executable_ms=1000, deadline_ms=10**12)[0], False)
        self.assertEqual(P.eligible_quote(dict(q, t_sent_ms=1001), 1000, 10**12)[0], True)

    def test_retrospective_or_candle_quote_is_rejected(self):
        q = dict(book(), t_sent_ms=2000, t_received_ms=2300, retrieval="kline close")
        self.assertFalse(P.eligible_quote(q, 1000, 10**12)[0])

    def test_quote_after_deadline_is_rejected(self):
        q = dict(book(), t_sent_ms=2000, t_received_ms=9000, retrieval="live request (not a retrospective quote)")
        self.assertFalse(P.eligible_quote(q, 1000, 5000)[0])

    def test_crossed_or_thin_book_is_rejected(self):
        self.assertIn("crossed or locked book", P.validate_book(book(bid=100, ask=99)))
        self.assertIn("fewer than 5 levels", P.validate_book(book(levels=3)))

    @unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
    def test_execute_never_fills_on_a_pre_executable_quote(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            clk = Clock(START_MS)
            proto = proto_for_tests()
            P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=clk, proto=proto, run={})
            P.confirm(base, clock=clk, remote=lambda p: ("c", U.rows(base / P.DECISIONS)))
            res = P.execute(base, clock=clk, fetch=quote_fetcher(clk, sent_offset_ms=-3_600_000), proto=proto, run={},
                            pause=lambda s: None)
            self.assertEqual(res["outcome"], "no eligible quote")
            self.assertEqual(U.rows(base / P.EXECUTIONS), [])
            self.assertTrue(all(not q["eligible"] for q in U.rows(base / P.QUOTES)))


# =============================================================================================
@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestJointMissingData(unittest.TestCase):
    def test_missing_forecast_holds_every_arm(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            rec = P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=Clock(START_MS), proto=proto_for_tests(), run={},
                           read_current=lambda b, n, h: {"state": "missing", "reason": "none"})
            self.assertEqual(rec["action"], "no-rebalance")
            self.assertNotIn("w_target", rec)
            self.assertIsNone(P.execute(base, clock=Clock(START_MS), fetch=quote_fetcher(Clock(START_MS)),
                                        proto=proto_for_tests(), run={}, pause=lambda s: None))

    def test_missing_bundle_holds_every_arm(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            for p in (base / "desk/inputs/2026-09").glob("*.gz"):
                p.unlink()
            rec = P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=Clock(START_MS), proto=proto_for_tests(), run={})
            self.assertEqual(rec["action"], "no-rebalance")

    def test_stale_decision_is_missed_not_executed_late(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            rec = P.decide(base, now=DEC + dt.timedelta(minutes=95), clock=Clock(START_MS), proto=proto_for_tests(), run={})
            self.assertEqual(rec["action"], "missed")

    def test_a_missed_quote_leaves_all_ledgers_unchanged_and_the_interval_open(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            clk, proto = Clock(START_MS), proto_for_tests()
            P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=clk, proto=proto, run={})
            P.confirm(base, clock=clk, remote=lambda p: ("c", U.rows(base / P.DECISIONS)))

            def fail(url, clock=None):
                raise OSError("no route")
            P.execute(base, clock=clk, fetch=fail, proto=proto, run={}, pause=lambda s: None)
            st = P.ledger_state(base, proto)
            self.assertTrue(all(v == {"cash": 100000.0, "btc": 0.0} for v in st.values()))

    def test_every_execution_row_set_covers_all_arms_and_scenarios(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            clk, proto = Clock(START_MS), proto_for_tests()
            P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=clk, proto=proto, run={})
            P.confirm(base, clock=clk, remote=lambda p: ("c", U.rows(base / P.DECISIONS)))
            P.execute(base, clock=clk, fetch=quote_fetcher(clk), proto=proto, run={}, pause=lambda s: None)
            got = {(r["scenario"], r["arm"]) for r in U.rows(base / P.EXECUTIONS)}
            self.assertEqual(got, {(s, a) for s in P.SCENARIOS for a in P.ARMS})
            self.assertEqual(len({r["quote_id"] for r in U.rows(base / P.EXECUTIONS)}), 1)


# =============================================================================================
class TestAccounting(unittest.TestCase):
    cost = {"taker_fee_bp": 10.0, "slippage_bp": 1.0}

    def test_buy_from_cash_charges_spread_slippage_and_fee(self):
        st, rec = P.rebalance({"cash": 100000.0, "btc": 0.0}, 0.5, book(83000.0, 83001.0), self.cost, 0.05)
        mid = 83000.5
        self.assertAlmostEqual(rec["equity_pre"], 100000.0)
        exp_price = 83001.0 * 1.0001
        self.assertAlmostEqual(rec["fill_price"], exp_price, places=6)
        self.assertAlmostEqual(rec["fee"], rec["notional"] * 0.001, places=9)
        self.assertAlmostEqual(st["cash"] + st["btc"] * mid, rec["equity_post"], places=6)
        self.assertAlmostEqual(rec["cost_vs_mid"], rec["traded_btc"] * (exp_price - mid) + rec["fee"], places=6)
        self.assertGreater(rec["cost_vs_mid"], 0)

    def test_full_weight_never_borrows(self):
        st, rec = P.rebalance({"cash": 100000.0, "btc": 0.0}, 1.0, book(), self.cost, 0.05)
        self.assertGreaterEqual(st["cash"], 0.0)

    def test_sell_never_shorts_and_band_suppresses_small_trades(self):
        st, rec = P.rebalance({"cash": 0.0, "btc": 1.0}, 0.0, book(), self.cost, 0.05)
        self.assertAlmostEqual(st["btc"], 0.0, places=12)
        st2, rec2 = P.rebalance({"cash": 50000.0, "btc": 50000.0 / 83000.25}, 0.53, book(), self.cost, 0.05)
        self.assertEqual(rec2["traded_btc"], 0.0)
        self.assertEqual(rec2["fee"], 0.0)

    def test_depth_walk_and_beyond_depth_penalty(self):
        f = P.fill_price(book(size=0.1, levels=5), "buy", 1.0, 0.0)
        self.assertAlmostEqual(f["beyond_captured_depth_btc"], 0.5)
        self.assertGreater(f["vwap"], 83000.5 + 2)

    def test_weights_match_the_protocol_formulas(self):
        c = P.constants(P.load_protocol())
        w = P.weights(0.01, 0.008, c)
        self.assertAlmostEqual(w["B2"], min(1, c["sigma_star_4h"] / (c["k_b2"] * 0.01)))
        self.assertAlmostEqual(w["VOL"], min(1, c["sigma_star_4h"] / (c["k_vol"] * 0.008)))
        self.assertAlmostEqual(w["FIXED"], c["sigma_star_4h"] / c["s_uncond"])
        self.assertEqual(P.weights(1e-6, 1e-6, c)["B2"], 1.0)

    def test_interval_returns_turnover_and_sharpe(self):
        # PS1 v2: duration-weighted on elapsed hours, log returns, exposure = weight held over the interval
        rows = [{"equity_pre": 100.0, "interval_log_return": None, "elapsed_h": None, "notional": 50.0, "w_after": 0.5,
                 "w_held": None, "cost_vs_mid": 0.1, "interval_flag": "entry"},
                {"equity_pre": 110.0, "interval_log_return": math.log(1.1), "elapsed_h": 4.0, "notional": 0.0, "w_after": 0.5,
                 "w_held": 0.5, "cost_vs_mid": 0.0, "interval_flag": "scheduled"},
                {"equity_pre": 99.0, "interval_log_return": math.log(0.9), "elapsed_h": 4.0, "notional": 10.0, "w_after": 0.4,
                 "w_held": 0.5, "cost_vs_mid": 0.02, "interval_flag": "scheduled"}]
        s = P.arm_stats(rows)
        self.assertAlmostEqual(s["net_return"], -0.01)
        self.assertAlmostEqual(s["max_drawdown_marks"], 99 / 110 - 1)
        self.assertAlmostEqual(s["exposure_mean"], 0.5)
        r = [math.log(1.1), math.log(0.9)]
        m, sd = sum(r) / 2, math.sqrt(sum((x - sum(r) / 2) ** 2 for x in r))
        self.assertAlmostEqual(s["sharpe_ann"], m / sd * math.sqrt(2190), places=9)
        self.assertAlmostEqual(s["turnover_ann"], 60 / (309 / 3) / (8 / 8760))

    def test_bootstrap_is_deterministic_and_gated_by_blocks(self):
        import random
        rnd = random.Random(1)
        a = [rnd.gauss(0.001, 0.01) for _ in range(430)]
        b = [x - 0.0005 for x in a]
        self.assertEqual(P.bootstrap_sharpe_diff(a, b, reps=200), P.bootstrap_sharpe_diff(a, b, reps=200))


# =============================================================================================
@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestRetries(unittest.TestCase):
    def test_decide_confirm_execute_are_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            clk, proto = Clock(START_MS), proto_for_tests()
            for _ in range(2):
                P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=clk, proto=proto, run={})
                P.confirm(base, clock=clk, remote=lambda p: ("c", U.rows(base / P.DECISIONS)))
                P.execute(base, clock=clk, fetch=quote_fetcher(clk), proto=proto, run={}, pause=lambda s: None)
            self.assertEqual(len(U.rows(base / P.DECISIONS)), 1)
            self.assertEqual(len(U.rows(base / P.CONFIRMS)), 1)
            self.assertEqual(len(U.rows(base / P.EXECUTIONS)), 6)
            self.assertTrue((base / P.LAUNCH).exists())

    def test_companion_retry_does_not_duplicate_or_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            f = CJ.fit_path(base, "2026-09")
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(synthetic_fit()))
            a = CJ.forecast(base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
            b = CJ.forecast(base, now=DEC + dt.timedelta(minutes=18), clock=Clock(START_MS - 500_000), run={})
            self.assertEqual((len(a), b), (3, []))
            self.assertEqual(len(U.rows(base / CJ.REGISTRY)), 3)

    def test_protocol_change_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "protocol.json"
            p.write_bytes(P.PROTOCOL.read_bytes().replace(b'"rebalance_band": 0.05', b'"rebalance_band": 0.04'))
            with self.assertRaises(P.Refused):
                P.load_protocol(p)


# =============================================================================================
class TestIdentityPreserved(unittest.TestCase):
    def test_protocol_and_calibration_hashes_are_frozen(self):
        proto = P.load_protocol()                                    # raises on any drift
        self.assertEqual(proto["id"], "PS1")
        cal = json.loads((DESK / "research/ps1/calibration.json").read_text())
        self.assertEqual(cal["constants"], proto["calibration"]["constants"])

    def test_rc1d_contract_model_and_job_identities_unchanged(self):
        import range_job as J
        self.assertEqual(C.contract_id("RC1D"), "RC1D/contract-12.0.0/175a4dd4c6c0")
        self.assertEqual(C.contract_id("RC1"), "RC1/contract-12.0.0/e8f291740f27")
        self.assertTrue(J.spec_ok())
        self.assertEqual(J.JOB_VERSION, "range-job-12.4.0")
        self.assertEqual(C.SELECTED, {"4h": "B2", "24h": "B2", "72h": "B2"})

    def test_lab_code_identity_unchanged(self):
        """The new code lives outside lab/, so the lab's code hash and every design's evaluation version stay."""
        from lab import common
        idx = json.loads((BASE / "research/evidence/index.json").read_text())["designs"]
        cards = [json.loads((BASE / f"research/evidence/v2/{d}@{i['current']}.json").read_text()) for d, i in idx.items()]
        self.assertTrue(all(c["dependencies"]["code_sha256"] == common.code_hash() for c in cards))

    @unittest.skipUnless(sys.version_info[:2] == (3, 12), "evaluation versions hash the Python 3.12 AST (production)")
    def test_lab_evaluation_versions_unchanged(self):
        from lab import experiments as E
        idx = json.loads((BASE / "research/evidence/index.json").read_text())["designs"]
        for p in E.design_files(str(BASE)):
            d = E.attach_version(str(BASE), E.load_design(p))
            self.assertEqual(d["_version"], idx[d["id"]]["current"], d["id"])

    def test_new_streams_write_nowhere_the_existing_streams_read(self):
        for mod in (CJ, P):
            for name in dir(mod):
                v = getattr(mod, name)
                if isinstance(v, str) and ("/" in v) and v.startswith(("registry", "state/", "research/", "lab/")):
                    self.fail(f"{mod.__name__}.{name} = {v}")
        self.assertTrue(CJ.ROOT.startswith("streams/") and P.ROOT.startswith("streams/"))

    def test_companion_ids_cannot_collide_with_rc1d_or_lab_ids(self):
        self.assertFalse(CJ.ID_PREFIX.startswith("range-"))
        self.assertNotIn("B1-underwater", CJ.ID_PREFIX)


# =============================================================================================
@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestRC1DCompatibility(unittest.TestCase):
    def test_registered_rc1d_record_still_validates_and_reads(self):
        import range_reader as RR
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            doc, entry, pub = U.rc1d_record(base, IDS[0])
            self.assertEqual(C.validate_rc1d(doc, IDS[0], entry, pub, {C.contract_id("RC1D")}), [])
            r = RR.read_current(base, DEC + dt.timedelta(minutes=40), "4h")
            self.assertEqual((r["state"], r["id"]), ("valid-current", IDS[0]))

    def test_companion_run_leaves_rc1d_files_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            before = {p: p.read_bytes() for p in list((base / "registry").rglob("*")) + [base / "state/forecast_manifest.json"] if p.is_file()}
            f = CJ.fit_path(base, "2026-09")
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(json.dumps(synthetic_fit()))
            CJ.forecast(base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
            clk = Clock(START_MS)
            P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=clk, proto=proto_for_tests(), run={})
            after = {p: p.read_bytes() for p in list((base / "registry").rglob("*")) + [base / "state/forecast_manifest.json"] if p.is_file()}
            self.assertEqual(before, after)

    def test_companion_scores_use_the_rc1d_loss_function(self):
        loss = C.losses(0.012, [0.008, 0.011, 0.02], 0.015)
        self.assertAlmostEqual(loss["abs_error_log_lr"], abs(math.log(0.012) - math.log(0.015)), places=10)


class TestFeasibility(unittest.TestCase):
    def test_no_eta_without_enough_events_and_intervals_contain_the_rate(self):
        import feasibility as F
        self.assertIsNone(F.eta_days(100, 0, 0, 10))
        self.assertIsNone(F.eta_days(100, 4, 4, 10))
        e = F.eta_days(100, 20, 20, 10)
        self.assertLess(e["fast"], e["central"])
        self.assertLess(e["central"], e["slow"])
        lo, hi = F.poisson_rate_ci90(20, 10)
        self.assertTrue(lo < 2.0 < hi)

    def test_report_builds_from_this_checkout_and_never_calls_unobservable_zero_a_rate(self):
        import feasibility as F
        doc = F.build(BASE)
        e1 = [r for r in doc["lab"] if r["id"].startswith("E1")]
        if e1:
            self.assertEqual(e1[0]["limiting_factor"], "infrastructure capability")
            self.assertIsNone(e1[0]["time_to_checkpoint"])

# =============================================================================================
# Repo 2.21 maintenance regressions
# =============================================================================================
SRC = "https://www.binance.com/api/v3/depth?symbol=BTCUSDT&limit=20"


class Interrupted(BaseException):
    """A simulated process death (not an Exception, so nothing in the job can swallow it)."""


def crash_after(k):
    def writer(base, rows):
        from storage import append_unique
        if k:
            append_unique(Path(base) / P.EXECUTIONS, rows[:k], key=lambda x: (x["execution_id"], x["scenario"], x["arm"]))
        raise Interrupted(f"interrupted after {k} row(s)")
    return writer


class CountingFetch:
    def __init__(self, clock, **kw):
        self.f, self.n = quote_fetcher(clock, **kw), 0

    def __call__(self, url, clock=None):
        self.n += 1
        return self.f(url)


def _rewrite(path, fn):
    rows = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    Path(path).write_text("".join(json.dumps(fn(r)) + "\n" for r in rows))


def _ps1_ready(base, clk, proto):
    P.decide(base, now=DEC + dt.timedelta(minutes=40), clock=clk, proto=proto, run={})
    P.confirm(base, clock=clk, remote=lambda p: ("c", U.rows(base / P.DECISIONS)))


def _final_states(base):
    return {e: st[-1]["state"] for e, st in P.exec_states(base).items()}


def _clean_ledger():
    with tempfile.TemporaryDirectory() as d:
        base = make_base(Path(d))
        clk, proto = Clock(START_MS), proto_for_tests()
        _ps1_ready(base, clk, proto)
        P.execute(base, clock=clk, fetch=quote_fetcher(clk), proto=proto, run={}, pause=lambda s: None)
        return P.ledger_state(base, proto)


@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestAtomicExecution(unittest.TestCase):
    """Finding 1: an execution writes all six rows or none, carries explicit states and recovers from its snapshot."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = make_base(Path(self.tmp.name))
        self.clk, self.proto = Clock(START_MS), proto_for_tests()
        _ps1_ready(self.base, self.clk, self.proto)

    def tearDown(self):
        self.tmp.cleanup()

    def _interrupt(self, k):
        fetch = CountingFetch(self.clk)
        with self.assertRaises(Interrupted):
            P.execute(self.base, clock=self.clk, fetch=fetch, proto=self.proto, run={}, pause=lambda s: None, writer=crash_after(k))
        return fetch

    def test_completed_execution_records_states_and_a_row_hash(self):
        P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={}, pause=lambda s: None)
        states = list(P.exec_states(self.base).values())[0]
        self.assertEqual([r["state"] for r in states], ["pending", "running", "completed"])
        rows = U.rows(self.base / P.EXECUTIONS)
        self.assertEqual(P.rows_sha(rows), states[-1]["rows_sha256"])
        self.assertTrue(all(r["execution_id"] == states[0]["execution_id"] for r in rows))

    def test_interruption_before_any_row_recovers_from_the_snapshot_without_a_new_quote(self):
        fetch = self._interrupt(0)
        self.assertEqual(U.rows(self.base / P.EXECUTIONS), [])
        self.assertEqual(set(_final_states(self.base).values()), {"running"})
        self.assertEqual(P.ledger(self.base)[0], [])                    # nothing in progress enters the ledger
        n = fetch.n
        self.assertIsNone(P.execute(self.base, clock=self.clk, fetch=fetch, proto=self.proto, run={}, pause=lambda s: None))
        self.assertEqual(fetch.n, n)                                    # recovery never captures a quote
        self.assertEqual(set(_final_states(self.base).values()), {"recovered"})
        self.assertEqual(P.ledger_state(self.base, self.proto), _clean_ledger())

    def test_interruption_after_the_first_row_preserves_it_and_rebuilds_under_a_new_id(self):
        self._interrupt(1)
        self.assertEqual(len(U.rows(self.base / P.EXECUTIONS)), 1)
        self.assertEqual(P.ledger(self.base)[0], [])                    # the partial row is not in the ledger
        P.recover(self.base, self.proto, self.clk, run={})
        fs = _final_states(self.base)
        self.assertEqual(sorted(fs.values()), ["partially_written", "recovered"])
        rows = U.rows(self.base / P.EXECUTIONS)
        self.assertEqual(len(rows), 7)                                  # 1 preserved + 6 rebuilt
        good, bad = P.ledger(self.base)
        self.assertEqual((len(good), bad), (6, []))
        self.assertTrue(all(r["execution_id"].endswith("~r1") for r in good))
        self.assertEqual(P.ledger_state(self.base, self.proto), _clean_ledger())

    def test_interruption_halfway_preserves_the_partial_set_as_a_record(self):
        self._interrupt(3)
        P.recover(self.base, self.proto, self.clk, run={})
        partial = [e for e, s in _final_states(self.base).items() if s == "partially_written"][0]
        st = P.exec_states(self.base)[partial]
        self.assertEqual(st[-1]["rows_written"], 3)
        self.assertEqual(len([r for r in U.rows(self.base / P.EXECUTIONS) if r["execution_id"] == partial]), 3)

    def test_failed_retry_is_recorded_failed_and_the_decision_is_missed_not_re_executed(self):
        self._interrupt(0)
        _rewrite(self.base / P.QUOTES, lambda q: dict(q, bids=[[str(float(p) - 50), z] for p, z in q["bids"]]))
        before = (self.base / P.QUOTES).read_bytes()
        P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={}, pause=lambda s: None)
        st = list(P.exec_states(self.base).values())[0]
        self.assertEqual(st[-1]["state"], "failed")
        self.assertIn("quote row missing or changed", st[-1]["reason"])
        self.assertEqual(U.rows(self.base / P.EXECUTIONS), [])
        self.assertEqual((self.base / P.QUOTES).read_bytes(), before)  # the changed record stays as found
        self.assertTrue(any(r.get("outcome") == "missed-execution" for r in U.rows(self.base / P.RUNS)))
        self.assertIsNone(P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={},
                                    pause=lambda s: None))
        self.assertEqual(len(P.exec_states(self.base)), 1)

    def test_duplicate_execution_attempts_are_refused(self):
        P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={}, pause=lambda s: None)
        d = P.decisions(self.base)["ps1-20260930T2000Z"]
        conf = P.verified_confirmations(self.base)[d["decision_id"]]
        q = [r for r in U.rows(self.base / P.QUOTES) if r["eligible"]][0]
        with self.assertRaises(P.DuplicateExecution):
            P.start_execution(self.base, d, conf, q, self.proto, self.clk, {})
        self.assertIsNone(P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={},
                                    pause=lambda s: None))
        self.assertEqual(len(U.rows(self.base / P.EXECUTIONS)), 6)

    def test_an_execution_in_progress_blocks_a_second_one(self):
        self._interrupt(0)
        d = P.decisions(self.base)["ps1-20260930T2000Z"]
        conf = P.verified_confirmations(self.base)[d["decision_id"]]
        q = U.rows(self.base / P.QUOTES)[0]
        with self.assertRaises(P.DuplicateExecution):
            P.start_execution(self.base, d, conf, q, self.proto, self.clk, {})


class TestTimeAccounting(unittest.TestCase):
    """Finding 2: elapsed holding time, duration weighting, a documented basis, and no interpolation."""
    T0 = dt.datetime(2026, 10, 3, 0, 0, tzinfo=UTC)

    def _rows(self, decision, fill_after_close_min, prior_decision=None, prior_fill_ms=None):
        proto = proto_for_tests()
        prior = None
        if prior_decision is not None:
            prior = {"cash_after": 70000.0, "btc_after": 30000 / 83000.25, "equity_pre": 100000.0, "fill_time_ms": prior_fill_ms,
                     "w_after": 0.3, "decision_utc": U.iso(prior_decision), "execution_id": "x"}
        snap = {"execution_id": "e", "prior": {f"{s}/{a}": prior for s in P.SCENARIOS for a in P.ARMS},
                "executable_ms": 0, "sha256": "s"}
        fill = U.ms(decision) + fill_after_close_min * 60000
        d = {"decision_id": f"ps1-{decision:%Y%m%dT%H%MZ}", "decision_utc": U.iso(decision), "w_target": {a: 0.3 for a in P.ARMS}}
        q = dict(book(), quote_id="q", t_sent_ms=fill - 300, t_received_ms=fill)
        return P.build_rows(snap, d, q, proto)

    def test_normal_4h_interval(self):
        r = self._rows(self.T0 + dt.timedelta(hours=4), 20, self.T0, U.ms(self.T0) + 20 * 60000)[0]
        self.assertAlmostEqual(r["elapsed_h"], 4.0)
        self.assertEqual(r["interval_flag"], "scheduled")
        self.assertAlmostEqual(r["w_held"], 0.3)

    def test_delayed_execution_uses_the_actual_elapsed_time(self):
        r = self._rows(self.T0 + dt.timedelta(hours=4), 70, self.T0, U.ms(self.T0) + 20 * 60000)[0]
        self.assertAlmostEqual(r["elapsed_h"], 4 + 50 / 60)
        self.assertEqual(r["interval_flag"], "scheduled")

    def test_skipped_decision_extends_the_interval_and_creates_no_intermediate_return(self):
        rows = self._rows(self.T0 + dt.timedelta(hours=8), 20, self.T0, U.ms(self.T0) + 20 * 60000)
        self.assertEqual(len(rows), 6)                                  # one row per arm and scenario, nothing interpolated
        self.assertAlmostEqual(rows[0]["elapsed_h"], 8.0)
        self.assertEqual(rows[0]["interval_flag"], "extended (2 decision steps)")

    def test_multi_day_hold(self):
        r = self._rows(self.T0 + dt.timedelta(days=3), 20, self.T0, U.ms(self.T0) + 20 * 60000)[0]
        self.assertAlmostEqual(r["elapsed_h"], 72.0)
        self.assertTrue(r["interval_flag"].startswith("extended (18"))

    def test_entry_row_has_no_interval_and_partial_data_has_no_return(self):
        r = self._rows(self.T0, 20)[0]
        self.assertEqual((r["interval_flag"], r["interval_log_return"], r["elapsed_h"]), ("entry", None, None))
        s = P.arm_stats([dict(r, notional=0.0)])
        self.assertEqual((s["intervals"], s["sharpe_ann"], s["return_ann"], s["exposure_mean"]), (0, None, None, None))

    def test_duration_weighting_numerical_fixture(self):
        rs, dts = [0.02, -0.01, 0.03], [4.0, 8.0, 4.0]
        mu = 0.04 / 16
        var = (0.01 ** 2 + 0.03 ** 2 + 0.02 ** 2) / (16 * 2 / 3)
        st = P.dw_stats(rs, dts)
        self.assertAlmostEqual(st["mu_h"], mu, places=15)
        self.assertAlmostEqual(st["var_h"], var, places=15)
        self.assertAlmostEqual(P.sharpe_dw(rs, dts), mu * 8760 / math.sqrt(var * 8760), places=10)
        self.assertAlmostEqual(P.sharpe_dw(rs, dts), 21.9 / math.sqrt(1.14975), places=9)

    def test_equal_4h_intervals_reduce_to_the_v1_formula(self):
        import random
        rnd = random.Random(3)
        r = [rnd.gauss(0.0002, 0.01) for _ in range(200)]
        m = sum(r) / len(r)
        sd = math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1))
        self.assertAlmostEqual(P.sharpe_dw(r, [4.0] * len(r)), m / sd * math.sqrt(2190), places=9)

    def test_a_long_interval_weighs_by_its_length(self):
        rows = [{"equity_pre": 100.0, "interval_log_return": None, "elapsed_h": None, "notional": 0.0, "w_after": 0.5,
                 "w_held": None, "cost_vs_mid": 0.0, "interval_flag": "entry"},
                {"equity_pre": 101.0, "interval_log_return": 0.01, "elapsed_h": 4.0, "notional": 0.0, "w_after": 0.5,
                 "w_held": 0.5, "cost_vs_mid": 0.0, "interval_flag": "scheduled"},
                {"equity_pre": 120.0, "interval_log_return": 0.17, "elapsed_h": 72.0, "notional": 0.0, "w_after": 0.2,
                 "w_held": 0.2, "cost_vs_mid": 0.0, "interval_flag": "extended (18 decision steps)"}]
        s = P.arm_stats(rows)
        self.assertAlmostEqual(s["return_ann"], 0.18 / 76 * 8760)
        self.assertAlmostEqual(s["exposure_mean"], (0.5 * 4 + 0.2 * 72) / 76)
        self.assertEqual((s["extended_intervals"], s["longest_interval_h"], s["elapsed_hours"]), (1, 72.0, 76.0))


class TestQuoteValidation(unittest.TestCase):
    """Finding 4: finite, positive, ordered, timely, symbol-consistent quotes only."""
    def q(self, **kw):
        return dict(book(), source=SRC, t_sent_ms=10_000, t_received_ms=10_300, http_date_ms=None, last_update_id=9, **kw)

    def _lvl(self, side, i, p=None, z=None):
        b = book()
        lv = list(b[side][i])
        if p is not None:
            lv[0] = p
        if z is not None:
            lv[1] = z
        b[side][i] = lv
        return dict(self.q(), **{side: b[side]})

    def test_valid_quote_passes(self):
        self.assertEqual(P.validate_quote(self.q()), [])

    def test_nan_quantity(self):
        self.assertTrue(P.validate_quote(self._lvl("asks", 2, z="NaN")))

    def test_nan_price(self):
        self.assertTrue(P.validate_quote(self._lvl("bids", 0, p="nan")))

    def test_infinite_values(self):
        self.assertTrue(P.validate_quote(self._lvl("asks", 0, p="Infinity")))
        self.assertTrue(P.validate_quote(self._lvl("asks", 1, z="inf")))

    def test_zero_liquidity(self):
        self.assertIn("non-positive price or size", P.validate_quote(self._lvl("asks", 0, z="0")))

    def test_negative_quantity(self):
        self.assertIn("non-positive price or size", P.validate_quote(self._lvl("bids", 4, z="-1.5")))

    def test_missing_and_malformed_values(self):
        self.assertTrue(P.validate_quote(self._lvl("asks", 0, z="")))
        self.assertTrue(P.validate_quote(self._lvl("asks", 0, p=83000.5)))          # not a decimal string
        self.assertTrue(P.validate_quote(dict(self.q(), asks=None)))
        self.assertTrue(P.validate_quote(dict(self.q(), bids=[["83000.00"]] * 20)))
        self.assertTrue(P.validate_quote(dict(self.q(), last_update_id=None)))

    def test_stale_timestamps(self):
        self.assertTrue(any("stale" in x for x in P.validate_quote(dict(self.q(), t_received_ms=25_001))))
        self.assertTrue(any("stale" in x for x in P.validate_quote(dict(self.q(), http_date_ms=10_300 - 600_000))))
        self.assertTrue(P.validate_quote(dict(self.q(), t_received_ms=9_000)))

    def test_crossed_market(self):
        self.assertIn("crossed or locked book", P.validate_quote(dict(self.q(), **book(bid=83001.0, ask=83000.0))))

    def test_symbol_consistency(self):
        self.assertTrue(P.validate_quote(dict(self.q(), source=SRC.replace("BTCUSDT", "ETHUSDT"))))

    def test_rebalance_refuses_an_invalid_book(self):
        b = book()
        b["asks"][0] = ["83000.50", "NaN"]
        with self.assertRaises(ValueError):
            P.rebalance({"cash": 100000.0, "btc": 0.0}, 0.5, b, {"taker_fee_bp": 10.0, "slippage_bp": 1.0}, 0.05)

    @unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
    def test_a_nan_quote_is_recorded_ineligible_and_never_fills(self):
        with tempfile.TemporaryDirectory() as d:
            base = make_base(Path(d))
            clk, proto = Clock(START_MS), proto_for_tests()
            _ps1_ready(base, clk, proto)
            inner = quote_fetcher(clk)

            def nan_fetch(url, clock=None):
                q = inner(url)
                q["asks"][0] = ["83000.50", float("nan")]
                return q
            res = P.execute(base, clock=clk, fetch=nan_fetch, proto=proto, run={}, pause=lambda s: None)
            self.assertEqual(res["outcome"], "no eligible quote")
            self.assertEqual(U.rows(base / P.EXECUTIONS), [])
            qs = U.rows(base / P.QUOTES)
            self.assertTrue(qs and not any(q["eligible"] for q in qs))
            self.assertEqual(qs[0]["asks"][0][1], "nan")              # recorded as found, serializable


@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestConfirmationIntegrity(unittest.TestCase):
    """Finding 3: bindings are verified before execution, scoring and reporting; failures exclude and preserve."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = make_base(Path(self.tmp.name))
        self.clk, self.proto = Clock(START_MS), proto_for_tests()
        _ps1_ready(self.base, self.clk, self.proto)

    def tearDown(self):
        self.tmp.cleanup()

    def _exec(self):
        return P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={}, pause=lambda s: None)

    def _excluded(self, reason_part):
        before = {f: (self.base / f).read_bytes() for f in (P.DECISIONS, P.CONFIRMS)}
        self.assertIsNone(self._exec())
        self.assertEqual(U.rows(self.base / P.EXECUTIONS), [])
        fails = U.rows(self.base / P.ROOT / "integrity.jsonl")
        self.assertTrue(any(reason_part in f["reason"] for f in fails), fails)
        self.assertTrue(all(f["action"] == "excluded; original record preserved" for f in fails))
        self.assertEqual({f: (self.base / f).read_bytes() for f in before}, before)

    def test_unchanged_record_verifies_and_executes(self):
        c = U.rows(self.base / P.CONFIRMS)[0]
        self.assertEqual(c["binding_sha256"], U.sha(c["binding"]))
        self.assertEqual(c["binding"]["contract"], "RC1D/contract-12.0.0/175a4dd4c6c0")
        self.assertEqual(self._exec()["outcome"], "executed")
        self.assertFalse((self.base / P.ROOT / "integrity.jsonl").exists())

    def test_changed_value_after_confirmation_is_excluded(self):
        _rewrite(self.base / P.DECISIONS, lambda d: dict(d, w_target=dict(d["w_target"], B2=0.99)))
        self._excluded("decision row changed after confirmation")

    def test_changed_timestamp_in_the_decision_is_excluded(self):
        _rewrite(self.base / P.DECISIONS, lambda d: dict(d, computed_end_ms=d["computed_end_ms"] - 60_000))
        self._excluded("decision row changed after confirmation")

    def test_changed_confirmation_time_is_excluded(self):
        _rewrite(self.base / P.CONFIRMS, lambda c: dict(c, confirmed_ms=c["confirmed_ms"] - 600_000))
        self._excluded("confirmation time or commit differs")

    def test_changed_binding_metadata_is_excluded(self):
        _rewrite(self.base / P.CONFIRMS, lambda c: dict(c, binding=dict(c["binding"], contract="RC1D/other")))
        self._excluded("binding missing or altered")

    def test_changed_execution_rows_withhold_metrics_and_block_execution(self):
        self._exec()
        _rewrite(self.base / P.EXECUTIONS, lambda r: dict(r, cash_after=r["cash_after"] + 1))
        doc = P.report(self.base, now=DEC + dt.timedelta(hours=1), proto=self.proto)
        self.assertFalse(doc["integrity"]["ok"])
        self.assertEqual(doc["evidence_class"], "unavailable")
        self.assertEqual(P.ledger(self.base)[0], [])
        self.assertEqual(P.execute(self.base, clock=self.clk, fetch=quote_fetcher(self.clk), proto=self.proto, run={},
                                   pause=lambda s: None)["outcome"], "refused")


@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestCompanionIntegrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = make_base(Path(self.tmp.name))
        f = CJ.fit_path(self.base, "2026-09")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(synthetic_fit()))
        CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        reg = CJ.registered(self.base)
        CJ.confirm(self.base, clock=Clock(START_MS - 300_000), remote=lambda p: ("c", reg[Path(p).stem]["sha256"]))
        score = {"id": IDS[0], "publication": {"eligible": True}, "events": [
            {"name": "B2 range model", "realized_ln_range": 0.01, "abs_error_log_lr": 0.2},
            {"name": "B0 persistence baseline", "realized_ln_range": 0.01, "abs_error_log_lr": 0.3}]}
        (self.base / "registry").mkdir(exist_ok=True)
        (self.base / "registry/scores.jsonl").write_text(json.dumps(score) + "\n")
        self.cid = "rc1d-b1-4h-20260930T2000Z"
        self.fpath = self.base / CJ.registered(self.base)[self.cid]["path"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_unchanged_record_is_scored_with_its_hash(self):
        rows = CJ.score(self.base)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["forecast_sha256"], CJ.registered(self.base)[self.cid]["sha256"])
        self.assertEqual(rows[0]["verification"], "verified")
        self.assertEqual(CJ.evaluation(self.base)["horizons"]["4h"]["paired"], 1)

    def test_changed_value_is_not_scored_and_the_file_is_left_as_found(self):
        doc = json.loads(self.fpath.read_bytes())
        doc["point"] = doc["point"] * 1.5
        self.fpath.write_bytes(U.canonical(doc) + b"\n")
        raw = self.fpath.read_bytes()
        self.assertEqual(CJ.score(self.base), [])
        self.assertEqual(self.fpath.read_bytes(), raw)
        self.assertTrue(U.rows(self.base / CJ.ROOT / "integrity.jsonl"))

    def test_changed_confirmation_timestamp_is_not_scored(self):
        _rewrite(self.base / CJ.CONFIRMS, lambda c: dict(c, confirmed_ms=c["confirmed_ms"] - 1))
        self.assertEqual(CJ.score(self.base), [])

    def test_changed_binding_metadata_is_not_scored(self):
        _rewrite(self.base / CJ.CONFIRMS, lambda c: dict(c, binding=dict(c["binding"], version={"job": "x"})))
        self.assertEqual(CJ.score(self.base), [])

    def test_change_after_scoring_is_excluded_from_the_evaluation(self):
        CJ.score(self.base)
        self.fpath.write_bytes(self.fpath.read_bytes().replace(b'"model"', b'"model_"'))
        ev = CJ.evaluation(self.base)["horizons"]["4h"]
        self.assertEqual((ev["paired"], ev["excluded_integrity"]), (0, 1))

    def test_legacy_confirmation_is_verified_against_the_registry_hash(self):
        _rewrite(self.base / CJ.CONFIRMS, lambda c: {k: v for k, v in c.items() if k not in ("binding", "binding_sha256")})
        rows = CJ.score(self.base)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["verification"].startswith("legacy confirmation"))


@unittest.skipUnless(_have_fixture(), "RC1D fixture batch not in this checkout")
class TestLifecycle(unittest.TestCase):
    """Finding 5: explicit states; termination is the operator's, stops every stage, keeps history."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = make_base(Path(self.tmp.name))
        self.clk, self.proto = Clock(START_MS), proto_for_tests()

    def tearDown(self):
        self.tmp.cleanup()

    def _exec(self, fetch=None):
        return P.execute(self.base, clock=self.clk, fetch=fetch or quote_fetcher(self.clk), proto=self.proto, run={},
                         pause=lambda s: None)

    def test_a_job_cannot_terminate_or_archive(self):
        for st in ("terminated", "archived"):
            with self.assertRaises(U.LifecycleError):
                U.transition(self.base, P.ROOT, P.PROTOCOL_SHA256, st, by="job", reason="x")

    def test_termination_before_execution(self):
        _ps1_ready(self.base, self.clk, self.proto)
        P.operator_lifecycle("terminated", "test", base=self.base)
        before = (self.base / P.DECISIONS).read_bytes()
        self.assertEqual(self._exec()["outcome"], "refused")
        self.assertEqual(U.rows(self.base / P.EXECUTIONS), [])
        self.assertEqual((self.base / P.DECISIONS).read_bytes(), before)
        self.assertIsNone(P.decide(self.base, now=DEC + dt.timedelta(hours=4, minutes=40), clock=self.clk, proto=self.proto, run={}))

    def test_termination_during_execution(self):
        _ps1_ready(self.base, self.clk, self.proto)
        inner = quote_fetcher(self.clk)

        def fetch_then_operator_terminates(url, clock=None):
            q = inner(url)
            (self.base / P.TERMINATED).write_text(json.dumps({"by": "operator", "reason": "test"}))
            return q
        res = self._exec(fetch_then_operator_terminates)
        self.assertEqual(res["outcome"], "failed")
        self.assertEqual(U.rows(self.base / P.EXECUTIONS), [])
        st = list(P.exec_states(self.base).values())[0]
        self.assertEqual(st[-1]["state"], "failed")
        self.assertIn("terminated", st[-1]["reason"])
        self.assertTrue(U.rows(self.base / P.QUOTES))                  # the captured quote is kept

    def test_termination_after_scoring_keeps_history_and_the_report(self):
        _ps1_ready(self.base, self.clk, self.proto)
        self._exec()
        a = P.report(self.base, now=DEC + dt.timedelta(hours=1), proto=self.proto)
        snap = {p: p.read_bytes() for p in (self.base / P.ROOT).glob("*.jsonl")}
        P.operator_lifecycle("terminated", "test", base=self.base)
        b = P.report(self.base, now=DEC + dt.timedelta(hours=1), proto=self.proto)
        self.assertEqual(b["lifecycle"]["state"], "terminated")
        self.assertEqual(b["evidence_class"], "retired")
        self.assertEqual(a["arms"], b["arms"])
        for p, raw in snap.items():
            self.assertTrue(p.read_bytes().startswith(raw))            # append-only: nothing removed or rewritten

    def test_restart_after_termination_is_refused(self):
        P.operator_lifecycle("terminated", "test", base=self.base)
        for st in ("active", "approved", "paused"):
            with self.assertRaises(U.LifecycleError):
                P.operator_lifecycle(st, "restart", base=self.base)
        P.operator_lifecycle("archived", "done", base=self.base)
        self.assertEqual(P.lifecycle(self.base)[0], "archived")
        self.assertIsNone(P.decide(self.base, now=DEC + dt.timedelta(minutes=40), clock=self.clk, proto=self.proto, run={}))
        self.assertTrue(any(r["outcome"] == "refused: lifecycle archived" for r in U.rows(self.base / P.RUNS)))

    def test_operator_pause_stops_decisions_and_job_pause_does_not(self):
        _ps1_ready(self.base, self.clk, self.proto)
        self._exec()
        self.assertEqual(P.lifecycle(self.base)[0], "active")
        P.report(self.base, now=DEC + dt.timedelta(days=2, hours=2), proto=self.proto)   # last 6 past deadline, none executed
        state, last = P.lifecycle(self.base)
        self.assertEqual((state, last["by"]), ("paused", "job"))
        self.assertTrue(P.stage_allowed(self.base, "decide")[0])
        P.operator_lifecycle("active", "resume", base=self.base)
        P.operator_lifecycle("paused", "operator hold", base=self.base)
        self.assertFalse(P.stage_allowed(self.base, "decide")[0])
        self.assertTrue(P.stage_allowed(self.base, "report")[0])

    def test_companion_termination_stops_forecasts_and_keeps_earlier_ones_scoreable(self):
        f = CJ.fit_path(self.base, "2026-09")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(synthetic_fit()))
        CJ.forecast(self.base, now=DEC + dt.timedelta(minutes=17), clock=Clock(START_MS - 600_000), run={})
        CJ.operator_lifecycle("terminated", "test", base=self.base)
        self.assertEqual(CJ.lifecycle(self.base)[0], "terminated")
        self.assertEqual(CJ.forecast(self.base, now=DEC + dt.timedelta(hours=4, minutes=17),
                                     clock=Clock(START_MS + 4 * 3600_000 - 600_000), run={}), [])
        self.assertEqual(len(CJ.registered(self.base)), 3)
        with self.assertRaises(U.LifecycleError):
            CJ.operator_lifecycle("active", "restart", base=self.base)


class TestWorkflowStages(unittest.TestCase):
    """Finding 6: every stage is logged; the verdict fails on any failed, missing or artifact-less required stage."""
    ID = {"run_id": "t1", "run_attempt": "1", "event": "test", "triggering_run": None, "code_commit": "x"}
    PY = [sys.executable, "-c"]

    def setUp(self):
        import stream_ops
        self.O = stream_ops
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_(self, stage, code="pass", required=True, artifacts=(), needs=(), tests=False):
        return self.O.run_stage(self.base, stage, required, self.PY + [code], artifacts, needs, tests, ident=self.ID)

    def test_all_required_stages_completed(self):
        self.run_("a")
        self.run_("b", "open('out.json','w').write('{}')", artifacts=["out.json"])
        doc = self.O.verdict(self.base, ["a", "b"], "success", ident=self.ID)
        self.assertEqual(doc["status"], "completed")
        r = doc["stages"]["b"]
        self.assertTrue(r["artifacts"][0]["exists"] and r["artifacts"][0]["sha256"])
        self.assertTrue(r["started_ms"] <= r["completed_ms"])

    def test_execution_failure_fails_the_workflow(self):
        self.run_("a")
        r = self.run_("ps1-execute", "import sys; sys.stderr.write('boom'); sys.exit(3)")
        self.assertEqual((r["status"], r["exit_code"]), ("failed", 3))
        self.assertIn("boom", r["error"])
        self.assertEqual(self.O.verdict(self.base, ["a", "ps1-execute"], "success", ident=self.ID)["status"], "failed")

    def test_report_failure_fails_the_workflow(self):
        self.run_("ps1-report", "raise RuntimeError('report broke')", artifacts=["r.json"])
        doc = self.O.verdict(self.base, ["ps1-report"], "success", ident=self.ID)
        self.assertEqual(doc["status"], "failed")

    def test_missing_or_stale_artifact_fails_the_stage(self):
        r = self.run_("ps1-report", "pass", artifacts=["reports/paper_ps1.json"])
        self.assertEqual(r["status"], "failed")
        self.assertIn("missing artifact", r["error"])
        old = self.base / "old.json"
        old.write_text("{}")
        os.utime(old, (1, 1))
        self.assertEqual(self.run_("again", "pass", artifacts=["old.json"])["status"], "failed")

    def test_partial_completion_fails_and_dependents_are_skipped(self):
        self.run_("publish", "raise SystemExit(1)")
        r = self.run_("ps1-confirm", needs=["publish"])
        self.assertEqual(r["status"], "skipped")
        doc = self.O.verdict(self.base, ["publish", "ps1-confirm", "ps1-execute"], "success", ident=self.ID)
        self.assertEqual(doc["status"], "failed")
        self.assertTrue(any("ps1-execute: not run" in p for p in doc["required_problems"]))

    def test_optional_stage_is_labelled_not_counted(self):
        self.run_("a")
        self.run_("feasibility-report", "raise SystemExit(2)", required=False)
        doc = self.O.verdict(self.base, ["a", "feasibility-report"], "success", ident=self.ID)
        self.assertEqual(doc["status"], "completed with optional stages not completed")
        self.assertEqual(len(doc["optional_not_completed"]), 1)

    def test_persist_failure_fails_the_workflow(self):
        self.run_("a")
        self.assertEqual(self.O.verdict(self.base, ["a"], "failure", ident=self.ID)["status"], "failed")

    def test_test_counts_are_reported_separately(self):
        c = self.O.parse_counts("....s.\n----\nRan 42 tests in 4.2s\n\nOK (skipped=3)\n")
        self.assertEqual((c["ran"], c["executed"], c["passed"], c["failed"], c["skipped"], c["unavailable"]), (42, 39, 39, 0, 3, None))
        c = self.O.parse_counts("Ran 10 tests in 1s\n\nFAILED (failures=1, errors=2, skipped=1)\n")
        self.assertEqual((c["executed"], c["passed"], c["failed"], c["errors"], c["skipped"]), (9, 6, 1, 2, 1))
        self.assertIsNotNone(self.O.parse_counts("ImportError: no module")["unavailable"])
        r = self.run_("t", "import sys; sys.stderr.write('Ran 2 tests in 0.1s\\n\\nOK (skipped=1)\\n')", tests=True)
        self.assertEqual((r["tests"]["executed"], r["tests"]["skipped"]), (1, 1))


class TestRetiredProtocol(unittest.TestCase):
    def test_v2_never_continues_a_ledger_launched_under_v1(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / P.ROOT).mkdir(parents=True)
            (base / P.LAUNCH).write_text(json.dumps({"protocol_sha256": P.PROTOCOL_V1_RETIRED[1]}))
            for call in (lambda: P.report(base, proto=proto_for_tests()),
                         lambda: P.decide(base, now=DEC, proto=proto_for_tests(), run={}),
                         lambda: P.execute(base, proto=proto_for_tests(), run={})):
                with self.assertRaises(P.Refused):
                    call()


    def test_v1_is_preserved_byte_identical_and_v2_names_it(self):
        path, sha = P.PROTOCOL_V1_RETIRED
        self.assertEqual(U.file_sha(BASE / path), sha)
        v2 = json.loads(P.PROTOCOL.read_text())
        self.assertEqual((v2["version"], v2["supersedes"]["sha256"]), (2, sha))
        v1 = json.loads((BASE / path).read_text())
        for k in ("question", "instrument", "policy", "calibration", "capital", "costs", "missing_data", "evidence", "start"):
            self.assertEqual(v1[k], v2[k], k)


if __name__ == "__main__":
    unittest.main()
