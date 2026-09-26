#!/usr/bin/env python3
"""Regressions for the 12.1 / repo 2.16 hardening findings. Each class reproduces a defect found in 12.0 / 2.15
and pins the fix. Classes marked REPO need the repository (schema.py, registration, the job); the rest also run
from the skill folder. Run: PYTHONDONTWRITEBYTECODE=1 python3 test_hardening.py
"""
import datetime as dt
import gzip
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

os.environ["RANGE_JOB_QUIET"] = "1"
DESK = Path(__file__).resolve().parent
sys.path[:0] = [str(DESK), str(DESK.parent)]

import range_contract as C          # noqa: E402
import range_model as R             # noqa: E402

try:
    import range_job as J           # noqa: E402
    import range_reader as RR       # noqa: E402
    import retained as K            # noqa: E402
    from test_range_job import Clock, PROD, dvol_rows, make_root   # noqa: E402
    from registration import register_batch   # noqa: E402,F401
    REPO = True
except ImportError:
    REPO = False
from test_range_model import synth_bars   # noqa: E402

UTC = dt.timezone.utc
T = lambda h, m=0, s=0, d=26: dt.datetime(2026, 9, d, h, m, s, tzinfo=UTC)   # noqa: E731
ms = C.ms
SEC = dt.timedelta(seconds=1)


def good_doc(h="24h", decision=T(0), delay_min=10):
    s = decision + dt.timedelta(minutes=delay_min)
    ev = lambda n: {"name": n, "type": "range", "point": 0.02, "q10": 0.012, "q50": 0.019, "q90": 0.035}  # noqa: E731
    return {"id": f"range-rc1d-{h}-{decision:%Y%m%dT%H%MZ}", "contract": C.contract_id("RC1D"),
            "instrument": "BTCUSDT perp, Binance last price", "reference_price": 80000.0,
            "decision_utc": C.iso(decision), "start_utc": C.iso(s), "made_utc": C.iso(decision + dt.timedelta(minutes=4)),
            "horizon_utc": C.iso(s + dt.timedelta(hours=C.HOURS[h])), "input_bundle": "a" * 64, "snapshot_hash": "a" * 64,
            "events": [ev("B2 range model range-11.1.0"), ev("B0 persistence baseline")]}


class TestStrictValidator(unittest.TestCase):
    """Finding 3: hash-correct but semantically inconsistent records are rejected, with reasons, never a crash."""

    def test_good_record_passes(self):
        self.assertEqual(C.validate_rc1d(good_doc()), [])

    def test_each_inconsistency_is_named(self):
        cases = {
            "window spans": lambda d: d.update(horizon_utc=C.iso(R._t(d["start_utc"]) + dt.timedelta(hours=24)), id=d["id"].replace("-24h-", "-4h-")),
            "B2: point": lambda d: d["events"][0].pop("point"),
            "exactly the B2 and B0": lambda d: d["events"].pop(),
            "quantiles not ordered": lambda d: d["events"][1].update(q10=0.05),
            "contract": lambda d: d.update(contract="RC1D/contract-9.9.9/000000000000"),
            "input_bundle": lambda d: d.update(snapshot_hash="b" * 64),
            "decision does not match": lambda d: d.update(id="range-rc1d-24h-20260926T0800Z"),
            "window start": lambda d: d.update(start_utc=C.iso(R._t(d["decision_utc"]) + dt.timedelta(minutes=2))),
            "timestamps": lambda d: d.update(made_utc="yesterday"),
            "finite": lambda d: d["events"][0].update(point=float("nan")),
        }
        for want, mutate in cases.items():
            with self.subTest(case=want):
                d = good_doc()
                mutate(d)
                errs = C.validate_rc1d(d)
                self.assertTrue(errs and any(want.split(":")[0].lower() in e.lower() for e in errs), errs)

    def test_malformed_manifest_and_publication_are_reasons_not_crashes(self):
        d = good_doc()
        self.assertTrue(C.validate_rc1d(d, entry="not a dict"))
        self.assertTrue(C.validate_rc1d(d, entry={"id": d["id"], "source": "x"}))
        self.assertTrue(C.validate_rc1d(d, publication={"confirmed": "soon", "ids": d["id"]}))
        self.assertTrue(C.validate_rc1d(["not", "a", "doc"]))


class TestExpiryRule(unittest.TestCase):
    """Finding 1, runnable from the skill folder: the expiry rule and a cached result on the consumer's clock."""

    def test_rule_and_revalidate(self):
        import range_reader as RS
        d = T(4)
        for h, until in (("4h", T(8, 20)), ("24h", T(9, 15)), ("72h", T(9, 15))):     # the live 04:00Z records
            start = d + dt.timedelta(minutes=20)
            end = start + dt.timedelta(hours=C.HOURS[h])
            self.assertEqual(RS.expiry(d, end), until, h)
            cached = {"state": "valid-current", "id": f"range-rc1d-{h}-20260926T0400Z", "contract": C.contract_id("RC1D"),
                      "start_utc": C.iso(start), "end_utc": C.iso(end), "valid_until_utc": C.iso(until)}
            self.assertEqual(RS.revalidate(cached, until - SEC)["state"], "valid-current")
            self.assertIn("not a remaining-range forecast", RS.revalidate(cached, until - SEC)["label"])
            self.assertIsNone(RS.revalidate(cached, until - SEC)["remaining"])
            self.assertEqual(RS.revalidate(cached, until)["state"], "stale")
        self.assertEqual(RS.revalidate({"state": "missing"}, T(5))["state"], "missing")      # never upgrades


@unittest.skipUnless((DESK / "fits/2026-09.json").exists(), "needs the repository's September fit")
class TestFitContract(unittest.TestCase):
    """Finding 7: an explicitly incompatible fit contract is refused; the pre-12.0 rule is explicit."""

    def test_rules(self):
        doc = json.loads((DESK / "fits/2026-09.json").read_text())
        cal = DESK / "releases_2020_2026.csv" if (DESK / "releases_2020_2026.csv").exists() else DESK / "data/releases_2020_2026.csv"
        m0 = dt.datetime(2026, 9, 1, tzinfo=UTC)
        C.validate_fit(doc, m0, cal, C._COMMON["model_spec_sha256"])                    # pre-12.0 fit: accepted
        for bad in ({"contract": "RC9/contract-9.0.0/abc"}, {"job": "someone-else"}):
            d = dict(doc, **bad)
            with self.assertRaises(C.FitInvalid):
                C.validate_fit(d, m0, cal, C._COMMON["model_spec_sha256"])
        C.validate_fit(dict(doc, contract=C.contract_id("RC1D")), m0, cal, C._COMMON["model_spec_sha256"])


@unittest.skipUnless(REPO, "needs the repository")
class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        n = 2400
        cls.bars = synth_bars(n, 21, 0.95, start=T(0) - dt.timedelta(hours=4 * n))
        cls.dvol = dvol_rows(cls.bars)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "registry").mkdir()
        (self.tmp / "state").mkdir()
        self.m0 = dt.datetime(2026, 9, 1, tzinfo=UTC)
        self.saved = (J.CALENDAR, J.CHAIN_ROOT)

    def tearDown(self):
        J.CALENDAR, J.CHAIN_ROOT = self.saved
        shutil.rmtree(self.tmp)

    def fit(self):
        return J.refit(self.m0 + dt.timedelta(days=3), base=self.tmp,
                       history=([b for b in self.bars if R._t(b["open_utc"]) < self.m0], self.dvol))

    def publish(self, now=T(0, 7)):
        self.fit()
        _, ids = J.forecast(now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol, clock=Clock(ms(now) + 5000), run=PROD)
        J.confirm(self.tmp, clock=lambda: ms(now) + 60_000, remote=lambda: ("c0ffee", json.loads(
            (self.tmp / "state/forecast_manifest.json").read_text())), run=PROD)
        return ids


class TestExpiry(Base):
    """Finding 1: a cached result and a fresh read agree before, at and after expiry (decision + 4h + grace,
    bounded by the window), including a missed next run and the previous decision's grace period."""

    def test_cached_and_fresh_agree(self):
        ids = self.publish()                                            # decision 00:00; 24h and 72h windows
        for h in ("24h", "72h"):
            cached = RR.read_current(self.tmp, T(4, 30), h)            # read during the next decision's window
            self.assertEqual(cached["state"], "valid-current")
            self.assertEqual(cached["valid_until_utc"], "2026-09-26T05:15:00Z")   # not 09:15
            until = T(5, 15)
            for t in (until - SEC, until, until + SEC, T(4, 10), T(5, 0)):    # before/at/after; grace period
                fresh, again = RR.read_current(self.tmp, t, h), RR.revalidate(cached, t)
                self.assertEqual(fresh["state"], again["state"], (h, t))
                self.assertEqual(fresh.get("elapsed_fraction"), again.get("elapsed_fraction"))
            self.assertEqual(RR.revalidate(cached, until)["state"], "stale")
        self.assertIn("not a remaining-range forecast", RR.revalidate(RR.read_current(self.tmp, T(1), "4h"), T(1, 30))["label"])
        self.assertIsNone(RR.revalidate(RR.read_current(self.tmp, T(1), "4h"), T(1, 30))["remaining"])
        self.assertEqual(RR.read_current(self.tmp, T(1), "4h")["valid_until_utc"], "2026-09-26T04:15:00Z")  # window end
        self.assertEqual(len(ids), 3)

    def test_cached_state_never_upgrades(self):
        cached = RR.read_current(self.tmp, T(0, 30), "4h")
        self.assertEqual(RR.revalidate(cached, T(0, 40))["state"], "missing")


class TestReaderNeverCrashes(Base):
    """Finding 3: forged hash-consistent records and malformed state files give integrity-failed with a reason."""

    def forge(self, fid, mutate):
        m = json.loads((self.tmp / "state/forecast_manifest.json").read_text())
        doc = json.loads((self.tmp / m[fid]["frozen"]).read_bytes())
        mutate(doc)
        raw = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode() + b"\n"
        h = hashlib.sha256(raw).hexdigest()
        (self.tmp / f"registry/frozen/{h}.json").write_bytes(raw)
        m[fid].update(sha256=h, frozen=f"registry/frozen/{h}.json")
        (self.tmp / "state/forecast_manifest.json").write_text(json.dumps(m))

    def test_forged_records(self):
        ids = self.publish()
        self.forge(ids[0], lambda d: d.update(horizon_utc=C.iso(R._t(d["start_utc"]) + dt.timedelta(hours=24))))
        self.forge(ids[2], lambda d: d["events"][0].pop("point"))
        r4, r72 = RR.read_current(self.tmp, T(0, 30), "4h"), RR.read_current(self.tmp, T(0, 30), "72h")
        self.assertEqual((r4["state"], r72["state"]), ("integrity-failed", "integrity-failed"))
        self.assertIn("spans 24h", r4["reason"]); self.assertIn("point", r72["reason"])
        st = RR.status(self.tmp, T(0, 30))
        self.assertEqual(len([p for p in st["integrity_failures"] if "range-rc1d" in p]), 2)
        import scoring                                                  # same boundary at scoring time
        fetch = lambda s, e: [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]   # noqa: E731
        _, new, _, alerts = scoring.score_registry(self.tmp, ms(T(4, 30, d=29)), "test", fetch=fetch)
        got = {r["id"]: r["status"] for r in new}
        self.assertEqual(got[ids[0]], "integrity failure — not scored")
        self.assertEqual(got[ids[2]], "integrity failure — not scored")
        self.assertEqual(got[ids[1]], "scored")                        # the untouched 24h record still scores

    def test_malformed_state_files(self):
        self.publish()
        (self.tmp / "state/range_publications.jsonl").write_text('{"attempt": 5}\n["x"]\n')
        r = RR.read_current(self.tmp, T(0, 30), "24h")
        self.assertEqual(r["state"], "ineligible")                     # its confirmation row is unusable
        st = RR.status(self.tmp, T(0, 30))
        self.assertTrue(any("malformed row" in p for p in st["integrity_failures"]))
        (self.tmp / "state/forecast_manifest.json").write_text("{not json")
        self.assertEqual(RR.read_current(self.tmp, T(0, 30), "24h")["state"], "integrity-failed")
        self.assertTrue(RR.status(self.tmp, T(0, 30))["integrity_failures"])
        (self.tmp / "state/forecast_manifest.json").write_text('["a list"]')
        self.assertEqual(RR.read_current(self.tmp, T(0, 30), "24h")["state"], "integrity-failed")

    def test_due_vs_current_decisions(self):
        self.publish()
        st = RR.status(self.tmp, T(0, 30))
        self.assertEqual((st["due_decisions"], st["current_decision"]["decision_utc"]), (0, "2026-09-26T00:00:00Z"))
        self.assertEqual(st["current"]["24h"]["state"], "valid-current")
        st = RR.status(self.tmp, T(1, 30))
        self.assertEqual((st["due_decisions"], st["outcomes"], st["current_decision"]), (1, {"registered-pending": 1}, None))


class TestRefitTail(Base):
    """Finding 2: an unpublished final archive segment is filled only from validated closed live bars."""

    def run_case(self, archive_state, archive_rows, live, states=None):
        root = make_root(self.tmp, [b for b in self.bars if b["open_utc"] < "2026-08-25T00:00:00Z"],
                         [r for r in self.dvol if r["open_utc"] < "2026-08-25T00:00:00Z"])
        J.CHAIN_ROOT = root
        import jbm_archive as A
        saved = (A.load_klines_span, A.load_dvol, J.fetch_recent_bars)
        man = [{"state": s} for s in (states or [archive_state])]
        A.load_klines_span = lambda f, l, i: (archive_state, archive_rows, man)
        A.load_dvol = lambda s, e, **k: ("ok", [r for r in self.dvol if s <= R._t(r["open_utc"]) < e], {"sha256": "y", "missing_hours": 0})
        J.fetch_recent_bars = live
        try:
            return J.refit(self.m0 + dt.timedelta(hours=1), base=self.tmp)
        finally:
            A.load_klines_span, A.load_dvol, J.fetch_recent_bars = saved

    def tail(self):
        return [b for b in self.bars if "2026-08-25T00:00:00Z" <= b["open_utc"] < "2026-09-01T00:00:00Z"]

    def test_missing_final_day_filled_equals_direct_fit(self):
        arch = [b for b in self.tail() if b["open_utc"] < "2026-08-31T00:00:00Z"]
        live = lambda m0, n=400, opener=None: ([b for b in self.tail() if b["open_utc"] >= "2026-08-30T00:00:00Z"], {"url": "mock"})  # noqa: E731
        got = json.loads(self.run_case("missing", arch, live, ["ok", "ok", "missing"]).read_text())
        ref = Path(tempfile.mkdtemp())
        want = json.loads(J.refit(self.m0 + dt.timedelta(hours=1), base=ref, history=(
            [b for b in self.bars if R._t(b["open_utc"]) < self.m0], self.dvol)).read_text())
        for h in C.HOURS:
            self.assertEqual(got["fits"][h]["beta"], want["fits"][h]["beta"])
        _, delta = J.read_blob(next((self.tmp / J.INPUTS / "refit").glob("*.json.gz")))
        self.assertEqual((delta["live_tail"]["from"], delta["live_tail"]["bars"], delta["live_tail"]["overlap_checked"]),
                         ("2026-08-31T00:00:00Z", 6, 6))

    def test_failures(self):
        tail = self.tail()
        arch = [b for b in tail if b["open_utc"] < "2026-08-31T00:00:00Z"]
        live_ok = lambda m0, n=400, opener=None: ([b for b in tail if b["open_utc"] >= "2026-08-30T00:00:00Z"], {})  # noqa: E731
        conflict = [dict(b) for b in tail if b["open_utc"] >= "2026-08-30T00:00:00Z"]
        conflict[0]["high"] *= 1.01
        unclosed = [b for b in tail if b["open_utc"] >= "2026-08-31T00:00:00Z"] + [
            dict(tail[-1], open_utc="2026-09-01T00:00:00Z", close_utc="2026-09-01T04:00:00Z")]
        bad = [dict(b) for b in tail if b["open_utc"] >= "2026-08-31T00:00:00Z"]
        bad[1]["low"] = bad[1]["high"] * 2

        def down(m0, n=400, opener=None):
            raise RuntimeError("recent bars not admissible: retrieval_error")
        cases = {
            "interior gap": ("missing", [b for b in arch if not b["open_utc"].startswith("2026-08-27")], live_ok, ["ok", "missing", "ok"]),
            "interior hole in ok bars": ("missing", [b for b in arch if b["open_utc"] != "2026-08-27T08:00:00Z"], live_ok, ["ok", "missing"]),
            "malformed archive": ("malformed", arch, live_ok, ["ok", "malformed"]),
            "conflicting overlap": ("missing", arch, lambda m0, n=400, opener=None: (conflict, {}), ["ok", "missing"]),
            "fallback unavailable": ("missing", arch, down, ["ok", "missing"]),
            "unclosed bar": ("missing", arch, lambda m0, n=400, opener=None: (unclosed, {}), ["ok", "missing"]),
            "malformed live bar": ("missing", arch, lambda m0, n=400, opener=None: (bad, {}), ["ok", "missing"]),
        }
        for name, (st, rows, live, states) in cases.items():
            with self.subTest(case=name):
                self.tearDown(); self.setUp()
                with self.assertRaises(RuntimeError):
                    self.run_case(st, rows, live, states)
                self.assertFalse((self.tmp / "desk/fits/2026-09.json").exists())


class TestRetainedRoot(Base):
    """Finding 5: an altered or missing root input stops the refit chain, exactly as it stops O21 replay."""

    def test_altered_root_refused(self):
        root = make_root(self.tmp, self.bars[:500], self.dvol[:2000])
        J.CHAIN_ROOT = root
        self.assertEqual(len(J.history_chain(self.tmp)[0]), 500)
        p = root / "inputs/klines_4h.json.gz"
        k = json.loads(gzip.decompress(p.read_bytes()))
        k["rows"][100]["high"] *= 1.5
        p.write_bytes(gzip.compress(json.dumps(k).encode()))
        with self.assertRaises(K.RetainedError):
            J.history_chain(self.tmp)
        with self.assertRaises(K.RetainedError):
            J.refit(dt.datetime(2026, 10, 1, 1, tzinfo=UTC), base=self.tmp)
        (root / "MANIFEST.json").write_text("{")
        with self.assertRaises(K.RetainedError):
            J.history_chain(self.tmp)

    def test_real_root_reproduces_the_september_fit(self):
        k, d = K.load_o21_inputs(DESK / "research/o21")
        base = Path(tempfile.mkdtemp())
        (base / "state").mkdir()
        p = J.refit(self.m0 + dt.timedelta(days=1), base=base, history=(
            [b for b in k["rows"] if R._t(b["open_utc"]) < self.m0], [r for r in d["rows"] if R._t(r["open_utc"]) < self.m0]))
        got, want = json.loads(p.read_text()), json.loads((DESK / "fits/2026-09.json").read_text())
        for h in C.HOURS:
            self.assertEqual((got["fits"][h]["beta"], got["fits"][h]["resid_q"]), (want["fits"][h]["beta"], want["fits"][h]["resid_q"]))
        shutil.rmtree(base)


class TestCalendarReplay(Base):
    """Finding 4: replay resolves the calendar version by hash after an additive refresh; missing or altered
    retained bytes fail clearly."""

    def test_additive_refresh(self):
        cal = self.tmp / "cal.csv"
        shutil.copy(self.saved[0], cal)
        J.CALENDAR = cal
        ids = self.publish()
        self.assertEqual(J.replay(ids[0], base=self.tmp)["_replay"]["calendar"], "current")
        with open(cal, "a") as f:
            f.write('2027-01-13T13:30:00Z,CPI,2027-01-13,08:30 ET,"test","future-only addition"\n')
        self.assertEqual(J.replay(ids[0], base=self.tmp)["_replay"]["calendar"], "retained")
        kept = next((self.tmp / "desk/calendars").glob("*.csv"))
        kept.write_bytes(kept.read_bytes() + b"\n")
        with self.assertRaises(K.RetainedError):
            J.replay(ids[0], base=self.tmp)
        kept.unlink()
        with self.assertRaises(K.RetainedError):                    # not current, not retained, no Git history
            J.replay(ids[0], base=self.tmp)


@unittest.skipUnless(REPO, "needs the repository")
class TestLiveRecords(unittest.TestCase):
    """The three registered 04:00Z forecasts stay authoritative, readable and replayable."""
    IDS = ["range-rc1d-4h-20260926T0400Z", "range-rc1d-24h-20260926T0400Z", "range-rc1d-72h-20260926T0400Z"]

    def test_read_and_replay(self):
        base = DESK.parent
        m = json.loads((base / "state/forecast_manifest.json").read_text())
        if not all(i in m for i in self.IDS):
            self.skipTest("checkout without the Sep 26 04:00Z registrations")
        for fid, h in zip(self.IDS, ("4h", "24h", "72h")):
            self.assertEqual(hashlib.sha256((base / m[fid]["frozen"]).read_bytes()).hexdigest(), m[fid]["sha256"])
            r = RR.read_current(base, T(4, 30), h)
            self.assertEqual((r["state"], r["id"]), ("valid-current", fid))
            self.assertEqual(J.replay(fid, base=base)["id"], fid)
        # scoring path on a disposable copy (synthetic 1m bars; real scoring needs the matured windows)
        import scoring
        tmp = Path(tempfile.mkdtemp())
        for d in ("registry", "state"):
            shutil.copytree(base / d, tmp / d)
        fetch = lambda s, e: [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]   # noqa: E731
        _, new, _, _ = scoring.score_registry(tmp, ms(T(12, 0, d=29)), "test", fetch=fetch)
        got = {r["id"]: r for r in new if r["id"] in self.IDS}
        self.assertEqual({r["status"] for r in got.values()}, {"scored"})
        self.assertEqual({r["events"][0]["loss_basis"] for r in got.values()}, {"point (desk/range_contract.py)"})
        shutil.rmtree(tmp)


@unittest.skipUnless(REPO, "needs the repository")
class TestReleaseChecker(unittest.TestCase):
    """Finding 7: the release check fails on a missing calendar or a changed retained artifact."""

    def test_missing_calendar_and_artifact(self):
        import make_release as M
        tmp = Path(tempfile.mkdtemp())
        for f in ("release.json", "range_model.py", *M.SHARED, "releases_2020_2026.csv"):
            shutil.copy(DESK / f, tmp / f)
        self.assertEqual([p for p in M.check(tmp) if "calendar" in p or "releases" in p], [])
        (tmp / "releases_2020_2026.csv").unlink()
        self.assertIn("releases_2020_2026.csv: missing", M.check(tmp))
        shutil.copytree(DESK / "research", tmp / "research")
        (tmp / "research/o21/holm_addendum_12.1.json").write_text("{}")
        self.assertTrue(any("holm_addendum" in p for p in M.check(tmp)))
        shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=1)
