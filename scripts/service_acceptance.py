#!/usr/bin/env python3
"""service_acceptance - the 24-hour infrastructure acceptance check for the recovery path (repo 2.25). Read-only.

    python scripts/service_acceptance.py --from 2026-10-05T00:00:00Z [--to ISO]   (default: --from + 24 h)

Measures, from the stored records only (a run that did not persist does not count):
  collection   expected 15-minute slots; slot intervals holding an automated stored run (native or recovery);
               the longest interval without one (window edges included); runs by provenance
  decisions    each 4H range and PS1 decision due in the window, with its recorded state (health.py's rules)
  scoring      the scoring backlog at the end of the window
  people       routine collector runs a person started (interventions)
Targets (stated before observing, from the 15-minute cadence and the decision deadlines; not research criteria):
  intervals with an automated run >= 97% (at most 3 of 95 empty), longest automated gap <= 45 min,
  every range decision published, every PS1 decision executed or a recorded no-rebalance, empty scoring backlog,
  no person-started run. The window must have ended; a partial window is reported "pending", never passed.
Exit 0 pass, 1 fail, 3 pending. This is an infrastructure acceptance period, not a research promotion criterion.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cadence                    # noqa: E402
import health                     # noqa: E402
from watchdog import load_runs    # noqa: E402

UTC = dt.timezone.utc
TARGETS = {"interval_share": 0.97, "longest_gap_min": 45}


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def measure(base, start, end, now):
    a, b = int(start.timestamp() * 1000), int(end.timestamp() * 1000)
    runs = [r for r in load_runs(base) if r["t"] <= int(now.timestamp() * 1000)]
    cov = cadence.coverage(cadence.load(base), runs, a, min(b, int(now.timestamp() * 1000)))
    rng, info = health.range_decisions(base, min(end, now))
    ps1, _ = health.ps1_decisions(base, min(end, now))
    within = lambda k: start <= parse(k) < end      # noqa: E731
    rng = {k: v for k, v in rng.items() if within(k)}
    ps1 = {k: v for k, v in ps1.items() if within(k)}
    backlog = {h: len(v) for h, v in (info.get("scoring_backlog") or {}).items() if v}
    people = cov["runs_by_source"].get("human", 0)
    share = cov["intervals_with_automated_run"] / cov["intervals"] if cov["intervals"] else 0.0
    checks = {
        "collection_intervals": share >= TARGETS["interval_share"],
        "longest_automated_gap": cov["longest_automated_gap_min"] <= TARGETS["longest_gap_min"],
        "range_decisions_published": all(v == "published" for v in rng.values()),
        "ps1_decisions_resolved": all(v in ("executed", "no-rebalance", "hold") or v.startswith("not expected")
                                      for v in ps1.values()),
        "scoring_backlog_empty": not backlog,
        "no_person_started_runs": people == 0,
    }
    verdict = "pending" if now < end else ("pass" if all(checks.values()) else "fail")
    return {"window": [start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ")],
            "evaluated_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "targets": TARGETS, "collection": cov,
            "interval_share": round(share, 4), "range": rng, "ps1": ps1, "scoring_backlog": backlog,
            "person_started_runs": people, "checks": checks, "verdict": verdict}


def main(argv):
    if "--from" not in argv:
        print(__doc__)
        return 2
    start = parse(argv[argv.index("--from") + 1])
    end = parse(argv[argv.index("--to") + 1]) if "--to" in argv else start + dt.timedelta(hours=24)
    now = parse(argv[argv.index("--now") + 1]) if "--now" in argv else dt.datetime.now(UTC)
    doc = measure(ROOT, start, end, now)
    print(json.dumps(doc, indent=1, sort_keys=True))
    return {"pass": 0, "fail": 1, "pending": 3}[doc["verdict"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
