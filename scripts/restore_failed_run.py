#!/usr/bin/env python3
"""restore_failed_run - preserve the observations of a collector run whose push failed (repo 2.26).

    python scripts/restore_failed_run.py --zip <artifact.zip> --sha256 <digest> --run <run id> --artifact <id> \
        [--expires ISO] [--base .]

The collector uploads data/, state/ and registry/frozen/ as artifact collector-recovery-<run id> when its job fails.
This script verifies the archive against GitHub's recorded digest, compares every data/**/*.jsonl row with the
repository and keeps only rows whose identity is absent from it (the collector's own keys: (t, sym), or the
liquidation-order key). Rows whose identity a later run already stored are superseded and not restored: the store
keeps the first persisted observation and a restored duplicate would break that.

Restored rows go, byte-identical, to data/restored/collector-<run id>/<original path> - never into the live files -
so no research job, lab input hash, forecast, score or paper execution reads them, and cadence/health never count
the failed run (its own run record is kept there as evidence, not in data/runs). data/restored/receipts.jsonl gets
one append-only row: run, artifact, digest, the observation interval, per-file counts with row hashes, restored_at
(this clock) and the rule that restored data was not available on time. Rerunning is idempotent. state/ files in
the archive are not restored (they are the run's working state, superseded by later runs). Stdlib only.
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import time
import zipfile
from pathlib import Path

VERSION = "restore-1.0.0"


def key(rel, row):
    if rel.startswith("data/liq/orders/"):
        return (row.get("t"), row.get("posSide"), row.get("side"), row.get("sz_contracts"), row.get("bkPx"))
    return (row.get("t"), row.get("sym"))


def rows(text):
    return [l for l in text.splitlines() if l.strip()]


def plan(archive: zipfile.ZipFile, base: Path) -> dict:
    """{rel: {"restore": [lines], "superseded": n, "present": n}} for every data/**/*.jsonl in the archive."""
    out = {}
    for name in sorted(archive.namelist()):
        if not (name.startswith("data/") and name.endswith(".jsonl")) or name.startswith("data/restored/"):
            continue
        lines = rows(archive.read(name).decode())
        live = base / name
        have = rows(live.read_text()) if live.exists() else []
        have_set = set(have)
        have_keys = {key(name, json.loads(l)) for l in have}
        entry = {"restore": [], "superseded": 0, "present": 0}
        for l in lines:
            if l in have_set:
                entry["present"] += 1
            elif key(name, json.loads(l)) in have_keys:
                entry["superseded"] += 1
            else:
                entry["restore"].append(l)
        if entry["restore"] or entry["superseded"]:
            out[name] = entry
    return out


def apply(base: Path, run_id: str, artifact: str, digest: str, expires, p: dict, now_ms=None) -> dict:
    base = Path(base)
    root = base / "data/restored" / f"collector-{run_id}"
    files, times = [], []
    for rel, e in sorted(p.items()):
        if not e["restore"]:
            files.append({"path": rel, "restored": 0, "superseded": e["superseded"]})
            continue
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        have = set(rows(dest.read_text())) if dest.exists() else set()
        new = [l for l in e["restore"] if l not in have]
        if new:
            with open(dest, "a") as f:
                f.write("".join(l + "\n" for l in new))
        times += [json.loads(l).get("t") for l in e["restore"] if isinstance(json.loads(l).get("t"), int)]
        files.append({"path": rel, "restored": len(e["restore"]), "superseded": e["superseded"],
                      "rows_sha256": [hashlib.sha256(l.encode()).hexdigest() for l in e["restore"]],
                      "kept_at": str(dest.relative_to(base))})
    now_ms = now_ms if now_ms is not None else int(time.time() * 1000)
    receipt = {"run_id": run_id, "artifact_id": artifact, "artifact_sha256": digest, "artifact_expires": expires,
               "observed_from_ms": min(times) if times else None, "observed_to_ms": max(times) if times else None,
               "restored_at_ms": now_ms, "tool": VERSION, "files": files,
               "rule": "restored after the fact: not available on time, not in the live files, not read by any "
                       "forecast, score, paper execution or lab input; the run stays a persistence failure"}
    receipts = base / "data/restored/receipts.jsonl"
    receipts.parent.mkdir(parents=True, exist_ok=True)
    have = [json.loads(l) for l in rows(receipts.read_text())] if receipts.exists() else []
    if not any(r.get("run_id") == run_id and r.get("artifact_sha256") == digest for r in have):
        with open(receipts, "a") as f:
            f.write(json.dumps(receipt, sort_keys=True) + "\n")
    return receipt


def main(argv):
    a = {k: argv[argv.index(k) + 1] for k in ("--zip", "--sha256", "--run", "--artifact", "--expires", "--base") if k in argv}
    if not all(k in a for k in ("--zip", "--sha256", "--run", "--artifact")):
        print(__doc__)
        return 2
    blob = Path(a["--zip"]).read_bytes()
    got = hashlib.sha256(blob).hexdigest()
    want = a["--sha256"].removeprefix("sha256:")
    if got != want:
        print(f"refused: archive sha256 {got} != recorded {want}", file=sys.stderr)
        return 1
    base = Path(a.get("--base", "."))
    p = plan(zipfile.ZipFile(io.BytesIO(blob)), base)
    r = apply(base, a["--run"], a["--artifact"], want, a.get("--expires"), p)
    print(json.dumps({f["path"]: {k: f[k] for k in ("restored", "superseded")} for f in r["files"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
