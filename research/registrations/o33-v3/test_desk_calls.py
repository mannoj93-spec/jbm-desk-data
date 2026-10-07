"""Tests for desk_calls (calls-1.0.0, O33 v2). Offline, stdlib only; synthetic closes."""
import datetime as dt
import math
import random
import statistics
import unittest

import desk_calls as D

UTC = dt.timezone.utc
T0 = dt.datetime(2026, 10, 7, 12, 0, tzinfo=UTC)


def walk(n, sigma=0.004, seed=1, start=T0 - dt.timedelta(hours=1), drift=0.0):
    """n 1H closes ending at `start`'s close time, log random walk."""
    rnd = random.Random(seed)
    t_end = int(start.timestamp() * 1000)
    c, out = 80_000.0, []
    for i in range(n):
        out.append((t_end - (n - 1 - i) * D.HOUR_MS, c))
        c *= math.exp(drift + rnd.gauss(0, sigma))
    return out


def call(closes, half=0.006, h=4, issue_lag_s=20, **kw):
    t_close = dt.datetime.fromtimestamp(closes[-1][0] / 1000, UTC)
    p = closes[-1][1]
    d = {"call_type": "containment", "instrument": "BTC", "issue_price": p, "lower": p * math.exp(-half),
         "upper": p * math.exp(half), "issue_utc": D.iso(t_close + dt.timedelta(seconds=issue_lag_s)),
         "graded_close_utc": D.iso(t_close + dt.timedelta(hours=h))}
    d.update(kw)
    return d


class RegistrationOrderTests(unittest.TestCase):
    def test_review_counterexample_sent_before_registration_is_late(self):
        # sent 12:00:20, registered 12:00:40, stated start 12:01:00: the 12.4.11 rule (start = issue rounded up,
        # eligible if registered before start) accepted it
        doc = {"version": 1, "start_utc": "2026-10-07T12:01:00Z"}
        st, why = D.registration_status(doc, "2026-10-07T12:00:40Z", True, sent_utc="2026-10-07T12:00:20Z")
        self.assertEqual(st, "late", why)

    def test_quoted_receipt_is_eligible_and_start_is_derived(self):
        st, why = D.registration_status({"version": 1}, "2026-10-07T12:00:40Z", True)
        self.assertEqual(st, "eligible")
        self.assertIn("window starts 2026-10-07T12:01:00Z", why)
        self.assertEqual(D.derived_start("2026-10-07T12:00:00Z"), dt.datetime(2026, 10, 7, 12, 1, tzinfo=UTC))

    def test_unquoted_backdated_and_changed_documents(self):
        self.assertEqual(D.registration_status({"version": 1}, "2026-10-07T12:00:40Z", False)[0], "order-unverified")
        self.assertEqual(D.registration_status({"version": 1, "start_utc": "2026-10-07T12:00:00Z"},
                                               "2026-10-07T12:00:40Z", True)[0], "backdated")
        self.assertEqual(D.registration_status({"version": 2}, "2026-10-07T12:00:40Z", True)[0], "ineligible")
        self.assertEqual(D.registration_status({"version": 1}, None, True)[0], "ineligible")


class IdentityTests(unittest.TestCase):
    def test_two_calls_in_one_minute_do_not_collide(self):
        a = {"call_type": "containment", "lower": 1, "upper": 2}
        b = {"call_type": "containment", "lower": 1, "upper": 3}
        ia = D.call_id("btc", "2026-10-07T12:00:05Z", "containment", D.content_sha256(a))
        ib = D.call_id("btc", "2026-10-07T12:00:05Z", "containment", D.content_sha256(b))
        il = D.call_id("btc", "2026-10-07T12:00:05Z", "lean", D.content_sha256(a))
        self.assertEqual(len({ia, ib, il}), 3)
        self.assertTrue(ia.startswith("DESK-BTC-20261007T120005Z-C-"))
        self.assertEqual(ia, D.call_id("BTC", "2026-10-07T12:00:05Z", "containment", D.content_sha256(dict(a))))

    def test_never_overwrite(self):
        a = {"lower": 1}
        self.assertEqual(D.plan_write(None, a), "write")
        self.assertEqual(D.plan_write(dict(a, registered_utc="x"), a), "duplicate")
        self.assertEqual(D.plan_write({"lower": 2}, a), "conflict")


class UnitTests(unittest.TestCase):
    def c(self, i, receipt, close="2026-10-07T16:00:00Z", issue="2026-10-07T12:00:20Z", **kw):
        d = {"id": i, "instrument": "BTC", "call_type": "containment", "issue_utc": issue, "graded_close_utc": close,
             "receipt_utc": receipt, "status": "eligible"}
        d.update(kw)
        return d

    def test_first_eligible_per_key_counts_and_others_stay_listed(self):
        calls = [self.c("b", "2026-10-07T12:00:50Z"), self.c("a", "2026-10-07T12:00:30Z"),
                 self.c("late", "2026-10-07T12:00:10Z", status="late"),
                 self.c("amend", "2026-10-07T12:02:00Z", amends="a"),
                 self.c("day", "2026-10-07T00:00:40Z", issue="2026-10-06T16:00:20Z"),     # 24 h call, same close
                 self.c("lean", "2026-10-07T12:00:45Z", call_type="lean")]
        counted, rest = D.scoring_units(calls)
        self.assertEqual(sorted(c["id"] for c in counted), ["a", "day", "lean"])
        why = {c["id"]: c["why"] for c in rest}
        self.assertIn("as a: not counted", why["b"])
        self.assertTrue(why["late"].startswith("not eligible"))
        self.assertTrue(why["amend"].startswith("amendment"))


class BaselineTests(unittest.TestCase):
    CL = walk(24 * 760)

    def test_support_restricted_to_symmetric_close_issued_whole_hours(self):
        self.assertTrue(D.baseline_support(call(self.CL), self.CL)[0])
        p = self.CL[-1][1]
        self.assertIn("asymmetric", D.baseline_support(call(self.CL, lower=p * 0.99, upper=p * 1.003), self.CL)[1])
        self.assertIn("mid-bar", D.baseline_support(call(self.CL, issue_lag_s=1800), self.CL)[1])
        self.assertIn("mid-bar", D.baseline_support(call(self.CL, issue_price=p * 1.001,
                                                         lower=p * 1.001 * 0.994, upper=p * 1.001 / 0.994), self.CL)[1])
        odd = call(self.CL)
        odd["graded_close_utc"] = D.iso(D._t(odd["graded_close_utc"]) + dt.timedelta(minutes=30))
        self.assertIn("whole number", D.baseline_support(odd, self.CL)[1])
        self.assertFalse(D.baseline_support(dict(call(self.CL), call_type="lean"), self.CL)[0])

    def test_future_bars_cannot_enter(self):
        later = self.CL + [(self.CL[-1][0] + D.HOUR_MS, self.CL[-1][1] * 1.01)]
        self.assertFalse(D.matched_baseline(call(self.CL), later)["available"])     # the issue is no longer the last close

    def test_rate_matches_an_independent_computation(self):
        cl = walk(24 * 40, seed=3)
        D_LOOK = D.LOOKBACK_DAYS
        c = call(cl, half=0.005, h=2)
        try:
            D.LOOKBACK_DAYS = 30
            got = D.matched_baseline(c, cl)
        finally:
            D.LOOKBACK_DAYS = D_LOOK
        # brute force
        lr = [math.log(cl[i + 1][1] / cl[i][1]) for i in range(len(cl) - 1)]
        k = 0.005 / (statistics.stdev(lr[-24:]) * math.sqrt(2))
        first = cl[-1][0] - 30 * 86_400_000
        ins = tot = 0
        for i in range(24, len(cl) - 2):
            if cl[i][0] < first:
                continue
            s = statistics.stdev(lr[i - 24:i]) * math.sqrt(2)
            ins += abs(math.log(cl[i + 2][1] / cl[i][1])) <= k * s
            tot += 1
        self.assertTrue(got["available"], got)
        self.assertEqual(got["windows"], tot)
        self.assertAlmostEqual(got["rate"], ins / tot, places=12)
        self.assertAlmostEqual(got["k_sigma"], k, places=9)

    def test_constant_vol_walk_gives_about_the_normal_rate(self):
        c = call(self.CL, h=1)
        sig = D.matched_baseline(dict(c), self.CL)["sigma_issue_log"]
        c = call(self.CL, half=sig, h=1)                                   # k = 1
        got = D.matched_baseline(c, self.CL)
        self.assertAlmostEqual(got["k_sigma"], 1.0, places=9)
        self.assertTrue(0.64 < got["rate"] < 0.71, got["rate"])           # ~0.683 less the 24-return sd noise
        self.assertGreater(got["windows"], 17_000)

    def test_lean_drift_and_outcome(self):
        cl = walk(24 * 740, sigma=0.0, drift=0.0001)
        self.assertAlmostEqual(D.lean_drift(cl, 24), 0.0024, places=9)
        self.assertAlmostEqual(D.lean_outcome(1, 100.0, 101.0, 0.0024), math.log(1.01) - 0.001 - 0.0024, places=12)
        self.assertAlmostEqual(D.lean_outcome(-1, 100.0, 101.0, 0.0024), -math.log(1.01) - 0.001 + 0.0024, places=12)


class PairedTests(unittest.TestCase):
    def units(self, n, weeks, d, se=0.0, noise=0.0, seed=5):
        rnd = random.Random(seed)
        return [{"d": d + rnd.gauss(0, noise), "se": se,
                 "graded_close_utc": D.iso(dt.datetime(2026, 1, 5, tzinfo=UTC) + dt.timedelta(weeks=i % weeks, hours=i))}
                for i in range(n)]

    def test_a_hundred_calls_in_few_weeks_get_no_interval(self):
        out = D.paired(self.units(100, 6, 0.1))
        self.assertIsNone(out["interval"])
        self.assertEqual(out["blocks"], 6)
        self.assertTrue(out["status"].startswith("descriptive"))

    def test_claim_needs_thresholds_and_an_interval_excluding_zero(self):
        out = D.paired(self.units(60, 20, 0.2, noise=0.3))
        self.assertTrue(out["status"].startswith("comparative"), out)
        self.assertEqual(out, D.paired(self.units(60, 20, 0.2, noise=0.3)))             # seeded, reproducible
        mid = D.paired(self.units(40, 12, 0.2, noise=0.3))
        self.assertIsNotNone(mid["interval"])
        self.assertIn("below the claim thresholds", mid["status"])
        null = D.paired(self.units(80, 26, 0.0, noise=0.4))
        self.assertEqual(null["status"], "comparative: no demonstrated difference")     # never "equivalent"

    def test_baseline_error_widens_the_interval(self):
        a = D.paired(self.units(60, 20, 0.1, noise=0.3))
        b = D.paired(self.units(60, 20, 0.1, noise=0.3, se=0.02))
        self.assertAlmostEqual((b["interval"][1] - b["interval"][0]) - (a["interval"][1] - a["interval"][0]),
                               2 * 1.959964 * 0.02, places=9)


# ------------------------------------------------------------------------------------------------ O33 v3 (calls-2.0.0)
FROZEN_V3_SHA = "7c884dc65da1ed7da072a0f6709e89ad7c3fdb5bfdcafaaa0c7dc60f50262d56"
A0 = dt.datetime(2026, 10, 7, 12, 26, tzinfo=UTC)          # anchor minute (mid-bar)


def walk1m(days, sigma_min=0.0006, seed=7, end=A0, drift=0.0):
    rnd = random.Random(seed)
    n = days * 1440
    end_ms = int(end.timestamp() * 1000)
    c, out = 80_000.0, {}
    for i in range(n):
        out[end_ms - (n - 1 - i) * D.MINUTE_MS] = c
        c *= math.exp(drift + rnd.gauss(0, sigma_min))
    return out


def call3(closes, k_up=1.0, k_dn=0.5, h_min=214, issue_s=37, sigma=None, **kw):
    a = int(A0.timestamp() * 1000)
    p = closes[a]
    s = sigma
    d = {"call_type": "containment", "instrument": "BTC", "issue_price": p,
         "issue_utc": D.iso(A0 + dt.timedelta(seconds=issue_s)), "graded_close_utc": D.iso(A0 + dt.timedelta(minutes=h_min))}
    if s is not None:
        d.update(upper=p * math.exp(k_up * s), lower=p / math.exp(k_dn * s))
    d.update(kw)
    return d


class V3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = D.V3_LOOKBACK_DAYS
        D.V3_LOOKBACK_DAYS = 120
        cls.CL = walk1m(122)

    @classmethod
    def tearDownClass(cls):
        D.V3_LOOKBACK_DAYS = cls.saved

    def sig(self, h_min):
        probe = call3(self.CL, h_min=h_min, upper=1e9, lower=1)
        a = int(A0.timestamp() * 1000)
        pts = [self.CL[a - j * D.HOUR_MS] for j in range(25)]
        r = [math.log(pts[j] / pts[j + 1]) for j in range(24)]
        return statistics.stdev(r) * math.sqrt(h_min / 60)

    def test_spec_is_frozen(self):
        self.assertEqual(D.v3_spec_sha256(), FROZEN_V3_SHA)      # any change is v4, not an edit of v3
        self.assertEqual(D.VERSION, "calls-2.0.0")

    def test_support(self):
        s = self.sig(214)
        self.assertTrue(D.v3_support(call3(self.CL, sigma=s))[0])
        self.assertFalse(D.v3_support(dict(call3(self.CL, sigma=s), call_type="lean"))[0])
        bad = call3(self.CL, sigma=s)
        bad["graded_close_utc"] = D.iso(D._t(bad["graded_close_utc"]) + dt.timedelta(seconds=30))
        self.assertIn("whole minute", D.v3_support(bad)[1])
        self.assertIn("horizon", D.v3_support(call3(self.CL, sigma=s, h_min=10))[1])
        self.assertIn("horizon", D.v3_support(call3(self.CL, sigma=s, h_min=4321))[1])
        p = self.CL[int(A0.timestamp() * 1000)]
        self.assertIn("bracket", D.v3_support(call3(self.CL, lower=p * 1.01, upper=p * 1.02))[1])

    def test_rate_matches_an_independent_computation(self):
        h = 214
        s = self.sig(h)
        c = call3(self.CL, k_up=0.9, k_dn=1.2, h_min=h, sigma=s)
        got = D.matched_baseline_v3(c, self.CL)
        self.assertTrue(got["available"], got)
        a = int(A0.timestamp() * 1000)
        first = a - 120 * 86_400_000 + 24 * D.HOUR_MS
        ins = n = 0
        rets = []
        t = a - h * 60_000
        while (t - a) % D.HOUR_MS:
            t -= 60_000
        while t >= first:
            pts = [self.CL[t - j * D.HOUR_MS] for j in range(25)]
            st = statistics.stdev([math.log(pts[j] / pts[j + 1]) for j in range(24)]) * math.sqrt(h / 60)
            r = math.log(self.CL[t + h * 60_000] / self.CL[t])
            ins += -1.2 * st <= r <= 0.9 * st
            n += 1
            rets.append(r)
            t -= D.HOUR_MS
        self.assertEqual(got["windows"], n)
        self.assertAlmostEqual(got["rate"], ins / n, places=12)
        self.assertAlmostEqual(got["k_up"], 0.9, places=9)
        self.assertAlmostEqual(got["k_dn"], 1.2, places=9)
        self.assertAlmostEqual(got["lean_drift"], sum(rets) / len(rets), places=12)
        self.assertAlmostEqual(got["effective_n"], n * 60 / h, places=9)
        self.assertEqual(got["anchor_utc"], "2026-10-07T12:26:00Z")       # issued 12:26:37 -> last closed minute

    def test_asymmetric_band_on_a_constant_vol_walk(self):
        h = 240
        s = self.sig(h)
        got = D.matched_baseline_v3(call3(self.CL, k_up=1.0, k_dn=0.5, h_min=h, sigma=s), self.CL)
        self.assertTrue(0.48 < got["rate"] < 0.58, got["rate"])           # N(0,1): 0.533, less sigma-estimation noise
        sym = D.matched_baseline_v3(call3(self.CL, k_up=0.75, k_dn=0.75, h_min=h, sigma=s), self.CL)
        self.assertGreater(abs(got["rate"] - sym["rate"]), -1)            # both computed; shape matters, no assumed order

    def test_future_closes_never_enter(self):
        s = self.sig(214)
        c = call3(self.CL, sigma=s)
        a = int(A0.timestamp() * 1000)
        more = dict(self.CL)
        for i in range(1, 600):
            more[a + i * 60_000] = self.CL[a] * (1.05 if i % 2 else 0.95)
        x, y = D.matched_baseline_v3(c, self.CL), D.matched_baseline_v3(c, more)
        for k in ("rate", "windows", "k_up", "k_dn", "lean_drift"):
            self.assertEqual(x[k], y[k], k)

    def test_missing_data_makes_it_unavailable(self):
        s = self.sig(214)
        c = call3(self.CL, sigma=s)
        a = int(A0.timestamp() * 1000)
        keep = {a - j * D.HOUR_MS for j in range(25)}
        rnd = random.Random(3)
        holes = {t: v for t, v in self.CL.items() if t in keep or rnd.random() > 0.02}   # 2% of minutes missing
        got = D.matched_baseline_v3(c, holes)
        self.assertFalse(got["available"])
        self.assertIn("usable", got["reason"])
        self.assertLess(got["windows"], 0.95 * got["candidate_windows"])
        no_anchor = {t: v for t, v in self.CL.items() if t != int(A0.timestamp() * 1000)}
        self.assertIn("anchor", D.matched_baseline_v3(c, no_anchor)["reason"])

    def test_bound_multiples_outside_range(self):
        s = self.sig(214)
        self.assertIn("outside", D.matched_baseline_v3(call3(self.CL, k_up=9, k_dn=1, sigma=s), self.CL)["reason"])
        self.assertIn("outside", D.matched_baseline_v3(call3(self.CL, k_up=1, k_dn=0.01, sigma=s), self.CL)["reason"])

    def test_secondary_time_of_day_weekend_and_release_matching(self):
        h = 214
        s = self.sig(h)
        a = int(A0.timestamp() * 1000)
        rel = sorted({a - d * 86_400_000 + 90 * 60_000 for d in range(0, 120)})     # 13:56Z daily, incl. inside the call
        c = call3(self.CL, sigma=s, h_min=h)
        got = D.matched_baseline_v3(c, self.CL, rel)
        sec = got["secondary"]
        self.assertTrue(sec["call_window_has_release"])
        # independent filter
        first = a - 120 * 86_400_000 + 24 * D.HOUR_MS
        n = ins = 0
        t = a - h * 60_000
        while (t - a) % D.HOUR_MS:
            t -= 60_000
        while t >= first:
            hr = (t // D.HOUR_MS) % 24
            wk = dt.datetime.fromtimestamp(t / 1000, UTC).weekday() >= 5
            has = any(t < r <= t + h * 60_000 for r in rel)
            if min((hr - 12) % 24, (12 - hr) % 24) <= 2 and wk is False and has:
                pts = [self.CL[t - j * D.HOUR_MS] for j in range(25)]
                st = statistics.stdev([math.log(pts[j] / pts[j + 1]) for j in range(24)]) * math.sqrt(h / 60)
                r = math.log(self.CL[t + h * 60_000] / self.CL[t])
                ins += -0.5 * st <= r <= 1.0 * st
                n += 1
            t -= D.HOUR_MS
        if n >= D.V3_SECONDARY_MIN:
            self.assertEqual((sec["windows"], sec["rate"]), (n, ins / n))
        else:
            self.assertEqual((sec["available"], sec["windows"]), (False, n))
        self.assertEqual(got["rate"], D.matched_baseline_v3(c, self.CL)["rate"])        # the primary never changes

    def test_outcome_at_the_graded_close(self):
        s = self.sig(214)
        c = call3(self.CL, sigma=s)
        g = int(D._t(c["graded_close_utc"]).timestamp() * 1000)
        self.assertIsNone(D.containment_outcome_v3(c, self.CL))                 # not yet in the data
        self.assertEqual(D.containment_outcome_v3(c, {g: (c["lower"] + c["upper"]) / 2}), 1)
        self.assertEqual(D.containment_outcome_v3(c, {g: c["upper"] * 1.001}), 0)

    def test_loader_reuses_archive_validation_without_changing_the_module(self):
        import jbm_archive as A
        before = dict(A.INTERVAL_MS)
        seen = {}

        def fake(first, last, interval, symbol, opener):
            seen.update(interval=interval, step=A.INTERVAL_MS[interval])
            return "ok", [{"close_utc": "2026-10-07T12:01:00Z", "close": 1.0}], []
        saved, A.load_klines_span = A.load_klines_span, fake
        try:
            st, closes, _ = D.load_closes_1m(dt.date(2026, 10, 7), dt.date(2026, 10, 7))
        finally:
            A.load_klines_span = saved
            A.INTERVAL_MS.clear(); A.INTERVAL_MS.update(before)
        self.assertEqual((st, seen), ("ok", {"interval": "1m", "step": 60_000}))
        self.assertEqual(closes, {int(dt.datetime(2026, 10, 7, 12, 1, tzinfo=UTC).timestamp() * 1000): 1.0})
        self.assertEqual(A.VERSION, "archive-12.0.0")


if __name__ == "__main__":
    unittest.main()
