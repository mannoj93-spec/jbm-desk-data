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
        q = dict(book(), t_sent_ms=1000, t_received_ms=1300, retrieval="live request (not a retrospective quote)")
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
        rows = [{"equity_pre": 100.0, "interval_return": None, "notional": 50.0, "w_after": 0.5, "cost_vs_mid": 0.1},
                {"equity_pre": 110.0, "interval_return": 0.10, "notional": 0.0, "w_after": 0.5, "cost_vs_mid": 0.0},
                {"equity_pre": 99.0, "interval_return": -0.10, "notional": 10.0, "w_after": 0.4, "cost_vs_mid": 0.02}]
        s = P.arm_stats(rows)
        self.assertAlmostEqual(s["net_return"], -0.01)
        self.assertAlmostEqual(s["max_drawdown_marks"], 99 / 110 - 1)
        self.assertAlmostEqual(s["exposure_mean"], 0.5)
        self.assertAlmostEqual(s["sharpe_ann"], 0.0)
        self.assertAlmostEqual(s["turnover_ann"], 60 / (309 / 3) / (2 / 2190))

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


if __name__ == "__main__":
    unittest.main()
