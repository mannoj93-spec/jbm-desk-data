"""A consistent lab_summary/3 (the lab's publication metadata) for merge-only regression tests."""
from lab import controls, evidence
from lab.common import iso


def empty_inventory(name, version, cut, required):
    """The evidence inventory of a design version with no referenced checkpoint, no used control and
    no stored decision or outcome (2.13)."""
    return {"schema": evidence.INVENTORY_SCHEMA, "design": name, "evaluation_version": version, "cutoff_ms": cut,
            "checkpoints": [], "controls": ({"hours": [], "missing": [], "fingerprint": controls.fingerprint([]),
                                             "unusable_at_cutoff": []} if required else None),
            "events": {"count": 0, "sha256": evidence._set_sha([])},
            "outcomes": {"count": 0, "sha256": evidence._set_sha([])}}


def valid_summary(cut, designs, status="exploratory", integrity="passed"):
    """Every named design valid at cutoff `cut`, no proposal. designs: {design id: evaluation version}."""
    out = {"schema": evidence.SUMMARY_SCHEMA, "t": iso(cut), "cutoff_ms": cut, "designs": {}}
    for name, version in designs.items():
        integ = {"required": integrity != "not_required", "status": integrity, "ok": True, "reasons": []}
        out["designs"][name] = {
            "design": name, "version": version, "cutoff_ms": cut, "status": status, "reason": "x",
            "validation": {"required": integ["required"], "status": integrity, "reasons": []}, "integrity": integ,
            "publication": {"schema": "publication/1", "design": name, "evaluation_version": version, "cutoff_ms": cut,
                            "status": status, "validation": {"required": integ["required"], "status": integrity},
                            "evaluation_valid": True, "proposal_eligible": False, "proposal_checkpoint": None,
                            "reasons": []},
            "inventory": empty_inventory(name, version, cut, integ["required"])}
    return out


def batch_metadata(inc, cut, designs, **kw):
    """Write a consistent summary plus the outputs a lab run publishes with it (one card per design,
    the index, both reports) into the incoming directory `inc`; returns the summary."""
    import json
    from pathlib import Path
    s = valid_summary(cut, designs, **kw)
    inc = Path(inc)
    (inc / "research/evidence/v2").mkdir(parents=True, exist_ok=True)
    (inc / "reports").mkdir(parents=True, exist_ok=True)
    index = {"designs": {}}
    for name, e in s["designs"].items():
        card = {"design": name, "evaluation_version": e["version"], "cutoff_ms": cut, "generated_at": s["t"],
                "status": e["status"], "publication": e["publication"], "research_integrity": e["integrity"],
                "evidence_inventory": e["inventory"]}
        (inc / f"research/evidence/v2/{name}@{e['version']}.json").write_text(json.dumps(card))
        index["designs"][name] = {"current": e["version"], "versions": {e["version"]: {
            "status": e["status"], "evaluation_valid": e["publication"]["evaluation_valid"]}}}
    (inc / "research/evidence/index.json").write_text(json.dumps(dict(index, updated=s["t"])))
    (inc / "reports/research.md").write_text(f"# Research evidence\n\nGenerated {s['t']}.\n")
    (inc / "reports/skill_proposals.md").write_text(f"# Proposed skill changes\n\nGenerated {s['t']}.\n")
    (inc / "lab-summary.json").write_text(json.dumps(s))
    return s
