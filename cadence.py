"""Collection cadence history and schedule arithmetic, shared by report.py and watchdog.py.

`cadence.json` lists every schedule the collector has run under, oldest first. Health figures
use the cadence in force at each moment, so the hourly period before 2.6 is judged against hourly
slots and is not reported as missing three runs in four.

Two different things are measured, and kept apart:
  * scheduled execution - how many runs the scheduler started (trigger "schedule") compared with
    how many nominal slots passed. Runs are counted, never matched to slots: GitHub starts
    scheduled jobs late by an unrecorded amount, so an actual start time does not say which slot
    a run was for. Manual runs never count here.
  * snapshot coverage - whether stored market snapshots exist in each slot-to-slot interval,
    whatever started the run. This is what the data actually holds.
Run records written before 2.6 have no trigger field; their scheduled share is reported as
unknown rather than guessed.
"""
import datetime as dt
from pathlib import Path
from storage import read_json

MINUTE = 60_000
HOUR = 60 * MINUTE
# Run modes that are routine collection. "hourly" is what records written before 2.6 carry.
ROUTINE_MODES = ("routine", "hourly")


def parse_utc(text):
    return int(dt.datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp() * 1000)


def load(base):
    """[(start_ms, minutes_past_the_hour, cron)] sorted by start; [] when no history exists."""
    raw = read_json(Path(base) / "cadence.json", None) or {}
    periods = []
    for item in raw.get("periods", []):
        minutes = sorted(int(m) for m in item["minutes"])
        if not minutes or any(not 0 <= m < 60 for m in minutes):
            raise ValueError(f"invalid cadence minutes: {item}")
        periods.append((parse_utc(item["from"]), minutes, item.get("cron", "")))
    periods.sort()
    return periods


def spans(periods, a, b):
    """Split [a, b) by cadence period: [(start, end, minutes)]."""
    out = []
    for i, (start, minutes, _) in enumerate(periods):
        end = periods[i + 1][0] if i + 1 < len(periods) else None
        lo, hi = max(a, start), b if end is None else min(b, end)
        if lo < hi:
            out.append((lo, hi, minutes))
    return out


def slots(periods, a, b):
    """Nominal scheduled slot times in [a, b), using the cadence in force at each slot."""
    out = []
    for lo, hi, minutes in spans(periods, a, b):
        hour = lo // HOUR * HOUR
        while hour < hi:
            out.extend(t for t in (hour + m * MINUTE for m in minutes) if lo <= t < hi)
            hour += HOUR
    return out


def interval_minutes(periods, t):
    """Nominal spacing of the cadence in force at t (60 for hourly, 15 for quarter-hourly)."""
    current = [minutes for start, minutes, _ in periods if start <= t]
    if not current:
        return None
    minutes = current[-1]
    return 60 // len(minutes)


def slot_buckets(periods, a, b):
    """Slot-to-slot intervals [slot, next slot) that lie wholly inside [a, b)."""
    edges = slots(periods, a, b)
    return [(s, e) for s, e in zip(edges, edges[1:])]


def is_routine(run):
    return run.get("mode") in ROUTINE_MODES


def trigger(run):
    """'schedule', 'workflow_dispatch', 'local' ... or None for records written before 2.6."""
    return run.get("trigger")


# ------------------------------------------------------------------ health shared by report and watchdog
STALE_MIN_DEFAULT = 90


def stale_minutes():
    """Minutes without a scheduled run before the collector is called stale (WATCHDOG_STALE_MIN).
    90 at a 15-minute cadence is six consecutive slots: ordinary GitHub start delays and the odd
    dropped scheduled run stay under it, a disabled schedule or a stuck queue does not."""
    import os
    raw = os.environ.get("WATCHDOG_STALE_MIN", "").strip()
    value = int(raw) if raw else STALE_MIN_DEFAULT
    if value < 15:
        raise ValueError("WATCHDOG_STALE_MIN below one 15-minute slot would alert on every normal delay")
    return value


def schedule_evidence(run):
    """Could this run have been started by the schedule? Manual and local runs cannot; records
    before 2.6 (no trigger) from the GitHub runner might have been, so they still count for
    staleness during the transition but are never counted as scheduled execution."""
    return is_routine(run) and (trigger(run) == "schedule"
                                or (trigger(run) is None and run.get("runner") == "github"))


def failure_summary(run):
    """(critical, problems): critical when the run lost the critical Binance share series or the
    whole snapshot (the snapshot stage raised, or not one open-interest book succeeded - 2.6
    called a 0/17 snapshot healthy); problems lists every visible failure, degradation or rate
    limit, by source. A partly degraded snapshot stays a warning."""
    problems = []
    for key, error in (run.get("errors") or {}).items():
        problems.append((f"run {key}", str(error)))
    for name, status in (run.get("series") or {}).items():
        if status.get("err"):
            problems.append((f"history {name}", str(status["err"])))
    if (run.get("liq") or {}).get("err"):
        problems.append(("liquidations", str(run["liq"]["err"])))
    snap = run.get("snap") or {}
    for name, error in {**(snap.get("failed") or {}), **(snap.get("other_failed") or {})}.items():
        problems.append((f"snapshot {name}", str(error)))
    for name, status in (run.get("forward") or {}).items():
        if status.get("err"):
            problems.append((f"forward book {name}", str(status["err"])))
    rate = (run.get("http") or {}).get("rate_limited_by_host") or {}
    for host, count in rate.items():
        problems.append((f"rate limit {host}", f"{count} rate-limited response(s)"))
    snapshot_lost = bool(snap.get("books")) and not snap.get("books_ok")
    if snapshot_lost:
        problems.insert(0, ("snapshot", f"no open-interest book collected (0/{snap.get('books')})"))
    critical = run.get("critical_ok") is False or "snap" in (run.get("errors") or {}) \
        or "series" in (run.get("errors") or {}) or snapshot_lost
    return critical, problems


def quantiles(values, qs=(0.5, 0.9)):
    values = sorted(values)
    if not values:
        return [None for _ in qs]
    return [values[min(len(values) - 1, int(q * (len(values) - 1) + 0.5))] for q in qs]
