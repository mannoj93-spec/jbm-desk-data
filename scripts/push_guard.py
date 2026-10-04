#!/usr/bin/env python3
"""push_guard - fail-closed check that an automated writer commits and pushes only its documented outputs (repo 2.25).

scripts/commit_push.sh calls it twice:
  push_guard.py --writer W staged          before committing: every staged change
  push_guard.py --writer W outgoing BASE   before each push attempt (and again after a rebase): every commit in
                                           BASE..HEAD, BASE being the last remote tip this job knows about
A change passes only if it adds or modifies a regular file that scripts/writers.json lists for writer W and that is
not maintained by a revision (scripts/check_checksums.py scope). Deletions, renames, type changes, symlinks,
submodules and merge commits fail. Exit 1 names each refused path and nothing is committed or pushed.

This guards against accidental misuse by the repository's own jobs (an unrelated file left staged, a commit made
earlier in the job). It cannot restrain someone who holds the deploy key directly. Stdlib only; prints paths, never
credentials.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_checksums import in_scope   # noqa: E402

POLICY = HERE / "writers.json"
REGULAR = {"100644", "100755"}


def load(path=POLICY) -> dict:
    return json.loads(Path(path).read_text())["writers"]


def allowed(rule: dict, path: str, status: str, mode: str) -> str | None:
    """None when the change is a documented output of this writer; otherwise the reason it is refused."""
    if status not in ("A", "M"):
        return {"D": "deletion", "T": "type change"}.get(status, f"status {status}")
    if mode not in REGULAR:
        return f"not a regular file (mode {mode})"
    if in_scope(path):
        return "maintained by a revision (release manifest scope)"
    for pattern in rule.get("add_only", []):
        if re.search(pattern, path):
            return None if status == "A" else "content-addressed file may only be added"
    for entry in rule.get("allow", []):
        if (entry.endswith("/") and path.startswith(entry)) or path == entry:
            return None
    return "not a documented output of this writer"


def git(*args, cwd=None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def parse_raw(text: str) -> list:
    """[(status, path, new_mode)] from `git diff --raw --no-renames -z` output."""
    out, parts, i = [], text.split("\0"), 0
    while i < len(parts) - 1:
        meta = parts[i]
        if not meta.startswith(":"):
            i += 1
            continue
        fields = meta[1:].split()
        new_mode, status = fields[1], fields[4][0]
        out.append((status, parts[i + 1], new_mode if status != "D" else fields[0]))
        i += 2
    return out


def staged(cwd=None) -> list:
    return parse_raw(git("diff", "--cached", "--raw", "--no-renames", "-z", cwd=cwd))


def outgoing(base: str, cwd=None) -> list:
    """[(commit, [changes] or None for a merge)] for every commit in base..HEAD, oldest first."""
    out = []
    for c in git("rev-list", "--reverse", "--parents", f"{base}..HEAD", cwd=cwd).split("\n"):
        if not c.strip():
            continue
        sha, *parents = c.split()
        if len(parents) != 1:
            out.append((sha, None))
            continue
        out.append((sha, parse_raw(git("diff-tree", "--raw", "--no-renames", "-r", "-z", "--no-commit-id",
                                       parents[0], sha, cwd=cwd))))
    return out


def problems(writer: str, changes: list, policy: dict) -> list:
    rule = policy.get(writer)
    if rule is None:
        return [f"writer {writer!r} is not listed in scripts/writers.json"]
    out = []
    for status, path, mode in changes:
        why = allowed(rule, path, status, mode)
        if why:
            out.append(f"{path}: {why}")
    return out


def main(argv) -> int:
    args = argv[1:]
    if len(args) < 3 or args[0] != "--writer" or args[2] not in ("staged", "outgoing"):
        print(__doc__, file=sys.stderr)
        return 2
    writer, mode = args[1], args[2]
    policy = load()
    if mode == "staged":
        found = problems(writer, staged(), policy)
        where = "staged changes"
    else:
        if len(args) != 4:
            print("outgoing needs BASE", file=sys.stderr)
            return 2
        found = []
        for sha, changes in outgoing(args[3]):
            if changes is None:
                found.append(f"{sha[:12]}: merge commit")
            else:
                found += [f"{sha[:12]} {p}" for p in problems(writer, changes, policy)]
        where = f"outgoing commits ({args[3][:12]}..HEAD)"
    if found:
        print(f"push guard ({writer}): refused {len(found)} change(s) in {where}:", file=sys.stderr)
        for p in found[:50]:
            print(f"  {p}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
