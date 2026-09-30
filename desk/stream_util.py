#!/usr/bin/env python3
"""stream_util — shared plumbing for the prospective research streams added in repo 2.20 (repo-only).

Used by companion_job.py (RC1D companion B1 forecasts) and paper_ps1.py (paper sizing experiment PS1). Neither
stream writes to registry/, state/forecast_manifest.json or any file the range stream, the scorer, the monitor or
the research lab reads: their records live under streams/ and their reports under reports/.

  clock_ms()                    wall clock in ms (injectable in tests)
  run_meta()                    GitHub run identity, trigger and the run's actual start delay
  remote_sha(path)              sha256 of a file on origin/main after `git fetch` (publication confirmation)
  rc1d_record(base, fid)        a registered RC1D forecast, verified: manifest entry, frozen bytes, publication row
  rc1d_bundle(base, doc)        its retained input bundle, verified against its content hash
Stdlib only.
"""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

VERSION = "stream-util-1.0.0"
DESK = Path(__file__).resolve().parent
BASE = DESK.parent
for p in (str(DESK), str(BASE)):
    if p not in sys.path:
        sys.path.insert(0, p)

UTC = dt.timezone.utc


def clock_ms() -> int:
    return int(time.time() * 1000)


def iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_ms(ms: int) -> str:
    t = dt.datetime.fromtimestamp(ms / 1000, tz=UTC)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"


def parse(s: str) -> dt.datetime:
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ" if "." in s else "%Y-%m-%dT%H:%M:%SZ"
    return dt.datetime.strptime(s, fmt).replace(tzinfo=UTC)


def ms(t: dt.datetime) -> int:
    return int(t.timestamp() * 1000)


def boundary(now: dt.datetime) -> dt.datetime:
    """The last 4H close at or before `now`."""
    return now.replace(minute=0, second=0, microsecond=0) - dt.timedelta(hours=now.hour % 4)


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(obj) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def file_sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(path) -> list:
    from storage import read_rows
    return read_rows(path)


def append(path, row, key) -> int:
    """Append-only, idempotent on `key(row)` (first write wins; a retry never duplicates a record)."""
    from storage import append_unique
    return append_unique(path, [row], key)


def run_meta(env=None, now_ms=None) -> dict:
    """Who ran this and how late. GitHub's scheduled and workflow_run triggers can start minutes late; the
    delay is recorded, never assumed away. `scheduled_for_ms` is the nominal cron instant when known."""
    env = os.environ if env is None else env
    now_ms = clock_ms() if now_ms is None else now_ms
    production = (env.get("GITHUB_ACTIONS") == "true" and env.get("GITHUB_REPOSITORY") == "mannoj93-spec/jbm-desk-data"
                  and env.get("GITHUB_REF") == "refs/heads/main")
    return {"event": env.get("GITHUB_EVENT_NAME", "local"), "run_id": env.get("GITHUB_RUN_ID"),
            "code_commit": env.get("GITHUB_SHA", "local"), "production": production, "started_ms": now_ms,
            "triggering_run": env.get("TRIGGERING_RUN_ID") or None}


def remote_sha(path: str, branch: str = "main", runner=subprocess.run) -> tuple:
    """(commit, sha256 of the file's bytes on origin/<branch>) after a fetch; (commit, None) if absent there."""
    runner(["git", "fetch", "--quiet", "origin", branch], check=True, timeout=60)
    commit = runner(["git", "rev-parse", f"origin/{branch}"], check=True, capture_output=True, text=True).stdout.strip()
    got = runner(["git", "show", f"origin/{branch}:{path}"], capture_output=True)
    if got.returncode != 0:
        return commit, None
    return commit, hashlib.sha256(got.stdout).hexdigest()


def remote_rows(path: str, branch: str = "main", runner=subprocess.run) -> tuple:
    """(commit, rows of a JSONL file on origin/<branch>) after a fetch."""
    runner(["git", "fetch", "--quiet", "origin", branch], check=True, timeout=60)
    commit = runner(["git", "rev-parse", f"origin/{branch}"], check=True, capture_output=True, text=True).stdout.strip()
    got = runner(["git", "show", f"origin/{branch}:{path}"], capture_output=True)
    if got.returncode != 0:
        return commit, []
    return commit, [json.loads(x) for x in got.stdout.decode().splitlines() if x.strip()]


class RecordUnavailable(ValueError):
    """The referenced RC1D record or its bundle cannot be verified."""


def rc1d_record(base, fid: str) -> tuple:
    """(frozen document, manifest entry, first publication row or None) for a registered RC1D forecast,
    verified: the frozen bytes hash to the manifest entry. Raises RecordUnavailable otherwise."""
    from storage import read_json
    base = Path(base)
    manifest = read_json(base / "state/forecast_manifest.json", {}) or {}
    entry = manifest.get(fid)
    if not isinstance(entry, dict) or not isinstance(entry.get("frozen"), str):
        raise RecordUnavailable(f"{fid}: not in the forecast manifest")
    raw = (base / entry["frozen"]).read_bytes() if (base / entry["frozen"]).exists() else None
    if raw is None or hashlib.sha256(raw).hexdigest() != entry.get("sha256"):
        raise RecordUnavailable(f"{fid}: frozen bytes missing or do not match the manifest hash")
    doc = json.loads(raw)
    pub = None
    for r in rows(base / "state/range_publications.jsonl"):
        if r.get("attempt") == entry.get("attempt"):
            pub = r
            break
    return doc, entry, pub


def rc1d_bundle(base, doc: dict) -> dict:
    """The RC1D input bundle a forecast names (desk/inputs/YYYY-MM/<sha>.json.gz), hash-verified."""
    bsha = doc.get("input_bundle")
    d = parse(doc["decision_utc"])
    path = Path(base) / "desk/inputs" / f"{d:%Y-%m}" / f"{bsha}.json.gz"
    if not path.exists():
        raise RecordUnavailable(f"input bundle {str(bsha)[:12]} missing")
    raw = gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest() != bsha:
        raise RecordUnavailable(f"input bundle {str(bsha)[:12]} altered")
    return json.loads(raw)
