#!/usr/bin/env python3
"""Offline replay of the lean-rule backtest reproduction (retrospective exploration; not a registered test).

    python research/retrospective/lean-rules-2026-10-05/replay.py [--pkg DIR]

Decompresses the retained inputs into a temporary directory, verifies their sha256 against MANIFEST.json, checks the
package modules' sha256 (default --pkg: this repository's desk/, which carries the same jbm_archive archive-12.0.0
and jbm_measure measure-11.1.0 bytes as package 12.4.11), runs reproduce/run.py .. run4.py from copies whose only
change is the sys.path line (pointed at --pkg; reproduce/CHANGES.md lists the original paths), and compares each
output with reproduce/outputs/ after trailing-whitespace normalization. Exit 0 when every line matches except the
one machine-precision diagnostic recorded in REPRODUCTION.md (run3 line 1), else 1. Standard library only; no network.
"""
import difflib
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
KNOWN = {"run3": {1}}            # 1-based output lines allowed to differ (sigma check at machine precision)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(argv):
    pkg = Path(argv[argv.index("--pkg") + 1]) if "--pkg" in argv else REPO / "desk"
    man = json.loads((HERE / "MANIFEST.json").read_text())
    ok = True
    for mod, want in man["modules"].items():
        got = sha((pkg / mod).read_bytes())
        print(f"module {mod}: {'ok' if got == want else 'MISMATCH ' + got}")
        ok &= got == want
    with tempfile.TemporaryDirectory() as tmp:
        data, code = Path(tmp) / "data", Path(tmp) / "code"
        data.mkdir()
        code.mkdir()
        for name, want in man["inputs"].items():
            raw = gzip.decompress((HERE / "reproduce/data" / (name + ".gz")).read_bytes())
            print(f"input {name}: {'ok' if sha(raw) == want else 'MISMATCH'}")
            ok &= sha(raw) == want
            (data / name).write_bytes(raw)
        for s in ("run.py", "run2.py", "run3.py", "run4.py"):
            src = (HERE / "reproduce" / s).read_text()
            (code / s).write_text(re.sub(r"sys\.path\.insert\(0,\s*'[^']*'\)", f"sys.path.insert(0,{str(pkg)!r})", src))
        for s in ("run", "run2", "run3", "run4"):
            p = subprocess.run([sys.executable, "-B", "-E", "-s", str(code / f"{s}.py")], cwd=data,
                               capture_output=True, text=True)
            got = [l.rstrip() for l in p.stdout.splitlines()]
            want = [l.rstrip() for l in (HERE / "reproduce/outputs" / f"out_{s}.txt").read_text().splitlines()]
            bad = [i + 1 for i, (a, b) in enumerate(zip(got, want)) if a != b]
            extra = len(got) != len(want)
            allowed = set(bad) <= KNOWN.get(s, set()) and not extra and p.returncode == 0
            print(f"{s}: {len(want)} lines, differing {bad or 'none'}{' (length differs)' if extra else ''}"
                  f"{' (known machine-precision line)' if bad and allowed else ''}")
            if not allowed:
                sys.stdout.writelines(difflib.unified_diff(want, got, "recorded", "replayed", lineterm="\n"))
                print(p.stderr[-2000:])
            ok &= allowed
    print("REPLAY", "MATCH" if ok else "DIFFERS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
