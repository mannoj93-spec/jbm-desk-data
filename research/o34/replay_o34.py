"""Offline replay of O34 v1 (package 12.4.16). Runs the frozen runner (run_o34.py, unchanged) on retained inputs
and compares every result field with results_v1.json. No network.

  python3 studies/o34/replay_o34.py --raw <dir>     exact provider bytes: the 38 monthly zip files and their
                                                    .CHECKSUM files; each is hash-checked against inputs_v1.json,
                                                    then loaded through jbm_archive's own validation
  python3 studies/o34/replay_o34.py --rows <file>   the normalized rows the run used (hash-checked)
The inputs are in the separate O34 evidence bundle (the skill installer rejects nested archives). Run from the
package root. Exit 0 = every variant, period and field reproduced.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
ROWS_SHA256 = "63f0c6eaba0aebcd81c91c4c9bf78dec7464ee4db842e00ad274345bd99f1ac6"
RECORDED_ENV = {"python": "3.13.16", "numpy": "2.5.3", "note": "the v1 run (Oct 12 13:30:54Z) and this replay's "
                "first execution used the same container; v1's results file did not record versions"}


def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check_raw(raw_dir) -> list[str]:
    spec = json.loads((HERE / "inputs_v1.json").read_text())
    probs = []
    for f in spec["files"]:
        base = os.path.basename(f["url"])
        p, ck = Path(raw_dir) / base, Path(raw_dir) / (base + ".CHECKSUM")
        if not p.exists() or not ck.exists():
            probs.append(f"{base}: missing")
            continue
        if _sha(p) != f["sha256"]:
            probs.append(f"{base}: bytes differ from the recorded sha256")
        if ck.read_text().split()[0].lower() != f["provider_sha256"]:
            probs.append(f"{base}: provider checksum file differs")
    return probs


def replay(raw_dir=None, rows_file=None) -> dict:
    import numpy as np
    import run_o34 as R
    if raw_dir:
        probs = check_raw(raw_dir)
        if probs:
            raise SystemExit("input verification failed: " + "; ".join(probs[:5]))
        import jbm_archive as A

        def local(url):
            p = Path(raw_dir) / os.path.basename(url)
            if not p.exists():
                raise FileNotFoundError(url)
            return p.read_bytes(), {}
        A._default_opener = local
        res = R.run(None)
    else:
        if _sha(rows_file) != ROWS_SHA256:
            raise SystemExit("rows file sha256 differs from the record")
        with tempfile.TemporaryDirectory() as d:
            cache = os.path.join(d, "rows.json")
            with open(rows_file, "rb") as src, open(cache, "wb") as dst:
                dst.write(src.read())
            res = R.run(cache)
    want = json.loads((HERE / "results_v1.json").read_text())
    diffs = []
    for v, per in want["variants"].items():
        for p, fields in per.items():
            for k, x in fields.items():
                y = res["variants"][v][p].get(k)
                if x != y:
                    diffs.append(f"{v}/{p}/{k}: recorded {x!r}, replay {y!r}")
    if res["primary"] != want["primary"]:
        diffs.append(f"primary: {res['primary']} vs {want['primary']}")
    if res["data"]["bars"] != want["data"]["bars"]:
        diffs.append(f"bars {res['data']['bars']} vs {want['data']['bars']}")
    return {"mode": "raw" if raw_dir else "rows", "differences": diffs, "bars": res["data"]["bars"],
            "environment": {"python": platform.python_version(), "numpy": np.__version__},
            "recorded_environment": RECORDED_ENV, "protocol_sha256": res["protocol_sha256"],
            "runner_sha256": res["runner_sha256"]}


if __name__ == "__main__":
    args = sys.argv[1:]
    raw = args[args.index("--raw") + 1] if "--raw" in args else None
    rows = args[args.index("--rows") + 1] if "--rows" in args else None
    if not (raw or rows):
        raise SystemExit(__doc__)
    out = replay(raw, rows)
    print(json.dumps(out, indent=1))
    sys.exit(1 if out["differences"] else 0)
