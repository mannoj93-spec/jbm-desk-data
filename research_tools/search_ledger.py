"""Append-only search ledger (search-ledger-1.0.0, repo 2.29; brief section 12).

Every research action - a hypothesis, a data query, a run (including failures, nulls, errors and aborts), a result
viewed, a registration, a rejection or retirement - is one entry with a stable id, linked to its parent and to the
previous entry by hash (a hash chain: an edited or deleted entry breaks verification). The ledger records selection
decisions, not hidden model reasoning: prompts and outputs are referenced by sha256 and a storage label; private
content stays out of the public repository.

Entry fields: id, prev_sha256, t_utc, request_id, experiment, actor {kind: model|human|system, id, version},
action, parent, details {...}, sha256.
  actor.version for a model is the pinned identifier when one exists; an alias that can change is recorded as such
  (lab/model_provenance.py).
Idempotency: the same request_id with the same payload returns the existing entry; the same request_id with a
different payload is refused (a silent replacement would rewrite history).
A new session, model or file name does not start a new history: the experiment id and its family carry the count.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "search-ledger-1.0.0"
ACTIONS = ("hypothesis", "query", "inspect", "run", "run-error", "run-aborted", "view-result", "register",
           "reject", "continue", "select", "retire", "disclosure", "evaluate", "note")
ACTOR_KINDS = ("model", "human", "system")


class Ledger:
    def __init__(self, path):
        self.path = Path(path)

    def entries(self):
        if not self.path.exists():
            return []
        return [E.loads_strict(x) for x in self.path.read_text(encoding="utf-8").splitlines() if x.strip()]

    def verify(self):
        """[] when the chain is intact; otherwise the problems (edited, reordered, deleted entries)."""
        probs, prev = [], None
        for i, e in enumerate(self.entries()):
            body = {k: v for k, v in e.items() if k != "sha256"}
            if E.content_sha256(body) != e.get("sha256"):
                probs.append(f"entry {i} ({e.get('id')}): content does not match its hash")
            if e.get("prev_sha256") != prev:
                probs.append(f"entry {i} ({e.get('id')}): chain broken (prev {e.get('prev_sha256')!r}, expected {prev!r})")
            prev = e.get("sha256")
        return probs

    def append(self, experiment, actor, action, details, request_id, t_utc, parent=None):
        if action not in ACTIONS:
            raise ValueError(f"action {action!r}")
        if not isinstance(actor, dict) or actor.get("kind") not in ACTOR_KINDS or not actor.get("id"):
            raise ValueError("actor needs kind (model|human|system) and id")
        if not request_id:
            raise ValueError("request_id is required (idempotency)")
        es = self.entries()
        payload = {"experiment": experiment, "actor": actor, "action": action, "details": details, "parent": parent}
        for e in es:
            if e["request_id"] == request_id:
                if E.content_sha256({k: e[k] for k in payload}) == E.content_sha256(payload):
                    return e                                         # a repeat: traceable, not duplicated
                raise ValueError(f"request_id {request_id} already used with a different payload")
        prev = es[-1]["sha256"] if es else None
        body = dict(payload, id=f"S{len(es) + 1:06d}", prev_sha256=prev, t_utc=E.iso(t_utc), request_id=request_id,
                    version=VERSION)
        e = dict(body, sha256=E.content_sha256(body))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(E.canon(e) + "\n")
        return e

    def family_count(self, family):
        """Distinct registered candidates and distinct runs in a family, across every session and model."""
        regs, runs = set(), 0
        for e in self.entries():
            if (e.get("details") or {}).get("family") != family:
                continue
            if e["action"] == "register":
                regs.add(e["details"].get("candidate_sha256"))
            if e["action"] in ("run", "run-error", "run-aborted"):
                runs += 1
        return {"family": family, "registered_candidates": len(regs), "runs_including_failures": runs}
