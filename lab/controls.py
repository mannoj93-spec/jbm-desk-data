"""Hourly comparison-observation (control) selection for collection-based modules (revisions 2.10-2.11).

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
  decision cutoff (2.11)  a candidate is usable at cutoff N only when its required inputs AND its
                 decision (a + 60 s) are available by N. Inputs at 09:59:30 with a 10:00:00 cutoff
                 are PENDING PROCESSING: nothing is returned or frozen; at 10:00:30 the same
                 candidate is selected, still in the 09:00 bucket. As the earliest candidate of an
                 hour also has the earliest decision, a pending earliest candidate makes the whole
                 hour pending (a later one is never taken instead). A stored selection is used
                 only if its inputs, decision AND persistence times are all known and <= N;
                 otherwise it is WITHHELD at that cutoff - never rewritten, never replaced.
  authority (2.11)  in a writing run the stored record is authoritative. New selections are
                 appended under a scoped file lock (first record per (policy, hour) wins), then
                 read back; the controls returned for labelling, baselines and checkpoints are
                 the stored records - complete, never mixed with a losing proposal - and the
                 in-memory context is refreshed so later variants see the same winners. A
                 proposal that lost to an existing record is reported as superseded, not as newly
                 frozen. A winner not usable at the cutoff is withheld and reported as an
                 unresolved conflict. A read-only run never writes; a selection it computes that
                 was not stored by its cutoff is PROVISIONAL, and it is withheld if it differs
                 from what was stored later.
  validation     before any control leaves this module: every control's inputs, decision and
                 persistence are known and within the cutoff, decision >= inputs + 60 s, one per
                 hour, and in a writing run each equals the stored record byte-for-byte
                 (fingerprint). A violation raises ControlIntegrityError, which fails the design.
Diagnostics (diagnose): covered hours, hours with eligible candidates, selected times, missing
hours with reasons (missing inputs, late inputs, no collection record), pending processing,
withheld stored records, accepted and superseded proposals, unresolved conflicts, ready-but-
unselected hours (an integrity error), delay from the hour to availability, closed versus partial
hours, and sha256 fingerprints of the controls used and of the stored records for those hours.
"""
import fcntl
import hashlib
import json
from pathlib import Path
import tempfile

from lab.asof import ASSUMED_PROCESSING_MS, decide
from lab.common import H, append_unique, month, read_rows

POLICY = "hourly-first-available-2"


class ControlIntegrityError(RuntimeError):
    """A control that would reach labelling violates the cutoff, uniqueness or authority rules."""


def candidate(key, t_event, t_first_observed, t_inputs, build, missing=None):
    """A possible control. `build(t_available)` returns its event record; `missing` names a
    required input that is absent (then it is not eligible)."""
    return {"key": key, "t_event": t_event, "t_first_observed": t_first_observed, "t_inputs": t_inputs,
            "build": build, "missing": missing}


def controls_dir(base, design):
    return Path(base) / f"research/v2/{design['id']}/{design['_version']}/controls"


def _canon(r):
    return json.dumps(r, sort_keys=True, separators=(",", ":"))


def fingerprint(records):
    """sha256 of the canonical JSON of records sorted by hour."""
    rs = sorted(records, key=lambda r: (r.get("control_hour") or 0, r.get("control_key") or ""))
    return hashlib.sha256("\n".join(_canon(r) for r in rs).encode()).hexdigest()


class _Lock:
    """Exclusive advisory lock scoped to one controls directory (outside the repository), so two
    local writers cannot both read-then-replace a monthly file; GitHub runs are also serialized."""
    def __init__(self, d):
        self.path = Path(tempfile.gettempdir()) / f"jbm-controls-{hashlib.sha1(str(Path(d).resolve()).encode()).hexdigest()[:16]}.lock"

    def __enter__(self):
        self.fh = open(self.path, "a")
        fcntl.flock(self.fh, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()


def persist_selections(base, design, records):
    """Append new selections, partitioned by the month of their hour, under the directory lock; the
    first record of a (policy, hour) wins, so repeated or concurrent runs never replace a stored
    selection. Returns the number of records actually added."""
    by = {}
    for r in records:
        by.setdefault(month(r["control_hour"]), []).append(r)
    d = controls_dir(base, design)
    with _Lock(d):
        return sum(append_unique(d / f"{m}.jsonl", rs, key=lambda r: (r["control_policy"], r["control_hour"]))
                   for m, rs in sorted(by.items()))


def load_selections(base, design):
    """Stored selections of a design version: {hour_ms: record}; the first stored record of an hour wins."""
    out = {}
    d = controls_dir(base, design)
    for p in sorted(d.glob("*.jsonl")) if d.exists() else []:
        for r in read_rows(p):
            if r.get("control_policy") == POLICY and isinstance(r.get("control_hour"), int):
                out.setdefault(r["control_hour"], r)
    return out


def _is_ms(x):
    return isinstance(x, int) and not isinstance(x, bool)


def stored_problem(rec, now):
    """None if a stored selection is usable at cutoff `now`, else why it is withheld."""
    for f in ("t_event", "t_inputs", "t_available", "t_persisted"):
        if not _is_ms(rec.get(f)):
            return f"malformed: {f} missing or not a millisecond time"
    if (rec["t_available"] < max(rec["t_inputs"], rec["t_event"]) + ASSUMED_PROCESSING_MS
            or rec["control_hour"] != rec["t_inputs"] // H * H):
        return "malformed: decision before source/inputs + processing, or hour not the inputs' hour"
    if rec["t_persisted"] < rec["t_available"]:
        return "malformed: persisted before its own decision"
    if rec["t_persisted"] > now:
        return "persisted after this cutoff"
    if rec["t_inputs"] > now or rec["t_available"] > now:
        return "malformed: persisted before its own inputs or decision"
    return None


def select(candidates, now, frozen=None, last_cutoff=None, write=False):
    """Returns (controls, proposals, diagnostics). `frozen` maps hour -> stored control record."""
    frozen = dict(frozen or {})
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
    controls, proposals, per_hour = [], [], {}
    pending, withheld, unresolved = {}, {}, {}
    for hour in sorted(set(buckets) | set(frozen)):
        best = min(buckets[hour], key=lambda x: x[:3]) if hour in buckets else None
        stored = frozen.get(hour)
        if stored is not None:
            why = stored_problem(stored, now)
            if best is None and (why == "persisted after this cutoff" and not write
                                 or (_is_ms(stored.get("t_inputs")) and stored["t_inputs"] > now)):
                continue      # nothing existed for this hour at this cutoff: missing / not reached, not withheld
            if why is None:
                controls.append(dict(stored))
                per_hour[hour] = {"selected": stored["t_inputs"], "decision": stored["t_available"], "state": "stored"}
            elif why == "persisted after this cutoff" and not write and best is not None:
                t_in, t_ev, key, avail, c = best
                if avail > now:
                    pending[hour] = avail
                elif key == stored.get("control_key"):          # what was later stored, computed as of now
                    rec = c["build"](avail)
                    rec.update(control_policy=POLICY, control_hour=hour, control_key=key, t_persisted=now,
                               hour_closed_at_selection=hour + H <= now, hour_closed_at_previous_run=False)
                    controls.append(rec)
                    per_hour[hour] = {"selected": t_in, "decision": avail, "state": "provisional"}
                else:
                    withheld[hour] = f"later stored selection {stored.get('control_key')} differs from {key}"
            else:
                withheld[hour] = why
                if write:
                    unresolved[hour] = why
            continue
        t_in, t_ev, key, avail, c = best
        if avail > now:                                          # decision not yet available
            pending[hour] = avail
            continue
        rec = c["build"](avail)
        rec.update(control_policy=POLICY, control_hour=hour, control_key=key, t_persisted=now,
                   hour_closed_at_selection=hour + H <= now,
                   hour_closed_at_previous_run=bool(last_cutoff is not None and hour + H <= last_cutoff))
        controls.append(rec)
        proposals.append(rec)
        per_hour[hour] = {"selected": t_in, "decision": avail, "state": "proposed" if write else "provisional"}
    return controls, proposals, {"per_hour": per_hour, "reasons": reasons, "pending": pending,
                                 "withheld": withheld, "unresolved": unresolved,
                                 "eligible_hours": sorted(buckets), "candidates": len(candidates)}


def validate(controls, now, stored=None):
    """Raise ControlIntegrityError unless every control is usable at `now`, there is one per hour and,
    when `stored` is given (a writing run), each control equals the stored record."""
    hours = set()
    for r in controls:
        why = stored_problem(r, now)
        if why is not None:
            raise ControlIntegrityError(f"control for hour {r.get('control_hour')}: {why}")
        if r["control_hour"] in hours:
            raise ControlIntegrityError(f"two controls for hour {r['control_hour']}")
        hours.add(r["control_hour"])
        if stored is not None and (r["control_hour"] not in stored or _canon(stored[r["control_hour"]]) != _canon(r)):
            raise ControlIntegrityError(f"control for hour {r['control_hour']} is not the stored selection")


def diagnose(sel_diag, now, window_start, used=(), stored=None):
    """Compact comparison-coverage diagnostics over the closed and current hours from window_start."""
    if window_start is None:
        return {"policy": POLICY, "window": None}
    start = window_start // H * H
    hours = list(range(start, now // H * H + H, H))
    closed = [h for h in hours if h + H <= now]
    ph, eligible = sel_diag["per_hour"], set(sel_diag["eligible_hours"])
    pending, withheld = sel_diag.get("pending", {}), sel_diag.get("withheld", {})
    missing = {}
    for h in closed:
        if h in ph or h in pending or h in withheld:
            continue
        why = sel_diag["reasons"].get(h)
        missing[h] = ("; ".join(f"{k} x{v}" for k, v in sorted(why.items())) if why
                      else "missing collection: no record with required inputs available in this hour")
    delays = sorted((v["selected"] - h) / 60_000 for h, v in ph.items())
    ready_unselected = [h for h in closed if h in eligible and h not in ph and h not in pending and h not in withheld]
    states = {}
    for v in ph.values():
        states[v["state"]] = states.get(v["state"], 0) + 1
    used_hours = {r["control_hour"] for r in used}
    out = {"policy": POLICY, "window": [start, now], "hours_covered": len(hours), "closed_hours": len(closed),
           "partial_hour": hours[-1] if hours and hours[-1] + H > now else None,
           "hours_with_eligible_candidates": len([h for h in hours if h in eligible or h in ph]),
           "selected": len(ph), "selected_closed": len([h for h in closed if h in ph]),
           "frozen_selected": states.get("stored", 0), "selection_states": states,
           "selected_times": [[h, v["selected"], v["decision"], v["state"]] for h, v in sorted(ph.items())],
           "pending_processing": [[h, t] for h, t in sorted(pending.items())],
           "pending_processing_closed_hours": len([h for h in closed if h in pending]),
           "withheld_stored": [[h, why] for h, why in sorted(withheld.items())],
           "missing_closed_hours": [[h, why] for h, why in sorted(missing.items())],
           "closed_hours_with_candidates_but_no_control": ready_unselected,
           "proposals_accepted": sel_diag.get("accepted", []), "proposals_superseded": sel_diag.get("superseded", []),
           "unresolved_conflicts": [[h, why] for h, why in sorted(sel_diag.get("unresolved", {}).items())],
           "controls_fingerprint": fingerprint(used),
           "stored_fingerprint": (fingerprint([stored[h] for h in used_hours if h in stored]) if stored is not None else None),
           "delay_from_hour_to_availability_min": ({"min": round(delays[0], 1), "median": round(delays[len(delays) // 2], 1),
                                                   "max": round(delays[-1], 1)} if delays else None)}
    out["used_equals_stored"] = (out["controls_fingerprint"] == out["stored_fingerprint"]) if stored is not None else None
    out["integrity_failures"] = len(out["unresolved_conflicts"]) + len(ready_unselected)
    return out


def apply(lab, candidates, window_start):
    """Select this run's controls for a module and return (controls, diagnostics).

    lab.control_context (set per design by lab/run.py) carries the stored selections ("frozen"),
    the previous run's cutoff, the design (whose version namespace stores selections) and a list
    of this run's accepted selections ("new"). With lab.write and a design, the run is a WRITING
    run: proposals are persisted under the lock, read back, and the returned controls are the
    stored records (see "authority"). Otherwise nothing is written and new selections are
    provisional. Without a context nothing is frozen or persisted."""
    now = getattr(lab, "now", None)
    if now is None:          # no cutoff given (offline helpers): as of the latest decision the data allow
        now = max((c["t_inputs"] for c in candidates if c["t_inputs"] is not None), default=0) + ASSUMED_PROCESSING_MS
    ctx = getattr(lab, "control_context", None)
    write = bool(ctx is not None and ctx.get("design") is not None and getattr(lab, "write", False))
    frozen = (ctx or {}).get("frozen") or {}
    controls, proposals, sel = select(candidates, now, frozen, (ctx or {}).get("last_cutoff"), write)
    stored = None
    if write:
        if proposals:
            persist_selections(lab.base, ctx["design"], proposals)
        stored = load_selections(lab.base, ctx["design"])                 # authoritative
        ctx["frozen"] = stored
        accepted = [p["control_hour"] for p in proposals
                    if p["control_hour"] in stored and _canon(stored[p["control_hour"]]) == _canon(p)]
        superseded = [p["control_hour"] for p in proposals if p["control_hour"] not in accepted]
        missing = [h for h in superseded if h not in stored]
        if missing:
            raise ControlIntegrityError(f"selections for hours {missing} were not stored")
        controls, again, sel = select(candidates, now, stored, ctx.get("last_cutoff"), write)
        if again:
            raise ControlIntegrityError(f"hours {[r['control_hour'] for r in again]} still unselected after storing")
        for h in accepted:
            if h in sel["per_hour"]:
                sel["per_hour"][h]["state"] = "accepted"
        sel["accepted"], sel["superseded"] = accepted, superseded
        ctx.setdefault("new", []).extend(stored[h] for h in accepted)
    elif ctx is not None:
        ctx.setdefault("new", []).extend(proposals)
    validate(controls, now, stored)
    return controls, diagnose(sel, now, window_start, controls, stored)


AGREEMENT_FIELDS = ("control_hour", "control_key", "t_event", "t_inputs", "t_available", "t_persisted",
                    "inputs_sha256", "features")


def evidence_agreement(labelled, stored):
    """Check that the controls a pass actually labelled (their long rows) are the stored selections,
    field by field. Returns {"checked": n, "mismatches": [...], "fingerprint": sha256}."""
    rows = [e for e, _, _ in labelled if e.get("group") == "control_long" and e.get("control_policy") == POLICY]
    bad = []
    for e in rows:
        s = stored.get(e.get("control_hour"))
        if s is None or any(_canon(e.get(f)) != _canon(s.get(f)) for f in AGREEMENT_FIELDS):
            bad.append(e.get("control_hour"))
    core = [{f: e.get(f) for f in AGREEMENT_FIELDS} for e in rows]
    return {"checked": len(rows), "mismatches": bad, "fingerprint": fingerprint(core)}
