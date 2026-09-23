#!/usr/bin/env python3
"""Build an auditable desk report. Importing this module has no side effects."""
import argparse
from collections import Counter
import datetime as dt
import os
from pathlib import Path
import subprocess
import sys
import time
from schema import H, SERIES
from storage import atomic_bytes, read_rows, read_json, loads
from scoring import score_registry
from research import run_tests

REPORT_VERSION = "report-2.2-2026-09-23"


def iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%MZ")


def _num(x, digits=4):
    return "n/a" if x is None else (f"{x:.{digits}f}" if isinstance(x, float) else str(x))


def format_event(event):
    """One line per scored event, naming every score the event type carries."""
    kind, label = event.get("type"), event.get("name") or event.get("type")
    if kind == "range":
        pin = event.get("pinball") or {}
        return (f"{label}: realized ln(H/L) {_num(event.get('realized_ln_range'), 5)}; "
                f"inside q10-q90: {event.get('covered_80')}; "
                f"pinball q10/q50/q90 {_num(pin.get('q10'), 5)}/{_num(pin.get('q50'), 5)}/{_num(pin.get('q90'), 5)}; "
                f"|q50 - realized| {_num(event.get('abs_error_lr'), 5)}; "
                f"|ln q50 - ln realized| {_num(event.get('abs_error_log_lr'), 4)} (E2 primary); "
                f"QLIKE {_num(event.get('qlike'), 4)}.")
    if kind == "interval":
        return (f"{label}: realized {_num(event.get('realized'), 2)}; inside {event.get('inside')} "
                f"(nominal {event.get('nominal')}); interval score {_num(event.get('interval_score'), 2)}.")
    if kind in ("touch", "terminal", "race"):
        return (f"{label}: outcome {event.get('outcome')}; p {event.get('p')} ({event.get('p_class')}); "
                f"log score {event.get('log_score')}; Brier {event.get('brier')}.")
    if kind == "lean":
        return (f"{label}: {event.get('direction')} -> outcome {event.get('outcome')}; "
                f"return {_num(event.get('return_pts'), 2)} pts; invalidated at {event.get('invalidated_at')}.")
    if kind == "predicate":
        value = f"; value {event.get('value')}" if "value" in event else ""
        return f"{label}: outcome {event.get('outcome')}{value}."
    return f"{label}: {event}"


def run_coverage(runs, start, end):
    # Scheduled run slots begin at :07; manual extra runs cannot raise coverage above 100%.
    slots = set(range((start - 7*60_000 + H - 1)//H, (end - 7*60_000)//H + 1))
    present = {((r["t"] - 7*60_000)//H) for r in runs if start <= r["t"] <= end}
    return len(slots & present), len(slots)


def build(base, now, days=7):
    base = Path(base)
    since = now - days * 24 * H
    lines, alerts, fold = [], [], []
    def read(pattern):
        rows = []
        for path in sorted(base.glob(pattern)):
            try:
                rows.extend(read_rows(path))
            except (ValueError, OSError) as exc:
                alerts.append(f"Unreadable data: {exc}")
        return rows
    runs_all = sorted(read("data/runs/*.jsonl"), key=lambda r: r["t"])
    if any(r["t"] > now for r in runs_all):
        alerts.append("Stored runs have future timestamps relative to this report clock; excluded from health totals.")
    runs = [r for r in runs_all if since <= r["t"] <= now and r.get("mode") == "hourly"]
    lines.extend([f"# JBM desk report — {iso(now)}", f"Window {iso(since)} → {iso(now)}. {REPORT_VERSION}.",
                  "Stored observations are research inputs. Missing observations never count as a failed forecast.",
                  "", "## 1. Collection health"])
    deployed = [r for r in runs_all if r.get("runner") == "github" and r.get("mode") == "hourly" and r["t"] <= now]
    if deployed:
        covered, expected = run_coverage(deployed, max(since, deployed[0]["t"]), now)
        lines.append(f"GitHub hourly slots observed: {covered}/{expected}; {len(runs)} hourly runs in window (all runners). "
                     "Slot counts approximate scheduled collection, not guaranteed uptime.")
    else:
        lines.append(f"{len(runs)} hourly runs in window. No GitHub deployment evidence in stored run records.")
    if not runs:
        alerts.append("No hourly collector run in the report window.")
    elif now - runs[-1]["t"] > 3 * H:
        alerts.append(f"Last hourly collector run {iso(runs[-1]['t'])}; over 3 hours old.")
    for run in runs:
        for key, error in run.get("errors", {}).items():
            alerts.append(f"{iso(run['t'])}: {key}: {error}")
        for name, status in run.get("series", {}).items():
            if status.get("err"):
                alerts.append(f"{iso(run['t'])}: history {name}: {status['err']}")
        if run.get("liq", {}).get("err"):
            alerts.append(f"{iso(run['t'])}: liquidations: {run['liq']['err']}")
        for name, status in (run.get("forward") or {}).items():
            if status.get("err"):
                alerts.append(f"{iso(run['t'])}: forward book {name}: {status['err']}")
        if not run.get("critical_ok", False):
            alerts.append(f"{iso(run['t'])}: critical collection failed")
    sources, current = {}, set()
    for snap in sorted((r for r in read("data/snap/*.jsonl") if since <= r["t"] <= now), key=lambda r: r["t"]):
        members = dict(snap.get("oi", {}), **{k:v for k,v in snap.items() if isinstance(v,dict) and "st" in v})
        current = set(members)          # sources in the most recent snapshot
        for name, value in members.items():
            sources.setdefault(name, []).append(value)
    lines.extend(["", "| Source | OK / observed | Latest status |", "|---|---:|---|"])
    for name, values in sorted(sources.items()):
        good = sum(v.get("st") == "ok" for v in values)
        latest = values[-1]
        status = str(latest.get("err") or latest.get("st")).replace("|", "/").replace("\n", " ")
        if name not in current:
            status = "retired: absent from the latest snapshot (see collector.py)"
        lines.append(f"| {name} | {good}/{len(values)} | {status} |")
        if name in current and latest.get("st") != "ok":
            alerts.append(f"Latest {name} snapshot unavailable: {status}")
        if len(values) >= 12 and good / len(values) <= .5:
            fold.append(f"Endpoint review: {name} succeeded in {good}/{len(values)} observations.")
    lines.extend(["", "## 2. History held", "Counts are unique timestamps per instrument; gaps are not independent research samples.",
                  "", "| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |", "|---|---|---|---:|---:|---:|"])
    for directory in sorted((base / "data/series").glob("*")):
        if not directory.is_dir():
            continue
        name = directory.name
        rows = read(f"data/series/{name}/*.jsonl")
        symbols = sorted({r.get("sym", "") for r in rows})
        for symbol in symbols:
            selected = [r for r in rows if r.get("sym", "") == symbol]
            stamps = sorted({r["t"] for r in selected})
            if not stamps:
                continue
            step = SERIES.get(name, (None,))[0]
            missing = sum(max(0, (b-a)//step - 1) for a,b in zip(stamps, stamps[1:])) if step else None
            duplicate = len(selected) - len(stamps)
            label = name + (" / " + symbol if symbol else "")
            lines.append(f"| {label} | {iso(stamps[0])} | {iso(stamps[-1])} | {len(stamps)} | {missing if missing is not None else 'variable cadence'} | {duplicate} |")
            if missing:
                alerts.append(f"{label}: {missing} missing intervals; retry backfill while source retention permits.")
            if duplicate:
                alerts.append(f"{label}: {duplicate} legacy duplicate rows; storage bytes preserved, counts deduplicated.")
            freshness = 3 * H + step if step else 12 * H
            if now - stamps[-1] > freshness:
                alerts.append(f"{label}: stale; last observation {iso(stamps[-1])}")
            if any(step and t % step for t in stamps):
                alerts.append(f"{label}: misaligned timestamps")
            if any(any(v is None for v in r.get('f', {}).values()) for r in selected):
                alerts.append(f"{label}: missing field values in stored history")
    lines.extend(["", "## 3. Forced-flow retention and revision"])
    orders = read("data/liq/orders/*.jsonl")
    unique = {(r['t'],r.get('posSide'),r.get('side'),r.get('sz_contracts'),r.get('bkPx')):r for r in orders}
    bounds = sorted(read("data/liq/boundary/*.jsonl"), key=lambda r:r['t'])
    lines.append(f"{len(unique)} distinct liquidation observations; {len(bounds)} retained boundary probes.")
    for row in bounds[-5:]:
        qualifier = "lower bound; page cap reached" if row.get("hit_page_cap") else "observed source boundary"
        lines.append(f"- {iso(row['t'])}: {row['retention_days']} days, {row['pages']} pages ({qualifier}).")
    if bounds:
        fold.append(f"Review measured liquidation retention: latest probe {bounds[-1]['retention_days']} days. This is not a guarantee of future availability.")
    by_hour = {}
    for row in unique.values():
        by_hour.setdefault(row['t']//H*H, []).append(row)
    revisions = []
    for hour, rows in by_hour.items():
        if not since <= hour+H <= now-6*H:
            continue
        live = next((r for r in runs_all if hour+H <= r['t'] <= hour+3*H
                     and r.get('mode') == 'hourly' and not r.get('liq',{}).get('err')
                     and r.get('liq',{}).get('window_oldest_ms', now) <= hour), None)
        followup = any(hour+7*H <= r['t'] <= now and r.get('mode')=='hourly' and not r.get('liq',{}).get('err')
                       and r.get('liq',{}).get('window_oldest_ms',now) <= hour for r in runs_all)
        if not live or not followup:
            continue
        total = sum(r['btc'] for r in rows)
        if total >= 10:
            # New records use completion-time observations, legacy records retain first_seen.
            end_capture = live['t'] + int(live.get('elapsed_s',0)*1000)
            first = sum(r['btc'] for r in rows if r.get('observed_at',r['first_seen']) <= end_capture)
            revisions.append((total-first)/total)
    if revisions:
        lines.append(f"Observed later revision after first live capture: n={len(revisions)} active hours; mean {100*sum(revisions)/len(revisions):.1f}%. "
                     "Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.")
    else:
        lines.append("Insufficient live capture/follow-up evidence to estimate revision.")
    lines.extend(["", "## 3b. Forward-only books (requirement 50)",
                  "Value starts on the first stored run; no source retains these books."])
    for label, pattern, count in (("Deribit BTC options, per-strike OI", "data/options/deribit_btc/*.jsonl",
                                   lambda r: f"{len(r.get('rows', []))} strikes with OI"),
                                  ("Hyperliquid BTC position map", "data/hl_positions/btc/*.jsonl",
                                   lambda r: f"{len(r.get('positions', []))} BTC positions in top {r.get('accounts_ranked')}")):
        paths = sorted(base.glob(pattern))
        window = [r for path in paths[-days - 1:] for r in read(path.relative_to(base).as_posix()) if since <= r["t"] <= now]
        if not window:
            lines.append(f"- {label}: no stored runs in window.")
            continue
        hours = len({r["t"] // H for r in window})
        degraded = sum(r.get("status") == "degraded" for r in window)
        lines.append(f"- {label}: {hours} hourly runs from {iso(window[0]['t'])} to {iso(window[-1]['t'])}; "
                     f"latest {count(window[-1])}; {degraded} degraded snapshot(s).")
        if now - window[-1]["t"] > 3 * H:
            alerts.append(f"{label}: stale; last stored run {iso(window[-1]['t'])}")
    lines.extend(["", "## 4. Forecast registry"])
    manifest = read_json(base / "state/forecast_manifest.json", {})
    registered_sources = {entry["source"] for entry in manifest.values()}
    for path in sorted((base / "registry").glob("*.json")):
        if not path.name.startswith("_") and path.relative_to(base).as_posix() not in registered_sources:
            alerts.append(f"{path.name}: not in frozen registration manifest; collector registration required")
    records, new, pending, scoring_alerts = score_registry(base, now, REPORT_VERSION)
    alerts.extend(scoring_alerts)
    completed = [r for r in records if r.get('status')=='scored']
    late = [r for r in records if r.get('status','').startswith('late')]
    lines.append(f"Scored: {len(completed)} total; {sum(r['status']=='scored' for r in new)} this report. Pending/retryable: {pending}. Late registrations: {len(late)}.")
    for rec in new:
        lines.append(f"- {rec['id']}: {rec['status']}; forecast SHA-256 {rec['forecast_sha256']}.")
        for event in rec.get('events',[]):
            lines.append(f"  - {format_event(event)}")
    if new:
        fold.append("Review newly scored forecasts and retained evidence. A small sample is not calibration.")
    lines.extend(["", "## 5. Pre-registered research tests",
                  "Post-registration labels describe timing only. Custom test code can bypass context helpers; leakage, episode independence and causal validity require review."])
    tests, test_alerts = run_tests(base, now, REPORT_VERSION)
    alerts.extend(test_alerts)
    for rec in tests:
        lines.append(f"- {rec['id']}: {rec['n_post_registration']} mature post-registration episodes; {rec['n_in_sample']} in-sample; {rec['n_rejected']} rejected.")
        lines.append(f"  - Post-registration summaries: {rec['post_registration']}")
        if rec['n_post_registration']:
            fold.append(f"Review {rec['id']}: {rec['n_post_registration']} mature post-registration episodes; eligibility is not established by count alone.")
    if not tests:
        lines.append("No research tests completed successfully.")
    lines.extend(["", "## 6. Fold candidates", "Human review required before changing the skill package."])
    lines.extend([f"- {value}" for value in fold] or ["None."])
    fixture = base / 'test_fixtures.py'
    try:
        check = subprocess.run([sys.executable,str(fixture)],capture_output=True,text=True,timeout=120)
        if check.returncode:
            alerts.append("Numerical fixtures failed: " + (check.stdout + check.stderr)[-1500:])
    except Exception as exc:
        alerts.append(f"Numerical fixtures unavailable: {exc}")
    lines.extend(["", "## 7. Alerts"])
    lines.extend([f"- {value}" for value in dict.fromkeys(alerts)] or ["None detected by implemented checks."])
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days',type=int,default=7)
    args = parser.parse_args()
    if not 1 <= args.days <= 365:
        parser.error('--days must be 1–365')
    base = Path(os.environ.get('OUT_DIR',Path(__file__).resolve().parent))
    now = int(time.time()*1000)
    text = build(base,now,args.days)
    date = dt.datetime.fromtimestamp(now/1000,dt.timezone.utc).strftime('%Y-%m-%d')
    for name in (date+'.md','latest.md'):
        atomic_bytes(base/'reports'/name,text.encode())
    print(text)


if __name__ == '__main__':
    main()
