#!/usr/bin/env python3
"""retained — verified access to the repository's retained inputs (crypto-desk 12.1, repo 2.16).

One loader for every consumer of retained bytes, so a changed byte stops every computation that would use it:
  load_o21_inputs(o21_dir)   the O21 root inputs (klines, DVOL), verified against research/o21/MANIFEST.json;
                             used by the O21 replay/reanalysis and as the root of the monthly refit chain.
  calendar_bytes(sha, base)  a release-calendar version by content hash: the current file, the retained
                             copy desk/calendars/<sha>.csv, or the repository's Git history - verified.
  git_blob(base, rel, sha)   any historical version of a tracked file whose sha256 is known.
Stdlib only. Raises RetainedError with the reason; never returns unverified bytes.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from pathlib import Path

VERSION = "retained-12.1.0"
DESK = Path(__file__).resolve().parent
CALENDAR_REL = "desk/releases_2020_2026.csv"
CALENDARS = "desk/calendars"


class RetainedError(ValueError):
    pass


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_o21_inputs(o21_dir) -> tuple:
    """(klines document, DVOL document), each verified against the uncompressed hash in MANIFEST.json."""
    o21 = Path(o21_dir)
    try:
        man = json.loads((o21 / "MANIFEST.json").read_text())
        files = man["files"]
    except FileNotFoundError as exc:
        raise RetainedError(f"O21 manifest missing: {exc.filename}") from exc
    except (ValueError, KeyError, TypeError) as exc:
        raise RetainedError(f"O21 manifest malformed: {exc}") from exc
    out = []
    for name in ("klines_4h.json", "dvol_1h.json"):
        key = f"inputs/{name}.gz"
        want = (files.get(key) or {}).get("sha256_uncompressed") if isinstance(files, dict) else None
        if not isinstance(want, str) or len(want) != 64:
            raise RetainedError(f"O21 manifest has no hash for {key}")
        path = o21 / key
        if not path.exists():
            raise RetainedError(f"retained input {key} missing - cannot compute without contacting providers")
        try:
            raw = gzip.decompress(path.read_bytes())
        except OSError as exc:
            raise RetainedError(f"retained input {key} is not valid gzip: {exc}") from exc
        if _sha(raw) != want:
            raise RetainedError(f"retained input {key} altered: hash mismatch")
        try:
            doc = json.loads(raw)
        except ValueError as exc:
            raise RetainedError(f"retained input {key} is not JSON: {exc}") from exc
        if not isinstance(doc, dict) or not isinstance(doc.get("rows"), list):
            raise RetainedError(f"retained input {key} has no rows")
        out.append(doc)
    return tuple(out)


def git_blob(base, rel: str, sha: str):
    """Bytes of `rel` from the first commit in `base`'s history whose version hashes to `sha`, or None."""
    base = Path(base)
    try:
        revs = subprocess.run(["git", "-C", str(base), "log", "--format=%H", "--", rel], check=True,
                              capture_output=True, text=True, timeout=60).stdout.split()
    except (OSError, subprocess.SubprocessError):
        return None
    for rev in revs:
        try:
            raw = subprocess.run(["git", "-C", str(base), "show", f"{rev}:{rel}"], check=True,
                                 capture_output=True, timeout=60).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        if _sha(raw) == sha:
            return raw
    return None


def calendar_bytes(sha: str, base, current: Path | None = None) -> tuple:
    """(bytes, where) of the calendar version with this sha256. Order: the current file, the retained copy,
    Git history. A retained copy whose content does not hash to its name is an error, not a fallback."""
    base = Path(base)
    current = Path(current) if current else base / CALENDAR_REL
    if current.exists() and _sha(current.read_bytes()) == sha:
        return current.read_bytes(), "current"
    kept = base / CALENDARS / f"{sha}.csv"
    if kept.exists():
        raw = kept.read_bytes()
        if _sha(raw) != sha:
            raise RetainedError(f"retained calendar {kept.name} altered: content hash {_sha(raw)[:12]}")
        return raw, "retained"
    raw = git_blob(base, CALENDAR_REL, sha)
    if raw is not None:
        return raw, "git history"
    raise RetainedError(f"calendar version {sha[:12]} not found (current file, {CALENDARS}/, or Git history)")


def retain_calendar(base, raw: bytes) -> Path:
    """Write desk/calendars/<sha>.csv once (content-addressed); an existing copy must match."""
    sha = _sha(raw)
    path = Path(base) / CALENDARS / f"{sha}.csv"
    if path.exists():
        if path.read_bytes() != raw:
            raise RetainedError(f"retained calendar {path.name} differs from the bytes it names")
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    tmp.replace(path)
    return path


def parse_calendar(raw: bytes) -> list:
    """Release times from calendar bytes; identical to range_model.load_calendar on the same bytes."""
    import csv
    import datetime as dt
    text = raw.decode("utf-8").splitlines(keepends=True)
    rows = csv.DictReader(line for line in text if not line.startswith("#"))
    return sorted(dt.datetime.strptime(r["release_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
                  for r in rows)
