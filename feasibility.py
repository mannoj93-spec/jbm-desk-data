#!/usr/bin/env python3
"""feasibility — can each active research hypothesis realistically accumulate evidence? (repo 2.20, read-only)

Reads only what the lab, the range stream and the new streams already wrote - the lab's current evidence cards
(research/evidence/index.json -> research/evidence/v2/<design>@<version>.json), the designs (lab/designs/), the
collector's schedule (cadence.json) and the stream reports (reports/range_status.json, reports/companion_b1.json,
reports/paper_ps1.json) - and writes reports/feasibility.{json,md}. It computes nothing the lab computes, changes
no definition, threshold, design, evaluation version or clock, and lives outside lab/ so the lab's code identity
(lab/common.py code_hash) is unchanged.

For each hypothesis: collection coverage, eligible observation time, raw candidates (firings), qualifying events,
distinct episodes, the module's recorded exclusion/skip counters (lab-2.2 records reasons by name; per-reason counts
exist only where a module recorded a counter), event and episode rates, warm-up requirements, checkpoint progress,
and the limiting factor: time (warm-up or accumulation), absent events, missing data, or infrastructure capability.

Time-to-checkpoint scenarios are printed only when the observed rate supports one: at least MIN_EVENTS_FOR_ETA
qualifying observations, with a 90% Poisson (Garwood) interval on the rate. Zero observed events give no ETA.
A zero from a period the collection could not observe is reported as "not observable", never as a zero rate.

  python3 feasibility.py            # write the report
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import sys
from pathlib import Path

VERSION = "feasibility-1.1.0"
BASE = Path(__file__).resolve().parent
UTC = dt.timezone.utc
MIN_EVENTS_FOR_ETA = 5
CHI2_90 = {}          # filled lazily by _chi2_quantile


def _read(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, ValueError):
        return default


def _t(s):
    s = s.replace("Z", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=UTC)
        except ValueError:
            pass
    raise ValueError(s)


def _gamma_quantile(p, k):
    """Quantile of Gamma(k, 1) by bisection on the regularized lower incomplete gamma (series). Stdlib."""
    def lower_reg(a, x):
        if x <= 0:
            return 0.0
        term, total, n = 1.0 / a, 1.0 / a, 0
        while n < 10000:
            n += 1
            term *= x / (a + n)
            total += term
            if term < total * 1e-14:
                break
        return total * math.exp(-x + a * math.log(x) - math.lgamma(a))
    lo, hi = 0.0, max(10.0, 10 * k)
    for _ in range(200):
        mid = (lo + hi) / 2
        if lower_reg(k, mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def poisson_rate_ci90(n: int, exposure_days: float) -> tuple:
    """Garwood 90% interval for a Poisson rate per day."""
    lo = 0.0 if n == 0 else _gamma_quantile(0.05, n) / exposure_days
    hi = _gamma_quantile(0.95, n + 1) / exposure_days
    return lo, hi


def eta_days(need: int, have: int, n_events: int, exposure_days: float):
    """(central, slow, fast) days to reach `need` from `have` at the observed rate, or None when unsupported."""
    if n_events < MIN_EVENTS_FOR_ETA or exposure_days <= 0 or have >= need:
        return None
    rate = n_events / exposure_days
    lo, hi = poisson_rate_ci90(n_events, exposure_days)
    gap = need - have
    return {"central": gap / rate, "slow": gap / lo if lo > 0 else None, "fast": gap / hi}


WARMUP = re.compile(r"(?P<have>[\d.]+)\s+(?P<what>[a-z][a-z \-]*?)(?: \([^)]*\))?;? the design needs (?P<need>[\d.]+)")
ZERO_QUAL = re.compile(r"(?P<have>\d+) qualifying; the design needs (?P<need>\d+)")


def _collector_start(base) -> dt.datetime | None:
    cad = _read(Path(base) / "cadence.json", {}) or {}
    periods = cad.get("periods") or []
    return _t(periods[0]["from"]) if periods else None


def lab_designs(base, now) -> list:
    base = Path(base)
    idx = (_read(base / "research/evidence/index.json", {}) or {}).get("designs", {})
    started = _collector_start(base)
    out = []
    for design, info in sorted(idx.items()):
        card = _read(base / f"research/evidence/v2/{design}@{info.get('current')}.json")
        if not card:
            out.append({"id": design, "kind": "lab", "limiting": "missing data", "note": "current evidence card unreadable"})
            continue
        prim = str(card["primary_horizon_min"])
        p = (card.get("passes") or {}).get("prospective") or {}
        test = ((((p.get("phases") or {}).get("evaluation") or {}).get(prim) or {}).get("counts") or {}).get("test") or {}
        ref = ((((p.get("phases") or {}).get("evaluation") or {}).get(prim) or {}).get("counts") or {}).get("reference") or {}
        reg, cut = _t(card["registered_at"]), _t(card["attempt"]["cutoff"])
        eligible_days = max(0.0, (cut - reg).total_seconds() / 86400)
        cc = ((card.get("comparison_coverage") or {}).get("by_horizon") or {}).get(prim, {}).get("evaluation") or {}
        hours = (cut - reg).total_seconds() / 3600
        pending = (card.get("checkpoints") or {}).get("pending") or {}
        state = p.get("state")
        reasons = p.get("reasons") or card.get("failures") or []
        row = {"id": design, "kind": "lab", "version": card["evaluation_version"], "status": card["status"],
               "question": card["condition"], "primary_horizon_min": int(prim),
               "data_state": state, "data_reasons": reasons,
               "calendar_exposure": {"from": card["registered_at"], "to": card["attempt"]["cutoff"],
                                     "days": round(eligible_days, 2),
                                     "basis": "calendar time since registration - not the time the collection could observe"},
               "collection_coverage": {"hourly_controls_selected": cc.get("selected"), "hours_elapsed": round(hours, 1),
                                       "share": round(cc["selected"] / hours, 3) if cc.get("selected") is not None and hours > 0 else None,
                                       "collector_running_since": started.strftime("%Y-%m-%dT%H:%MZ") if started else None},
               "raw_candidates_prospective": p.get("firings"), "episodes_prospective": p.get("episodes"),
               "test_evaluation_phase": {k: test.get(k) for k in ("firings", "episodes", "scorable", "retained", "blocks")},
               "reference_evaluation_phase": {k: ref.get(k) for k in ("episodes", "retained")},
               "exclusions_named": card.get("exclusions", []),
               "recorded_counters": _counters(design, p.get("coverage") or {}),
               "checkpoint": {"look": pending.get("look"), "retained": pending.get("retained"), "need": pending.get("need"),
                              "min_dependence_blocks": card.get("min_dependence_blocks")}}
        retained = test.get("retained") or 0
        episodes = test.get("episodes") or 0
        observable = state != "unavailable"
        sel = cc.get("selected")
        obs_days = (sel / 24.0) if (observable and isinstance(sel, (int, float)) and sel > 0) else None
        row["capability"] = "observable" if observable else "not observable (the collection cannot see these events)"
        row["observable_exposure"] = {
            "days": round(obs_days, 2) if obs_days is not None else None,
            "basis": "hours with a selected hourly control in the evaluation phase (the lab's own coverage count) / 24"
                     if obs_days is not None else ("not observable" if not observable else "no recorded coverage count")}
        if obs_days:
            row["rates_per_observable_day"] = {"test_episodes": round(episodes / obs_days, 3),
                                               "test_retained": round(retained / obs_days, 3)}
        else:
            row["rates_per_observable_day"] = {"test_episodes": None, "test_retained": None,
                                               "why": row["observable_exposure"]["basis"]}
        # limiting factor
        if state == "unavailable":
            lim, obs = "infrastructure capability", "not observable: the collection cannot see these events"
        elif state == "insufficient_data":
            m = ZERO_QUAL.search(" ".join(reasons))
            if m and int(m.group("have")) == 0:
                lim, obs = "absent events", "observed zero qualifying events while the detector ran (see capability note)"
            else:
                lim = "time (warm-up)"
                obs = (f"warm-up not complete per the lab ({'; '.join(reasons)}); {retained} retained test observation(s) "
                       f"in {test.get('blocks') or 0} block(s) are already recorded" if retained else
                       f"warm-up not complete per the lab ({'; '.join(reasons)}); no retained test observation yet")
                w = WARMUP.search(" ".join(reasons))
                if w and started:
                    have, need = float(w.group("have")), float(w.group("need"))
                    elapsed = (cut - started).total_seconds() / 86400
                    rate = have / elapsed if elapsed > 0 else 0
                    row["warmup"] = {"have": have, "need": need, "unit": w.group("what").strip(),
                                     "observed_accumulation_per_day": round(rate, 2),
                                     "days_to_complete_at_observed_rate": round((need - have) / rate, 1) if rate > 0 else None,
                                     "basis": "averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after"}
        elif episodes == 0:
            lim, obs = "absent events", "observed zero test episodes with data available"
        else:
            lim, obs = "time (accumulation)", "events occur; evidence accumulates with time"
        row["limiting_factor"], row["zero_interpretation"] = lim, obs
        if lim == "time (warm-up)" and not retained:          # a warm-up zero is not an observed event rate
            row["rates_per_observable_day"] = {"test_episodes": None, "test_retained": None,
                                               "why": "warm-up incomplete per the lab; a zero here is not an observed rate"}
        need = pending.get("need") or card.get("min_retained_observations")
        row["time_to_checkpoint"] = eta_days(need or 0, retained, retained, obs_days) if (need and obs_days) else None
        if row["time_to_checkpoint"] is None:
            row["time_to_checkpoint_note"] = (
                "no ETA: not observable" if not observable else
                "no ETA: no observable-exposure denominator recorded" if not obs_days else
                f"no ETA: {retained} retained test observation(s) in {obs_days:.1f} observable days; "
                f"an ETA needs >= {MIN_EVENTS_FOR_ETA}")
            
        out.append(row)
    return out


def _counters(design, cov: dict) -> dict:
    """The module's own recorded counters, with the per-reason counts that can be read from them. Never inferred."""
    if design.startswith("D1"):
        progs, btc = cov.get("programs"), cov.get("btc_programs")
        return {"twap_checks": cov.get("twap_checks"), "programs_observed": progs, "btc_programs": btc,
                "excluded_non_btc": (progs - btc) if isinstance(progs, int) and isinstance(btc, int) else None,
                "btc_programs_not_qualifying": btc,
                "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule "
                                   "(first observed after finishing vs below the notional floor)"}
    if design.startswith("A1"):
        return {k: cov.get(k) for k in ("steps", "events", "skipped_history", "skipped_missing", "late_inputs",
                                         "spot_not_yet_available")}
    if design.startswith("E1"):
        return {"stream_data_dir": cov.get("stream_data_dir")}
    if design.startswith("H1"):
        return {k: cov.get(k) for k in ("buckets", "liquidation_orders", "stress_rows", "unavailable_sources")}
    flat = {k: v for k, v in cov.items() if isinstance(v, (int, float, str)) or k == "behaviour_counts"}
    return flat or {"note": "no counters recorded by the module"}


def desk_streams(base, now) -> list:
    base = Path(base)
    out = []
    rs = _read(base / "reports/range_status.json", {}) or {}
    ev = (rs.get("evaluation") or {}).get("horizons") or {}
    for h, e in ev.items():
        n, blocks = e.get("n") or 0, e.get("blocks") or 0
        first = e.get("first_decision_utc")
        days = ((now - _t(first)).total_seconds() / 86400) if first else 0
        rate = n / days if days > 0 else 0
        need = 10 * 42
        out.append({"id": f"RC1D B2 vs B0 ({h})", "kind": "range stream", "limiting_factor": "time (accumulation)",
                    "calendar_exposure": {"from": first, "days": round(days, 2), "basis": "calendar days since the stream start (one window per 4H decision)"}, "paired_scored": n,
                    "blocks": blocks, "checkpoint": {"need_blocks": 10, "block": 42},
                    "rate_per_day": round(rate, 2),
                    "time_to_checkpoint": {"central": (need - n) / rate} if rate > 0 and n >= MIN_EVENTS_FOR_ETA else None,
                    "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation"})
    cb = _read(base / "reports/companion_b1.json")
    if cb:
        for h, e in ((cb.get("evaluation") or {}).get("horizons") or {}).items():
            out.append({"id": f"Companion B2 vs B1 ({h})", "kind": "companion stream", "limiting_factor": "time (accumulation)"
                        if e.get("paired") else "not started", "paired": e.get("paired"),
                        "missing": e.get("missing_companion"), "late": e.get("late_companion"),
                        "checkpoint": {"need_blocks": 10, "block": 42}})
    else:
        out.append({"id": "Companion B2 vs B1", "kind": "companion stream", "limiting_factor": "not started",
                    "note": "reports/companion_b1.json not written yet (workflow not deployed or no run)"})
    ps = _read(base / "reports/paper_ps1.json")
    if ps and ps.get("launch"):
        out.append({"id": "PS1 paper sizing", "kind": "paper experiment", "limiting_factor":
                    "infrastructure capability" if ps.get("status") == "paused" else "time (accumulation)",
                    "coverage": ps.get("coverage"), "intervals": ((ps.get("paired") or {}).get("ordinary") or {}).get("n_intervals"),
                    "checkpoint": ps.get("checkpoints"), "outcomes": ps.get("outcomes")})
    else:
        out.append({"id": "PS1 paper sizing", "kind": "paper experiment", "limiting_factor": "not started",
                    "note": (ps or {}).get("reason") or "reports/paper_ps1.json not written yet"})
    return out


INFRA = {
    "D1-active-twap": ("TWAP programs are read by polling each fixed-cohort account's twapHistory every 15 minutes. "
                       "A program that starts and finishes between polls is first seen finished and excluded, so the "
                       "collection systematically under-observes short programs. Observing starts needs an event stream "
                       "(Hyperliquid's websocket user events for the cohort accounts). Not commissioned: the recorded "
                       "universe (2 BTC programs in 272) suggests qualifying BTC programs are rare even when seen, so a "
                       "stream would not by itself make D1 feasible; decide after the per-reason counts exist."),
    "E1-liquidity-recovery": ("Needs second-scale order-book depth around shocks. The repository's stream/ recorder exists "
                              "but is not deployed (it needs a persistent host, not GitHub Actions); until then E1 cannot "
                              "observe a single event and its zero is 'not observable'. Not commissioned here."),
}


def build(base=BASE, now=None) -> dict:
    now = now or dt.datetime.now(UTC)
    lab = lab_designs(base, now)
    for r in lab:
        if r["id"] in INFRA:
            r["capability_note"] = INFRA[r["id"]]
    cut = [r["calendar_exposure"]["to"] for r in lab if r.get("calendar_exposure")]
    return {"report": "feasibility", "schema": "feasibility-report-2", "generated_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source_cutoff_utc": max(cut) if cut else None, "job": VERSION,
            "evidence_class": "not applicable (an operations report: it restates counts and carries no hypothesis evidence)",
            "lifecycle": "not applicable",
            "integrity": "not verified here: inputs are the lab's evidence cards and the stream reports as written",
            "lab": lab,
            "streams": desk_streams(base, now),
            "rules": {"eta": f"only with >= {MIN_EVENTS_FOR_ETA} qualifying observations; 90% Garwood interval on the rate",
                      "zeros": "observed zero (collection capable) is reported separately from not observable; "
                               "an unobservable rate is null, never 0.0",
                      "denominators": "rates and ETAs use observable exposure (the lab's coverage count); calendar time "
                                      "since registration is shown separately and is never a rate denominator",
                      "definitions": "no design, threshold or evaluation version is changed by this report"}}


def _fmt_eta(e):
    if not e:
        return "no ETA"
    parts = [f"~{e['central']:.0f} d"]
    if e.get("fast") is not None:
        parts.append(f"(90%: {e['fast']:.0f}–{e['slow']:.0f} d)" if e.get("slow") else f"(fast {e['fast']:.0f} d)")
    return " ".join(parts)


def markdown(doc) -> str:
    L = ["# Research feasibility", "",
         f"Generated {doc['generated_utc']} by {doc['job']}; source cutoff {doc.get('source_cutoff_utc')}. Read-only: it restates what the lab and the streams recorded "
         "and changes no definition. A zero the collection could not observe is marked **not observable**.", "",
         "## Lab designs", "",
         "| design | status | capability | calendar days | observable days | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in doc["lab"]:
        if "calendar_exposure" not in r:
            L.append(f"| {r['id']} | — | — | — | — | — | — | {r['limiting']} | — |")
            continue
        od = r["observable_exposure"]["days"]
        ck = r["checkpoint"]
        L.append(f"| {r['id']} | {r['status']} | {r['capability'].split(' (')[0]} | {r['calendar_exposure']['days']} | "
                 f"{'unavailable' if od is None else od} | {r['raw_candidates_prospective']} / {r['episodes_prospective']} | "
                 f"{ck['retained']} / {ck['need']} | {r['limiting_factor']} | {_fmt_eta(r['time_to_checkpoint'])} |")
    L += ["", "Observable days = hours with a selected hourly control (the lab's coverage count) ÷ 24; calendar days are "
          "shown for reference only and never divide a count.", ""]
    for r in doc["lab"]:
        if "calendar_exposure" not in r:
            continue
        L += [f"### {r['id']} ({r['version']})", "",
              f"- Data: {r['data_state']}" + (f" — {'; '.join(r['data_reasons'])}" if r['data_reasons'] else ""),
              f"- Zeros: {r['zero_interpretation']}",
              f"- Test (evaluation phase, primary {r['primary_horizon_min']} min): " +
              ", ".join(f"{k} {v}" for k, v in r["test_evaluation_phase"].items()),
              f"- Rates per observable day: test episodes {r['rates_per_observable_day']['test_episodes'] if r['rates_per_observable_day']['test_episodes'] is not None else 'unavailable'}, "
              f"retained {r['rates_per_observable_day']['test_retained'] if r['rates_per_observable_day']['test_retained'] is not None else 'unavailable'}"
              + (f" ({r['rates_per_observable_day']['why']})" if r['rates_per_observable_day'].get('why') else ""),
              f"- Exclusions (named in the design): {'; '.join(r['exclusions_named']) or '—'}",
              f"- Recorded counters: {json.dumps(r['recorded_counters'], sort_keys=True)}"]
        if r.get("warmup"):
            w = r["warmup"]
            L.append(f"- Warm-up: {w['have']:g} of {w['need']:g} {w['unit']}; observed {w['observed_accumulation_per_day']}/day → "
                     f"{w['days_to_complete_at_observed_rate']} more days at that rate ({w['basis']})")
        if r.get("time_to_checkpoint_note"):
            L.append(f"- Checkpoint 1: {r['time_to_checkpoint_note']}")
        if r.get("capability_note"):
            L.append(f"- Capability: {r['capability_note']}")
        L.append("")
    L += ["## Desk streams", "", "| stream | limiting factor | detail |", "|---|---|---|"]
    for s in doc["streams"]:
        detail = {k: v for k, v in s.items() if k not in ("id", "kind", "limiting_factor")}
        if s.get("time_to_checkpoint"):
            detail["time_to_checkpoint"] = f"~{s['time_to_checkpoint']['central']:.0f} d"
        L.append(f"| {s['id']} | {s['limiting_factor']} | {json.dumps(detail, sort_keys=True, default=str)[:400]} |")
    L += ["", f"Rules: {doc['rules']['eta']}. {doc['rules']['zeros']}. {doc['rules']['definitions']}.", ""]
    return "\n".join(L)


def write(base=BASE, now=None) -> dict:
    doc = build(base, now)
    base = Path(base)
    (base / "reports").mkdir(exist_ok=True)
    (base / "reports/feasibility.json").write_text(json.dumps(doc, indent=1, sort_keys=True, default=str) + "\n")
    (base / "reports/feasibility.md").write_text(markdown(doc))
    return doc


if __name__ == "__main__":
    write()
    print("feasibility: reports/feasibility.{json,md} written")
