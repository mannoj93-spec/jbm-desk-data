#!/usr/bin/env python3
"""jbm_archive — Binance USD-M bulk-archive loader for the JBM crypto desk.

Version: archive-11.1.0 (package 11.1, Sep 25 2026; 11.1 adds klines and DVOL loaders and headerless-csv
support — metrics and bookDepth computation unchanged from archive-11.0.0). Stdlib only; imports jbm_measure from the same
folder. Status: implemented and tested offline (test_jbm_archive.py, synthetic and captured-byte
fixtures); deployed only when a fresh thread runs the tests from the mounted skill folder
(runbook §D). archive-10.0.0 is retired: it returned `ok` on wrong-day, off-grid, NaN, missing-value,
and negative-ratio files, raised on malformed numbers, and surveyed a 1-row day as `ok`.

WHAT A ROW IS KNOWN AT — four separate times (runbook §B "Availability"):
  archive_stamp_utc  the file's create_time T (for taker: window start, trades in [T, T+5m)).
  aligned_at_utc     T + 5m. Verified alignment only: the archive row T equals the live API row
                     stamped T+5m (OI, three ratios) and the taker window closes at T+5m
                     (baserates §1b V1-V2, Aug 22 - Sep 21 2026). This is the earliest the value
                     could exist, not when it was first published.
  available_at_utc   aligned_at + PUBLICATION_ALLOWANCE (default 5 min, PROVISIONAL policy). The
                     runbook records 1h `futures/data` rows appearing ~3-4 min after their stamp and
                     one row missing; 5m publication delay is unmeasured. Decision-time filtering
                     (as_of) uses this field. Historical first availability before Aug 22 2026 is
                     ASSUMED, not observed.
  retrieved_at_utc   when this code downloaded the file (provenance, per day).
The archive FILE for day D is written after D closes (Last-Modified observed ~07:05Z D+1 on
2026-09-20); a research design that needs a value intraday assumes the live API served it.

REVISION STATUS: a day's bytes are identified by sha256. Pass a pinned manifest entry to detect a
later provider revision (state `revised`). A hash detects change; it does not recover old bytes —
recovery needs the bytes stored somewhere durable (save_blob; the container is not durable).

STATES (SKILL.md M-19): ok | missing (HTTP 404) | retrieval_error (network, non-404 HTTP, provider
checksum mismatch) | malformed (unreadable zip, schema, wrong symbol/date, off grid, unparseable or
non-finite or out-of-domain values) | incomplete (valid rows but empty required values, conflicting
duplicates, or missing slots/coverage) | revised (bytes differ from a pinned manifest).
Precedence: missing/retrieval_error > revised > malformed > incomplete > ok. Only `ok` rows are
admissible to a test without an explicit, labelled override. Zero is a legitimate value; empty is
missing; 'nan', 'inf', text and negatives are malformed.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import math
import os
import urllib.error
import urllib.request
import zipfile

from jbm_measure import share_from_ratio

VERSION = "archive-12.0.0"
BASE = "https://data.binance.vision/data/futures/um/daily"
UA = {"User-Agent": "jbm-archive/12.0.0"}
ALIGN_LAG = dt.timedelta(minutes=5)                   # verified alignment (V1-V2)
PUBLICATION_ALLOWANCE = dt.timedelta(minutes=5)       # PROVISIONAL policy, not a measurement
FIRST_DAY = {"metrics": dt.date(2020, 9, 1), "bookDepth": dt.date(2023, 1, 1)}  # paged Sep 22 2026
SLOTS = {"metrics": 288}
GRID_MIN = 5
DEPTH_BANDS = (-5.0, -4.0, -3.0, -2.0, -1.0, -0.2, 0.2, 1.0, 2.0, 3.0, 4.0, 5.0)
# Band layouts observed in provider files (Sep 25 2026): 2026-09-20 has twelve bands; 2023-01-01 has
# ten (no +/-0.2). A snapshot is complete when it carries exactly one known layout; the day reports
# which, and a day mixing layouts is flagged. When the +/-0.2 bands began is not yet surveyed.
DEPTH_LAYOUTS = {"12band": frozenset(DEPTH_BANDS), "10band": frozenset(b for b in DEPTH_BANDS if abs(b) != 0.2)}
DEPTH_BUCKET_MIN = 5          # PROVISIONAL coverage rule: every 5-minute bucket holds >= 1 complete snapshot
STATE_ORDER = ("ok", "incomplete", "malformed", "revised", "retrieval_error", "missing")

# archive column -> (desk field, is_ratio)
METRIC_FIELDS = {
    "sum_open_interest": ("oi_btc", False),
    "sum_open_interest_value": ("oi_usd", False),
    "count_long_short_ratio": ("global_account", True),          # API globalLongShortAccountRatio
    "count_toptrader_long_short_ratio": ("top_account", True),   # API topLongShortAccountRatio
    "sum_toptrader_long_short_ratio": ("top_notional", True),    # API topLongShortPositionRatio
    "sum_taker_long_short_vol_ratio": ("taker_buy", True),       # API takerlongshortRatio (buy/sell)
}
METRIC_REQUIRED = ("create_time", "symbol") + tuple(METRIC_FIELDS)
DEPTH_REQUIRED = ("timestamp", "percentage", "depth", "notional")


def _iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def _worse(a: str, b: str) -> str:
    return a if STATE_ORDER.index(a) >= STATE_ORDER.index(b) else b


def _parse_ts(s):
    """Strict 'YYYY-MM-DD HH:MM:SS' (UTC). Returns None when unparseable."""
    try:
        return dt.datetime.strptime((s or "").strip(), "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None


def _parse_num(s):
    """-> ('ok', float) | ('missing', None) | ('malformed', reason). Zero is ok; empty is missing."""
    if s is None or str(s).strip() == "":
        return "missing", None
    try:
        v = float(str(s).strip())
    except ValueError:
        return "malformed", "unparseable"
    if not math.isfinite(v):
        return "malformed", "non_finite"
    if v < 0:
        return "malformed", "negative"
    return "ok", v


# --------------------------------------------------------------------------------------------
# Retrieval with provenance
# --------------------------------------------------------------------------------------------
def _default_opener(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read(), {k.lower(): v for k, v in r.headers.items()}


def _open(opener, url):
    got = opener(url)
    if isinstance(got, tuple):
        return got[0], {k.lower(): v for k, v in (got[1] or {}).items()}
    return got, {}


def day_url(dataset: str, day: dt.date, symbol: str) -> str:
    return f"{BASE}/{dataset}/{symbol}/{symbol}-{dataset}-{day.isoformat()}.zip"


def fetch_day(dataset: str, day: dt.date, symbol: str = "BTCUSDT", opener=None,
              verify_checksum: bool = True, pin: dict | None = None):
    """Return (state, raw_rows, prov) for one daily archive file."""
    return fetch_url(day_url(dataset, day, symbol), opener, verify_checksum, pin)


def fetch_url(url: str, opener=None, verify_checksum: bool = True, pin: dict | None = None,
              fieldnames: tuple | None = None):
    """Return (state, raw_rows, prov). prov records url, retrieval time, sha256, provider checksum
    status, Last-Modified/ETag when served, pin status, and code version. Never raises on data.
    With `fieldnames`, the csv may be headerless (older kline files) or carry that header row."""
    opener = opener or _default_opener
    prov = {"url": url, "retrieved_at_utc": _iso(_now()), "code_version": VERSION, "sha256": None,
            "provider_sha256": None, "checksum_status": "not_checked", "last_modified": None,
            "etag": None, "pin_status": "unpinned", "note": ""}
    try:
        blob, headers = _open(opener, url)
    except urllib.error.HTTPError as e:
        prov["note"] = f"HTTP {e.code}"
        return ("missing" if e.code == 404 else "retrieval_error"), [], prov
    except Exception as e:  # noqa: BLE001 — a failure is a state, never a silent empty
        prov["note"] = f"{type(e).__name__}: {e}"
        return "retrieval_error", [], prov
    if not isinstance(blob, (bytes, bytearray)):
        prov["note"] = "opener returned no bytes"
        return "retrieval_error", [], prov
    prov["sha256"] = hashlib.sha256(blob).hexdigest()
    prov["last_modified"], prov["etag"] = headers.get("last-modified"), headers.get("etag")
    if verify_checksum:
        try:
            ck, _ = _open(opener, url + ".CHECKSUM")
            prov["provider_sha256"] = ck.decode("ascii", "replace").split()[0].lower()
            prov["checksum_status"] = "match" if prov["provider_sha256"] == prov["sha256"] else "mismatch"
        except Exception as e:  # noqa: BLE001
            prov["checksum_status"] = "unavailable"
            prov["note"] = f"checksum: {type(e).__name__}"
        if prov["checksum_status"] == "mismatch":
            prov["note"] = "downloaded bytes differ from the provider's published sha256"
            return "retrieval_error", [], prov
    try:
        z = zipfile.ZipFile(io.BytesIO(blob))
        names = [n for n in z.namelist() if n.endswith(".csv")]
        if len(names) != 1:
            prov["note"] = f"expected one csv, found {len(names)}"
            return "malformed", [], prov
        stream = io.TextIOWrapper(z.open(names[0]), encoding="utf-8", newline="")
        if fieldnames:
            raw = list(csv.reader(stream))
            if raw and raw[0] and raw[0][0].strip() == fieldnames[0]:
                raw = raw[1:]
            rows = [dict(zip(fieldnames, r)) if len(r) == len(fieldnames) else {"_ragged": r} for r in raw]
        else:
            rows = list(csv.DictReader(stream))
    except Exception as e:  # noqa: BLE001
        prov["note"] = f"unreadable archive: {type(e).__name__}"
        return "malformed", [], prov
    state = "ok"
    if pin:
        prov["pin_status"] = "match" if pin.get("sha256") == prov["sha256"] else "revised"
        if prov["pin_status"] == "revised":
            state = "revised"
    return state, rows, prov


def save_blob(cache_dir: str, blob: bytes) -> str:
    """Content-addressed copy of raw bytes (filename = sha256). Durable only if cache_dir is."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, hashlib.sha256(blob).hexdigest() + ".zip")
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(blob)
    return path


# --------------------------------------------------------------------------------------------
# Validation — one implementation, used by load_* and survey
# --------------------------------------------------------------------------------------------
def inspect_metrics(raw_rows, day: dt.date, symbol: str = "BTCUSDT",
                    allowance: dt.timedelta = PUBLICATION_ALLOWANCE):
    """Validate raw metrics rows for one requested day. Returns (state, rows, report)."""
    rep = {"raw_rows": len(raw_rows), "malformed_rows": {}, "missing_values": {}, "exact_duplicates_dropped": 0,
           "conflicting_stamps_excluded": [], "valid_slots": 0, "complete_slots": 0,
           "missing_slots": SLOTS["metrics"], "flags": []}
    if not raw_rows:
        rep["flags"].append("no_rows")
        return "incomplete", [], rep
    cols = set(raw_rows[0].keys())
    absent = [c for c in METRIC_REQUIRED if c not in cols]
    if absent:
        rep["flags"].append("schema_missing:" + ",".join(absent))
        return "malformed", [], rep
    extra = sorted(c for c in cols if c not in METRIC_REQUIRED and c is not None)
    if extra:
        rep["flags"].append("extra_columns:" + ",".join(extra))

    def bad(reason):
        rep["malformed_rows"][reason] = rep["malformed_rows"].get(reason, 0) + 1

    by_stamp: dict = {}
    for r in raw_rows:
        if None in r:  # more cells than headers
            bad("ragged_row"); continue
        t = _parse_ts(r.get("create_time"))
        if t is None:
            bad("bad_timestamp"); continue
        if (r.get("symbol") or "").strip() != symbol:
            bad("wrong_symbol"); continue
        if t.date() != day:
            bad("wrong_date"); continue
        if t.second or t.minute % GRID_MIN:
            bad("off_grid"); continue
        vals, row_bad = {}, None
        for col in METRIC_FIELDS:
            st, v = _parse_num(r.get(col))
            if st == "malformed":
                row_bad = f"{col}:{v}"; break
            vals[col] = v
        if row_bad:
            bad(row_bad); continue
        by_stamp.setdefault(t, []).append(tuple(vals[c] for c in METRIC_FIELDS))

    out = []
    for t in sorted(by_stamp):
        variants = set(by_stamp[t])
        if len(variants) > 1:
            rep["conflicting_stamps_excluded"].append(_iso(t)); continue
        rep["exact_duplicates_dropped"] += len(by_stamp[t]) - 1
        vals = dict(zip(METRIC_FIELDS, by_stamp[t][0]))
        aligned = t + ALIGN_LAG
        rec = {"archive_stamp_utc": _iso(t), "aligned_at_utc": _iso(aligned),
               "available_at_utc": _iso(aligned + allowance),
               "availability_basis": f"assumed: API alignment +{int(allowance.total_seconds() // 60)}m provisional allowance",
               "code_version": VERSION, "flags": []}
        complete = True
        for col, (name, is_ratio) in METRIC_FIELDS.items():
            v = vals[col]
            rec[name] = v
            if v is None:
                complete = False
                rec["flags"].append("missing:" + name)
                rep["missing_values"][name] = rep["missing_values"].get(name, 0) + 1
            if is_ratio:
                rec[name + "_share"] = None if v is None else share_from_ratio(v)
        rep["valid_slots"] += 1
        rep["complete_slots"] += complete
        out.append(rec)
    rep["missing_slots"] = SLOTS["metrics"] - rep["valid_slots"]
    rep["rows_out"] = len(out)
    state = "ok"
    if rep["malformed_rows"]:
        state = "malformed"
    elif rep["missing_slots"] or rep["missing_values"] or rep["conflicting_stamps_excluded"]:
        state = "incomplete"
    return state, out, rep


def inspect_bookdepth(raw_rows, day: dt.date):
    """Validate bookDepth rows: schema, day, band set, finite non-negative values, cumulative
    monotonicity by side, and coverage (every 5-minute bucket holds >= 1 complete snapshot)."""
    rep = {"raw_rows": len(raw_rows), "malformed_rows": {}, "snapshots": 0, "complete_snapshots": 0, "band_layouts": {},
           "incomplete_snapshots": 0, "non_monotone_snapshots": 0, "buckets_covered": 0,
           "buckets_expected": 24 * 60 // DEPTH_BUCKET_MIN, "max_gap_s": None, "flags": []}
    if not raw_rows:
        rep["flags"].append("no_rows")
        return "incomplete", [], rep
    absent = [c for c in DEPTH_REQUIRED if c not in raw_rows[0]]
    if absent:
        rep["flags"].append("schema_missing:" + ",".join(absent))
        return "malformed", [], rep

    def bad(reason):
        rep["malformed_rows"][reason] = rep["malformed_rows"].get(reason, 0) + 1

    snaps: dict = {}
    for r in raw_rows:
        t = _parse_ts(r.get("timestamp"))
        if t is None:
            bad("bad_timestamp"); continue
        if t.date() != day:
            bad("wrong_date"); continue
        try:
            band = round(float(r["percentage"]), 4)
        except (TypeError, ValueError):
            bad("bad_band"); continue
        if band not in DEPTH_BANDS:
            bad("unknown_band"); continue
        sd, depth = _parse_num(r.get("depth"))
        sn, notional = _parse_num(r.get("notional"))
        if "malformed" in (sd, sn):
            bad("bad_value"); continue
        if "missing" in (sd, sn):
            bad("missing_value"); continue
        s = snaps.setdefault(t, {})
        if band in s and s[band] != (depth, notional):
            bad("conflicting_band"); continue
        s[band] = (depth, notional)

    out, complete_times, layouts = [], [], {}
    for t in sorted(snaps):
        s = snaps[t]
        rep["snapshots"] += 1
        layout = next((k for k, v in DEPTH_LAYOUTS.items() if frozenset(s) == v), None)
        if layout is None:
            rep["incomplete_snapshots"] += 1; continue
        layouts[layout] = layouts.get(layout, 0) + 1
        bands = sorted(s)
        # Cumulative depth AND cumulative notional must both be non-decreasing outward on each side (12.0:
        # a snapshot with rising BTC depth but falling notional is impossible and no longer passes).
        mono = all(
            all(s[b2][k] >= s[b1][k] for b1, b2 in zip(side, side[1:]))
            for side in ([b for b in bands if b > 0], sorted((b for b in bands if b < 0), reverse=True))
            for k in (0, 1))
        if not mono:
            rep["non_monotone_snapshots"] += 1; continue
        rep["complete_snapshots"] += 1
        complete_times.append(t)
        for b in bands:
            out.append({"snapshot_utc": _iso(t), "available_at_utc": _iso(t), "band_pct": b,
                        "depth_btc": s[b][0], "notional_usd": s[b][1], "code_version": VERSION})
    buckets = {(t.hour * 60 + t.minute) // DEPTH_BUCKET_MIN for t in complete_times}
    rep["buckets_covered"] = len(buckets)
    if len(complete_times) > 1:
        rep["max_gap_s"] = max((b - a).total_seconds() for a, b in zip(complete_times, complete_times[1:]))
    rep["rows_out"] = len(out)
    rep["band_layouts"] = layouts
    if len(layouts) > 1:
        rep["flags"].append("mixed_band_layouts")
    if rep["malformed_rows"] or rep["non_monotone_snapshots"]:
        state = "malformed"
    elif rep["incomplete_snapshots"] or rep["buckets_covered"] < rep["buckets_expected"] or len(layouts) > 1:
        state = "incomplete"
    else:
        state = "ok"
    return state, out, rep


# --------------------------------------------------------------------------------------------
# Loading, surveying, decision-time filtering, pinning
# --------------------------------------------------------------------------------------------
def _load(dataset, day, symbol, opener, verify_checksum, pin, inspect):
    if day < FIRST_DAY[dataset]:
        return "missing", [], {"prov": {"note": f"before first published day {FIRST_DAY[dataset]}"}}
    state, raw, prov = fetch_day(dataset, day, symbol, opener, verify_checksum, pin)
    if state in ("missing", "retrieval_error") or (state == "malformed" and not raw):
        return state, [], {"prov": prov}
    vstate, rows, rep = inspect(raw)
    for r in rows:
        r["source_sha256"] = prov["sha256"]
    rep["prov"] = prov
    return _worse(state, vstate), rows, rep


def load_metrics(day: dt.date, symbol: str = "BTCUSDT", opener=None, verify_checksum: bool = True,
                 pin: dict | None = None, allowance: dt.timedelta = PUBLICATION_ALLOWANCE):
    return _load("metrics", day, symbol, opener, verify_checksum, pin,
                 lambda raw: inspect_metrics(raw, day, symbol, allowance))


def load_bookdepth(day: dt.date, symbol: str = "BTCUSDT", opener=None, verify_checksum: bool = True,
                   pin: dict | None = None):
    return _load("bookDepth", day, symbol, opener, verify_checksum, pin,
                 lambda raw: inspect_bookdepth(raw, day))


def survey(dataset: str, start: dt.date, end: dt.date, symbol: str = "BTCUSDT", opener=None,
           verify_checksum: bool = True):
    """Per-day completeness through the SAME validation as loading. No rows returned."""
    loader = load_metrics if dataset == "metrics" else load_bookdepth
    out, day = [], start
    while day <= end:
        state, _, rep = loader(day, symbol, opener, verify_checksum)
        prov = rep.get("prov", {})
        rec = {"day": day.isoformat(), "state": state, "sha256": prov.get("sha256"),
               "checksum_status": prov.get("checksum_status"), "note": prov.get("note", "")}
        rec.update({k: v for k, v in rep.items() if k not in ("prov",)})
        out.append(rec)
        day += dt.timedelta(days=1)
    return out


# --------------------------------------------------------------------------------------------
# Klines (archive) and DVOL (Deribit API) — added 11.1 for the range model
# --------------------------------------------------------------------------------------------
KLINE_COLS = ("open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume",
              "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore")
INTERVAL_MS = {"1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000}
FIRST_KLINE_MONTH = (2020, 1)          # 2019-12 is 404 (probed Sep 25 2026)
UM_ROOT = "https://data.binance.vision/data/futures/um"


def kline_url(interval: str, period: str, symbol: str = "BTCUSDT") -> str:
    """period 'YYYY-MM' -> monthly file; 'YYYY-MM-DD' -> daily file."""
    kind = "monthly" if len(period) == 7 else "daily"
    return f"{UM_ROOT}/{kind}/klines/{symbol}/{interval}/{symbol}-{interval}-{period}.zip"


def _ms_to_dt(ms: int) -> dt.datetime:
    return dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc)


def inspect_klines(raw_rows, start: dt.datetime, end: dt.datetime, interval: str = "4h"):
    """Validate kline rows for the window [start, end): grid, window, close_time, OHLC consistency,
    finite positive prices, non-negative volume, duplicates, completeness. A bar is available at its
    close (open + interval). Returns (state, rows, report)."""
    step = INTERVAL_MS[interval]
    s_ms, e_ms = int(start.timestamp() * 1000), int(end.timestamp() * 1000)
    expected = (e_ms - s_ms) // step
    rep = {"raw_rows": len(raw_rows), "malformed_rows": {}, "exact_duplicates_dropped": 0,
           "conflicting_bars_excluded": [], "expected_bars": expected, "valid_bars": 0, "missing_bars": expected,
           "flags": []}

    def bad(reason):
        rep["malformed_rows"][reason] = rep["malformed_rows"].get(reason, 0) + 1

    if not raw_rows:
        rep["flags"].append("no_rows")
        return "incomplete", [], rep
    by_open: dict = {}
    for r in raw_rows:
        if "_ragged" in r:
            bad("ragged_row"); continue
        try:
            o_ms, c_ms = int(r["open_time"]), int(r["close_time"])
        except (TypeError, ValueError):
            bad("bad_timestamp"); continue
        if o_ms > 10**14:                      # microsecond stamps: convert and flag
            o_ms, c_ms = o_ms // 1000, c_ms // 1000
            if "microsecond_stamps" not in rep["flags"]:
                rep["flags"].append("microsecond_stamps")
        if o_ms % step:
            bad("off_grid"); continue
        if not (s_ms <= o_ms < e_ms):
            bad("outside_window"); continue
        if c_ms != o_ms + step - 1:
            bad("bad_close_time"); continue
        vals = {}
        for k in ("open", "high", "low", "close", "volume", "taker_buy_volume"):
            st, v = _parse_num(r.get(k))
            if st != "ok":
                vals = None; bad(f"{k}:{st if st == 'missing' else v}"); break
            vals[k] = v
        if vals is None:
            continue
        o, h, l, c = vals["open"], vals["high"], vals["low"], vals["close"]
        if min(o, h, l, c) <= 0:
            bad("non_positive_price"); continue
        if h < max(o, c) or l > min(o, c) or h < l:
            bad("ohlc_inconsistent"); continue
        by_open.setdefault(o_ms, []).append(tuple(vals[k] for k in ("open", "high", "low", "close", "volume", "taker_buy_volume")))
    out = []
    for o_ms in sorted(by_open):
        variants = set(by_open[o_ms])
        if len(variants) > 1:
            rep["conflicting_bars_excluded"].append(_iso(_ms_to_dt(o_ms))); continue
        rep["exact_duplicates_dropped"] += len(by_open[o_ms]) - 1
        o, h, l, c, v, tb = by_open[o_ms][0]
        t0 = _ms_to_dt(o_ms)
        out.append({"open_utc": _iso(t0), "close_utc": _iso(t0 + dt.timedelta(milliseconds=step)),
                    "available_at_utc": _iso(t0 + dt.timedelta(milliseconds=step)),
                    "open": o, "high": h, "low": l, "close": c, "volume": v, "taker_buy_volume": tb,
                    "code_version": VERSION})
    rep["valid_bars"] = len(out)
    rep["missing_bars"] = expected - len(out)
    rep["rows_out"] = len(out)
    if rep["malformed_rows"]:
        return "malformed", out, rep
    if rep["missing_bars"] or rep["conflicting_bars_excluded"]:
        return "incomplete", out, rep
    return "ok", out, rep


def load_klines(period: str, interval: str = "4h", symbol: str = "BTCUSDT", opener=None,
                verify_checksum: bool = True, pin: dict | None = None):
    """One monthly ('YYYY-MM') or daily ('YYYY-MM-DD') kline file through the shared validation."""
    if len(period) == 7:
        y, m = map(int, period.split("-"))
        if (y, m) < FIRST_KLINE_MONTH:
            return "missing", [], {"prov": {"note": "before first published month"}}
        start = dt.datetime(y, m, 1, tzinfo=dt.timezone.utc)
        end = dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=dt.timezone.utc)
    else:
        d = dt.date.fromisoformat(period)
        start = dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc)
        end = start + dt.timedelta(days=1)
    state, raw, prov = fetch_url(kline_url(interval, period, symbol), opener, verify_checksum, pin, KLINE_COLS)
    if state in ("missing", "retrieval_error") or (state == "malformed" and not raw):
        return state, [], {"prov": prov}
    vstate, rows, rep = inspect_klines(raw, start, end, interval)
    for r in rows:
        r["source_sha256"] = prov["sha256"]
    rep["prov"] = prov
    return _worse(state, vstate), rows, rep


def load_klines_span(first: dt.date, last: dt.date, interval: str = "4h", symbol: str = "BTCUSDT",
                     opener=None, verify_checksum: bool = True):
    """Bars from `first` through `last` (inclusive days): monthly files for whole past months, daily
    files for the rest. Returns (worst_state, rows, manifest) with one manifest entry per file."""
    rows, manifest, worst = [], [], "ok"
    cur = dt.date(first.year, first.month, 1)
    while cur <= last:
        nxt = dt.date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)
        month_end = nxt - dt.timedelta(days=1)
        periods = [cur.strftime("%Y-%m")] if month_end <= last else \
            [(cur + dt.timedelta(days=i)).isoformat() for i in range((last - cur).days + 1)]
        for per in periods:
            st, rs, rep = load_klines(per, interval, symbol, opener, verify_checksum)
            if len(per) == 7 and st == "missing":          # month not yet published: fall back to days
                for i in range((month_end - cur).days + 1):
                    d = cur + dt.timedelta(days=i)
                    if d > last:
                        break
                    st2, rs2, rep2 = load_klines(d.isoformat(), interval, symbol, opener, verify_checksum)
                    rows += rs2; manifest.append(manifest_entry(st2, rep2)); worst = _worse(worst, st2)
                continue
            rows += rs; manifest.append(manifest_entry(st, rep)); worst = _worse(worst, st)
        cur = nxt
    rows = [r for r in rows if first.isoformat() <= r["open_utc"][:10] <= last.isoformat()]
    return worst, rows, manifest


DERIBIT = "https://www.deribit.com/api/v2/public/get_volatility_index_data"


def load_dvol(start: dt.datetime, end: dt.datetime, currency: str = "BTC", opener=None, window_h: int = 900):
    """Hourly DVOL candles [start, end) from the Deribit API (not an archive: no provider checksum;
    provenance is the request list, retrieval time, and a sha256 over the responses). A candle stamped
    T is admitted at T + 1h (its close). Returns (state, rows, report)."""
    import json
    opener = opener or _default_opener
    rep = {"requests": [], "retrieved_at_utc": _iso(_now()), "malformed_rows": {}, "flags": [],
           "code_version": VERSION}
    h = hashlib.sha256()
    got: dict = {}
    conflicts: set = set()
    t = start
    while t < end:
        t2 = min(end, t + dt.timedelta(hours=window_h))
        url = (f"{DERIBIT}?currency={currency}&resolution=3600&start_timestamp={int(t.timestamp()*1000)}"
               f"&end_timestamp={int(t2.timestamp()*1000) - 1}")
        rep["requests"].append(url)
        try:
            blob, _ = _open(opener, url)
            h.update(blob)
            payload = json.loads(blob)
            data = payload["result"]["data"]
        except Exception as e:  # noqa: BLE001
            rep["flags"].append(f"retrieval_error:{type(e).__name__}")
            return "retrieval_error", [], rep
        for row in data:
            try:
                ts, c = int(row[0]), float(row[4])
            except (TypeError, ValueError, IndexError):
                rep["malformed_rows"]["bad_row"] = rep["malformed_rows"].get("bad_row", 0) + 1
                continue
            if ts % 3_600_000 or not math.isfinite(c) or c <= 0:
                rep["malformed_rows"]["bad_value"] = rep["malformed_rows"].get("bad_value", 0) + 1
                continue
            if start.timestamp() * 1000 <= ts < end.timestamp() * 1000:
                # 12.0: an exact duplicate is deduplicated; a conflicting value for the same hour is never
                # resolved by row order - the hour is dropped and the result is `malformed`.
                if ts in got and got[ts] != c:
                    conflicts.add(ts)
                elif ts in got:
                    rep["duplicates"] = rep.get("duplicates", 0) + 1
                got.setdefault(ts, c)
        t = t2
    for ts in conflicts:
        got.pop(ts, None)
    rep["conflicts"] = len(conflicts)
    if conflicts:
        rep["malformed_rows"]["conflicting_hour"] = len(conflicts)
        rep["flags"].append("conflicting_values:" + ",".join(_iso(_ms_to_dt(ts)) for ts in sorted(conflicts)[:5]))
    rows = [{"open_utc": _iso(_ms_to_dt(ts)), "available_at_utc": _iso(_ms_to_dt(ts + 3_600_000)),
             "dvol": got[ts], "code_version": VERSION} for ts in sorted(got)]
    expected = int((end - start).total_seconds() // 3600)
    rep.update(sha256=h.hexdigest(), expected_hours=expected, rows_out=len(rows), missing_hours=expected - len(rows))
    if rep["malformed_rows"]:
        return "malformed", rows, rep
    return ("incomplete" if rep["missing_hours"] else "ok"), rows, rep


def as_of(rows, decision_utc: dt.datetime, basis: str = "available_at_utc"):
    """Rows admissible at a decision time. Default basis is the assumed availability; 'aligned_at_utc'
    is allowed only as a labelled sensitivity run. The archive stamp is never a basis (M-01)."""
    if basis not in ("available_at_utc", "aligned_at_utc"):
        raise ValueError("basis must be available_at_utc or aligned_at_utc; the stamp is look-ahead")
    if decision_utc.tzinfo is None:
        raise ValueError("decision_utc must be timezone-aware UTC")
    cut = _iso(decision_utc.astimezone(dt.timezone.utc))
    return [r for r in rows if r[basis] <= cut]


def manifest_entry(state: str, rep: dict) -> dict:
    """Compact, storable record that pins the exact bytes a result used."""
    p = rep.get("prov", {})
    return {"url": p.get("url"), "sha256": p.get("sha256"), "provider_sha256": p.get("provider_sha256"),
            "checksum_status": p.get("checksum_status"), "last_modified": p.get("last_modified"),
            "etag": p.get("etag"), "retrieved_at_utc": p.get("retrieved_at_utc"),
            "code_version": VERSION, "state": state, "flags": rep.get("flags", []),
            "malformed_rows": rep.get("malformed_rows", {}), "missing_slots": rep.get("missing_slots")}


def reconcile(archive_rows, api_rows_by_field, tol=6e-5):
    """Compare archive rows to live-API rows. OI and shares match on aligned_at (API stamp = archive
    stamp + 5m); taker on the archive stamp (window start). Shares, not ratios: the API ratio is
    computed from 4-dp-rounded shares. Tolerances: shares 6e-5; OI 1 ppm; taker 0.1% relative."""
    out = {}
    for field, api in api_rows_by_field.items():
        matched = within = 0
        max_abs, worst = 0.0, None
        for r in archive_rows:
            key = r["archive_stamp_utc"] if field == "taker_buy" else r["aligned_at_utc"]
            if key not in api or r.get(field) is None:
                continue
            matched += 1
            d = abs(r[field] - api[key])
            t = 1e-6 * abs(api[key]) if field in ("oi_btc", "oi_usd") else (
                1e-3 * abs(api[key]) if field == "taker_buy" else tol)
            within += d <= t
            if d > max_abs:
                max_abs, worst = d, key
        out[field] = {"matched": matched, "within_tol": within, "max_abs_diff": max_abs, "worst_stamp": worst}
    return out


if __name__ == "__main__":  # smoke run: one day, state and provenance
    import json
    import sys
    d = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date(2026, 9, 20)
    ds = sys.argv[2] if len(sys.argv) > 2 else "metrics"
    st, rows, rep = (load_metrics if ds == "metrics" else load_bookdepth)(d)
    print(VERSION, ds, d, st, len(rows))
    print(json.dumps(manifest_entry(st, rep), indent=1))
