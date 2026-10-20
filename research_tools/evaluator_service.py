"""Evaluator service: the evaluator role as a separate process (evaluator-service-1.0.0, repo 2.30; F6).

research_api's role flag is a convention inside one process: any code that can read the evaluator's files can read
unreleased results. This service is the boundary the brief asks for, at the strength the host provides:

  process   the evaluator runs in its own process and answers JSON requests on a Unix socket. A researcher process
            gets released records and nothing else through it; there is no operation that returns an unreleased
            result, an observation or a confirmation label.
  files     results, observations and the ledger anchor live under the service's private root. Started as a
            separate OS user with that root mode 0700 (serve(..., mode=0o700)), a researcher running as another user
            cannot read them; the test in regression/test_rev230.py checks exactly that with a real setuid'd process
            when it runs as root, and is skipped otherwise.
  anchor    after every evaluation (and on request) the service anchors the shared search ledger's entry count and
            head hash in its private root, so a researcher who deletes or rewrites ledger entries is detected.

What it is not: on a single-user checkout, or a CI runner where every step runs as one user, the private root is
readable by everyone who can run code there - the separation is a convention, and the readiness record says so. No
workflow in this repository deploys the service; it is prepared, not commissioned.

Usage:
    python -m research_tools.evaluator_service --shared research/search --private /srv/evaluator --socket S
"""
import json
import os
from pathlib import Path
import socket
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402
from research_tools import research_api as RA  # noqa: E402
from research_tools.search_ledger import FileAnchor  # noqa: E402

VERSION = "evaluator-service-1.0.0"
OPS = ("evaluate", "released", "anchor", "ping")


class Service:
    def __init__(self, shared, private, provider, clock, actor=None):
        self.shared, self.private = Path(shared), Path(private)
        self.anchor = FileAnchor(self.private / "ledger-anchor.jsonl", writer=VERSION)
        self.api = RA.ResearchAPI(self.shared, provider, "evaluator", actor or {"kind": "system", "id": VERSION},
                                  clock, anchor=self.anchor, private_root=self.private)
        self.clock = clock

    def handle(self, req):
        op = (req or {}).get("op")
        if op not in OPS:
            return {"error": f"unknown op {op!r}"}
        try:
            if op == "ping":
                return {"version": VERSION}
            if op == "anchor":
                return {"anchor": self.api.ledger.anchor_now(self.clock())}
            if op == "released":
                recs = [r for r in RA._read_results(self.private, req["experiment"], req["candidate_sha256"])
                        if r.get("released")]
                return {"records": recs}
            out = self.api.evaluate(req["experiment"], req["candidate_sha256"], req["request_id"])
            return {"released": out["released"], "evidence_class": out["evidence_class"],
                    "status": {k: out["status"][k] for k in ("released_checkpoints", "settled_through_utc")}}
        except RA.Refused as exc:
            return {"refused": str(exc)}


def serve(service, sock_path, mode=0o700, max_requests=None):
    """Answer one JSON request per connection until max_requests (None: forever)."""
    service.private.mkdir(parents=True, exist_ok=True)
    os.chmod(service.private, mode)
    if os.path.exists(sock_path):
        os.unlink(sock_path)
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(sock_path)
    os.chmod(sock_path, 0o666)                                         # anyone may ask; only released data answers
    srv.listen(8)
    n = 0
    try:
        while max_requests is None or n < max_requests:
            conn, _ = srv.accept()
            with conn:
                buf = b""
                while not buf.endswith(b"\n"):
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    buf += chunk
                try:
                    req = json.loads(buf.decode() or "{}")
                    resp = service.handle(req)
                except ValueError as exc:
                    resp = {"error": f"bad request: {exc}"}
                conn.sendall((json.dumps(resp, default=str) + "\n").encode())
            n += 1
    finally:
        srv.close()


class Client:
    def __init__(self, sock_path, timeout=30):
        self.sock_path, self.timeout = sock_path, timeout

    def call(self, req):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect(self.sock_path)
        try:
            s.sendall((json.dumps(req) + "\n").encode())
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = s.recv(65536)
                if not chunk:
                    break
                buf += chunk
        finally:
            s.close()
        resp = json.loads(buf.decode())
        if "refused" in resp:
            raise RA.Refused(resp["refused"])
        if "error" in resp:
            raise ValueError(resp["error"])
        return resp


def _main(argv=None):
    import argparse
    import datetime as _dt
    ap = argparse.ArgumentParser(prog="research_tools.evaluator_service")
    ap.add_argument("--shared", required=True)
    ap.add_argument("--private", required=True)
    ap.add_argument("--socket", required=True)
    a = ap.parse_args(argv)
    svc = Service(a.shared, a.private, RA.store_provider(ROOT), lambda: _dt.datetime.now(_dt.timezone.utc))
    serve(svc, a.socket)
    return 0


if __name__ == "__main__":
    E.iso  # noqa: B018 (keep the contract import explicit)
    sys.exit(_main())
