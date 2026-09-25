#!/usr/bin/env python3
"""Before/after reproductions of the two defects fixed in 2.12, for any code tree.

  python scripts/repro_publication_212.py [CODE_ROOT]

CODE_ROOT defaults to this checkout; point it at a checkout of b4db7d0 (2.11) to reproduce the
reviewed behaviour. The lab, experiments, evidence and merge code come from CODE_ROOT; the
synthetic observations and the compute -> merge pipeline come from this checkout's
regression/test_rev212.py. Everything runs in temporary directories. Prints one JSON object per
reproduction.
"""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE).resolve()
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(HERE / "regression")]
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("rev212", HERE / "regression/test_rev212.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
from lab import experiments  # noqa: E402
_m = importlib.util.spec_from_file_location("merge_under_test", ROOT / "scripts/merge_research.py")
t.merge_research = importlib.util.module_from_spec(_m)          # the merge of CODE_ROOT, not of this checkout
_m.loader.exec_module(t.merge_research)

H, T0, MINUTE = t.H, t.T0, t.MINUTE


def repro_boundary():
    """A stored control persisted 1 ms before its decision, at the run where look 1 completes."""
    b = t.BoundaryTests
    with tempfile.TemporaryDirectory() as tmp:
        world, repo, a = b().scenario(tmp)
        rc, err, inc, mrc, merr = t.publish(tmp, repo, b.NOW_B, world, "b")
        card, inc_card = t.card_of(repo), t.card_of(inc)
        summ = json.loads(Path(inc, "lab-summary.json").read_text())["designs"][t.DID]
        return {"repro": "integrity failure at a checkpoint boundary",
                "lab_exit": rc, "lab_stderr": err.strip().splitlines()[-1] if err.strip() else "",
                "lab_output_checkpoints": {k: r["verdict"] for k, r in experiments.load_checkpoints(inc, t.the_design()).items()},
                "lab_output_card": {"status": inc_card["status"],
                                    "research_integrity_ok": (inc_card.get("research_integrity") or {}).get("ok"),
                                    "research_integrity_status": (inc_card.get("research_integrity") or {}).get("status")},
                "lab_output_proposal": f"## {t.DID} @ {t.VER}" in Path(inc, "reports/skill_proposals.md").read_text(),
                "summary_validation": summ.get("validation"), "summary_publication_valid": (summ.get("publication") or {}).get("evaluation_valid"),
                "merge_exit": mrc, "merge_stderr": merr.strip().splitlines()[0] if merr.strip() else "",
                "published_checkpoints": {k: r["verdict"] for k, r in t.cps_of(repo).items()},
                "published_card_status": card["status"], "published_status_reason": card["status_reason"][:160],
                "published_proposal": f"## {t.DID} @ {t.VER}" in Path(repo, "reports/skill_proposals.md").read_text(),
                "watermark": {"before": b.NOW_A, "after": t.watermark(repo), "advanced": t.watermark(repo) != b.NOW_A},
                "last_valid_result": (card.get("last_valid_result") or {}).get("status")}


def repro_formatting():
    """The stored selection, and the same record with other whitespace / key order."""
    c = t.CanonicalMergeTests
    compact = json.dumps(c.WIN, sort_keys=True, separators=(",", ":"))
    reordered = json.dumps({"features": {"b": {"y": "s", "x": [1, 2]}, "a": 1}, "t_persisted": T0 + H,
                            "t_event": T0 + 20 * MINUTE, "control_hour": T0, "control_policy": c.WIN["control_policy"]},
                           separators=(", ", ": "))
    out = {"repro": "JSON-formatting false merge conflict"}
    for name, line in (("reformatted identical record", reordered),
                       ("genuinely different record", json.dumps(dict(c.WIN, t_event=T0 + 10 * MINUTE)))):
        with tempfile.TemporaryDirectory() as tmp:
            repo, inc, p = c().files(tmp, [compact], [line])
            before = p.read_bytes()
            rc, err = t.merge(inc, repo)
            out[name] = {"merge_exit": rc, "stderr": err.strip().splitlines()[0] if err.strip() else "",
                         "stored_bytes_unchanged": p.read_bytes() == before, "lines": len(p.read_text().splitlines())}
    return out


if __name__ == "__main__":
    print(json.dumps({"code_root": str(ROOT), "has_2_12_gate": hasattr(experiments, "input_integrity")}))
    for f in (repro_boundary, repro_formatting):
        try:
            print(json.dumps(f(), default=str))
        except Exception as exc:
            print(json.dumps({"repro": f.__name__, "error": f"{type(exc).__name__}: {exc}"}))
