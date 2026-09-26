#!/usr/bin/env python3
"""Offline tests for range_job / range_reader (crypto-desk 12.0, repo 2.15): transactional registration,
recovery, publication eligibility, fit validation, admissibility, replay, the reader's states and the status
surface. Uses the repository's own schema.py, registration.py and scoring.py in a temporary directory.
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_range_job.py
"""
import datetime as dt
import gzip
import hashlib
import json
import math
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
sys.path[:0] = [str(DESK), str(DESK.parent)]

import range_contract as C                # noqa: E402
import range_job as J                     # noqa: E402
import range_model as R                   # noqa: E402
import range_reader as RR                 # noqa: E402
from test_range_model import synth_bars   # noqa: E402

UTC = dt.timezone.utc
T = lambda h, m=0, s=0: dt.datetime(2026, 9, 26, h, m, s, tzinfo=UTC)   # noqa: E731
ms = C.ms
PROD = {"event": "schedule", "run_id": "42", "code_commit": "abc", "production": True}


def dvol_rows(bars, level=40.0):
    t0, t1 = R._t(bars[0]["open_utc"]), R._t(bars[-1]["close_utc"])
    out, t = [], t0
    while t < t1:
        out.append({"open_utc": R._iso(t), "available_at_utc": R._iso(t + dt.timedelta(hours=1)), "dvol": level})
        t += dt.timedelta(hours=1)
    return out


class Clock:
    """A clock that returns `first` for the first n calls and `then` afterwards (injected timing)."""
    def __init__(self, first, n=10 ** 9, then=None):
        self.first, self.n, self.then, self.calls = first, n, then, 0

    def __call__(self):
        self.calls += 1
        return self.first if self.calls <= self.n else self.then


class Base(unittest.TestCase):
    now = T(0, 7)

    @classmethod
    def setUpClass(cls):
        n = 2400
        start = T(0) - dt.timedelta(hours=4 * n)
        cls.bars = synth_bars(n, 21, 0.95, start=start)
        cls.dvol = dvol_rows(cls.bars)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "registry").mkdir()
        (self.tmp / "state").mkdir()
        self.m0 = dt.datetime(2026, 9, 1, tzinfo=UTC)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def fit(self):
        hist = [b for b in self.bars if R._t(b["open_utc"]) < self.m0]
        return J.refit(self.m0 + dt.timedelta(days=3), base=self.tmp, history=(hist, self.dvol))

    def run_forecast(self, clock=None, now=None, **kw):
        kw.setdefault("run", PROD)
        return J.forecast(now or self.now, base=self.tmp, bars=self.bars[-400:], dvol=kw.pop("dvol", self.dvol),
                          clock=clock or Clock(ms(self.now) + 5000), **kw)

    def manifest(self):
        p = self.tmp / "state/forecast_manifest.json"
        return json.loads(p.read_text()) if p.exists() else {}

    def attempts(self):
        p = self.tmp / J.ATTEMPTS
        return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

    def sources(self):
        return sorted(p.name for p in (self.tmp / "registry").glob("range-*.json"))

    def remote_ok(self):
        return lambda: ("c0ffee", self.manifest())


class TestSpec(Base):
    def test_model_file_is_the_frozen_spec(self):
        self.assertTrue(J.spec_ok())
        self.assertEqual(hashlib.sha256((DESK / "range_model.py").read_bytes()).hexdigest(), J.FROZEN_SPEC)


class TestTransaction(Base):
    def test_success_registers_three_with_one_freeze_time(self):
        self.fit()
        state, ids = self.run_forecast()
        self.assertEqual(state, "frozen")
        m = self.manifest()
        self.assertEqual(sorted(m), sorted(ids))
        self.assertEqual({m[i]["registered"] for i in ids}, {ms(self.now) + 5000})
        for i in ids:
            doc = json.loads((self.tmp / m[i]["frozen"]).read_bytes())
            self.assertEqual(doc["start_utc"], "2026-09-26T00:15:00Z")          # 00:07:05 + 5 min -> 00:15
            self.assertEqual(doc["contract"], C.contract_id("RC1D"))
            self.assertIn("point", doc["events"][0])
        self.assertEqual(self.sources(), sorted(f"{i}.json" for i in ids))

    def test_reproduced_timing_cannot_strand_files(self):
        """Audit sequence: validation at 00:07:05, registration clock later. 2.14 left three unregistered files
        and a retry skipped them. Now: one freeze time; if the clock crosses the margin, nothing is exposed."""
        self.fit()
        late = Clock(ms(T(0, 7, 5)), n=2, then=ms(T(0, 13, 30)))       # prepared 00:07:05 (start 00:15), freeze 00:13:30
        with self.assertRaises(RuntimeError):
            self.run_forecast(clock=late)
        self.assertEqual((self.sources(), self.manifest()), ([], {}))
        self.assertFalse(list((self.tmp / "registry").glob("frozen/*")))
        self.assertEqual(self.attempts()[-1]["state"], "abandoned")
        with self.assertRaises(J.AttemptRefused):                     # retry at 00:14 cannot move the window
            self.run_forecast(clock=Clock(ms(T(0, 14))), now=T(0, 14))
        self.assertEqual((self.sources(), self.manifest()), ([], {}))

    def test_original_timing_now_registers_completely(self):
        self.fit()
        state, ids = self.run_forecast(clock=Clock(ms(T(0, 7, 5)), n=2, then=ms(T(0, 11))))
        self.assertEqual((state, len(self.manifest())), ("frozen", 3))

    def test_idempotent_retry_verifies_the_manifest(self):
        self.fit()
        self.run_forecast()
        before = self.manifest()
        state, _ = self.run_forecast(clock=Clock(ms(T(0, 9))), now=T(0, 9))
        self.assertEqual((state, self.manifest()), ("existing", before))

    def test_injected_failures_before_commit_leave_nothing(self):
        for point in ("after_frozen", "before_manifest"):
            with self.subTest(point=point):
                self.tearDown(); self.setUp(); self.fit()

                def boom():
                    raise OSError(f"injected at {point}")
                with self.assertRaises(OSError):
                    self.run_forecast(hooks={point: boom})
                self.assertEqual((self.sources(), self.manifest()), ([], {}))
                self.assertFalse(list((self.tmp / "registry").glob("frozen/*")))
                self.assertEqual(self.attempts()[-1]["state"], "failed")
                self.assertTrue(self.attempts()[-1]["start_ms"])       # the window is on record
                with self.assertRaises(J.AttemptRefused):
                    self.run_forecast(clock=Clock(ms(T(0, 8))), now=T(0, 8))

    def test_failure_after_commit_rolls_forward(self):
        self.fit()

        def boom():
            raise OSError("injected after manifest")
        state, ids = self.run_forecast(hooks={"after_manifest": boom})
        self.assertEqual((state, len(self.manifest())), ("frozen", 3))
        self.assertEqual(len(self.sources()), 3)
        (self.tmp / "registry" / f"{ids[0]}.json").unlink()            # a lost source is derivable
        J.reconcile(self.tmp, ms(T(0, 9)), PROD)
        self.assertEqual(len(self.sources()), 3)

    def test_orphan_with_different_bytes_blocks_registration(self):
        self.fit()
        (self.tmp / "registry/range-rc1d-4h-20260926T0000Z.json").write_text("{}\n")
        with self.assertRaises(Exception):
            self.run_forecast()
        self.assertEqual(self.manifest(), {})


class TestEligibility(Base):
    def test_confirmed_before_start_is_eligible_and_current(self):
        self.fit()
        _, ids = self.run_forecast()
        rows = J.confirm(self.tmp, clock=lambda: ms(T(0, 8)), remote=self.remote_ok(), run=PROD)
        self.assertTrue(rows[0]["eligible"])
        r = RR.read_current(self.tmp, T(1, 0), "4h")
        self.assertEqual((r["state"], r["id"]), ("valid-current", ids[0]))
        self.assertIn("not a remaining-range forecast", r["label"])
        self.assertIsNone(r["remaining"])
        self.assertAlmostEqual(r["elapsed_fraction"], 45 / 240, places=3)

    def test_confirmed_after_start_is_ineligible(self):
        self.fit()
        self.run_forecast()
        J.confirm(self.tmp, clock=lambda: ms(T(0, 16)), remote=self.remote_ok(), run=PROD)
        self.assertEqual(self.attempts()[-1]["state"], "published-late")
        self.assertEqual(RR.read_current(self.tmp, T(1), "24h")["state"], "ineligible")

    def test_never_confirmed_becomes_unconfirmed(self):
        self.fit()
        self.run_forecast()
        self.assertEqual(RR.read_current(self.tmp, T(0, 9), "4h")["state"], "ineligible")
        J.reconcile(self.tmp, ms(T(4, 3)), PROD)
        self.assertEqual(self.attempts()[-1]["state"], "unconfirmed")

    def test_remote_without_entries_is_not_confirmed(self):
        self.fit()
        self.run_forecast()
        self.assertEqual(J.confirm(self.tmp, clock=lambda: ms(T(0, 8)), remote=lambda: ("c0ffee", {}), run=PROD), [])

    def test_scoring_respects_publication(self):
        import scoring
        self.fit()
        _, ids = self.run_forecast()
        J.confirm(self.tmp, clock=lambda: ms(T(0, 8)), remote=self.remote_ok(), run=PROD)

        def fetch(start, end):
            return [(t, 101.0, 99.0, 100.0) for t in range(start, end, 60_000)]
        records, new, pending, alerts = scoring.score_registry(self.tmp, ms(T(4, 30)), "test", fetch=fetch)
        got = {r["id"]: r for r in new}
        self.assertEqual(got[ids[0]]["status"], "scored")
        self.assertEqual(got[ids[0]]["events"][0]["loss_basis"], "point (desk/range_contract.py)")
        self.assertAlmostEqual(got[ids[0]]["events"][0]["realized_ln_range"], math.log(101 / 99), places=10)
        self.assertEqual(pending, 2)                                    # 24h and 72h not matured

    def test_scoring_marks_unconfirmed(self):
        import scoring
        self.fit()
        _, ids = self.run_forecast()
        fetch = lambda s, e: [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]   # noqa: E731
        _, new, _, _ = scoring.score_registry(self.tmp, ms(T(4, 30)), "test", fetch=fetch)
        self.assertEqual({r["id"]: r["status"] for r in new}[ids[0]], "publication unconfirmed — not scored")


class TestFitValidation(Base):
    def test_valid_existing_fit_is_reused(self):
        p = self.fit()
        before = p.read_bytes()
        J.refit(self.m0 + dt.timedelta(days=10), base=self.tmp)       # validates, never rewrites
        self.assertEqual(p.read_bytes(), before)

    def test_bogus_metadata_refused_before_publication(self):
        """Audit reproduction: zeroed spec/calendar hashes and month 1999-01 registered three forecasts in 2.14."""
        p = self.fit()
        doc = json.loads(p.read_text())
        doc.update(month="1999-01", spec_sha256="0" * 64, calendar_sha256="0" * 64)
        p.write_text(json.dumps(doc))
        with self.assertRaises(C.FitInvalid):
            self.run_forecast()
        self.assertEqual((self.manifest(), self.sources()), ({}, []))
        self.assertEqual(self.attempts()[-1]["state"], "failed")

    def test_each_corruption_is_caught(self):
        p = self.fit()
        good = json.loads(p.read_text())
        cases = {
            "terms order": lambda d: d["fits"]["4h"]["terms"].reverse(),
            "beta length": lambda d: d["fits"]["24h"]["beta"].pop(),
            "non-finite": lambda d: d["fits"]["72h"]["beta"].__setitem__(2, float("nan")),
            "resid unsorted": lambda d: d["fits"]["4h"]["resid_q"].reverse(),
            "model": lambda d: d["fits"]["4h"].__setitem__("model", "B1"),
            "cutoff": lambda d: d.__setitem__("last_bar", "2026-08-31T16:00:00Z"),
            "horizon missing": lambda d: d["fits"].pop("72h"),
            "calendar": lambda d: (d.__setitem__("calendar_sha256", "0" * 64), d.pop("calendar_prefix_sha256")),
            "b0 quantiles": lambda d: d["b0_resid_q"]["4h"].append(0.1),
            "n": lambda d: d["fits"]["4h"].__setitem__("n", 10),
        }
        for name, corrupt in cases.items():
            with self.subTest(name=name):
                d = json.loads(json.dumps(good))
                corrupt(d)
                with self.assertRaises(C.FitInvalid):
                    C.validate_fit(d, self.m0, J.CALENDAR, J.FROZEN_SPEC)
        C.validate_fit(good, self.m0, J.CALENDAR, J.FROZEN_SPEC)

    def test_committed_september_fit_validates(self):
        doc = json.loads((DESK / "fits/2026-09.json").read_text())
        C.validate_fit(doc, self.m0, J.CALENDAR, J.FROZEN_SPEC)


class TestAdmissibility(Base):
    def test_malformed_dvol_refused(self):
        self.fit()
        with self.assertRaises(ValueError):
            self.run_forecast(dvol_state="malformed", dvol_report={"conflicts": 1})
        self.assertEqual(self.manifest(), {})

    def test_incomplete_dvol_admitted_only_with_the_decision_candle(self):
        self.fit()
        state, ids = self.run_forecast(dvol_state="incomplete", dvol_report={"missing_hours": 3})
        self.assertEqual(state, "frozen")
        doc = json.loads((self.tmp / self.manifest()[ids[0]]["frozen"]).read_bytes())
        _, bundle = J.read_blob(self.tmp / J.INPUTS / "2026-09" / f"{doc['input_bundle']}.json.gz")
        self.assertEqual(bundle["sources"]["dvol_admissibility"]["override"], "dvol_incomplete_live")
        self.tearDown(); self.setUp(); self.fit()
        cut = [r for r in self.dvol if r["available_at_utc"] < "2026-09-25T17:00:00Z"]   # >6h before the decision
        with self.assertRaises(ValueError):
            self.run_forecast(dvol=cut, dvol_state="incomplete", dvol_report={"missing_hours": 7})

    def test_stale_decision_skipped_and_logged(self):
        self.fit()
        with self.assertRaises(J.StaleDecision):
            self.run_forecast(now=T(1, 30), clock=Clock(ms(T(1, 30))))
        self.assertEqual(self.attempts()[-1]["state"], "skipped")


class TestReplay(Base):
    def test_replay_reproduces_and_detects_tampering(self):
        base = DESK.parent
        self.fit()
        _, ids = self.run_forecast()
        old = J.BASE
        try:
            got = J.replay(ids[1], base=self.tmp)
            self.assertEqual(got["id"], ids[1])
            doc = json.loads((self.tmp / self.manifest()[ids[1]]["frozen"]).read_bytes())
            path = self.tmp / J.INPUTS / "2026-09" / f"{doc['input_bundle']}.json.gz"
            raw = json.loads(gzip.decompress(path.read_bytes()))
            raw["bars"][-1]["high"] *= 1.01
            path.write_bytes(gzip.compress(json.dumps(raw).encode()))
            with self.assertRaises(ValueError):
                J.replay(ids[1], base=self.tmp)
            path.unlink()
            with self.assertRaises(FileNotFoundError):
                J.replay(ids[1], base=self.tmp)
        finally:
            J.BASE = old
        self.assertTrue(base.exists())


class TestReaderStates(Base):
    def test_missing_unregistered_integrity_stale(self):
        self.assertEqual(RR.read_current(self.tmp, T(0, 30), "4h")["state"], "missing")
        (self.tmp / "registry/range-rc1d-4h-20260926T0000Z.json").write_text("{}")
        self.assertEqual(RR.read_current(self.tmp, T(0, 30), "4h")["state"], "unregistered")
        (self.tmp / "registry/range-rc1d-4h-20260926T0000Z.json").unlink()
        self.fit()
        _, ids = self.run_forecast()
        J.confirm(self.tmp, clock=lambda: ms(T(0, 8)), remote=self.remote_ok(), run=PROD)
        self.assertEqual(RR.read_current(self.tmp, T(6), "4h")["state"], "stale")          # window ended
        self.assertEqual(RR.read_current(self.tmp, T(9), "72h")["state"], "stale")        # newer decision expected
        frozen = self.tmp / self.manifest()[ids[2]]["frozen"]
        frozen.write_bytes(frozen.read_bytes().replace(b'"note":"', b'"note":"x'))
        self.assertEqual(RR.read_current(self.tmp, T(1), "72h")["state"], "integrity-failed")

    def test_legacy_records_are_not_current(self):
        m = {"range-b2-4h-20260926T0400Z": {"frozen": "registry/frozen/x.json", "sha256": "x", "registered": 0, "source": "x"}}
        (self.tmp / "state/forecast_manifest.json").write_text(json.dumps(m))
        r = RR.read_current(self.tmp, T(4, 30), "4h")
        self.assertEqual(r["state"], "missing"); self.assertIn("legacy", r["reason"])


class TestStatus(Base):
    def test_reconciles_expected_decisions(self):
        self.fit()
        self.run_forecast()
        J.confirm(self.tmp, clock=lambda: ms(T(0, 8)), remote=self.remote_ok(), run=PROD)
        nxt = dict(self.bars[-1], open_utc="2026-09-26T00:00:00Z", close_utc="2026-09-26T04:00:00Z")
        with self.assertRaises(J.StaleDecision):          # the 04:00 decision's run starts too late
            J.forecast(T(5, 30), base=self.tmp, bars=self.bars[-399:] + [nxt], dvol=self.dvol,
                       clock=Clock(ms(T(5, 30))), run=PROD)
        J.forecast(T(0, 9), base=self.tmp, bars=self.bars[-400:], dvol=self.dvol, clock=Clock(ms(T(0, 9))),
                   run=dict(PROD, production=False))    # a local re-run: verified as existing, not counted
        st = RR.status(self.tmp, T(13, 30))
        self.assertEqual(st["outcomes"], {"registered-pending": 1, "skipped": 1, "missing": 2})
        self.assertEqual([r["outcome"] for r in st["recent"]], ["registered-pending", "skipped", "missing", "missing"])
        self.assertEqual(st["current"]["72h"]["state"], "stale")
        self.assertIn("registered-pending", RR.markdown(st))


class TestChainedRefit(Base):
    """October-style refit: history from the retained chain (root + deltas) plus the days since, fetched through
    the loader (faked here); the delta is retained content-addressed and the fit validates."""

    def test_refit_from_chain_and_delta(self):
        import jbm_archive as A
        root = self.tmp / "root"
        root.mkdir()
        cut = "2026-08-20T00:00:00Z"
        kb = [b for b in self.bars if b["open_utc"] < cut]
        dv = [r for r in self.dvol if r["open_utc"] < cut]
        (root / "klines_4h.json.gz").write_bytes(gzip.compress(json.dumps({"rows": kb}).encode()))
        (root / "dvol_1h.json.gz").write_bytes(gzip.compress(json.dumps({"rows": dv}).encode()))
        later = [b for b in self.bars if cut <= b["open_utc"] < "2026-09-01T00:00:00Z"]
        dlater = [r for r in self.dvol if cut <= r["open_utc"] < "2026-09-01T00:00:00Z"]
        saved = (J.CHAIN_ROOT, A.load_klines_span, A.load_dvol)
        J.CHAIN_ROOT = root
        A.load_klines_span = lambda first, last, interval: ("ok", later, [{"url": "fake", "sha256": "x"}])
        A.load_dvol = lambda s, e, **kw: ("ok", [r for r in dlater if R._t(r["open_utc"]) >= s], {"sha256": "y", "missing_hours": 0})
        try:
            p = J.refit(self.m0 + dt.timedelta(hours=1), base=self.tmp)
        finally:
            J.CHAIN_ROOT, A.load_klines_span, A.load_dvol = saved
        doc = json.loads(p.read_text())
        self.assertEqual(doc["data"]["chain"][0], "o21-inputs")
        self.assertEqual(len(doc["data"]["chain"]), 2)
        ref = self.tmp / "ref"
        (ref / "state").mkdir(parents=True)
        want = json.loads(J.refit(self.m0 + dt.timedelta(hours=1), base=ref,
                                  history=([b for b in self.bars if b["open_utc"] < "2026-09-01T00:00:00Z"], self.dvol)).read_text())
        for h in C.HOURS:
            self.assertEqual(doc["fits"][h]["beta"], want["fits"][h]["beta"])
        J.CHAIN_ROOT = root
        try:
            bars, dvol, links = J.history_chain(self.tmp)
        finally:
            J.CHAIN_ROOT = saved[0]
        self.assertEqual(bars[-1]["open_utc"], "2026-08-31T20:00:00Z")
        delta = next((self.tmp / J.INPUTS / "refit").glob("*.json.gz"))
        delta.write_bytes(gzip.compress(b'{"month":"2026-09","bars":[],"dvol":[]}'))
        J.CHAIN_ROOT = root
        try:
            with self.assertRaises(ValueError):
                J.history_chain(self.tmp)
        finally:
            J.CHAIN_ROOT = saved[0]


if __name__ == "__main__":
    unittest.main(verbosity=1)
