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


def check():
    m = json.loads((D / "manifest.json").read_text())
    probs = [f"{k}: drift" for k, v in body().items() if m.get(k) != v]
    if (D / "enforcement/desk_evidence.py").read_bytes() != (ROOT / "research_tools/evidence_contract.py").read_bytes():
        probs.append("evidence contract copies differ")
    reg = json.loads((D / "../o33-v3/registration.json").read_text())
    if reg["files_sha256"]["desk_calls.py"] != sha("../o33-v3/desk_calls.py"):
        probs.append("frozen v3 desk_calls.py changed")
    return probs


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        (D / "manifest.json").write_text(json.dumps(body(), indent=1, sort_keys=True) + "\n")
        print("written")
    else:
        p = check()
        print("OK" if not p else "\n".join(p))
        sys.exit(1 if p else 0)
