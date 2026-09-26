#!/usr/bin/env python3
"""range_monitor — health check of the desk's range stream (crypto-desk 12.2, repo 2.17).

Stdlib only and independent of the forecasting modules (it never imports them), so it keeps working when
the forecast test suite fails. Read-only: it inspects the repository's own records and, when a token is
available, the GitHub Actions run list of range.yml. Scheduled by .github/workflows/range-monitor.yml.

Checks (each problem is one line; exit 1 when any exists, 0 when healthy):
  runs         each due 4H decision in the lookback has a published attempt, a recorded skip, or is flagged:
               failed (lifecycle or attempt log, with its stage and reason) or absent (no record at all)
  publication  hours since the last eligible publication (confirmed before its window start)
  freshness    reports/range_status.json regenerated within the stale limit
  scoring      eligible forecasts matured more than SCORE_LAG_MIN ago with no score record, per horizon
  actions      (token only) failed or missing scheduled range.yml runs the repository has no record of
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

VERSION = "monitor-12.2.0"
UTC = dt.timezone.utc
GRACE_MIN = 75            # a decision is due once its run window (grace) has passed
LOOKBACK_H = 12            # due decisions checked for failed or absent runs (older ones: info only)
PUBLICATION_STALE_H = 8.5  # two missed decisions plus grace
STATUS_STALE_MIN = 150     # hourly scoring refreshes the status; 2.5 h without it is stale
SCORE_LAG_MIN = 150        # a matured, eligible forecast unscored for this long is backlog
MATURITY_MIN = 5


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _rows(path):
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


def _json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, ValueError):
        return default


def boundary(now):
    return now.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=now.hour % 4)


def check(base, now, actions=None) -> tuple:
    """(problems, info). `actions`: optional list of range.yml runs [{run_id, event, created_utc, conclusion}]."""
    base = Path(base)
    problems, info = [], {"monitor": VERSION, "now_utc": _iso(now)}
    attempts = [a for a in _rows(base / "state/range_attempts.jsonl")
                if isinstance(a.get("run"), dict) and a["run"].get("production") and isinstance(a.get("decision_utc"), str)]
    runs = [r for r in _rows(base / "state/range_runs.jsonl") if isinstance(r.get("decision_utc"), str)
            and r.get("event") in ("schedule", "workflow_dispatch")]
    pubs = [p for p in _rows(base / "state/range_publications.jsonl") if p.get("eligible") is True]
    release = _json(base / "desk/release.json", {})
    stream_start = _t(release["range_stream_start_utc"]) if isinstance(release.get("range_stream_start_utc"), str) else None
    # runs
    last_due = boundary(now) if now - boundary(now) >= dt.timedelta(minutes=GRACE_MIN) else boundary(now) - dt.timedelta(hours=4)
    d = max(last_due - dt.timedelta(hours=LOOKBACK_H), stream_start or last_due)
    seen = {}
    while d <= last_due:
        key = _iso(d)
        mine = [a for a in attempts if a["decision_utc"] == key]
        life = [r for r in runs if r["decision_utc"] == key]
        final = mine[-1].get("state") if mine else None
        if final == "published":
            seen[key] = "published"
        elif final == "skipped":
            seen[key] = "skipped"
        elif final is not None:
            seen[key] = f"attempt {final}"
            problems.append(f"runs: decision {key}: attempt ended {final}: {mine[-1].get('reason') or ''}".rstrip(": "))
        elif life:
            lr = life[-1]
            fails = [r for r in life if r.get("outcome") in ("failure", "cancelled", "failed")]
            why = (f"{fails[0].get('stage')} {fails[0].get('outcome')}" + (f": {fails[0].get('reason')}" if fails[0].get("reason") else "")) \
                if fails else f"last record {lr.get('stage')} {lr.get('outcome')}"
            seen[key] = "failed before forecasting"
            problems.append(f"runs: decision {key}: run {lr.get('run_id')} produced no attempt ({why})")
        else:
            seen[key] = "absent"
            problems.append(f"runs: decision {key}: no attempt and no run record (run absent or failed before persisting)")
        d += dt.timedelta(hours=4)
    info["decisions"] = seen
    # publication
    if pubs:
        last = max(pubs, key=lambda p: p.get("start_ms", 0))
        age_h = (now - dt.datetime.fromtimestamp(last["start_ms"] / 1000, UTC)).total_seconds() / 3600
        info["last_eligible_publication"] = {"attempt": last.get("attempt"), "age_hours": round(age_h, 2)}
        if age_h > PUBLICATION_STALE_H:
            problems.append(f"publication: last eligible publication {last.get('attempt')} is {age_h:.1f} h old")
    elif stream_start and now - stream_start > dt.timedelta(hours=PUBLICATION_STALE_H):
        problems.append("publication: no eligible publication recorded since the stream started")
    # freshness of the status file
    st = _json(base / "reports/range_status.json", {})
    gen = st.get("generated_utc") if isinstance(st, dict) else None
    if not isinstance(gen, str):
        problems.append("freshness: reports/range_status.json missing or malformed")
    else:
        age_m = (now - _t(gen)).total_seconds() / 60
        info["status_age_min"] = round(age_m, 1)
        if age_m > STATUS_STALE_MIN:
            problems.append(f"freshness: reports/range_status.json generated {gen} ({age_m:.0f} min ago)")
        cur = st.get("current") if isinstance(st.get("current"), dict) else {}
        info["current_states"] = {h: (c.get("state") if isinstance(c, dict) else None) for h, c in cur.items()}
    # scoring backlog (eligible publications only; the scorer decides scorability)
    manifest = _json(base / "state/forecast_manifest.json", {})
    scores = {r.get("id") for r in _rows(base / "registry/scores.jsonl")}
    backlog = {}
    by_attempt = {p.get("attempt"): p for p in pubs}
    for fid, e in (manifest.items() if isinstance(manifest, dict) else []):
        if not (isinstance(fid, str) and fid.startswith("range-rc1d-") and isinstance(e, dict)):
            continue
        p = by_attempt.get(e.get("attempt")) if isinstance(e.get("attempt"), str) else None
        if not p or not isinstance(p.get("start_ms"), int) or fid in scores:
            continue
        h = fid.split("-")[2]
        end = dt.datetime.fromtimestamp(p["start_ms"] / 1000, UTC) + dt.timedelta(hours={"4h": 4, "24h": 24, "72h": 72}.get(h, 0))
        lag = (now - end).total_seconds() / 60 - MATURITY_MIN
        if lag > SCORE_LAG_MIN:
            backlog.setdefault(h, []).append(fid)
    info["scoring_backlog"] = backlog
    for h, ids in sorted(backlog.items()):
        problems.append(f"scoring: {len(ids)} matured {h} forecast(s) unscored > {SCORE_LAG_MIN} min: {', '.join(sorted(ids)[:4])}")
    # GitHub Actions (optional)
    if actions is not None:
        recorded = {r.get("run_id") for r in runs} | {(a.get("run") or {}).get("run_id") for a in attempts}
        for run in actions:
            if run.get("event") == "schedule" and run.get("conclusion") not in (None, "success") \
                    and str(run.get("run_id")) not in recorded:
                problems.append(f"actions: range.yml run {run.get('run_id')} ({run.get('created_utc')}) concluded "
                                f"{run.get('conclusion')} with no record in the repository")
    return problems, info


def fetch_actions(repo, token, opener=None):
    """Recent range.yml runs from the GitHub API, or None when unavailable (never fatal)."""
    opener = opener or urllib.request.urlopen
    url = f"https://api.github.com/repos/{repo}/actions/workflows/range.yml/runs?per_page=20"
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
        with opener(req, timeout=20) as r:
            js = json.loads(r.read())
        return [{"run_id": str(x.get("id")), "event": x.get("event"), "created_utc": x.get("created_at"),
                 "conclusion": x.get("conclusion")} for x in js.get("workflow_runs", [])]
    except Exception as exc:                            # noqa: BLE001 - reported, not fatal
        print(f"::warning::GitHub API unavailable ({type(exc).__name__}); run-list check skipped")
        return None


def main():
    base = Path(os.environ.get("RANGE_BASE", Path(__file__).resolve().parent.parent))
    now = dt.datetime.now(UTC).replace(microsecond=0)
    actions = None
    if os.environ.get("GITHUB_TOKEN") and os.environ.get("GITHUB_REPOSITORY"):
        actions = fetch_actions(os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_TOKEN"])
    problems, info = check(base, now, actions)
    print(json.dumps(info, indent=1, sort_keys=True))
    for p in problems:
        print(f"::error::{p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
