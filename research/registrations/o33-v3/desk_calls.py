"""desk_calls - registration order, identity, matched baselines and paired scoring for O33 (registered desk calls).

calls-2.0.0 (package 12.4.13): adds the O33 v3 baseline (matched_baseline_v3, below the v2 functions, which are
unchanged in behaviour). calls-1.0.0 (package 12.4.12) introduced the v2 functions. Pure functions over values the caller supplies (registry documents, server receipt
times, 1H closes from jbm_archive.load_klines_span(..., interval="1h")); no network, no clock. Frozen for O33 v2:
a later change is a new VERSION, and calls scored under different versions are reported as separate cohorts.

What it decides
  identity      call_id(): DESK-<INSTR>-<issue to the second>-<L|C>-<content hash 8>; plan_write() refuses to
                overwrite an existing document (write_db "set" replaces) and treats identical content as one call
  order         registration_status(): the window start is DERIVED from the server receipt (the first whole minute
                strictly after it), never taken from a stated time; a stored start earlier than that is backdated;
                a read sent before its receipt is late; a read that does not quote its registration receipt cannot
                show that registration preceded delivery and is scored apart ("order unverified")
  units         scoring_units(): one unit per (instrument, call type, horizon in hours, graded close); the first
                eligible receipt counts; later ones stay registered and are listed, never deleted; amendments are
                separate documents and never change the original
  baseline      baseline_support() + matched_baseline(): only for the symmetric, close-issued, whole-hour subset
                (bounds symmetric in log terms within 5 %, issue price = the last closed 1H bar, issued within 5 min of
                that close, graded at a 1H close 1-72 h later). Baseline = share of trailing-730-day 1H windows of the
                same length whose |log return| <= k x sigma_t, where k = the call's half-width / issue-time sigma and
                sigma_t is the sd of the 24 1H log returns ending at each window's start (x sqrt(h)), all ending at or
                before the issue's data cutoff. Anything else: baseline unavailable, the call stays descriptive.
  lean drift    lean_drift(): mean h-hour log return over the same trailing 730 days, ending at the data cutoff
  statistics    paired(): per unit d = outcome - baseline (containment: inside 0/1 minus the matched rate; lean:
                direction x log return - 10 bp - direction x drift); mean d with a WEEKLY block
                bootstrap (ISO week of the graded close, B = 10,000, seed 33), widened for baseline estimation error
                (fully correlated, conservative). Below 10 blocks or 30 units: no interval. A comparative statement
                needs >= 20 blocks, >= 60 units and a 95 % interval excluding zero; otherwise descriptive.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import random

VERSION = "calls-2.0.0"
V2_VERSION = "calls-1.0.0"          # the v2 baseline, unchanged
UTC = dt.timezone.utc
HOUR_MS = 3_600_000
LOOKBACK_DAYS = 730
SIGMA_BARS = 24
SYMMETRY_TOL = 0.05
CLOSE_ISSUE_MAX_S = 300
MAX_H = 72
COST_BP = 10.0
COMPARE = {"resampling_unit": "ISO week of the graded close", "B": 10_000, "seed": 33, "min_blocks": 10,
           "min_units": 30, "claim_blocks": 20, "claim_units": 60, "level": 0.95}


def _t(x) -> dt.datetime:
    if isinstance(x, dt.datetime):
        return x.astimezone(UTC)
    return dt.datetime.fromisoformat(str(x).replace("Z", "+00:00")).astimezone(UTC)


def iso(t: dt.datetime) -> str:
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S") + ("Z" if not t.microsecond else f".{t.microsecond:06d}Z")


def content_sha256(doc: dict) -> str:
    """Canonical JSON hash of a call's content, excluding fields the server or scorer adds."""
    body = {k: v for k, v in doc.items() if k not in ("content_sha256", "registered_utc", "start_utc", "updatedAt")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def call_id(instrument: str, issue_utc, call_type: str, sha: str) -> str:
    """Collision-resistant id: two calls on one instrument in one minute (or second) differ by type or content hash;
    identical content at the same second is the same call."""
    if call_type not in ("lean", "containment"):
        raise ValueError(f"call_type {call_type!r}")
    t = _t(issue_utc)
    return f"DESK-{instrument.upper()}-{t:%Y%m%dT%H%M%S}Z-{'L' if call_type == 'lean' else 'C'}-{sha[:8]}"


def plan_write(existing: dict | None, doc: dict) -> str:
    """'write' when the id is free; 'duplicate' (do not write) when the stored document has identical content;
    'conflict' (refuse; never overwrite) otherwise."""
    if existing is None:
        return "write"
    return "duplicate" if content_sha256(existing) == content_sha256(doc) else "conflict"


def derived_start(receipt_utc) -> dt.datetime:
    """The first whole minute strictly after the server receipt."""
    r = _t(receipt_utc)
    return r.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)


def registration_status(doc: dict, receipt_utc, read_quotes_receipt: bool, sent_utc=None) -> tuple[str, str]:
    """(status, reason). status: eligible | late | order-unverified | backdated | ineligible.
    receipt_utc: the registry's server time for version 1 (artifact updatedAt). sent_utc: the delivery time of the
    read when the operator supplies it (not observable to the model)."""
    if receipt_utc is None:
        return "ineligible", "no server receipt (unregistered)"
    if int(doc.get("version") or 1) != 1:
        return "ineligible", "document above version 1 (changed after registration)"
    start = derived_start(receipt_utc)
    stated = doc.get("start_utc")
    if stated is not None and _t(stated) < start:
        return "backdated", f"stated start {stated} precedes the derived start {iso(start)}"
    if sent_utc is not None and _t(sent_utc) < _t(receipt_utc):
        return "late", f"read sent {iso(_t(sent_utc))} before registration {iso(_t(receipt_utc))}"
    if not read_quotes_receipt:
        return "order-unverified", "the read does not quote its registration id and receipt; delivery may have preceded it"
    return "eligible", f"registered {iso(_t(receipt_utc))}, window starts {iso(start)}"


def horizon_h(call: dict) -> float:
    return (_t(call["graded_close_utc"]) - _t(call["issue_utc"])).total_seconds() / 3600


def scoring_units(calls: list[dict]) -> tuple[list[dict], list[dict]]:
    """(counted, not_counted). calls carry status (registration_status), instrument, call_type, issue_utc,
    graded_close_utc, receipt_utc. Only eligible calls form units; the first receipt per key counts."""
    counted, rest, seen = [], [], {}
    for c in sorted(calls, key=lambda c: (_t(c["receipt_utc"]) if c.get("receipt_utc") else dt.datetime.max.replace(tzinfo=UTC))):
        if c.get("amends"):
            rest.append(dict(c, why="amendment: recorded, never scored in place of its original"))
            continue
        if c.get("status") != "eligible":
            rest.append(dict(c, why=f"not eligible: {c.get('status')}"))
            continue
        key = (c["instrument"], c["call_type"], round(horizon_h(c)), c["graded_close_utc"])
        if key in seen:
            rest.append(dict(c, why=f"same instrument, type, horizon and graded close as {seen[key]}: not counted"))
            continue
        seen[key] = c.get("id")
        counted.append(c)
    return counted, rest


def _sd(xs):
    n = len(xs)
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def baseline_support(call: dict, closes: list[tuple[int, float]]) -> tuple[bool, str]:
    """Whether the implemented baseline covers this call. closes: [(close_time_ms, close)] 1H, ascending, ending at
    or before the issue's data cutoff (the caller must not pass later bars)."""
    if call.get("call_type") != "containment":
        return False, "not a containment call"
    lo, hi, p = float(call["lower"]), float(call["upper"]), float(call["issue_price"])
    if not (0 < lo < p < hi):
        return False, "bounds do not bracket the issue price"
    up, dn = math.log(hi / p), math.log(p / lo)
    if abs(up - dn) > SYMMETRY_TOL * (up + dn) / 2:
        return False, "asymmetric bounds (structural levels): matched baseline unavailable"
    if not closes:
        return False, "no 1H closes"
    t_close, c = closes[-1]
    issue = _t(call["issue_utc"])
    lag = (issue - dt.datetime.fromtimestamp(t_close / 1000, UTC)).total_seconds()
    if not (0 <= lag <= CLOSE_ISSUE_MAX_S) or abs(c - p) > 1e-9 * p:
        return False, "not issued at the last closed 1H bar's close (mid-bar issue): unavailable"
    h = (_t(call["graded_close_utc"]) - dt.datetime.fromtimestamp(t_close / 1000, UTC)).total_seconds() / 3600
    if abs(h - round(h)) > 1e-9 or not (1 <= round(h) <= MAX_H):
        return False, "graded close is not a whole number of hours (1-72) after the issue close: unavailable"
    return True, f"symmetric, close-issued, {round(h)} h"


def matched_baseline(call: dict, closes: list[tuple[int, float]]) -> dict:
    """The frozen matched rate for a supported call (see the module docstring)."""
    ok, why = baseline_support(call, closes)
    if not ok:
        return {"available": False, "reason": why, "version": V2_VERSION}
    t_close, c0 = closes[-1]
    h = round((_t(call["graded_close_utc"]) - dt.datetime.fromtimestamp(t_close / 1000, UTC)).total_seconds() / 3600)
    half = (math.log(float(call["upper"]) / c0) + math.log(c0 / float(call["lower"]))) / 2
    times = [t for t, _ in closes]
    if any(b - a != HOUR_MS for a, b in zip(times, times[1:])):
        return {"available": False, "reason": "1H closes have gaps or duplicates", "version": V2_VERSION}
    lr = [math.log(b / a) for (_, a), (_, b) in zip(closes, closes[1:])]          # lr[i]: close i -> i+1
    n = len(closes)
    if n - 1 < SIGMA_BARS:
        return {"available": False, "reason": "fewer than 24 1H returns before the issue", "version": V2_VERSION}
    sig_issue = _sd(lr[-SIGMA_BARS:]) * math.sqrt(h)
    k = half / sig_issue
    first_t = t_close - LOOKBACK_DAYS * 86_400_000
    inside = total = 0
    for i in range(SIGMA_BARS, n - h):                 # window start i (needs 24 returns ending at i), end i+h <= n-1
        if times[i] < first_t:
            continue
        s = _sd(lr[i - SIGMA_BARS:i]) * math.sqrt(h)
        r = math.log(closes[i + h][1] / closes[i][1])
        inside += abs(r) <= k * s
        total += 1
    if total < 200 * h:
        return {"available": False, "reason": f"only {total} trailing windows", "version": V2_VERSION}
    p = inside / total
    eff = total / h                                     # overlapping h-hour windows: about total/h independent
    return {"available": True, "rate": p, "windows": total, "effective_n": eff, "se": math.sqrt(p * (1 - p) / eff),
            "k_sigma": k, "sigma_issue_log": sig_issue, "horizon_h": h,
            "data_cutoff_utc": iso(dt.datetime.fromtimestamp(t_close / 1000, UTC)), "version": V2_VERSION}


def lean_drift(closes: list[tuple[int, float]], h: int) -> float:
    """Mean h-hour log return over the trailing 730 days of 1H closes ending at the data cutoff."""
    t_end = closes[-1][0]
    xs = [math.log(closes[i + h][1] / closes[i][1]) for i in range(len(closes) - h)
          if closes[i][0] >= t_end - LOOKBACK_DAYS * 86_400_000]
    return sum(xs) / len(xs)


def lean_outcome(direction: int, issue_price: float, close_at_horizon: float, drift: float) -> float:
    """Drift-adjusted signed log return after a 10 bp round trip, in log units."""
    return direction * math.log(close_at_horizon / issue_price) - COST_BP / 1e4 - direction * drift


def _week(t) -> str:
    y, w, _ = _t(t).isocalendar()
    return f"{y}-W{w:02d}"


def paired(units: list[dict]) -> dict:
    """units: [{"d": outcome - baseline, "graded_close_utc": ..., "se": baseline se or 0}]. Mean paired difference
    with a weekly block bootstrap; status descriptive unless the claim thresholds are met."""
    n = len(units)
    blocks = {}
    for u in units:
        blocks.setdefault(_week(u["graded_close_utc"]), []).append(u["d"])
    nb = len(blocks)
    out = {"version": VERSION, "units": n, "blocks": nb, "rules": COMPARE,
           "mean_d": (sum(u["d"] for u in units) / n) if n else None}
    if n < COMPARE["min_units"] or nb < COMPARE["min_blocks"]:
        out.update(interval=None, status=f"descriptive: {n} units in {nb} weekly blocks (an interval needs "
                                           f">= {COMPARE['min_units']} units and >= {COMPARE['min_blocks']} blocks)")
        return out
    keys = sorted(blocks)
    rnd = random.Random(COMPARE["seed"])
    means = []
    for _ in range(COMPARE["B"]):
        tot = cnt = 0
        for _ in keys:
            b = blocks[keys[rnd.randrange(nb)]]
            tot += sum(b)
            cnt += len(b)
        means.append(tot / cnt)
    means.sort()
    a = (1 - COMPARE["level"]) / 2
    lo, hi = means[int(a * len(means))], means[int((1 - a) * len(means)) - 1]
    widen = 1.959964 * sum(u.get("se", 0.0) for u in units) / n          # baseline error, fully correlated
    lo, hi = lo - widen, hi + widen
    claim = n >= COMPARE["claim_units"] and nb >= COMPARE["claim_blocks"]
    out.update(interval=[lo, hi], baseline_widening=widen,
               status=("comparative: interval excludes zero" if claim and (lo > 0 or hi < 0) else
                       "comparative: no demonstrated difference" if claim else
                       f"descriptive: below the claim thresholds ({COMPARE['claim_units']} units, "
                       f"{COMPARE['claim_blocks']} blocks)"))
    return out


# ============================================================================================================ O33 v3
# Frozen with calls-2.0.0 (package 12.4.12 -> 12.4.13, Oct 7 2026; operator decision the same day). A per-call matched
# baseline for the calls the desk actually makes: asymmetric structural bounds, issued at any minute, graded at a
# close any whole number of minutes later. Changing any constant or rule below is v4 with its own cohort.
MINUTE_MS = 60_000
V3 = {
    "o33": "v3", "module": "calls-2.0.0",
    "data": "Binance USD-M perp 1m closes through jbm_archive (validated, provider checksums); load_closes_1m",
    "anchor": "the last 1m close at or before issue_utc - the data cutoff; nothing later is read",
    "horizon": "H = graded_close_utc - anchor in whole minutes, 15 <= H <= 4320 (72 h); graded close on a whole minute",
    "sigma": "sd (n-1) of the 24 non-overlapping 60-minute log returns ending at a window start, x sqrt(H/60)",
    "bounds": "k_up = ln(upper/issue_price) / sigma_issue, k_dn = ln(issue_price/lower) / sigma_issue; each in [0.05, 8]",
    "windows": "starts t = anchor - j hours (the anchor's minute of the hour), t - 24 h >= anchor - 730 days, t + H <= anchor",
    "inside": "-k_dn x sigma_t <= ln(C(t+H) / C(t)) <= k_up x sigma_t",
    "missing": "a window needing any absent close is skipped; unavailable below 2,000 usable windows or 95 % usability",
    "effective_n": "windows x min(1, 60/H); se = sqrt(p(1-p)/effective_n)",
    "secondary": "declared, reported beside the primary and never replacing it: the primary's windows restricted to a "
                 "start hour (UTC) within +-2 h of the anchor's (circular), the same weekday/weekend class (UTC date), "
                 "and containing a scheduled release (data/releases_2020_2026.csv: CPI, NFP, PPI, FOMC) in (t, t+H] "
                 "iff the call's (anchor, graded close] does; unavailable below 300 windows",
    "outcome": "containment: lower <= the 1m close ending at graded_close_utc <= upper",
    "lean_drift": "mean H-minute log return over the primary window set",
    "statistic": "paired() unchanged; v3 units form their own cohort; the comparative claim reads the primary only",
}
V3_LOOKBACK_DAYS = 730
V3_MIN_H, V3_MAX_H = 15, 4320
V3_K_RANGE = (0.05, 8.0)
V3_MIN_WINDOWS, V3_MIN_USABLE = 2000, 0.95
V3_SECONDARY_MIN = 300
V3_TOD_HOURS = 2


def v3_spec_sha256() -> str:
    return hashlib.sha256(json.dumps(V3, sort_keys=True).encode()).hexdigest()


def load_closes_1m(first: dt.date, last: dt.date, symbol: str = "BTCUSDT", opener=None):
    """(state, {close_ms: close}, manifest) for 1m bars from jbm_archive. The archive module's validation is reused
    unchanged; only the 1m step is registered with it for this process (its file and version are untouched)."""
    import jbm_archive as A
    A.INTERVAL_MS.setdefault("1m", MINUTE_MS)
    state, rows, manifest = A.load_klines_span(first, last, "1m", symbol, opener)
    return state, {int(_t(r["close_utc"]).timestamp() * 1000): r["close"] for r in rows}, manifest


def releases_ms(path) -> list[int]:
    """Scheduled release times (ms) from the package calendar."""
    import csv
    out = []
    with open(path, newline="") as f:
        for row in csv.DictReader(line for line in f if not line.startswith("#")):
            out.append(int(_t(row["release_utc"]).timestamp() * 1000))
    return sorted(out)


def _floor_minute_ms(t: dt.datetime) -> int:
    ms = int(t.timestamp() * 1000)
    return ms - ms % MINUTE_MS


def v3_support(call: dict) -> tuple[bool, str]:
    """Whether a call's shape is within v3 (data availability is checked by matched_baseline_v3)."""
    if call.get("call_type") != "containment":
        return False, "not a containment call"
    try:
        lo, hi, p = float(call["lower"]), float(call["upper"]), float(call["issue_price"])
        issue, graded = _t(call["issue_utc"]), _t(call["graded_close_utc"])
    except (KeyError, TypeError, ValueError):
        return False, "missing issue, bounds or graded close"
    if not (0 < lo < p < hi):
        return False, "bounds do not bracket the issue price"
    if graded.second or graded.microsecond:
        return False, "graded close is not on a whole minute"
    h = (int(graded.timestamp() * 1000) - _floor_minute_ms(issue)) // MINUTE_MS
    if not (V3_MIN_H <= h <= V3_MAX_H):
        return False, f"horizon {h} min outside {V3_MIN_H}-{V3_MAX_H}"
    return True, f"{h} min"


def _has_release(rel: list[int], a: int, b: int) -> bool:
    import bisect
    i = bisect.bisect_right(rel, a)
    return i < len(rel) and rel[i] <= b


def matched_baseline_v3(call: dict, closes: dict, releases: list[int] | None = None) -> dict:
    """O33 v3 primary (and declared secondary) matched rate for one containment call. closes: {close_ms: close} 1m;
    any close after the anchor is ignored, never read."""
    ok, why = v3_support(call)
    out = {"version": VERSION, "o33": "v3", "spec_sha256": v3_spec_sha256()}
    if not ok:
        return dict(out, available=False, reason=why)
    a = _floor_minute_ms(_t(call["issue_utc"]))
    if a not in closes:
        return dict(out, available=False, reason="no 1m close at the anchor (data cutoff)")
    g = int(_t(call["graded_close_utc"]).timestamp() * 1000)
    h_min = (g - a) // MINUTE_MS
    hm = h_min * MINUTE_MS
    p = float(call["issue_price"])

    def sigma(t):
        pts = [closes.get(t - j * HOUR_MS) for j in range(25)]
        if any(x is None for x in pts):
            return None
        r = [math.log(pts[j] / pts[j + 1]) for j in range(24)]
        return _sd(r) * math.sqrt(h_min / 60)
    s_issue = sigma(a)
    if not s_issue:
        return dict(out, available=False, reason="1m closes missing for the issue-time sigma")
    k_up, k_dn = math.log(float(call["upper"]) / p) / s_issue, math.log(p / float(call["lower"])) / s_issue
    if not (V3_K_RANGE[0] <= k_up <= V3_K_RANGE[1] and V3_K_RANGE[0] <= k_dn <= V3_K_RANGE[1]):
        return dict(out, available=False, reason=f"bound multiples k_up {k_up:.2f} / k_dn {k_dn:.2f} outside {V3_K_RANGE}")
    first = a - V3_LOOKBACK_DAYS * 86_400_000 + 24 * HOUR_MS
    call_rel = _has_release(releases, a, g) if releases is not None else None
    a_hour = (a // HOUR_MS) % 24
    a_wkend = dt.datetime.fromtimestamp(a / 1000, UTC).weekday() >= 5
    cand = used = ins = 0
    sec_n = sec_in = 0
    rets = []
    t = a - hm
    t -= ((t - a) % HOUR_MS)                                  # align to the anchor's minute of the hour
    while t >= first:
        cand += 1
        c0, c1, s = closes.get(t), closes.get(t + hm), sigma(t)
        if c0 is not None and c1 is not None and s:
            used += 1
            r = math.log(c1 / c0)
            rets.append(r)
            inside = -k_dn * s <= r <= k_up * s
            ins += inside
            if releases is not None:
                hr = (t // HOUR_MS) % 24
                dh = min((hr - a_hour) % 24, (a_hour - hr) % 24)
                wk = dt.datetime.fromtimestamp(t / 1000, UTC).weekday() >= 5
                if dh <= V3_TOD_HOURS and wk == a_wkend and _has_release(releases, t, t + hm) == call_rel:
                    sec_n += 1
                    sec_in += inside
        t -= HOUR_MS
    out.update(anchor_utc=iso(dt.datetime.fromtimestamp(a / 1000, UTC)), horizon_min=h_min, sigma_issue_log=s_issue,
               k_up=k_up, k_dn=k_dn, candidate_windows=cand, windows=used,
               anchor_close=closes[a], issue_vs_anchor_log=math.log(p / closes[a]))
    if used < V3_MIN_WINDOWS or used < V3_MIN_USABLE * cand:
        return dict(out, available=False, reason=f"{used} of {cand} windows usable")
    rate = ins / used
    eff = used * min(1.0, 60 / h_min)
    out.update(available=True, rate=rate, effective_n=eff, se=math.sqrt(rate * (1 - rate) / eff),
               lean_drift=sum(rets) / len(rets))
    if releases is None:
        out["secondary"] = {"available": False, "reason": "no release calendar supplied"}
    elif sec_n < V3_SECONDARY_MIN:
        out["secondary"] = {"available": False, "reason": f"{sec_n} matched windows", "windows": sec_n,
                            "call_window_has_release": call_rel}
    else:
        sr = sec_in / sec_n
        se_ = sec_n * min(1.0, 60 / h_min)
        out["secondary"] = {"available": True, "rate": sr, "windows": sec_n, "effective_n": se_,
                            "se": math.sqrt(sr * (1 - sr) / se_), "call_window_has_release": call_rel}
    return out


def containment_outcome_v3(call: dict, closes: dict):
    """1 inside / 0 outside at the graded close, or None when that 1m close is not available."""
    c = closes.get(int(_t(call["graded_close_utc"]).timestamp() * 1000))
    if c is None:
        return None
    return int(float(call["lower"]) <= c <= float(call["upper"]))
