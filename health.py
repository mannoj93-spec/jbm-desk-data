#!/usr/bin/env python3
"""health - operational health of the desk, one dimension at a time, on an explicit clock (repo 2.24).

Five questions are kept apart, because each fails differently and a green answer to one says nothing about
another:
  source      the collector's NATIVE scheduled cadence: last scheduled run, its age, and every silence longer than the
              stale limit (cadence.scheduled_gaps), recovered or ongoing. A recovered gap stays listed.
              source.service (repo 2.25): automated service continuity - native or recovery-dispatcher runs
              (provenance.py), with its own gaps; source.coverage_24h: expected slots, runs by provenance, intervals
              holding an automated stored run and the longest automated gap. A person's run counts in neither.
  decisions   expected 4H work: the range stream (published / skipped / failed / absent, desk/range_monitor.py's
              rules) and PS1 after its launch (executed / no-rebalance / missed-execution / no decision record /
              not expected under an operator pause or termination / pending inside its deadline). Recorded
              state only: a later run, a backfill or recovered price bars never complete an earlier decision.
  coverage    PS1's coverage is as of its report's generation; decisions that fell due after that are listed
              separately with their recorded state (the report is never re-run from here).
  availability the range status file judged on this check's clock (its own exact expiry rules).
  scoring     matured, eligible RC1D forecasts still unscored (the monitor's backlog rule).
  monitors    heartbeat (last completed run, any result) and last result of the watchdog and range-monitor, kept
              apart from their last success (2.26), the dispatcher, and the newest scheduled run of any workflow
              (GitHub API, when a token is given); unknown without one. An old success is never current health. A
              failed monitor run whose check executed detected a problem; one whose job never received a runner or
              ran no step could not execute (2.27, job/step evidence) - it detected nothing.
  2.28        the monitor's own CHECK step is read (watchdog / range-monitor check step names): passed, found a
              problem (failed with a finding annotation), check failed (no finding reported), failed before
              checking, check skipped, no runner, unknown. Setup steps running is not the check running.
              monitors.external_timer: arrivals of the designated primary trigger per :12/:27/:42/:57 opportunity
              (on time / delayed / absent) apart from the native dispatcher heartbeat; overall service health stays
              its own question and may be healthy while external arrivals are missing.
  2.27        source.service separates data freshness (the newest automated CRITICAL SUCCESS) from activity (the
              newest automated run record, any result): a fresh failure stays "failing", fresh activity never makes
              stale data healthy, and the 45-minute restoration acceptance target is reported beside - never merged
              with - the stale limit. A stale report means no newer report was persisted; it does not by itself say
              the scheduler was silent (the run may not have executed, may have failed or may not have persisted).

Modes:  python health.py            read-only: print the JSON, write nothing
        python health.py --record   also write reports/health.{json,md} and append new incidents to
                                    state/incidents.jsonl (deduplicated; event times from the records,
                                    first_recorded_utc from this clock)
It never reads or writes forecast, research or paper-trading state beyond reading their records, and never
runs, repeats or backdates any work. Stdlib only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for p in (str(ROOT), str(ROOT / "desk")):
    if p not in sys.path:
        sys.path.insert(0, p)

import cadence                    # noqa: E402
from watchdog import load_runs    # noqa: E402

VERSION = "health-1.4.0"
ACCEPTANCE_GAP_MIN = 45          # restoration acceptance target (scripts/service_acceptance.py) - not the watchdog limit
UTC = dt.timezone.utc
LOOKBACK_H = 72                   # decisions and gaps examined (incidents already recorded stay recorded)
MONITORS = {"watchdog.yml": 90, "range-monitor.yml": 510}
DISPATCHER = ("recovery.yml", 45)   # repo 2.25: any event; three 15-minute invocations   # minutes: 90 = the collector stale limit (three
#   30-minute watchdog slots); 510 = 8.5 h, the range monitor's publication limit (two 4-hourly slots + grace)
SCHEDULED_WORKFLOWS = ("collect.yml", "watchdog.yml", "dashboard.yml", "intake.yml", "range-score.yml", "range.yml",
                       "research-streams.yml", "range-monitor.yml", "research.yml")
INCIDENTS = "state/incidents.jsonl"
PROBLEM_STATES = ("absent", "failed", "missed", "no decision record", "invalid")


def iso(ms):
    return None if ms is None else dt.datetime.fromtimestamp(ms / 1000, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    try:
        fmt = "%Y-%m-%dT%H:%M:%S.%fZ" if "." in s else "%Y-%m-%dT%H:%M:%SZ"
        return dt.datetime.strptime(s, fmt).replace(tzinfo=UTC)
    except (TypeError, ValueError):
        return None


def rows(path):
    out = []
    try:
        for line in Path(path).read_text().splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if isinstance(r, dict):
                out.append(r)
    except FileNotFoundError:
        pass
    return out


def jload(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, ValueError):
        return default


# --------------------------------------------------------------------------------------------- source
def source(base, now_ms, stale_min):
    runs = [r for r in load_runs(base) if r["t"] <= now_ms]
    sched = [r for r in runs if cadence.schedule_evidence(r)]
    last = sched[-1]["t"] if sched else None
    gaps = cadence.scheduled_gaps(runs, stale_min, since_ms=now_ms - LOOKBACK_H * 3_600_000, now_ms=now_ms)
    age = (now_ms - last) / 60_000 if last else None
    state = "missing" if last is None else ("stale" if age > stale_min else
                                            ("failing" if cadence.failure_summary(sched[-1])[0] else "healthy"))
    manual = [r for r in runs if cadence.is_routine(r) and not cadence.automated_evidence(r) and (not last or r["t"] > last)]
    # Repo 2.27: data outcome and activity are separate facts. The newest automated activity (any result) is the
    # heartbeat; the newest automated CRITICAL SUCCESS is the data freshness. A fresh failure stays visible as
    # "failing"; fresh activity never makes stale data healthy.
    auto = [r for r in runs if cadence.automated_evidence(r)]
    good = [r for r in auto if cadence.critical_success(r)]
    alast, glast = (auto[-1] if auto else None), (good[-1] if good else None)
    aage = (now_ms - alast["t"]) / 60_000 if alast else None
    gage = (now_ms - glast["t"]) / 60_000 if glast else None
    data_state = "missing" if glast is None else ("stale" if gage > stale_min else "fresh")
    latest_failed = bool(alast) and not cadence.critical_success(alast)
    sstate = ("missing" if alast is None and glast is None else "stale" if data_state != "fresh" else
              "failing" if latest_failed else "healthy")
    sgaps = cadence.gaps(runs, stale_min, cadence.successful_automated, since_ms=now_ms - LOOKBACK_H * 3_600_000, now_ms=now_ms)
    service = {"state": sstate, "data_state": data_state,
               "last_success_utc": iso(glast["t"]) if glast else None,
               "data_age_min": round(gage, 1) if gage is not None else None,
               "last_activity_utc": iso(alast["t"]) if alast else None,
               "last_activity_result": None if alast is None else ("critical success" if not latest_failed else "critical failure"),
               "last_automated_utc": iso(alast["t"]) if alast else None,          # 2.25 name: the activity heartbeat
               "last_source": None if alast is None else ("native-schedule" if cadence.schedule_evidence(alast) else "recovery"),
               "age_min": round(aage, 1) if aage is not None else None,
               "gaps": [dict(g, start_utc=iso(g["start_ms"]), end_utc=iso(g["end_ms"])) for g in sgaps],
               "acceptance_target": {"max_gap_min": ACCEPTANCE_GAP_MIN,
                                     "current_gap_min": round(gage, 1) if gage is not None else None,
                                     "breached_now": gage is None or gage > ACCEPTANCE_GAP_MIN,
                                     "rule": "restoration acceptance target (45 min between persisted critical "
                                             "successes); separate from the watchdog's stale limit"},
               "rule": "native schedule or the authenticated recovery dispatcher; a person's dispatch never counts; "
                       "gaps and data freshness use critical successes only (2.27)"}
    periods = cadence.load(base)
    cov = cadence.coverage(periods, runs, now_ms - 24 * 3_600_000, now_ms) if periods else None
    if cov:
        cov = dict(cov, from_utc=iso(cov["from_ms"]), to_utc=iso(cov["to_ms"]))
        service["acceptance_target"]["longest_successful_gap_24h_min"] = cov["longest_successful_gap_min"]
        service["acceptance_target"]["breached_24h"] = cov["longest_successful_gap_min"] > ACCEPTANCE_GAP_MIN
    return {"state": state, "last_scheduled_utc": iso(last), "age_min": round(age, 1) if age is not None else None,
            "stale_limit_min": stale_min, "manual_runs_since": len(manual),
            "gaps": [dict(g, start_utc=iso(g["start_ms"]), end_utc=iso(g["end_ms"])) for g in gaps],
            "rule": "scheduled runs only (manual, local and recovery runs do not close a scheduled gap)",
            "service": service, "coverage_24h": cov}


# --------------------------------------------------------------------------------------------- decisions
def range_decisions(base, now):
    import range_monitor as M
    problems, info = M.check(base, now, None, lookback_h=LOOKBACK_H)
    states = info.get("decisions", {})
    norm = {}
    for k, v in states.items():
        # "skipped" is range_job's stale-decision refusal (processed more than an hour after the close): the live
        # decision was missed even though a later run left a record, so it is a problem state here
        norm[k] = ("absent" if v == "absent" else "failed: " + v if v.startswith(("attempt", "failed")) else
                   "missed: skipped (processed after the freshness limit)" if v == "skipped" else v)
    return norm, info


def _lifecycle_at(rows_, key, t_ms):
    state, by = "proposed", None
    for r in rows_:
        if r.get("key") == key and isinstance(r.get("t_ms"), int) and r["t_ms"] <= t_ms:
            state, by = r.get("state"), r.get("by")
    return state, by


def ps1_decisions(base, now):
    base = Path(base)
    launch = jload(base / "streams/ps1/launch.json")
    if not isinstance(launch, dict) or not parse(launch.get("first_decision_utc")):
        return {}, {"launched": False}
    proto = jload(base / "desk/research/ps1/protocol.json", {}) or {}
    max_delay = int(((proto.get("execution") or {}).get("max_delay_min")) or 90)
    decs = {r.get("decision_id"): r for r in rows(base / "streams/ps1/decisions.jsonl")}
    fills = {}
    for r in rows(base / "streams/ps1/executions.jsonl"):
        if isinstance(r.get("fill_time_ms"), int):
            fills[r.get("decision_id")] = min(fills.get(r.get("decision_id"), r["fill_time_ms"]), r["fill_time_ms"])
    executed = set(fills)
    missed = {r.get("decision_id") for r in rows(base / "streams/ps1/runs.jsonl")
              if r.get("stage") == "execute" and r.get("outcome") == "missed-execution"}
    life = rows(base / "streams/ps1/lifecycle.jsonl")
    key = launch.get("protocol_sha256")
    out, t = {}, parse(launch["first_decision_utc"])
    while t <= now:
        did = f"ps1-{t:%Y%m%dT%H%MZ}"
        due = now > t + dt.timedelta(minutes=max_delay)
        st, by = _lifecycle_at(life, key, int(t.timestamp() * 1000))
        if did in executed:
            s = "executed"
        elif st in ("terminated", "archived") or (st == "paused" and by == "operator"):
            s = f"not expected (lifecycle {st}{' by ' + by if by else ''})"
        elif did in decs:
            a = decs[did].get("action")
            # 2.27: explicit actions only - an unrecognized action is an invalid record, never a resolved decision
            s = (f"invalid: unrecognized action {str(a)[:40]!r}" if a not in ("rebalance", "no-rebalance", "missed") else
                 f"missed: execution ({a})" if did in missed else
                 f"{a}" if a != "rebalance" else ("missed: not executed" if due else "pending"))
        else:
            s = "missed: no decision record (run absent)" if due else "pending"
        out[t.strftime("%Y-%m-%dT%H:%M:%SZ")] = s
        t += dt.timedelta(hours=4)
    return out, {"launched": True, "max_delay_min": max_delay, "fills": fills}


def ps1_coverage(base, now, ps1, delay=90, fills=None):
    rep = jload(Path(base) / "reports/paper_ps1.json", {}) or {}
    gen = parse(rep.get("generated_utc"))
    if gen is None:
        return {"report_generated_utc": None, "not_covered": [], "note": "no PS1 report"}
    fills, g_ms = fills or {}, gen.timestamp() * 1000
    def covered(k):     # the report resolved it: past its deadline at generation, or already filled by then
        return parse(k) + dt.timedelta(minutes=delay) <= gen or fills.get(f"ps1-{parse(k):%Y%m%dT%H%MZ}", 1e18) <= g_ms
    not_cov = [{"decision_utc": k, "recorded_state": v} for k, v in ps1.items()
               if not covered(k) and not v.startswith("pending")]
    return {"report_generated_utc": rep.get("generated_utc"), "report_coverage": rep.get("coverage"),
            "report_scheduled_decisions": rep.get("scheduled_decisions"),
            "report_age_min": round((now - gen).total_seconds() / 60, 1),
            "not_covered": not_cov,
            "rule": "the report's coverage is as of its generation; decisions due after it are listed here with "
                    "their recorded state, never folded into its percentage"}


# --------------------------------------------------------------------------------------------- availability
def availability(base, now):
    st = jload(Path(base) / "reports/range_status.json", {}) or {}
    exp = parse(st.get("status_expires_utc"))
    out = {"generated_utc": st.get("generated_utc"), "status_expires_utc": st.get("status_expires_utc"),
           "status": "unknown" if exp is None else ("expired" if now >= exp else "within expiry"), "horizons": {}}
    for h, c in sorted((st.get("current") or {}).items()):
        c = c if isinstance(c, dict) else {}
        vu = parse(c.get("valid_until_utc"))
        state = c.get("state")
        if state == "valid-current" and (out["status"] != "within expiry" or vu is None or now >= vu):
            state = "expired on this clock"
        out["horizons"][h] = {"recorded_state": c.get("state"), "state_now": state, "valid_until_utc": c.get("valid_until_utc")}
    return out


# --------------------------------------------------------------------------------------------- monitors
def monitors(now, token=None, repo=None, opener=None):
    if not (token and repo):
        return {"source": "unavailable (no GitHub token in this run)", "workflows": {},
                "state": "unknown"}
    opener = opener or urllib.request.urlopen
    out, newest = {}, None
    for wf in SCHEDULED_WORKFLOWS:
        url = f"https://api.github.com/repos/{repo}/actions/workflows/{wf}/runs?per_page=30&event=schedule"
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}",
                                                       "Accept": "application/vnd.github+json"})
            with opener(req, timeout=20) as r:
                runs = json.loads(r.read()).get("workflow_runs", [])
        except Exception as exc:                                  # noqa: BLE001 - reported as unknown
            out[wf] = {"state": "unknown", "error": type(exc).__name__}
            continue
        e, last_start = heartbeat(runs, now, MONITORS.get(wf))
        if wf in MONITORS and e.get("last_result") not in (None, "success") and e.get("last_run_id"):
            e.update(execution(e["last_run_id"], token, repo, opener, wf))
        if last_start and (newest is None or last_start > newest):
            newest = last_start
        out[wf] = e
    wf, lim = DISPATCHER
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/actions/workflows/{wf}/runs?per_page=30",
                                     headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
        with opener(req, timeout=20) as r:
            runs = json.loads(r.read()).get("workflow_runs", [])
        e, _ = heartbeat(runs, now, lim)
        e["events"] = sorted({x.get("event") for x in runs if x.get("event")})
        native = [x for x in runs if x.get("event") == "schedule"]
        e["native"], _ = heartbeat(native, now, lim)
        out[wf] = e
    except Exception as exc:                                      # noqa: BLE001 - reported as unknown
        out[wf] = {"state": "unknown", "error": type(exc).__name__}
    try:
        ext = _get(f"https://api.github.com/repos/{repo}/actions/workflows/{wf}/runs?per_page=100&event=workflow_dispatch",
                   token, opener).get("workflow_runs", [])
        timer = external_timer(ext, now)
    except Exception as exc:                                      # noqa: BLE001 - reported as unknown
        timer = {"state": "unknown", "error": type(exc).__name__}
    states = [v.get("state") for k, v in out.items() if k in MONITORS]
    detected = sorted(k for k, v in out.items() if k in MONITORS and v.get("last_check") == "found a problem")
    not_run = sorted(k for k, v in out.items() if k in MONITORS and v.get("last_executed") is False)
    return {"source": "GitHub Actions API, scheduled runs", "workflows": out,
            "newest_scheduled_start_utc": newest and newest.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "state": "stale" if "stale" in states else ("unknown" if "unknown" in states or not states else "fresh"),
            "problems_detected_by": detected, "could_not_execute": not_run,
            "rule": "state is the heartbeat (last completed run, any result); last_result is how that run ended; "
                    "last_check is what its check step did (2.28): only a check that ran and reported a finding "
                    "detected a problem - setup running, a skipped check or no runner detected nothing",
            "dispatcher_state": (out.get(DISPATCHER[0]) or {}).get("state"),
            "external_timer": timer}


CHECK_STEPS = {"watchdog.yml": "Check for a stale, missing, or failing collector",
               "range-monitor.yml": "Check the range stream"}


def _get(url, token, opener):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    with opener(req, timeout=20) as r:
        return json.loads(r.read())


def execution(run_id, token, repo, opener=None, wf=None):
    """What the monitor's CHECK did in one run (repo 2.28; 2.27 counted any executed step, so a run whose setup ran
    but whose check was skipped read "check executed"): {last_executed, last_execution, last_check}."""
    import execution as X
    opener = opener or urllib.request.urlopen
    try:
        jobs = _get(f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs?per_page=50", token, opener).get("jobs")
    except Exception as exc:                                      # noqa: BLE001 - reported as unknown
        return {"last_executed": None, "last_check": "unknown", "last_execution": f"unknown (jobs unavailable: {type(exc).__name__})"}
    if not isinstance(jobs, list):
        return {"last_executed": None, "last_check": "unknown", "last_execution": "unknown (no jobs in the response)"}
    step = CHECK_STEPS.get(wf)
    notes = None
    if step:
        failed = [j for j in jobs for s in (j.get("steps") or []) if s.get("name") == step and s.get("conclusion") == "failure"]
        if failed:
            try:
                notes = [a.get("message") for a in _get(f"https://api.github.com/repos/{repo}/check-runs/{failed[0]['id']}"
                                                       f"/annotations", token, opener) if a.get("annotation_level") == "failure"]
            except Exception:                                     # noqa: BLE001 - finding unknown
                notes = None
        outcome, ran = X.check_outcome(jobs, step, notes)
    else:
        ran = X.steps_executed(jobs)
        outcome = "unknown" if ran is None else ("steps executed" if ran else "no step executed")
    finding = next((n for n in notes or [] if not str(n).startswith(X.EXIT_ONLY)), None)
    return {"last_executed": ran, "last_check": outcome,
            "last_execution": outcome + (f": {finding[:160]}" if finding else "")}


def external_timer(runs, now, hours=24, tolerance_s=90, delayed_s=600):
    """Arrivals of the designated primary trigger - external-titled dispatcher runs - against its quarter-hour
    opportunities (:12/:27/:42/:57) over the last `hours`, apart from the native dispatcher (repo 2.28). An opportunity
    is on time (created within `tolerance_s`), delayed (within `delayed_s`), or absent. A healthy native dispatcher or
    healthy service never hides an absent external arrival; this is arrival evidence only - it says nothing about
    whether the timer sent a request (that needs the provider's history)."""
    ext = sorted(t for t in (parse(x.get("created_at")) for x in runs
                             if x.get("event") == "workflow_dispatch" and x.get("display_title") == "Recovery dispatcher (external)")
                 if t)
    end = now - dt.timedelta(seconds=delayed_s)
    t = (end - dt.timedelta(hours=hours)).replace(second=0, microsecond=0)
    while t.minute not in (12, 27, 42, 57):
        t += dt.timedelta(minutes=1)
    on, late, absent, lags = 0, [], [], []
    while t <= end:
        hit = [e for e in ext if t <= e < t + dt.timedelta(minutes=15)]
        lag = (hit[0] - t).total_seconds() if hit else None
        if lag is None or lag > delayed_s:
            absent.append(t.strftime("%Y-%m-%dT%H:%M:%SZ"))
        elif lag > tolerance_s:
            late.append({"slot": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "lag_s": round(lag)})
        else:
            on += 1
            lags.append(lag)
        t += dt.timedelta(minutes=15)
    last = ext[-1] if ext else None
    age = (now - last).total_seconds() / 60 if last else None
    n = on + len(late) + len(absent)
    return {"window_h": hours, "opportunities": n, "on_time": on, "delayed": late, "absent": absent,
            "on_time_max_lag_s": round(max(lags)) if lags else None,
            "last_arrival_utc": last and last.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "state": "silent" if age is None or age > 45 else ("gaps" if absent or late else "arriving"),
            "rule": "external-titled dispatcher runs per :12/:27/:42/:57 opportunity; arrivals only - whether the "
                    "timer sent each request needs the provider's execution history"}


def heartbeat(runs, now, limit_min):
    """(entry, last start) for one workflow's runs (repo 2.26). Heartbeat = the newest COMPLETED run whatever it found;
    last_result = that run's conclusion; last_success_utc kept separately. Before 2.26 the state used the last
    success, so a monitor that ran on time and correctly failed on a missed decision read as stale."""
    def t(x):
        return parse(x.get("run_started_at") or x.get("created_at"))
    started = [t(x) for x in runs if t(x)]
    done = sorted(((parse(x.get("updated_at")) or t(x), x) for x in runs
                   if (x.get("status") == "completed" or (x.get("status") is None and x.get("conclusion"))) and t(x)),
                  key=lambda p: p[0])
    ok = [t(x) for x in runs if x.get("conclusion") == "success" and t(x)]
    last_start = max(started) if started else None
    last_done, last_run = done[-1] if done else (None, None)
    f = lambda d: d and d.strftime("%Y-%m-%dT%H:%M:%SZ")   # noqa: E731
    e = {"last_scheduled_start_utc": f(last_start), "last_completed_utc": f(last_done),
         "last_result": last_run.get("conclusion") if last_run else None,
         "last_run_id": last_run.get("id") if last_run else None, "last_success_utc": f(max(ok) if ok else None)}
    if limit_min:
        e["stale_after_min"] = limit_min
        e["state"] = "unknown" if last_done is None else (
            "stale" if (now - last_done).total_seconds() / 60 > limit_min else "fresh")
    return e, last_start


# --------------------------------------------------------------------------------------------- assemble
def evaluate(base=ROOT, now_ms=None, token=None, repo=None, opener=None, stale_min=None):
    base = Path(base)
    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
    now = dt.datetime.fromtimestamp(now_ms / 1000, UTC)
    stale_min = stale_min or cadence.stale_minutes()
    rng, rinfo = range_decisions(base, now)
    ps1, pinfo = ps1_decisions(base, now)
    doc = {"report": "health", "schema": "health-1", "job": VERSION,
           "generated_utc": iso(now_ms), "clock": "runner UTC clock at the check (time.time)",
           "source": source(base, now_ms, stale_min),
           "decisions": {"range": rng, "ps1": ps1, "ps1_launched": pinfo.get("launched"),
                         "rule": "recorded state only; later runs, backfills and recovered bars never complete an earlier decision"},
           "ps1_coverage": ps1_coverage(base, now, ps1, pinfo.get("max_delay_min", 90), pinfo.get("fills")),
           "availability": availability(base, now),
           "scoring_backlog": rinfo.get("scoring_backlog", {}),
           "monitors": monitors(now, token, repo, opener),
           "freshness_rule": f"this report is written by the collector run; older than {stale_min} min means no "
                             "collector run has persisted a newer report - the scheduler may have been silent, the run "
                             "may not have executed (no runner), may have failed, or may have failed to persist; its "
                             "contents are not current"}
    return doc


def incidents(doc):
    """Incident rows implied by one evaluation: event times from the records, never from this clock."""
    out = []
    for g in doc["source"]["gaps"]:
        out.append({"kind": "collector_gap", "subject": "scheduled collector", "start_utc": g["start_utc"],
                    "end_utc": g["end_utc"], "minutes": g["minutes"], "status": "ongoing" if g["end_utc"] is None else "resolved"})
    for g in (doc["source"].get("service") or {}).get("gaps", []):
        out.append({"kind": "service_gap", "subject": "automated collector (native or recovery)", "start_utc": g["start_utc"],
                    "end_utc": g["end_utc"], "minutes": g["minutes"], "status": "ongoing" if g["end_utc"] is None else "resolved"})
    for stream in ("range", "ps1"):
        for k, v in doc["decisions"][stream].items():
            if any(v.startswith(p) for p in PROBLEM_STATES):
                out.append({"kind": f"{stream}_decision", "subject": k, "start_utc": k, "end_utc": k,
                            "minutes": None, "status": v})
    return out


def record(base, doc):
    """Append incidents not yet on file (key: kind, subject, start, end - an ongoing gap is recorded once open and
    once resolved). first_recorded_utc is this check's clock; recorded_after_end marks retrospective records."""
    base = Path(base)
    path = base / INCIDENTS
    have = {(r.get("kind"), r.get("subject"), r.get("start_utc"), r.get("end_utc")) for r in rows(path)}
    new = []
    for inc in incidents(doc):
        k = (inc["kind"], inc["subject"], inc["start_utc"], inc["end_utc"])
        if k in have:
            continue
        end = parse(inc["end_utc"]) if inc["end_utc"] else None
        if inc["kind"].endswith("_decision"):
            end = None
        row = dict(inc, first_recorded_utc=doc["generated_utc"], detector=VERSION, clock=doc["clock"],
                   recorded_after_end=bool(inc["kind"] in ("collector_gap", "service_gap") and inc["end_utc"] is not None))
        new.append(row)
        have.add(k)
    if new:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            for r in new:
                f.write(json.dumps(r, sort_keys=True) + "\n")
    (base / "reports").mkdir(exist_ok=True)
    (base / "reports/health.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
    (base / "reports/health.md").write_text(markdown(doc))
    return new


def markdown(doc):
    s, cov, av, mon = doc["source"], doc["ps1_coverage"], doc["availability"], doc["monitors"]
    L = ["# Operational health", "", f"Generated {doc['generated_utc']} by {doc['job']} ({doc['clock']}). {doc['freshness_rule']}.", "",
         f"**Source:** {s['state']}; last scheduled collector run {s['last_scheduled_utc']} ({s['age_min']} min). "
         f"Silences over {s['stale_limit_min']} min in the last {LOOKBACK_H} h: "
         + ("; ".join(f"{g['start_utc']} to {g['end_utc'] or 'ongoing'} ({g['minutes']:.0f} min)" for g in s["gaps"]) or "none") + ".", "",
         f"**Service continuity:** {(s.get('service') or {}).get('state')}; last persisted critical success "
         f"{(s.get('service') or {}).get('last_success_utc')} ({(s.get('service') or {}).get('data_age_min')} min); last automated "
         f"activity {(s.get('service') or {}).get('last_activity_utc')} ({(s.get('service') or {}).get('last_activity_result')}, "
         f"{(s.get('service') or {}).get('last_source')}). 45-min acceptance target "
         f"{'BREACHED' if ((s.get('service') or {}).get('acceptance_target') or {}).get('breached_now') else 'met'} now. "
         + (lambda c: (f"Last 24 h: {c['expected_slots']} slots; runs by source "
                       + ", ".join(f"{k} {v}" for k, v in sorted(c['runs_by_source'].items()))
                       + f"; {c['intervals_with_successful_automated_run']} of {c['intervals']} slot intervals hold an "
                       f"automated critical success ({c['intervals_with_automated_run']} hold any automated activity); "
                       f"longest gap between successes {c['longest_successful_gap_min']} min.") if c else "")(s.get("coverage_24h")), "",
         "**Range decisions:** " + ("; ".join(f"{k[5:16]} {v}" for k, v in list(doc["decisions"]["range"].items())[-8:]) or "none due") + ".", "",
         "**PS1 decisions:** " + ("; ".join(f"{k[5:16]} {v}" for k, v in list(doc["decisions"]["ps1"].items())[-8:]) or "not launched") + ".", "",
         f"**PS1 report coverage:** {cov.get('report_coverage')} as of {cov.get('report_generated_utc')}; due since and not covered: "
         + ("; ".join(f"{x['decision_utc'][5:16]} {x['recorded_state']}" for x in cov["not_covered"]) or "none") + ".", "",
         f"**Range availability:** status {av['status']} (expires {av['status_expires_utc']}); "
         + "; ".join(f"{h} {v['state_now']}" for h, v in av["horizons"].items()) + ".", "",
         "**Scoring backlog:** " + ("; ".join(f"{h} {len(v)}" for h, v in doc["scoring_backlog"].items()) or "none") + ".", "",
         f"**Monitors:** {mon['state']} ({mon['source']})"
         + "".join(f"; {k} heartbeat {v.get('state', 'n/a')} (last run {v.get('last_completed_utc')}: {v.get('last_result')}"
                   + (f", {v['last_execution']}" if v.get('last_execution') else "") + f"; last success {v.get('last_success_utc')})"
                   for k, v in mon["workflows"].items() if k in MONITORS)
         + (f"; newest scheduled start of any workflow {mon.get('newest_scheduled_start_utc')}" if mon.get("newest_scheduled_start_utc") else "") + ".", "",
         (lambda t: f"**External timer (primary trigger):** {t.get('state')}; {t.get('on_time')} of {t.get('opportunities')} "
                    f"opportunities on time in {t.get('window_h')} h, {len(t.get('delayed') or [])} delayed, absent "
                    + (", ".join(t.get('absent') or []) or "none") + f"; last arrival {t.get('last_arrival_utc')}. Arrivals "
                    "only: whether each request was sent needs the provider's history." if isinstance(t, dict) and "opportunities" in t
                    else "**External timer:** unknown.")(mon.get("external_timer") or {}), ""]
    return "\n".join(L)


def main(argv):
    doc = evaluate(token=os.environ.get("GITHUB_TOKEN"), repo=os.environ.get("GITHUB_REPOSITORY"))
    if "--record" in argv:
        new = record(ROOT, doc)
        print(f"health: {len(new)} new incident(s) recorded; reports/health.json written")
    else:
        print(json.dumps(doc, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
