#!/usr/bin/env python3
"""preserve_research_artifact - keep the outputs of a research-lab run whose persist job never ran (repo 2.27).

    python scripts/preserve_research_artifact.py --zip <artifact.zip> --sha256 <digest> --run <run id> \
        --artifact <id> --created ISO --expires ISO [--base .]

On 2026-10-05 research run 37359675540 computed (job 111930818862, success) and uploaded artifact
research-37359675540, but its persist job (111932497914) never received a runner. This tool:
  1. verifies the archive against GitHub's recorded digest (refuses on mismatch);
  2. copies the archive byte-identically to data/restored/research-<run>/artifact.zip;
  3. runs the existing publication gate (scripts/merge_research.py: conflict, publication and evidence checks) on a
     temporary copy of the checkout - a DRY RUN, nothing in research/, reports/ or state/ is written - and records
     its exit code and what it would have added;
  4. appends one receipt to data/restored/receipts.jsonl.
It never publishes into the live research files. The lab freezes a decision at "the first lab run that computed
it" and records that run's data cutoff as t_persisted; merging these outputs now would place records stamped with
the 18:58 cutoff into the live store about two hours later, i.e. claim an on-time freeze that the repository did not
hold. The next lab run recomputes them from the collected inputs and freezes them at its own cutoff. GitHub's
artifact creation time (server-recorded) and the digest are kept as evidence that the computation happened then.
Stdlib only.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

VERSION = "preserve-research-1.0.0"
ROOT = Path(__file__).resolve().parents[1]


def main(argv):
    def arg(k, default=None):
        return argv[argv.index(k) + 1] if k in argv else default
    zpath, want, run, art = Path(arg("--zip")), arg("--sha256", "").removeprefix("sha256:"), arg("--run"), arg("--artifact")
    base = Path(arg("--base", str(ROOT)))
    raw = zpath.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != want:
        print(f"refused: archive sha256 {got} != recorded {want}", file=sys.stderr)
        return 3
    dest = base / f"data/restored/research-{run}"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "artifact.zip").write_bytes(raw)
    with zipfile.ZipFile(zpath) as z:
        names = sorted(z.namelist())
        summary = json.loads(z.read("lab-summary.json")) if "lab-summary.json" in names else None
        with tempfile.TemporaryDirectory() as tmp:
            inc, repo = Path(tmp) / "incoming", Path(tmp) / "repo"
            z.extractall(inc)
            files = subprocess.run(["git", "ls-files"], cwd=base, capture_output=True, text=True).stdout.split()
            for f in files:
                if f.startswith(("research/", "reports/", "state/lab_", "lab/", "scripts/", "research.py")) or "/" not in f:
                    (repo / f).parent.mkdir(parents=True, exist_ok=True)
                    if (base / f).is_file():
                        shutil.copy2(base / f, repo / f)
            for d in ("lab", "scripts"):
                if (base / d).is_dir() and not (repo / d).exists():
                    shutil.copytree(base / d, repo / d)
            r = subprocess.run([sys.executable, str(repo / "scripts/merge_research.py"), str(inc), str(repo)],
                               capture_output=True, text=True, cwd=repo)
            would = [l for l in r.stdout.splitlines() if ": +" in l and not l.split(": +")[1].startswith("0 ")]
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=base, capture_output=True, text=True).stdout.strip()
    receipt = {"tool": VERSION, "kind": "research", "run_id": str(run), "artifact_id": str(art),
               "artifact_sha256": got, "artifact_created": arg("--created"), "artifact_expires": arg("--expires"),
               "kept_at": f"data/restored/research-{run}/artifact.zip", "files": len(names),
               "lab_summary": None if summary is None else {"schema": summary.get("schema"), "t": summary.get("t"),
                                                            "cutoff_ms": summary.get("cutoff_ms"),
                                                            "commit": summary.get("commit"),
                                                            "code_sha256": summary.get("code_sha256")},
               "gate_dry_run": {"checkout": commit, "exit": r.returncode, "would_add": would,
                                "stderr": r.stderr.strip()[-400:]},
               "published": False,
               "restored_at_ms": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
               "rule": "preserved, not published: merging would stamp records with the run's 18:58Z freeze cutoff "
                       "although the repository did not hold them until later; the next lab run recomputes and "
                       "freezes them at its own cutoff. Never read by any forecast, score, paper execution or lab input."}
    with open(base / "data/restored/receipts.jsonl", "a") as f:
        f.write(json.dumps(receipt, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
