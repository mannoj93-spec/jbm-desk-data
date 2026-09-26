#!/usr/bin/env python3
"""As-of reading, shared eligibility and strict RC1D validation (crypto-desk 12.2, repo 2.17).

Deterministic: every read runs against a disposable copy of desk/fixtures/rc1d_20260926 (byte copies of the first
two production batches, 04:00Z and 08:00Z on Sep 26 2026), never against the growing production registry. A
synthetic third batch is added to show that later registrations cannot change a historical read. ID-specific
compatibility with the production registry (same bytes, replayable) is checked separately, and only when the
repository's records are present. Needs the repository (schema.py, registration.py, scoring.py).
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_asof.py
"""
import copy
import datetime as dt
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parent
sys.path[:0] = [str(DESK), str(DESK.parent)]

import range_contract as C          # noqa: E402

try:
    import range_reader as RR       # noqa: E402
    import schema                   # noqa: E402,F401
    REPO = True
except ImportError:
    REPO = False

UTC = dt.timezone.utc
FX = DESK / "fixtures/rc1d_20260926"
T = lambda h, m=0, s=0, d=26, us=0: dt.datetime(2026, 9, d, h, m, s, us, tzinfo=UTC)   # noqa: E731
MS = lambda t: int(round(t.timestamp() * 1000))                                          # noqa: E731
IDS4 = [f"range-rc1d-{h}-20260926T0400Z" for h in ("4h", "24h", "72h")]
IDS8 = [f"range-rc1d-{h}-20260926T0800Z" for h in ("4h", "24h", "72h")]


class Repo:
    """A disposable repository-shaped copy of the fixture with helpers to add or alter records."""

    def __init__(self):
        self.base = Path(tempfile.mkdtemp())
        shutil.copytree(FX / "registry", self.base / "registry")
        shutil.copytree(FX / "state", self.base / "state")

    def manifest(self):
        return json.loads((self.base / "state/forecast_manifest.json").read_text())

    def pubs(self):
        return [json.loads(x) for x in (self.base / "state/range_publications.jsonl").read_text().splitlines() if x.strip()]

    def doc(self, fid):
        return json.loads((self.base / self.manifest()[fid]["frozen"]).read_bytes())

    def put(self, fid, doc, entry=None, pub=None):
        """(Re)write one record: frozen bytes, manifest entry (hash recomputed) and optionally its publication row."""
        raw = C.canonical(doc) if doc is not None else None
        m = self.manifest()
        e = dict(m.get(fid) or {}, **(entry or {}))
        if raw is not None:
            sha = hashlib.sha256(raw).hexdigest()
            (self.base / f"registry/frozen/{sha}.json").write_bytes(raw)
            (self.base / f"registry/{fid}.json").write_bytes(raw)
            e.update(sha256=sha, frozen=f"registry/frozen/{sha}.json", id=fid, source=f"registry/{fid}.json")
        m[fid] = e
        (self.base / "state/forecast_manifest.json").write_text(json.dumps(m, indent=1, sort_keys=True))
        if pub is not None:
            rows = [r for r in self.pubs() if r.get("attempt") != pub.get("attempt")] + [pub]
            (self.base / "state/range_publications.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))

    def drop(self, ids):
        m = self.manifest()
        for i in ids:                                  # a missed run: no entry and no source file
            (self.base / m.pop(i)["source"]).unlink()
        (self.base / "state/forecast_manifest.json").write_text(json.dumps(m, indent=1, sort_keys=True))

    def add_batch(self, decision, prepared, registered_ms, confirmed_ms):
        """A synthetic batch: the 08:00Z documents moved to `decision` with their canonical RC1D windows."""
        attempt = f"{C.iso(decision)}#synthetic"
        ids = []
        for h in ("4h", "24h", "72h"):
            src = self.doc(f"range-rc1d-{h}-20260926T0800Z")
            s, e = C.window("RC1D", decision, h, prepared)
            fid = f"range-rc1d-{h}-{decision:%Y%m%dT%H%MZ}"
            d = dict(src, id=fid, decision_utc=C.iso(decision), made_utc=C.iso(prepared), start_utc=C.iso(s),
                     horizon_utc=C.iso(e))
            self.put(fid, d, {"attempt": attempt, "registered": registered_ms, "prepared": MS(prepared)})
            ids.append(fid)
        s, _ = C.window("RC1D", decision, "4h", prepared)
        self.put(ids[0], None, pub={"attempt": attempt, "confirmed": confirmed_ms, "eligible": True, "ids": ids,
                                    "start_ms": MS(s)})
        return ids

    def read(self, t, h="4h"):
        return RR.read_current(self.base, t, h)

    def close(self):
        shutil.rmtree(self.base, ignore_errors=True)


@unittest.skipUnless(REPO and FX.exists(), "needs the repository and its fixture")
class TestAsOf(unittest.TestCase):
    """Finding 1: a forecast is readable only once decision, preparation, registration and publication have all
    happened; the newest such record governs; later registrations never change a historical read."""

    def setUp(self):
        self.r = Repo()

    def tearDown(self):
        self.r.close()

    def states(self, t):
        return {h: (x["state"], x.get("id")) for h in ("4h", "24h", "72h") for x in [self.r.read(t, h)]}

    def test_before_and_after_each_publication(self):
        # 04:00Z batch: registered 04:13:17.546, confirmed 04:13:19.582; 08:00Z: 08:15:19.365 / 08:15:21.137
        for t in (T(3, 59), T(4, 0), T(4, 13, 17), T(4, 13, 19, us=581000)):
            self.assertEqual({s for s, _ in self.states(t).values()}, {"missing"}, t)
        for t in (T(4, 13, 20), T(4, 30), T(8, 5), T(8, 15, 21)):
            self.assertEqual(self.states(t)["24h"], ("valid-current", IDS4[1]), t)
        for t in (T(8, 15, 22), T(9, 0), T(12, 0)):
            self.assertEqual(self.states(t)["24h"], ("valid-current", IDS8[1]), t)
        self.assertNotIn("newer_pending", self.r.read(T(8, 10)))           # 08:00Z not yet registered at 08:10
        at = self.r.read(T(8, 15, 20), "24h")                       # 08:00Z registered, not yet confirmed
        self.assertEqual((at["state"], at["id"], at["newer_pending"]), ("valid-current", IDS4[1], [IDS8[1]]))

    def test_expiry_and_grace(self):
        self.assertEqual(self.r.read(T(8, 19, 59))["id"], IDS8[0])                  # 08:00Z published 08:15:21
        self.r.drop(IDS8)                                          # 08:00Z run missed: grace keeps 04:00Z current
        self.assertEqual(self.r.read(T(8, 19, 59))["state"], "valid-current")          # 04:00Z 4h window ends 08:20
        self.assertEqual((self.r.read(T(8, 20))["state"], self.r.read(T(8, 20))["reason"]), ("stale", "window ended"))
        self.assertEqual(self.r.read(T(9, 14, 59), "24h")["state"], "valid-current")
        self.assertEqual(self.r.read(T(9, 15), "24h")["state"], "stale")
        self.assertIn("expired at 2026-09-26T09:15:00Z", self.r.read(T(9, 15), "24h")["reason"])

    def test_window_may_start_after_now(self):
        x = self.r.read(T(8, 15, 22), "4h")                        # window starts 08:25, published 08:15:21
        self.assertEqual((x["state"], x["id"], x["elapsed_fraction"]), ("valid-current", IDS8[0], 0.0))
        self.assertGreater(C.ms(RR._t(x["start_utc"])), MS(T(8, 15, 22)))

    def test_revalidate_has_a_lower_bound(self):
        cached = self.r.read(T(8, 30), "4h")
        self.assertEqual(cached["id"], IDS8[0])
        self.assertEqual(RR.revalidate(cached, T(8, 10))["state"], "unavailable")     # before it existed
        self.assertEqual(RR.revalidate(cached, T(3, 0))["state"], "unavailable")      # before its decision
        self.assertEqual(RR.revalidate(cached, T(12, 24, 59))["state"], "valid-current")
        self.assertEqual(RR.revalidate(cached, T(12, 25))["state"], "stale")
        for t in (T(8, 15, 22), T(10), T(12, 24, 59), T(12, 25)):              # cached == fresh after availability
            self.assertEqual(RR.revalidate(cached, t)["state"], self.r.read(t, "4h")["state"], t)

    def test_a_third_batch_does_not_change_history(self):
        before = {t: self.states(t) for t in (T(4, 30), T(8, 5), T(8, 16), T(9, 20), T(12, 9, 2))}
        self.r.add_batch(T(12), T(12, 9), MS(T(12, 9, 1)), MS(T(12, 9, 3)))
        for t, want in before.items():
            self.assertEqual(self.states(t), want, t)
        self.assertEqual(self.states(T(12, 9, 4))["4h"], ("valid-current", "range-rc1d-4h-20260926T1200Z"))

    def test_integrity_failure_is_not_skipped(self):
        fid = IDS8[0]
        e = self.r.manifest()[fid]
        (self.r.base / e["frozen"]).write_bytes(b'{"tampered": true}')
        self.assertEqual(self.r.read(T(8, 30))["state"], "integrity-failed")         # no fallback to 04:00Z
        self.assertEqual(self.r.read(T(8, 5))["state"], "valid-current")             # did not exist yet at 08:05


@unittest.skipUnless(REPO and FX.exists(), "needs the repository and its fixture")
class TestEligibilityAndValidation(unittest.TestCase):
    """Finding 2: reader and scorer share one eligibility rule; the strict validator uses the canonical window
    and never raises on malformed types."""

    def setUp(self):
        self.r = Repo()
        self.doc = self.r.doc(IDS4[0])

    def tearDown(self):
        self.r.close()

    def score(self, now):
        import scoring
        fetch = lambda s, e: [(t, 101.0, 99.0, 100.0) for t in range(s, e, 60_000)]   # noqa: E731
        _, new, _, alerts = scoring.score_registry(self.r.base, MS(now), "test", fetch=fetch, only_prefix="range-rc1d-")
        return {x["id"]: x["status"] for x in new}, alerts

    def test_late_registration_is_ineligible_in_both(self):
        start = MS(RR._t(self.doc["start_utc"]))
        self.r.put(IDS4[0], None, {"registered": start})
        pub = next(p for p in self.r.pubs() if p["attempt"] == self.r.manifest()[IDS4[0]]["attempt"])
        self.r.put(IDS4[0], None, pub=dict(pub, confirmed=start + 1))
        x = self.r.read(T(4, 30))
        self.assertEqual((x["state"], x["reason"]), ("ineligible", "registered at or after the window start"))
        got, _ = self.score(T(12))
        self.assertEqual(got[IDS4[0]], "late registration — not scored")

    def test_late_publication_is_ineligible_in_both(self):
        start = MS(RR._t(self.doc["start_utc"]))
        pub = next(p for p in self.r.pubs() if p["attempt"] == self.r.manifest()[IDS4[0]]["attempt"])
        self.r.put(IDS4[0], None, pub=dict(pub, confirmed=start))
        self.assertEqual(self.r.read(T(4, 30))["state"], "ineligible")
        self.assertEqual(self.score(T(12))[0][IDS4[0]], "late publication — not scored")

    def test_confirmation_before_registration_is_an_integrity_failure(self):
        e = self.r.manifest()[IDS4[0]]
        pub = next(p for p in self.r.pubs() if p["attempt"] == e["attempt"])
        self.r.put(IDS4[0], None, pub=dict(pub, confirmed=e["registered"] - 1))
        x = self.r.read(T(4, 30))
        self.assertEqual(x["state"], "integrity-failed")
        self.assertIn("confirmed before the record was registered", x["reason"])
        self.assertEqual(self.score(T(12))[0][IDS4[0]], "integrity failure — not scored")

    def test_exact_window(self):
        d = dict(self.doc, id="range-rc1d-4h-20260926T0000Z", decision_utc="2026-09-26T00:00:00Z",
                 made_utc="2026-09-26T00:04:00Z", start_utc="2026-09-26T01:00:00Z", horizon_utc="2026-09-26T05:00:00Z")
        errs = C.validate_rc1d(d)
        self.assertTrue(any("not the RC1D window" in e and "00:10:00" in e for e in errs), errs)
        ok = dict(d, start_utc="2026-09-26T00:10:00Z", horizon_utc="2026-09-26T04:10:00Z")
        self.assertEqual(C.validate_rc1d(ok), [])
        late = dict(d, made_utc="2026-09-26T01:10:00Z", start_utc="2026-09-26T01:15:00Z", horizon_utc="2026-09-26T05:15:00Z")
        self.assertTrue(any("allowed 5-70" in e for e in C.validate_rc1d(late)))     # operating limit kept too

    def test_malformed_types_never_crash(self):
        for bad in ({"contract": []}, {"contract": {"a": 1}}, {"events": "x"}, {"events": [None, 3]},
                    {"reference_price": "80000"}, {"decision_utc": 5}, {"id": ["x"]}):
            errs = C.validate_rc1d(dict(self.doc, **bad), IDS4[0])
            self.assertTrue(errs, bad)
        for entry in ({"attempt": []}, {"attempt": {"x": 1}}, {"registered": "soon"}, {"registered": True},
                      {"prepared": "x"}):
            r = Repo()
            r.put(IDS4[0], None, entry)
            x = r.read(T(4, 30))
            self.assertEqual(x["state"], "integrity-failed", entry)
            import scoring
            scoring.score_registry(r.base, MS(T(12)), "test", fetch=lambda s, e: [], only_prefix="range-rc1d-")
            r.close()
        r = Repo()
        r.put(IDS4[0], dict(self.doc, contract=[]))
        self.assertEqual(r.read(T(4, 30))["state"], "integrity-failed")
        r.close()

    def test_missing_point_and_wrong_horizon(self):
        d = copy.deepcopy(self.doc)
        del d["events"][1]["point"]
        self.r.put(IDS4[0], d)
        self.assertIn("point and q10", self.r.read(T(4, 30))["reason"])
        r = Repo()
        d = dict(self.doc, horizon_utc=C.iso(RR._t(self.doc["start_utc"]) + dt.timedelta(hours=24)))
        r.put(IDS4[0], d)
        self.assertIn("not 4h", r.read(T(4, 30))["reason"])
        r.close()

    def test_future_availability(self):
        e = self.r.manifest()[IDS4[0]]
        self.r.put(IDS4[0], None, {"registered": MS(T(4, 50))})                  # registered after the window start
        pub = next(p for p in self.r.pubs() if p["attempt"] == e["attempt"])
        self.r.put(IDS4[0], None, pub=dict(pub, confirmed=MS(T(4, 50, 2))))
        self.assertEqual(self.r.read(T(4, 30))["state"], "missing")               # did not exist at 04:30
        self.assertEqual(self.r.read(T(5))["state"], "ineligible")                # exists, late
        self.assertEqual(e["attempt"], self.r.manifest()[IDS4[0]]["attempt"])

    def test_point_and_quantiles_stay_distinct(self):
        x = self.r.read(T(4, 30))
        b2 = next(e for e in self.doc["events"] if e["name"].startswith("B2"))
        self.assertEqual((x["point_lr"], x["q_lr"]), (b2["point"], [b2["q10"], b2["q50"], b2["q90"]]))
        self.assertNotEqual(x["point_lr"], x["q_lr"][1])

    def test_legacy_records_unchanged(self):
        m = self.r.manifest()
        m["range-b2-4h-20260926T0000Z"] = {"sha256": "0" * 64}
        (self.r.base / "state/forecast_manifest.json").write_text(json.dumps(m))
        self.assertIn("legacy 2.14 records exist", self.r.read(T(3, 0))["reason"])


@unittest.skipUnless(REPO and FX.exists(), "needs the repository and its fixture")
class TestProductionCompatibility(unittest.TestCase):
    """ID by ID: the fixture's bytes are the production registry's, and every production RC1D record replays
    (bytes never rewritten). Skips outside a repository checkout that has the records."""

    def test_fixture_matches_production_and_replays(self):
        base = DESK.parent
        prod = json.loads((base / "state/forecast_manifest.json").read_text())
        fx = json.loads((FX / "state/forecast_manifest.json").read_text())
        if not all(i in prod for i in fx):
            self.skipTest("checkout without the Sep 26 production records")
        for fid, e in fx.items():
            self.assertEqual(prod[fid], e, fid)
            self.assertEqual(hashlib.sha256((base / e["frozen"]).read_bytes()).hexdigest(), e["sha256"])
            self.assertEqual((base / e["frozen"]).read_bytes(), (FX / e["frozen"]).read_bytes())

    def test_every_production_record_validates_and_replays(self):
        import range_job as J
        base = DESK.parent
        prod = json.loads((base / "state/forecast_manifest.json").read_text())
        ids = sorted(i for i in prod if i.startswith("range-rc1d-"))
        if not ids:
            self.skipTest("no production RC1D records")
        for fid in ids:
            before = (base / prod[fid]["frozen"]).read_bytes()
            self.assertEqual(C.validate_rc1d(json.loads(before), fid, prod[fid]), [], fid)
            self.assertEqual(J.replay(fid, base=base)["id"], fid)
            self.assertEqual((base / prod[fid]["frozen"]).read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=1)
