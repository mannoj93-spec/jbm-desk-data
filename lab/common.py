"""Shared constants, versions, provenance and storage for the research lab.

Layers and where they live (lab-2.0; all compact JSON, no raw ticks). Everything is namespaced by
the evaluation version (lab/versioning.py) so a code or design change never mixes with, or
overwrites, earlier evidence:
  research/v2/<design>/<version>/events/YYYY-MM.jsonl    frozen decisions (every firing, features
                                                         included = the features layer), first write wins
  research/v2/<design>/<version>/outcomes/YYYY-MM.jsonl  complete outcome labels of episode heads
  research/v2/experiments/YYYY-MM.jsonl                  one compact result per design per run
  research/v2/ledger/YYYY-MM.jsonl                       every variant tried, null results included
  research/evidence/v2/<design>@<version>.json           evidence card (schema evidence_card/2)
  research/evidence/index.json                           current / superseded / legacy card index
  state/lab_registrations.json, state/lab_run_state.json registration clocks and last cutoffs
  reports/research.md, reports/skill_proposals.md
Legacy lab-1.0 outputs (research/evidence/cards, research/experiments, research/ledger,
state/lab_registered.json) are kept as recorded and never written again.
Time fields on every record are defined in lab/asof.py. Historical reconstructions say so in
`basis`.
"""
import datetime as dt
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storage import append_unique, atomic_json, canonical, digest, read_json, read_rows  # noqa: E402

LAB_VERSION = "lab-2.2-2026-09-24"
MINUTE = 60_000
H = 60 * MINUTE
DAY = 24 * H
PROCESSING_LATENCY_MS = 60_000     # ASSUMED processing time added to input availability (lab/asof.py);
                                   # an assumption about a live pipeline, never a measurement
HORIZONS_MIN = (30, 60, 240, 480)  # 30 minutes, 1 hour, 4 hours, 8 hours
BASIS_PROSPECTIVE = ("as-of replay of collected inputs: each input used only from its availability (observed_at, "
                     "never earlier); decision time = latest required input + 60 s ASSUMED processing; computed "
                     "by the 6-hourly lab, not live; frozen at the first lab run that computed it (t_persisted)")
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
