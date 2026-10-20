"""Append-only search ledger (search-ledger-1.1.0, repo 2.30; 1.0.0 was repo 2.29, brief section 12).

Every research action - a hypothesis, a data query, a run (including failures, nulls, errors and aborts), a result
viewed, a registration, a rejection or retirement, a model/prompt/tool configuration, a diagnostic view of protected
outcomes - is one entry with a stable id, linked to its parent and to the previous entry by hash. The ledger records
selection decisions, not hidden model reasoning.

Entry fields: id, prev_sha256, t_utc, request_id, experiment, actor {kind: model|human|system, id, version}, action,
parent, details {...}, objects {name: sha256}, version, sha256.

1.1.0 (Oct 19 2026 review, F6):
  - Integrity is checked before every read and append; a torn final line from a crash is moved aside (kept, never
    deleted) and the repair is itself an entry.
  - Suffix truncation. A hash chain alone cannot show that its last entries were deleted: 1.0.0 verified a
    truncated ledger as intact and its search counts fell. An Anchor (count + head hash, written by a process outside
    the researcher's writable boundary - research_tools/evaluator_service.py, or a main-branch commit) makes a
    truncation or rewrite detectable. Without an anchor, verify_report() says "internally consistent (unanchored)",
    never "deletion-proof".
  - Recoverable records. Specifications, artifacts, configurations, prompts and errors referenced by an entry are kept
    whole in a content-addressed ObjectStore (objects/<sha256>.json), so a failed or rejected candidate stays
    reproducible, not just a hash.
  - Concurrency. Appends hold an exclusive file lock; request ids are checked under the lock (preflight idempotency:
    the same request id with the same payload returns the existing entry; with a different payload it is refused
    before anything is written).
A new session, model or file name does not start a new history: the family carries the count.
"""
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "search-ledger-1.1.0"
ACTIONS = ("hypothesis", "query", "inspect", "run", "run-error", "run-aborted", "view-result", "register",
           "reject", "continue", "select", "retire", "disclosure", "evaluate", "note", "config", "exposure",
           "ablation", "counterexamples", "repair", "anchor")
ACTOR_KINDS = ("model", "human", "system")
SEARCH_ACTIONS = ("run", "run-error", "run-aborted", "ablation", "counterexamples", "reject", "config", "exposure")


class LedgerCorrupt(Exception):
    """The ledger's chain or its anchor does not verify; nothing is appended to it."""


class ObjectStore:
    """Content-addressed, write-once JSON objects. put() returns the sha256 of the canonical bytes; an existing object
    is re-verified, never trusted by its name."""

    def __init__(self, root):
        self.root = Path(root)

    def put(self, obj) -> str:
        try:
            data = E.canon(obj).encode()
        except (TypeError, ValueError):                       # NaN, infinities, non-JSON values: keep them as text
            data = E.canon({"non_canonical_json": json.dumps(obj, sort_keys=True, allow_nan=True, default=repr)}).encode()
        sha = hashlib.sha256(data).hexdigest()
        p = self.root / f"{sha}.json"
        if p.exists():
            if hashlib.sha256(p.read_bytes()).hexdigest() != sha:
                raise LedgerCorrupt(f"object {sha} on disk does not match its name")
            return sha
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_bytes(data)
        os.replace(tmp, p)
        return sha

    def get(self, sha):
        p = self.root / f"{sha}.json"
        if not p.exists():
            raise LedgerCorrupt(f"object {sha} missing")
        data = p.read_bytes()
        if hashlib.sha256(data).hexdigest() != sha:
            raise LedgerCorrupt(f"object {sha} altered")
        return E.loads_strict(data.decode())

    def has(self, sha):
        return (self.root / f"{sha}.json").exists()


class FileAnchor:
    """Append-only anchor records {count, head_sha256, t_utc, by}. Trustworthy only when written by a process the
    researcher cannot impersonate and kept where the researcher cannot write (the evaluator service's directory, or
    a main-branch commit). In a single-user checkout it is a convention, and verify_report says so."""

    def __init__(self, path, writer="evaluator"):
        self.path, self.writer = Path(path), writer

    def records(self):
        if not self.path.exists():
            return []
        return [E.loads_strict(x) for x in self.path.read_text().splitlines() if x.strip()]

    def read(self):
        r = self.records()
        return r[-1] if r else None

    def write(self, count, head, t_utc):
        last = self.read()
        if last and count < last["count"]:
            raise LedgerCorrupt(f"anchor count would fall from {last['count']} to {count}")
        rec = {"count": count, "head_sha256": head, "t_utc": E.iso(t_utc), "by": self.writer}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(E.canon(rec) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return rec


class Ledger:
    def __init__(self, path, anchor=None, objects=None):
        self.path = Path(path)
        self.anchor = anchor
        self.objects = objects or ObjectStore(self.path.parent / "objects")

    # ------------------------------------------------------------------------------------------------ reading
    def _lines(self):
        if not self.path.exists():
            return []
        return self.path.read_bytes().split(b"\n")

    def entries(self):
        out = []
        for i, line in enumerate(self._lines()):
            if not line.strip():
                continue
            try:
                out.append(E.loads_strict(line.decode("utf-8")))
            except (ValueError, UnicodeDecodeError) as exc:
                raise LedgerCorrupt(f"line {i + 1} unreadable ({exc}); run repair()") from exc
        return out

    def verify(self):
        """[] when the chain is intact and, if anchored, consistent with the anchor; otherwise the problems."""
        try:
            es = self.entries()
        except LedgerCorrupt as exc:
            return [str(exc)]
        probs, prev = [], None
        for i, e in enumerate(es):
            body = {k: v for k, v in e.items() if k != "sha256"}
            if E.content_sha256(body) != e.get("sha256"):
                probs.append(f"entry {i} ({e.get('id')}): content does not match its hash")
            if e.get("prev_sha256") != prev:
                probs.append(f"entry {i} ({e.get('id')}): chain broken (prev {e.get('prev_sha256')!r}, expected {prev!r})")
            prev = e.get("sha256")
        a = self.anchor.read() if self.anchor else None
        if a:
            if len(es) < a["count"]:
                probs.append(f"ledger has {len(es)} entries; the anchor ({a['t_utc']}, by {a['by']}) recorded "
                             f"{a['count']}: entries were deleted (suffix truncation)")
            elif es[a["count"] - 1]["sha256"] != a["head_sha256"]:
                probs.append(f"entry {a['count'] - 1} differs from the anchored head: history was rewritten")
        return probs

    def verify_report(self):
        probs = self.verify()
        a = self.anchor.read() if self.anchor else None
        return {"version": VERSION, "problems": probs, "entries": len(self.entries()) if not probs or a else None,
                "anchored": a is not None,
                "claim": ("anchored: truncation or rewrite before the anchor is detectable" if a else
                          "internally consistent (unanchored: deletion of a suffix is not detectable)")
                if not probs else "failed"}

    # ------------------------------------------------------------------------------------------------ writing
    @contextlib.contextmanager
    def _locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path.with_suffix(self.path.suffix + ".lock"), "a+") as lf:
            fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lf.fileno(), fcntl.LOCK_UN)

    def repair(self, t_utc, actor=None):
        """Move a torn final line aside (kept as <ledger>.torn-<sha12>) and record the repair. Only a torn LAST line
        is repaired; damage elsewhere is reported, not rewritten."""
        with self._locked():
            lines = self._lines()
            body = [x for x in lines if x.strip()]
            if not body:
                return None
            try:
                E.loads_strict(body[-1].decode("utf-8"))
                return None
            except (ValueError, UnicodeDecodeError):
                pass
            torn = body[-1]
            keep = body[:-1]
            for x in keep:
                E.loads_strict(x.decode("utf-8"))                             # anything else broken: refuse
            side = self.path.with_name(self.path.name + f".torn-{hashlib.sha256(torn).hexdigest()[:12]}")
            side.write_bytes(torn)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_bytes(b"".join(x + b"\n" for x in keep))
            os.replace(tmp, self.path)
        return self.append("-", actor or {"kind": "system", "id": "ledger-repair"}, "repair",
                           {"torn_line_kept_at": side.name, "bytes": len(torn)}, f"repair-{side.name}", t_utc)

    def append(self, experiment, actor, action, details, request_id, t_utc, parent=None, objects=None):
        if action not in ACTIONS:
            raise ValueError(f"action {action!r}")
        if not isinstance(actor, dict) or actor.get("kind") not in ACTOR_KINDS or not actor.get("id"):
            raise ValueError("actor needs kind (model|human|system) and id")
        if not request_id:
            raise ValueError("request_id is required (idempotency)")
        refs = {}
        for name, obj in (objects or {}).items():
            refs[name] = self.objects.put(obj)
        payload = {"experiment": experiment, "actor": actor, "action": action, "details": details, "parent": parent}
        if refs:
            payload["objects"] = refs
        with self._locked():
            probs = self.verify()
            if probs:
                raise LedgerCorrupt("; ".join(probs[:3]))
            es = self.entries()
            for e in es:
                if e["request_id"] == request_id:
                    if E.content_sha256({k: e.get(k) for k in payload}) == E.content_sha256(payload):
                        return e                                         # a repeat: traceable, not duplicated
                    raise ValueError(f"request_id {request_id} already used with a different payload")
            prev = es[-1]["sha256"] if es else None
            body = dict(payload, id=f"S{len(es) + 1:06d}", prev_sha256=prev, t_utc=E.iso(t_utc),
                        request_id=request_id, version=VERSION)
            e = dict(body, sha256=E.content_sha256(body))
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(E.canon(e) + "\n")
                f.flush()
                os.fsync(f.fileno())
            return e

    def find(self, request_id):
        for e in self.entries():
            if e["request_id"] == request_id:
                return e
        return None

    def preflight(self, request_id, payload):
        """'new' | 'repeat' | 'conflict' for a request id and payload, before anything is written."""
        e = self.find(request_id)
        if e is None:
            return "new"
        same = E.content_sha256({k: e.get(k) for k in payload}) == E.content_sha256(payload)
        return "repeat" if same else "conflict"

    def anchor_now(self, t_utc):
        if self.anchor is None:
            raise ValueError("no anchor configured")
        probs = self.verify()
        if probs:
            raise LedgerCorrupt("; ".join(probs[:3]))
        es = self.entries()
        return self.anchor.write(len(es), es[-1]["sha256"] if es else None, t_utc)

    def family_count(self, family):
        """Distinct registered candidates and every search action in a family, across every session and model."""
        regs, runs, search = set(), 0, {}
        for e in self.entries():
            if (e.get("details") or {}).get("family") != family:
                continue
            if e["action"] == "register":
                regs.add(e["details"].get("candidate_sha256"))
            if e["action"] in ("run", "run-error", "run-aborted"):
                runs += 1
            if e["action"] in SEARCH_ACTIONS:
                search[e["action"]] = search.get(e["action"], 0) + 1
        return {"family": family, "registered_candidates": len(regs), "runs_including_failures": runs,
                "search_actions": search, "search_total": sum(search.values()) + len(regs)}
