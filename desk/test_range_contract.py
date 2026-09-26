#!/usr/bin/env python3
"""Parity tests for range_contract (crypto-desk 12.0): evaluation, registration and scoring produce the same
windows, features, points, quantiles and losses. Offline, seeded synthetic data; the repository's own
schema.py and scoring.py are exercised where the scoring path is concerned.
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_range_contract.py
"""
import datetime as dt
import math
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
sys.path[:0] = [str(DESK), str(DESK.parent)]

import range_contract as C          # noqa: E402
import range_model as R             # noqa: E402
from test_range_model import synth_bars   # noqa: E402

try:                                # the registration and scoring paths live in the repository only
    import range_job as J           # noqa: E402
    import scoring                  # noqa: E402,F401
    REPO = True
except ImportError:                 # skill folder: the contract's own tests still run
    REPO = False

UTC = dt.timezone.utc
TOL = C.PARITY_TOL


def dvol_rows(bars, level=40.0):
    t0, t1 = R._t(bars[0]["open_utc"]), R._t(bars[-1]["close_utc"])
    out, t = [], t0
    while t < t1:
        out.append({"open_utc": R._iso(t), "available_at_utc": R._iso(t + dt.timedelta(hours=1)),
                    "dvol": level + 5 * math.sin(t.timestamp() / 86400)})
        t += dt.timedelta(hours=1)
    return out


def minute_bars(bar4h, seed_shift=0):
    """240 one-minute bars inside a 4H bar whose max high / min low equal the 4H bar's (scoring input shape)."""
    t0 = R._t(bar4h["open_utc"])
    mid = (bar4h["high"] * bar4h["low"]) ** 0.5
    out = []
    for k in range(240):
        hi = bar4h["high"] if k == 37 + seed_shift else mid * 1.0001
        lo = bar4h["low"] if k == 181 else mid * 0.9999
        out.append((C.ms(t0 + dt.timedelta(minutes=k)), hi, lo, mid))
    return out


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        n = 2600
        start = dt.datetime(2026, 9, 26, tzinfo=UTC) - dt.timedelta(hours=4 * n)
        cls.bars = synth_bars(n, 5, 0.95, start=start)
        cls.dvol = dvol_rows(cls.bars)
        # a synthetic calendar with releases scattered through the sample, one near a window boundary
        t0 = R._t(cls.bars[300]["open_utc"])
        cls.releases = sorted(t0 + dt.timedelta(hours=37 * k + 13, minutes=30) for k in range(250))
        cls.tmp = Path(tempfile.mkdtemp())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)


class TestCalendarParity(Fixture):
    def test_aligned_window_terms_equal_range_model(self):
        series = R.dvol_series(self.dvol)
        checked = 0
        for i in range(400, 2400, 7):
            hist = self.bars[i - 179: i + 1]
            d = R._t(hist[-1]["close_utc"])
            for h in C.HOURS:
                f = R.features_at(hist, self.releases, series, h)
                s, e = C.window("RC1", d, h)
                t = C.calendar_terms(s, e, self.releases)
                self.assertAlmostEqual(t["sat_share"], f["sat_share"], places=12)
                self.assertAlmostEqual(t["sun_share"], f["sun_share"], places=12)
                self.assertEqual(t["releases"], f["releases"])
                checked += 1
        self.assertGreater(checked, 800)

    def test_release_near_boundary_counts_for_the_window_actually_scored(self):
        d = R._t(self.bars[1500]["close_utc"])
        rel = sorted(self.releases + [d + dt.timedelta(hours=4, minutes=3)])
        s1, e1 = C.window("RC1", d, "4h")
        s2, e2 = C.window("RC1D", d, "4h", prepared=d + dt.timedelta(minutes=6))
        self.assertEqual(s2, d + dt.timedelta(minutes=15))           # 00:06 + 5 min -> next 5-minute boundary
        self.assertEqual(C.calendar_terms(s1, e1, rel)["releases"] - C.calendar_terms(s1, e1, self.releases)["releases"], 0)
        self.assertEqual(C.calendar_terms(s2, e2, rel)["releases"] - C.calendar_terms(s2, e2, self.releases)["releases"], 1)
        row = C.decision_row(self.bars[:1501], rel, self.dvol, "4h", s2, e2)
        self.assertEqual(row["releases"], C.calendar_terms(s2, e2, rel)["releases"])   # feature = event_regime window

    def test_weekend_share_is_time_weighted_for_shifted_windows(self):
        sat = dt.datetime(2026, 9, 19, 20, 10, tzinfo=UTC)          # Saturday 20:10 -> Sunday 00:10
        t = C.calendar_terms(sat, sat + dt.timedelta(hours=4), [])
        self.assertAlmostEqual(t["sat_share"], 230 / 240); self.assertAlmostEqual(t["sun_share"], 10 / 240)


@unittest.skipUnless(REPO, "registration/scoring paths need the repository (desk/ with root modules)")
class TestPathParity(Fixture):
    """The evaluation path (C.walk_forward), the registration path (refit file -> C.values) and the scoring
    path (scoring.score on 1m bars) agree on one decision per horizon."""

    def test_eval_registration_scoring_agree(self):
        import scoring
        m0 = dt.datetime(2026, 9, 1, tzinfo=UTC)
        hist = [b for b in self.bars if R._t(b["open_utc"]) < m0]
        base = self.tmp / "parity"
        (base / "desk/fits").mkdir(parents=True)
        orig_cal = J.calendar
        J.calendar = lambda: (self.releases, "synthetic")
        try:
            doc = J.refit(m0 + dt.timedelta(days=2), base=base, history=(hist, self.dvol))
        except Exception:
            J.calendar = orig_cal
            raise
        import json
        fit = json.loads(Path(doc).read_text())
        J.calendar = orig_cal
        panel = R.build_panel(self.bars, self.releases, self.dvol)
        i = next(k for k, b in enumerate(self.bars) if b["close_utc"] == "2026-09-10T08:00:00Z")
        d = R._t(self.bars[i]["close_utc"])
        for h, n in (("4h", 1), ("24h", 6), ("72h", 18)):
            ev = C.walk_forward(panel[h], "B2", "2026-09-01T00:00:00Z", "2026-09-26T00:00:00Z")
            e_row = next(r for r in ev if r["decision_utc"] == R._iso(d))
            b0 = C.walk_forward(panel[h], "B0", "2026-09-01T00:00:00Z", "2026-09-26T00:00:00Z")
            b0_row = next(r for r in b0 if r["decision_utc"] == R._iso(d))
            s, e = C.window("RC1", d, h)
            row = C.decision_row(self.bars[: i + 1], self.releases, self.dvol, h, s, e)
            v = C.values(fit["fits"][h], fit["b0_resid_q"][h], row)
            self.assertLess(abs(v["B2"]["point"] - e_row["point"]), TOL)
            for a, b in zip(v["B2"]["q"], e_row["q"]):
                self.assertLess(abs(a - b), TOL)
            self.assertLess(abs(v["B0"]["point"] - b0_row["point"]), TOL)
            for a, b in zip(v["B0"]["q"], b0_row["q"]):
                self.assertLess(abs(a - b), TOL)
            # scoring path: a registry document with this event, scored on 1m bars of the same window
            target = self.bars[i + 1: i + 1 + n]
            minutes = [m for b in target for m in minute_bars(b)]
            fc = {"id": f"parity-{h}", "instrument": "BTCUSDT perp, Binance last price", "reference_price": 1.0,
                  "start_utc": R._iso(s), "horizon_utc": R._iso(e),
                  "events": [C.event("B2 range model", v["B2"]), C.event("B0 persistence baseline", v["B0"])]}
            got, _ = scoring.score(fc, minutes, lambda name: [])
            eval_loss = C.loss_rows([e_row])[0]
            self.assertLess(abs(got[0]["realized_ln_range"] - eval_loss["realized_ln_range"]), TOL)
            for k in ("abs_error_log_lr", "qlike", "abs_error_lr"):
                self.assertLess(abs(got[0][k] - eval_loss[k]), TOL, k)
            for k in ("q10", "q50", "q90"):
                self.assertLess(abs(got[0]["pinball"][k] - eval_loss["pinball"][k]), TOL)
            self.assertEqual(got[0]["covered_80"], eval_loss["covered_80"])
            self.assertEqual(got[0]["loss_basis"], "point (desk/range_contract.py)")


class TestPoint(unittest.TestCase):
    def test_point_is_not_the_residual_median(self):
        fit_h = {"model": "B2", "beta": [0.0] * 9, "resid_q": [-0.5, -0.04, 0.6]}
        row = {t: 1.0 for t in R.MODEL_TERMS["B2"]}
        row["b0"] = -4.0
        v = C.values(fit_h, [-0.4, -0.03, 0.5], row)
        self.assertEqual(v["B2"]["point"], 0.0)
        self.assertAlmostEqual(v["B2"]["q"][1], -0.04)
        e = C.event("B2", v["B2"])
        self.assertAlmostEqual(e["q50"] / e["point"], math.exp(-0.04), places=10)


class TestCoherence(unittest.TestCase):
    def test_violation_reported_not_applied(self):
        points = {"4h": -4.0, "24h": -4.2, "72h": -3.0}
        self.assertEqual(C.coherence_violations(points), ["24h<4h"])
        raised = R.coherent(points["4h"], points["24h"], points["72h"])
        self.assertEqual(raised[1], -4.0)                           # range_model.forecast_now would raise it
        self.assertEqual(points["24h"], -4.2)                       # the contract leaves the point as fitted

    def test_live_and_eval_agree_when_coherence_would_bind(self):
        row = {t: 1.0 for t in R.MODEL_TERMS["B2"]}
        row["b0"] = -4.0
        fits = {"4h": {"model": "B2", "beta": [-3.0] + [0.0] * 8, "resid_q": [-0.5, 0, 0.5]},
                "24h": {"model": "B2", "beta": [-3.5] + [0.0] * 8, "resid_q": [-0.5, 0, 0.5]}}
        live = {h: C.values(f, [-0.5, 0, 0.5], row)["B2"]["point"] for h, f in fits.items()}
        ev = {h: R.predict({"model": "B2", "beta": f["beta"]}, row) for h, f in fits.items()}   # walk_forward's call
        self.assertEqual(live, ev)
        self.assertEqual(C.coherence_violations(live), ["24h<4h"])


class TestSplits(unittest.TestCase):
    def test_every_horizon_matures_inside_its_period(self):
        start = dt.datetime(2024, 9, 1, tzinfo=UTC)
        bars = synth_bars(3200, 9, 0.9, start=start)
        panel = R.build_panel(bars, [], None)
        for h, rows in panel.items():
            val = [r for r in rows if C.in_period(r, *C.PERIODS["validation"])]
            self.assertTrue(val)
            self.assertTrue(all(r["target_close_utc"] <= C.PERIODS["validation"][1] for r in val))
            # the decision-only rule O21 used would admit rows maturing inside the holdout at 24h and 72h
            old = [r for r in rows if "2024-09-23T00:00:00Z" <= r["decision_utc"] <= "2025-09-22T23:59:59Z"
                   and r["y"] is not None]
            leak = [r for r in old if r["target_close_utc"] > C.PERIODS["validation"][1]]
            self.assertEqual(len(leak), {"4h": 0, "24h": 5, "72h": 17}[h])
            self.assertEqual(len(old) - len(val), len(leak))

    def test_holm(self):
        adj = C.holm({"a": 0.01, "b": 0.04, "c": 0.03})
        self.assertAlmostEqual(adj["a"], 0.03); self.assertAlmostEqual(adj["c"], 0.06); self.assertAlmostEqual(adj["b"], 0.06)


class TestContractIdentity(unittest.TestCase):
    def test_ids_are_distinct_and_stable(self):
        a, b = C.contract_id("RC1"), C.contract_id("RC1D")
        self.assertNotEqual(a, b)
        self.assertEqual(a, C.contract_id("RC1"))
        self.assertTrue(b.startswith("RC1D/" + C.CONTRACT_VERSION + "/"))
        # 12.1: the contract id is semantic and unchanged since 12.0, so every registered record stays readable
        self.assertEqual((a, b), ("RC1/contract-12.0.0/e8f291740f27", "RC1D/contract-12.0.0/175a4dd4c6c0"))
        with self.assertRaises(ValueError):
            C.spec("RC2")


if __name__ == "__main__":
    unittest.main(verbosity=1)
