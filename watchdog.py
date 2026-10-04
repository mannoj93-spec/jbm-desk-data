#!/usr/bin/env python3
"""Fail loudly when the collector has gone quiet, and say so differently when it is running but
failing.

A failing collector run already fails its own workflow. What it cannot report is its own
absence: a disabled schedule, a queue that never drains, or runs that stop committing. This
check reads the stored run records and distinguishes three states:

  exit 1  stale or missing: no automated run - native schedule or, from repo 2.25, the recovery
          dispatcher (manual and local runs excluded) - within WATCHDOG_STALE_MIN minutes (default 90,
          six 15-minute slots). A native-only silence is a warning while recovery runs continue.
  exit 2  running but failing: the latest automated run lost critical data (the Binance share
          series, or the whole snapshot: the stage failed or no open-interest book succeeded).
  exit 0  healthy; source-level failures and degraded books in recent runs are printed as
          warnings (GitHub annotations) without failing the check.

Timing: the watchdog is scheduled every 30 minutes, and GitHub may start it late, so a collector
that stops is reported roughly 90-120 minutes after its last run, plus any delay in starting
the watchdog itself.
"""
import os
from pathlib import Path
import sys
import time
import cadence
from storage import read_rows

MINUTE = 60_000


def iso(ms):
    return time.strftime('%Y-%m-%d %H:%MZ', time.gmtime(ms / 1000))


def load_runs(base):
    """Every stored run record, newest last. All files are read: partition names are not trusted
    to order the records inside them."""
    rows = []
    for path in (Path(base) / "data/runs").glob("*.jsonl"):
        rows.extend(read_rows(path))
    return sorted(rows, key=lambda r: r["t"])


def check(base, now_ms, stale_min=None):
    """(exit code, message, warnings)[:2] is (code, message) for callers of the 2.5 interface.

    Repo 2.25: the verdict is service continuity - the newest AUTOMATED run (native schedule, or the recovery
    dispatcher authenticated by provenance.py). Native cadence is reported beside it: a native silence while recovery
    runs keep collecting is a warning, never hidden. A person's dispatch counts as neither."""
    stale_min = stale_min or cadence.stale_minutes()
    runs = [r for r in load_runs(base) if r["t"] <= now_ms]
    auto = [r for r in runs if cadence.automated_evidence(r)]
    scheduled = [r for r in runs if cadence.schedule_evidence(r)]
    manual = [r for r in runs if cadence.is_routine(r) and not cadence.automated_evidence(r)]
    warnings = []
    if manual and (not auto or manual[-1]["t"] > auto[-1]["t"]):
        warnings.append(f"newest routine run {iso(manual[-1]['t'])} was manual/local "
                        f"({cadence.trigger(manual[-1]) or manual[-1].get('runner')}); not counted as scheduled or automated")
    if not auto:
        return Result(1, "collector missing: no scheduled or recovery collector run has ever been stored", warnings)
    last = auto[-1]
    age = (now_ms - last["t"]) / MINUTE
    src = "native schedule" if cadence.schedule_evidence(last) else "recovery dispatcher"
    where = (f"last automated run {iso(last['t'])} ({age:.0f} min ago, {src}, {last.get('code_version')}, "
             f"trigger {cadence.trigger(last) or 'not recorded (pre-2.6)'})")
    if age > stale_min:
        return Result(1, f"collector stale: silent for {age:.0f} min (limit {stale_min}); {where}; "
                         "check the Collector workflow, the native schedule and the recovery dispatcher", warnings)
    native_age = (now_ms - scheduled[-1]["t"]) / MINUTE if scheduled else None
    if native_age is None or native_age > stale_min:
        warnings.append("native schedule silent " + (f"for {native_age:.0f} min (last scheduled run "
                        f"{iso(scheduled[-1]['t'])})" if scheduled else "(no scheduled run stored)")
                        + "; collection continued through the recovery dispatcher")
    critical, problems = cadence.failure_summary(last)
    recent = [r for r in auto if now_ms - r["t"] <= stale_min * MINUTE]
    seen = {}
    for run in recent:
        for source, message in cadence.failure_summary(run)[1]:
            count, _ = seen.get(source, (0, None))
            seen[source] = (count + 1, message)
    for source, (count, message) in sorted(seen.items()):
        warnings.append(f"{source}: {count}/{len(recent)} recent automated runs; latest: {message[:160]}")
    # 2.24: a recovered silence stays visible as a warning for a day; health.py records it durably
    for gap in cadence.scheduled_gaps(runs, stale_min, since_ms=now_ms - 24 * 60 * MINUTE):
        warnings.append(f"recovered native gap: no scheduled run {iso(gap['start_ms'])} to {iso(gap['end_ms'])} "
                        f"({gap['minutes']:.0f} min, limit {stale_min}); see reports/health.json")
    for gap in cadence.gaps(runs, stale_min, cadence.automated_evidence, since_ms=now_ms - 24 * 60 * MINUTE):
        warnings.append(f"recovered service gap: no automated run {iso(gap['start_ms'])} to {iso(gap['end_ms'])} "
                        f"({gap['minutes']:.0f} min, limit {stale_min}); see reports/health.json")
    if critical:
        return Result(2, f"collector running but failing: {where}; latest run lost critical data: "
                         + "; ".join(f"{s}: {m[:120]}" for s, m in problems[:4]), warnings)
    return Result(0, f"collector healthy: {where}; {len(recent)} automated run(s) in the last "
                     f"{stale_min} min", warnings)


class Result(tuple):
    """(code, message) with .warnings: indexes 0 and 1 keep the 2.5 return shape."""
    def __new__(cls, code, message, warnings):
        self = super().__new__(cls, (code, message))
        self.warnings = warnings
        return self


def main():
    base = os.environ.get("OUT_DIR", Path(__file__).resolve().parent)
    result = check(base, int(time.time() * 1000))
    code, message = result
    title = {0: "Collector healthy", 1: "Collector stale or missing", 2: "Collector failing"}[code]
    print(f"::{'notice' if code == 0 else 'error'} title={title}::{message}")
    for line in result.warnings:
        print(f"::warning title=Collector source warning::{line}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(f"### {title}\n\n{message}\n\n" + "".join(f"- {w}\n" for w in result.warnings))
    sys.exit(code)


if __name__ == "__main__":
    main()
