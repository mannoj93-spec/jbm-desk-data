"""Prospective directional opportunity and forecast stream (directional-1.1.0, repo 2.30; 1.0.0 was repo 2.29).

A separate contract and operational path from the range stream, PS1 and O33 grades. Nothing here is live until a
registration has a verifiable published effective time (research/registrations/dir1-prepared/ is PREPARED only).
The operational entry point is research_tools/dir1_runner.py; the functions here are its parts.

1.1.0 repairs (Oct 19 2026 review, F4 and F5):
  - grade() enforced nothing: it returned "graded" with no publication evidence, a wrong content hash and p_up 2.0, and
    had no evaluation cutoff. It now grades only an admission produced by admit() (verified durable publication bound
    to the exact forecast bytes), only a probability in [0, 1], and only when the exit bar was available at the
    explicit evaluation cutoff (otherwise 'pending').
  - parse_forecast() raised AttributeError on JSON true, 42 or a list, and a NaN output broke infer()'s attempt
    record. A forecast must be a JSON object with a finite p_up in [0, 1]; every failure is an attempt record, and the
    raw output is kept as text even when it is not canonical JSON.
  - compare_arms() sorted arm names and reported frontier minus baseline as the primary comparison although the
    protocol registers statistical minus baseline. Comparisons now come from the protocol's registered list, each on
    its own pair-specific intersection, with the schedule as the denominator source (an opportunity every arm missed
    still counts) and late, missing, abstaining, failed and ungradable opportunities reported separately.
  - Targets. Forecast quality is scored against one common target for every arm (the forward return from the first
    bar at or after decision + publication deadline + execution delay), so arms with different publication delays
    forecast the same outcome. Paper economics stay latency-aware: each arm enters after its own publication.
  - Economics. Entry and exit prices are a bar-based paper price proxy (1m bar open/close), not observed executable
    quotes. Funding is the settled funding over the holding window, signed by side; a missing settlement makes net
    value unavailable (never zero). Inference cost in USD is reported beside trading economics, not netted.
  - Statistical arm. statistical_arm() validates its artifact (schema, equal-length coefficients, finite values,
    training cutoff, hash) instead of silently zipping mismatched arrays.

Clocks: source availability, feature build, inference start/end, durable publication (first availability on main or a
registry receipt), activation, first eligible bar. The forecast is never backdated to a bar close.
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

VERSION = "directional-1.1.0"
MIN = 60_000
TRANSITIONS = {
    None: ("expected",),
    "expected": ("inputs-ready", "inputs-unavailable", "missed"),
    "inputs-ready": ("inference-started", "missed"),
    "inference-started": ("forecast", "abstention", "error", "timeout"),
    "forecast": ("published", "publish-late", "publish-failed"),
    "abstention": ("published", "publish-late", "publish-failed", "graded", "ungradable"),
    "published": ("graded", "ungradable"),
    "publish-late": ("graded", "ungradable"),
}
TERMINAL = ("inputs-unavailable", "missed", "error", "timeout", "publish-failed", "graded", "ungradable")
ARMS = ("baseline", "statistical", "frontier", "text-event")
PROTOCOL_REQUIRED = ("id", "status", "instrument", "schedule", "inputs", "horizon_min", "forecast", "conversion",
                     "publication", "execution", "costs", "inference", "arms", "evaluation", "effective_utc")
PRICE_BASIS = "bar-based paper price proxy (1m bar open/close); not an observed executable quote"
METRICS = ("brier", "utility_bp", "net_bp")


# ------------------------------------------------------------------------------------------------- contract
def validate_protocol(p):
    probs = [f"missing {k}" for k in PROTOCOL_REQUIRED if k not in p]
    if probs:
        return probs
    if p["status"] not in ("prepared", "registered"):
        probs.append(f"status {p['status']!r}")
    if p["status"] == "registered" and not (p.get("effective_utc") and p.get("effective_evidence")):
        probs.append("a registered protocol needs effective_utc AND effective_evidence (a merge commit or registry receipt)")
    if p["status"] == "prepared" and p.get("effective_utc"):
        probs.append("a prepared protocol has no effective time")
    c = p["conversion"]
    if not (0 < c.get("short_below", -1) < c.get("long_above", 2) < 1):
        probs.append("conversion needs 0 < short_below < long_above < 1 on P(up)")
    if p["inference"].get("selection") != "first-valid-parse":
        probs.append("inference.selection must be 'first-valid-parse' (keeping the best of many answers is a search)")
    if set(p["arms"]) - set(ARMS):
        probs.append(f"unknown arms {sorted(set(p['arms']) - set(ARMS))}")
    if p["publication"].get("deadline_s") is None:
        probs.append("publication.deadline_s required")
    comps = (p.get("evaluation") or {}).get("comparisons")
    if comps is not None:
        for c in [comps.get("primary")] + list(comps.get("secondary") or []):
            if not isinstance(c, dict) or c.get("metric") not in METRICS or c.get("a") not in p["arms"] \
                    or c.get("b") not in p["arms"] or c.get("a") == c.get("b"):
                probs.append(f"comparison {c!r}: needs metric in {METRICS} and two different registered arms a, b")
    return probs


def protocol_sha256(p):
    return E.content_sha256(p)


# ---------------------------------------------------------------------------------------------- opportunities
def expected(protocol, start_ms, end_ms):
    """Scheduled opportunity times in [start, end): schedule = {"every_min": k, "offset_min": m}."""
    s = protocol["schedule"]
    step, off = s["every_min"] * MIN, s.get("offset_min", 0) * MIN
    t = (start_ms - off + step - 1) // step * step + off
    out = []
    while t < end_ms:
        out.append(t)
        t += step
    return out


def opp_id(protocol, t, arm):
    return f"{protocol['id']}-{arm}-{E.iso(E.epoch_ms(t)).replace(':', '').replace('-', '')}"


class OpportunityLog:
    """An append-only list of events [{opportunity, arm, state, t_utc, data, sha256}] with allowed transitions.
    In memory unless a path is given; dir1_runner.DurableOpportunityLog is the persistent, locked, recoverable form."""

    def __init__(self, events=None):
        self.events = list(events or [])

    def state(self, oid):
        st = None
        for e in self.events:
            if e["opportunity"] == oid:
                st = e["state"]
        return st

    def _event(self, oid, arm, state, t_utc, data):
        cur = self.state(oid)
        if state not in TRANSITIONS.get(cur, ()):
            raise ValueError(f"{oid}: transition {cur} -> {state} not allowed")
        e = {"opportunity": oid, "arm": arm, "state": state, "t_utc": E.iso(t_utc), "data": data or {}}
        e["sha256"] = E.content_sha256(e)
        return e

    def add(self, oid, arm, state, t_utc, data=None):
        e = self._event(oid, arm, state, t_utc, data)
        self.events.append(e)
        return e

    def history(self, oid):
        return [e for e in self.events if e["opportunity"] == oid]


def reconcile(protocol, log, start_ms, end_ms, now):
    """Create every expected opportunity; mark 'missed' any whose decision deadline passed without inference starting.
    Runs independently of the worker."""
    n = int(E.instant(now).timestamp() * 1000)
    dl = protocol["publication"]["deadline_s"] * 1000
    for t in expected(protocol, start_ms, end_ms):
        for arm in protocol["arms"]:
            oid = opp_id(protocol, t, arm)
            if log.state(oid) is None:
                log.add(oid, arm, "expected", E.epoch_ms(t), {"decision_t_utc": E.iso(E.epoch_ms(t))})
            if log.state(oid) in ("expected", "inputs-ready") and n > t + dl:
                log.add(oid, arm, "missed", now, {"reason": "no inference started before the publication deadline"})
    return log


# ------------------------------------------------------------------------------------------------- inference
def raw_text(raw):
    """The raw output as text for retention, whatever it is (bytes, dict, NaN-bearing object, text)."""
    if raw is None:
        return None
    if isinstance(raw, (bytes, bytearray)):
        return bytes(raw).decode("utf-8", errors="replace")
    if isinstance(raw, str):
        return raw
    return json.dumps(raw, sort_keys=True, allow_nan=True, default=repr)


def parse_forecast(raw):
    """A structured forecast {"p_up": float in [0,1]} from a model's raw output (a dict, or JSON text/bytes); never
    repaired. Anything that is not a JSON object - true, 42, a list, a string - is refused, not an exception."""
    if isinstance(raw, (bytes, bytearray)):
        try:
            raw = bytes(raw).decode("utf-8")
        except UnicodeDecodeError:
            return None, "unparseable (not UTF-8)"
    if isinstance(raw, dict):
        d = raw
    elif isinstance(raw, str):
        try:
            d = E.loads_strict(raw)
        except ValueError:
            return None, "unparseable"
    else:
        return None, f"not a JSON object ({type(raw).__name__})"
    if not isinstance(d, dict):
        return None, f"not a JSON object ({type(d).__name__})"
    p, st = E.number(d.get("p_up"), "probability")
    return (p, "ok") if st == "ok" else (None, f"p_up {st}")


def _attempt(k, t0, t1, raw, cost, err, model, pol):
    lat = (E.instant(t1) - E.instant(t0)).total_seconds()
    p, why = (None, err) if err else parse_forecast(raw)
    if lat > pol["timeout_s"]:
        p, why = None, f"timeout ({lat:.1f} s > {pol['timeout_s']} s; measured after return - not a cancellation)"
    txt = raw_text(raw)
    return {"attempt": k, "start_utc": E.iso(t0), "end_utc": E.iso(t1), "latency_s": round(lat, 3),
            "cost_usd": cost, "raw_sha256": hashlib.sha256(txt.encode()).hexdigest() if txt is not None else None,
            "raw_text": txt, "parse": why, "p_up": p, "model": model}


def infer(arm_fn, features, protocol, clock, model=None):
    """In-process attempt policy for deterministic arms and fixtures. arm_fn(features, attempt) -> (raw, cost_usd).
    The selection is the first attempt that parses. A call that hangs is NOT cancelled here; operational inference uses
    dir1_runner.infer_with_deadline, which runs each attempt in a child process and kills it at the deadline."""
    pol = protocol["inference"]
    attempts, chosen = [], None
    for k in range(pol["max_attempts"]):
        t0 = clock()
        try:
            raw, cost = arm_fn(features, k)
            err = None
        except Exception as exc:
            raw, cost, err = None, 0.0, f"{type(exc).__name__}: {str(exc)[:120]}"
        t1 = clock()
        attempts.append(_attempt(k, t0, t1, raw, cost, err, model, pol))
        if attempts[-1]["p_up"] is not None:
            chosen = k
            break
    return _selection(attempts, chosen)


def _selection(attempts, chosen):
    costs = [a["cost_usd"] for a in attempts]
    return {"selected_attempt": chosen, "attempts": attempts,
            "p_up": attempts[chosen]["p_up"] if chosen is not None else None,
            "cost_usd": None if any(c is None for c in costs) else round(sum(costs), 6),
            "cost_usd_known": round(sum(c for c in costs if c is not None), 6),
            "latency_s": round(sum(a["latency_s"] for a in attempts), 3),
            "outcome": "forecast" if chosen is not None else
            ("timeout" if attempts and str(attempts[-1]["parse"]).startswith("timeout") else "error")}


def action(protocol, p_up):
    c = protocol["conversion"]
    if p_up is None:
        return None
    return 1 if p_up > c["long_above"] else -1 if p_up < c["short_below"] else 0


# ---------------------------------------------------------------------------------------------- publication
def publication_status(protocol, decision_ms, content, evidence):
    """The timing/binding check on CLAIMED evidence {"kind", "ref", "published_utc", "content_sha256"}: late if after
    decision + deadline; failed if it does not bind this content or is backdated. A claim is not a proof: admit() is
    the operational check (it asks a verifier for the durable copy's own first availability)."""
    if not isinstance(evidence, dict) or evidence.get("kind") not in ("git-commit", "registry") or not evidence.get("ref"):
        return "publish-failed", "no durable publication evidence"
    if evidence.get("content_sha256") != E.content_sha256(content):
        return "publish-failed", "published content differs from the forecast (an on-time id with other content)"
    pt = E.maybe_instant(evidence.get("published_utc"))
    if pt is None:
        return "publish-failed", "publication time missing or without a timezone"
    dl = decision_ms + protocol["publication"]["deadline_s"] * 1000
    pm = int(pt.timestamp() * 1000)
    if pm < decision_ms:
        return "publish-failed", "publication time before the decision time (backdated)"
    return ("published", "on time") if pm <= dl else ("publish-late", f"{(pm - dl) / 1000:.0f} s after the deadline")


def admit(protocol, decision_ms, content, evidence, verifier):
    """The admission of a forecast: the verifier confirms the durable copy (main-branch first availability or a
    registry receipt with read-back) holds exactly these bytes and returns its own first-availability time; the
    caller's or the Git author's timestamp is never used. Returns {"class": on-time | late | failed, ...}."""
    if verifier is None:
        return {"class": "failed", "reason": "no verifier: publication cannot be established"}
    ok, first_utc, why, receipt = verifier.verify(evidence, content)
    if not ok:
        return {"class": "failed", "reason": why, "evidence": evidence}
    claimed = dict(evidence, published_utc=first_utc, content_sha256=evidence.get("content_sha256"))
    st, detail = publication_status(protocol, decision_ms, content, claimed)
    cls = {"published": "on-time", "publish-late": "late"}.get(st, "failed")
    return {"class": cls, "reason": detail, "published_utc": first_utc, "content_sha256": E.content_sha256(content),
            "evidence": evidence, "verified_by": getattr(verifier, "name", type(verifier).__name__),
            "receipt": receipt, "fixture": bool(getattr(verifier, "fixture", False))}


# -------------------------------------------------------------------------------------------------- grading
def first_executable(bars, after_ms, delay_s=0):
    """The first 1m bar whose open is at or after after_ms + delay: its open is the paper entry price proxy."""
    t = (after_ms + delay_s * 1000 + MIN - 1) // MIN * MIN
    for k in range(0, 120):
        b = bars.get(t + k * MIN)
        if b is not None:
            return t + k * MIN, b["o"]
    return None, None


def settled_funding(funding, entry_ms, exit_ms, every_h=8):
    """(sum of settled rates over (entry, exit], state). funding: [{"t": settle_ms, "rate": r}] or None. Every
    scheduled settlement in the window must be present; otherwise ('unavailable')."""
    if funding is None:
        return None, "funding-unavailable: no settled funding supplied"
    step = every_h * 60 * MIN
    have = {int(x["t"]): x for x in funding}
    total, t = 0.0, (entry_ms // step + 1) * step
    while t <= exit_ms:
        x = have.get(t)
        r, st = E.number(x.get("rate") if x else None, "funding_rate")
        if st != "ok":
            return None, f"funding-unavailable: settlement {E.iso(E.epoch_ms(t))} {st}"
        total += r
        t += step
    return total, "ok"


def grade(protocol, decision_ms, p_up, admission, bars, evaluation_cutoff_ms=None, funding=None, inference_usd=None):
    """Grade one admitted forecast. Refuses (state 'refused') without an on-time or late admission from admit(), an
    invalid probability or an evaluation cutoff; 'pending' when the outcome was not available at the cutoff. Three
    separate numbers: forecast quality (Brier on the common target), directional utility and net paper value (each on
    this arm's own latency-aware entry), plus inference cost in USD beside them."""
    if evaluation_cutoff_ms is None:
        return {"state": "refused", "reason": "no evaluation cutoff: label maturity cannot be judged"}
    p, pst = E.number(p_up, "probability")
    if pst != "ok":
        return {"state": "refused", "reason": f"p_up {pst}"}
    if not isinstance(admission, dict) or admission.get("class") not in ("on-time", "late"):
        return {"state": "refused", "reason": "no verified durable publication (admit() did not admit it)"}
    pub_ms = int(E.instant(admission["published_utc"]).timestamp() * 1000)
    a = action(protocol, p)
    h = protocol["horizon_min"]
    delay = protocol["execution"]["delay_s"]
    tgt_t, tgt_open = first_executable(bars, decision_ms + protocol["publication"]["deadline_s"] * 1000, delay)
    entry_t, entry = first_executable(bars, max(decision_ms, pub_ms), delay)
    if entry_t is None or tgt_t is None:
        return {"state": "ungradable", "reason": "no bar after publication"}
    exit_b, tgt_exit = bars.get(entry_t + (h - 1) * MIN), bars.get(tgt_t + (h - 1) * MIN)
    if exit_b is None or tgt_exit is None:
        last = max(entry_t, tgt_t) + (h - 1) * MIN
        if last + MIN > evaluation_cutoff_ms:
            return {"state": "pending", "reason": "outcome window not closed at the evaluation cutoff"}
        return {"state": "ungradable", "reason": "exit bar missing"}
    avail = max(exit_b.get("avail") or 0, tgt_exit.get("avail") or 0)
    if not exit_b.get("avail") or not tgt_exit.get("avail") or avail > evaluation_cutoff_ms:
        return {"state": "pending", "reason": "outcome not available at the evaluation cutoff"}
    r = 1e4 * math.log(exit_b["c"] / entry)
    target = 1e4 * math.log(tgt_exit["c"] / tgt_open)
    up = 1 if target > 0 else 0
    out = {"state": "graded", "admission": admission["class"], "entry_utc": E.iso(E.epoch_ms(entry_t)), "entry": entry,
           "exit": exit_b["c"], "forward_bp": round(r, 4), "target_utc": E.iso(E.epoch_ms(tgt_t)),
           "target_bp": round(target, 4), "action": a, "label_available_ms": avail, "p_up": p,
           "brier": round((p - up) ** 2, 6), "utility_bp": None if a is None else round(a * r, 4),
           "price_basis": PRICE_BASIS, "inference_usd": inference_usd}
    c = protocol["costs"]
    if a:
        f, fst = settled_funding(funding, entry_t, entry_t + h * MIN)
        if fst != "ok":
            out.update(net_bp=None, net_state=fst)
        else:
            cost = 2 * c["fee_bp_per_side"] + 2 * c["spread_slippage_bp_per_side"] + a * f * 1e4
            out.update(net_bp=round(a * r - cost, 4), cost_bp=round(cost, 4), funding_bp=round(a * f * 1e4, 4),
                       net_state="ok")
    else:
        out.update(net_bp=0.0 if a == 0 else None, net_state="no position")
    out["evidence_class"] = ("paper simulation on a bar-based price proxy; not execution"
                             + ("; FIXTURE publication" if admission.get("fixture") else ""))
    return out


def compare_arms(graded, protocol=None, schedule=None):
    """graded: {arm: {opportunity_t: grade-or-state}}. Per-arm full denominators from the schedule (or, without one,
    the union of recorded times - reported as such), and each REGISTERED comparison (protocol evaluation.comparisons)
    on its own pair-specific intersection of on-time graded opportunities. Arm order and extra arms change nothing."""
    arms = sorted(graded)
    if schedule is not None:
        ts, source = sorted(set(schedule)), "schedule"
    else:
        ts, source = sorted({t for a in arms for t in graded[a]}), "union of recorded opportunities (no schedule given)"
    out = {"version": VERSION, "opportunities": len(ts), "denominator_source": source, "arms": {}}

    def rec(a, t):
        g = graded.get(a, {}).get(t)
        return g if isinstance(g, dict) else None

    for a in arms:
        ok = [rec(a, t) for t in ts if (rec(a, t) or {}).get("state") == "graded"]
        on = [x for x in ok if x.get("admission", "on-time") == "on-time"]
        taken = [x["net_bp"] for x in on if x.get("net_bp") is not None and x.get("action")]
        br = [x["brier"] for x in on if x.get("brier") is not None]
        out["arms"][a] = {"graded": len(ok), "graded_on_time": len(on), "graded_late": len(ok) - len(on),
                          "not_graded": len(ts) - len(ok),
                          "states": _count((rec(a, t) or {}).get("state") or "missing" for t in ts),
                          "abstentions": sum(1 for x in on if x.get("action") == 0),
                          "mean_brier_conditional_on_valid": round(sum(br) / len(br), 6) if br else None,
                          "trades": len(taken), "mean_net_bp": round(sum(taken) / len(taken), 4) if taken else None}
    out["paired_intersection"] = sum(1 for t in ts if all((rec(a, t) or {}).get("state") == "graded" for a in arms))
    comps = ((protocol or {}).get("evaluation") or {}).get("comparisons")
    if comps is None:
        out["comparisons"] = None
        out["comparison_note"] = "no registered comparisons supplied: no primary difference is computed"
    else:
        out["comparisons"] = {}
        for role, c in [("primary", comps["primary"])] + [(f"secondary-{i + 1}", x)
                                                          for i, x in enumerate(comps.get("secondary") or [])]:
            m, a, b = c["metric"], c["a"], c["b"]
            pair = [t for t in ts if all((rec(x, t) or {}).get("state") == "graded"
                                         and rec(x, t).get("admission", "on-time") == "on-time"
                                         and rec(x, t).get(m) is not None for x in (a, b))]
            d = [rec(a, t)[m] - rec(b, t)[m] for t in pair]

            def valid(x, t):
                g = rec(x, t) or {}
                return g.get("state") == "graded" and g.get("admission", "on-time") == "on-time" and g.get(m) is not None
            out["comparisons"][role] = {"metric": m, "difference": f"{a} - {b}", "n_pair": len(pair),
                                        "mean_difference": round(sum(d) / len(d), 6) if d else None,
                                        "scheduled": len(ts),
                                        "not_valid": {x: sum(1 for t in ts if not valid(x, t)) for x in (a, b)},
                                        "policy": "pair-specific intersection of on-time graded forecasts; no score "
                                                  "is invented for a missing forecast; full denominators beside it"}
    out["note"] = "overlapping horizons: opportunities are not independent; uncertainty via research_tools/calibration.py blocks"
    return out


def _count(xs):
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


def latency_report(records):
    """Distributions of the measured path (seconds): input age at the decision, feature build, inference, decision to
    durable publication, publication to first eligible bar, and the whole available-input to entry path."""
    keys = ("input_age_s", "build_s", "inference_s", "publish_delay_s", "quote_delay_s", "input_to_entry_s")
    out = {}
    for k in keys:
        xs = sorted(r[k] for r in records if r.get(k) is not None)
        out[k] = {"n": len(xs), "median": xs[len(xs) // 2] if xs else None,
                  "p90": xs[min(len(xs) - 1, int(0.9 * len(xs)))] if xs else None, "max": xs[-1] if xs else None}
    return out


# --------------------------------------------------------------------------------------------- reference arms
def baseline_arm(protocol):
    """The declared simple baseline: P(up) = 0.5 + clip(ret_1h_bp / 400, -0.2, 0.2) (trailing-hour momentum)."""
    def fn(features, attempt):
        r = features.get("ret_1h_bp")
        if r is None:
            return {"p_up": None}, 0.0
        return {"p_up": round(0.5 + max(-0.2, min(0.2, r / 400)), 6)}, 0.0
    return fn


def statistical_arm(artifact, allowed_cutoff=None):
    """A frozen logistic model from fit_logistic(). The artifact is validated first (research_api.
    validate_statistical_artifact): mismatched coefficient and feature arrays, non-finite values, a training cutoff
    after allowed_cutoff or an altered hash raise ValueError instead of being truncated or trusted."""
    from research_tools.research_api import validate_statistical_artifact
    probs = validate_statistical_artifact(artifact, allowed_cutoff)
    if probs:
        raise ValueError("; ".join(probs))

    def fn(features, attempt):
        xs = [features.get(k) for k in artifact["features"]]
        if any(x is None for x in xs):
            return {"p_up": None}, 0.0
        z = artifact["intercept"] + sum(c * x for c, x in zip(artifact["coef"], xs))
        return {"p_up": round(1 / (1 + math.exp(-max(-30, min(30, z)))), 6)}, 0.0
    fn.artifact_sha256 = artifact["sha256"]
    return fn


def frontier_arm_stub(responses):
    """TEST-ONLY stand-in for a model call: returns the scripted raw outputs in order. Never a live model; records
    produced with it are fixtures."""
    seq = list(responses)

    def fn(features, attempt):
        item = seq.pop(0) if seq else RuntimeError("no scripted response")
        if isinstance(item, Exception):
            raise item
        return item, 0.002
    fn.test_only = True
    return fn


def fit_logistic(rows, labels, features, train_cutoff_ms, l2=1.0, iters=300, lr=0.05):
    """Fit the statistical arm on rows with T < train_cutoff and labels available before it (no confirmation data)."""
    lab = {x["t"]: x for x in labels if x.get("state") == "ok" and x["label_available"] is not None
           and x["label_available"] < train_cutoff_ms}
    X, y = [], []
    for r in rows:
        if r["t"] >= train_cutoff_ms or r["t"] not in lab:
            continue
        xs = [r["features"].get(k) for k in features]
        if any(v is None for v in xs):
            continue
        X.append(xs)
        y.append(1 if lab[r["t"]]["label_bp"] > 0 else 0)
    w, b = [0.0] * len(features), 0.0
    n = len(X)
    for _ in range(iters if n else 0):
        gw, gb = [l2 * wi / n for wi in w], 0.0
        for xs, yi in zip(X, y):
            p = 1 / (1 + math.exp(-max(-30, min(30, b + sum(wi * xi for wi, xi in zip(w, xs))))))
            e = p - yi
            gb += e / n
            gw = [g + e * xi / n for g, xi in zip(gw, xs)]
        w = [wi - lr * g for wi, g in zip(w, gw)]
        b -= lr * gb
    art = {"schema": "directional-statistical/1", "features": features, "coef": [round(x, 8) for x in w],
           "intercept": round(b, 8), "train_cutoff_utc": E.iso(E.epoch_ms(train_cutoff_ms)), "n_train": n,
           "training_rows_sha256": E.content_sha256([[r["t"] for r in rows if r["t"] < train_cutoff_ms]])}
    art["sha256"] = E.content_sha256(art)
    return art


def model_identity_changes(attempts):
    """Observed model identities across attempts in time order; a change of observed version under one requested id
    (an alias that moved) is reported, so a challenger comparison never silently spans two models."""
    seen, changes = {}, []
    for a in attempts:
        m = a.get("model") or {}
        key = (m.get("provider"), m.get("id"))
        v = m.get("observed_version")
        if key in seen and v is not None and seen[key] != v:
            changes.append({"model": key, "from": seen[key], "to": v, "at": a.get("start_utc"),
                            "pinned": m.get("pinned")})
        if v is not None:
            seen[key] = v
    return changes
