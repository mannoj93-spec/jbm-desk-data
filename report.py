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
import cadence

REPORT_VERSION = "report-2.6-2026-09-24"


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
    # Hourly slots at :07 (the pre-2.6 schedule); extra runs cannot raise coverage above 100%.
    # Used only for the legacy period, whose records do not say what started them.
    slots = set(range((start - 7*60_000 + H - 1)//H, (end - 7*60_000)//H + 1))
    present = {((r["t"] - 7*60_000)//H) for r in runs if start <= r["t"] <= end}
    return len(slots & present), len(slots)


def _minutes(values):
    mid, p90 = cadence.quantiles(values)
    return "n/a" if mid is None else f"median {mid:.1f}, p90 {p90:.1f}, max {max(values):.1f}"


def collection_health(runs_all, runs, snaps, periods, since, now):
    """Section 1. Scheduled execution (starts the scheduler made, counted against the nominal
    slots of the cadence in force) and snapshot coverage (market snapshots actually stored per
    slot interval, whatever started them) are reported separately; see cadence.py."""
    lines, alerts = [], []
    stale_min = cadence.stale_minutes()
    grace = 20 * 60_000     # a slot this recent may simply not have started yet
    by_trigger = Counter(cadence.trigger(r) or f"not recorded ({r.get('runner')})" for r in runs)
    lines.append(f"{len(runs)} routine runs in window, by trigger: "
                 + (", ".join(f"{k} {v}" for k, v in sorted(by_trigger.items())) or "none") + ".")
    if not periods:
        lines.append("No cadence history (cadence.json); scheduled execution not assessed.")
    else:
        lines.extend(["", "| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |",
                      "|---|---|---:|---|---|---:|"])
        for lo, hi, minutes in cadence.spans(periods, since, now):
            cron = [c for start, m, c in periods if start <= lo][-1]
            due = cadence.slots(periods, lo, min(hi, now - grace + 1))
            in_span = [r for r in runs_all if lo <= r["t"] < hi and r["t"] <= now and cadence.is_routine(r)]
            scheduled = [r for r in in_span if cadence.trigger(r) == "schedule"]
            legacy = [r for r in in_span if cadence.trigger(r) is None and r.get("runner") == "github"]
            if legacy and not scheduled:
                covered, _ = run_coverage(legacy, lo, hi) if len(minutes) == 1 and minutes == [7] else (None, None)
                started = (f"{len(legacy)} GitHub runs, trigger not recorded (pre-2.6)"
                           + (f"; slots with a run: {covered}/{len(due)}, an upper bound (manual runs indistinguishable)"
                              if covered is not None else ""))
            else:
                share = f" ({100 * min(len(scheduled), len(due)) / len(due):.0f}%)" if due else ""
                started = f"{len(scheduled)}{share}"
                if legacy:
                    started += f"; plus {len(legacy)} pre-2.6 runs with no trigger recorded"
            buckets = [(a, b) for a, b in cadence.slot_buckets(periods, lo, hi) if b <= now]
            stamps = [r["t"] for r in snaps if lo <= r["t"] < hi]
            j, hit = 0, 0
            for a, b in buckets:
                while j < len(stamps) and stamps[j] < a:
                    j += 1
                hit += j < len(stamps) and stamps[j] < b
            span_snaps = [r for r in snaps if lo <= r["t"] < hi]
            degraded = sum(1 for r in span_snaps if any(v.get("st") != "ok" for v in (r.get("oi") or {}).values()))
            coverage = f"{hit}/{len(buckets)} slot intervals" if buckets else "no complete interval"
            lines.append(f"| {iso(lo)} → {iso(hi)} | `{cron}` | {len(due)} | {started} | {coverage} | {degraded}/{len(span_snaps)} |")
        lines.append("Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded "
                     "amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). "
                     f"Slots in the last {grace // 60_000} minutes are not yet due. Manual runs never count as scheduled starts; "
                     "they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.")
    sched = [r for r in runs if cadence.schedule_evidence(r)]
    current = cadence.interval_minutes(periods, now) if periods else None
    gaps = [(b["t"] - a["t"]) / 60_000 for a, b in zip(sched, sched[1:])
            if current and cadence.interval_minutes(periods, a["t"]) == current]
    if gaps:
        legacy = any(cadence.trigger(r) is None for r in sched)
        lines.append(f"Actual interval between scheduled starts under the current {current}-minute cadence (min): {_minutes(gaps)}"
                     + ("; includes pre-2.6 GitHub runs, whose trigger is unrecorded." if legacy else "."))
    snap_gaps = [(b["t"] - a["t"]) / 60_000 for a, b in zip(snaps, snaps[1:])]
    if snap_gaps:
        lines.append(f"Actual interval between stored snapshots, all triggers (min): {_minutes(snap_gaps)}.")
    elapsed = [r["elapsed_s"] for r in runs if isinstance(r.get("elapsed_s"), (int, float))]
    if elapsed:
        mid, p90 = cadence.quantiles(elapsed)
        hit_deadline = sum(1 for r in runs if r.get("deadline_reached"))
        lines.append(f"Runtime per routine run (s): median {mid:.0f}, p90 {p90:.0f}, max {max(elapsed):.0f}; "
                     f"{hit_deadline} run(s) reached the network budget.")
        if hit_deadline:
            alerts.append(f"{hit_deadline} routine run(s) reached the network budget; later stages were cut short.")
    rate = Counter()
    for r in runs:
        rate.update((r.get("http") or {}).get("rate_limited_by_host") or {})
    hl_backoffs = sum(((r.get("forward") or {}).get("hl_positions") or {}).get("rate_limited") or 0 for r in runs)
    with_http = sum(1 for r in runs if r.get("http"))
    lines.append("Rate-limit incidents: " + (", ".join(f"{h} {n}" for h, n in rate.most_common()) or "none recorded")
                 + f" across {with_http} run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: {hl_backoffs}.")
    if not runs:
        alerts.append("No routine collector run in the report window.")
    last = [r for r in runs_all if cadence.schedule_evidence(r) and r["t"] <= now]
    if last and now - last[-1]["t"] > stale_min * 60_000:
        alerts.append(f"Collector stale: last scheduled run {iso(last[-1]['t'])}, over {stale_min} minutes before this report.")
    # One alert per source, not one per run: at 96 runs a day a persistent fault would otherwise
    # bury everything else.
    grouped, critical = {}, []
    for r in runs:
        is_critical, problems = cadence.failure_summary(r)
        if is_critical:
            critical.append(r)
        for source, message in problems:
            g = grouped.setdefault(source, {"n": 0, "first": r["t"], "last": r["t"], "msg": message})
            g["n"] += 1
            g["last"], g["msg"] = r["t"], message
    if critical:
        alerts.append(f"Critical collection failed in {len(critical)}/{len(runs)} routine run(s): "
                      + ", ".join(iso(r["t"]) for r in critical[-5:]) + (" (latest five)" if len(critical) > 5 else ""))
    for source, g in sorted(grouped.items(), key=lambda kv: -kv[1]["last"]):
        when = iso(g["first"]) if g["n"] == 1 else f"{iso(g['first'])} → {iso(g['last'])}"
        cleared = "; absent from the latest run" if g["last"] < runs[-1]["t"] else ""
        alerts.append(f"{source}: {g['n']}/{len(runs)} routine run(s), {when}; latest: {g['msg']}{cleared}")
    return lines, alerts


def research_datasets(base, since, now, read, alerts):
    """Section 3c: the 2.7 research datasets - coverage, states and freshness, never outcomes."""
    from schema import PRICE_SERIES
    lines = ["", "## 3c. Research datasets (collector 2.7)",
             "Coverage of stored inputs only. These are samples and summaries, not trading results."]
    for name in PRICE_SERIES:
        bars = {}
        for path in sorted(base.glob(f"data/prices/{name}/*.jsonl"))[-2:]:
            for batch in read(path.relative_to(base).as_posix()):
                for bar in batch.get("bars", []):
                    if since <= bar[0] <= now:
                        bars.setdefault(bar[0], True)
        if not bars:
            lines.append(f"- {name}: no bars in window.")
            continue
        stamps = sorted(bars)
        missing = sum(max(0, (b - a) // 60_000 - 1) for a, b in zip(stamps, stamps[1:]))
        lines.append(f"- {name}: {len(stamps)} bars {iso(stamps[0])} → {iso(stamps[-1])}; {missing} missing minutes inside the span.")
        if now - stamps[-1] > cadence.stale_minutes() * 60_000:
            alerts.append(f"{name}: stale; last bar {iso(stamps[-1])}")
    def recent(pattern, days_back=8):
        paths = sorted(base.glob(pattern))[-days_back:]
        return [r for p in paths for r in read(p.relative_to(base).as_posix()) if since <= r["t"] <= now]
    opts = [r for r in recent("data/options/deribit_btc/*.jsonl") if r.get("schema")]
    if opts:
        last = opts[-1]
        lines.append(f"- Deribit options schema 2: {len(opts)} runs; latest {len(last['rows'])} with OI, "
                     f"{len(last.get('zero_oi', []))} zero OI, {len(last.get('absent', []))} absent, "
                     f"{len(last.get('past_expiry', []))} past expiry; panel {last.get('panel_status')}; "
                     f"metadata {last.get('meta_status')}.")
    quotes = recent("data/options/deribit_btc_quotes/*.jsonl")
    lines.append(f"- Deribit hourly quote records: {len(quotes)}.")
    hl = recent("data/hl_accounts/*.jsonl")
    if hl:
        states = Counter()
        for r in hl:
            states.update(r.get("counts", {}))
        lines.append(f"- Hyperliquid sample v2: {len(hl)} snapshots; account checks by state "
                     + ", ".join(f"{k} {v}" for k, v in sorted(states.items()))
                     + f"; fixed cohort {hl[-1]['fixed']['cohort_id']} ({hl[-1]['fixed']['size']}), rotating "
                     f"{hl[-1]['rotating']['size']} per run.")
    enr = recent("data/hl_enrich/*.jsonl")
    if enr:
        kinds = Counter((q["kind"], q["status"]) for r in enr for q in r["requests"])
        lines.append("- Hyperliquid enrichment requests: " + ", ".join(f"{k} {st} {n}" for (k, st), n in sorted(kinds.items())) + ".")
    ins = [r for r in read("data/okx_insurance/*.jsonl") if since <= r["t"] <= now]
    if ins:
        types = Counter(r["type"] for r in ins)
        lines.append("- OKX insurance fund rows: " + ", ".join(f"{k} {v}" for k, v in sorted(types.items())) + ".")
    exps = [r for r in read("research/v2/experiments/*.jsonl") if r["t"] <= now] or \
        [r for r in read("research/experiments/*.jsonl") if r["t"] <= now]
    if exps:
        last_t = max(r["t"] for r in exps)
        latest = [r for r in exps if r["t"] == last_t]
        by = Counter(r["status"] for r in latest)
        lines.append(f"- Research lab: {len({r['t'] for r in exps if r['t'] >= since})} runs in window; latest "
                     f"{iso(last_t)}: " + ", ".join(f"{k} {v}" for k, v in sorted(by.items()))
                     + " (statuses per design; see reports/research.md).")
        if now - last_t > 30 * H:
            alerts.append(f"research lab: no run since {iso(last_t)}")
        errs = [r["design"] for r in latest if r["status"] == "error"]
        if errs:
            alerts.append("research lab: design error(s) " + ", ".join(errs))
    return lines


FRESHNESS = [("collector runs", "data/runs/*.jsonl"), ("snapshots", "data/snap/*.jsonl"),
             ("1-minute prices (BTC perp)", "data/prices/binance_klines_1m_BTCUSDT_perp/*.jsonl"),
             ("Deribit options", "data/options/deribit_btc/*.jsonl"),
             ("Hyperliquid account sample", "data/hl_accounts/*.jsonl"),
             ("Hyperliquid enrichment", "data/hl_enrich/*.jsonl"), ("OKX insurance fund", "data/okx_insurance/*.jsonl"),
             ("OKX liquidation orders", "data/liq/orders/*.jsonl"),
             ("research lab", "research/v2/experiments/*.jsonl")]


def provenance(base, now, kind):
    """Header lines: generation time, input cutoff, versions, dataset freshness."""
    def latest(pattern):
        best = None
        for path in sorted(base.glob(pattern))[-2:]:
            try:
                for r in read_rows(path):
                    t = r.get("observed_at") if "research" not in pattern else r.get("t")
                    if t is not None and t <= now and (best is None or t > best[0]):
                        best = (t, r)
            except (ValueError, OSError):
                continue
        return best
    run = latest("data/runs/*.jsonl")
    lab = latest("research/v2/experiments/*.jsonl")
    lines = [f"Generated {iso(now)} by {REPORT_VERSION} ({kind}). Input cutoff: "
             + (f"{iso(run[0])} (latest collector run written, {run[1].get('code_version')})" if run else "no runs")
             + ". Research lab: " + (f"last run {iso(lab[0])}, {lab[1].get('lab_version')}" if lab else "no research lab run yet")
             + ". This file is refreshed every 6 hours by the Research lab workflow; if the generation time is "
               "older than that, the refresh has stopped.", "",
             "| Dataset | Latest observation written | Age |", "|---|---|---:|"]
    for label, pattern in FRESHNESS:
        got = latest(pattern)
        if pattern.startswith("research/") and got:
            label = f"{label} ({got[1].get('lab_version') or 'version not recorded'})"   # the recorded version
        lines.append(f"| {label} | {iso(got[0]) if got else 'none'} | "
                     f"{f'{(now - got[0]) / 60_000:.0f} min' if got else 'n/a'} |")
    return lines + [""]


def build(base, now, days=7, coverage_only=False):
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
    runs = [r for r in runs_all if since <= r["t"] <= now and cadence.is_routine(r)]
    lines.extend([f"# JBM desk report — {iso(now)}", f"Window {iso(since)} → {iso(now)}. {REPORT_VERSION}.",
                  "Stored observations are research inputs. Missing observations never count as a failed forecast.",
                  ""])
    lines.extend(provenance(base, now, "coverage refresh; forecast scoring and research tests are in the weekly "
                                       "report" if coverage_only else "weekly report"))
    lines.extend(["## 1. Collection health"])
    snaps = sorted((r for r in read("data/snap/*.jsonl") if since <= r["t"] <= now), key=lambda r: r["t"])
    try:
        periods = cadence.load(base)
    except (ValueError, KeyError, TypeError) as exc:
        alerts.append(f"cadence.json unreadable ({exc}); scheduled execution not assessed.")
        periods = []
    health_lines, health_alerts = collection_health(runs_all, runs, snaps, periods, since, now)
    lines.extend(health_lines)
    alerts.extend(health_alerts)
    sources, current = {}, set()
    for snap in snaps:
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
                     and cadence.is_routine(r) and not r.get('liq',{}).get('err')
                     and r.get('liq',{}).get('window_oldest_ms', now) <= hour), None)
        followup = any(hour+7*H <= r['t'] <= now and cadence.is_routine(r) and not r.get('liq',{}).get('err')
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
        lines.append(f"- {label}: {len(window)} stored snapshots in {hours} distinct hours from {iso(window[0]['t'])} "
                     f"to {iso(window[-1]['t'])}; latest {count(window[-1])}; {degraded} degraded snapshot(s).")
        if now - window[-1]["t"] > cadence.stale_minutes() * 60_000:
            alerts.append(f"{label}: stale; last stored run {iso(window[-1]['t'])}")
    lines.extend(research_datasets(base, since, now, read, alerts))
    if coverage_only:
        weekly = sorted(p.name for p in (base / "reports").glob("20??-??-??.md"))
        lines.extend(["", "## 4. Forecast registry", "Not run in the coverage refresh (scoring writes evidence); see "
                      f"the weekly report{' reports/' + weekly[-1] if weekly else ''}.",
                      "", "## 5. Pre-registered research tests", "Not run in the coverage refresh; see the weekly report."])
    else:
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
    parser.add_argument('--coverage-only', action='store_true',
                        help='refresh reports/latest.md without scoring or research tests (no other side effects)')
    args = parser.parse_args()
    if not 1 <= args.days <= 365:
        parser.error('--days must be 1–365')
    base = Path(os.environ.get('OUT_DIR',Path(__file__).resolve().parent))
    now = int(time.time()*1000)
    text = build(base,now,args.days,coverage_only=args.coverage_only)
    date = dt.datetime.fromtimestamp(now/1000,dt.timezone.utc).strftime('%Y-%m-%d')
    for name in (('latest.md',) if args.coverage_only else (date+'.md','latest.md')):
        atomic_bytes(base/'reports'/name,text.encode())
    print(text)


if __name__ == '__main__':
    main()
