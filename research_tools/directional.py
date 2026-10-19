"""Prospective directional opportunity and forecast stream (directional-1.0.0, repo 2.29; brief sections 13-14, 16).

A separate contract and operational path from the range stream, PS1 and O33 grades. Nothing here is live until a
registration has a verifiable published effective time (research/registrations/dir1-prepared/ is PREPARED only).

1. Contract  protocol JSON (validate_protocol): instrument, decision schedule, allowed inputs and age limits,
             horizon, forecast representation (P(up) in [0,1]), long/short/abstain thresholds, publication deadline
             and what counts as durable publication, entry/exit and price source, costs (fees, spread/slippage,
             funding, inference), retry/timeout/parse policy, arms, primary metric, dependence and checkpoints.
2. Opportunities  expected(protocol, start, end) lists every scheduled opportunity from the schedule alone. reconcile()
             creates a 'missed' record for any expected opportunity no worker touched, so a non-running worker
             cannot erase its misses. Every opportunity keeps an append-only event list with allowed transitions:
                expected -> inputs-ready | inputs-unavailable | missed
                inputs-ready -> inference-started
                inference-started -> forecast | abstention | error | timeout
                forecast | abstention -> published | publish-late | publish-failed
                published | publish-late | abstention -> graded | ungradable
             A transition not in the table is refused; an event is never edited.
3. Attempts  every inference attempt is kept (latency, cost, raw-output hash, parse result). The selection rule is
             registered: the FIRST attempt that parses. Asking again and keeping the most persuasive answer is a
             search, not a retry, and is refused by construction.
4. Clocks    source availability (max input avail), feature-build end, inference start/end, durable publication,
             activation, first eligible executable quote. The forecast is never backdated to a bar close; a quote
             before the decision could have existed is never scored; an on-time id with late content is late
             (publication evidence binds the content sha256).
5. Arms      paired on the same opportunities: 'baseline' (declared simple rule), 'statistical' (frozen model on the
             same permitted inputs), 'frontier' (a model call through a pinned interface), 'text-event' (gated). Missing
             forecasts stay in each arm's denominator; the intersection is reported beside the full denominator.
6. Grading   three separate numbers: forecast quality (Brier score of P(up) against the realized sign), directional
             utility (action x forward return, bp, before costs), net execution value (after fees, spread/slippage,
             funding and inference cost). A paper simulation is never labelled execution.
Model provenance (section 13) is recorded on every attempt: provider, model id, whether it is a pinned version or an
alias that can change, observed version strings, prompt/template sha256, tool policy.
"""
import hashlib
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "directional-1.0.0"
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
    """In-memory view over an append-only list of events [{opportunity, arm, state, t_utc, data}]."""

    def __init__(self, events=None):
        self.events = list(events or [])

    def state(self, oid):
        st = None
        for e in self.events:
            if e["opportunity"] == oid:
                st = e["state"]
        return st

    def add(self, oid, arm, state, t_utc, data=None):
        cur = self.state(oid)
        if state not in TRANSITIONS.get(cur, ()):
            raise ValueError(f"{oid}: transition {cur} -> {state} not allowed")
        e = {"opportunity": oid, "arm": arm, "state": state, "t_utc": E.iso(t_utc), "data": data or {}}
        e["sha256"] = E.content_sha256(e)
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
def parse_forecast(raw):
    """A structured forecast {"p_up": float in [0,1]} from a model's raw output (dict or JSON text); never repaired."""
    try:
        d = raw if isinstance(raw, dict) else E.loads_strict(str(raw))
    except ValueError:
        return None, "unparseable"
    p, st = E.number((d or {}).get("p_up"), "probability")
    return (p, "ok") if st == "ok" else (None, f"p_up {st}")


def infer(arm_fn, features, protocol, clock, model=None):
    """Run the registered attempt policy. arm_fn(features, attempt) -> (raw_output, cost_usd). Returns the selected
    forecast and every attempt. The selection is the first attempt that parses; later attempts are not requested
    once one parses."""
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
        lat = (E.instant(t1) - E.instant(t0)).total_seconds()
        p, why = (None, err) if err else parse_forecast(raw)
        if lat > pol["timeout_s"]:
            p, why = None, f"timeout ({lat:.1f} s > {pol['timeout_s']} s)"
        attempts.append({"attempt": k, "start_utc": E.iso(t0), "end_utc": E.iso(t1), "latency_s": round(lat, 3),
                         "cost_usd": cost, "raw_sha256": hashlib.sha256(E.canon(raw).encode()).hexdigest()
                         if raw is not None else None, "parse": why, "p_up": p, "model": model})
        if p is not None:
            chosen = k
            break
    return {"selected_attempt": chosen, "attempts": attempts,
            "p_up": attempts[chosen]["p_up"] if chosen is not None else None,
            "cost_usd": round(sum(a["cost_usd"] or 0 for a in attempts), 6),
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
    """evidence: {"kind": "git-commit"|"registry", "ref", "published_utc", "content_sha256"} - the durable copy's
    own time and the hash of the bytes it holds. Late if published after decision + deadline; failed if the evidence
    does not bind this content."""
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


# -------------------------------------------------------------------------------------------------- grading
def first_executable(bars, after_ms, delay_s=0):
    """The first 1m bar whose open is at or after after_ms + delay: its open is the first eligible executable quote
    under the paper policy (bars: {open_ms: {"o","c","avail"}})."""
    t = (after_ms + delay_s * 1000 + MIN - 1) // MIN * MIN
    for k in range(0, 120):
        b = bars.get(t + k * MIN)
        if b is not None:
            return t + k * MIN, b["o"]
    return None, None


def grade(protocol, decision_ms, p_up, publication, bars, funding_bp=0.0):
    """Three separate numbers for one opportunity, from the first eligible quote after max(decision, publication,
    activation). Returns state graded | ungradable with reasons."""
    a = action(protocol, p_up)
    pub_ms = int(E.instant(publication["published_utc"]).timestamp() * 1000) if publication else decision_ms
    start = max(decision_ms, pub_ms)
    entry_t, entry = first_executable(bars, start, protocol["execution"]["delay_s"])
    if entry_t is None:
        return {"state": "ungradable", "reason": "no executable quote after publication"}
    exit_b = bars.get(entry_t + (protocol["horizon_min"] - 1) * MIN)
    if exit_b is None:
        return {"state": "ungradable", "reason": "exit bar missing"}
    r = 1e4 * math.log(exit_b["c"] / entry)
    up = 1 if r > 0 else 0
    out = {"state": "graded", "entry_utc": E.iso(E.epoch_ms(entry_t)), "entry": entry, "exit": exit_b["c"],
           "forward_bp": round(r, 4), "action": a, "label_available_ms": exit_b.get("avail"),
           "brier": None if p_up is None else round((p_up - up) ** 2, 6),
           "utility_bp": None if a is None else round(a * r, 4)}
    c = protocol["costs"]
    if a:
        cost = 2 * c["fee_bp_per_side"] + 2 * c["spread_slippage_bp_per_side"] + a * funding_bp
        out["net_bp"] = round(a * r - cost, 4)
        out["cost_bp"] = round(cost, 4)
    else:
        out["net_bp"] = 0.0 if a == 0 else None
    out["evidence_class"] = "paper simulation at first eligible quote; not execution"
    return out


def compare_arms(graded):
    """graded: {arm: {opportunity_t: grade-or-state}}. Full denominators per arm and the paired intersection."""
    arms = sorted(graded)
    ts = sorted({t for a in arms for t in graded[a]})
    out = {"version": VERSION, "opportunities": len(ts), "arms": {}}
    for a in arms:
        g = graded[a]
        ok = [g[t] for t in ts if isinstance(g.get(t), dict) and g[t].get("state") == "graded"]
        taken = [x["net_bp"] for x in ok if x.get("net_bp") is not None and x.get("action")]
        br = [x["brier"] for x in ok if x.get("brier") is not None]
        out["arms"][a] = {"graded": len(ok), "not_graded": len(ts) - len(ok),
                          "states": _count((g[t].get("state") or "missing") if isinstance(g.get(t), dict) else "missing"
                                           for t in ts),
                          "mean_brier": round(sum(br) / len(br), 6) if br else None,
                          "trades": len(taken), "mean_net_bp": round(sum(taken) / len(taken), 4) if taken else None}
    both = [t for t in ts if all(isinstance(graded[a].get(t), dict) and graded[a][t].get("state") == "graded" for a in arms)]
    out["paired_intersection"] = len(both)
    if len(arms) >= 2 and both:
        a0, a1 = arms[0], arms[1]
        d = [graded[a1][t]["brier"] - graded[a0][t]["brier"] for t in both
             if graded[a1][t]["brier"] is not None and graded[a0][t]["brier"] is not None]
        out["paired_brier_diff"] = {"arms": f"{a1} - {a0}", "n": len(d), "mean": round(sum(d) / len(d), 6) if d else None}
    out["note"] = "overlapping horizons: opportunities are not independent; uncertainty via research_tools/calibration.py blocks"
    return out


def _count(xs):
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


def latency_report(records):
    """Distributions of the measured path: inputs-to-decision, inference, decision-to-publication, publication-to-
    first-quote (seconds)."""
    keys = ("input_age_s", "inference_s", "publish_delay_s", "quote_delay_s")
    out = {}
    for k in keys:
        xs = sorted(r[k] for r in records if r.get(k) is not None)
        out[k] = {"n": len(xs), "median": xs[len(xs) // 2] if xs else None, "max": xs[-1] if xs else None}
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


def statistical_arm(artifact):
    """A frozen logistic model: artifact {"features", "coef", "intercept", "train_cutoff_utc", "sha256"} fitted on
    data before its training cutoff (lab/panel.fit_transform for scaling)."""
    def fn(features, attempt):
        xs = [features.get(k) for k in artifact["features"]]
        if any(x is None for x in xs):
            return {"p_up": None}, 0.0
        z = artifact["intercept"] + sum(c * x for c, x in zip(artifact["coef"], xs))
        return {"p_up": round(1 / (1 + math.exp(-max(-30, min(30, z)))), 6)}, 0.0
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
           "intercept": round(b, 8), "train_cutoff_utc": E.iso(E.epoch_ms(train_cutoff_ms)), "n_train": n}
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
