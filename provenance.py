"""provenance - what started this run, from the runner's own environment (repo 2.25). Stdlib only.

  native-schedule  GitHub's scheduler (event "schedule")
  recovery         the recovery dispatcher (recovery.py): event "workflow_dispatch", input trigger=recovery, AND
                   triggered by github-actions[bot] - only a workflow in this repository can dispatch as that actor,
                   so a person cannot produce this label by typing "recovery" into the Run workflow form
  human            any other workflow_dispatch, including a person who declared trigger=recovery (kept in
                   "declared" so the claim is visible but never credited to automation)
  chained          event "workflow_run" (started by another workflow's completion)
  push, pull_request, issues, local ...   the event itself

The recovery dispatcher passes its own run id and its own provenance in `origin` ("<run id>:<source>"), so a recovery
run can be traced to the dispatcher run and to whatever started that (native schedule, external automation or a
person). Labels are recorded, never inferred later from start times.
"""
from __future__ import annotations

import os

BOT = "github-actions[bot]"
VERSION = "provenance-1.0.0"


def source(env=None) -> str:
    env = os.environ if env is None else env
    event = env.get("GITHUB_EVENT_NAME") or "local"
    declared = (env.get("DESK_DISPATCH_TRIGGER") or "").strip()
    actor = env.get("GITHUB_TRIGGERING_ACTOR") or env.get("GITHUB_ACTOR") or ""
    if event == "schedule":
        return "native-schedule"
    if event == "workflow_dispatch":
        return "recovery" if declared == "recovery" and actor == BOT else "human"
    if event == "workflow_run":
        return "chained"
    return event


def record(env=None) -> dict:
    """The provenance block stored with a run's records."""
    env = os.environ if env is None else env
    return {"source": source(env), "event": env.get("GITHUB_EVENT_NAME") or "local",
            "triggering_actor": env.get("GITHUB_TRIGGERING_ACTOR") or env.get("GITHUB_ACTOR") or None,
            "declared": (env.get("DESK_DISPATCH_TRIGGER") or "").strip() or None,
            "slot": (env.get("DESK_DISPATCH_SLOT") or "").strip() or None,
            "origin": (env.get("DESK_DISPATCH_ORIGIN") or "").strip() or None,
            "version": VERSION}


def automated(prov) -> bool:
    """Started without a person: GitHub's schedule or the authenticated recovery dispatcher."""
    return isinstance(prov, dict) and prov.get("source") in ("native-schedule", "recovery")
