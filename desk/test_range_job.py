#!/usr/bin/env python3
"""Offline tests for range_job (crypto-desk 11.2). Uses the repository's own schema.py and
registration.py against a temporary directory, so registration semantics are the real ones."""
import datetime as dt
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

import range_job as J                     # noqa: E402
import range_model as R                   # noqa: E402
from test_range_model import synth_bars   # noqa: E402
from registration import register         # noqa: E402
from schema import validate               # noqa: E402

UTC = dt.timezone.utc


def dvol_rows(bars, level=40.0):
    t0, t1 = R._t(bars[0]["open_utc"]), R._t(bars[-1]["close_utc"])
    out, t = [], t0
    while t < t1:
        out.append({"open_utc": R._iso(t), "available_at_utc": R._iso(t + dt.timedelta(hours=1)), "dvol": level})
        t += dt.timedelta(hours=1)
    return out


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "registry").mkdir()
        (self.tmp / "state").mkdir()
        # 2,400 synthetic bars ending at the 2026-09-26 00:00Z close
        n = 2400
        start = dt.datetime(2026, 9, 26, tzinfo=UTC) - dt.timedelta(hours=4 * n)
        self.bars = synth_bars(n, 21, 0.95, start=start)
        self.dvol = dvol_rows(self.bars)
        self.m0 = dt.datetime(2026, 9, 1, tzinfo=UTC)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def fit(self):
        hist = [b for b in self.bars if R._t(b["open_utc"]) < self.m0]
        return J.refit(self.m0 + dt.timedelta(days=3), base=self.tmp, history=(hist, self.dvol))


class TestSpec(Base):
    def test_model_file_is_the_frozen_spec(self):
        self.assertTrue(J.spec_ok())
        self.assertEqual(hashlib.sha256((DESK / "range_model.py").read_bytes()).hexdigest(), J.FROZEN_SPEC)


class TestRefit(Base):
    def test_refit_writes_once(self):
        p = self.fit()
        doc = json.loads(p.read_text())
        self.assertEqual((doc["month"], doc["spec_sha256"]), ("2026-09", J.FROZEN_SPEC))
        self.assertEqual(set(doc["fits"]), {"4h", "24h", "72h"})
        mtime = p.stat().st_mtime_ns
        self.fit()
        self.assertEqual(p.stat().st_mtime_ns, mtime)          # existing month file is never rewritten

    def test_refit_refuses_gap_to_month_start(self):
        hist = [b for b in self.bars if R._t(b["open_utc"]) < self.m0 - dt.timedelta(days=1)]
        with self.assertRaises(RuntimeError):
            J.refit(self.m0 + dt.timedelta(days=3), base=self.tmp, history=(hist, self.dvol))


class TestForecast(Base):
    now = dt.datetime(2026, 9, 26, 0, 7, tzinfo=UTC)          # 7 minutes after the close

    def clock(self):
        return int(self.now.timestamp() * 1000) + 5_000

    def test_three_valid_forecasts_registered_before_start(self):
        self.fit()
        docs, written = J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                                   register_fn=register, validate_fn=validate, clock=self.clock)
        self.assertEqual(len(written), 3)
        manifest = json.loads((self.tmp / "state/forecast_manifest.json").read_text())
        for doc in docs:
            self.assertEqual(validate(doc, self.clock()), [])
            entry = manifest[doc["id"]]
            self.assertLess(entry["registered"], R._t(doc["start_utc"]).timestamp() * 1000)
            names = [e["name"].split(" ")[0] for e in doc["events"]]
            self.assertEqual(names, ["B2", "B0"])
            for ev in doc["events"]:
                self.assertTrue(0 < ev["q10"] <= ev["q50"] <= ev["q90"] < 1)
        self.assertEqual(docs[0]["start_utc"], "2026-09-26T00:10:00Z")
        self.assertEqual(docs[2]["horizon_utc"], "2026-09-29T00:10:00Z")

    def test_idempotent(self):
        self.fit()
        J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                   register_fn=register, validate_fn=validate, clock=self.clock)
        _, written = J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                                register_fn=register, validate_fn=validate, clock=self.clock)
        self.assertEqual(written, [])

    def test_stale_decision_refused(self):
        self.fit()
        with self.assertRaises(J.StaleDecision):
            J.forecast(self.now + dt.timedelta(hours=1, minutes=5), base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                       register_fn=register, validate_fn=validate, clock=self.clock)

    def test_missing_fit_refused(self):
        with self.assertRaises(RuntimeError):
            J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                       register_fn=register, validate_fn=validate, clock=self.clock)

    def test_late_registration_aborts(self):
        self.fit()
        late = lambda: int(dt.datetime(2026, 9, 26, 0, 30, tzinfo=UTC).timestamp() * 1000)
        with self.assertRaises(RuntimeError):
            J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                       register_fn=register, validate_fn=validate, clock=late)

    def test_forecast_uses_only_closed_bars(self):
        self.fit()
        a, _ = J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=self.dvol,
                          register_fn=lambda b, n: ([], []), validate_fn=validate, clock=self.clock)
        shutil.rmtree(self.tmp / "registry"); (self.tmp / "registry").mkdir()
        dv = [r for r in self.dvol] + [{"open_utc": "2026-09-26T00:00:00Z", "available_at_utc": "2026-09-26T01:00:00Z",
                                         "dvol": 99.0}]                    # a candle not yet closed at the decision
        b, _ = J.forecast(self.now, base=self.tmp, bars=self.bars[-400:], dvol=dv,
                          register_fn=lambda b, n: ([], []), validate_fn=validate, clock=self.clock)
        self.assertEqual([d["events"] for d in a], [d["events"] for d in b])


class TestSummary(Base):
    def test_skill_and_coverage(self):
        rows = []
        for i, (e2, e0) in enumerate([(0.2, 0.3), (0.4, 0.5)]):
            rows.append({"id": f"range-b2-4h-2026092{i}T0000Z", "status": "scored", "events": [
                {"name": "B2 range model", "type": "range", "abs_error_log_lr": e2, "covered_80": True},
                {"name": "B0 persistence baseline", "type": "range", "abs_error_log_lr": e0, "covered_80": i == 0}]})
        rows.append({"id": "range-b2-24h-20260921T0000Z", "status": "late registration — not scored"})
        rows.append({"id": "someone-else", "status": "scored", "events": []})
        (self.tmp / "registry/scores.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        s = J.summary(base=self.tmp)
        self.assertEqual(s["4h"]["scored"], 2); self.assertEqual(s["24h"]["late"], 1)
        text = (self.tmp / "reports/range.md").read_text()
        self.assertIn("| 4h | 2 | 0 / 0 | 0.3000 | 0.4000 | 25.0% | 100% | 50% |", text)


if __name__ == "__main__":
    unittest.main(verbosity=1)
