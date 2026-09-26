#!/usr/bin/env python3
"""Numerical fixtures for jbm_measure (package 11.0). Offline, stdlib unittest.

Each expected value is either closed-form, recomputed independently here, or a dated desk figure
whose inputs are stated (cases.md / baserates.md cite these tests by name). These fixtures are the
single source for the numbers; evals.md lists them by test name only.
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_jbm_measure.py
"""
import datetime as dt
import math
import random
import unittest

import jbm_measure as M

UTC = dt.timezone.utc


def T(s):
    return dt.datetime.fromisoformat(s).replace(tzinfo=UTC)


class TestUnitsAndTags(unittest.TestCase):
    def test_implied_sigma_matches_sep25_state(self):
        # cases.md §S: implied 623.2 points at DVOL 34.74, reference 83,943
        s = M.implied_sigma_4h(34.74)
        self.assertEqual((s.kind, s.unit), ("sigma", "log"))
        self.assertAlmostEqual(s.value, 0.3474 / math.sqrt(2190), places=12)
        # the recorded 623.2 reproduces to 0.05 pts; the thread's exact reference price was not recorded
        self.assertAlmostEqual(M.to_points(s, 83943).value, 623.2, delta=0.1)

    def test_range_is_refused_where_sigma_required(self):
        rng = M.range_realized([84000, 84500], [83000, 83600])
        sig = M.Measure(0.008, "sigma", "log", "sd_c2c_4h_7d")
        with self.assertRaises(TypeError):
            M.operative_sigma(rng, sig)
        with self.assertRaises(TypeError):
            M.scale_factor_k(rng, sig)
        with self.assertRaises(TypeError):
            M.sigma_distance(84000, 82000, rng)

    def test_points_are_refused_where_log_required(self):
        pts = M.to_points(M.Measure(0.008, "sigma", "log", "c2c"), 84000)
        with self.assertRaises(TypeError):
            M.operative_sigma(pts, M.Measure(0.007, "sigma", "log", "p6"))

    def test_bare_float_is_refused(self):
        with self.assertRaises(TypeError):
            M.scale_factor_k(0.008, M.Measure(0.007, "sigma", "log", "full"))

    def test_brownian_range_constant(self):
        self.assertAlmostEqual(M.BROWNIAN_RANGE_OVER_SIGMA, 1.5958, places=4)

    def test_range_reported_in_expected_ranges(self):
        sig = M.Measure(0.01, "sigma", "log", "s")
        rng = M.Measure(0.015958, "range", "log", "r")
        self.assertAlmostEqual(M.range_in_expected_ranges(rng, sig), 1.0, places=4)


class TestEstimators(unittest.TestCase):
    def test_c2c_alternating(self):
        c = [100.0]
        for i in range(42):
            c.append(c[-1] * math.exp(0.01 if i % 2 == 0 else -0.01))
        s = M.sd_c2c(c)
        self.assertAlmostEqual(s.value, math.sqrt(42 * 1e-4 / 41), places=9)

    def test_c2c_floor(self):
        with self.assertRaises(ValueError):
            M.sd_c2c([100.0] * 10)

    def test_parkinson_constant_range(self):
        h = [100 * math.exp(0.02)] * 6
        l = [100.0] * 6
        self.assertAlmostEqual(M.sd_parkinson(h, l, "p6").value, 0.02 / math.sqrt(4 * math.log(2)), places=12)

    def test_simulated_bars_parkinson_recovers_sigma_range_does_not(self):
        rnd = random.Random(20260925)
        sigma, steps, bars = 0.008, 240, 3000
        highs, lows = [], []
        for _ in range(bars):
            x = hi = lo = 0.0
            for _ in range(steps):
                x += rnd.gauss(0, sigma / math.sqrt(steps))
                hi, lo = max(hi, x), min(lo, x)
            highs.append(100 * math.exp(hi)); lows.append(100 * math.exp(lo))
        park = M.sd_parkinson(highs, lows, "p").value
        self.assertAlmostEqual(park / sigma, 1.0, delta=0.06)    # discretisation biases it slightly low
        rng = M.range_realized(highs, lows, "r").value
        self.assertGreater(rng / sigma, 1.35)                      # a range in the sigma slot inflates k

    def test_log_range(self):
        self.assertAlmostEqual(M.log_range(82000, 80000), 0.024693, places=6)


class TestPrecedence(unittest.TestCase):
    c2c = M.Measure(0.010, "sigma", "log", "c2c")
    p6 = M.Measure(0.004, "sigma", "log", "p6")
    iv = M.Measure(0.0074, "sigma", "log", "implied")

    def test_o21_default_is_parkinson_6(self):
        s, why = M.operative_sigma(self.c2c, M.Measure(0.009, "sigma", "log", "p6"))
        self.assertEqual(s.name, "p6"); self.assertIn("O21", why)

    def test_house_rule_reproducible(self):
        s, why = M.operative_sigma(self.c2c, self.p6, rule="house-10.2")
        self.assertEqual(s.name, "p6"); self.assertIn("compression", why)
        s, _ = M.operative_sigma(self.c2c, M.Measure(0.009, "sigma", "log", "p6"), rule="house-10.2")
        self.assertEqual(s.name, "c2c")
        with self.assertRaises(ValueError):
            M.operative_sigma(self.c2c, self.p6, rule="other")

    def test_print_requires_implied(self):
        self.assertEqual(M.operative_sigma(self.c2c, self.p6, self.iv, True)[0].name, "implied")
        with self.assertRaises(ValueError):
            M.operative_sigma(self.c2c, self.p6, None, True)

    def test_k(self):
        self.assertAlmostEqual(M.scale_factor_k(self.c2c, M.Measure(0.008, "sigma", "log", "full")), 1.25)


class TestCalendar(unittest.TestCase):
    def test_roll_off_sep25(self):
        self.assertEqual(M.roll_off_exit(T("2026-09-18T12:00:00")), T("2026-09-25T16:00:00"))

    def test_countdown_t10(self):
        self.assertEqual(M.countdown(T("2026-09-16T15:43:00"), T("2026-09-16T18:00:00")), (2, 17))


class TestUncertainty(unittest.TestCase):
    def test_zero_of_28(self):
        self.assertAlmostEqual(M.upper_limit_zero(28), 0.1015, delta=0.0001)   # '~10.1%'
        self.assertAlmostEqual(M.clopper_pearson(0, 28)[1], 0.1234, places=4)

    def test_three_of_three(self):
        lo, hi = M.clopper_pearson(3, 3)
        self.assertAlmostEqual(lo, 0.2924, places=4); self.assertEqual(hi, 1.0)

    def test_m14_wilson(self):
        lo, hi = M.wilson(40, 52)
        self.assertAlmostEqual(lo, 0.64, delta=0.01); self.assertAlmostEqual(hi, 0.86, delta=0.01)

    def test_five_of_five_one_sided(self):
        self.assertAlmostEqual(0.05 ** (1 / 5), 0.5493, places=4)

    def test_four_of_four_at_p81(self):
        self.assertAlmostEqual(0.19 ** 4, 0.0013, places=4)


class TestPositioning(unittest.TestCase):
    def test_share(self):
        self.assertAlmostEqual(M.share_from_ratio(1.5), 0.6)
        self.assertEqual(M.share_from_ratio(0.0), 0.0)            # a legitimate zero

    def test_share_domain(self):
        for bad in (-2.0, -1.0, float("nan"), float("inf"), "1.5", True):
            with self.assertRaises(ValueError):
                M.share_from_ratio(bad)

    def test_synthetic_index_scales_with_oi(self):
        self.assertAlmostEqual(M.synthetic_index(100, 0.6, 0.7), -10.0)
        self.assertAlmostEqual(M.synthetic_index(120, 0.6, 0.7), -12.0)

    def test_size_concentration(self):
        self.assertAlmostEqual(M.size_concentration(0.70, 0.60), 1.556, places=3)
        self.assertAlmostEqual(0.70 / 0.60, 1.167, places=3)       # retired statistic, a different quantity


class TestFunding(unittest.TestCase):
    def test_hyperliquid(self):
        f8, h = M.hyperliquid_rates(0.0)
        self.assertAlmostEqual(f8, 0.0001); self.assertAlmostEqual(h, 0.0000125)
        f8, h = M.hyperliquid_rates(0.01)
        self.assertAlmostEqual(f8, 0.0095); self.assertAlmostEqual(h, 0.0011875)
        f8, h = M.hyperliquid_rates(-0.0002)
        self.assertAlmostEqual(f8, 0.0001)

    def test_dead_zone_not_invertible(self):
        self.assertIsNone(M.premium_from_rate(M.funding_binance_family(-0.0002)))
        self.assertAlmostEqual(M.premium_from_rate(M.funding_binance_family(0.0012)), 0.0012)


class TestPositionArithmetic(unittest.TestCase):
    def test_add_valuation_toy(self):
        r = M.add_valuation(10000, 2000, 1000, [-2000, -2000, 1000, -500], [-1500, -3000, 1000, -500])
        self.assertAlmostEqual(r["E_W_hold"], 11125); self.assertAlmostEqual(r["E_W_add"], 11000)
        self.assertAlmostEqual(r["marginal"], -125)
        self.assertAlmostEqual(r["minus_C_Pliq_add"], -250); self.assertAlmostEqual(r["loss_avoided"], 125)

    def test_add_valuation_far_barrier(self):
        r = M.add_valuation(10000, 2000, 1000, [300, -300, 100, 0], [300, -300, 100, 0])
        self.assertAlmostEqual(r["marginal"], 0.0)
        self.assertAlmostEqual(M.cash_yield_foregone(1000, 0.04, 168), 0.767, places=3)

    def test_ratio_stress_t12(self):
        self.assertAlmostEqual(M.ratio_stress_pnl(5.305, 2744.44, 84725, 0.03149), -405.6, delta=0.1)

    def test_implied_add_price(self):
        self.assertAlmostEqual(M.implied_add_price(1, 100, 2, 95), 90.0)


class TestVenueHoldout(unittest.TestCase):
    base = {"binance": 40000.0, "hyperliquid": 20000.0, "okx": 15000.0, "kucoin": 8000.0, "gate": 5000.0}
    sig, hrs = 0.0085, 0.25   # 4H log sigma; 15-minute snapshots

    def snap(self, **chg):
        s = dict(self.base)
        for k, v in chg.items():
            s[k] += v
        return s

    def test_gross_net(self):
        g = M.gross_net({"a": -711, "b": 40, "c": -20})
        self.assertAlmostEqual(g["gross_share"]["a"], 711 / 771)
        self.assertEqual(g["largest"], "a"); self.assertAlmostEqual(g["net_ex_largest"], 20)

    def test_swing_without_price_cause_is_held_then_resolved(self):
        h = M.VenueHoldout()
        s0, s1 = self.base, self.snap(kucoin=-711, binance=30, okx=-10)
        r1 = h.step(T("2026-09-23T10:00:00"), s0, s1, 0.0002, self.sig, self.hrs)
        self.assertEqual(r1["flagged"], ["kucoin"]); self.assertAlmostEqual(r1["net_ex_held"], 20)
        self.assertEqual(r1["coverage_books"], "4/5")
        s2 = self.snap(binance=40, okx=-5)                          # kucoin reverts (+711)
        r2 = h.step(T("2026-09-23T10:15:00"), s1, s2, 0.0001, self.sig, self.hrs)
        self.assertIn("kucoin", r2["resolved_noise"]); self.assertAlmostEqual(r2["net_ex_held"], 15)

    def test_price_cause_present_is_not_held(self):
        h = M.VenueHoldout()
        r = h.step(T("2026-09-23T10:00:00"), self.base, self.snap(kucoin=-711), 0.004, self.sig, self.hrs)
        self.assertEqual(r["flagged"], []); self.assertAlmostEqual(r["net_ex_held"], -711)

    def test_persisted_move_restored_once(self):
        h = M.VenueHoldout()
        s1 = self.snap(hyperliquid=-1000)
        h.step(T("2026-09-23T10:00:00"), self.base, s1, 0.0, self.sig, self.hrs)
        s2 = self.snap(hyperliquid=-950)
        r2 = h.step(T("2026-09-23T10:15:00"), s1, s2, 0.0, self.sig, self.hrs)
        self.assertIn("hyperliquid", r2["held"]); self.assertAlmostEqual(r2["net_ex_held"], 0)
        s3 = self.snap(hyperliquid=-980)
        r3 = h.step(T("2026-09-23T10:30:00"), s2, s3, 0.0, self.sig, self.hrs)
        self.assertAlmostEqual(r3["restored"]["hyperliquid"], -980)
        self.assertAlmostEqual(r3["net_ex_held"], -980)             # enters once, cumulative since reference

    def test_twice_in_session_held_until_utc_midnight(self):
        h = M.VenueHoldout()
        s1 = self.snap(kucoin=-700)
        h.step(T("2026-09-23T10:00:00"), self.base, s1, 0.0, self.sig, self.hrs)
        h.step(T("2026-09-23T10:15:00"), s1, self.base, 0.0, self.sig, self.hrs)          # resolves
        r = h.step(T("2026-09-23T11:00:00"), self.base, self.snap(kucoin=+1250), 0.0, self.sig, self.hrs)
        self.assertEqual(r["held"]["kucoin"], "held for session (flagged twice)")
        r = h.step(T("2026-09-23T23:45:00"), self.snap(kucoin=+1250), self.snap(kucoin=+1260, okx=5), 0.0, self.sig, self.hrs)
        self.assertIn("kucoin", r["held"]); self.assertAlmostEqual(r["net_ex_held"], 5)
        r = h.step(T("2026-09-24T00:00:00"), self.snap(kucoin=+1260), self.snap(kucoin=+1270), 0.0, self.sig, self.hrs)
        self.assertTrue(any(x.startswith("kucoin") for x in r["resolved_noise"]))
        self.assertEqual(r["held"], {})

    def test_undetermined_price_leg_is_reported(self):
        r = M.VenueHoldout().step(T("2026-09-23T10:00:00"), self.base, self.snap(kucoin=-711))
        self.assertIn("undetermined", r["price_leg"]); self.assertEqual(r["flagged"], ["kucoin"])

    def test_invalid_book_leaves_intersection(self):
        s1 = self.snap(); s1["gate"] = float("nan")
        r = M.VenueHoldout().step(T("2026-09-23T10:00:00"), self.base, s1, 0.0, self.sig, self.hrs)
        self.assertIn("gate", r["excluded_invalid_or_missing"]); self.assertEqual(r["coverage_books"], "4/4")


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(M.VERSION, "measure-11.1.0")


if __name__ == "__main__":
    unittest.main(verbosity=1)
