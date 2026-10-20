#!/usr/bin/env python3
"""Write or check research/registrations/o33-v3.1/manifest.json (hashes computed, never typed).
    python3 scripts/o33_v31_manifest.py write|check"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "research/registrations/o33-v3.1"
FILES = ["spec.json", "README.md", "enforcement/desk_register.py", "enforcement/desk_evidence.py"]
FROZEN = ["../o33-v3/desk_calls.py", "../o33-v3/test_desk_calls.py", "../o33-v3/registration.json",
          "../o33-v3/enforcement/desk_calls_freeze.py"]


def sha(p):
    return hashlib.sha256((D / p).read_bytes()).hexdigest()


def body():
    return {"schema": "o33-amendment-manifest/1", "id": "O33 v3.1", "status": "prepared (effective at first push to main)",
            "files_sha256": {f: sha(f) for f in FILES}, "depends_on_frozen_sha256": {f: sha(f) for f in FROZEN},
            "evidence_contract_parity": "enforcement/desk_evidence.py == research_tools/evidence_contract.py",
            "wrapper_version": "register-2.3.0", "contract_version": "evidence-1.0.0"}


C = ROOT / "research/registrations/o33-v3.1-correction-1"
C_FILES = ["spec.json", "README.md", "enforcement/desk_register.py", "enforcement/desk_evidence.py"]


def correction_body():
    """Repo 2.30: O33 v3.1 correction 1 (evidence classes); it pins its own files and the v3.1 files it leaves frozen."""
    return {"schema": "o33-correction-manifest/1", "id": "O33 v3.1 correction 1",
            "status": "prepared (effective at first push to main)",
            "files_sha256": {f: hashlib.sha256((C / f).read_bytes()).hexdigest() for f in C_FILES},
            "depends_on_frozen_sha256": {f"../o33-v3.1/{f}": sha(f) for f in FILES},
            "evidence_contract_parity": "enforcement/desk_evidence.py == research_tools/evidence_contract.py",
            "wrapper_version": "register-2.4.0", "contract_version": "evidence-1.0.0"}


def _effective_problems(p, label):
    e = json.loads(p.read_text())
    a = e["evidence"]["activity"]
    if e["effective_utc"] != a["timestamp"] or a["after"] != e["evidence"]["merge_commit"]:
        return [f"{label}/effective.json: effective time or merge commit inconsistent with its activity record"]
    return []


def effective_check():
    """Each effective.json (v3.1 and, from repo 2.30.1, correction 1) is self-consistent: the API read is in the file.
    v3.1's is required (PR #44 merged 2026-10-19T19:51:07Z); correction 1's is required once it exists on main
    (PR #48 merged 2026-10-20T12:14:00Z), so a deleted record is reported."""
    probs = []
    if not (D / "effective.json").exists():
        probs.append("o33-v3.1/effective.json missing (PR #44 merged 2026-10-19T19:51:07Z)")
    else:
        probs += _effective_problems(D / "effective.json", "o33-v3.1")
    if not (C / "effective.json").exists():
        probs.append("o33-v3.1-correction-1/effective.json missing (PR #48 merged 2026-10-20T12:14:00Z)")
    else:
        probs += _effective_problems(C / "effective.json", "o33-v3.1-correction-1")
    return probs


def check():
    m = json.loads((D / "manifest.json").read_text())
    probs = [f"{k}: drift" for k, v in body().items() if m.get(k) != v]
    if (C / "manifest.json").exists():
        cm = json.loads((C / "manifest.json").read_text())
        probs += [f"correction-1 {k}: drift" for k, v in correction_body().items() if cm.get(k) != v]
        if (C / "enforcement/desk_evidence.py").read_bytes() != (ROOT / "research_tools/evidence_contract.py").read_bytes():
            probs.append("correction-1 evidence contract copy differs")
    else:
        probs.append("o33-v3.1-correction-1/manifest.json missing")
    probs += effective_check()
    if (D / "enforcement/desk_evidence.py").read_bytes() != (ROOT / "research_tools/evidence_contract.py").read_bytes():
        probs.append("evidence contract copies differ")
    reg = json.loads((D / "../o33-v3/registration.json").read_text())
    if reg["files_sha256"]["desk_calls.py"] != sha("../o33-v3/desk_calls.py"):
        probs.append("frozen v3 desk_calls.py changed")
    return probs


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        (D / "manifest.json").write_text(json.dumps(body(), indent=1, sort_keys=True) + "\n")
        (C / "manifest.json").write_text(json.dumps(correction_body(), indent=1, sort_keys=True) + "\n")
        print("written")
    else:
        p = check()
        print("OK" if not p else "\n".join(p))
        sys.exit(1 if p else 0)
