#!/usr/bin/env python3
"""check_checksums - the release manifest SHA256SUMS: its scope, verification and refresh (repo 2.23; scope 2.25).

Scope (the single definition; VALIDATION.md and README cite it): every file tracked by git that is maintained by a
revision - code, workflows, documentation, tests, fixtures, protocols, the dashboard's source and static assets, and
frozen release artifacts - and nothing that changes without a revision:
  - collector and stream records: data/, streams/, state/, reports/, research/ (the lab's evidence and ledgers),
    registry/ (except its README and template), tests/ (except its README and template), desk/inputs/, desk/fits/;
  - append-only operational logs: desk/deployments.jsonl, desk/provenance_corrections.jsonl;
  - content-addressed calendar copies written by the range job: desk/calendars/<sha256>.csv (each name is its own
    hash, verified by desk/make_release.py check; repo 2.25);
  - files governed by a nested manifest: desk/research/o21/inputs/ and desk/research/o21/original/ (their hashes are
    in desk/research/o21/MANIFEST.json, which is itself in scope);
  - the manifest itself, and generated dashboard output (.dashboard-build/, never tracked).

  check     verify every listed hash AND that the listed set equals the scope; exit 1 on any difference
  refresh   rewrite SHA256SUMS for the scope (a release step, run on purpose; review the diff)
Stdlib only; needs git for the tracked-file list.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "SHA256SUMS"
EXCLUDED_TREES = ("data/", "streams/", "state/", "reports/", "research/", "desk/inputs/", "desk/fits/",
                  "desk/calendars/", "desk/research/o21/inputs/", "desk/research/o21/original/", ".dashboard-build/")
EXCLUDED_FILES = {MANIFEST, "desk/deployments.jsonl", "desk/provenance_corrections.jsonl"}
DATA_TREES_WITH_MAINTAINED_FILES = {"registry/": {"registry/README.md", "registry/_TEMPLATE.json"},
                                    "tests/": {"tests/README.md", "tests/_template.py"}}


def in_scope(path: str) -> bool:
    if path in EXCLUDED_FILES or path.startswith(EXCLUDED_TREES):
        return False
    for tree, keep in DATA_TREES_WITH_MAINTAINED_FILES.items():
        if path.startswith(tree):
            return path in keep
    return True


def tracked(root=ROOT) -> list:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True).stdout
    return sorted(p for p in out.decode().split("\0") if p)


def scope(root=ROOT, files=None) -> list:
    return [p for p in (files if files is not None else tracked(root)) if in_scope(p)]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(text: str) -> dict:
    out = {}
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        digest, _, name = line.partition("  ")
        if len(digest) != 64 or not name:
            raise ValueError(f"{MANIFEST} line {n} is malformed")
        if name in out:
            raise ValueError(f"{MANIFEST} lists {name} twice")
        out[name] = digest
    return out


def check(root=ROOT, files=None) -> list:
    """Problems (empty = the manifest verifies and matches its scope)."""
    root = Path(root)
    listed = parse((root / MANIFEST).read_text())
    want = set(scope(root, files))
    problems = []
    for name, digest in sorted(listed.items()):
        p = root / name
        if not p.is_file():
            problems.append(f"listed but missing: {name}")
        elif sha(p) != digest:
            problems.append(f"hash mismatch: {name}")
    problems += [f"in scope but not listed: {n}" for n in sorted(want - set(listed))]
    problems += [f"listed but out of scope: {n}" for n in sorted(set(listed) - want)]
    return problems


def refresh(root=ROOT, files=None) -> int:
    root = Path(root)
    names = scope(root, files)
    (root / MANIFEST).write_text("".join(f"{sha(root / n)}  {n}\n" for n in names))
    return len(names)


def main(argv) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    if cmd == "refresh":
        print(f"{MANIFEST}: {refresh()} files")
        return 0
    if cmd != "check":
        print(__doc__)
        return 2
    problems = check()
    n = len(parse((ROOT / MANIFEST).read_text()))
    for p in problems:
        print(f"FAIL {p}")
    print(f"{MANIFEST}: {n} entries; " + ("OK (hashes verify; listed set equals scope)" if not problems else f"{len(problems)} problem(s)"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
