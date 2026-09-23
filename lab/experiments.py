"""Versioned experiment designs, chronological evaluation and the variants ledger.

A design (lab/designs/<id>.json) is frozen by its SHA-256. The first time the lab sees a design
hash it stamps a registration time in state/lab_registered.json (the same append-only clock idea as
tests/ and forecasts). Episodes are then split, never mixed:
  exploratory  historical reconstruction, or prospective decisions before registration
               (where thresholds may have been tuned);
  evaluation   prospective decisions at or after registration, with inputs as actually written.
Status (see STATUS_RULES) can only reach "supported" on evaluation episodes, after the design's
minimum count of independent, non-overlapping episodes, with an interval for (test - reference)
and for the residual over the simple baseline both excluding zero in the hypothesised direction,
and with the same sign in both chronological halves. Nothing is described as significant or
profitable; intervals are descriptive, and the family's number of tested variants is reported.

Reference groups. A design compares its test group(s) either with another event group (weak vs
strong response, slow vs fast recovery ...) or with scheduled controls. Controls are labelled in
BOTH directions ("control" long, "control_short" short) and the reference value at each control
time is p_long x long outcome + (1 - p_long) x short outcome, where p_long is the test group's
share of long episodes: the outcome of entering at a scheduled time with the test group's
direction mix, costs included. Regression baselines use the controls' own recorded orientation.
"""
import hashlib
import json
from pathlib import Path

from lab import outcomes, stats
from lab.common import (H, LAB_VERSION, MINUTE, append, atomic_json, digest, iso, read_json)
from lab.events import collapse

STATUS_RULES = {
    "exploratory": "no evaluation episodes yet, or the design is not registered",
    "under prospective evaluation": "registered; evaluation episodes accumulating below the design minimum, "
                                    "or intervals not yet excluding zero",
    "supported": "evaluation episodes >= min_independent_episodes; 90% day-block intervals for test-minus-"
                 "reference AND (when the design names baseline predictors) residual-over-baseline exclude zero in the hypothesised direction; same sign in "
                 "both chronological halves",
    "retired": "superseded design version, or evaluation interval at the minimum count lies entirely on the "
               "wrong side of zero",
}


def design_files(base):
    return sorted((Path(base) / "lab/designs").glob("*.json"))


def load_design(path):
    raw = Path(path).read_bytes()
    d = json.loads(raw)
    d["_sha256"] = hashlib.sha256(raw).hexdigest()
    d["_file"] = "lab/designs/" + Path(path).name
    return d


def register(base, designs, now):
    """Stamp first-seen times for new design hashes (never rewrites an existing stamp)."""
    path = Path(base) / "state/lab_registered.json"
    stamps = read_json(path, {})
    changed = False
    for d in designs:
        key = f"{d['_file']}@{d['_sha256']}"
        if key not in stamps:
            stamps[key] = now
            changed = True
    if changed:
        atomic_json(path, stamps)
    return {d["id"]: stamps[f"{d['_file']}@{d['_sha256']}"] for d in designs}


def orient(outcome, metric):
    return outcome.get(metric) if outcome and outcome.get("status") == "complete" else None


def label_all(heads, bars, now, horizons, funding, snaps):
    labelled = []
    immature = incomplete = 0
    for e in heads:
        hs = None
        if snaps and e["basis"].startswith("prospective"):
            hs, _ = outcomes.half_spread_bp(snaps, e["t_available"])
        lab = outcomes.label(e["t_available"], e["direction"], bars, now, horizons, funding, hs)
        immature += sum(1 for v in lab.values() if v["status"] == "immature")
        incomplete += sum(1 for v in lab.values() if v["status"] == "incomplete")
        labelled.append((e, lab))
    return labelled, immature, incomplete


def regime_fn(bars):
    """Descriptive regime label at t from bars stored before t: trailing-24h realised volatility
    above/below the median over the pass window, and trailing-24h return sign. The volatility
    median uses the whole window, so the split is descriptive only and never an input to a decision."""
    import math
    hourly = sorted(t for t in bars if t % H == 0)
    rv, ret = {}, {}
    for t in hourly:
        seq = [bars.get(t - k * MINUTE) for k in range(1440, 0, -1)]
        if sum(b is None for b in seq) > 60:
            continue
        cl = [b["c"] for b in seq if b]
        rv[t] = math.sqrt(sum(math.log(b / a) ** 2 for a, b in zip(cl, cl[1:])))
        ret[t] = math.log(cl[-1] / cl[0])
    if not rv:
        return lambda t: "unknown"
    med = sorted(rv.values())[len(rv) // 2]

    def f(t):
        h = t // H * H
        if h not in rv:
            return "unknown"
        return ("high_vol" if rv[h] > med else "low_vol") + ("/up" if ret[h] >= 0 else "/down")
    return f


def summarize(labelled, design, registered, phase, basis="prospective", regime_of=None):
    """Per-horizon comparison of the test group with the reference group and controls."""
    metric = design["outcome"]["metric"]
    test_g, ref_g = design["comparison"]["test_group"], design["comparison"]["reference_group"]
    test_g = set(test_g) if isinstance(test_g, list) else {test_g}
    sign = design["comparison"].get("hypothesised_sign", -1)
    keys = design.get("baseline_predictors", [])
    out = {}
    for hmin in design["outcome"]["horizons_min"]:
        def rows(groups):
            items = []
            for e, lab in labelled:
                if e["group"] not in groups:
                    continue
                y = orient(lab.get(hmin) or lab.get(str(hmin)), metric)
                if y is None:
                    continue
                if phase == "evaluation" and (registered is None or e["t_event"] < registered):
                    continue
                if (phase == "exploratory" and basis == "prospective" and registered is not None
                        and e["t_event"] >= registered):
                    continue                                    # evaluation episodes never tune the design
                items.append(dict({k: e["features"].get(k) for k in keys}, t=e["t_event"], y=y, d=e["direction"]))
            return stats.nonoverlap(items, hmin * MINUTE)
        test, ctl = rows(test_g), rows({"control"})
        p_long = sum(1 for r in test if r["d"] > 0) / len(test) if test else None
        if ref_g == "control":
            shorts = {r["t"]: r["y"] for r in rows({"control_short"})}
            longs = {r["t"]: r["y"] for r in rows({"control_long"})}
            w = p_long if p_long is not None else 0.5
            ref = [{"t": t, "y": w * longs[t] + (1 - w) * shorts[t]} for t in sorted(longs) if t in shorts]
        else:
            ref = rows({ref_g})
        res, beta = stats.residualize(ctl, test, keys) if keys else (None, None)
        diff = stats.block_bootstrap_diff([(r["t"], r["y"]) for r in test], [(r["t"], r["y"]) for r in ref])
        resid_ci = stats.block_bootstrap_diff(res, [(t, 0.0) for t, _ in res]) if res else None
        halves = None
        if len(test) >= 4 and len(ref) >= 4:
            mid = sorted(r["t"] for r in test + ref)[len(test + ref) // 2]
            h1 = stats.mean([r["y"] for r in test if r["t"] < mid]), stats.mean([r["y"] for r in ref if r["t"] < mid])
            h2 = stats.mean([r["y"] for r in test if r["t"] >= mid]), stats.mean([r["y"] for r in ref if r["t"] >= mid])
            halves = [None if None in h1 else h1[0] - h1[1], None if None in h2 else h2[0] - h2[1]]
        out[str(hmin)] = {"test": stats.describe([r["y"] for r in test]), "reference": stats.describe([r["y"] for r in ref]),
                          "controls": stats.describe([r["y"] for r in ctl]), "diff_test_minus_reference_90": diff,
                          "residual_over_baseline": stats.describe([v for _, v in res]) if res else {"n": 0},
                          "residual_90": resid_ci, "baseline_beta": beta, "chronological_halves": halves,
                          "hypothesised_sign": sign, "test_share_long": p_long,
                          "independent_test_episodes": len(test), "independent_reference_episodes": len(ref),
                          "by_regime": _by_regime(test, regime_of) if regime_of else None,
                          "period": [iso(min(r["t"] for r in test)), iso(max(r["t"] for r in test))] if test else None,
                          "days": len({r["t"] // (24 * H) for r in test + ref})}
    return out


def _by_regime(rows, regime_of):
    out = {}
    for r in rows:
        out.setdefault(regime_of(r["t"]), []).append(r["y"])
    return {k: stats.describe(v) for k, v in sorted(out.items())}


def status(design, evaluation, superseded=False):
    if superseded:
        return "retired", "superseded by a newer design version"
    h = str(design["outcome"]["primary_horizon"])
    s = evaluation.get(h) if evaluation else None
    if not s or s["independent_test_episodes"] == 0:
        return "exploratory", "no evaluation episodes yet"
    sign, need = s["hypothesised_sign"], design["min_independent_episodes"]
    d, r = s["diff_test_minus_reference_90"], s["residual_90"]
    if s["independent_test_episodes"] < need:
        return "under prospective evaluation", f"{s['independent_test_episodes']}/{need} independent evaluation episodes"
    def excludes(ci):
        return ci and ((sign < 0 and ci["hi90"] < 0) or (sign > 0 and ci["lo90"] > 0))
    def wrong(ci):
        return ci and ((sign < 0 and ci["lo90"] > 0) or (sign > 0 and ci["hi90"] < 0))
    halves = s["chronological_halves"]
    resid_ok = excludes(r) if design.get("baseline_predictors") else True
    if excludes(d) and resid_ok and halves and all(x is not None and x * sign > 0 for x in halves):
        return "supported", "evaluation criteria met at the primary horizon"
    if wrong(d):
        return "retired", "evaluation interval lies on the wrong side of zero"
    return "under prospective evaluation", "minimum count reached; criteria not met"


def run_design(lab, design, module, registered, superseded=False):
    """Run every variant of a design; returns the experiment result and ledger rows."""
    horizons = design["outcome"]["horizons_min"]
    funding = lab.store.funding_events()
    snaps = lab.store.snaps()
    variants, ledger = [], []
    for variant in design["variants"]:
        res = module.run(lab, variant["params"])
        vout = {"name": variant["name"], "params": variant["params"], "passes": []}
        for p in res["passes"]:
            heads = collapse([dict(e) for e in p["events"]], design["collapse_ms"])
            controls = [dict(c, episode_head=True, episode_size=1) for c in p["controls"]]
            if design["comparison"]["reference_group"] == "control":
                controls += [dict(c, group=g, direction=dr, event_id=c["event_id"] + suffix)
                             for c in p["controls"] for g, dr, suffix in (("control_long", 1, "L"), ("control_short", -1, "S"))]
            labelled, immature, incomplete = label_all(heads + controls, p["bars"], lab.now, horizons, funding,
                                                       snaps if p["basis"] == "prospective" else ())
            reg = regime_fn(p["bars"])
            phases = {"exploratory": summarize(labelled, design, registered, "exploratory", p["basis"], reg)}
            if p["basis"] == "prospective":
                phases["evaluation"] = summarize(labelled, design, registered, "evaluation", regime_of=reg)
                if lab.write and variant["name"] == design["primary_variant"]:
                    persist(lab, design, variant, labelled)
            vout["passes"].append({"basis": p["basis"], "state": p["state"], "reasons": p["reasons"],
                                   "coverage": p["coverage"], "firings": len(p["events"]), "episodes": len(heads),
                                   "controls": len(controls), "immature_labels": immature,
                                   "incomplete_labels": incomplete, "data_sha256": p.get("data_sha256"),
                                   "phases": phases,
                                   "window": [iso(min(p["bars"])) if p["bars"] else None,
                                              iso(max(p["bars"])) if p["bars"] else None]})
            ledger.append({"t": lab.now, "design": design["id"], "design_sha256": design["_sha256"],
                           "variant": variant["name"], "basis": p["basis"], "family": design["family"],
                           "episodes": len(heads), "primary": phases.get("evaluation", phases["exploratory"]).get(
                               str(design["outcome"]["primary_horizon"]), {}).get("diff_test_minus_reference_90"),
                           "lab_version": LAB_VERSION})
        variants.append(vout)
    primary = next(v for v in variants if v["name"] == design["primary_variant"])
    prospective = next((p for p in primary["passes"] if p["basis"] == "prospective"), None)
    st, why = status(design, prospective["phases"].get("evaluation") if prospective else None, superseded)
    return {"t": lab.now, "design": design["id"], "design_sha256": design["_sha256"], "registered": registered,
            "module": design["module"], "status": st, "status_reason": why, "variants": variants,
            "lab_version": LAB_VERSION, "code_sha256": lab.code, "cost_model": outcomes.COST_MODEL}, ledger


def persist(lab, design, variant, labelled):
    """Store detector event records (features included) and their complete outcome labels
    (idempotent; first write wins). Scheduled controls are not stored: they are a deterministic
    function of the schedule and the stored bars, and are recomputed on every run."""
    evs, outs = [], []
    for e, lab_out in labelled:
        if e["group"].startswith("control"):
            continue
        evs.append(dict(e, design=design["id"], variant=variant["name"]))
        for h, v in lab_out.items():
            if v["status"] == "complete":
                outs.append({"t_event": e["t_event"], "event_id": e["event_id"], "design": design["id"],
                             "variant": variant["name"], "horizon_min": int(h), "group": e["group"],
                             "direction": e["direction"], "t_available": e["t_available"], "label": v,
                             "cost_model": outcomes.COST_MODEL["version"], "lab_version": LAB_VERSION})
    n_e = append(lab.base, f"research/events/{design['id']}", evs,
                 key=lambda r: (r["event_id"], r.get("variant"), r.get("detector_version")))
    n_o = append(lab.base, f"research/outcomes/{design['id']}", outs,
                 key=lambda r: (r["event_id"], r["variant"], r["horizon_min"], r["cost_model"]))
    return n_e, n_o
