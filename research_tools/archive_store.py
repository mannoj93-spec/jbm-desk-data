"""Raw-response retention and replay (archive-store-1.1.0, repo 2.30; 1.0.0 was repo 2.29, brief section 8).

High-volume bytes stay out of Git history. Exact provider responses are written content-addressed (sha256) to a local
cache and, when configured, a durable backend (stream/storage.S3Backend or any object with put/get); Git keeps only
the compact manifest linking each object to the rows derived from it.

1.1.0 (Oct 19 2026 review, F9). 1.0.0 described first_durable_utc but never required or captured it, read only local
files, trusted any file already at a hash-named path, and parsed before verifying: a whitespace change altered the raw
bytes without changing the parsed JSON, verify() failed but replay() returned ok. Now:
  - put() verifies an existing object instead of trusting its name (a wrong copy is quarantined and rewritten),
    writes with fsync and reads the bytes back, then writes to the backend and reads them back there. The line records
    the source/event time, the retrieval time and the durable-write evidence separately: first_durable_utc is the
    backend read-back time (scope 'backend'), or the local fsync time (scope 'local') without a backend; a failed or
    interrupted upload leaves state 'local-only' and no backend durability claim.
  - get() verifies size and hash; a missing or corrupt local copy is restored from the backend and re-verified.
  - replay() verifies size and hash BEFORE parsing and checks the parser identity (name, version, code sha256)
    recorded at put; raw corruption fails even when the parsed rows would be unchanged.
  - Manifest lines are immutable and hash-chained (Manifest); corrections are new lines.
  - Provenance: 'original' (captured live) or 'reconstructed' (backfilled), and a reconstructed object's historical
    availability is 'unknown' - never inferred from event times.
  - Accounting separates unique retained bytes from repeated observations; a Budget refuses writes beyond the daily or
    total limit before collector integration; retention_candidates() lists, never deletes.
Collector integration is opt-in and not wired (a deployment step with a storage budget); a mock backend is not a live
archive.
"""
import datetime as dt
import hashlib
import inspect
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "archive-store-1.1.0"
META_REQUIRED = ("source", "url_or_channel", "retrieved_utc", "parser", "parser_version", "provenance")


class ArchiveCorrupt(Exception):
    pass


class BudgetExceeded(Exception):
    pass


def parser_identity(parser):
    """(name, code sha256) of a parser function: its module's source bytes."""
    try:
        src = inspect.getsource(sys.modules[parser.__module__]).encode()
    except (OSError, TypeError, KeyError):
        src = inspect.getsource(parser).encode()
    return parser.__name__, hashlib.sha256(src).hexdigest()


class Budget:
    def __init__(self, max_bytes_per_day=None, max_total_bytes=None):
        self.day, self.total = max_bytes_per_day, max_total_bytes

    def check(self, lines, day, new_bytes, sha):
        if any(m["object_sha256"] == sha for m in lines):
            return                                                     # a repeated observation stores nothing new
        uniq = {}
        for m in lines:
            uniq.setdefault(m["object_sha256"], m)
        used_day = sum(m["bytes"] for m in uniq.values() if str(m.get("stored_utc", ""))[:10] == day)
        used = sum(m["bytes"] for m in uniq.values())
        if self.day is not None and used_day + new_bytes > self.day:
            raise BudgetExceeded(f"daily archive budget {self.day} bytes would be exceeded on {day}")
        if self.total is not None and used + new_bytes > self.total:
            raise BudgetExceeded(f"total archive budget {self.total} bytes would be exceeded")


class Manifest:
    """Append-only, hash-chained manifest lines (immutable; a correction is a new line)."""

    def __init__(self, path):
        self.path = Path(path)

    def lines(self):
        if not self.path.exists():
            return []
        return [E.loads_strict(x) for x in self.path.read_text().splitlines() if x.strip()]

    def append(self, line):
        ls = self.lines()
        body = dict(line, prev_sha256=ls[-1]["sha256"] if ls else None)
        rec = dict(body, sha256=E.content_sha256(body))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(E.canon(rec) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return rec

    def verify(self):
        probs, prev = [], None
        for i, m in enumerate(self.lines()):
            if E.content_sha256({k: v for k, v in m.items() if k != "sha256"}) != m["sha256"] or m["prev_sha256"] != prev:
                probs.append(f"manifest line {i}: altered or reordered")
            prev = m["sha256"]
        return probs


class ArchiveStore:
    def __init__(self, root, backend=None, clock=None, budget=None, backend_name=None):
        self.root, self.backend = Path(root), backend
        self.clock = clock or (lambda: dt.datetime.now(dt.timezone.utc))
        self.budget = budget
        self.backend_name = backend_name or (type(backend).__name__ if backend is not None else None)
        self.manifest = Manifest(self.root / "manifest.jsonl")

    def key(self, sha):
        return f"objects/{sha[:2]}/{sha}"

    def _write_local(self, sha, raw):
        p = self.root / self.key(sha)
        if p.exists():
            have = p.read_bytes()
            if hashlib.sha256(have).hexdigest() == sha and len(have) == len(raw):
                return "existing-verified"
            q = self.root / "quarantine" / f"{sha}.{hashlib.sha256(have).hexdigest()[:12]}"
            q.parent.mkdir(parents=True, exist_ok=True)
            os.replace(p, q)                                             # kept for inspection, never trusted
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".tmp")
        with open(tmp, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
        if hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            raise ArchiveCorrupt(f"local read-back of {sha[:12]} does not match")
        return "written"

    def put(self, raw: bytes, meta: dict, derived_rows=None, parser=None):
        miss = [k for k in META_REQUIRED if not meta.get(k)]
        if miss:
            raise ValueError(f"meta missing {miss}")
        if meta["provenance"] not in ("original", "reconstructed"):
            raise ValueError("provenance is original or reconstructed")
        if E.maybe_instant(meta["retrieved_utc"]) is None:
            raise ValueError("retrieved_utc must be timezone-aware")
        if meta.get("event_utc") is not None and E.maybe_instant(meta["event_utc"]) is None:
            raise ValueError("event_utc must be timezone-aware")
        sha = hashlib.sha256(raw).hexdigest()
        now = E.iso(self.clock())
        if self.budget is not None:
            self.budget.check(self.manifest.lines(), now[:10], len(raw), sha)
        local = self._write_local(sha, raw)
        dur = {"local": {"state": local, "fsync_readback_utc": now}}
        first_durable, scope, state = now, "local", "local-only" if self.backend is not None else "local"
        if self.backend is not None:
            try:
                self.backend.put(self.key(sha), raw)
                back = self.backend.get(self.key(sha))
                if back is None or len(back) != len(raw) or hashlib.sha256(back).hexdigest() != sha:
                    raise ArchiveCorrupt("backend read-back differs from the bytes written")
                t = E.iso(self.clock())
                dur["backend"] = {"name": self.backend_name, "readback_utc": t, "readback_sha256": sha}
                first_durable, scope, state = t, "backend", "durable"
            except Exception as exc:                                     # noqa: BLE001 - an upload failure is a state
                dur["backend"] = {"name": self.backend_name, "error": f"{type(exc).__name__}: {str(exc)[:160]}"}
        pname, pcode = parser_identity(parser) if parser is not None else (meta["parser"], None)
        line = dict(meta, object_sha256=sha, bytes=len(raw), key=self.key(sha), version=VERSION, state=state,
                    stored_utc=now, first_durable_utc=first_durable, durable_scope=scope, durability=dur,
                    parser_code_sha256=pcode, event_utc=meta.get("event_utc"),
                    historical_availability=("unknown (reconstructed)" if meta["provenance"] == "reconstructed"
                                             else "retrieved_utc"),
                    derived_sha256=E.content_sha256(derived_rows) if derived_rows is not None else None)
        if parser is not None and pname != meta["parser"]:
            raise ValueError(f"parser {pname} differs from meta.parser {meta['parser']}")
        return self.manifest.append(line)

    def get(self, sha, size=None):
        """Verified bytes, restoring from the backend when the local copy is missing or corrupt; None if neither
        verifies."""
        p = self.root / self.key(sha)
        if p.exists():
            b = p.read_bytes()
            if hashlib.sha256(b).hexdigest() == sha and (size is None or len(b) == size):
                return b
        if self.backend is None:
            return None
        try:
            b = self.backend.get(self.key(sha))
        except Exception:                                                # noqa: BLE001
            return None
        if b is None or hashlib.sha256(b).hexdigest() != sha or (size is not None and len(b) != size):
            return None
        self._write_local(sha, b)                                       # restored, re-verified
        return b

    def verify(self, lines):
        probs = []
        for m in lines:
            p = self.root / self.key(m["object_sha256"])
            if not p.exists():
                probs.append(f"{m['object_sha256'][:12]}: object missing locally")
                continue
            b = p.read_bytes()
            if len(b) != m["bytes"]:
                probs.append(f"{m['object_sha256'][:12]}: size {len(b)} != {m['bytes']}")
            elif hashlib.sha256(b).hexdigest() != m["object_sha256"]:
                probs.append(f"{m['object_sha256'][:12]}: bytes do not match the key")
        return probs

    def replay(self, line, parser):
        """Re-derive rows from verified bytes with the recorded parser identity; integrity first."""
        b = self.get(line["object_sha256"], size=line.get("bytes"))
        if b is None:
            p = self.root / self.key(line["object_sha256"])
            return {"state": "integrity-failed" if p.exists() else "unavailable",
                    "reason": "raw bytes fail their size/hash" if p.exists() else "object not retained or restorable"}
        name, code = parser_identity(parser)
        if name != line.get("parser") or (line.get("parser_code_sha256") and code != line["parser_code_sha256"]):
            return {"state": "parser-mismatch", "reason": f"recorded parser {line.get('parser')} "
                                                          f"{(line.get('parser_code_sha256') or '')[:12]}, given {name} {code[:12]}"}
        rows = parser(b)
        got = E.content_sha256(rows)
        return {"state": "ok" if got == line.get("derived_sha256") else "mismatch", "derived_sha256": got,
                "rows": rows, "provenance": line.get("provenance")}

    @staticmethod
    def accounting(lines):
        """Unique retained bytes versus repeated observations of the same bytes."""
        uniq = {}
        for m in lines:
            uniq.setdefault(m["object_sha256"], m["bytes"])
        return {"lines": len(lines), "unique_objects": len(uniq), "unique_bytes": sum(uniq.values()),
                "observed_bytes": sum(m["bytes"] for m in lines),
                "repeated_observations": len(lines) - len(uniq)}

    @staticmethod
    def growth(lines):
        out, seen = {}, set()
        for m in lines:
            if m["object_sha256"] in seen:
                continue
            seen.add(m["object_sha256"])
            d = E.iso(m.get("stored_utc") or m["retrieved_utc"])[:10]
            out[d] = out.get(d, 0) + m["bytes"]
        return out

    @staticmethod
    def retention_candidates(lines, keep_days, now):
        """Objects older than keep_days (by stored time) and durable on the backend: candidates for an OPERATOR
        decision. Nothing is deleted here."""
        cut = E.instant(now) - dt.timedelta(days=keep_days)
        return sorted({m["object_sha256"] for m in lines if m.get("state") == "durable"
                       and E.instant(m.get("stored_utc") or m["retrieved_utc"]) < cut})


def parse_binance_klines(raw: bytes):
    """The collector's 1m kline batch rows from a raw Binance klines response (closed bars only are kept by the
    caller): [t, o, h, l, c, v, qv, n, tbv, tbqv]."""
    page = E.loads_strict(raw.decode())
    return [[int(k[0]), float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5]), float(k[7]), int(k[8]),
             float(k[9]), float(k[10])] for k in page]
