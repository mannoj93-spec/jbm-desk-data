"""DIR1 guarded operational runner (dir1-runner-1.0.0, repo 2.30; Oct 19 2026 review, F4).

One entry point that does every step in order and records each one durably, so no caller can skip a check:

  1. reconcile   expected opportunities come from the schedule, independently of any worker; an opportunity no arm
                 touched is 'missed' after its deadline and still counts.
  2. protocol    operational mode needs a registered protocol whose effective evidence the verifier confirms and an
                 effective time at or before the decision; fixture mode is explicit and stamps every record FIXTURE.
  3. inputs      the as-of panel row (research_tools/panel.py) for the registered instrument; every required feature
                 eligible (panel.eligible) and no older than inputs.max_input_age_s; otherwise inputs-unavailable.
  4. packet      the exact input packet is kept (content-addressed object) and its hash bound to the forecast.
  5. inference   each arm through an Adapter; every attempt runs in a child process that is killed at the protocol's
                 timeout (a real cancellation, not latency measured after a hung call returns); every attempt -
                 success, parse failure, exception, timeout - is recorded with its raw output kept as text, its cost
                 (unknown when cancelled) and the model identity; the FIRST valid parse is selected.
  6. publication the forecast record is published through a Publisher and admitted only through a Verifier that
                 confirms the durable copy's own first availability and exact bytes (admit()).
  7. grading     grade_matured() grades only admitted forecasts whose outcome was available at the evaluation cutoff.
  8. results     result records go to a hash-chained store under the runner's private root.

The log (DurableOpportunityLog) is append-only JSONL with a hash chain, validated on load (hashes, chain, every
transition replayed), written under an exclusive lock, torn-line recovery, and idempotent re-invocation: running the
same decision twice adds nothing. A restart that finds an opportunity in inference-started records the interrupted
attempt and uses the remaining attempts only if the deadline allows.

Adapters: CallableAdapter (deterministic in-repo arms), CommandAdapter (any external program; the real boundary for
a model client), HTTPJSONAdapter (a JSON-over-HTTP model endpoint). The frontier arm is NOT commissioned: no account,
model identity or transport is configured in this repository; FixtureAdapter exists for tests and marks records.
Publishers/verifiers: FixtureMain (tests), GitHubMainVerifier (main-branch first availability through the GitHub API,
mockable), RegistryReceiptVerifier (receipt + read-back).
"""
import base64
import contextlib
import fcntl
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import directional as D  # noqa: E402
from research_tools import evidence_contract as E  # noqa: E402
from research_tools import panel as P  # noqa: E402
from research_tools.search_ledger import ObjectStore  # noqa: E402

VERSION = "dir1-runner-1.0.0"
MIN = 60_000


class LogCorrupt(Exception):
    pass


class Refused(Exception):
    pass


# ------------------------------------------------------------------------------------------------- the log
class DurableOpportunityLog(D.OpportunityLog):
    def __init__(self, path):
        self.path = Path(path)
        self.recovered = []
        super().__init__(self._load())

    @contextlib.contextmanager
    def _locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(self.path) + ".lock", "a+") as lf:
            fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lf.fileno(), fcntl.LOCK_UN)

    def _load(self):
        if not self.path.exists():
            return []
        lines = [x for x in self.path.read_bytes().split(b"\n") if x.strip()]
        evs = []
        for i, x in enumerate(lines):
            try:
                evs.append(E.loads_strict(x.decode("utf-8")))
            except (ValueError, UnicodeDecodeError):
                if i != len(lines) - 1:
                    raise LogCorrupt(f"{self.path}: line {i + 1} unreadable (not the last line): not repaired")
                side = self.path.with_name(self.path.name + f".torn-{hashlib.sha256(x).hexdigest()[:12]}")
                side.write_bytes(x)
                self.path.write_bytes(b"".join(y + b"\n" for y in lines[:-1]))
                self.recovered.append(side.name)
        prev, state = None, {}
        for i, e in enumerate(evs):
            body = {k: v for k, v in e.items() if k != "sha256"}
            if E.content_sha256(body) != e.get("sha256") or e.get("prev_sha256") != prev:
                raise LogCorrupt(f"{self.path}: event {i} altered or out of order")
            cur = state.get(e["opportunity"])
            if e["state"] not in D.TRANSITIONS.get(cur, ()):
                raise LogCorrupt(f"{self.path}: event {i} transition {cur} -> {e['state']} not allowed")
            state[e["opportunity"]] = e["state"]
            prev = e["sha256"]
        return evs

    def add(self, oid, arm, state, t_utc, data=None, idempotent=False):
        with self._locked():
            self.events = self._load()                                 # another process may have appended
            hist = self.history(oid)
            if idempotent and hist and hist[-1]["state"] == state and hist[-1]["data"] == (data or {}):
                return hist[-1]
            cur = self.state(oid)
            if state not in D.TRANSITIONS.get(cur, ()):
                raise ValueError(f"{oid}: transition {cur} -> {state} not allowed")
            body = {"opportunity": oid, "arm": arm, "state": state, "t_utc": E.iso(t_utc), "data": data or {},
                    "prev_sha256": self.events[-1]["sha256"] if self.events else None, "version": VERSION}
            e = dict(body, sha256=E.content_sha256(body))
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(E.canon(e) + "\n")
                f.flush()
                os.fsync(f.fileno())
            self.events.append(e)
            return e


class ResultStore:
    """Hash-chained result records under the runner's private root (the protected evaluator side)."""

    def __init__(self, path):
        self.path = Path(path)

    def records(self):
        if not self.path.exists():
            return []
        return [E.loads_strict(x) for x in self.path.read_text().splitlines() if x.strip()]

    def append(self, rec):
        rs = self.records()
        if any(r["opportunity"] == rec["opportunity"] for r in rs):
            return next(r for r in rs if r["opportunity"] == rec["opportunity"])
        body = dict(rec, prev_sha256=rs[-1]["sha256"] if rs else None)
        out = dict(body, sha256=E.content_sha256(body))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(E.canon(out) + "\n")
        return out

    def verify(self):
        probs, prev = [], None
        for i, r in enumerate(self.records()):
            if E.content_sha256({k: v for k, v in r.items() if k != "sha256"}) != r["sha256"] or r["prev_sha256"] != prev:
                probs.append(f"result {i}: altered or reordered")
            prev = r["sha256"]
        return probs


# ---------------------------------------------------------------------------------------------- adapters
class CallableAdapter:
    """A deterministic in-repository arm: fn(features, attempt) -> (raw, cost_usd)."""
    fixture = False

    def __init__(self, name, fn, model=None):
        self.name, self.fn = name, fn
        self.model = model or {"provider": "repository", "id": name, "pinned": True, "observed_version": D.VERSION}

    def call(self, packet, attempt):
        raw, cost = self.fn(packet["features"], attempt)
        return raw, cost, self.model


class FixtureAdapter(CallableAdapter):
    """TEST-ONLY scripted responses (raw outputs, exceptions, or ('sleep', seconds) to hang). Records are fixtures."""
    fixture = True

    def __init__(self, name, responses):
        self.seq = list(responses)
        super().__init__(name, None, {"provider": "fixture", "id": name, "pinned": False, "observed_version": "fixture"})

    def call(self, packet, attempt):
        item = self.seq[attempt] if attempt < len(self.seq) else RuntimeError("no scripted response")
        if isinstance(item, tuple) and item and item[0] == "sleep":
            time.sleep(item[1])
            return {"p_up": 0.5}, 0.001, self.model
        if isinstance(item, Exception):
            raise item
        return item, 0.002, self.model


class CommandAdapter:
    """An external program is the model client: the packet JSON on stdin; stdout is either an envelope
    {"raw": ..., "cost_usd": x, "model": {...}} or the raw output itself (cost then unknown)."""
    fixture = False

    def __init__(self, name, argv, model, env=None):
        self.name, self.argv, self.model, self.env = name, list(argv), model, env

    def call(self, packet, attempt):
        p = subprocess.run(self.argv, input=json.dumps(dict(packet, attempt=attempt)).encode(), capture_output=True,
                           env=self.env)
        if p.returncode != 0:
            raise RuntimeError(f"exit {p.returncode}: {p.stderr.decode(errors='replace')[:200]}")
        out = p.stdout
        try:
            env = E.loads_strict(out.decode("utf-8"))
            if isinstance(env, dict) and "raw" in env:
                return env["raw"], env.get("cost_usd"), env.get("model") or self.model
        except (ValueError, UnicodeDecodeError):
            pass
        return out, None, self.model


class HTTPJSONAdapter:
    """A JSON-over-HTTP model endpoint (the frontier arm's transport when commissioned). The request body is the
    packet; credentials come from the named environment variable and are never recorded. The response body is the
    raw output. The deadline is enforced by the child process running this call, not by socket timeouts."""
    fixture = False

    def __init__(self, name, url, model, token_env=None):
        self.name, self.url, self.model, self.token_env = name, url, model, token_env

    def call(self, packet, attempt):
        import urllib.request
        req = urllib.request.Request(self.url, data=json.dumps(dict(packet, attempt=attempt)).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
        if self.token_env and os.environ.get(self.token_env):
            req.add_header("Authorization", f"Bearer {os.environ[self.token_env]}")
        with urllib.request.urlopen(req) as r:                       # noqa: S310 (operator-configured endpoint)
            body = r.read()
            cost = r.headers.get("X-Cost-USD")
        return body, float(cost) if cost else None, self.model


def _child(adapter, packet, attempt, conn):
    try:
        raw, cost, model = adapter.call(packet, attempt)
        if isinstance(raw, (bytes, bytearray)):
            raw = bytes(raw)
        conn.send(("ok", raw, cost, model))
    except BaseException as exc:                                       # noqa: BLE001 - every failure is recorded
        conn.send(("error", f"{type(exc).__name__}: {str(exc)[:200]}", None, None))
    finally:
        conn.close()


def infer_with_deadline(adapter, packet, protocol, clock, objects):
    """The registered attempt policy with real cancellation: each attempt runs in a forked child that is killed at
    inference.timeout_s. Returns directional._selection(...) with raw outputs kept in the object store."""
    pol = protocol["inference"]
    ctx = mp.get_context("fork")
    attempts, chosen = [], None
    for k in range(pol["max_attempts"]):
        t0, m0 = clock(), time.monotonic()
        parent, child = ctx.Pipe(duplex=False)
        proc = ctx.Process(target=_child, args=(adapter, packet, k, child), daemon=True)
        proc.start()
        child.close()
        got = parent.poll(pol["timeout_s"])
        if got:
            try:
                kind, raw, cost, model = parent.recv()
            except EOFError:
                kind, raw, cost, model = "error", "child exited without a result", None, None
        proc.join(0.5)
        if proc.is_alive():
            proc.terminate()
            proc.join(1)
            if proc.is_alive():
                proc.kill()
                proc.join(1)
        lat = round(time.monotonic() - m0, 3)
        t1 = clock()
        if not got:
            a = {"attempt": k, "start_utc": E.iso(t0), "end_utc": E.iso(t1), "latency_s": lat, "cost_usd": None,
                 "cost_state": "unknown: call cancelled at the deadline", "raw_sha256": None, "raw_object": None,
                 "parse": f"timeout (cancelled at {pol['timeout_s']} s)", "p_up": None,
                 "model": getattr(adapter, "model", None)}
        else:
            if kind == "error":
                p, why, txt = None, raw, None
            else:
                p, why = D.parse_forecast(raw)
                txt = D.raw_text(raw)
            a = {"attempt": k, "start_utc": E.iso(t0), "end_utc": E.iso(t1), "latency_s": lat, "cost_usd": cost,
                 "raw_sha256": hashlib.sha256(txt.encode()).hexdigest() if txt is not None else None,
                 "raw_object": objects.put({"raw_text": txt}) if txt is not None else None, "parse": why, "p_up": p,
                 "model": model or getattr(adapter, "model", None)}
            if cost is None:
                a["cost_state"] = "unknown: the adapter reported no cost"
        attempts.append(a)
        if a["p_up"] is not None:
            chosen = k
            break
    return D._selection(attempts, chosen)


# -------------------------------------------------------------------------------------- publication / verify
class FixtureMain:
    """TEST-ONLY stand-in for main: publish() stores the bytes and the clock time they became available (plus an
    injected delay); verify() checks the bytes and returns that time. Every admission it makes is marked fixture."""
    fixture = True
    name = "fixture-main"

    def __init__(self, clock, delay_ms=0, tamper=False, fail=False):
        self.clock, self.delay_ms, self.tamper, self.fail = clock, delay_ms, tamper, fail
        self.store = {}

    def publish(self, content):
        if self.fail:
            raise RuntimeError("publication failed (fixture)")
        body = dict(content, p_up=round(1 - content["p_up"], 6)) if self.tamper else content
        ref = hashlib.sha256(E.canon(body).encode()).hexdigest()[:40]
        t = E.epoch_ms(int(E.instant(self.clock()).timestamp() * 1000) + self.delay_ms)
        self.store[ref] = (E.canon(body).encode(), E.iso(t))
        return {"kind": "git-commit", "ref": ref, "path": f"streams/dir1/{content['opportunity']}.json",
                "content_sha256": E.content_sha256(content), "published_utc": E.iso(self.clock())}

    def verify(self, evidence, content):
        got = self.store.get((evidence or {}).get("ref"))
        if got is None:
            return False, None, "no such commit on main", None
        data, first = got
        if hashlib.sha256(data).hexdigest() != hashlib.sha256(E.canon(content).encode()).hexdigest():
            return False, None, "the published bytes differ from the forecast", None
        return True, first, "fixture main", {"ref": evidence["ref"], "first_available_utc": first}


class GitHubMainVerifier:
    """First availability on main from GitHub's own records. gh(args) -> parsed JSON (default: the gh CLI).
    Checks: the file at the commit holds exactly the forecast bytes; the commit is on main; the earliest push to main
    (repository activity API) whose new head contains the commit gives the time. The commit's author/committer
    dates are never used."""
    fixture = False
    name = "github-main-activity"

    def __init__(self, repo, gh=None):
        self.repo = repo
        self.gh = gh or (lambda args: json.loads(subprocess.run(["gh", "api", *args], capture_output=True, check=True,
                                                               text=True).stdout))

    def _contains(self, head, sha):
        c = self.gh([f"repos/{self.repo}/compare/{sha}...{head}"])
        return c.get("status") in ("identical", "ahead")

    def verify(self, evidence, content):
        sha, path = (evidence or {}).get("ref"), (evidence or {}).get("path")
        if not sha or not path:
            return False, None, "evidence needs the commit and the file path", None
        f = self.gh([f"repos/{self.repo}/contents/{path}?ref={sha}"])
        data = base64.b64decode(f.get("content", ""))
        try:
            same = E.content_sha256(E.loads_strict(data.decode())) == E.content_sha256(content)
        except (ValueError, UnicodeDecodeError):
            same = False
        if not same:
            return False, None, "the file at that commit is not this forecast", None
        if not self._contains("main", sha):
            return False, None, "the commit is not on main", None
        acts = self.gh([f"repos/{self.repo}/activity?ref=refs/heads/main&activity_type=push&per_page=100&direction=asc"])
        for a in sorted(acts, key=lambda x: x["timestamp"]):
            if a.get("after") == sha or self._contains(a["after"], sha):
                return True, E.iso(E.instant(a["timestamp"])), "first push to main containing the commit", \
                    {"activity_id": a.get("id"), "after": a.get("after"), "timestamp": a["timestamp"]}
        return False, None, "no push to main containing the commit was found", None

    def first_main(self, sha):
        if not self._contains("main", sha):
            return False, None, "the commit is not on main", None
        acts = self.gh([f"repos/{self.repo}/activity?ref=refs/heads/main&activity_type=push&per_page=100&direction=asc"])
        for a in sorted(acts, key=lambda x: x["timestamp"]):
            if a.get("after") == sha or self._contains(a["after"], sha):
                return True, E.iso(E.instant(a["timestamp"])), "first push to main containing the commit", a
        return False, None, "no push to main containing the commit was found", None

    def verify_effective(self, evidence):
        """A protocol's effective evidence {"merge_commit": sha}: effective at the first push to main containing it."""
        sha = (evidence or {}).get("merge_commit")
        return self.first_main(sha) if sha else (False, None, "effective evidence names no merge commit", None)


class RegistryReceiptVerifier:
    """A registry write: receipt naming the content hash plus a read-back equal to the content."""
    fixture = False
    name = "registry-receipt"

    def verify(self, evidence, content):
        rc, rb = (evidence or {}).get("receipt") or {}, (evidence or {}).get("readback")
        if rc.get("content_sha256") != E.content_sha256(content) or rb != content:
            return False, None, "receipt or read-back does not match the forecast", None
        t = E.maybe_instant(rc.get("receipt_utc"))
        if t is None:
            return False, None, "receipt time missing", None
        return True, E.iso(t), "registry receipt with matching read-back", rc


# ---------------------------------------------------------------------------------------------- panel source
class PanelSource:
    """The as-of panel row at a decision time from the collector's stored data (lab/data.Store)."""

    def __init__(self, base, instrument="Binance USD-M BTCUSDT perpetual"):
        self.base, self.instrument = base, instrument

    def row_at(self, decision_ms):
        from lab.data import Store
        t0 = time.monotonic()
        pn = P.build(Store(self.base, cutoff=decision_ms), decision_ms, decision_ms + 1)
        return (pn["rows"][0] if pn["rows"] else None), {"panel_version": pn["version"],
                                                          "policy_sha256": pn["policy_sha256"],
                                                          "build_s": round(time.monotonic() - t0, 3)}


class FixturePanelSource:
    def __init__(self, rows, instrument="Binance USD-M BTCUSDT perpetual"):
        self.rows, self.instrument = rows, instrument

    def row_at(self, decision_ms):
        return self.rows.get(decision_ms), {"panel_version": P.VERSION, "policy_sha256": P.policy_sha256(),
                                            "build_s": 0.0, "fixture": True}


FEATURE_SOURCES = {"flow_btc": ("perp_window",), "ret_15m_bp": ("perp_window",),
                   "depth_25bp_btc": ("perp_window", "depth"), "flow_per_depth": ("perp_window", "depth"),
                   "response_bp_per_100btc": ("perp_window",), "funding_mean_bp_8h": ("funding_estimate",),
                   "funding_dispersion_bp_8h": ("funding_estimate",), "d_oi_1h_pct": ("oi",), "ret_1h_bp": ("oi",),
                   "oi_x_ret": ("oi",), "d_oi_per_volume": ("oi",), "basis_bp": ("basis",)}


def feature_age_s(row, k):
    srcs = (row.get("inputs") or {}).get("sources") or {}
    ages = [srcs.get(s, {}).get("age_s") for s in FEATURE_SOURCES.get(k, ())]
    return None if not ages or any(a is None for a in ages) else max(ages)


# ------------------------------------------------------------------------------------------------- runner
class DIR1Runner:
    def __init__(self, protocol, root, mode, adapters, publisher, verifier, panel_source, clock, private_root=None):
        if mode not in ("fixture", "operational"):
            raise ValueError(mode)
        self.p, self.mode, self.adapters = protocol, mode, adapters
        self.publisher, self.verifier, self.panel, self.clock = publisher, verifier, panel_source, clock
        self.root = Path(root)
        self.private = Path(private_root) if private_root else self.root / "private"
        self.log = DurableOpportunityLog(self.root / "opportunities.jsonl")
        self.objects = ObjectStore(self.root / "objects")
        self.results = ResultStore(self.private / "results.jsonl")
        if mode == "operational" and any(getattr(a, "fixture", False) for a in adapters.values()):
            raise Refused("a fixture adapter cannot run in operational mode")
        if mode == "operational" and getattr(verifier, "fixture", False):
            raise Refused("a fixture verifier cannot admit operational publications")

    def _now_ms(self):
        return int(E.instant(self.clock()).timestamp() * 1000)

    def check_protocol(self, decision_ms):
        probs = D.validate_protocol(self.p)
        if probs:
            raise Refused("invalid protocol: " + "; ".join(probs))
        if self.mode == "fixture":
            return
        if self.p["status"] != "registered":
            raise Refused(f"protocol {self.p['id']} is {self.p['status']}: not effective; operational runs refused")
        ev = self.p.get("effective_evidence") or {}
        ok, first, why, _ = (self.verifier.verify_effective(ev) if hasattr(self.verifier, "verify_effective")
                             else (False, None, "verifier cannot confirm effective evidence", None))
        if not ok or E.instant(first) > E.epoch_ms(decision_ms):
            raise Refused(f"effective evidence not confirmed for this decision ({why})")

    def _tag(self, data):
        return dict(data, fixture=True) if self.mode == "fixture" else data

    def reconcile(self, start_ms, end_ms, now):
        n = int(E.instant(now).timestamp() * 1000)
        dl = self.p["publication"]["deadline_s"] * 1000
        for t in D.expected(self.p, start_ms, end_ms):
            for arm in self.p["arms"]:
                oid = D.opp_id(self.p, t, arm)
                if self.log.state(oid) is None:
                    self.log.add(oid, arm, "expected", E.epoch_ms(t), self._tag({"decision_t_utc": E.iso(E.epoch_ms(t))}))
                if self.log.state(oid) in ("expected", "inputs-ready") and n > t + dl:
                    self.log.add(oid, arm, "missed", now, {"reason": "no inference started before the publication deadline"})
        return self.accounting(start_ms, end_ms)

    def accounting(self, start_ms, end_ms):
        """Every scheduled opportunity per arm with its current state (the denominator source is the schedule)."""
        out = {}
        for arm in self.p["arms"]:
            c = {}
            for t in D.expected(self.p, start_ms, end_ms):
                s = self.log.state(D.opp_id(self.p, t, arm)) or "not-yet-reconciled"
                c[s] = c.get(s, 0) + 1
            out[arm] = c
        return out

    def run(self, decision_ms):
        """Steps 1-6 for every arm at one decision time. Idempotent: a re-run adds nothing for steps already done."""
        self.check_protocol(decision_ms)
        out = {}
        for arm in self.p["arms"]:
            out[arm] = self._run_arm(decision_ms, arm)
        return out

    def _run_arm(self, d, arm):
        oid = D.opp_id(self.p, d, arm)
        dl = d + self.p["publication"]["deadline_s"] * 1000
        if self.log.state(oid) is None:
            self.log.add(oid, arm, "expected", E.epoch_ms(d), self._tag({"decision_t_utc": E.iso(E.epoch_ms(d))}))
        st = self.log.state(oid)
        if st in D.TERMINAL or st in ("published", "publish-late", "forecast", "abstention"):
            return st
        if st == "expected":
            if self._now_ms() > dl:
                self.log.add(oid, arm, "missed", self.clock(), {"reason": "worker started after the publication deadline"})
                return "missed"
            if arm not in self.adapters:
                self.log.add(oid, arm, "inputs-unavailable", self.clock(),
                             {"reason": f"arm {arm} not commissioned (no adapter)"})
                return "inputs-unavailable"
            st = self._inputs(oid, arm, d)
            if st != "inputs-ready":
                return st
        packet_obj = self.log.history(oid)[-1]["data"].get("packet_object") if st == "inputs-ready" else None
        prior = [e for e in self.log.history(oid) if e["state"] == "inference-started"]
        if st == "inference-started":
            packet_obj = next(e["data"]["packet_object"] for e in self.log.history(oid) if e["state"] == "inputs-ready")
            interrupted = {"attempt": "interrupted", "reason": "the worker stopped during inference (restart)"}
            if self._now_ms() > dl:
                self.log.add(oid, arm, "error", self.clock(), {"attempts": [interrupted],
                                                               "reason": "interrupted; deadline passed"})
                return "error"
            used = 1
        else:
            self.log.add(oid, arm, "inference-started", self.clock(),
                         {"policy": self.p["inference"], "adapter": arm, "packet_object": packet_obj})
            used = 0
        packet = self.objects.get(packet_obj)
        proto = self.p
        if used:
            proto = dict(self.p, inference=dict(self.p["inference"], max_attempts=max(0, self.p["inference"]["max_attempts"] - used)))
        res = infer_with_deadline(self.adapters[arm], packet, proto, self.clock, self.objects) \
            if proto["inference"]["max_attempts"] else D._selection([], None)
        attempts = ([{"attempt": "interrupted", "reason": "restart"}] if used else []) + res["attempts"]
        att_obj = self.objects.put(attempts)
        summary = {"attempts_object": att_obj, "n_attempts": len(attempts), "selected_attempt": res["selected_attempt"],
                   "p_up": res["p_up"], "cost_usd": res["cost_usd"], "cost_usd_known": res["cost_usd_known"],
                   "latency_s": res["latency_s"], "models": [a.get("model") for a in res["attempts"]]}
        if res["outcome"] != "forecast":
            self.log.add(oid, arm, res["outcome"], self.clock(), self._tag(summary))
            return res["outcome"]
        self.log.add(oid, arm, "forecast", self.clock(), self._tag(summary))
        content = {"protocol": self.p["id"], "protocol_sha256": D.protocol_sha256(self.p), "opportunity": oid,
                   "arm": arm, "decision_utc": E.iso(E.epoch_ms(d)), "p_up": res["p_up"],
                   "action": D.action(self.p, res["p_up"]), "packet_object": packet_obj,
                   "attempts_object": att_obj, "selected_attempt": res["selected_attempt"]}
        try:
            evidence = self.publisher.publish(content)
        except Exception as exc:                                       # noqa: BLE001
            self.log.add(oid, arm, "publish-failed", self.clock(), {"reason": f"{type(exc).__name__}: {exc}"[:200]})
            return "publish-failed"
        adm = D.admit(self.p, d, content, evidence, self.verifier)
        st2 = {"on-time": "published", "late": "publish-late"}.get(adm["class"], "publish-failed")
        self.log.add(oid, arm, st2, self.clock(), self._tag({"admission": adm, "content_object": self.objects.put(content)}))
        return st2

    def _inputs(self, oid, arm, d):
        inst = self.p["instrument"]["target"]
        if getattr(self.panel, "instrument", None) != inst:
            self.log.add(oid, arm, "inputs-unavailable", self.clock(),
                         {"reason": f"wrong instrument: source is {getattr(self.panel, 'instrument', None)!r}, protocol needs {inst!r}"})
            return "inputs-unavailable"
        row, meta = self.panel.row_at(d)
        req = self.p["inputs"]["required"]
        why = []
        if row is None:
            why = ["no panel row at the decision time"]
        else:
            ok, why = P.eligible(row, req)
            lim = self.p["inputs"]["max_input_age_s"]
            for k in req:
                age = feature_age_s(row, k)
                if age is None and ok:
                    why.append(f"{k}: source age unknown")
                elif age is not None and age > lim:
                    why.append(f"{k}: {age} s old at the decision (limit {lim} s)")
        if why:
            self.log.add(oid, arm, "inputs-unavailable", self.clock(), self._tag({"reasons": why, "panel": meta}))
            return "inputs-unavailable"
        feats = {k: row["features"][k] for k in sorted(row["features"]) if (row.get("fstate") or {}).get(k, "ok") == "ok"}
        packet = {"schema": "dir1-packet/1", "protocol": self.p["id"], "protocol_sha256": D.protocol_sha256(self.p),
                  "decision_utc": E.iso(E.epoch_ms(d)), "instrument": inst, "features": feats,
                  "sources": (row.get("inputs") or {}).get("sources"), "panel": meta,
                  "input_age_s": max(feature_age_s(row, k) for k in req)}
        self.log.add(oid, arm, "inputs-ready", self.clock(), self._tag({"packet_object": self.objects.put(packet),
                                                                      "input_age_s": packet["input_age_s"],
                                                                      "build_s": meta.get("build_s")}))
        return "inputs-ready"

    def grade_matured(self, bars, evaluation_cutoff_ms, funding=None):
        """Grade every admitted forecast whose outcome was available at the evaluation cutoff; write results."""
        done = {"graded": 0, "ungradable": 0, "pending": 0}
        for oid in sorted({e["opportunity"] for e in self.log.events}):
            st = self.log.state(oid)
            if st not in ("published", "publish-late"):
                continue
            h = self.log.history(oid)
            pub = h[-1]["data"]
            fc = next(e for e in h if e["state"] == "forecast")["data"]
            content = self.objects.get(pub["content_object"])
            d = int(E.instant(content["decision_utc"]).timestamp() * 1000)
            g = D.grade(self.p, d, fc["p_up"], pub["admission"], bars, evaluation_cutoff_ms, funding,
                        inference_usd=fc.get("cost_usd"))
            if g["state"] == "pending":
                done["pending"] += 1
                continue
            if g["state"] == "refused":
                raise Refused(f"{oid}: {g['reason']}")
            ready = next(e for e in h if e["state"] == "inputs-ready")["data"]
            pub_ms = int(E.instant(pub["admission"]["published_utc"]).timestamp() * 1000)
            lat = {"input_age_s": ready.get("input_age_s"), "build_s": ready.get("build_s"),
                   "inference_s": fc.get("latency_s"), "publish_delay_s": (pub_ms - d) / 1000}
            if g["state"] == "graded":
                entry = int(E.instant(g["entry_utc"]).timestamp() * 1000)
                lat["quote_delay_s"] = (entry - pub_ms) / 1000
                lat["input_to_entry_s"] = (entry - d) / 1000 + (ready.get("input_age_s") or 0)
            self.log.add(oid, h[-1]["arm"], "graded" if g["state"] == "graded" else "ungradable",
                         E.epoch_ms(evaluation_cutoff_ms), {"evaluation_cutoff_utc": E.iso(E.epoch_ms(evaluation_cutoff_ms))})
            self.results.append(self._tag({"schema": "dir1-result/1", "opportunity": oid, "arm": h[-1]["arm"],
                                           "decision_utc": content["decision_utc"], "grade": g, "latency": lat,
                                           "evaluation_cutoff_utc": E.iso(E.epoch_ms(evaluation_cutoff_ms)),
                                           "runner": VERSION}))
            done[g["state"]] += 1
        return done

    def graded_by_arm(self):
        out = {a: {} for a in self.p["arms"]}
        for r in self.results.records():
            t = int(E.instant(r["decision_utc"]).timestamp() * 1000)
            out.setdefault(r["arm"], {})[t] = r["grade"]
        for e in self.log.events:
            st = self.log.state(e["opportunity"])
            if st in D.TERMINAL and st not in ("graded", "ungradable"):
                t = int(E.instant(self.log.history(e["opportunity"])[0]["data"]["decision_t_utc"]).timestamp() * 1000)
                out.setdefault(e["arm"], {}).setdefault(t, {"state": st})
        return out
