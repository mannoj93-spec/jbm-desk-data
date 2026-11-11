"""Daily files for the Binance 5-minute series from 2026-12-01 (collector.series_partition, repo 2.30.11)."""
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import collector
import schema
import storage
from lab.data import Store

M5 = 5 * schema.MINUTE
H = schema.H
CUT = schema.ms("2026-12-01T00:00:00Z")
NAME = "binance_topLongShortPositionRatio_5m"


def setUpModule():
    collector.DEADLINE = time.monotonic() + collector.RUN_BUDGET_S      # a fresh run budget (see test_rev22)


def fake_binance(stamps, step):
    def get(url, **_):
        end = int(url.split("endTime=")[1])
        return [{"timestamp": t, "buySellRatio": "1"} for t in stamps if t <= end][-500:], None
    return get


class Partition(unittest.TestCase):
    def test_cutover_is_the_december_month_start(self):
        self.assertEqual(collector.SERIES_DAILY_FROM_MS, CUT)
        self.assertEqual(collector.month(CUT - 1), "2026-11")
        self.assertEqual(collector.day(CUT), "2026-12-01")

    def test_only_five_minute_series_change_and_only_from_the_cutover(self):
        p = collector.series_partition(NAME)
        self.assertEqual([p(CUT - M5), p(CUT), p(CUT + 26 * H), p(schema.ms("2027-01-01T00:00:00Z"))],
                         ["2026-11", "2026-12-01", "2026-12-02", "2027-01-01"])
        self.assertEqual(p(schema.ms("2026-09-25T00:00:00Z")), "2026-09")            # a backfill of old rows stays monthly
        for hourly in ("binance_topLongShortPositionRatio_1h", "okx_mark_1h", "binance_funding_settled", "deribit_dvol_1h"):
            q = collector.series_partition(hourly)
            self.assertIs(q, collector.month)
            self.assertEqual(q(CUT + H), "2026-12")

    def test_every_daily_name_sorts_after_every_monthly_name(self):
        names = ["2026-09.jsonl", "2026-10.jsonl", "2026-11.jsonl", "2026-12-01.jsonl", "2026-12-31.jsonl", "2027-01-01.jsonl"]
        self.assertEqual(sorted(names), names)
        # the reason the switch is on a month boundary: inside a month a daily name sorts BEFORE the monthly one
        self.assertLess("2026-11-12.jsonl", "2026-11.jsonl")


class Collection(unittest.TestCase):
    def collect(self, tmp, stamps, nows):
        ck = None
        for now in nows:
            with patch.object(collector, "BASE", tmp), patch.object(collector, "NOW", now), \
                 patch.object(collector, "get", side_effect=fake_binance([t for t in stamps if t <= now], M5)):
                rows, err, _ = collector.binance_futures_data(NAME, "x", "5m", ["buySellRatio"], ck)
                self.assertIsNone(err)
                if rows:
                    collector.append_rows(f"series/{NAME}", rows, partition=collector.series_partition(NAME))
                    ck = rows[-1]["t"]

    def test_routine_runs_across_the_boundary_store_every_stamp_once(self):
        first = CUT - 3 * H
        stamps = [first + i * M5 for i in range(6 * 12 + 1)]                       # 21:00 Nov 30 to 03:00 Dec 1
        nows = [first + 20 * schema.MINUTE + k * 15 * schema.MINUTE for k in range(24)]
        with tempfile.TemporaryDirectory() as tmp:
            self.collect(tmp, stamps, nows)
            self.collect(tmp, stamps, nows[-3:])                                   # a repeated run adds nothing
            folder = Path(tmp) / "data/series" / NAME
            self.assertEqual(sorted(p.name for p in folder.glob("*.jsonl")), ["2026-11.jsonl", "2026-12-01.jsonl"])
            nov = [r["t"] for r in storage.read_rows(folder / "2026-11.jsonl")]
            dec = [r["t"] for r in storage.read_rows(folder / "2026-12-01.jsonl")]
            self.assertEqual(nov, list(range(first, CUT, M5)))                     # nothing at or after the cutover
            self.assertEqual(dec[0], CUT)
            self.assertEqual(dec, list(range(CUT, dec[-1] + M5, M5)))
            # the reader every study uses sees one continuous series, each stamp once, in time order
            got = [r["t"] for r in Store(tmp, cutoff=nows[-1] + H).series(NAME)]
            self.assertEqual(got, nov + dec)
            self.assertEqual(len(got), len(set(got)))
            row = storage.read_rows(folder / "2026-12-01.jsonl")[0]
            self.assertEqual(sorted(row), ["code_commit", "code_version", "f", "observed_at", "r", "t"])   # row content unchanged

    def test_a_backfill_spanning_the_boundary_splits_by_stamp(self):
        first = CUT - 2 * 24 * H
        stamps = [first + i * M5 for i in range(4 * 288)]                          # Nov 29 to Dec 2
        with tempfile.TemporaryDirectory() as tmp:
            self.collect(tmp, stamps, [stamps[-1] + 10 * schema.MINUTE])
            folder = Path(tmp) / "data/series" / NAME
            self.assertEqual(sorted(p.name for p in folder.glob("*.jsonl")),
                             ["2026-11.jsonl", "2026-12-01.jsonl", "2026-12-02.jsonl"])
            counts = {p.name: len(storage.read_rows(p)) for p in folder.glob("*.jsonl")}
            self.assertEqual(counts["2026-12-01.jsonl"], 288)
            self.assertEqual(sum(counts.values()), len(stamps))

    def test_the_collector_calls_the_partition_for_the_binance_series(self):
        src = Path(collector.__file__).read_text()
        self.assertEqual(src.count('append_rows(f"series/{name}", rows, partition=series_partition(name))'), 1)


if __name__ == "__main__":
    unittest.main()
