"""Controlled, model-independent research interface (research-api-1.0.0, repo 2.29; brief sections 12-13).

Ordinary versioned operations any model, script or person can call; scientific definitions are not bound to a vendor
or a prompt. Two roles:

  researcher  open_experiment, panel (discovery partition only), inspect, run (discovery only, with a recorded
              budget), register, results (only what the disclosure policy releases)
  evaluator   evaluate (confirmation partition: rows whose decision time is at or after the candidate's
              registration, labels matured), writes immutable result records

Partitions. An experiment fixes discovery_cutoff when it is opened. Discovery = panel rows with T < discovery_cutoff
and labels available before it. Confirmation = rows with T >= the candidate's registration time - outcomes that did
not exist when the candidate was frozen. The strongest protection is that temporal fact, not the role check.

Enforcement boundary, stated plainly. The role check and the partition filters are enforced in this API and its
tests: no researcher operation returns a confirmation row, label or unreleased result, and alternate operations
(inspect, run with partition='confirmation', results before a checkpoint) are refused. This module does NOT sandbox
the filesystem: a researcher process with the repository checked out can read data/ directly. Reading data past the
discovery cutoff outside the API is exposure and must be logged (ledger action 'query' with the dates); it does not
reset the experiment's history. Results the evaluator writes are hash-chained; an edited record fails verification.

Candidate specification (executable, model-independent):
  {"family", "features": [...], "rule": {"type": "linear-score", "weights": {f: w}, "bias": b,
   "long_above": x, "short_below": y}, "horizon_min", "transform": <panel.fit_transform artifact or null>}
Actions are long (+1), short (-1) or abstain (0); the conversion is part of the frozen spec, so explanation quality
cannot change the trading policy. Other rule types run through register(..., code_path=...) with the module's sha256
recorded; this version executes linear-score only.

Model modes (section 13): mode 'research-assistant' (historical discovery; results are discovery evidence; a
candidate must be frozen and evaluated on later outcomes) or 'live-forecaster' (research_tools/directional.py). A model's
knowledge of historical outcomes through training is a leakage risk no as-of packet removes: every run records the
model identity and its known/unknown training cutoff, and historical results are labelled 'discovery (possible
training-data exposure)' unless the rows post-date the model's documented cutoff - a provider claim recorded as a
claim, never proof.
"""
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402
from research_tools.search_ledger import Ledger  # noqa: E402

VERSION = "research-api-1.0.0"
ROLES = ("researcher", "evaluator")
MODES = ("research-assistant", "live-forecaster")


class Refused(Exception):
    """An operation outside the caller's role or partition."""


def _ms(x):
    return int(E.instant(x).timestamp() * 1000)


class ResearchAPI:
    def __init__(self, root, provider, role, actor, clock):
        """root: folder for experiments, candidates, results and the ledger (research/search/ in the repository).
        provider(cutoff_ms) -> {"rows": panel rows (research_tools/panel.py), "labels": {h: [label rows]}} using only data
        available at cutoff. actor: {kind, id, version, training_cutoff (optional, a claim)}. clock: () -> now (UTC)."""
        if role not in ROLES:
            raise ValueError(role)
        self.root, self.provider, self.role, self.actor, self.clock = Path(root), provider, role, actor, clock
        self.ledger = Ledger(self.root / "ledger.jsonl")

    # ------------------------------------------------------------------------------------------------ helpers
    def _need(self, role):
        if self.role != role:
            raise Refused(f"{role} operation called by the {self.role} role")

    def _exp(self, exp_id):
        p = self.root / "experiments" / f"{exp_id}.json"
        if not p.exists():
            raise Refused(f"no experiment {exp_id}")
        return E.loads_strict(p.read_text())

    def _log(self, exp, action, details, request_id, parent=None):
        return self.ledger.append(exp, self.actor, action, details, request_id, self.clock(), parent)

    def _exposure_label(self, rows):
        tc = self.actor.get("training_cutoff")
        first = min((r["t"] for r in rows), default=None)
        if tc is None:
            return "discovery (model training cutoff unknown: possible training-data exposure)"
        if first is not None and first > _ms(tc):
            return f"discovery (rows after the model's stated training cutoff {tc}; a provider claim, not proof)"
        return f"discovery (rows before the model's stated training cutoff {tc}: possible training-data exposure)"

    # ------------------------------------------------------------------------------------------- researcher
    def open_experiment(self, exp_id, family, discovery_cutoff, disclosure, request_id, mode="research-assistant"):
        """disclosure: {"checkpoints_n": [n1, n2, ...] - results released only at these confirmation counts,
        "metrics": [...]} fixed before any confirmation outcome exists."""
        self._need("researcher")
        if mode not in MODES:
            raise ValueError(mode)
        p = self.root / "experiments" / f"{exp_id}.json"
        rec = {"schema": "research-experiment/1", "id": exp_id, "family": family, "mode": mode,
               "discovery_cutoff_utc": E.iso(discovery_cutoff), "opened_utc": E.iso(self.clock()),
               "disclosure": disclosure, "api_version": VERSION}
        if E.instant(discovery_cutoff) > E.instant(self.clock()):
            raise Refused("discovery cutoff in the future")
        if p.exists():
            old = E.loads_strict(p.read_text())
            if {k: old[k] for k in ("family", "mode", "discovery_cutoff_utc", "disclosure")} != \
                    {k: rec[k] for k in ("family", "mode", "discovery_cutoff_utc", "disclosure")}:
                raise Refused(f"experiment {exp_id} exists with another definition; open a new experiment id")
            return old
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(E.canon(rec))
        self._log(exp_id, "hypothesis", {"family": family, "mode": mode, "discovery_cutoff_utc": rec["discovery_cutoff_utc"],
                                         "disclosure": disclosure}, request_id)
        return rec

    def panel(self, exp_id, cutoff, request_id):
        """Discovery rows and labels known before min(cutoff, discovery cutoff). A later cutoff is refused."""
        self._need("researcher")
        exp = self._exp(exp_id)
        dc = _ms(exp["discovery_cutoff_utc"])
        c = _ms(cutoff)
        if c > dc:
            self._log(exp_id, "query", {"family": exp["family"], "refused": "cutoff after discovery cutoff",
                                        "cutoff_utc": E.iso(cutoff)}, request_id)
            raise Refused(f"cutoff {E.iso(cutoff)} is after the discovery cutoff {exp['discovery_cutoff_utc']}")
        data = self.provider(c)
        rows = [r for r in data["rows"] if r["t"] < c]
        labels = {h: [x for x in xs if x["label_available"] is not None and x["label_available"] < c
                      and x["t"] < c] for h, xs in data.get("labels", {}).items()}
        self._log(exp_id, "query", {"family": exp["family"], "cutoff_utc": E.iso(cutoff), "rows": len(rows),
                                    "dates_exposed": [E.iso(E.epoch_ms(min(r["t"] for r in rows))) if rows else None,
                                                      E.iso(E.epoch_ms(max(r["t"] for r in rows))) if rows else None],
                                    "exposure": self._exposure_label(rows)}, request_id)
        return {"rows": rows, "labels": labels, "partition": "discovery", "exposure": self._exposure_label(rows)}

    def inspect(self, exp_id, cutoff, request_id):
        """Coverage, provenance and exclusion reasons on the discovery partition (no labels)."""
        self._need("researcher")
        d = self.panel(exp_id, cutoff, request_id + ":panel")
        cov = {}
        for r in d["rows"]:
            for fam, st in r["state"].items():
                cov.setdefault(fam, {}).setdefault(st.split(":")[0], 0)
                cov[fam][st.split(":")[0]] += 1
        self._log(exp_id, "inspect", {"family": self._exp(exp_id)["family"], "coverage": cov}, request_id)
        return {"coverage": cov, "rows": len(d["rows"])}

    def run(self, exp_id, spec, cutoff, budget, request_id, partition="discovery"):
        """Execute a candidate on the discovery partition. budget: {"max_rows": n} recorded with the run. Failures
        are recorded as run-error and re-raised; nothing is dropped from history."""
        self._need("researcher")
        exp = self._exp(exp_id)
        if partition != "discovery":
            self._log(exp_id, "run-aborted", {"family": exp["family"], "refused": f"partition {partition!r}"}, request_id)
            raise Refused("researchers run on the discovery partition only")
        d = self.panel(exp_id, cutoff, request_id + ":panel")
        rows = d["rows"][-int(budget.get("max_rows", len(d["rows"]))):]
        try:
            res = score(spec, rows, d["labels"].get(spec["horizon_min"], []))
        except Exception as exc:
            self._log(exp_id, "run-error", {"family": exp["family"], "spec_sha256": E.content_sha256(spec),
                                            "error": f"{type(exc).__name__}: {exc}"[:300], "budget": budget}, request_id)
            raise
        self._log(exp_id, "run", {"family": exp["family"], "spec_sha256": E.content_sha256(spec), "budget": budget,
                                  "result": res, "exposure": d["exposure"]}, request_id)
        return dict(res, partition="discovery", exposure=d["exposure"])

    def register(self, exp_id, spec, request_id, code_path=None):
        """Freeze an executable candidate: spec hash, code hashes (this API, the panel, any code_path), the
        transform artifact, the actor and the registration time. Confirmation starts at this time."""
        self._need("researcher")
        exp = self._exp(exp_id)
        import hashlib
        code = {}
        for p in [Path(__file__), Path(__file__).with_name("panel.py")] + ([Path(code_path)] if code_path else []):
            code[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
        cand = {"schema": "research-candidate/1", "experiment": exp_id, "family": exp["family"], "spec": spec,
                "candidate_sha256": E.content_sha256(spec), "code_sha256": code, "actor": self.actor,
                "registered_utc": E.iso(self.clock()), "confirmation_starts_utc": E.iso(self.clock()),
                "api_version": VERSION}
        p = self.root / "candidates" / f"{exp_id}-{cand['candidate_sha256'][:12]}.json"
        if p.exists():
            return E.loads_strict(p.read_text())
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(E.canon(cand))
        self._log(exp_id, "register", {"family": exp["family"], "candidate_sha256": cand["candidate_sha256"],
                                       "confirmation_starts_utc": cand["confirmation_starts_utc"]}, request_id)
        return cand

    def results(self, exp_id, candidate_sha256, request_id):
        """Only results the disclosure policy releases: evaluator records at the declared checkpoint counts."""
        self._need("researcher")
        out = [r for r in _read_results(self.root, exp_id, candidate_sha256) if r.get("released")]
        self._log(exp_id, "view-result", {"family": self._exp(exp_id)["family"], "candidate_sha256": candidate_sha256,
                                          "released_records": [r["sha256"] for r in out]}, request_id)
        return out

    # -------------------------------------------------------------------------------------------- evaluator
    def evaluate(self, exp_id, candidate_sha256, request_id):
        """Score the frozen candidate on confirmation rows (T >= registration) whose labels matured by now. A record
        is released only when the count reaches a declared checkpoint; others are kept unreleased."""
        self._need("evaluator")
        exp = self._exp(exp_id)
        p = self.root / "candidates" / f"{exp_id}-{candidate_sha256[:12]}.json"
        if not p.exists():
            raise Refused("unregistered candidate")
        cand = E.loads_strict(p.read_text())
        now = _ms(self.clock())
        start = _ms(cand["confirmation_starts_utc"])
        data = self.provider(now)
        rows = [r for r in data["rows"] if start <= r["t"] < now]
        labels = [x for x in data.get("labels", {}).get(cand["spec"]["horizon_min"], [])
                  if x["label_available"] is not None and x["label_available"] <= now and x["t"] >= start]
        res = score(cand["spec"], rows, labels)
        n = res["scored"]
        cps = exp["disclosure"].get("checkpoints_n", [])
        released_at = max((c for c in cps if n >= c), default=None)
        prior = _read_results(self.root, exp_id, candidate_sha256)
        already = {r["checkpoint_n"] for r in prior if r.get("released")}
        rec = {"schema": "research-result/1", "experiment": exp_id, "candidate_sha256": candidate_sha256,
               "evaluated_utc": E.iso(self.clock()), "partition": "confirmation",
               "confirmation_window": [cand["confirmation_starts_utc"], E.iso(self.clock())],
               "checkpoint_n": released_at, "released": released_at is not None and released_at not in already,
               "result": res if (released_at is not None and released_at not in already) else {"scored": n},
               "evidence_class": "prospective confirmation (outcomes after registration)"}
        _append_result(self.root, rec)
        self._log(exp_id, "evaluate", {"family": exp["family"], "candidate_sha256": candidate_sha256, "scored": n,
                                       "released": rec["released"]}, request_id)
        return rec


# ---------------------------------------------------------------------------------------------------- scoring
def actions(spec, rows):
    """Deterministic actions from the frozen conversion: +1 long, -1 short, 0 abstain, None when a feature is
    missing (an explicit missing decision, never a zero)."""
    r = spec["rule"]
    if r.get("type") != "linear-score":
        raise ValueError(f"rule type {r.get('type')!r} is not executable in {VERSION}")
    out = {}
    for row in rows:
        xs = [row["features"].get(k) for k in spec["features"]]
        if any(x is None for x in xs):
            out[row["t"]] = None
            continue
        s = r.get("bias", 0.0) + sum(r["weights"][k] * x for k, x in zip(spec["features"], xs))
        out[row["t"]] = 1 if s > r["long_above"] else -1 if s < r["short_below"] else 0
    return out


def score(spec, rows, labels, cost_bp=None):
    """Directional utility: mean of action x forward return (bp) on taken decisions, minus a per-trade cost when given.
    The full opportunity denominator is reported: rows, missing decisions, abstentions, unlabelled."""
    acts = actions(spec, rows)
    lab = {x["t"]: x for x in labels if x.get("state") == "ok"}
    taken, missing, abstain, unlabelled = [], 0, 0, 0
    for t, a in sorted(acts.items()):
        if a is None:
            missing += 1
        elif a == 0:
            abstain += 1
        elif t not in lab:
            unlabelled += 1
        else:
            taken.append(a * lab[t]["label_bp"] - (cost_bp or 0.0))
    n = len(taken)
    m = sum(taken) / n if n else None
    sd = math.sqrt(sum((x - m) ** 2 for x in taken) / (n - 1)) if n > 1 else None
    return {"opportunities": len(acts), "missing_decision": missing, "abstain": abstain, "unlabelled": unlabelled,
            "scored": n, "mean_bp": None if m is None else round(m, 4), "sd_bp": None if sd is None else round(sd, 4),
            "cost_bp": cost_bp, "note": "overlapping horizons and common shocks: rows are not independent (calibration.py)"}


def _rpath(root, exp_id):
    return Path(root) / "results" / f"{exp_id}.jsonl"


def _read_results(root, exp_id, cand):
    p = _rpath(root, exp_id)
    if not p.exists():
        return []
    return [r for r in (E.loads_strict(x) for x in p.read_text().splitlines() if x.strip())
            if r["candidate_sha256"] == cand]


def verify_results(root, exp_id):
    p = _rpath(root, exp_id)
    probs, prev = [], None
    if not p.exists():
        return probs
    for i, r in enumerate(E.loads_strict(x) for x in p.read_text().splitlines() if x.strip()):
        body = {k: v for k, v in r.items() if k != "sha256"}
        if E.content_sha256(body) != r.get("sha256") or r.get("prev_sha256") != prev:
            probs.append(f"result {i}: altered or reordered")
        prev = r.get("sha256")
    return probs


def _append_result(root, rec):
    p = _rpath(root, rec["experiment"])
    prev = None
    if p.exists():
        lines = [x for x in p.read_text().splitlines() if x.strip()]
        prev = E.loads_strict(lines[-1])["sha256"] if lines else None
    body = dict(rec, prev_sha256=prev)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(E.canon(dict(body, sha256=E.content_sha256(body))) + "\n")


def store_provider(base, horizons=(60,), days=30):
    """The production provider: lab/data.Store at the cutoff, lab/panel.build over the last `days`."""
    from lab.data import Store
    from research_tools import panel as P
    from lab.common import DAY

    def provide(cutoff_ms):
        st = Store(base, cutoff=cutoff_ms)
        pn = P.build(st, cutoff_ms - days * DAY, cutoff_ms)
        return {"rows": pn["rows"], "labels": {h: P.labels(st, pn, h) for h in horizons}}
    return provide


# ------------------------------------------------------------------------------------------------------- CLI
def _cli(argv=None):
    """python -m research_tools.research_api --root research/search --role researcher --actor actor.json <op> --args args.json
    ops: open | panel | inspect | run | register | results | evaluate | verify. args.json holds the operation's
    keyword arguments (request_id always). Output: JSON on stdout. The provider is the repository's stored data."""
    import argparse
    import datetime as _dt
    ap = argparse.ArgumentParser(prog="research_tools.research_api")
    ap.add_argument("--root", default=str(ROOT / "research" / "search"))
    ap.add_argument("--role", choices=ROLES, required=True)
    ap.add_argument("--actor", required=True, help="JSON file: {kind, id, version, training_cutoff}")
    ap.add_argument("op", choices=("open", "panel", "inspect", "run", "register", "results", "evaluate", "verify"))
    ap.add_argument("--args", required=True, help="JSON file with the operation's arguments")
    a = ap.parse_args(argv)
    actor = json.loads(Path(a.actor).read_text())
    kw = json.loads(Path(a.args).read_text())
    api = ResearchAPI(a.root, store_provider(ROOT), a.role, actor, lambda: _dt.datetime.now(_dt.timezone.utc))
    ops = {"open": lambda: api.open_experiment(kw["experiment"], kw["family"], kw["discovery_cutoff_utc"],
                                               kw["disclosure"], kw["request_id"], kw.get("mode", "research-assistant")),
           "panel": lambda: (lambda d: {"rows": d["rows"], "labels": d["labels"], "partition": d["partition"],
                                        "exposure": d["exposure"]})(api.panel(kw["experiment"], kw["cutoff_utc"],
                                                                              kw["request_id"])),
           "inspect": lambda: api.inspect(kw["experiment"], kw["cutoff_utc"], kw["request_id"]),
           "run": lambda: api.run(kw["experiment"], kw["spec"], kw["cutoff_utc"], kw.get("budget", {}), kw["request_id"]),
           "register": lambda: api.register(kw["experiment"], kw["spec"], kw["request_id"], kw.get("code_path")),
           "results": lambda: api.results(kw["experiment"], kw["candidate_sha256"], kw["request_id"]),
           "evaluate": lambda: api.evaluate(kw["experiment"], kw["candidate_sha256"], kw["request_id"]),
           "verify": lambda: {"ledger": api.ledger.verify(), "results": verify_results(a.root, kw["experiment"])}}
    try:
        print(json.dumps(ops[a.op](), indent=1, default=str))
        return 0
    except Refused as exc:
        print(json.dumps({"refused": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(_cli())
