#!/usr/bin/env python3
"""recovery - dispatch the desk's time-critical work when GitHub's native schedule has not started it (repo 2.25).

Native scheduling degraded from Oct 3 2026 (docs/incidents/2026-10-03-native-schedule.md). This dispatcher is started
from outside GitHub's scheduler (an external cron calling workflow_dispatch on .github/workflows/recovery.yml, plus a
native schedule of its own as a fallback) and dispatches, with the workflow token, only work that is due and that no
run has covered. Every dispatched run carries inputs trigger=recovery, slot=<key> and origin=<this run>:<its source>,
and is labelled by provenance.py; native cadence health never counts it.

What is due (UTC; derived from the contracts, not tuned to results):
  collector       the latest 15-minute slot (cadence.json) at least COLLECTOR_GRACE_MIN old with no run since it that
                  can still collect it (progressing(): succeeded, in progress, or queued < 10 min - 1.3.0). At most
                  COLLECTOR_MAX_DISPATCHES (2) per slot. A recovery collector run yields (collects nothing) only when a
                  CRITICALLY SUCCESSFUL record already exists at or after its slot (`recovery.py covered`), and leaves a
                  durable yield receipt naming that record; a failed record never covers a slot.
  range           the latest 4H decision, between RANGE_GRACE_MIN and RANGE_LAST_DISPATCH_MIN after the close, with no
                  run since the close that succeeded or is progressing - failed, cancelled, never-started (no runner)
                  and long-queued runs do not count (1.3.0) - at most RANGE_MAX_DISPATCHES per decision.
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
  python recovery.py covered --slot ISO [--receipt]
                                           yield check for a recovery collector run: covered=true|false; only a
                                           CRITICALLY SUCCESSFUL record covers (1.3.0); --receipt appends the
                                           durable yield proof to state/recovery_yields.jsonl
  python recovery.py chain --slot ISO      from a recovery range run: dispatch the research streams for its decision
                                           (1.1.0; a token-started run raises no workflow_run event)
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
VERSION = "recovery-1.3.0"
UTC = dt.timezone.utc
API = "https://api.github.com"
PRODUCTION_REF = "main"
_sleep = time.sleep                # between API retries; replaced in tests

COLLECTOR_GRACE_MIN = 4
RANGE_GRACE_MIN = 8               # native cron is :02 after each 4H close; give it 6 more minutes
RANGE_LAST_DISPATCH_MIN = 45      # 60-minute freshness limit minus start, queue and preflight headroom
RANGE_MAX_DISPATCHES = 2
STREAMS_DELAY_MIN = 3             # after the range run completes, leave workflow_run time to start
STREAMS_FALLBACK_MIN = 50         # the streams workflow's own fallback cron
STREAMS_LAST_DISPATCH_MIN = 75    # PS1 executes within 90 minutes of the decision
SCORING_STALE_MIN = 70
# 1.3.0 (repo 2.27): a run suppresses a dispatch only while it can still do the work - completed successfully, in
# progress (bounded), or queued for less than the wait below. A run that failed, was cancelled, never received a
# runner or has been queued longer no longer suppresses, so dead attempts cannot block recovery indefinitely; the
# per-key caps bound retries (at most two dispatches per collector slot, range decision or streams decision).
QUEUE_WAIT_MIN = {"collector": 10, "range": 10, "streams": 10, "scoring": 20}
IN_PROGRESS_MAX_MIN = 40
COLLECTOR_MAX_DISPATCHES = 2
STREAMS_MAX_DISPATCHES = 2
WAITING = ("queued", "pending", "waiting", "requested")
YIELDS = "state/recovery_yields.jsonl"

WORKFLOWS = {"collector": ("collect.yml", "Collector"), "range": ("range.yml", "Range forecasts"),
             "streams": ("research-streams.yml", "Research streams"), "scoring": ("range-score.yml", "Range scoring")}


def parse(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def title(name, key):
    """The run-name stem a recovery dispatch gets. From 2.26 each target's run-name appends " via <origin>", so the
    chain's root is visible in the Actions run list (service_acceptance reads it); is_title matches either form."""
    return f"{name} recovery {key}"


def is_title(display, name, key):
    stem = title(name, key)
    return isinstance(display, str) and (display == stem or display.startswith(stem + " via "))


def via(display):
    """The origin a recovery run's title carries ("<root run>:<label>[:<parent>]"), or None."""
    return display.split(" via ", 1)[1] if isinstance(display, str) and " via " in display else None


def live(run):
    return run.get("conclusion") != "cancelled"


def progressing(run, now, wait_min):
    """Can this run still do (or has it done) the work? completed -> only a success; in progress -> for at most
    IN_PROGRESS_MAX_MIN; queued/pending -> for at most wait_min after creation. Never-started, failed, cancelled and
    long-queued runs do not (repo 2.27)."""
    st, c = run.get("status"), created(run)
    if st == "completed":
        return run.get("conclusion") == "success"
    if c is None:
        return False
    age = (now - c).total_seconds() / 60
    if st in WAITING:
        return age <= wait_min
    if st == "in_progress":
        return age <= IN_PROGRESS_MAX_MIN
    return False


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
    """[(workflow key, slot key, reason)] due now. runs: {workflow key: [run dicts from the Actions API]}.
    Only production-ref runs are considered (production()); a run without head_branch is not production."""
    runs = production(runs)
    out = []
    # collector
    slot = collector_slot(now, minutes)
    if slot:
        rs = runs.get("collector", [])
        key = iso(slot)
        since = [r for r in rs if created(r) and created(r) >= slot]
        mine = [r for r in rs if is_title(r.get("display_title"), "Collector", key)]
        if not any(progressing(r, now, QUEUE_WAIT_MIN["collector"]) for r in since) and len(mine) < COLLECTOR_MAX_DISPATCHES:
            out.append(("collector", key, f"no collector run able to collect slot {key}"
                                          + (f" ({len(since)} run(s) since it failed, never started or stalled; "
                                             f"dispatch {len(mine) + 1} of {COLLECTOR_MAX_DISPATCHES})" if since else "")))
    # range, streams
    d = decision(now)
    age = (now - d).total_seconds() / 60
    key = iso(d)
    rr = [r for r in runs.get("range", []) if created(r) and created(r) >= d]
    mine = [r for r in runs.get("range", []) if is_title(r.get("display_title"), "Range forecasts", key)]
    if RANGE_GRACE_MIN <= age <= RANGE_LAST_DISPATCH_MIN and len(mine) < RANGE_MAX_DISPATCHES \
            and not any(progressing(r, now, QUEUE_WAIT_MIN["range"]) for r in rr):
        out.append(("range", key, f"no range run for decision {key} after {age:.0f} min" if not rr else
                                  f"no range run for decision {key} succeeded or is progressing ({len(rr)} failed, "
                                  f"never started or stalled); retry {len(mine) + 1} of {RANGE_MAX_DISPATCHES}"))
    done = [finished(r) for r in rr if finished(r)]
    if done:
        anchor = max(done)
    elif not any(progressing(r, now, QUEUE_WAIT_MIN["range"]) for r in rr):
        anchor = d + dt.timedelta(minutes=STREAMS_FALLBACK_MIN)
    else:
        anchor = None
    if anchor and age <= STREAMS_LAST_DISPATCH_MIN and now >= anchor + dt.timedelta(minutes=STREAMS_DELAY_MIN):
        ss = runs.get("streams", [])
        smine = [r for r in ss if is_title(r.get("display_title"), "Research streams", key)]
        if not any(progressing(r, now, QUEUE_WAIT_MIN["streams"]) and created(r) >= anchor - dt.timedelta(minutes=1)
                   for r in ss) and len(smine) < STREAMS_MAX_DISPATCHES:
            out.append(("streams", key, f"no research-streams run progressing since {iso(anchor)}"))
    # scoring
    sc = [created(r) for r in runs.get("scoring", []) if progressing(r, now, QUEUE_WAIT_MIN["scoring"])]
    if not sc or (now - max(sc)).total_seconds() / 60 > SCORING_STALE_MIN:
        hk = iso(now.replace(minute=0, second=0, microsecond=0))
        if not any(is_title(r.get("display_title"), "Range scoring", hk) for r in runs.get("scoring", [])):
            out.append(("scoring", hk, "no successful or progressing range-scoring run for "
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


def list_runs(repo, token, opener=None, ref=None):
    ref = ref or PRODUCTION_REF
    out = {}
    for key, (wf, _) in WORKFLOWS.items():
        status, body = _request("GET", f"{API}/repos/{repo}/actions/workflows/{wf}/runs?per_page=40&branch={ref}",
                                token, opener=opener)
        if status != 200:
            raise RuntimeError(f"listing {wf}: HTTP {status}")
        runs = (body or {}).get("workflow_runs")
        if not isinstance(runs, list):
            raise RuntimeError(f"listing {wf}: no workflow_runs in the response")
        out[key] = [{k: r.get(k) for k in ("id", "event", "status", "conclusion", "created_at", "updated_at",
                                            "display_title", "head_branch")} for r in runs]
    return out


def production(runs, ref=PRODUCTION_REF):
    """Only runs of the production ref may cover, suppress or anchor recovery (repo 2.26): a run on another branch,
    or one whose branch is not stated, never counts as production work."""
    return {k: [r for r in v if r.get("head_branch") == ref] for k, v in runs.items()}


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
def covering(base, slot):
    """The stored run record that already collected the slot (repo 2.27): the first CRITICALLY SUCCESSFUL routine
    record (cadence.critical_success) at or after the slot, else None. A critical-failed record does not cover a
    slot - the recovery run then collects."""
    sys.path.insert(0, str(ROOT))
    import cadence
    from watchdog import load_runs
    ms = int(slot.timestamp() * 1000)
    for r in load_runs(base):
        if r.get("t", 0) >= ms and cadence.critical_success(r):
            return r
    return None


def covered(base, slot):
    return covering(base, slot) is not None


def record_sha256(rec):
    import hashlib
    return hashlib.sha256(json.dumps(rec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def yield_receipt(slot, rec, env=None, now=None):
    """The durable proof of a legitimate no-op (repo 2.27): the slot, the yielding run and the identity, quality and
    time of the already-persisted record that covered it. A title or a missing output is never proof of a yield."""
    env = os.environ if env is None else env
    now = now or dt.datetime.now(UTC)
    return {"schema": "recovery-yield/1", "slot": iso(slot), "run_id": str(env.get("GITHUB_RUN_ID") or ""),
            "run_attempt": str(env.get("GITHUB_RUN_ATTEMPT") or ""), "workflow": "collect.yml",
            "ref": env.get("GITHUB_REF_NAME") or None, "checked_utc": iso(now), "tool": VERSION,
            "covering": {"run_id": str(rec.get("run_id")), "t": rec.get("t"), "trigger": rec.get("trigger"),
                         "critical_ok": rec.get("critical_ok"), "record_sha256": record_sha256(rec)}}


def valid_yield(receipt, records, run=None):
    """(ok, reason) for one yield receipt against the stored records and, when given, the Actions run it names."""
    import cadence
    if not isinstance(receipt, dict) or receipt.get("schema") != "recovery-yield/1":
        return False, "not a recovery-yield/1 receipt"
    slot = parse(receipt.get("slot"))
    cov = receipt.get("covering") or {}
    if slot is None or not receipt.get("run_id"):
        return False, "receipt without slot or run"
    if run is not None:
        if str(run.get("id")) != str(receipt["run_id"]) or run.get("head_branch") != PRODUCTION_REF:
            return False, "receipt does not name this production run"
        if not is_title(run.get("display_title"), "Collector", iso(slot)):
            return False, "receipt slot differs from the run's dispatched slot"
    match = [r for r in records if str(r.get("run_id")) == str(cov.get("run_id")) and r.get("t") == cov.get("t")]
    if not match:
        return False, "covering record not stored"
    rec = match[0]
    if record_sha256(rec) != cov.get("record_sha256"):
        return False, "covering record differs from the one the receipt names"
    if not cadence.critical_success(rec):
        return False, "covering record is not a critical success"
    if rec["t"] < int(slot.timestamp() * 1000):
        return False, "covering record predates the slot"
    checked = parse(receipt.get("checked_utc"))
    if checked is None or checked.timestamp() * 1000 < rec["t"]:
        return False, "receipt checked before the covering record existed"
    return True, "verified"


def origin_label(env=None):
    """The dispatcher is a chain's root: "<its run id>:<native-schedule | external | human>"."""
    import provenance
    env = os.environ if env is None else env
    src = provenance.source(env)
    if src == "human" and (env.get("DESK_DISPATCH_TRIGGER") or "").strip() == "external":
        src = "external"            # declared by the caller; the token is the owner's, so the label is a declaration
    if src not in provenance.ROOT_LABELS:
        src = "human" if env.get("GITHUB_EVENT_NAME") == "workflow_dispatch" else src
    return f"{env.get('GITHUB_RUN_ID', 'local')}:{src}"


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "plan"
    if cmd == "covered":
        slot = parse(argv[argv.index("--slot") + 1]) if "--slot" in argv else None
        if slot is None:
            print("covered needs --slot", file=sys.stderr)
            return 2
        rec = covering(ROOT, slot)
        yes = rec is not None
        print(f"covered={'true' if yes else 'false'}")
        if yes and "--receipt" in argv:
            rc = yield_receipt(slot, rec)
            path = ROOT / YIELDS
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a") as f:
                f.write(json.dumps(rc, sort_keys=True) + "\n")
            print(json.dumps(rc))
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"covered={'true' if yes else 'false'}\n")
        return 0
    if cmd == "chain":
        slot = argv[argv.index("--slot") + 1] if "--slot" in argv else ""
        token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
        if not (slot and token and repo):
            print("chain needs --slot, GITHUB_TOKEN and GITHUB_REPOSITORY", file=sys.stderr)
            return 2
        import provenance
        res = dispatch(repo, token, [("streams", slot, "chained from the recovery range run")],
                       provenance.child_origin())                   # 1.2.0: the chain's root passed on
        print(json.dumps(res))
        if not res[0]["ok"]:
            print(f"::error title=Recovery chain failed::research streams {slot}: {res[0].get('error')}")
            return 1
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
