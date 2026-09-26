#!/usr/bin/env python3
"""Fixtures for jbm_archive (package 11.0). Offline; stdlib unittest.

Sources: the original twelve archive-10.0.0 fixtures (values pulled Sep 22 2026 from
data.binance.vision, the live futures/data API and aggTrades), kept and renamed to the 11.0 time
fields; regression probes for every defect found in the Sep 25 audit; and captured provider bytes
(fixtures/*.zip.b64 — the provider zips base64-encoded, because a skill upload may not contain nested zips —
with the provider's .CHECKSUM, downloaded Sep 25 2026; the decoded bytes must match that checksum).
Run: PYTHONDONTWRITEBYTECODE=1 python3 test_jbm_archive.py
"""
import base64
import csv
import datetime as dt
import hashlib
import io
import os
import unittest
import urllib.error
import zipfile

import jbm_archive as A

HERE = os.path.dirname(os.path.abspath(__file__))
UTC = dt.timezone.utc
D = dt.date(2026, 9, 20)
HDR = ("create_time,symbol,sum_open_interest,sum_open_interest_value,count_toptrader_long_short_ratio,"
       "sum_toptrader_long_short_ratio,count_long_short_ratio,sum_taker_long_short_vol_ratio")
ROW_1200 = ("2026-09-20 12:00:00,BTCUSDT,108964.5470000000000000,8765498266.0102330000000000,"
            "1.10714348,2.17215600,0.95769369,0.54288100")
ROW_1155 = ("2026-09-20 11:55:00,BTCUSDT,108940.7550000000000000,8764109434.5420000000000000,"
            "1.10778830,2.17343500,0.95793106,0.58032100")


def rows_from(text):
    return list(csv.DictReader(io.StringIO(text)))


def zip_of(text, name="x.csv"):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr(name, text)
    return b.getvalue()


def serve(text, headers=None, checksum="auto"):
    """Offline opener: the zip for the data URL, its sha256 for .CHECKSUM (or a supplied value)."""
    blob = zip_of(text)

    def opener(url):
        if url.endswith(".CHECKSUM"):
            if checksum is None:
                raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
            h = hashlib.sha256(blob).hexdigest() if checksum == "auto" else checksum
            return (h + "  f.zip\n").encode(), {}
        return blob, (headers or {})
    return opener


def day_text(day=D, step=5, oi="100", ratio="1.5", n=288, offset=0, symbol="BTCUSDT"):
    base = dt.datetime.combine(day, dt.time()) + dt.timedelta(minutes=offset)
    return HDR + "\n" + "\n".join(
        f"{(base + dt.timedelta(minutes=step * i)):%Y-%m-%d %H:%M:%S},{symbol},{oi},1000,{ratio},{ratio},{ratio},{ratio}"
        for i in range(n)) + "\n"


DEPTH_HDR = "timestamp,percentage,depth,notional\n"
BANDS = ("-5.00", "-4.00", "-3.00", "-2.00", "-1.00", "-0.20", "0.20", "1.00", "2.00", "3.00", "4.00", "5.00")


def depth_text(day=D, every_s=30, n=2880, bands=BANDS):
    lines = []
    base = dt.datetime.combine(day, dt.time()) + dt.timedelta(seconds=4)
    for i in range(n):
        t = base + dt.timedelta(seconds=every_s * i)
        for b in bands:
            d = 1000 + 100 * abs(float(b))
            lines.append(f"{t:%Y-%m-%d %H:%M:%S},{b},{d:.3f},{d * 80000:.2f}")
    return DEPTH_HDR + "\n".join(lines) + "\n"


# ---------------------------------------------------------------- the original twelve, 11.0 field names
class TestKnowledgeTime(unittest.TestCase):
    def test_offset_fixture_oi_and_shares(self):
        st, out, rep = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n"), D)
        r = out[0]
        self.assertEqual(r["archive_stamp_utc"], "2026-09-20T12:00:00Z")
        self.assertEqual(r["aligned_at_utc"], "2026-09-20T12:05:00Z")          # = live API stamp
        self.assertAlmostEqual(r["oi_btc"], 108964.547, places=6)
        self.assertAlmostEqual(r["top_account"], 1.10714348, places=8)
        self.assertAlmostEqual(0.5254 / 0.4746, 1.1070, delta=6e-5)
        self.assertGreater(abs(r["top_account"] - 1.1070), 6e-5)                # why reconciliation runs on shares
        self.assertAlmostEqual(r["top_notional"], 2.1722, delta=6e-5)
        self.assertAlmostEqual(r["global_account"], 0.9577, delta=6e-5)
        self.assertAlmostEqual(r["top_account_share"], 0.5254, delta=6e-5)
        self.assertAlmostEqual(r["top_notional_share"], 0.6848, delta=6e-5)
        self.assertAlmostEqual(r["global_account_share"], 0.4892, delta=6e-5)

    def test_taker_window_fixture(self):
        _, out, _ = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n"), D)
        self.assertAlmostEqual(out[0]["taker_buy"], 65.396 / 120.459, delta=6e-5)
        self.assertEqual(out[0]["aligned_at_utc"], "2026-09-20T12:05:00Z")      # window closes at 12:05

    def test_reconcile_uses_shift_for_oi_not_taker(self):
        _, out, _ = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1155 + "\n" + ROW_1200 + "\n"), D)
        api = {"oi_btc": {"2026-09-20T12:00:00Z": 108940.755, "2026-09-20T12:05:00Z": 108964.547},
               "top_notional_share": {"2026-09-20T12:05:00Z": 0.6848},
               "top_account_share": {"2026-09-20T12:00:00Z": 0.5256, "2026-09-20T12:05:00Z": 0.5254},
               "taker_buy": {"2026-09-20T12:00:00Z": 0.5429}}
        res = A.reconcile(out, api)
        self.assertEqual(res["oi_btc"]["within_tol"], 2)
        self.assertEqual(res["top_notional_share"]["within_tol"], 1)
        self.assertEqual(res["top_account_share"]["within_tol"], 2)
        self.assertEqual(res["taker_buy"]["within_tol"], 1)


class TestDedupe(unittest.TestCase):
    def test_exact_duplicates_dropped(self):
        _, out, rep = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n" + ROW_1200 + "\n"), D)
        self.assertEqual(len(out), 1)
        self.assertEqual(rep["exact_duplicates_dropped"], 1)

    def test_conflicting_duplicates_excluded_not_averaged(self):
        bad = ROW_1200.replace("0.54288100", "0.99999999")
        st, out, rep = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n" + bad + "\n" + ROW_1155 + "\n"), D)
        self.assertEqual([r["archive_stamp_utc"] for r in out], ["2026-09-20T11:55:00Z"])
        self.assertEqual(rep["conflicting_stamps_excluded"], ["2026-09-20T12:00:00Z"])
        self.assertEqual(st, "incomplete")

    def test_sorted_output(self):
        _, out, _ = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n" + ROW_1155 + "\n"), D)
        self.assertEqual(out[0]["archive_stamp_utc"], "2026-09-20T11:55:00Z")


class TestStates(unittest.TestCase):
    def test_missing_is_a_state_not_empty(self):
        def opener(u):
            raise urllib.error.HTTPError(u, 404, "Not Found", {}, None)
        st, rows, _ = A.load_metrics(dt.date(2024, 8, 31), opener=opener)
        self.assertEqual((st, rows), ("missing", []))
        self.assertEqual(A.load_metrics(dt.date(2020, 8, 31), opener=opener)[0], "missing")  # before first day

    def test_incomplete_day_flagged(self):
        st, _, _ = A.load_metrics(D, opener=serve(HDR + "\n" + ROW_1200 + "\n"))
        self.assertEqual(st, "incomplete")

    def test_other_failure_is_retrieval_error(self):
        def opener(u):
            raise TimeoutError("timed out")
        self.assertEqual(A.load_metrics(D, opener=opener)[0], "retrieval_error")


class TestShares(unittest.TestCase):
    def test_share_from_ratio(self):
        self.assertAlmostEqual(A.share_from_ratio(1.5), 0.6)


class TestBookDepthRows(unittest.TestCase):
    def test_bookdepth_rows(self):
        st, out, _ = A.inspect_bookdepth(rows_from(depth_text(n=1)), D)
        self.assertEqual(out[0]["available_at_utc"], "2026-09-20T00:00:04Z")
        self.assertEqual(sorted({r["band_pct"] for r in out}), sorted(A.DEPTH_BANDS))
        self.assertEqual(st, "incomplete")                                     # one snapshot is not a day


class TestVersion(unittest.TestCase):
    def test_version_string(self):
        self.assertEqual(A.VERSION, "archive-12.0.0")
        self.assertEqual(A.FIRST_DAY["metrics"], dt.date(2020, 9, 1))
        self.assertEqual(A.FIRST_DAY["bookDepth"], dt.date(2023, 1, 1))


# ---------------------------------------------------------------- Sep 25 audit regressions
class TestAuditRegressions(unittest.TestCase):
    def test_clean_day_is_ok(self):
        st, rows, rep = A.load_metrics(D, opener=serve(day_text()))
        self.assertEqual((st, len(rows), rep["missing_slots"]), ("ok", 288, 0))
        self.assertEqual(rep["prov"]["checksum_status"], "match")

    def test_wrong_date_is_malformed(self):
        st, rows, rep = A.load_metrics(D, opener=serve(day_text(day=dt.date(2026, 9, 19))))
        self.assertEqual(st, "malformed"); self.assertEqual(rows, [])
        self.assertEqual(rep["malformed_rows"], {"wrong_date": 288})

    def test_off_grid_is_malformed(self):
        st, _, rep = A.load_metrics(D, opener=serve(day_text(offset=2)))
        self.assertEqual(st, "malformed"); self.assertEqual(rep["malformed_rows"]["off_grid"], 288)

    def test_wrong_symbol_is_malformed(self):
        st, _, rep = A.load_metrics(D, opener=serve(day_text(symbol="ETHUSDT")))
        self.assertEqual(st, "malformed"); self.assertEqual(rep["malformed_rows"]["wrong_symbol"], 288)

    def test_empty_oi_is_missing_not_ok(self):
        st, rows, rep = A.load_metrics(D, opener=serve(day_text(oi="")))
        self.assertEqual(st, "incomplete"); self.assertEqual(rep["missing_values"]["oi_btc"], 288)
        self.assertIsNone(rows[0]["oi_btc"]); self.assertIn("missing:oi_btc", rows[0]["flags"])

    def test_nan_and_inf_are_malformed(self):
        for bad in ("nan", "inf", "-inf", "NaN"):
            st, _, rep = A.load_metrics(D, opener=serve(day_text(oi=bad)))
            self.assertEqual(st, "malformed", bad)

    def test_negative_ratio_is_malformed_not_a_200pct_share(self):
        for bad in ("-2", "-1"):
            st, rows, rep = A.load_metrics(D, opener=serve(day_text(ratio=bad)))
            self.assertEqual(st, "malformed"); self.assertEqual(rows, [])

    def test_unparseable_number_is_a_state_not_an_exception(self):
        st, _, rep = A.load_metrics(D, opener=serve(day_text(oi="abc")))
        self.assertEqual(st, "malformed")
        self.assertEqual(rep["malformed_rows"], {"sum_open_interest:unparseable": 288})

    def test_legitimate_zero_preserved(self):
        st, rows, _ = A.load_metrics(D, opener=serve(day_text(ratio="0", oi="0")))
        self.assertEqual(st, "ok"); self.assertEqual(rows[0]["taker_buy_share"], 0.0)
        self.assertEqual(rows[0]["oi_btc"], 0.0)

    def test_schema_missing_column(self):
        st, rows, rep = A.load_metrics(D, opener=serve("create_time,symbol,sum_open_interest\n2026-09-20 00:00:00,BTCUSDT,1\n"))
        self.assertEqual(st, "malformed"); self.assertTrue(rep["flags"][0].startswith("schema_missing"))

    def test_survey_uses_the_same_validation(self):
        res = A.survey("metrics", D, D, opener=serve(day_text(n=1)))
        self.assertEqual((res[0]["state"], res[0]["missing_slots"]), ("incomplete", 287))
        res = A.survey("metrics", D, D, opener=serve(day_text(oi="nan")))
        self.assertEqual(res[0]["state"], "malformed")

    def test_empty_bookdepth_is_incomplete(self):
        st, rows, rep = A.load_bookdepth(D, opener=serve(DEPTH_HDR))
        self.assertEqual((st, rows), ("incomplete", [])); self.assertIn("no_rows", rep["flags"])

    def test_single_band_bookdepth_is_incomplete(self):
        st, rows, rep = A.load_bookdepth(D, opener=serve(depth_text(n=2880, bands=("-1.00",))))
        self.assertEqual(st, "incomplete"); self.assertEqual(rep["complete_snapshots"], 0)

    def test_full_bookdepth_day_is_ok(self):
        st, rows, rep = A.load_bookdepth(D, opener=serve(depth_text()))
        self.assertEqual(st, "ok"); self.assertEqual(rep["buckets_covered"], 288)
        self.assertEqual(rep["max_gap_s"], 30.0)

    def test_bookdepth_coverage_gap_is_incomplete(self):
        st, _, rep = A.load_bookdepth(D, opener=serve(depth_text(n=2000)))    # stops ~16:40Z
        self.assertEqual(st, "incomplete"); self.assertLess(rep["buckets_covered"], 288)

    def test_bookdepth_non_monotone_is_malformed(self):
        text = depth_text(n=1).replace(",-2.00,1200.000", ",-2.00,900.000")
        st, _, rep = A.inspect_bookdepth(rows_from(text), D)
        self.assertEqual(st, "malformed"); self.assertEqual(rep["non_monotone_snapshots"], 1)

    def test_bookdepth_ten_band_layout_with_integer_labels(self):
        # the 2023-01-01 provider file carries ten bands (no +/-0.2) and writes "-5" where 2026 writes "-5.00"
        text = depth_text(n=2880, bands=("-5", "-4", "-3", "-2", "-1", "1", "2", "3", "4", "5"))
        st, rows, rep = A.inspect_bookdepth(rows_from(text), D)
        self.assertEqual((st, rep["complete_snapshots"], rep["band_layouts"]), ("ok", 2880, {"10band": 2880}))

    def test_bookdepth_mixed_layouts_flagged(self):
        text = depth_text(n=1440) + depth_text(n=1440, bands=BANDS[:5] + BANDS[7:]).split("\n", 1)[1]
        text = text.replace("2026-09-20 00:", "2026-09-20 00:", 1)
        rows = rows_from(text)
        # shift the second half into the afternoon so snapshots do not collide
        for r in rows[1440 * 12:]:
            t = dt.datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S") + dt.timedelta(hours=12)
            r["timestamp"] = t.strftime("%Y-%m-%d %H:%M:%S")
        st, _, rep = A.inspect_bookdepth(rows, D)
        self.assertIn("mixed_band_layouts", rep["flags"]); self.assertEqual(st, "incomplete")


class TestProvenanceAndAvailability(unittest.TestCase):
    def test_checksum_mismatch_is_retrieval_error(self):
        st, _, rep = A.load_metrics(D, opener=serve(day_text(), checksum="0" * 64))
        self.assertEqual(st, "retrieval_error"); self.assertEqual(rep["prov"]["checksum_status"], "mismatch")

    def test_checksum_unavailable_is_recorded_not_fatal(self):
        st, _, rep = A.load_metrics(D, opener=serve(day_text(), checksum=None))
        self.assertEqual(st, "ok"); self.assertEqual(rep["prov"]["checksum_status"], "unavailable")

    def test_provenance_fields(self):
        st, rows, rep = A.load_metrics(D, opener=serve(day_text(), headers={"Last-Modified": "Mon, 21 Sep 2026 07:05:56 GMT", "ETag": '"x"'}))
        p = rep["prov"]
        for k in ("url", "retrieved_at_utc", "sha256", "provider_sha256", "code_version", "last_modified"):
            self.assertTrue(p[k], k)
        self.assertEqual(rows[0]["source_sha256"], p["sha256"])
        m = A.manifest_entry(st, rep)
        self.assertEqual((m["state"], m["code_version"]), ("ok", "archive-12.0.0"))

    def test_pinned_bytes_detect_revision(self):
        st, _, rep = A.load_metrics(D, opener=serve(day_text()))
        pin = A.manifest_entry(st, rep)
        self.assertEqual(A.load_metrics(D, opener=serve(day_text()), pin=pin)[0], "ok")
        st2, rows2, rep2 = A.load_metrics(D, opener=serve(day_text(oi="101")), pin=pin)
        self.assertEqual(st2, "revised"); self.assertEqual(rep2["prov"]["pin_status"], "revised")

    def test_four_times_are_distinct(self):
        _, out, _ = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n"), D)
        r = out[0]
        self.assertEqual((r["archive_stamp_utc"], r["aligned_at_utc"], r["available_at_utc"]),
                         ("2026-09-20T12:00:00Z", "2026-09-20T12:05:00Z", "2026-09-20T12:10:00Z"))
        self.assertIn("assumed", r["availability_basis"])

    def test_as_of_filters_on_availability_not_stamp(self):
        _, out, _ = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1155 + "\n" + ROW_1200 + "\n"), D)
        at = lambda s: dt.datetime.fromisoformat(s).replace(tzinfo=UTC)
        self.assertEqual(len(A.as_of(out, at("2026-09-20T12:05:00"))), 1)      # 11:55 row only
        self.assertEqual(len(A.as_of(out, at("2026-09-20T12:10:00"))), 2)
        self.assertEqual(len(A.as_of(out, at("2026-09-20T12:05:00"), basis="aligned_at_utc")), 2)
        with self.assertRaises(ValueError):
            A.as_of(out, at("2026-09-20T12:05:00"), basis="archive_stamp_utc")
        with self.assertRaises(ValueError):
            A.as_of(out, dt.datetime(2026, 9, 20, 12, 5))

    def test_allowance_is_a_parameter(self):
        _, out, _ = A.inspect_metrics(rows_from(HDR + "\n" + ROW_1200 + "\n"), D, allowance=dt.timedelta(0))
        self.assertEqual(out[0]["available_at_utc"], out[0]["aligned_at_utc"])


class TestCapturedBytes(unittest.TestCase):
    """Provider bytes downloaded Sep 25 2026 with their published sha256."""

    def opener_for(self, day):
        base = os.path.join(HERE, "fixtures", f"BTCUSDT-metrics-{day}.zip")

        def opener(url):
            if url.endswith(".CHECKSUM"):
                with open(base + ".CHECKSUM", "rb") as f:
                    return f.read(), {}
            with open(base + ".b64", "rb") as f:
                return base64.b64decode(f.read()), {}
        return opener

    def test_2026_09_20_ok_and_matches_fixture_row(self):
        st, rows, rep = A.load_metrics(D, opener=self.opener_for("2026-09-20"))
        self.assertEqual((st, len(rows), rep["prov"]["checksum_status"]), ("ok", 288, "match"))
        r = [x for x in rows if x["archive_stamp_utc"] == "2026-09-20T12:00:00Z"][0]
        self.assertAlmostEqual(r["oi_btc"], 108964.547, places=6)

    def test_2020_09_01_exact_duplicates(self):
        st, rows, rep = A.load_metrics(dt.date(2020, 9, 1), opener=self.opener_for("2020-09-01"))
        self.assertEqual((st, rep["raw_rows"], len(rows), rep["exact_duplicates_dropped"]), ("ok", 576, 288, 288))
        self.assertEqual(rep["conflicting_stamps_excluded"], [])


class TestKlinesAndDvol(unittest.TestCase):
    """11.1: 4H klines (monthly and daily files; headerless and header) and hourly DVOL."""
    H = ",".join(A.KLINE_COLS)

    def day_text(self, header=True, n=6, day=D, bad=None):
        base = int(dt.datetime.combine(day, dt.time(), tzinfo=UTC).timestamp() * 1000)
        lines = [self.H] if header else []
        for i in range(n):
            o = base + i * 14_400_000
            row = [str(o), "100", "101", "99", "100.5", "10", str(o + 14_399_999), "1000", "5", "4", "400", "0"]
            if bad and i == 0:
                row = bad(row)
            lines.append(",".join(row))
        return "\n".join(lines) + "\n"

    def _serve(self, text):
        blob = zip_of(text)
        return lambda u: ((hashlib.sha256(blob).hexdigest() + "  x\n").encode(), {}) if u.endswith(".CHECKSUM") else (blob, {})

    def test_header_and_headerless_both_parse(self):
        for header in (True, False):
            st, rows, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(header=header)))
            self.assertEqual((st, len(rows)), ("ok", 6), header)
            self.assertEqual(rows[0]["available_at_utc"], "2026-09-20T04:00:00Z")   # a bar is known at its close

    def test_missing_bar_incomplete(self):
        st, rows, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(n=5)))
        self.assertEqual((st, rep["missing_bars"]), ("incomplete", 1))

    def test_ohlc_inconsistent_malformed(self):
        st, _, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(bad=lambda r: r[:2] + ["99.5"] + r[3:])))
        self.assertEqual(st, "malformed"); self.assertIn("ohlc_inconsistent", rep["malformed_rows"])

    def test_off_grid_and_bad_close_time(self):
        st, _, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(bad=lambda r: [str(int(r[0]) + 60000)] + r[1:])))
        self.assertEqual(st, "malformed"); self.assertIn("off_grid", rep["malformed_rows"])
        st, _, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(bad=lambda r: r[:6] + [str(int(r[6]) + 1)] + r[7:])))
        self.assertIn("bad_close_time", rep["malformed_rows"])

    def test_wrong_day_is_malformed(self):
        st, _, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(day=dt.date(2026, 9, 19))))
        self.assertEqual(st, "malformed"); self.assertEqual(rep["malformed_rows"]["outside_window"], 6)

    def test_microsecond_stamps_flagged(self):
        def us(r):
            return [str(int(r[0]) * 1000)] + r[1:6] + [str(int(r[6]) * 1000 + 999)] + r[7:]
        st, rows, rep = A.load_klines(D.isoformat(), opener=self._serve(self.day_text(bad=us)))
        self.assertIn("microsecond_stamps", rep["flags"]); self.assertEqual(st, "ok")

    def test_month_before_first_is_missing(self):
        self.assertEqual(A.load_klines("2019-12")[0], "missing")

    def test_dvol_paging_and_missing_hour(self):
        import json as J
        start = dt.datetime(2026, 9, 20, tzinfo=UTC)

        def opener(url):
            q = dict(kv.split("=") for kv in url.split("?")[1].split("&"))
            s, e = int(q["start_timestamp"]), int(q["end_timestamp"])
            data = [[ts, 40, 41, 39, 40.0 + (ts - s) / 3.6e9] for ts in range(s, e + 1, 3_600_000)
                    if ts != int(start.timestamp() * 1000) + 5 * 3_600_000]
            return J.dumps({"result": {"data": data}}).encode(), {}
        st, rows, rep = A.load_dvol(start, start + dt.timedelta(hours=30), opener=opener, window_h=10)
        self.assertEqual((st, rep["missing_hours"], len(rep["requests"])), ("incomplete", 1, 3))
        self.assertEqual(rows[0]["available_at_utc"], "2026-09-20T01:00:00Z")     # admitted at candle close


# ---------------------------------------------------------------- 12.0 audit regressions
class TestAudit12(unittest.TestCase):
    start = dt.datetime(2026, 9, 1, tzinfo=UTC)

    def _dvol(self, data):
        import json as J
        return A.load_dvol(self.start, self.start + dt.timedelta(hours=2),
                           opener=lambda url: (J.dumps({"result": {"data": data}}).encode(), {}))

    def test_conflicting_dvol_hour_is_malformed_in_either_order(self):
        t = int(self.start.timestamp() * 1000)
        a = self._dvol([[t, 0, 0, 0, 40.0], [t, 0, 0, 0, 90.0], [t + 3_600_000, 0, 0, 0, 41.0]])
        b = self._dvol([[t, 0, 0, 0, 90.0], [t, 0, 0, 0, 40.0], [t + 3_600_000, 0, 0, 0, 41.0]])
        for st, rows, rep in (a, b):
            self.assertEqual(st, "malformed")
            self.assertEqual(rep["conflicts"], 1)
            self.assertEqual([r["dvol"] for r in rows], [41.0])      # the conflicted hour is dropped, never chosen
        self.assertEqual(a[1], b[1])                                  # row order cannot change the output

    def test_exact_duplicate_dvol_is_deduplicated(self):
        t = int(self.start.timestamp() * 1000)
        st, rows, rep = self._dvol([[t, 0, 0, 0, 40.0], [t, 0, 0, 0, 40.0], [t + 3_600_000, 0, 0, 0, 41.0]])
        self.assertEqual((st, [r["dvol"] for r in rows], rep["duplicates"], rep["conflicts"]), ("ok", [40.0, 41.0], 1, 0))

    def test_decreasing_cumulative_notional_is_malformed(self):
        # depth rises outward on every band, notional falls outward on the bid side at -2%
        text = depth_text(n=1).replace(",-2.00,1200.000,96000000.00", ",-2.00,1200.000,70000000.00")
        st, _, rep = A.inspect_bookdepth(rows_from(text), D)
        self.assertEqual((st, rep["non_monotone_snapshots"]), ("malformed", 1))


if __name__ == "__main__":
    unittest.main(verbosity=1)
