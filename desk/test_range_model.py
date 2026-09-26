#!/usr/bin/env python3
"""Tests for range_model (package 11.1). Offline, stdlib unittest, seeded synthetic data.

The machinery is proven on data with a known answer before any real result is trusted:
volatility that clusters (B1 must beat B0) and volatility that does not (B1 must not find structure).
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_range_model.py
"""
import datetime as dt
import json
import math
import random
import unittest

import range_model as R

UTC = dt.timezone.utc


def synth_bars(n, seed, persistence, start=dt.datetime(2021, 1, 4, tzinfo=UTC), base_sigma=0.008, steps=24):
    """4H bars from a Brownian path whose per-bar log sigma follows AR(1) with the given persistence
    (0 = i.i.d. volatility)."""
    rnd = random.Random(seed)
    price, ls = 30000.0, math.log(base_sigma)
    mu, bars = math.log(base_sigma), []
    for i in range(n):
        ls = mu + persistence * (ls - mu) + (0.25 * math.sqrt(1 - persistence ** 2) if persistence else 0.0) * rnd.gauss(0, 1)
        s = math.exp(ls) if persistence else base_sigma
        x = hi = lo = 0.0
        for _ in range(steps):
            x += rnd.gauss(0, s / math.sqrt(steps))
            hi, lo = max(hi, x), min(lo, x)
        o = price
        t0 = start + dt.timedelta(hours=4 * i)
        bars.append({"open_utc": R._iso(t0), "close_utc": R._iso(t0 + dt.timedelta(hours=4)), "open": o,
                     "high": o * math.exp(hi), "low": o * math.exp(lo), "close": o * math.exp(x)})
        price = o * math.exp(x)
    return bars


def flat_bars(n, start=dt.datetime(2026, 9, 18, 0, tzinfo=UTC), rng=0.01):
    out = []
    for i in range(n):
        t0 = start + dt.timedelta(hours=4 * i)
        out.append({"open_utc": R._iso(t0), "close_utc": R._iso(t0 + dt.timedelta(hours=4)), "open": 100.0,
                    "high": 100.0 * math.exp(rng / 2), "low": 100.0 * math.exp(-rng / 2), "close": 100.0 + (i % 2) * 0.01})
    return out


class TestOLS(unittest.TestCase):
    def test_exact_one_regressor(self):
        X = [[1.0, x] for x in range(10)]
        y = [2 + 3 * x for x in range(10)]
        b = R.ols(X, y)
        self.assertAlmostEqual(b[0], 2.0, places=9); self.assertAlmostEqual(b[1], 3.0, places=9)

    def test_exact_two_regressors(self):
        pts = [(a, b) for a in range(5) for b in range(4)]
        b = R.ols([[1.0, a, c] for a, c in pts], [1 + 2 * a - 0.5 * c for a, c in pts])
        for got, want in zip(b, (1.0, 2.0, -0.5)):
            self.assertAlmostEqual(got, want, places=9)

    def test_singular_design_raises(self):
        with self.assertRaises(ValueError):
            R.ols([[1.0, 2.0], [1.0, 2.0], [1.0, 2.0]], [1, 2, 3])


class TestSyntheticKnownAnswers(unittest.TestCase):
    """B1 must beat B0 when volatility clusters, and must find no structure when it does not."""

    def run_case(self, persistence, seed):
        bars = synth_bars(3000, seed, persistence)
        panel = R.build_panel(bars, [], None, horizons=("4h",))["4h"]
        ev0 = panel[1800]["decision_utc"]; ev1 = panel[-2]["decision_utc"]
        b0 = R.walk_forward(panel, "B0", ev0, ev1)
        b1 = R.walk_forward(panel, "B1", ev0, ev1)
        cmp = R.compare(b1, b0, "4h")
        f = R.fit(panel, "B1", R._t(ev1))
        har = sum(f["beta"][1:5])
        return cmp, har

    def test_clustering_b1_beats_b0(self):
        cmp, har = self.run_case(0.97, 11)
        self.assertGreater(cmp["skill"], 0.03)
        self.assertLess(cmp["dm_p"], 0.05)
        self.assertGreater(har, 0.5)

    def test_iid_no_structure(self):
        cmp, har = self.run_case(0.0, 12)
        self.assertLess(abs(cmp["skill"]), 0.03)
        self.assertLess(abs(har), 0.5)


class TestNoLookAhead(unittest.TestCase):
    def test_features_ignore_future_bars(self):
        bars = synth_bars(400, 5, 0.9)
        i = 300
        a = R.build_panel(bars[: i + 1] + bars[i + 1:], [], None)
        spiked = [dict(b) for b in bars]
        for b in spiked[i + 1:]:
            b["high"] *= 1.5; b["low"] *= 0.6
        s = R.build_panel(spiked, [], None)
        for h in ("4h", "24h", "72h"):
            ra = [r for r in a[h] if r["decision_utc"] == bars[i]["close_utc"]][0]
            rs = [r for r in s[h] if r["decision_utc"] == bars[i]["close_utc"]][0]
            fa = {k: v for k, v in ra.items() if k not in ("y", "target_close_utc")}
            fs = {k: v for k, v in rs.items() if k not in ("y", "target_close_utc")}
            self.assertEqual(fa, fs, h)
            self.assertNotEqual(ra["y"], rs["y"])

    def test_dvol_not_used_before_its_close(self):
        t = dt.datetime(2026, 9, 20, 12, tzinfo=UTC)
        series = R.dvol_series([{"available_at_utc": "2026-09-20T11:00:00Z", "dvol": 40.0},
                                {"available_at_utc": "2026-09-20T12:01:00Z", "dvol": 90.0}])
        self.assertEqual(R.dvol_as_of(series, t), 40.0)
        self.assertIsNone(R.dvol_as_of(series, t - dt.timedelta(hours=2)))
        self.assertIsNone(R.dvol_as_of(series, t + dt.timedelta(hours=8)))    # stale beyond 6h

    def test_training_excludes_unclosed_targets(self):
        bars = synth_bars(800, 7, 0.9)
        rows = R.build_panel(bars, [], None, horizons=("72h",))["72h"]
        cut = R._t(rows[500]["decision_utc"])
        f = R.fit(rows, "B1", cut)
        used = [r for r in rows if r["y"] is not None and r["target_close_utc"] <= R._iso(cut)]
        self.assertEqual(f["n"], len(used))
        self.assertTrue(all(R._t(r["target_close_utc"]) <= cut for r in used))


class TestCalendarAndSession(unittest.TestCase):
    def setUp(self):
        # Fri Sep 18 2026 00:00Z start; bar 179 closes Fri Sep 18 + 30 days ... use explicit index lookups
        self.bars = flat_bars(260, start=dt.datetime(2026, 8, 1, tzinfo=UTC))

    def row(self, h, close_utc, releases):
        p = R.build_panel(self.bars, releases, None, horizons=(h,))[h]
        return [r for r in p if r["decision_utc"] == close_utc][0]

    def test_release_inside_horizon(self):
        rel = [dt.datetime(2026, 9, 4, 12, 30, tzinfo=UTC), dt.datetime(2026, 9, 4, 16, 0, tzinfo=UTC)]
        r4 = self.row("4h", "2026-09-04T12:00:00Z", rel)
        r24 = self.row("24h", "2026-09-04T12:00:00Z", rel)
        self.assertEqual(r4["releases"], 1)          # 12:30 inside [12:00, 16:00); 16:00 excluded
        self.assertEqual(r24["releases"], 2)
        self.assertTrue(r4["release_within_24h"])

    def test_weekend_shares(self):
        r = self.row("24h", "2026-09-04T20:00:00Z", [])   # Friday 20:00Z close
        self.assertAlmostEqual(r["sat_share"], 5 / 6)
        self.assertAlmostEqual(r["sun_share"], 0.0)

    def test_b0_on_constant_ranges(self):
        r = self.row("24h", "2026-09-04T20:00:00Z", [])
        self.assertAlmostEqual(r["b0"], math.log(0.01), places=3)   # b0 is mean ln(lr); lr = 0.01 here


class TestScoring(unittest.TestCase):
    def test_dm_identical(self):
        md, z, p = R.diebold_mariano([1, 2, 3, 4], [1, 2, 3, 4], 2)
        self.assertEqual((md, p), (0, 1.0))

    def test_newey_west_lag0_is_variance(self):
        d = [1.0, 3.0, 2.0, 6.0]
        m = sum(d) / 4
        self.assertAlmostEqual(R.newey_west_var(d, 0), sum((x - m) ** 2 for x in d) / 4)

    def test_coherence(self):
        self.assertEqual(R.coherent(-3.0, -3.5, -3.2), (-3.0, -3.0, -3.0, 2))
        self.assertEqual(R.coherent(-4.0, -3.0, -2.0)[3], 0)

    def test_stage1_composite_uses_implied_near_release(self):
        row = {"release_within_24h": True, "sd_implied": 0.007, "sd_park_6": 0.002, "sd_c2c_42": 0.009}
        self.assertEqual(R.stage1_sigma(row, "m10_composite"), 0.007)
        row["release_within_24h"] = False
        self.assertEqual(R.stage1_sigma(row, "m10_composite"), 0.002)     # compression: 0.009 > 2 x 0.002


class TestReproducibility(unittest.TestCase):
    def test_same_inputs_same_bytes(self):
        bars = synth_bars(900, 3, 0.95)
        out = []
        for _ in range(2):
            p = R.build_panel(bars, [], None, horizons=("4h",))["4h"]
            fc = R.walk_forward(p, "B1", p[500]["decision_utc"], p[-2]["decision_utc"])
            out.append(json.dumps([fc, R.block_bootstrap_skill([abs(r["y"] - r["f"]) for r in fc], [1.0] * len(fc), reps=50)],
                                  sort_keys=True))
        self.assertEqual(out[0], out[1])

    def test_forecast_document(self):
        bars = synth_bars(1200, 9, 0.95, start=dt.datetime(2026, 3, 1, tzinfo=UTC))
        doc = R.forecast_now(bars, [], None, {"4h": "B1", "24h": "B1", "72h": "B0"}, "test")
        self.assertTrue(doc["id"].startswith("RANGE-LR-"))
        self.assertEqual(len(doc["content_sha256"]), 64)
        h = doc["horizons"]
        self.assertLessEqual(h["4h"]["point_coherent"], h["24h"]["point_coherent"])
        self.assertLessEqual(h["24h"]["point_coherent"], h["72h"]["point_coherent"])
        self.assertGreater(h["4h"]["range_points"], 0)


class TestVersion(unittest.TestCase):
    def test_version(self):
        self.assertEqual(R.VERSION, "range-11.1.0")


if __name__ == "__main__":
    unittest.main(verbosity=1)
