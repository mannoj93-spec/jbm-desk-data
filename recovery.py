#!/usr/bin/env python3
"""recovery - dispatch the desk's time-critical work when GitHub's native schedule has not started it (repo 2.25).

Native scheduling degraded from Oct 3 2026 (docs/incidents/2026-10-03-native-schedule.md). This dispatcher is started
from outside GitHub's scheduler (an external cron calling workflow_dispatch on .github/workflows/recovery.yml, plus a
native schedule of its own as a fallback) and dispatches, with the workflow token, only work that is due and that no
run has covered. Every dispatched run carries inputs trigger=recovery, slot=<key> and origin=<this run>:<its source>,
and is labelled by provenance.py; native cadence health never counts it.

What is due (UTC; derived from the contracts, not tuned to results):
  collector       the latest 15-minute slot (cadence.json) at least COLLECTOR_GRACE_MIN old with no run created since
                  it. One dispatch per slot. A recovery collector run yields (collects nothing) when a run record
                  already exists at or after its slot (`recovery.py covered`), so a late native run and a recovery run
                  never both collect one slot.
  range           the latest 4H decision, between RANGE_GRACE_MIN and RANGE_LAST_DISPATCH_MIN after the close, with no
                  run created since the close, or only failed ones (at most RANGE_MAX_DISPATCHES per decision).
                  range_job refuses a decision older than 1.0 h at its forecast step; a dispatch at +45 min leaves
                  15 min for runner start (~1), the repo-write queue (one collector or stream job, ~2-3 each) and the
                  preflight/refit steps (~2). The job itself is idempotent: an already registered decision returns
                  "existing"; one with a recorded window is never retried.
  research streams after the decision's range run completed (or from 50 min after the close when none did), when no
                  streams run started since: normally workflow_run starts it at once; this covers a dropped chain.
                  Dispatched until STREAMS_LAST_DISPATCH_MIN, inside PS1's 90-minute execution deadline.
  range scoring   no run created for SCORING_STALE_MIN (hourly schedule + 10 min).
At most one dispatch per workflow per invocation; listing failures dispatch nothing; every dispatch failure fails the
run. It never cancels, re-runs or edits a run, and never touches research state.

  python recovery.py plan [--now ISO]      print what would be dispatched (read-only; needs GITHUB_TOKEN)
  python recovery.py dispatch              plan and dispatch (GITHUB_TOKEN with actions: write)
  python recovery.py covered --slot ISO    yield check for a recovery collector run: covered=true|false
Stdlib only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION = "recovery-1.0.0"
UTC = dt.timezone.utc
API = "https://api.github.com"
_sleep = time.sleep                # between API retries; replaced in tests

COLLECTOR_GRACE_MIN = 4
RANGE_GRACE_MIN = 8               # native cron is :02 after each 4H close; give it 6 more minutes
RANGE_LAST_DISPATCH_MIN = 45      # 60-minute freshness limit minus start, queue and preflight headroom
RANGE_MAX_DISPATCHES = 2
STREAMS_DELAY_MIN = 3             # after the range run completes, leave workflow_run time to start
STREAMS_FALLBACK_MIN = 50         # the streams workflow's own fallback cron
STREAMS_LAST_DISPATCH_MIN = 75    # PS1 executes within 90 minutes of the decision
SCORING_STALE_MIN = 70

WORKFLOWS = {"collector": ("collect.yml", "Collector"), "range": ("range.yml", "Range forecasts"),
             "streams": ("research-streams.yml", "Research streams"), "scoring": ("range-score.yml", "Range scoring")}


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def title(name, key):
    """The run-name a recovery dispatch gets (each target workflow's run-name expression produces exactly this)."""
    return f"{name} recovery {key}"


def live(run):
    return run.get("conclusion") != "cancelled"


def created(run):
    return parse(run.get("created_at"))


def finished(run):
    return parse(run.get("updated_at")) if run.get("status") == "completed" else None


def collector_slot(now, minutes=None):
    """Latest nominal collector slot at least COLLECTOR_GRACE_MIN old (cadence.json's current period)."""
    if minutes is None:
        import cadence
        periods = cadence.load(ROOT)
        minutes = periods[-1][1] if periods else [7, 22, 37, 52]
    t = now - dt.timedelta(minutes=COLLECTOR_GRACE_MIN)
    hour = t.replace(minute=0, second=0, microsecond=0)
    for h in (hour, hour - dt.timedelta(hours=1)):
        for m in sorted(minutes, reverse=True):
            s = h + dt.timedelta(minutes=m)
            if s <= t:
                return s
    return None


def decision(now):
    return now.replace(hour=now.hour // 4 * 4, minute=0, second=0, microsecond=0)


def plan(now, runs, minutes=None):
    """[(workflow key, slot key, reason)] due now. runs: {workflow key: [run dicts from the Actions API]}."""
    out = []
    # collector
    slot = collector_slot(now, minutes)
    if slot:
        rs = runs.get("collector", [])
        key = iso(slot)
        if not any(live(r) and created(r) >= slot for r in rs):
            if not any(r.get("display_title") == title("Collector", key) for r in rs):
                out.append(("collector", key, f"no collector run since slot {key}"))
    # range, streams
    d = decision(now)
    age = (now - d).total_seconds() / 60
    key = iso(d)
    rr = [r for r in runs.get("range", []) if live(r) and created(r) >= d]
    mine = [r for r in runs.get("range", []) if r.get("display_title") == title("Range forecasts", key)]
    if RANGE_GRACE_MIN <= age <= RANGE_LAST_DISPATCH_MIN and len(mine) < RANGE_MAX_DISPATCHES:
        if not rr:
            out.append(("range", key, f"no range run for decision {key} after {age:.0f} min"))
        elif all(r.get("status") == "completed" and r.get("conclusion") == "failure" for r in rr):
            out.append(("range", key, f"every range run for decision {key} failed; retry {len(mine) + 1} of "
                                      f"{RANGE_MAX_DISPATCHES}"))
    done = [finished(r) for r in rr if finished(r)]
    anchor = max(done) if done else (d + dt.timedelta(minutes=STREAMS_FALLBACK_MIN) if not rr else None)
    if anchor and age <= STREAMS_LAST_DISPATCH_MIN and now >= anchor + dt.timedelta(minutes=STREAMS_DELAY_MIN):
        ss = runs.get("streams", [])
        if not any(live(r) and created(r) >= anchor - dt.timedelta(minutes=1) for r in ss) and \
                not any(r.get("display_title") == title("Research streams", key) for r in ss):
            out.append(("streams", key, f"no research-streams run since {iso(anchor)}"))
    # scoring
    sc = [created(r) for r in runs.get("scoring", []) if live(r)]
    if not sc or (now - max(sc)).total_seconds() / 60 > SCORING_STALE_MIN:
        hk = iso(now.replace(minute=0, second=0, microsecond=0))
        if not any(r.get("display_title") == title("Range scoring", hk) for r in runs.get("scoring", [])):
            out.append(("scoring", hk, "no range-scoring run for "
                                       + (f"{(now - max(sc)).total_seconds() / 60:.0f} min" if sc else "the listed history")))
    return out


# ------------------------------------------------------------------------------------------------ GitHub API
def _request(method, url, token, body=None, opener=None, tries=2):
    opener = opener or urllib.request.urlopen
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for i in range(tries):
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28", **({"Content-Type": "application/json"} if data else {})})
        try:
            with opener(req, timeout=20) as r:
                raw = r.read()
                return r.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return e.code, None
            last = f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = type(e).__name__
        if i + 1 < tries:
            _sleep(3)
    raise RuntimeError(f"{method} {url.split('/repos/')[-1]}: {last}")


def list_runs(repo, token, opener=None):
    out = {}
    for key, (wf, _) in WORKFLOWS.items():
        status, body = _request("GET", f"{API}/repos/{repo}/actions/workflows/{wf}/runs?per_page=40", token, opener=opener)
        if status != 200:
            raise RuntimeError(f"listing {wf}: HTTP {status}")
        out[key] = [{k: r.get(k) for k in ("id", "event", "status", "conclusion", "created_at", "updated_at",
                                            "display_title")} for r in (body or {}).get("workflow_runs", [])]
    return out


def dispatch(repo, token, items, origin, opener=None, ref="main"):
    results = []
    for wkey, slot, reason in items:
        wf = WORKFLOWS[wkey][0]
        try:
            status, _ = _request("POST", f"{API}/repos/{repo}/actions/workflows/{wf}/dispatches", token,
                                 {"ref": ref, "inputs": {"trigger": "recovery", "slot": slot, "origin": origin}},
                                 opener=opener)
            ok = status in (200, 204)
            results.append({"workflow": wf, "slot": slot, "reason": reason, "ok": ok,
                            "status": status, **({} if ok else {"error": f"HTTP {status}"})})
        except RuntimeError as e:
            results.append({"workflow": wf, "slot": slot, "reason": reason, "ok": False, "error": str(e)})
    return results


# ------------------------------------------------------------------------------------------------ yield check
def covered(base, slot):
    """True when a collector run record (any trigger) exists at or after the slot: the slot is already collected."""
    sys.path.insert(0, str(ROOT))
    from watchdog import load_runs
    ms = int(slot.timestamp() * 1000)
    return any(r.get("t", 0) >= ms and r.get("mode") in ("routine", "hourly") for r in load_runs(base))


def origin_label(env=None):
    import provenance
    env = os.environ if env is None else env
    src = provenance.source(env)
    if src == "human" and (env.get("DESK_DISPATCH_TRIGGER") or "").strip() == "external":
        src = "external"            # declared by the caller; the token is the owner's, so the label is a declaration
    return f"{env.get('GITHUB_RUN_ID', 'local')}:{src}"


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "plan"
    if cmd == "covered":
        slot = parse(argv[argv.index("--slot") + 1]) if "--slot" in argv else None
        if slot is None:
            print("covered needs --slot", file=sys.stderr)
            return 2
        yes = covered(ROOT, slot)
        print(f"covered={'true' if yes else 'false'}")
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"covered={'true' if yes else 'false'}\n")
        return 0
    if cmd not in ("plan", "dispatch"):
        print(__doc__)
        return 2
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not (token and repo):
        print("recovery: GITHUB_TOKEN and GITHUB_REPOSITORY are required", file=sys.stderr)
        return 2
    now = parse(argv[argv.index("--now") + 1]) if "--now" in argv else dt.datetime.now(UTC)
    try:
        runs = list_runs(repo, token)
    except RuntimeError as e:
        print(f"::error title=Recovery dispatcher::Actions API unavailable ({e}); nothing dispatched")
        return 1
    items = plan(now, runs)
    doc = {"job": VERSION, "now_utc": iso(now), "origin": origin_label(), "due": [list(i) for i in items]}
    if cmd == "dispatch" and items:
        doc["dispatched"] = dispatch(repo, token, items, doc["origin"])
    print(json.dumps(doc, indent=1))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write(f"### Recovery dispatcher ({doc['origin']})\n\n" + ("".join(
                f"- {w} {s}: {r}\n" for w, s, r in items) or "Nothing due: native or earlier runs covered everything.\n"))
            for d in doc.get("dispatched", []):
                f.write(f"- dispatched {d['workflow']} {d['slot']}: {'ok' if d['ok'] else d['error']}\n")
    failed = [d for d in doc.get("dispatched", []) if not d["ok"]]
    for d in failed:
        print(f"::error title=Recovery dispatch failed::{d['workflow']} {d['slot']}: {d['error']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
