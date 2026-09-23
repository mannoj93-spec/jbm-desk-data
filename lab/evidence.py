"""Evidence cards, the research report and skill-change proposals (lab-2.0).

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
evidence, every variant tried, the status with the checks of the last look, limitations, and how
to reproduce it.

reports/skill_proposals.md proposes a change ONLY for a design whose current version is
"supported"; otherwise it says why not. Nothing here edits a skill file. No card or report calls a
result significant, profitable or an edge.
"""
from pathlib import Path

from lab import outcomes
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


def card(design, result, commit, input_hashes, registration, superseded):
    primary = next(v for v in result["variants"] if v["name"] == design["primary_variant"])
    passes = {}
    for p in primary["passes"]:
        passes[p["basis"]] = {k: p[k] for k in ("state", "reasons", "coverage", "window", "firings", "episodes",
                                                "controls", "quality", "freeze_audit", "data_sha256")}
        passes[p["basis"]]["phases"] = {ph: _public(s) for ph, s in p["phases"].items()}
    return {
        "schema": CARD_SCHEMA, "design": design["id"], "evaluation_version": design["_version"],
        "design_version": design.get("version"), "design_sha256": design["_sha256"],
        "version_components": design["_components"], "registered_at": iso(registration["registered"]) if registration else None,
        "superseded_versions": superseded, "module": design["module"], "family": design["family"],
        "condition": design["question"], "comparison": design["comparison"],
        "horizons_min": design["outcome"]["horizons_min"], "primary_horizon_min": design["outcome"]["primary_horizon"],
        "outcome_metric": design["outcome"]["metric"], "status": result["status"],
        "status_reason": result["status_reason"], "last_look": result.get("look"),
        "promotion_rules": "lab/experiments.py (module docstring)",
        "min_retained_observations": design["min_retained_observations"],
        "min_dependence_blocks": design.get("min_dependence_blocks", 20),
        "primary_variant": design["primary_variant"], "passes": passes,
        "baseline": {"predictors": design.get("baseline", {}).get("predictors"),
                     "method": "OLS on controls whose labels matured before each UTC day; residual difference"},
        "costs": outcomes.COST_MODEL, "exclusions": design.get("exclusions", []),
        "failures": [f"{p['basis']}: {r}" for p in primary["passes"] for r in p["reasons"]],
        "contradictory_evidence": contradictions(design, result),
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
            "module": design["module"], "family": design["family"], "condition": design["question"],
            "status": res["status"], "status_reason": res["status_reason"], "error": res.get("error"),
            "primary_horizon_min": design["outcome"]["primary_horizon"], "passes": {},
            "min_retained_observations": design.get("min_retained_observations"),
            "contradictory_evidence": [], "limitations": LIMITATIONS, "generated_at": iso(now)}


def write_cards(base, cards, now):
    base = Path(base)
    index = read_json(base / "research/evidence/index.json", {"designs": {}})
    for c in cards:
        if c.get("evaluation_version"):
            atomic_json(base / "research/evidence/v2" / f"{c['design']}@{c['evaluation_version']}.json", c)
        entry = index["designs"].setdefault(c["design"], {"versions": {}})
        entry["current"] = c.get("evaluation_version")
        entry["versions"].setdefault(c.get("evaluation_version") or "none", {})
        entry["versions"][c.get("evaluation_version") or "none"].update(status=c["status"], updated=iso(now))
        for old in c.get("superseded_versions") or []:
            entry["versions"].setdefault(old, {}).update(status="retired (superseded)")
        legacy = base / "research/evidence/cards" / f"{c['design']}.json"
        if legacy.exists():
            entry["legacy_lab_1_0_card"] = {"path": legacy.relative_to(base).as_posix(),
                                            "interpretation": "lab-1.0 output kept as recorded; superseded; not "
                                                              "evaluation evidence (see CHANGELOG 2.8)"}
    index.update(schema="evidence_index/1", updated=iso(now), lab_version=LAB_VERSION)
    atomic_json(base / "research/evidence/index.json", index)


def report(cards, now, meta):
    L = [f"# Research evidence", "",
         f"Generated {iso(now)} (input cutoff {iso(meta['cutoff'])}); {LAB_VERSION}; code {meta['code_sha256'][:12]}; "
         f"commit {meta.get('commit') or 'n/a'}; cost model {outcomes.COST_MODEL['version']} (assumed fees). "
         "Refreshed by the Research lab workflow every 6 hours; anything older is stale.", "",
         "Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.", "",
         "| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | "
         "Baseline residual diff (adj.) | Data |", "|---|---|---|---|---|---|---|"]
    for c in cards:
        ph = str(c["primary_horizon_min"])
        pro = (c.get("passes") or {}).get("prospective") or {}
        ev = ((pro.get("phases") or {}).get("evaluation") or {}).get(ph) or {}
        cnt = (ev.get("counts") or {}).get("test") or {}
        L.append(f"| {c['module']} | {c['design']} @ {c.get('evaluation_version')} | {c['status']} | "
                 f"{cnt.get('retained', 0)}/{c.get('min_retained_observations')} ; {cnt.get('blocks', 0)} | "
                 f"{_ci((ev.get('diff_test_minus_reference') or {}).get('adjusted'))} | "
                 f"{_ci(((ev.get('baseline') or {}).get('residual_diff') or {}).get('adjusted'))} | "
                 f"{pro.get('state', 'n/a')} |")
    L += ["", "## Per design", ""]
    for c in cards:
        ph = str(c["primary_horizon_min"])
        L.append(f"### {c['design']} @ {c.get('evaluation_version')} - {c['status']}")
        L.append(f"{c['condition']} Status: {c['status_reason']}.")
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
         "lab-2.0 promotion rules (data quality, retained observations and dependence blocks, multiplicity-adjusted "
         "effect, out-of-sample baseline added value, comparability, stability, at a scheduled look).", ""]
    supported = [c for c in cards if c["status"] == "supported"]
    if not supported:
        L += ["**No change is proposed.** No design's current version is supported.", "",
              "| Design @ version | Status | Why no proposal |", "|---|---|---|"]
        for c in cards:
            why = c["status_reason"]
            pro = (c.get("passes") or {}).get("prospective") or {}
            if pro.get("reasons"):
                why += "; " + pro["reasons"][0]
            L.append(f"| {c['design']} @ {c.get('evaluation_version')} | {c['status']} | {why} |")
        L += ["", "Reanalysis and reconstruction results are hypotheses, never grounds for a rule."]
        return "\n".join(L) + "\n"
    for c in supported:
        ph = str(c["primary_horizon_min"])
        ev = c["passes"]["prospective"]["phases"]["evaluation"][ph]
        L += [f"## {c['design']} @ {c['evaluation_version']}",
              f"Proposed wording (as a conditional base rate, not a rule): \"{c['condition']} Prospective replays since "
              f"{c['registered_at']}: {ev['counts']['test']['retained']} retained observations in "
              f"{ev['counts']['test']['blocks']} dependence blocks; test minus reference at {ph} minutes, "
              f"multiplicity-adjusted interval {_ci(ev['diff_test_minus_reference']['adjusted'])}, net of assumed costs; "
              f"out-of-sample baseline residual difference {_ci(ev['baseline']['residual_diff']['adjusted'])}.\"",
              f"Limitations: {' '.join(LIMITATIONS)}",
              f"Contradictory evidence: {c['contradictory_evidence'] or 'none recorded'}.",
              f"Card: research/evidence/v2/{c['design']}@{c['evaluation_version']}.json", ""]
    return "\n".join(L) + "\n"
