"""Evidence cards, the research report and skill-change proposals (lab-2.2, revisions 2.10-2.12).

Cards are versioned: research/evidence/v2/<design>@<evaluation version>.json (schema
evidence_card/2), one per evaluation version, never overwritten by another version.
research/evidence/index.json names the current version of each design, every superseded version
and the legacy lab-1.0 cards (research/evidence/cards/, kept byte-for-byte, marked legacy and not
evaluation evidence).

A card carries: the condition, horizons, versions and the components they bind, the phases
(reanalysis / evaluation / exploratory), per-horizon sample accounting (firings, episodes,
scorable, retained, blocks), outcome distributions, 90% and multiplicity-adjusted intervals, the
out-of-sample baseline and its residual difference, comparability, stability, regimes, costs,
data quality, freeze audit (frozen / revised / late replays), exclusions, failures, contradictory
evidence, every variant tried, the recorded checkpoints (look, n, cutoff, verdict, checks, manifest
sha256, whether the stored manifest re-verifies), the pending look, drift between a record and the
current data, limitations, and how to reproduce it.

reports/skill_proposals.md proposes a change ONLY for a design whose current version is
"supported" by a recorded checkpoint whose manifest re-verifies, and quotes that checkpoint's
numbers (never the growing live summary); otherwise it says why not. Nothing here edits a skill file. No card or report calls a
result significant, profitable or an edge.

PUBLICATION (2.12). publication(card) is the single decision used by the card, the run summary
(run_summary, read by scripts/merge_research.py), the report and skill_proposals: an attempt is
evaluation_valid only when its required research integrity passed or is not required
(experiments.evaluation_allowed) and it did not error; a proposal additionally needs status
"supported" from a re-verifying recorded checkpoint. A failed or incomplete integrity check
suppresses proposals even when an earlier recorded checkpoint says "supported". The card of a
failed attempt carries attempt (this cutoff, not valid) and last_valid_result (the last valid
card of this version, or none) so the last valid evidence is kept without being presented as a
current passing evaluation. Collection health (reports/latest.md), research integrity and
publication eligibility are reported separately.
"""
from pathlib import Path

from lab import experiments, outcomes
from lab.common import LAB_VERSION, atomic_json, iso, read_json

CARD_SCHEMA = "evidence_card/2"
REPO_URL = "https://github.com/mannoj93-spec/jbm-desk-data"
LIMITATIONS = [
    "Decisions are as-of replays computed by a 6-hourly lab; decision times assume 60 s of processing after the "
    "last required input and were not executed live (t_persisted shows when each was actually computed).",
    "Retained observations do not overlap in their label intervals; that does not make them independent. "
    "Intervals resample dependence blocks (overlap or same UTC day).",
    "Intervals are descriptive bootstrap intervals; the adjusted interval divides alpha by variants x looks "
    "(Bonferroni), which is conservative but not a formal test of profitability.",
    "Net returns use cost model costs-1, whose fee and slippage values are assumptions (see VALIDATION.md).",
    "'supported' means the declared criteria held on prospective replays; it is not proof of profitability.",
]


def _fmt(x):
    return "n/a" if x is None else f"{x * 1e4:+.1f} bp"


def _ci(ci):
    return "n/a" if not ci else f"[{_fmt(ci[0])}, {_fmt(ci[1])}]"


def _public(summary):
    """A phase summary without the private per-observation rows."""
    return {h: {k: v for k, v in s.items() if not k.startswith("_")} for h, s in (summary or {}).items()}


def contradictions(design, result):
    out, sign = [], design["comparison"]["hypothesised_sign"]
    ph = str(design["outcome"]["primary_horizon"])
    for v in result["variants"]:
        for p in v["passes"]:
            for phase, summ in p["phases"].items():
                for h, s in summ.items():
                    ci = (s.get("diff_test_minus_reference") or {}).get("alpha_0.10")
                    if ci and ((sign > 0 and ci[1] < 0) or (sign < 0 and ci[0] > 0)):
                        out.append(f"{v['name']} / {p['basis']} / {phase} / {h}m: 90% interval {_ci(ci)} lies on "
                                   "the opposite side of zero")
                    halves = s.get("chronological_halves")
                    if h == ph and halves and None not in halves and halves[0] * halves[1] < 0:
                        out.append(f"{v['name']} / {p['basis']} / {phase} / {h}m: chronological halves disagree "
                                   f"({_fmt(halves[0])} vs {_fmt(halves[1])})")
    return out


def checkpoint_view(design, result):
    """The card's view of recorded checkpoints: everything but the per-row manifest (which stays in
    research/v2/<design>/<version>/checkpoints.jsonl), plus whether the stored manifest re-verifies."""
    cps = result.get("checkpoints") or {}
    recs = []
    for r in cps.get("records") or []:
        recs.append({"look": r["look"], "n": r["n"], "cutoff": iso(r["cutoff"]), "cutoff_ms": r["cutoff"],
                     "completed_at": iso(r["completed_at"]), "verdict": r["verdict"], "checks": r["checks"],
                     "criteria": r["manifest"]["criteria"], "baseline": r["manifest"]["baseline"],
                     "manifest_sha256": r["manifest_sha256"], "lab_version": r.get("lab_version"),
                     "verified": experiments.verify_checkpoint(r, design)})
    return {"file": f"{experiments.ns(design)}/checkpoints.jsonl", "records": recs,
            "pending": cps.get("pending"), "drift": cps.get("drift") or [],
            "rule": "a checkpoint is computed once, from data known by its cutoff, and never recomputed"}


BAR_BASED = ("hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the "
             "collection-time policy)")
HORIZON_RULE = ("Only the primary horizon, fixed in the design before any data, decides checkpoints, status and "
                "skill proposals; secondary horizons are descriptive and cannot override a failed primary or "
                "trigger a proposal on their own.")


def control_accounting(design, registration, labelled, now):
    """Per-horizon accounting of the comparison observations (controls) of the primary prospective
    pass, per phase, from the labels the lab actually computed (read-only): selected, mature
    (horizon elapsed and bars in), scorable (complete label), retained (non-overlapping label
    intervals), baseline-usable (complete label with every baseline feature). An immature label or
    overlap thinning is counted here, never reported as a collection gap. Plus decision timing of
    the frozen events: source time, assumed decision time, actual lab persistence time."""
    from lab import experiments, stats
    ctl = [(e, labs, bf) for e, labs, bf in labelled if e["group"] == "control_long"]
    out = {}
    for h in design["outcome"]["horizons_min"]:
        row = {}
        for phase in ("reanalysis", "evaluation"):
            rows = [(e, labs.get(h) or labs.get(str(h)) or {}, bf) for e, labs, bf in ctl
                    if experiments._in_phase(e, phase, registration)]
            done = [v for _, v, _ in rows if v.get("status") == "complete"]
            kept, _ = stats.nonoverlap_intervals([dict(entry_t=v["entry_t"], exit_t=v["exit_t"]) for v in done])
            row[phase] = {"selected": len(rows), "mature": sum(1 for _, v, _ in rows if v.get("status") != "immature"),
                          "incomplete": sum(1 for _, v, _ in rows if v.get("status") == "incomplete"),
                          "scorable": len(done), "retained": len(kept),
                          "baseline_usable": sum(1 for _, v, bf in rows if v.get("status") == "complete" and bf)}
        out[str(h)] = row
    frozen = [e for e, _, _ in labelled if not e["group"].startswith("control") and e.get("t_persisted") is not None]
    lags = sorted((e["t_persisted"] - e["t_available"]) / 60_000 for e in frozen)
    timing = {"definitions": {"t_event": "source time the record describes",
                              "t_inputs": "required-input availability (latest observed_at of the inputs)",
                              "t_available": "ASSUMED decision time = t_inputs + 60 s processing (not measured)",
                              "t_persisted": "actual time a lab run first computed and froze the decision"},
              "frozen_events": len(frozen),
              "decision_lag_min": ({"median": round(lags[len(lags) // 2], 1), "max": round(lags[-1], 1)} if lags else None),
              "basis": "as-of replay by a 6-hourly lab; decisions were not executed live"}
    return {"by_horizon": out, "decision_timing": timing}


def card(design, result, commit, input_hashes, registration, superseded, accounting=None):
    primary = next(v for v in result["variants"] if v["name"] == design["primary_variant"])
    passes = {}
    for p in primary["passes"]:
        passes[p["basis"]] = {k: p[k] for k in ("state", "reasons", "coverage", "window", "firings", "episodes",
                                                "controls", "quality", "freeze_audit", "data_sha256")}
        if result.get("evaluation_blocked"):
            passes[p["basis"]]["phases"] = {}
            passes[p["basis"]]["phases_withheld"] = ("research integrity did not pass: descriptive summaries "
                                                     "computed from unvalidated inputs are not published")
        else:
            passes[p["basis"]]["phases"] = {ph: _public(s) for ph, s in p["phases"].items()}
    return {
        "schema": CARD_SCHEMA, "design": design["id"], "evaluation_version": design["_version"],
        "cutoff_ms": result["t"], "design_version": design.get("version"), "design_sha256": design["_sha256"],
        "version_components": design["_components"], "registered_at": iso(registration["registered"]) if registration else None,
        "superseded_versions": superseded, "module": design["module"], "family": design["family"],
        "condition": design["question"], "comparison": design["comparison"],
        "horizons_min": design["outcome"]["horizons_min"], "primary_horizon_min": design["outcome"]["primary_horizon"],
        "outcome_metric": design["outcome"]["metric"],
        "horizons": {"primary_min": design["outcome"]["primary_horizon"],
                     "secondary_min": [h for h in design["outcome"]["horizons_min"]
                                       if h != design["outcome"]["primary_horizon"]], "rule": HORIZON_RULE},
        "comparison_coverage": {"policy": ((passes.get("prospective") or {}).get("coverage") or {}).get("comparison")
                                or {"policy": BAR_BASED},
                                **(accounting or {"by_horizon": None, "decision_timing": None})},
        "research_integrity": result.get("integrity"),
        "status": result["status"],
        "status_reason": result["status_reason"], "checkpoints": checkpoint_view(design, result),
        "promotion_rules": "lab/experiments.py (module docstring)",
        "min_retained_observations": design["min_retained_observations"],
        "min_dependence_blocks": design.get("min_dependence_blocks", 20),
        "primary_variant": design["primary_variant"], "passes": passes,
        "baseline": {"predictors": design.get("baseline", {}).get("predictors"),
                     "method": "one OLS model per horizon on same-horizon controls whose labels were available "
                               "before each UTC day (and before a checkpoint's cutoff); residual difference"},
        "costs": outcomes.COST_MODEL, "exclusions": design.get("exclusions", []),
        "failures": [f"{p['basis']}: {r}" for p in primary["passes"] for r in p["reasons"]],
        "contradictory_evidence": [] if result.get("evaluation_blocked") else contradictions(design, result),
        "tested_variants": [{"name": v["name"], "params": v["params"], "descriptive": v["descriptive"],
                             "by_basis": {p["basis"]: {"episodes": p["episodes"], "state": p["state"]}
                                          for p in v["passes"]}} for v in result["variants"]],
        "multiple_testing": {"variants_tried_in_family": result["n_variants_family"],
                             "looks": 4, "adjustment": "Bonferroni: alpha 0.10 / (variants x looks)"},
        "limitations": LIMITATIONS,
        "dependencies": {"lab_version": LAB_VERSION, "code_sha256": result["code_sha256"],
                         "cost_model": outcomes.COST_MODEL["version"], "inputs": input_hashes},
        "reproduce": {"command": f"python -m lab.run update --now {result['t']}", "commit": commit,
                      "links": {"design": f"{REPO_URL}/blob/{commit or 'main'}/{design['_file']}"}},
        "generated_at": iso(result["t"]),
    }


def error_card(design, res, now):
    return {"schema": CARD_SCHEMA, "design": design["id"], "evaluation_version": design.get("_version"),
            "cutoff_ms": now, "research_integrity": res.get("integrity"), "module": design["module"], "family": design["family"], "condition": design["question"],
            "status": res["status"], "status_reason": res["status_reason"], "error": res.get("error"),
            "primary_horizon_min": design["outcome"]["primary_horizon"], "passes": {},
            "min_retained_observations": design.get("min_retained_observations"),
            "contradictory_evidence": [], "limitations": LIMITATIONS, "generated_at": iso(now)}


# ---- publication (2.12) ----------------------------------------------------------------------------
PUBLICATION_SCHEMA = "publication/1"
SUMMARY_SCHEMA = "lab_summary/2"


def verified_supported(card):
    """The recorded checkpoint a proposal would quote: supported and re-verified, else None."""
    return next((r for r in (card.get("checkpoints") or {}).get("records") or []
                 if r.get("verdict") == "supported" and r.get("verified")), None)


def publication(card):
    """The single publication decision for one attempt (see the module docstring)."""
    integ = card.get("research_integrity")
    st = card.get("status")
    valid = experiments.evaluation_allowed(integ) and st not in ("error", "not run")
    reasons = []
    if not integ:
        reasons.append("research integrity result missing")
    elif not experiments.evaluation_allowed(integ):
        reasons.append(f"research integrity {integ.get('status')}: " + ("; ".join(integ.get("reasons") or []) or "no reason"))
    if st in ("error", "not run"):
        reasons.append(f"evaluation {st}: {card.get('status_reason')}")
    cp = verified_supported(card)
    proposal = bool(valid and st == "supported" and cp is not None)
    if valid and st == "supported" and cp is None:
        reasons.append("status supported but no recorded checkpoint re-verifies")
    return {"schema": PUBLICATION_SCHEMA, "design": card.get("design"), "evaluation_version": card.get("evaluation_version"),
            "cutoff_ms": card.get("cutoff_ms"), "status": st,
            "validation": {"required": (integ or {}).get("required"), "status": (integ or {}).get("status", "missing")},
            "evaluation_valid": valid, "proposal_eligible": proposal,
            "proposal_checkpoint": ({"look": cp["look"], "manifest_sha256": cp["manifest_sha256"]} if proposal else None),
            "reasons": reasons}


def previous_card(base, card):
    """The card currently stored for this design version (None if none or unreadable)."""
    if not card.get("evaluation_version"):
        return None
    return read_json(Path(base) / "research/evidence/v2" / f"{card['design']}@{card['evaluation_version']}.json", None)


def _valid_view(c):
    return {"cutoff": iso(c.get("cutoff_ms")) if c.get("cutoff_ms") else c.get("generated_at"),
            "cutoff_ms": c.get("cutoff_ms"), "status": c.get("status"), "status_reason": c.get("status_reason"),
            "checkpoints": [{k: r.get(k) for k in ("look", "n", "cutoff", "verdict", "manifest_sha256", "verified")}
                            for r in (c.get("checkpoints") or {}).get("records") or []]}


def with_attempt(card, previous=None):
    """Attach the publication decision, this attempt, and the last valid result of this version."""
    card = dict(card, publication=publication(card))
    valid = card["publication"]["evaluation_valid"]
    card["attempt"] = {"cutoff": iso(card.get("cutoff_ms")), "cutoff_ms": card.get("cutoff_ms"),
                       "status": card.get("status"), "evaluation_valid": valid}
    if valid:
        card["last_valid_result"] = {"this_attempt": True, "cutoff_ms": card.get("cutoff_ms")}
    else:
        prev = previous or {}
        if (prev.get("publication") or {}).get("evaluation_valid") is True:
            card["last_valid_result"] = dict(_valid_view(prev), this_attempt=False)
        else:
            lv = prev.get("last_valid_result")
            card["last_valid_result"] = lv if isinstance(lv, dict) and not lv.get("this_attempt") else None
    return card


def run_summary(results, cards, now, commit, write, meta):
    """Machine-readable summary of a lab run (stdout / --summary): the publication metadata the
    persist job verifies before publishing anything."""
    by = {c["design"]: c for c in cards}
    designs = {}
    for r in results:
        c = by.get(r["design"]) or {}
        pub = c.get("publication") or publication(dict(c, design=r["design"], status=r["status"]))
        integ = r.get("integrity")
        designs[r["design"]] = {
            "design": r["design"], "version": r.get("version"), "cutoff_ms": now, "cutoff": iso(now),
            "status": r["status"], "reason": r["status_reason"], "seconds": r.get("seconds"),
            "passes": [(p["basis"], p["state"], p["episodes"]) for v in r.get("variants", [])[:1] for p in v["passes"]],
            "validation": {"required": (integ or {}).get("required"), "status": (integ or {}).get("status", "missing"),
                           "reasons": (integ or {}).get("reasons") or []},
            "integrity": integ, "publication": pub, "last_valid_result": c.get("last_valid_result")}
    return {"schema": SUMMARY_SCHEMA, "t": iso(now), "cutoff_ms": now, "seconds": meta["seconds"], "commit": commit,
            "code_sha256": meta.get("code_sha256"), "wrote": write, "designs": designs}


def write_cards(base, cards, now):
    base = Path(base)
    index = read_json(base / "research/evidence/index.json", {"designs": {}})
    for c in cards:
        if c.get("evaluation_version"):
            atomic_json(base / "research/evidence/v2" / f"{c['design']}@{c['evaluation_version']}.json", c)
        entry = index["designs"].setdefault(c["design"], {"versions": {}})
        entry["current"] = c.get("evaluation_version")
        entry["versions"].setdefault(c.get("evaluation_version") or "none", {})
        pub = c.get("publication") or publication(c)
        lv = c.get("last_valid_result") or {}
        entry["versions"][c.get("evaluation_version") or "none"].update(
            status=c["status"], updated=iso(now), evaluation_valid=pub["evaluation_valid"],
            validation=pub["validation"]["status"], proposal_eligible=pub["proposal_eligible"],
            last_valid=(iso(lv.get("cutoff_ms")) if lv.get("cutoff_ms") else None))
        for old in c.get("superseded_versions") or []:
            v = entry["versions"].setdefault(old, {})
            v.update(status="retired (superseded)")
            v.setdefault("superseded_by", c.get("evaluation_version"))
        legacy = base / "research/evidence/cards" / f"{c['design']}.json"
        if legacy.exists():
            entry["legacy_lab_1_0_card"] = {"path": legacy.relative_to(base).as_posix(),
                                            "interpretation": "lab-1.0 output kept as recorded; superseded; not "
                                                              "evaluation evidence (see CHANGELOG 2.8)"}
    index.update(schema="evidence_index/1", updated=iso(now), lab_version=LAB_VERSION)
    atomic_json(base / "research/evidence/index.json", index)


def _hm(ms):
    return iso(ms)[11:16] if ms else "n/a"


def coverage_lines(c):
    """Compact comparison-coverage lines for the research report."""
    cc = c.get("comparison_coverage") or {}
    pol = cc.get("policy") or {}
    L = []
    if pol.get("window"):
        miss = pol.get("missing_closed_hours") or []
        dl = pol.get("delay_from_hour_to_availability_min") or {}
        L.append(f"- comparison coverage ({pol['policy']}): {iso(pol['window'][0])} to {iso(pol['window'][1])}; "
                 f"{pol['closed_hours']} closed hours + {'1 partial' if pol.get('partial_hour') else '0 partial'}; "
                 f"{pol['hours_with_eligible_candidates']} hours with eligible candidates; {pol['selected']} selected "
                 f"({pol['frozen_selected']} frozen earlier); {len(miss)} closed hours without a control"
                 + (f" (e.g. {_hm(miss[0][0])}: {miss[0][1]})" if miss else "")
                 + (f"; availability {dl['median']} min after the hour (median, range {dl['min']}-{dl['max']})" if dl else ""))
        pend = pol.get("pending_processing") or []
        if pend or pol.get("proposals_accepted") or pol.get("proposals_superseded") or pol.get("withheld_stored"):
            L.append(f"- selections: {len(pol.get('proposals_accepted') or [])} accepted this run, "
                     f"{len(pol.get('proposals_superseded') or [])} proposals superseded by stored winners, "
                     f"{len(pend)} hours pending processing (decision after the cutoff), "
                     f"{len(pol.get('withheld_stored') or [])} stored records withheld at this cutoff")
        if pol.get("controls_fingerprint"):
            L.append(f"- controls used: sha256 {pol['controls_fingerprint'][:16]}"
                     + (f"; equal to the stored selections: {pol['used_equals_stored']}" if pol.get("used_equals_stored") is not None else ""))
        integ = cc.get("integrity") or {}
        if integ and not integ.get("ok", True):
            L.append(f"- RESEARCH INTEGRITY FAILURE: unresolved conflicts {integ.get('unresolved_conflicts')}; "
                     f"ready-but-unselected hours {integ.get('ready_but_unselected')}; evidence mismatches "
                     f"{(integ.get('evidence_agreement') or {}).get('mismatches')}")
        elif integ.get("evidence_agreement"):
            ea = integ["evidence_agreement"]
            L.append(f"- labelled controls = stored selections: {ea['checked']} checked, {len(ea['mismatches'])} mismatches")
        if pol.get("closed_hours_with_candidates_but_no_control"):
            L.append(f"- WARNING: closed hours with eligible candidates but no selected control: "
                     f"{', '.join(_hm(h) for h in pol['closed_hours_with_candidates_but_no_control'])}")
    elif pol.get("policy"):
        L.append(f"- comparison coverage: {pol['policy']}")
    bh = cc.get("by_horizon") or {}
    if bh:
        prim = str((c.get("horizons") or {}).get("primary_min") or c.get("primary_horizon_min"))
        cells = []
        for h in sorted(bh, key=int):
            e = bh[h]["evaluation"]
            r = bh[h]["reanalysis"]
            cells.append(f"{h}m{'*' if h == prim else ''} eval {e['selected']}/{e['mature']}/{e['scorable']}/"
                         f"{e['retained']}/{e['baseline_usable']}, reanalysis {r['selected']}/{r['mature']}/"
                         f"{r['scorable']}/{r['retained']}/{r['baseline_usable']}")
        L.append("- controls selected/mature/scorable/retained/baseline-usable (* primary): " + "; ".join(cells))
    dt_ = cc.get("decision_timing") or {}
    if dt_.get("frozen_events"):
        lag = dt_.get("decision_lag_min") or {}
        L.append(f"- decision timing: {dt_['frozen_events']} frozen events; lab persisted them {lag.get('median')} min "
                 f"(median, max {lag.get('max')}) after the assumed decision time (inputs + 60 s); as-of replay, "
                 "not live execution")
    return L


def _integ_cell(c):
    i = c.get("research_integrity")
    if not i:
        return "MISSING"
    return {"not_required": "not required (bar-based)", "passed": "passed", "failed": "FAILED",
            "incomplete": "INCOMPLETE"}.get(i.get("status"), str(i.get("status")))


def _pub_cell(c):
    pub = c.get("publication") or publication(c)
    if not pub["evaluation_valid"]:
        return "BLOCKED"
    return "valid; proposal eligible" if pub["proposal_eligible"] else "valid"


def report(cards, now, meta):
    L = [f"# Research evidence", "",
         f"Generated {iso(now)} (input cutoff {iso(meta['cutoff'])}); {LAB_VERSION}; code {meta['code_sha256'][:12]}; "
         f"commit {meta.get('commit') or 'n/a'}; cost model {outcomes.COST_MODEL['version']} (assumed fees). "
         "Refreshed by the Research lab workflow every 6 hours; anything older is stale.", "",
         "Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.", "",
         "Three separate signals: **collection health** is the collector's (reports/latest.md; the Data column is "
         "the state of this design's inputs); **research integrity** is whether the design's required inputs "
         "(hourly controls: policy conflicts, stored = labelled) validated in this attempt; **publication** is "
         "whether this attempt's evaluation may stand as the current result and, if supported, feed a proposal. A "
         "blocked attempt names the last valid result instead of presenting it as current.", "",
         "| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | "
         "Baseline residual diff (adj.) | Data | Integrity | Publication |", "|---|---|---|---|---|---|---|---|---|"]
    for c in cards:
        ph = str(c["primary_horizon_min"])
        pro = (c.get("passes") or {}).get("prospective") or {}
        ev = ((pro.get("phases") or {}).get("evaluation") or {}).get(ph) or {}
        cnt = (ev.get("counts") or {}).get("test") or {}
        L.append(f"| {c['module']} | {c['design']} @ {c.get('evaluation_version')} | {c['status']} | "
                 f"{cnt.get('retained', 0)}/{c.get('min_retained_observations')} ; {cnt.get('blocks', 0)} | "
                 f"{_ci((ev.get('diff_test_minus_reference') or {}).get('adjusted'))} | "
                 f"{_ci(((ev.get('baseline') or {}).get('residual_diff') or {}).get('adjusted'))} | "
                 f"{pro.get('state', 'n/a')} | {_integ_cell(c)} | {_pub_cell(c)} |")
    L += ["", "## Per design", ""]
    for c in cards:
        ph = str(c["primary_horizon_min"])
        L.append(f"### {c['design']} @ {c.get('evaluation_version')} - {c['status']}")
        L.append(f"{c['condition']} Status: {c['status_reason']}.")
        pub = c.get("publication") or publication(c)
        L.append(f"- research integrity: {_integ_cell(c)}; publication: {_pub_cell(c)}"
                 + (f" ({'; '.join(pub['reasons'])})" if pub["reasons"] else ""))
        if not pub["evaluation_valid"]:
            lv = c.get("last_valid_result")
            L.append("- LATEST ATTEMPT BLOCKED at " + str(iso(c.get("cutoff_ms"))) + "; last valid result of this version: "
                     + (f"{lv['status']} as of {lv['cutoff']} (history, not a current passing evaluation)" if lv
                        else "none recorded"))
        cp = c.get("checkpoints") or {}
        hist = "" if pub["evaluation_valid"] else " [recorded earlier; history]"
        for r in cp.get("records") or []:
            L.append(f"- checkpoint {r['look']}: n={r['n']}, cutoff {r['cutoff']}, verdict {r['verdict']}, manifest "
                     f"{r['manifest_sha256'][:12]} ({'re-verified' if r['verified'] else 'FAILED re-verification'}){hist}")
        if cp.get("pending"):
            q = cp["pending"]
            L.append(f"- checkpoint {q['look']} pending: {q['retained']}/{q['need']} retained test observations known")
        for d in cp.get("drift") or []:
            L.append(f"- drift at checkpoint {d['look']}: {d['note']}")
        hz = c.get("horizons") or {}
        if hz:
            L.append(f"- horizons: primary {hz['primary_min']} min (decides status and proposals); secondary "
                     f"{', '.join(str(x) for x in hz['secondary_min']) or 'none'} min (descriptive only)")
        L += coverage_lines(c)
        if c.get("error"):
            L.append(f"- error: {c['status_reason']}")
        for basis, p in (c.get("passes") or {}).items():
            for phase, summ in p["phases"].items():
                s = summ.get(ph)
                if not s:
                    continue
                t, r = s["counts"]["test"], s["counts"]["reference"]
                L.append(f"- {basis}/{phase}: test firings {t['firings']}, episodes {t['episodes']}, scorable "
                         f"{t['scorable']}, retained {t['retained']} in {t['blocks']} blocks; reference retained "
                         f"{r['retained']}; test mean {_fmt(s['test'].get('mean'))} vs reference "
                         f"{_fmt(s['reference'].get('mean'))}; 90% {_ci(s['diff_test_minus_reference']['alpha_0.10'])}.")
            if p.get("freeze_audit"):
                L.append(f"- frozen decisions: {p['freeze_audit']}")
            if p["reasons"]:
                L.append(f"- {basis} data: {'; '.join(p['reasons'])}")
        if c.get("contradictory_evidence"):
            L.append(f"- contradictory evidence ({len(c['contradictory_evidence'])}): {c['contradictory_evidence'][0]}")
        if c.get("multiple_testing"):
            L.append(f"- variants tried in family {c['family']}: {c['multiple_testing']['variants_tried_in_family']}")
        L.append("")
    return "\n".join(L) + "\n"


def skill_proposals(cards, now):
    L = ["# Proposed skill changes", "", f"Generated {iso(now)}. For human review; nothing here edits a skill file.",
         "A change is proposed only for a design whose CURRENT evaluation version is **supported** under the "
         "lab-2.1+ promotion rules (data quality, retained observations and dependence blocks, multiplicity-adjusted "
         "effect, out-of-sample baseline added value, comparability, stability) at a RECORDED checkpoint whose manifest "
         "re-verifies; the wording quotes that checkpoint, not later data. " + HORIZON_RULE, ""]

    evidence_cp = verified_supported
    supported = [c for c in cards if publication(c)["proposal_eligible"]]
    if not supported:
        L += ["**No change is proposed.** No design's current version is supported by a verified checkpoint.", "",
              "| Design @ version | Status | Why no proposal |", "|---|---|---|"]
        for c in cards:
            why = c["status_reason"]
            pub = publication(c)
            if not pub["evaluation_valid"]:
                why = "proposal suppressed - " + "; ".join(pub["reasons"])
                if any(r.get("verdict") == "supported" for r in (c.get("checkpoints") or {}).get("records") or []):
                    why += " (an earlier recorded checkpoint says supported; it cannot override failed input integrity)"
            elif c["status"] == "supported":
                why = "status supported but no recorded checkpoint re-verifies; proposal withheld"
            pro = (c.get("passes") or {}).get("prospective") or {}
            if pro.get("reasons"):
                why += "; " + pro["reasons"][0]
            L.append(f"| {c['design']} @ {c.get('evaluation_version')} | {c['status']} | {why} |")
        L += ["", "Reanalysis and reconstruction results are hypotheses, never grounds for a rule."]
        return "\n".join(L) + "\n"
    for c in supported:
        r = evidence_cp(c)
        ch = r["checks"]
        L += [f"## {c['design']} @ {c['evaluation_version']}",
              f"Proposed wording (as a conditional base rate, not a rule): \"{c['condition']} Prospective replays since "
              f"{c['registered_at']}, checkpoint {r['look']} (cutoff {r['cutoff']}): {r['n']} retained observations in "
              f"{ch['blocks']['value']} dependence blocks; test minus reference at {c['primary_horizon_min']} minutes, "
              f"multiplicity-adjusted interval {_ci(ch['effect_adjusted']['interval'])}, net of assumed costs; "
              f"out-of-sample {r['baseline'].get('horizon_min')}-minute baseline residual difference "
              f"{_ci(ch['baseline_added_value']['interval'])}.\"",
              f"Evidence: {c['checkpoints']['file']} look {r['look']}, manifest sha256 {r['manifest_sha256']}.",
              f"Limitations: {' '.join(LIMITATIONS)}",
              f"Contradictory evidence: {c['contradictory_evidence'] or 'none recorded'}.",
              f"Card: research/evidence/v2/{c['design']}@{c['evaluation_version']}.json", ""]
    for c in cards:
        pub = publication(c)
        if c in supported:
            continue
        if not pub["evaluation_valid"]:
            L.append(f"- {c['design']} @ {c.get('evaluation_version')}: proposal suppressed - {'; '.join(pub['reasons'])}.")
        elif c["status"] == "supported":
            L.append(f"- {c['design']} @ {c.get('evaluation_version')}: status supported but no recorded checkpoint "
                     "re-verifies; proposal withheld.")
    return "\n".join(L) + "\n"
