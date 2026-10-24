"""Controlled, model-independent research interface (research-api-1.1.0, repo 2.30; 1.0.0 was repo 2.29).

Ordinary versioned operations any model, script or person can call; scientific definitions are not bound to a vendor
or a prompt. Two roles:
  researcher  open_experiment, panel (discovery partition only), inspect, run, ablate, counterexamples, config,
              register, results (only what the disclosure policy releases)
  evaluator   evaluate (confirmation partition), writes immutable result records and anchors the ledger

1.1.0 repairs (Oct 19 2026 review, F3):
  - The frozen transform is applied. 1.0.0 ignored spec.transform when computing actions and accepted malformed
    transforms. validate_spec() is strict (rule type, feature order, weights for exactly the features, finite numbers,
    ordered thresholds, horizon, transform artifact identity/version/params) and actions() standardises with the
    artifact. Unsupported rule types and code_path are refused at registration: a hash of unexecuted code proves
    nothing.
  - Registration is transactional and bound to the ledger. register() validates, preflights the request id, stores
    immutable copies of every execution artifact (spec, transform, executing code) in the ledger's ObjectStore,
    appends the register event (the commit point), then writes the candidate file as a derived copy. evaluate()
    loads the candidate from the register event and its objects, refuses an orphaned or edited candidate file,
    refuses when the executing code differs from the registered code (register a successor), and checks the
    transform's training cutoff against the experiment's discovery cutoff.
  - Prospective status needs evidence. A registration time recorded on the researcher's own disk can be edited, so a
    result is "chronological confirmation (registration locally recorded, not externally anchored)" unless the
    register event is covered by an anchor written outside the researcher's boundary (evaluator_service.py, or a
    main-branch commit); then confirmation starts at the anchor time and the class is "prospective confirmation".
  - Longitudinal data. The provider receives an explicit window start (the confirmation start) instead of a rolling
    30 days, so early confirmation observations are never dropped as the experiment ages; the evaluator also keeps a
    durable, hash-chained observation log and reports any later revision of an admitted observation instead of using
    it.
  - Horizon. Labels are requested for the candidate's registered horizon; a provider without them is refused.
  - Checkpoints. Membership is fixed in advance: checkpoint N is the first N scored confirmation decisions in
    decision-time order (ties by row hash), counting a decision only when its label matured by
    t + horizon + label_watermark_min; it is released once, when every earlier decision has passed its watermark,
    and repeated or differently timed evaluate() calls cannot change its membership or add looks. Scheduled,
    eligible, missing, abstaining, unlabelled, taken and scored counts are kept separate.

Partitions. An experiment fixes discovery_cutoff when it is opened. Discovery = rows with T < discovery_cutoff and labels
available before it. Confirmation = rows with T >= the candidate's confirmation start.

Enforcement boundary. Role and partition checks are enforced in this API. They are conventions inside one process:
a researcher process that can read the evaluator's files bypasses them. evaluator_service.py runs the evaluator as a
separate process (and, where the host provides it, a separate OS user whose directory the researcher cannot read);
only that deployment is an access-control boundary.

Model modes: 'research-assistant' (historical discovery; results are discovery evidence; every run records the model
identity and its stated training cutoff - a provider claim, never proof) or 'live-forecaster' (directional.py).
"""
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402
from research_tools.search_ledger import Ledger, LedgerCorrupt, ObjectStore  # noqa: E402

VERSION = "research-api-1.1.1"
ROLES = ("researcher", "evaluator")
MODES = ("research-assistant", "live-forecaster")
RULE_TYPES = ("linear-score",)
HORIZONS = tuple(range(15, 24 * 60 + 1, 15))
DEFAULT_WATERMARK_MIN = 60
CODE_FILES = ("research_api.py", "panel.py", "evidence_contract.py")


class Refused(Exception):
    """An operation outside the caller's role or partition, or an invalid / unverifiable object."""


def _ms(x):
    return int(E.instant(x).timestamp() * 1000)


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


# --------------------------------------------------------------------------------------------- validation
def validate_transform(art, features):
    """Problems with a panel-transform/1 artifact for these features ([] when valid)."""
    if art is None:
        return []
    if not isinstance(art, dict) or art.get("schema") != "panel-transform/1":
        return ["transform: schema must be panel-transform/1"]
    probs = []
    body = {k: v for k, v in art.items() if k != "sha256"}
    if hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() != art.get("sha256"):
        probs.append("transform: sha256 does not match its content")
    from research_tools import panel as P
    if art.get("panel_version") != P.VERSION:
        probs.append(f"transform: fitted on {art.get('panel_version')!r}, executing panel is {P.VERSION}")
    if E.maybe_instant(art.get("train_cutoff_utc")) is None:
        probs.append("transform: train_cutoff_utc missing")
    if art.get("max_train_t") is not None and art["max_train_t"] >= _ms(art.get("train_cutoff_utc") or "1970-01-01T00:00:00Z"):
        probs.append("transform: fitted on rows at or after its own training cutoff")
    params = art.get("params")
    if not isinstance(params, dict):
        return probs + ["transform: params missing"]
    for k in features:
        p = params.get(k, "absent")
        if p == "absent":
            continue                                               # untransformed feature: used raw
        if p is None:
            probs.append(f"transform: feature {k} has no fitted parameters (too few training rows)")
            continue
        if not isinstance(p, dict) or not all(_finite(p.get(x)) for x in ("lo", "hi", "mean", "sd")):
            probs.append(f"transform: feature {k} parameters not finite numbers")
            continue
        if p["sd"] <= 0 or p["lo"] > p["hi"]:
            probs.append(f"transform: feature {k} needs sd > 0 and lo <= hi")
    extra = sorted(set(params) - set(features))
    if extra:
        probs.append(f"transform: parameters for features the rule does not use {extra}")
    return probs


def validate_spec(spec):
    """Problems with a candidate specification ([] when it is executable by this version)."""
    if not isinstance(spec, dict):
        return ["spec is not an object"]
    probs = []
    allowed = {"family", "features", "rule", "horizon_min", "transform", "note"}
    if set(spec) - allowed:
        probs.append(f"unknown spec fields {sorted(set(spec) - allowed)}")
    if not isinstance(spec.get("family"), str) or not spec.get("family"):
        probs.append("family must be a non-empty string")
    fs = spec.get("features")
    if not isinstance(fs, list) or not fs or not all(isinstance(x, str) and x for x in fs) or len(set(fs)) != len(fs):
        return probs + ["features must be a non-empty list of distinct names (order is part of the spec)"]
    if spec.get("horizon_min") not in HORIZONS or isinstance(spec.get("horizon_min"), bool):
        probs.append(f"horizon_min must be a multiple of 15 minutes between 15 and 1440 (got {spec.get('horizon_min')!r})")
    r = spec.get("rule")
    if not isinstance(r, dict) or r.get("type") not in RULE_TYPES:
        return probs + [f"rule type {(r or {}).get('type') if isinstance(r, dict) else r!r} is not executable in {VERSION}"]
    if set(r) - {"type", "weights", "bias", "long_above", "short_below"}:
        probs.append(f"unknown rule fields {sorted(set(r) - {'type', 'weights', 'bias', 'long_above', 'short_below'})}")
    w = r.get("weights")
    if not isinstance(w, dict) or set(w) != set(fs):
        probs.append("rule.weights must name exactly the spec's features")
    elif not all(_finite(v) for v in w.values()):
        probs.append("rule.weights must be finite numbers")
    if not _finite(r.get("bias", 0.0)):
        probs.append("rule.bias must be a finite number")
    la, sb = r.get("long_above"), r.get("short_below")
    if not (_finite(la) and _finite(sb)) or not sb <= la:
        probs.append("rule needs finite short_below <= long_above")
    probs += validate_transform(spec.get("transform"), fs)
    return probs


def validate_statistical_artifact(art, allowed_cutoff=None):
    """Problems with a directional-statistical/1 artifact: features, coef of the same length, finite values, a parseable
    training cutoff no later than allowed_cutoff, and a matching sha256. No silent truncation."""
    if not isinstance(art, dict) or art.get("schema") != "directional-statistical/1":
        return ["statistical artifact: schema must be directional-statistical/1"]
    probs = []
    fs, co = art.get("features"), art.get("coef")
    if not isinstance(fs, list) or not fs or not all(isinstance(x, str) for x in fs) or len(set(fs)) != len(fs):
        probs.append("statistical artifact: features must be distinct names")
    if not isinstance(co, list) or not isinstance(fs, list) or len(co) != len(fs):
        probs.append("statistical artifact: coef and features differ in length")
    elif not all(_finite(c) for c in co):
        probs.append("statistical artifact: coef not finite")
    if not _finite(art.get("intercept")):
        probs.append("statistical artifact: intercept not finite")
    tc = E.maybe_instant(art.get("train_cutoff_utc"))
    if tc is None:
        probs.append("statistical artifact: train_cutoff_utc missing or without a timezone")
    elif allowed_cutoff is not None and tc > E.instant(allowed_cutoff):
        probs.append(f"statistical artifact: trained to {E.iso(tc)}, after the permitted cutoff {E.iso(allowed_cutoff)}")
    body = {k: v for k, v in art.items() if k != "sha256"}
    if E.content_sha256(body) != art.get("sha256"):
        probs.append("statistical artifact: sha256 does not match its content")
    return probs


# ---------------------------------------------------------------------------------------------------- API
class ResearchAPI:
    def __init__(self, root, provider, role, actor, clock, anchor=None, private_root=None, service=None):
        """root: experiments, candidates, results, objects and the ledger (research/search/ in the repository).
        provider(cutoff_ms, start_ms=None, horizons=(60,)) -> {"rows": panel rows, "labels": {h: [label rows]}} using
        only data available at cutoff (a 1.0.0 provider taking only cutoff is accepted for discovery). anchor: a
        search_ledger.FileAnchor written by the evaluator side (None: unanchored). private_root: where the evaluator
        keeps results and observations (default: root - a convention, not a boundary). service: an
        evaluator_service.Client; a researcher with one reads released results only through it."""
        if role not in ROLES:
            raise ValueError(role)
        self.root, self.provider, self.role, self.actor, self.clock = Path(root), provider, role, actor, clock
        self.private = Path(private_root) if private_root else self.root
        self.service = service
        self.objects = ObjectStore(self.root / "objects")
        self.ledger = Ledger(self.root / "ledger.jsonl", anchor=anchor, objects=self.objects)

    # ------------------------------------------------------------------------------------------------ helpers
    def _need(self, role):
        if self.role != role:
            raise Refused(f"{role} operation called by the {self.role} role")

    def _exp(self, exp_id):
        # The shared JSON is a convenience copy. The verified hypothesis object is
        # the frozen definition, including the disclosure policy and discovery cutoff.
        probs = self.ledger.verify()
        if probs:
            raise Refused("ledger does not verify: " + "; ".join(probs[:2]))
        events = [e for e in self.ledger.entries()
                  if e["action"] == "hypothesis" and e["experiment"] == exp_id]
        if len(events) != 1 or "experiment" not in events[0].get("objects", {}):
            raise Refused(f"no unique registered definition for experiment {exp_id}")
        try:
            frozen = self.objects.get(events[0]["objects"]["experiment"])
        except LedgerCorrupt as exc:
            raise Refused(f"experiment definition unavailable: {exc}") from exc
        p = self.root / "experiments" / f"{exp_id}.json"
        if p.exists():
            try:
                disk = E.loads_strict(p.read_text())
            except ValueError as exc:
                raise Refused("experiment file is not valid JSON") from exc
            if E.content_sha256(disk) != E.content_sha256(frozen):
                raise Refused("experiment file differs from its frozen hypothesis; open a new experiment for a change")
        return frozen

    def _log(self, exp, action, details, request_id, parent=None, objects=None):
        return self.ledger.append(exp, self.actor, action, details, request_id, self.clock(), parent, objects)

    def _provide(self, cutoff, start=None, horizons=(60,)):
        try:
            return self.provider(cutoff, start_ms=start, horizons=tuple(horizons))
        except TypeError:
            d = self.provider(cutoff)                                  # 1.0.0 provider (fixtures)
            if start is not None:
                d = dict(d, rows=[r for r in d["rows"] if r["t"] >= start])
            return d

    def _exposure_label(self, rows):
        tc = self.actor.get("training_cutoff")
        first = min((r["t"] for r in rows), default=None)
        if tc is None:
            return "discovery (model training cutoff unknown: possible training-data exposure)"
        if first is not None and first > _ms(tc):
            return f"discovery (rows after the model's stated training cutoff {tc}; a provider claim, not proof)"
        return f"discovery (rows before the model's stated training cutoff {tc}: possible training-data exposure)"

    # ------------------------------------------------------------------------------------------- researcher
    def open_experiment(self, exp_id, family, discovery_cutoff, disclosure, request_id, mode="research-assistant",
                        parent=None, mechanism=None):
        """disclosure: {"checkpoints_n": [n1, n2, ...], "metrics": [...], "label_watermark_min": W} fixed before any
        confirmation outcome exists. parent/mechanism: the hypothesis lineage (counted with its family)."""
        self._need("researcher")
        if mode not in MODES:
            raise ValueError(mode)
        cps = disclosure.get("checkpoints_n", [])
        if not isinstance(cps, list) or any(not isinstance(c, int) or isinstance(c, bool) or c <= 0 for c in cps) \
                or cps != sorted(set(cps)):
            raise Refused("disclosure.checkpoints_n must be increasing positive integers")
        p = self.root / "experiments" / f"{exp_id}.json"
        rec = {"schema": "research-experiment/1", "id": exp_id, "family": family, "mode": mode,
               "discovery_cutoff_utc": E.iso(discovery_cutoff), "opened_utc": E.iso(self.clock()),
               "disclosure": disclosure, "api_version": VERSION}
        if E.instant(discovery_cutoff) > E.instant(self.clock()):
            raise Refused("discovery cutoff in the future")
        if p.exists() or any(e["action"] == "hypothesis" and e["experiment"] == exp_id
                             for e in self.ledger.entries()):
            old = self._exp(exp_id)
            if {k: old[k] for k in ("family", "mode", "discovery_cutoff_utc", "disclosure")} != \
                    {k: rec[k] for k in ("family", "mode", "discovery_cutoff_utc", "disclosure")}:
                raise Refused(f"experiment {exp_id} exists with another definition; open a new experiment id")
            return old
        p.parent.mkdir(parents=True, exist_ok=True)
        self._log(exp_id, "hypothesis", {"family": family, "mode": mode, "discovery_cutoff_utc": rec["discovery_cutoff_utc"],
                                         "disclosure": disclosure, "parent": parent, "mechanism": mechanism},
                  request_id, objects={"experiment": rec})
        p.write_text(E.canon(rec))
        return rec

    def panel(self, exp_id, cutoff, request_id, horizons=(60,)):
        """Discovery rows and labels known before min(cutoff, discovery cutoff). A later cutoff is refused."""
        self._need("researcher")
        exp = self._exp(exp_id)
        dc = _ms(exp["discovery_cutoff_utc"])
        c = _ms(cutoff)
        if c > dc:
            self._log(exp_id, "query", {"family": exp["family"], "refused": "cutoff after discovery cutoff",
                                        "cutoff_utc": E.iso(cutoff)}, request_id)
            raise Refused(f"cutoff {E.iso(cutoff)} is after the discovery cutoff {exp['discovery_cutoff_utc']}")
        data = self._provide(c, None, horizons)
        rows = [r for r in data["rows"] if r["t"] < c]
        labels = {h: [x for x in xs if x["label_available"] is not None and x["label_available"] < c
                      and x["t"] < c] for h, xs in data.get("labels", {}).items()}
        self._log(exp_id, "query", {"family": exp["family"], "cutoff_utc": E.iso(cutoff), "rows": len(rows),
                                    "horizons": list(horizons),
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

    def _discovery_run(self, exp_id, spec, cutoff, budget, request_id, action, extra=None):
        exp = self._exp(exp_id)
        probs = validate_spec(spec)
        if probs:
            self._log(exp_id, "run-error", {"family": exp["family"], "spec_sha256": _spec_sha(spec),
                                            "error": "invalid spec: " + "; ".join(probs[:4]), "budget": budget},
                      request_id, objects={"spec": spec})
            raise ValueError("invalid spec: " + "; ".join(probs))
        if spec.get("transform") and _ms(spec["transform"]["train_cutoff_utc"]) > _ms(exp["discovery_cutoff_utc"]):
            self._log(exp_id, "run-error", {"family": exp["family"], "spec_sha256": _spec_sha(spec),
                                            "error": "transform fitted beyond the discovery cutoff"}, request_id,
                      objects={"spec": spec})
            raise Refused("transform fitted on data beyond the discovery cutoff (unauthorized training data)")
        d = self.panel(exp_id, cutoff, request_id + ":panel", horizons=(spec["horizon_min"],))
        rows = d["rows"][-int(budget.get("max_rows", len(d["rows"]))):]
        res = score(spec, rows, d["labels"].get(spec["horizon_min"], []))
        self._log(exp_id, action, dict({"family": exp["family"], "spec_sha256": _spec_sha(spec), "budget": budget,
                                        "result": res, "exposure": d["exposure"]}, **(extra or {})),
                  request_id, objects={"spec": spec})
        return dict(res, partition="discovery", exposure=d["exposure"])

    def run(self, exp_id, spec, cutoff, budget, request_id, partition="discovery"):
        """Execute a candidate on the discovery partition. Failures are recorded (with the full spec) and re-raised."""
        self._need("researcher")
        exp = self._exp(exp_id)
        if partition != "discovery":
            self._log(exp_id, "run-aborted", {"family": exp["family"], "refused": f"partition {partition!r}"}, request_id)
            raise Refused("researchers run on the discovery partition only")
        return self._discovery_run(exp_id, spec, cutoff, budget, request_id, "run")

    def ablate(self, exp_id, spec, cutoff, request_id, drop=None):
        """Feature ablations on the discovery partition: the spec with each named feature (default: each feature)
        removed. Every variant is a counted search action with its full spec retained."""
        self._need("researcher")
        out = {}
        for k in (drop or spec["features"]):
            if k not in spec["features"] or len(spec["features"]) == 1:
                continue
            v = json.loads(json.dumps(spec))
            v["features"] = [x for x in spec["features"] if x != k]
            v["rule"]["weights"] = {x: w for x, w in spec["rule"]["weights"].items() if x != k}
            if v.get("transform"):
                v["transform"] = None                                  # an ablation never reuses a fitted artifact
            out[k] = self._discovery_run(exp_id, v, cutoff, {}, f"{request_id}:drop:{k}", "ablation",
                                         {"ablated": k, "parent_spec_sha256": _spec_sha(spec)})
        return out

    def counterexamples(self, exp_id, spec, cutoff, request_id, k=10):
        """The k discovery decisions with the worst action x outcome, as failure packets (inputs, action, outcome)."""
        self._need("researcher")
        exp = self._exp(exp_id)
        d = self.panel(exp_id, cutoff, request_id + ":panel", horizons=(spec["horizon_min"],))
        acts = actions(spec, d["rows"])
        lab = {x["t"]: x for x in d["labels"].get(spec["horizon_min"], []) if x.get("state") == "ok"}
        bad = sorted((a * lab[t]["label_bp"], t) for t, a in acts.items() if a and t in lab)[:k]
        rows = {r["t"]: r for r in d["rows"]}
        packets = [{"t_utc": E.iso(E.epoch_ms(t)), "action": acts[t], "outcome_bp": lab[t]["label_bp"],
                    "features": {f: rows[t]["features"].get(f) for f in spec["features"]},
                    "inputs": rows[t].get("inputs", {})} for _, t in bad]
        self._log(exp_id, "counterexamples", {"family": exp["family"], "spec_sha256": _spec_sha(spec), "k": k,
                                              "returned": len(packets)}, request_id, objects={"spec": spec,
                                                                                               "packets": packets})
        return packets

    def config(self, exp_id, configuration, request_id):
        """Record a model / prompt / tool configuration or its revision (counted as search)."""
        self._need("researcher")
        exp = self._exp(exp_id)
        return self._log(exp_id, "config", {"family": exp["family"], "kind": configuration.get("kind"),
                                            "label": configuration.get("label")}, request_id,
                         objects={"configuration": configuration})

    def register(self, exp_id, spec, request_id, code_path=None):
        """Freeze an executable candidate (transactional; see the module docstring). Confirmation starts at the
        register event, or at the anchor covering it when the ledger is anchored."""
        self._need("researcher")
        exp = self._exp(exp_id)
        if code_path is not None:
            self._log(exp_id, "reject", {"family": exp["family"], "spec_sha256": _spec_sha(spec),
                                         "reason": "code_path is not executed by this version"}, request_id,
                      objects={"spec": spec})
            raise Refused(f"code_path is not executed by {VERSION}: a hash of code that does not run proves nothing")
        probs = validate_spec(spec)
        if not probs and spec.get("family") != exp["family"]:
            probs = [f"spec family {spec.get('family')!r} differs from the experiment's {exp['family']!r}"]
        if not probs and spec.get("transform") and _ms(spec["transform"]["train_cutoff_utc"]) > _ms(exp["discovery_cutoff_utc"]):
            probs = ["transform fitted beyond the experiment's discovery cutoff (unauthorized training data)"]
        if probs:
            self._log(exp_id, "reject", {"family": exp["family"], "spec_sha256": _spec_sha(spec),
                                         "reason": "; ".join(probs[:4])}, request_id, objects={"spec": spec})
            raise Refused("invalid candidate: " + "; ".join(probs))
        code = _code_objects()
        cand_sha = _spec_sha(spec)
        details = {"family": exp["family"], "candidate_sha256": cand_sha, "horizon_min": spec["horizon_min"],
                   "code_sha256": {k: v["sha256"] for k, v in code.items()}}
        payload = {"experiment": exp_id, "actor": self.actor, "action": "register", "details": details, "parent": None}
        pf = self.ledger.preflight(request_id, payload)
        if pf == "conflict":
            raise Refused(f"request_id {request_id} already used with a different payload; nothing written")
        objs = {"spec": spec}
        objs.update({f"code:{k}": v for k, v in code.items()})
        if spec.get("transform"):
            objs["transform"] = spec["transform"]
        ev = self._log(exp_id, "register", details, request_id, objects=objs)    # the commit point
        cand = self._candidate(exp_id, ev)
        _write_candidate(self.root, cand)
        return cand

    def _candidate(self, exp_id, ev):
        spec = self.objects.get(ev["objects"]["spec"])
        return {"schema": "research-candidate/2", "experiment": exp_id, "family": ev["details"]["family"],
                "spec": spec, "candidate_sha256": ev["details"]["candidate_sha256"],
                "code_sha256": ev["details"]["code_sha256"], "objects": ev["objects"], "actor": ev["actor"],
                "registered_utc": ev["t_utc"], "register_entry": ev["id"], "register_entry_sha256": ev["sha256"],
                "confirmation_starts_utc": ev["t_utc"], "api_version": VERSION}

    def results(self, exp_id, candidate_sha256, request_id):
        """Only results the disclosure policy releases."""
        self._need("researcher")
        if self.service is not None:
            out = self.service.call({"op": "released", "experiment": exp_id, "candidate_sha256": candidate_sha256})["records"]
        else:
            out = [r for r in _read_results(self.private, exp_id, candidate_sha256) if r.get("released")]
        self._log(exp_id, "view-result", {"family": self._exp(exp_id)["family"], "candidate_sha256": candidate_sha256,
                                          "released_records": [r["sha256"] for r in out]}, request_id)
        return out

    # -------------------------------------------------------------------------------------------- evaluator
    def load_candidate(self, exp_id, candidate_sha256):
        """The registered candidate, from its ledger event and immutable objects; refuses orphans and edits."""
        probs = self.ledger.verify()
        if probs:
            raise Refused("ledger does not verify: " + "; ".join(probs[:2]))
        evs = [e for e in self.ledger.entries() if e["action"] == "register" and e["experiment"] == exp_id
               and (e.get("details") or {}).get("candidate_sha256") == candidate_sha256]
        p = _cand_path(self.root, exp_id, candidate_sha256)
        if not evs:
            raise Refused("unregistered candidate" + (" (an orphaned candidate file has no register event)"
                                                      if p.exists() else ""))
        ev = evs[0]
        try:
            cand = self._candidate(exp_id, ev)
            for name, sha in ev["objects"].items():
                self.objects.get(sha)                                      # every artifact present and intact
        except LedgerCorrupt as exc:
            raise Refused(f"registered artifacts unavailable: {exc}") from exc
        if _spec_sha(cand["spec"]) != candidate_sha256:
            raise Refused("registered spec does not hash to the candidate id")
        if p.exists():
            disk = E.loads_strict(p.read_text())
            if E.content_sha256(disk) != E.content_sha256(cand):
                raise Refused("the candidate file differs from its registration (edited after registration); the "
                              "registered objects are the candidate - register a successor for a change")
        else:
            _write_candidate(self.root, cand)                                  # crash after the commit point
        now_code = {k: v["sha256"] for k, v in _code_objects().items()}
        if now_code != cand["code_sha256"]:
            diff = sorted(k for k in now_code if now_code[k] != cand["code_sha256"].get(k))
            raise Refused(f"executing code differs from the registered code ({diff}); register a successor")
        a = self.ledger.anchor.read() if self.ledger.anchor else None
        idx = int(ev["id"][1:])
        if a and a["count"] >= idx and self.ledger.entries()[idx - 1]["sha256"] == ev["sha256"]:
            first = next(r for r in self.ledger.anchor.records() if r["count"] >= idx)
            cand["anchored_utc"] = first["t_utc"]
            cand["confirmation_starts_utc"] = max(cand["registered_utc"], first["t_utc"], key=E.instant)
            cand["evidence_class"] = "prospective confirmation (registration anchored outside the researcher boundary)"
        else:
            cand["evidence_class"] = ("chronological confirmation (registration locally recorded, not externally "
                                      "anchored: not protected prospective evidence)")
        return cand

    def evaluate(self, exp_id, candidate_sha256, request_id):
        """Score the frozen candidate on confirmation decisions whose labels matured, releasing each declared
        checkpoint once with fixed membership."""
        self._need("evaluator")
        exp = self._exp(exp_id)
        cand = self.load_candidate(exp_id, candidate_sha256)
        spec = cand["spec"]
        h = spec["horizon_min"]
        wm = int(exp["disclosure"].get("label_watermark_min", DEFAULT_WATERMARK_MIN)) * 60_000
        now = _ms(self.clock())
        start = _ms(cand["confirmation_starts_utc"])
        data = self._provide(now, start, (h,))
        if h not in data.get("labels", {}):
            raise Refused(f"the provider supplied no labels for the candidate's horizon ({h} min)")
        rows = sorted((r for r in data["rows"] if start <= r["t"] < now), key=lambda r: (r["t"], _row_sha(r)))
        labels = {x["t"]: x for x in data["labels"][h]
                  if x["label_available"] is not None and x["label_available"] <= now and x["t"] >= start}
        obs = ObservationLog(self.private, exp_id, candidate_sha256)
        revisions, pending = obs.admit(rows, labels, spec, h, wm, now)
        cohort = obs.cohort(pending, rows)
        cps = exp["disclosure"].get("checkpoints_n", [])
        prior = _read_results(self.private, exp_id, candidate_sha256)
        done = {r["checkpoint_n"] for r in prior if r.get("released")}
        released = []
        for n in cps:
            if n in done:
                continue
            members = cohort["scored"][:n]
            if len(members) < n or members[-1]["t"] > cohort["settled_through"]:
                break                                                  # not yet determinable: no look
            last_t = members[-1]["t"]
            window = [o for o in cohort["all"] if o["t"] <= last_t]
            res = _summarize(window, members, spec)
            rec = {"schema": "research-result/2", "experiment": exp_id, "candidate_sha256": candidate_sha256,
                   "evaluated_utc": E.iso(self.clock()), "partition": "confirmation",
                   "confirmation_window": [cand["confirmation_starts_utc"], E.iso(E.epoch_ms(last_t))],
                   "checkpoint_n": n, "released": True, "membership_rule": "first N scored decisions by decision "
                   f"time; a label counts if available by t + {h} min + {wm // 60000} min",
                   "members_sha256": E.content_sha256([o["t"] for o in members]),
                   "result": res, "evidence_class": cand["evidence_class"], "api_version": VERSION}
            _append_result(self.private, rec)
            released.append(rec)
            done.add(n)
        status = {"scheduled": len(cohort["all"]), "scored_so_far": len(cohort["scored"]),
                  "settled_through_utc": E.iso(E.epoch_ms(cohort["settled_through"])) if cohort["settled_through"] else None,
                  "released_checkpoints": sorted(done), "revisions": revisions}
        self._log(exp_id, "evaluate", {"family": exp["family"], "candidate_sha256": candidate_sha256,
                                       "released_now": [r["checkpoint_n"] for r in released],
                                       "revisions_detected": len(revisions)}, request_id)
        if self.ledger.anchor is not None:
            self.ledger.anchor_now(self.clock())
        return {"released": released, "status": status, "evidence_class": cand["evidence_class"]}


# ---------------------------------------------------------------------------------------------------- scoring
def _spec_sha(spec):
    try:
        return E.content_sha256(spec)
    except (TypeError, ValueError):
        return hashlib.sha256(json.dumps(spec, sort_keys=True, default=repr).encode()).hexdigest()


def _row_sha(r):
    return hashlib.sha256(E.canon({"t": r["t"], "features": r.get("features")}).encode()).hexdigest()


def _transformed(spec, row):
    """The feature vector the frozen spec acts on: transformed with the artifact where it has parameters; None when a
    feature is unavailable (state not ok) - never zero."""
    from research_tools import panel as P
    ok, _ = P.eligible(row, spec["features"])
    if not ok:
        return None
    art = spec.get("transform")
    xs = []
    for k in spec["features"]:
        x = row["features"][k]
        p = (art or {}).get("params", {}).get(k, "absent") if art else "absent"
        if p == "absent":
            xs.append(x)
        elif p is None:
            return None
        else:
            xs.append((min(max(x, p["lo"]), p["hi"]) - p["mean"]) / p["sd"])
    return xs


def actions(spec, rows):
    """Deterministic actions from the frozen conversion: +1 long, -1 short, 0 abstain, None when a feature is
    missing or ineligible (an explicit missing decision, never a zero)."""
    probs = validate_spec(spec)
    if probs:
        raise ValueError("invalid spec: " + "; ".join(probs))
    r = spec["rule"]
    out = {}
    for row in rows:
        xs = _transformed(spec, row)
        if xs is None:
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


def _summarize(window, members, spec):
    vals = [o["value_bp"] for o in members]
    n = len(vals)
    m = sum(vals) / n if n else None
    sd = math.sqrt(sum((x - m) ** 2 for x in vals) / (n - 1)) if n > 1 else None
    c = {}
    for o in window:
        c[o["kind"]] = c.get(o["kind"], 0) + 1
    return {"scheduled": len(window), "eligible": len(window) - c.get("missing", 0), "missing_decision": c.get("missing", 0),
            "abstain": c.get("abstain", 0), "unlabelled": c.get("unlabelled", 0),
            "taken": c.get("scored", 0) + c.get("unlabelled", 0), "scored": n,
            "mean_bp": None if m is None else round(m, 4), "sd_bp": None if sd is None else round(sd, 4),
            "note": "overlapping horizons and common shocks: decisions are not independent (calibration.py)"}


class ObservationLog:
    """The evaluator's durable, hash-chained record of confirmation decisions as first admitted. A later rebuild that
    differs is reported as a revision and never replaces the admitted observation."""

    def __init__(self, root, exp_id, cand):
        self.path = Path(root) / "observations" / exp_id / f"{cand[:16]}.jsonl"

    def records(self):
        if not self.path.exists():
            return []
        return [E.loads_strict(x) for x in self.path.read_text().splitlines() if x.strip()]

    def admit(self, rows, labels, spec, h, wm, now):
        have = {o["t"]: o for o in self.records()}
        acts = actions(spec, rows)
        new, revisions, pending = [], [], []
        for r in rows:
            t = r["t"]
            a = acts.get(t)
            lab = labels.get(t)
            deadline = t + h * 60_000 + wm
            if a is None:
                kind, val = "missing", None
            elif a == 0:
                kind, val = "abstain", None
            elif lab is not None and lab.get("state") == "ok" and lab["label_available"] <= deadline:
                kind, val = "scored", a * lab["label_bp"]
            elif now > deadline:
                kind, val = "unlabelled", None
            else:
                if t not in have:
                    pending.append(t)                                  # label may still arrive in time: not admitted
                continue
            o = {"t": t, "kind": kind, "action": a, "value_bp": val, "row_sha256": _row_sha(r),
                 "label_available": lab["label_available"] if lab else None}
            if t in have:
                if {k: have[t][k] for k in ("kind", "action", "value_bp", "row_sha256")} != \
                        {k: o[k] for k in ("kind", "action", "value_bp", "row_sha256")}:
                    revisions.append({"t_utc": E.iso(E.epoch_ms(t)), "admitted": have[t]["kind"], "rebuilt": kind})
                continue
            new.append(o)
        if new:
            prev = (self.records() or [{"sha256": None}])[-1]["sha256"]
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                for o in sorted(new, key=lambda x: x["t"]):
                    body = dict(o, prev_sha256=prev)
                    rec = dict(body, sha256=E.content_sha256(body))
                    f.write(E.canon(rec) + "\n")
                    prev = rec["sha256"]
        return revisions, pending

    def cohort(self, pending, rows):
        """Admitted decisions in decision-time order (ties by row hash) and the time through which every scheduled
        decision is settled: just before the earliest decision still awaiting its label."""
        obs = sorted(self.records(), key=lambda o: (o["t"], o["row_sha256"]))
        if pending:
            through = min(pending) - 1
        else:
            through = max((r["t"] for r in rows), default=None)
            if obs:
                through = max(through or obs[-1]["t"], obs[-1]["t"])
        return {"all": obs, "scored": [o for o in obs if o["kind"] == "scored"], "settled_through": through}


# ---------------------------------------------------------------------------------------------- persistence
def _code_objects():
    here = Path(__file__).resolve().parent
    out = {}
    for name in CODE_FILES:
        data = (here / name).read_bytes()
        out[name] = {"name": name, "sha256": hashlib.sha256(data).hexdigest(), "text": data.decode("utf-8")}
    return out


def _cand_path(root, exp_id, cand):
    return Path(root) / "candidates" / f"{exp_id}-{cand[:12]}.json"


def _write_candidate(root, cand):
    p = _cand_path(root, cand["experiment"], cand["candidate_sha256"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(E.canon(cand))


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
    """The production provider: lab/data.Store at the cutoff and research_tools/panel.build from start_ms (the
    confirmation start, or the discovery window) to the cutoff. days only bounds a discovery query given no start.
    Labels for every requested horizon."""
    from lab.data import Store
    from research_tools import panel as P
    from lab.common import DAY

    def provide(cutoff_ms, start_ms=None, horizons=horizons):
        st = Store(base, cutoff=cutoff_ms)
        pn = P.build(st, start_ms if start_ms is not None else cutoff_ms - days * DAY, cutoff_ms)
        return {"rows": pn["rows"], "labels": {h: P.labels(st, pn, h) for h in horizons}, "panel": P.freeze(pn)}
    return provide


# ------------------------------------------------------------------------------------------------------- CLI
def _cli(argv=None):
    """python -m research_tools.research_api --root research/search --role researcher --actor actor.json <op> --args args.json
    ops: open | panel | inspect | run | ablate | counterexamples | config | register | results | evaluate | verify.
    args.json holds the operation's keyword arguments (request_id always). The provider is the repository's stored
    data; labels are built for the horizon the operation needs (the candidate's registered horizon for evaluate)."""
    import argparse
    import datetime as _dt
    ap = argparse.ArgumentParser(prog="research_tools.research_api")
    ap.add_argument("--root", default=str(ROOT / "research" / "search"))
    ap.add_argument("--role", choices=ROLES, required=True)
    ap.add_argument("--actor", required=True, help="JSON file: {kind, id, version, training_cutoff}")
    ap.add_argument("--anchor", help="anchor file written by the evaluator side (evaluator_service.py)")
    ap.add_argument("op", choices=("open", "panel", "inspect", "run", "ablate", "counterexamples", "config", "register",
                                   "results", "evaluate", "verify"))
    ap.add_argument("--args", required=True, help="JSON file with the operation's arguments")
    a = ap.parse_args(argv)
    actor = json.loads(Path(a.actor).read_text())
    kw = json.loads(Path(a.args).read_text())
    from research_tools.search_ledger import FileAnchor
    api = ResearchAPI(a.root, store_provider(ROOT), a.role, actor, lambda: _dt.datetime.now(_dt.timezone.utc),
                      anchor=FileAnchor(a.anchor) if a.anchor else None)
    h = (kw.get("spec") or {}).get("horizon_min", 60)
    ops = {"open": lambda: api.open_experiment(kw["experiment"], kw["family"], kw["discovery_cutoff_utc"],
                                               kw["disclosure"], kw["request_id"], kw.get("mode", "research-assistant")),
           "panel": lambda: api.panel(kw["experiment"], kw["cutoff_utc"], kw["request_id"],
                                      tuple(kw.get("horizons", [60]))),
           "inspect": lambda: api.inspect(kw["experiment"], kw["cutoff_utc"], kw["request_id"]),
           "run": lambda: api.run(kw["experiment"], kw["spec"], kw["cutoff_utc"], kw.get("budget", {}), kw["request_id"]),
           "ablate": lambda: api.ablate(kw["experiment"], kw["spec"], kw["cutoff_utc"], kw["request_id"], kw.get("drop")),
           "counterexamples": lambda: api.counterexamples(kw["experiment"], kw["spec"], kw["cutoff_utc"],
                                                          kw["request_id"], kw.get("k", 10)),
           "config": lambda: api.config(kw["experiment"], kw["configuration"], kw["request_id"]),
           "register": lambda: api.register(kw["experiment"], kw["spec"], kw["request_id"], kw.get("code_path")),
           "results": lambda: api.results(kw["experiment"], kw["candidate_sha256"], kw["request_id"]),
           "evaluate": lambda: api.evaluate(kw["experiment"], kw["candidate_sha256"], kw["request_id"]),
           "verify": lambda: {"ledger": api.ledger.verify_report(), "results": verify_results(a.root, kw["experiment"])}}
    del h
    try:
        print(json.dumps(ops[a.op](), indent=1, default=str))
        return 0
    except Refused as exc:
        print(json.dumps({"refused": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(_cli())
