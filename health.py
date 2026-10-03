#!/usr/bin/env python3
"""health - operational health of the desk, one dimension at a time, on an explicit clock (repo 2.24).

Five questions are kept apart, because each fails differently and a green answer to one says nothing about
another:
  source      the collector's scheduled cadence: last scheduled run, its age, and every silence longer than the
              stale limit (cadence.scheduled_gaps), recovered or ongoing. A recovered gap stays listed.
  decisions   expected 4H work: the range stream (published / skipped / failed / absent, desk/range_monitor.py's
              rules) and PS1 after its launch (executed / no-rebalance / missed-execution / no decision record /
              not expected under an operator pause or termination / pending inside its deadline). Recorded
              state only: a later run, a backfill or recovered price bars never complete an earlier decision.
  coverage    PS1's coverage is as of its report's generation; decisions that fell due after that are listed
              separately with their recorded state (the report is never re-run from here).
  availability the range status file judged on this check's clock (its own exact expiry rules).
  scoring     matured, eligible RC1D forecasts still unscored (the monitor's backlog rule).
  monitors    last successful watchdog and range-monitor runs and the newest scheduled run of any workflow
              (GitHub API, when a token is given); unknown without one. An old success is never current health.

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

VERSION = "health-1.0.0"
UTC = dt.timezone.utc
LOOKBACK_H = 72                   # decisions and gaps examined (incidents already recorded stay recorded)
MONITORS = {"watchdog.yml": 90, "range-monitor.yml": 510}   # minutes: 90 = the collector stale limit (three
#   30-minute watchdog slots); 510 = 8.5 h, the range monitor's publication limit (two 4-hourly slots + grace)
SCHEDULED_WORKFLOWS = ("collect.yml", "watchdog.yml", "dashboard.yml", "intake.yml", "range-score.yml", "range.yml",
                       "research-streams.yml", "range-monitor.yml", "research.yml")
INCIDENTS = "state/incidents.jsonl"
PROBLEM_STATES = ("absent", "failed", "missed", "no decision record")


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
    manual = [r for r in runs if cadence.is_routine(r) and not cadence.schedule_evidence(r) and (not last or r["t"] > last)]
    return {"state": state, "last_scheduled_utc": iso(last), "age_min": round(age, 1) if age is not None else None,
            "stale_limit_min": stale_min, "manual_runs_since": len(manual),
            "gaps": [dict(g, start_utc=iso(g["start_ms"]), end_utc=iso(g["end_ms"])) for g in gaps],
            "rule": "scheduled runs only (manual and local runs do not close a scheduled gap)"}


# --------------------------------------------------------------------------------------------- decisions
def range_decisions(base, now):
    import range_monitor as M
    problems, info = M.check(base, now, None, lookback_h=LOOKBACK_H)
    states = info.get("decisions", {})
    norm = {}
    for k, v in states.items():
        norm[k] = ("absent" if v == "absent" else "failed: " + v if v.startswith(("attempt", "failed")) else v)
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
            s = (f"missed: execution ({a})" if did in missed else
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
        started = [parse(x.get("run_started_at") or x.get("created_at")) for x in runs]
        started = [s for s in started if s]
        ok = [parse(x.get("run_started_at") or x.get("created_at")) for x in runs if x.get("conclusion") == "success"]
        ok = [s for s in ok if s]
        last_start, last_ok = (max(started) if started else None), (max(ok) if ok else None)
        if last_start and (newest is None or last_start > newest):
            newest = last_start
        e = {"last_scheduled_start_utc": last_start and last_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
             "last_success_utc": last_ok and last_ok.strftime("%Y-%m-%dT%H:%M:%SZ")}
        if wf in MONITORS:
            lim = MONITORS[wf]
            e["stale_after_min"] = lim
            e["state"] = "unknown" if last_ok is None else ("stale" if (now - last_ok).total_seconds() / 60 > lim else "fresh")
        out[wf] = e
    states = [v.get("state") for k, v in out.items() if k in MONITORS]
    return {"source": "GitHub Actions API, scheduled runs", "workflows": out,
            "newest_scheduled_start_utc": newest and newest.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "state": "stale" if "stale" in states else ("unknown" if "unknown" in states or not states else "fresh")}


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
           "freshness_rule": f"this report is written by the collector run; older than {stale_min} min means the "
                             "collector (and probably GitHub's scheduler) has been silent - its contents are not current"}
    return doc


def incidents(doc):
    """Incident rows implied by one evaluation: event times from the records, never from this clock."""
    out = []
    for g in doc["source"]["gaps"]:
        out.append({"kind": "collector_gap", "subject": "scheduled collector", "start_utc": g["start_utc"],
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
                   recorded_after_end=bool(inc["kind"] == "collector_gap" and inc["end_utc"] is not None))
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
         "**Range decisions:** " + ("; ".join(f"{k[5:16]} {v}" for k, v in list(doc["decisions"]["range"].items())[-8:]) or "none due") + ".", "",
         "**PS1 decisions:** " + ("; ".join(f"{k[5:16]} {v}" for k, v in list(doc["decisions"]["ps1"].items())[-8:]) or "not launched") + ".", "",
         f"**PS1 report coverage:** {cov.get('report_coverage')} as of {cov.get('report_generated_utc')}; due since and not covered: "
         + ("; ".join(f"{x['decision_utc'][5:16]} {x['recorded_state']}" for x in cov["not_covered"]) or "none") + ".", "",
         f"**Range availability:** status {av['status']} (expires {av['status_expires_utc']}); "
         + "; ".join(f"{h} {v['state_now']}" for h, v in av["horizons"].items()) + ".", "",
         "**Scoring backlog:** " + ("; ".join(f"{h} {len(v)}" for h, v in doc["scoring_backlog"].items()) or "none") + ".", "",
         f"**Monitors:** {mon['state']} ({mon['source']})"
         + "".join(f"; {k} last success {v.get('last_success_utc')} ({v.get('state', 'n/a')})" for k, v in mon["workflows"].items() if k in MONITORS)
         + (f"; newest scheduled start of any workflow {mon.get('newest_scheduled_start_utc')}" if mon.get("newest_scheduled_start_utc") else "") + ".", ""]
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
