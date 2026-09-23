"""Shared constants, versions, provenance and storage for the research lab.

Layers and where they live (all compact JSON; no raw ticks):
  research/events/<design>/YYYY-MM.jsonl    detector firings of the primary variant, each with its
                                            feature record (the features layer), episode id and
                                            input hash; scheduled controls are recomputed, not stored
  research/outcomes/<design>/YYYY-MM.jsonl  mature outcome labels (only complete ones are stored)
  research/experiments/YYYY-MM.jsonl        one compact result per design run (append-only history)
  research/ledger/variants.jsonl            every tested variant, including null results
  research/evidence/cards/<design>.json     machine-readable evidence card (latest)
  reports/research.md, reports/skill_proposals.md
Every record carries the lab code hash, a detector/design version, and the three times that must
never be confused: t_event (what the record describes), t_first_observed (when the first required
input was written by the collector) and t_available (when every required input had arrived plus
processing latency). Historical reconstructions say so in `basis`.
"""
import datetime as dt
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storage import append_unique, atomic_json, canonical, digest, read_json, read_rows  # noqa: E402

LAB_VERSION = "lab-1.0-2026-09-23"
MINUTE = 60_000
H = 60 * MINUTE
DAY = 24 * H
PROCESSING_LATENCY_MS = 60_000     # live processing assumed to finish within 1 minute of the last input
HORIZONS_MIN = (30, 60, 240, 480)  # 30 minutes, 1 hour, 4 hours, 8 hours
BASIS_PROSPECTIVE = "prospective: inputs as written by the collector (observed_at); processing latency added"
BASIS_RECONSTRUCTION = ("historical reconstruction: public history fetched later; availability assumed at "
                        "t_event + processing latency, which the live pipeline did not achieve")


def code_hash():
    """Identity of the lab code: sha256 over every lab/*.py and lab/modules/*.py file."""
    h = hashlib.sha256()
    here = Path(__file__).resolve().parent
    for path in sorted(list(here.glob("*.py")) + list(here.glob("modules/*.py"))):
        h.update(path.relative_to(here).as_posix().encode() + b"\0" + path.read_bytes() + b"\0")
    return h.hexdigest()


def month(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m")


def iso(ms):
    if ms is None:
        return None
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def ceil_minute(ms):
    return -(-ms // MINUTE) * MINUTE


def append(base, rel_dir, rows, key):
    """Idempotent monthly append (first observation wins); returns rows added."""
    by = {}
    for r in rows:
        by.setdefault(month(r["t_event"] if "t_event" in r else r["t"]), []).append(r)
    return sum(append_unique(Path(base) / rel_dir / f"{m}.jsonl", rs, key) for m, rs in by.items())


def read_dir(base, rel_dir):
    out = []
    for p in sorted((Path(base) / rel_dir).glob("*.jsonl")):
        out.extend(read_rows(p))
    return out


def hash_inputs(items):
    """Hash of the exact input values a feature used (canonical JSON)."""
    return digest(items)


__all__ = ["ROOT", "LAB_VERSION", "MINUTE", "H", "DAY", "PROCESSING_LATENCY_MS", "HORIZONS_MIN",
           "BASIS_PROSPECTIVE", "BASIS_RECONSTRUCTION", "code_hash", "month", "iso", "ceil_minute", "append",
           "read_dir", "hash_inputs", "atomic_json", "canonical", "digest", "read_json", "read_rows"]
