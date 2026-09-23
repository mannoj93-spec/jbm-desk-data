"""One forecast schema for phone intake, direct commits, registration, and scoring."""
import copy
import datetime as dt
import math
import re

MINUTE = 60_000
H = 60 * MINUTE
INSTRUMENT = "BTCUSDT perp, Binance last price"
TOP = {"id", "code_version", "snapshot_hash", "instrument", "reference_price", "start_utc", "horizon_utc",
       "event_regime", "events", "note", "made_utc", "package"}
COMMON = {"name", "type"}
EVENT_KEYS = {
    "touch": {"level", "dir", "p", "p_class"},
    "terminal": {"level", "dir", "p", "p_class"},
    "race": {"a", "b", "p", "p_class"},
    "interval": {"lo", "hi", "coverage"},
    "lean": {"direction", "basis", "invalidation"},
    "predicate": {"series", "op", "value", "at_utc", "by_utc"},
    # Desk forecast target (runbook E2): ln(max high / min low) over [start, horizon), quantiles.
    "range": {"q10", "q50", "q90"},
}
SERIES = {}
for endpoint, fields in {
    "globalLongShortAccountRatio": {"longAccount", "shortAccount", "longShortRatio"},
    "topLongShortAccountRatio": {"longAccount", "shortAccount", "longShortRatio"},
    "topLongShortPositionRatio": {"longAccount", "shortAccount", "longShortRatio"},
    "openInterestHist": {"sumOpenInterest", "sumOpenInterestValue"},
    "takerlongshortRatio": {"buySellRatio", "buyVol", "sellVol"},
}.items():
    for period, step in (("5m", 5 * MINUTE), ("1h", H)):
        SERIES[f"binance_{endpoint}_{period}"] = (step, fields)
for name in ("okx_mark_1h", "okx_index_1h", "deribit_dvol_1h"):
    SERIES[name] = (H, {"o", "h", "l", "c"})
SERIES["okx_acct_ratio_1h"] = (H, {"longShortRatio"})
# 1-minute reference and executable price bars (2.7), stored as one batch record per collector run
# in data/prices/<name>/YYYY-MM.jsonl (see enrich.py), not as data/series rows, to keep storage
# compact. Each name states venue, instrument and price type: "klines" are last-trade bars with
# volume and taker-buy volume; "markklines" are the exchange's mark price bars (no volume). A bar
# opening at T is known no earlier than T + 1m and no earlier than the batch's observed_at.
KLINE_FIELDS = {"o", "h", "l", "c", "v", "qv", "n", "tbv", "tbqv"}
PRICE_SERIES = {
    "binance_klines_1m_BTCUSDT_perp": ("Binance USD-M BTCUSDT perpetual", "last trade", KLINE_FIELDS),
    "binance_markklines_1m_BTCUSDT_perp": ("Binance USD-M BTCUSDT perpetual", "mark price", {"o", "h", "l", "c"}),
    "binance_klines_1m_BTCUSDT_spot": ("Binance spot BTCUSDT", "last trade", KLINE_FIELDS),
    "binance_klines_1m_ETHUSDT_perp": ("Binance USD-M ETHUSDT perpetual", "last trade", KLINE_FIELDS),
    "binance_klines_1m_SOLUSDT_perp": ("Binance USD-M SOLUSDT perpetual", "last trade", KLINE_FIELDS),
}

# Stamp semantics, measured live 2026-09-22 (see CHANGELOG 2.2):
#   snapshot -- the row stamped T is the value AS OF T (Binance 1h ratio/OI rows equal the 5m
#               rows at the same stamp; OKX account ratio stamped T is published before T+1h).
#               Knowledge time is T+5m (Binance M-01, verified field by field in the archive).
#   interval -- the row stamped T summarises [T, T+step) and is known at its close T+step
#               (Binance taker volumes sum the twelve 5m rows from T; OKX/Deribit candles).
KNOWLEDGE_LAG = 5 * MINUTE
SERIES_KIND = {name: ("interval" if name.startswith("binance_takerlongshortRatio")
                      or name in ("okx_mark_1h", "okx_index_1h", "deribit_dvol_1h") else "snapshot")
               for name in SERIES}


def observed_time(name, t):
    """The instant a stored row describes: its stamp (snapshot) or its interval close."""
    return t if SERIES_KIND[name] == "snapshot" else t + SERIES[name][0]


def known_time(name, t):
    """Earliest instant a stored row could have been known (never its stamp)."""
    return t + KNOWLEDGE_LAG if SERIES_KIND[name] == "snapshot" else t + SERIES[name][0]


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def ms(value):
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    d = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if d.tzinfo is None or d.utcoffset() != dt.timedelta(0):
        raise ValueError("explicit UTC (Z or +00:00) required")
    if d.microsecond:
        raise ValueError("fractional seconds are not supported")
    return int(d.timestamp() * 1000)


def iso(value):
    return dt.datetime.fromtimestamp(value / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def prepare(fc, now):
    if not isinstance(fc, dict):
        return fc
    fc = copy.deepcopy(fc)
    if not fc.get("start_utc"):
        fc["start_utc"] = iso((now // 300_000 + 1) * 300_000)
    fc.setdefault("instrument", INSTRUMENT)
    return fc


def predicate_step(series):
    if series in ("high", "low"):
        return MINUTE
    if series in ("close_1h", "close_4h"):
        return H if series == "close_1h" else 4 * H
    if isinstance(series, str) and series.startswith("series:"):
        parts = series.split(":")
        if len(parts) == 3 and parts[1] in SERIES and parts[2] in SERIES[parts[1]][1]:
            return SERIES[parts[1]][0]
    raise ValueError("unknown predicate series or field (only fixed-cadence series supported)")


def validate(fc, now=None):
    """now=None validates historical records without requiring a future start."""
    errors = []
    if not isinstance(fc, dict):
        return ["forecast must be an object"]
    extra = set(fc) - TOP
    if extra:
        errors.append(f"unapproved forecast fields: {sorted(extra)}")
    if not isinstance(fc.get("id"), str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{2,79}", fc["id"]):
        errors.append("id must be 3–80 filename-safe characters")
    if not num(fc.get("reference_price")) or fc.get("reference_price", 0) <= 0:
        errors.append("reference_price must be positive and finite")
    if fc.get("instrument") != INSTRUMENT:
        errors.append(f"instrument must be {INSTRUMENT!r}")
    for key in TOP - {"events", "reference_price"}:
        if key in fc and (not isinstance(fc[key], str) or len(fc[key]) > 2000):
            errors.append(f"{key} must be text of at most 2000 characters")
    try:
        start, end = ms(fc["start_utc"]), ms(fc["horizon_utc"])
        if start % MINUTE or end % MINUTE:
            errors.append("start and horizon must align to whole UTC minutes")
        if not start < end <= start + 31 * 24 * H:
            errors.append("horizon must follow start by at most 31 days")
        if now is not None and start <= now:
            errors.append("start must be strictly after registration time")
        if fc.get("made_utc"):
            ms(fc["made_utc"])
    except (ValueError, TypeError, KeyError, OverflowError):
        return errors + ["start/horizon/made timestamps require explicit ISO-8601 UTC"]
    events = fc.get("events")
    if not isinstance(events, list) or not 1 <= len(events) <= 100:
        return errors + ["events must be a list of 1–100 objects"]
    for i, ev in enumerate(events):
        prefix = f"event {i + 1}: "
        def fail(message):
            errors.append(prefix + message)
        if not isinstance(ev, dict):
            fail("must be an object")
            continue
        kind = ev.get("type")
        if not isinstance(kind, str) or kind not in EVENT_KEYS:
            fail("unknown type")
            continue
        if set(ev) - COMMON - EVENT_KEYS[kind]:
            fail("unexpected fields for this event type")
        for key in ("name", "basis"):
            if key in ev and (not isinstance(ev[key], str) or len(ev[key]) > 500):
                fail(f"{key} must be short text")
        if kind in ("touch", "terminal", "race"):
            if not num(ev.get("p")) or not 0 <= ev.get("p", -1) <= 1:
                fail("probability must be finite and in [0,1]")
            if ev.get("p_class") not in ("measured", "model", "prior"):
                fail("p_class must be measured, model, or prior")
        if kind in ("touch", "terminal"):
            if not num(ev.get("level")) or ev.get("level", 0) <= 0:
                fail("level must be positive and finite")
            if ev.get("dir") not in (("up", "down") if kind == "touch" else ("above", "below")):
                fail("invalid direction")
        if kind == "race":
            for leg in ("a", "b"):
                value = ev.get(leg)
                if (not isinstance(value, dict) or set(value) != {"level", "dir"}
                    or not num(value.get("level")) or value.get("level", 0) <= 0
                    or value.get("dir") not in ("up", "down")):
                    fail(f"{leg} requires exactly positive finite level and dir up/down")
        if kind == "interval":
            if not (num(ev.get("lo")) and num(ev.get("hi")) and 0 < ev["lo"] < ev["hi"]):
                fail("interval requires 0 < lo < hi")
            if not num(ev.get("coverage")) or not 0 < ev.get("coverage", 0) < 1:
                fail("coverage must be in (0,1)")
        if kind == "lean":
            if ev.get("direction") not in ("up", "down"):
                fail("direction must be up/down")
            inv = ev.get("invalidation")
            if inv is not None and (not isinstance(inv, dict) or set(inv) != {"level", "dir", "basis"}
                or not num(inv.get("level")) or inv.get("level", 0) <= 0
                or inv.get("dir") not in ("above", "below") or inv.get("basis") not in ("close_1h", "close_4h")):
                fail("invalidation requires level, dir above/below, basis close_1h/close_4h")
        if kind == "range":
            qs = [ev.get(k) for k in ("q10", "q50", "q90")]
            if not all(num(q) for q in qs) or not 0 < qs[0] <= qs[1] <= qs[2] < 1:
                fail("range requires 0 < q10 <= q50 <= q90 < 1, in ln(high/low) units")
        if kind == "predicate":
            series = ev.get("series")
            if series is None:
                if set(ev) - COMMON:
                    fail("manual predicate may contain only name and type")
                continue
            try:
                step = predicate_step(series)
                if ev.get("op") not in ("<", ">", "<=", ">=") or not num(ev.get("value")):
                    fail("requires comparison op and finite value")
                if ("at_utc" in ev) == ("by_utc" in ev):
                    fail("specify exactly one of at_utc/by_utc")
                deadline = ms(ev.get("at_utc", ev.get("by_utc")))
                if not start < deadline <= end or deadline % MINUTE:
                    fail("deadline must be a whole minute strictly after start and within horizon")
                if "at_utc" in ev and deadline % step:
                    fail("at_utc must align to a completed interval")
                if "by_utc" in ev and (start // step + 1) * step > deadline:
                    fail("no completed interval in the requested window")
            except (ValueError, TypeError, OverflowError):
                fail("invalid series/field or UTC deadline")
    return errors
