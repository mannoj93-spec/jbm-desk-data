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

1.1.0 (repo 2.26) keeps the immediate MECHANISM (`source`) apart from the INITIATING origin (`root`): every hop passes
the root on unchanged and appends its own run id, origin = "<root run>:<root label>[:<parent run>]", so dispatcher ->
range -> streams all name the run that started the chain and what started it. A recovery child of a person's
dispatcher run is human-assisted, never automated. A root label is a declaration until checked against the Actions
API (scripts/service_acceptance.py): "native-schedule" verifies when that run's event is schedule; "external" (the
owner's token from an outside timer) stays declared unless timer evidence corroborates it; anything else is unknown.
"""
from __future__ import annotations

import os

BOT = "github-actions[bot]"
VERSION = "provenance-1.1.0"


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


ROOT_LABELS = ("native-schedule", "external", "human")


def root(prov) -> dict:
    """{"run": id or None, "label": native-schedule | external | human | unknown, "parent": id or None}."""
    if not isinstance(prov, dict):
        return {"run": None, "label": "unknown", "parent": None}
    if prov.get("source") == "native-schedule":
        return {"run": None, "label": "native-schedule", "parent": None}
    if prov.get("source") == "human":
        return {"run": None, "label": "human", "parent": None}
    parts = (prov.get("origin") or "").split(":")
    if len(parts) >= 2 and parts[0].isdigit():
        label = parts[1] if parts[1] in ROOT_LABELS else "unknown"
        return {"run": parts[0], "label": label, "parent": parts[2] if len(parts) > 2 and parts[2].isdigit() else None}
    return {"run": None, "label": "unknown", "parent": None}


def automated(prov) -> bool:
    """Service activity started without a person: GitHub's schedule, or a recovery run whose chain was not started
    by a person (root native-schedule, external or an unrecorded/legacy root - counted, but unverified until
    service_acceptance checks it). A recovery child of a person's dispatcher run is human-assisted: False."""
    if not isinstance(prov, dict) or prov.get("source") not in ("native-schedule", "recovery"):
        return False
    return prov.get("source") == "native-schedule" or root(prov)["label"] != "human"


def child_origin(env=None) -> str:
    """origin input for a run this job dispatches: the root passed on, this run appended as parent."""
    env = os.environ if env is None else env
    run = env.get("GITHUB_RUN_ID", "local")
    if source(env) == "native-schedule":
        return f"{run}:native-schedule"
    r = root(record(env))
    if r["run"]:
        return f"{r['run']}:{r['label']}:{run}"
    return f"{run}:{source(env)}"
