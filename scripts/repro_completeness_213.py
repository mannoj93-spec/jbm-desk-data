#!/usr/bin/env python3
"""Before/after reproduction of the evidence-completeness gap fixed in 2.13, for any code tree.

  python scripts/repro_completeness_213.py [CODE_ROOT]

A valid run reaches a supported 100/20 checkpoint (synthetic inputs, real lab and merge code of
CODE_ROOT, via this checkout's regression/test_rev212.py); its handoff then loses the checkpoint
file, or the control files, before the merge. Temporary directories only; one JSON line per case.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE).resolve()
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(HERE / "regression")]
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("rev212", HERE / "regression/test_rev212.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
_m = importlib.util.spec_from_file_location("merge_under_test", ROOT / "scripts/merge_research.py")
t.merge_research = importlib.util.module_from_spec(_m)
_m.loader.exec_module(t.merge_research)
REL = f"research/v2/{t.DID}/{t.VER}"

print(json.dumps({"code_root": str(ROOT), "completeness_gate": hasattr(t.merge_research, "completeness_problems")}))
for name, drop in (("checkpoint file removed", "checkpoints.jsonl"), ("control files removed", "controls")):
    with tempfile.TemporaryDirectory() as tmp:
        world, repo, _ = t.BoundaryTests().scenario(tmp, malformed=False)
        rc, err, inc = t.compute(tmp, repo, t.BoundaryTests.NOW_B, world, "b")
        p = Path(inc, REL, drop)
        shutil.rmtree(p) if p.is_dir() else p.unlink()
        before = t.snapshot(repo)
        mrc, merr = t.merge(inc, repo)
        card = t.card_of(repo) or {}
        cps = t.cps_of(repo)
        stored = t.controls.load_selections(repo, t.the_design())
        integ = card.get("research_integrity") or {}
        used = [row[0] for row in ((card.get("comparison_coverage") or {}).get("policy") or {}).get("selected_times") or []]
        print(json.dumps({"case": name, "lab_exit": rc, "merge_exit": mrc,
                          "merge_stderr": merr.strip().splitlines()[0][:90] if merr.strip() else "",
                          "destination_unchanged": t.snapshot(repo) == before,
                          "published_card_status": card.get("status"),
                          "card_references_look": [r["look"] for r in (card.get("checkpoints") or {}).get("records") or []],
                          "published_checkpoints": sorted(cps),
                          "published_proposal": f"## {t.DID} @ {t.VER}" in (Path(repo, "reports/skill_proposals.md").read_text()
                                                                           if Path(repo, "reports/skill_proposals.md").exists() else ""),
                          "stored_controls_fingerprint_matches_card": (t.controls.fingerprint([stored[h] for h in used if h in stored])
                                                                       == integ.get("controls_fingerprint")) if card else None}))
