"""Raw-response retention and replay (archive-store-1.0.0, repo 2.29; brief section 8).

High-volume bytes stay out of Git history. Exact provider responses are written content-addressed (sha256) to an
object store - a local directory, or any S3-compatible bucket through the stream recorder's existing backend
(stream/storage.S3Backend; credentials from the environment, nothing provisioned here). Git keeps only the compact
manifest: one line per retained object linking it to the derived rows built from it.

  ArchiveStore(root, backend=None).put(raw_bytes, meta) -> manifest line
      meta: {"source", "url_or_channel", "retrieved_utc", "first_durable_utc", "parser", "parser_version"}
      (event times are NEVER used as availability; backfilled history carries provenance 'reconstructed')
  verify(manifest_lines)    every object present and re-hashing to its key
  replay(line, parser)      re-derive rows from the retained bytes and compare their hash with the manifest's
                            derived_sha256 - a hash without retained bytes is identity, not a replay archive
Retention: objects are immutable; deletion is an operator decision recorded in the manifest. Growth is reported by
growth() (bytes per day). Collector integration is opt-in (not wired into collector.py in repo 2.29): turning it on
is a deployment step with a storage budget (docs/RESEARCH_INTERFACE.md, deployment handoff).
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "archive-store-1.0.0"
META_REQUIRED = ("source", "url_or_channel", "retrieved_utc", "parser", "parser_version", "provenance")


class ArchiveStore:
    def __init__(self, root, backend=None):
        self.root, self.backend = Path(root), backend

    def key(self, sha):
        return f"objects/{sha[:2]}/{sha}"

    def put(self, raw: bytes, meta: dict, derived_rows=None):
        miss = [k for k in META_REQUIRED if not meta.get(k)]
        if miss:
            raise ValueError(f"meta missing {miss}")
        if meta["provenance"] not in ("original", "reconstructed"):
            raise ValueError("provenance is original or reconstructed")
        if E.maybe_instant(meta["retrieved_utc"]) is None:
            raise ValueError("retrieved_utc must be timezone-aware")
        sha = hashlib.sha256(raw).hexdigest()
        p = self.root / self.key(sha)
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        if self.backend is not None:
            self.backend.put(self.key(sha), raw)
        line = dict(meta, object_sha256=sha, bytes=len(raw), key=self.key(sha), version=VERSION,
                    derived_sha256=E.content_sha256(derived_rows) if derived_rows is not None else None)
        return line

    def get(self, sha):
        p = self.root / self.key(sha)
        return p.read_bytes() if p.exists() else None

    def verify(self, lines):
        probs = []
        for m in lines:
            b = self.get(m["object_sha256"])
            if b is None:
                probs.append(f"{m['object_sha256'][:12]}: object missing")
            elif hashlib.sha256(b).hexdigest() != m["object_sha256"]:
                probs.append(f"{m['object_sha256'][:12]}: bytes do not match the key")
        return probs

    def replay(self, line, parser):
        b = self.get(line["object_sha256"])
        if b is None:
            return {"state": "unavailable", "reason": "object not retained"}
        rows = parser(b)
        got = E.content_sha256(rows)
        return {"state": "ok" if got == line.get("derived_sha256") else "mismatch", "derived_sha256": got,
                "rows": rows}

    @staticmethod
    def growth(lines):
        out = {}
        for m in lines:
            d = E.iso(m["retrieved_utc"])[:10]
            out[d] = out.get(d, 0) + m["bytes"]
        return out


def parse_binance_klines(raw: bytes):
    """The collector's 1m kline batch rows from a raw Binance klines response (closed bars only are kept by the
    caller): [t, o, h, l, c, v, qv, n, tbv, tbqv]."""
    page = E.loads_strict(raw.decode())
    return [[int(k[0]), float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5]), float(k[7]), int(k[8]),
             float(k[9]), float(k[10])] for k in page]
