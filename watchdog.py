#!/usr/bin/env python3
"""Fail loudly when the hourly collector has gone quiet.

A failing collector run already fails its own workflow. What it cannot report is its own
absence: a disabled schedule, a queue that never drains, or runs that stop committing. This
check reads the last stored run record and exits 1 when it is older than the limit, so GitHub's
failed-workflow email reaches the owner within about two hours instead of at the weekly report.
"""
import os
from pathlib import Path
import sys
import time
from storage import read_rows

LIMIT_H = 3


def last_run(base):
    for path in sorted((Path(base) / "data/runs").glob("*.jsonl"), reverse=True):
        rows = [r for r in read_rows(path) if r.get("mode") == "hourly"]
        if rows:
            return max(rows, key=lambda r: r["t"])
    return None


def check(base, now_ms):
    run = last_run(base)
    if run is None:
        return 1, "no hourly collector run has ever been stored"
    age_h = (now_ms - run["t"]) / 3_600_000
    where = f"last hourly run {time.strftime('%Y-%m-%d %H:%MZ', time.gmtime(run['t'] / 1000))} ({age_h:.1f}h ago, runner {run.get('runner')})"
    if age_h > LIMIT_H:
        return 1, f"collector silent: {where}; check the Hourly collector workflow"
    return 0, f"collector healthy: {where}"


if __name__ == "__main__":
    code, message = check(os.environ.get("OUT_DIR", Path(__file__).resolve().parent), int(time.time() * 1000))
    print(message)
    sys.exit(code)
