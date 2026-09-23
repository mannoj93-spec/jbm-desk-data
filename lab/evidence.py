"""Evidence cards, the compact research report and skill-change proposals.

A card (research/evidence/cards/<design>.json, schema evidence_card/1) is the machine-readable
record a reviewer needs to judge one design without re-running anything: the condition, horizon,
versions and dependencies, independent episode counts, period and regimes, outcome distributions,
uncertainty, the simple baseline, costs, failures and exclusions, coverage, contradictory evidence,
every tested variant (null results included), the status, and how to reproduce it (command, code
hash, data hashes, commit, links).

reports/research.md summarises the cards. reports/skill_proposals.md proposes a change to the
trading skill files ONLY for a design whose status is "supported"; otherwise it says, per design,
why no change is proposed. Nothing here edits a skill file; proposals are for human review.
Language rule: no card or report calls a result significant, profitable or an edge; intervals are
descriptive and the number of variants tested in the family is always shown beside them.
"""
from pathlib import Path

from lab import outcomes
from lab.common import LAB_VERSION, atomic_json, iso

CARD_SCHEMA = "evidence_card/1"
REPO_URL = "https://github.com/mannoj93-spec/jbm-desk-data"


def _fmt(x, pct=True):
    if x is None:
        return "n/a"
    return f"{x * 1e4:+.1f} bp" if pct else f"{x:.3g}"


def contradictions(design, result):
    """Evidence that cuts against the design's hypothesis, gathered mechanically."""
    out, sign = [], design["comparison"]["hypothesised_sign"]
    ph = str(design["outcome"]["primary_horizon"])
    for v in result["variants"]:
        for p in v["passes"]:
            for phase, summ in p["phases"].items():
                for h, s in summ.items():
                    ci = s.get("diff_test_minus_reference_90")
                    if ci and ((sign > 0 and ci["hi90"] < 0) or (sign < 0 and ci["lo90"] > 0)):
                        out.append(f"{v['name']} / {p['basis']} / {phase} / {h}m: interval "
                                   f"[{_fmt(ci['lo90'])}, {_fmt(ci['hi90'])}] lies on the opposite side of zero")
                    halves = s.get("chronological_halves")
                    if h == ph and halves and None not in halves and halves[0] * halves[1] < 0:
                        out.append(f"{v['name']} / {p['basis']} / {phase} / {h}m: the two chronological halves "
                                   f"disagree in sign ({_fmt(halves[0])} vs {_fmt(halves[1])})")
    return out


def card(design, result, family_variants, commit, input_hashes):
    ph = str(design["outcome"]["primary_horizon"])
    primary = next(v for v in result["variants"] if v["name"] == design["primary_variant"])
    passes = {}
    for p in primary["passes"]:
        passes[p["basis"]] = {
            "state": p["state"], "reasons": p["reasons"], "coverage": p["coverage"], "window": p["window"],
            "firings": p["firings"], "independent_episodes_collapsed": p["episodes"], "controls": p["controls"],
            "immature_labels": p["immature_labels"], "incomplete_labels": p["incomplete_labels"],
            "data_sha256": p.get("data_sha256"),
            "primary_horizon": {ph: {phase: summ.get(ph) for phase, summ in p["phases"].items()}},
            "all_horizons": p["phases"]}
    failures = [f"{p['basis']}: {r}" for p in primary["passes"] for r in p["reasons"]]
    return {
        "schema": CARD_SCHEMA, "design": design["id"], "design_version": design["version"],
        "design_sha256": design["_sha256"], "module": design["module"], "family": design["family"],
        "condition": design["question"], "comparison": design["comparison"],
        "horizons_min": design["outcome"]["horizons_min"], "primary_horizon_min": design["outcome"]["primary_horizon"],
        "outcome_metric": design["outcome"]["metric"], "registered_at": iso(result["registered"]),
        "status": result["status"], "status_reason": result["status_reason"],
        "min_independent_episodes": design["min_independent_episodes"], "status_note": design.get("status_note"),
        "primary_variant": design["primary_variant"], "passes": passes,
        "baseline": {"reference_group": design["comparison"]["reference_group"],
                     "predictors": design.get("baseline_predictors", []),
                     "method": "test minus reference (day-block bootstrap, 90%); residual over an OLS fit on controls "
                               "when predictors are named"},
        "costs": outcomes.COST_MODEL, "exclusions": design.get("exclusions", []), "failures": failures,
        "contradictory_evidence": contradictions(design, result),
        "tested_variants": [{"name": v["name"], "params": v["params"],
                             "by_basis": {p["basis"]: {"episodes": p["episodes"], "state": p["state"],
                                                       "primary": {ph_: (s.get(ph) or {}).get("diff_test_minus_reference_90")
                                                                   for ph_, s in p["phases"].items()}}
                                          for p in v["passes"]}} for v in result["variants"]],
        "multiple_testing": {"variants_tested_in_family": family_variants,
                             "note": "intervals are not adjusted; read them against the number of variants tried"},
        "dependencies": {"lab_version": LAB_VERSION, "code_sha256": result["code_sha256"],
                         "cost_model": outcomes.COST_MODEL["version"], "inputs": input_hashes},
        "reproduce": {"command": "python -m lab.run update" + ("" if "reconstruction" not in passes else
                                                                " --reconstruct-days N"),
                      "commit": commit,
                      "links": {"design": f"{REPO_URL}/blob/{commit or 'main'}/{design['_file']}",
                                "module": f"{REPO_URL}/blob/{commit or 'main'}/lab/modules/{design['module']}.py"}},
        "generated_at": iso(result["t"]),
    }


def write_cards(base, cards):
    for c in cards:
        atomic_json(Path(base) / "research/evidence/cards" / f"{c['design']}.json", c)


def report(cards, now, run_meta):
    L = [f"# Research evidence ({iso(now)})", "",
         f"Lab {LAB_VERSION}; code {run_meta['code_sha256'][:12]}; commit {run_meta.get('commit') or 'n/a'}; "
         f"cost model {outcomes.COST_MODEL['version']} (assumed fees - see VALIDATION.md). "
         "Descriptive intervals only; no result here is described as significant or profitable.", "",
         "| Module | Design | Status | Prospective eval episodes | Primary diff (90%) | Data state |",
         "|---|---|---|---|---|---|"]
    for c in cards:
        ph = str(c["primary_horizon_min"])
        pro = c["passes"].get("prospective", {})
        ev = (pro.get("primary_horizon", {}).get(ph, {}) or {}).get("evaluation") or {}
        ci = ev.get("diff_test_minus_reference_90")
        L.append(f"| {c['module']} | {c['design']} ({ph}m) | {c['status']} | "
                 f"{ev.get('independent_test_episodes', 0)}/{c['min_independent_episodes']} | "
                 f"{'[' + _fmt(ci['lo90']) + ', ' + _fmt(ci['hi90']) + ']' if ci else 'n/a'} | "
                 f"{pro.get('state', 'n/a')} |")
    L += ["", "## Per design", ""]
    for c in cards:
        ph = str(c["primary_horizon_min"])
        L.append(f"### {c['design']} - {c['status']}")
        L.append(f"{c['condition']} Status reason: {c['status_reason']}.")
        for basis, p in c["passes"].items():
            summ = p["primary_horizon"][ph]
            for phase, s in summ.items():
                if not s:
                    continue
                ci = s.get("diff_test_minus_reference_90")
                L.append(f"- {basis}/{phase}: {s['independent_test_episodes']} test vs "
                         f"{s['independent_reference_episodes']} reference independent episodes over {s['days']} days; "
                         f"test mean {_fmt(s['test'].get('mean'))}, reference mean {_fmt(s['reference'].get('mean'))}, "
                         f"diff 90% {('[' + _fmt(ci['lo90']) + ', ' + _fmt(ci['hi90']) + ']') if ci else 'n/a'}.")
            if p["reasons"]:
                L.append(f"- {basis} data: {'; '.join(p['reasons'])}")
        if c["contradictory_evidence"]:
            L.append(f"- contradictory evidence: {len(c['contradictory_evidence'])} item(s), e.g. {c['contradictory_evidence'][0]}")
        L.append(f"- variants tested in family {c['family']}: {c['multiple_testing']['variants_tested_in_family']}")
        L.append("")
    return "\n".join(L) + "\n"


def skill_proposals(cards, now):
    L = [f"# Proposed skill changes ({iso(now)})", "",
         "Generated for human review. Nothing here has been applied to any skill file; the lab never edits "
         "skill files. A change is proposed only for a design whose status is **supported** (evaluation "
         "episodes at or after registration, minimum count met, intervals excluding zero in the "
         "hypothesised direction, both chronological halves agreeing).", ""]
    supported = [c for c in cards if c["status"] == "supported"]
    if not supported:
        L += ["**No change is proposed.** No design has reached supported status.", "",
              "| Design | Status | Why no proposal |", "|---|---|---|"]
        for c in cards:
            why = c["status_reason"]
            pro = (c.get("passes") or {}).get("prospective") or {}
            if pro.get("reasons"):
                why += "; " + pro["reasons"][0]
            L.append(f"| {c['design']} | {c['status']} | {why} |")
        L += ["", "Exploratory reconstructions and pre-registration episodes may be read as hypotheses to watch, "
              "never as grounds for a rule. Evaluate a revised skill with `python -m lab.skill_eval` before and "
              "after any change a human decides to make."]
        return "\n".join(L) + "\n"
    for c in supported:
        ph = str(c["primary_horizon_min"])
        ev = c["passes"]["prospective"]["primary_horizon"][ph]["evaluation"]
        ci = ev["diff_test_minus_reference_90"]
        L += [f"## {c['design']}",
              f"Proposed text (for the research-target section, as a conditional base rate, not a rule): "
              f"\"{c['condition']} Prospective evaluation since {c['registered_at']}: "
              f"{ev['independent_test_episodes']} independent episodes, test minus reference at {ph} minutes "
              f"{_fmt(ev['test'].get('mean'))} vs {_fmt(ev['reference'].get('mean'))}, 90% day-block interval "
              f"[{_fmt(ci['lo90'])}, {_fmt(ci['hi90'])}], net of assumed costs; "
              f"{c['multiple_testing']['variants_tested_in_family']} variants tested in the family.\"",
              f"Contradictory evidence to weigh: {c['contradictory_evidence'] or 'none recorded'}.",
              f"Card: research/evidence/cards/{c['design']}.json", ""]
    return "\n".join(L) + "\n"
