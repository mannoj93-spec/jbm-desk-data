#!/usr/bin/env python3
"""execution - what is actually known about one GitHub Actions run, stage by stage (repo 2.27).

The October 5 runner-assignment disruption (docs/incidents/2026-10-03-native-schedule.md, update 2026-10-05 20:14Z)
showed workflow runs that were created - the trigger was accepted - whose jobs never received a runner (runner_id 0,
no steps) and were cancelled, while the run's conclusion read "failure". A run's existence, creation time or
conclusion is therefore not evidence that anything executed. Each stage below is a separate fact with its own
evidence, and an unobserved stage stays unknown (None):

  trigger_accepted   the run exists in the Actions run list                          (run metadata)
  runner_assigned    at least one job received a runner (runner_id > 0)           (jobs API)
  steps_executed     at least one job step ran (a step with started_at, not skipped) (jobs API)
  critical_success   the stored run record is a critical success (cadence.critical_success)  (repository record)
  persisted          a run record for this run id is in data/runs                     (repository record)
  yielded            a valid yield receipt names this run (recovery.yield_receipt)   (repository receipt)

phase() folds them into one word for reports: queued, in-progress, never-started (completed with no runner),
failed-before-execution (runner but no executed step), executed-no-output, critical-failure, persisted-success,
yielded, unknown. queue_age_min is measured on the caller's clock for runs not yet started. Stdlib only.
"""
from __future__ import annotations

import datetime as dt

VERSION = "execution-1.0.0"
WAITING = ("queued", "pending", "waiting", "requested")


def _parse(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if isinstance(s, str) and s else None
    except ValueError:
        return None


def runner_assigned(jobs):
    """True / False / None (no job evidence)."""
    if jobs is None:
        return None
    if not jobs:
        return False
    return any(isinstance(j.get("runner_id"), int) and j["runner_id"] > 0 for j in jobs)


def steps_executed(jobs):
    """True when any job step ran; False when the jobs are known and none did; None without job evidence."""
    if jobs is None:
        return None
    for j in jobs:
        for s in j.get("steps") or []:
            if s.get("started_at") and s.get("conclusion") not in ("skipped",):
                return True
    return False


def stages(run, jobs=None, record=None, receipt=None, now=None):
    """Stage facts for one run. jobs: the run's jobs from the Actions API (None = not retrieved); record: its stored
    run record or None; receipt: a validated yield receipt or None."""
    import cadence
    status = (run or {}).get("status")
    out = {"run": (run or {}).get("id"), "trigger_accepted": run is not None, "status": status,
           "conclusion": (run or {}).get("conclusion"), "runner_assigned": runner_assigned(jobs),
           "steps_executed": steps_executed(jobs), "persisted": record is not None,
           "critical_success": None if record is None else cadence.critical_success(record),
           "yielded": receipt is not None, "queue_age_min": None}
    created = _parse((run or {}).get("created_at"))
    if status in WAITING and created and now:
        out["queue_age_min"] = round((now - created).total_seconds() / 60, 1)
    out["phase"] = phase(out)
    return out


def phase(st):
    if not st.get("trigger_accepted"):
        return "unknown"
    if st.get("persisted"):
        return "persisted-success" if st.get("critical_success") else "critical-failure"
    if st.get("yielded"):
        return "yielded"
    if st.get("status") in WAITING:
        return "queued"
    if st.get("status") == "in_progress":
        return "in-progress"
    if st.get("status") != "completed":
        return "unknown"
    if st.get("runner_assigned") is False:
        return "never-started"
    if st.get("runner_assigned") and st.get("steps_executed") is False:
        return "failed-before-execution"
    if st.get("steps_executed"):
        return "executed-no-output"
    return "unknown"


NOT_EXECUTED = ("never-started", "failed-before-execution")


# ---------------------------------------------------------------------------------------------- monitor checks
EXIT_ONLY = ("Process completed with exit code",)


def check_outcome(jobs, step_name, annotations=None):
    """What a monitor run's CHECK did (repo 2.28), from job/step evidence - setup steps executing is not the check
    executing. Returns (outcome, executed) with outcome one of:
      passed                 the check step ran and succeeded
      found a problem        the check step ran and failed, and the job carries a finding annotation
      check failed           the check step ran and failed with no finding reported (a crash cannot be excluded)
      failed before checking the job ran, the check step never started (an earlier step failed or it was skipped
                             after a failure)
      check skipped          the check step was skipped although nothing before it failed
      no runner              no job received a runner
      running                the check step is in progress
      unknown                no job/step evidence
    `annotations`: the failing job's check-run annotations (messages), when retrieved."""
    if jobs is None:
        return "unknown", None
    if runner_assigned(jobs) is False:
        return "no runner", False
    steps = [s for j in jobs for s in (j.get("steps") or [])]
    names = [s.get("name") for s in steps]
    if step_name not in names:
        return ("failed before checking", False) if steps else ("unknown", None)
    i = names.index(step_name)
    st = steps[i]
    c = st.get("conclusion")
    if st.get("status") == "in_progress":
        return "running", True
    if c == "success":
        return "passed", True
    if c == "failure" and st.get("started_at"):
        found = [a for a in (annotations or []) if a and not str(a).startswith(EXIT_ONLY)]
        return ("found a problem" if found else "check failed"), True
    earlier_failed = any(s.get("conclusion") in ("failure", "cancelled", "timed_out") for s in steps[:i])
    if c in ("skipped", None) or not st.get("started_at"):
        return ("failed before checking" if earlier_failed else "check skipped"), False
    return "check failed", True
