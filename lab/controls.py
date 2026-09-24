"""Hourly comparison-observation (control) selection for collection-based modules (revision 2.10).

Modules B (account behaviour), C (liquidation exposure) and F (options/perp disagreement) draw
their controls from the collector's own records, whose times are the actual run times (GitHub
starts the nominal :07/:22/:37/:52 runs late, often after :15). Up to 2.9 they kept a record as a
control only if its source time fell before minute 15 of the UTC hour, so a late-starting hour
produced no control at all. This module replaces that gate with one policy, POLICY:

  candidate      every collection record with the module's REQUIRED inputs (C: the account
                 observation and the same run's Hyperliquid mark; F: the option record only - never
                 funding or a signal; B: both account observations of the transition).
                 required-input availability a = the latest observed_at among those inputs.
  eligible       a candidate whose decision is not excluded by lab/asof.decide (inputs more than
                 LATE_INPUT_MAX_MS after the source time are excluded, as before).
  hour bucket    floor(a / 1 h) in UTC: the hour in which the required inputs became available.
                 A record whose source time is 09:58 but whose inputs arrive at 10:03 belongs to
                 the 10:00 bucket; the decision time is always a + ASSUMED_PROCESSING_MS and may
                 fall in the next hour (a = 10:59:30 -> decision 11:00:30, still the 10:00
                 bucket). Nothing is ever re-dated to the hour boundary.
  selection      per bucket, the eligible candidate with the smallest a; ties broken by source
                 time, then by the candidate's stable key (a function of its inputs' identity).
                 Nothing about outcomes, label completeness, baseline fit or profitability is
                 read. If the earliest record lacks a required input it is not a candidate and
                 the next one is considered. An hour with no eligible candidate has NO control;
                 its reason is recorded and nothing is carried into it from another hour.
  freezing       the first lab run that selects a control for a bucket freezes it (t_persisted,
                 append-only under research/v2/<design>/<version>/controls/, keyed by policy and
                 hour; first record wins, also in scripts/merge_research.py). Later runs use the
                 frozen record as stored: a record committed late - even one with an earlier
                 availability - never displaces it, and a later price, funding or label change
                 never replaces it. A frozen selection is used only at cutoffs after its
                 t_persisted, so an earlier cutoff never sees a later decision.
Diagnostics (diagnose): covered hours, hours with eligible candidates, selected times, missing
hours with reasons, delay from the hour boundary to availability, closed versus partial hours.
"""
from pathlib import Path

from lab.asof import decide
from lab.common import H, append_unique, month, read_rows

POLICY = "hourly-first-available-1"


def candidate(key, t_event, t_first_observed, t_inputs, build, missing=None):
    """A possible control. `build(t_available)` returns its event record; `missing` names a
    required input that is absent (then it is not eligible)."""
    return {"key": key, "t_event": t_event, "t_first_observed": t_first_observed, "t_inputs": t_inputs,
            "build": build, "missing": missing}


def controls_dir(base, design):
    return Path(base) / f"research/v2/{design['id']}/{design['_version']}/controls"


def persist_selections(base, design, records):
    """Append new selections, partitioned by the month of their hour; the first record of a
    (policy, hour) wins, so repeated or concurrent runs never replace a stored selection."""
    by = {}
    for r in records:
        by.setdefault(month(r["control_hour"]), []).append(r)
    return sum(append_unique(controls_dir(base, design) / f"{m}.jsonl", rs,
                             key=lambda r: (r["control_policy"], r["control_hour"])) for m, rs in sorted(by.items()))


def load_selections(base, design):
    """Frozen selections of a design version: {hour_ms: record}; the first stored record of an hour wins."""
    out = {}
    d = controls_dir(base, design)
    for p in sorted(d.glob("*.jsonl")) if d.exists() else []:
        for r in read_rows(p):
            if r.get("control_policy") == POLICY:
                out.setdefault(r["control_hour"], r)
    return out


def select(candidates, now, frozen=None, last_cutoff=None):
    """Returns (controls, new_selections, diagnostics). `frozen` maps hour -> stored control record;
    only those persisted by `now` are used."""
    frozen = {h: r for h, r in (frozen or {}).items()
              if r.get("t_persisted") is not None and r["t_persisted"] <= now}      # unknown time: not used
    buckets, reasons = {}, {}
    for c in candidates:
        if c["t_inputs"] is None or c["t_inputs"] > now:
            continue
        hour = c["t_inputs"] // H * H
        if c["missing"]:
            reasons.setdefault(hour, {}).setdefault(f"missing {c['missing']}", 0)
            reasons[hour][f"missing {c['missing']}"] += 1
            continue
        avail, excluded = decide(c["t_event"], c["t_inputs"])
        if excluded:
            reasons.setdefault(hour, {}).setdefault(excluded, 0)
            reasons[hour][excluded] += 1
            continue
        buckets.setdefault(hour, []).append((c["t_inputs"], c["t_event"], str(c["key"]), avail, c))
    controls, new, per_hour = [], [], {}
    for hour in sorted(set(buckets) | set(frozen)):
        if hour in frozen:
            rec = dict(frozen[hour])
            controls.append(rec)
            per_hour[hour] = {"selected": rec["t_inputs"], "decision": rec["t_available"], "frozen": True}
            continue
        t_in, t_ev, key, avail, c = min(buckets[hour], key=lambda x: x[:3])
        rec = c["build"](avail)
        rec.update(control_policy=POLICY, control_hour=hour, control_key=key, t_persisted=now,
                   hour_closed_at_selection=hour + H <= now,
                   hour_closed_at_previous_run=bool(last_cutoff is not None and hour + H <= last_cutoff))
        controls.append(rec)
        new.append(rec)
        per_hour[hour] = {"selected": t_in, "decision": avail, "frozen": False}
    return controls, new, {"per_hour": per_hour, "reasons": reasons,
                           "eligible_hours": sorted(buckets), "candidates": len(candidates)}


def diagnose(sel_diag, now, window_start, first_record=None):
    """Compact comparison-coverage diagnostics over the closed and current hours from window_start."""
    if window_start is None:
        return {"policy": POLICY, "window": None}
    start = window_start // H * H
    hours = list(range(start, now // H * H + H, H))
    closed = [h for h in hours if h + H <= now]
    ph, eligible = sel_diag["per_hour"], set(sel_diag["eligible_hours"])
    missing = {}
    for h in closed:
        if h in ph:
            continue
        why = sel_diag["reasons"].get(h)
        missing[h] = ("; ".join(f"{k} x{v}" for k, v in sorted(why.items())) if why
                      else "no collection record with required inputs available in this hour")
    delays = sorted((v["selected"] - h) / 60_000 for h, v in ph.items())
    flagged = [h for h in closed if h in eligible and h not in ph]      # must stay empty
    return {"policy": POLICY, "window": [start, now], "hours_covered": len(hours), "closed_hours": len(closed),
            "partial_hour": hours[-1] if hours and hours[-1] + H > now else None,
            "hours_with_eligible_candidates": len([h for h in hours if h in eligible or h in ph]),
            "selected": len(ph), "selected_closed": len([h for h in closed if h in ph]),
            "frozen_selected": sum(1 for v in ph.values() if v["frozen"]),
            "selected_times": [[h, v["selected"], v["decision"]] for h, v in sorted(ph.items())],
            "missing_closed_hours": [[h, why] for h, why in sorted(missing.items())],
            "closed_hours_with_candidates_but_no_control": flagged,
            "delay_from_hour_to_availability_min": ({"min": round(delays[0], 1), "median": round(delays[len(delays) // 2], 1),
                                                    "max": round(delays[-1], 1)} if delays else None)}


def apply(lab, candidates, window_start):
    """Select this run's controls for a module. The frozen selections, the previous lab run's cutoff,
    the design (whose version namespace stores selections) and a list collecting new selections come
    from lab.control_context (set per design by lab/run.py). New selections are persisted here, at
    selection time, when lab.write; without a context nothing is frozen or persisted.
    Returns (controls, diagnostics)."""
    now = getattr(lab, "now", None)
    if now is None:
        now = max((c["t_inputs"] for c in candidates if c["t_inputs"] is not None), default=0)
    ctx = getattr(lab, "control_context", None)
    controls, new, sel = select(candidates, now, (ctx or {}).get("frozen"), (ctx or {}).get("last_cutoff"))
    if ctx is not None:
        ctx.setdefault("new", []).extend(new)
        if ctx.get("design") is not None and getattr(lab, "write", False) and new:
            # stored at selection time, before experiments.run_design can record any checkpoint that
            # uses them; first record per (policy, hour) wins, so other variants' copies are no-ops
            persist_selections(lab.base, ctx["design"], new)
    return controls, diagnose(sel, now, window_start)
