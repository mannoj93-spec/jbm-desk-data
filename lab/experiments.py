"""Versioned designs, sample accounting, out-of-sample baselines and promotion (lab-2.0).

EVALUATION VERSION. A design is evaluated under a version id that binds the design JSON to the
semantic implementation (lab/versioning.py). The first lab run that sees a version id stamps its
registration time in state/lab_registrations.json (never rewritten). A code-only change to the
detector, labels, costs, baseline or evaluation rules is a new version with a new clock; data
commits and documentation edits are not.

PHASES of a prospective (as-of replay) pass:
  reanalysis   decisions available before this version was registered: collected data re-read
               under this version's logic. Never evidence of prospective performance.
  evaluation   decisions available at or after registration AND frozen by a lab run
               (t_persisted). A decision first computed after a lab run had already covered its
               decision time (it appeared only because inputs arrived late) is a late replay and is
               excluded. A frozen decision stands even if later data would change it.
A reconstruction pass (history fetched later) is exploratory only.

SAMPLE ACCOUNTING, per group and horizon, all visible on the card:
  firings      raw detector firings
  episodes     firings collapsed per the design's collapse window (the decision unit)
  scorable     episodes whose label at this horizon is complete (immature/incomplete excluded)
  retained     scorable observations kept after deterministic thinning on their ACTUAL label
               intervals [entry_t, exit_t) (stats.nonoverlap_intervals); identical entries count once
  blocks       dependence blocks over the retained test AND reference observations together: label
               intervals that overlap, or entries on the same UTC day, share a block; intervals are
               bootstrapped by block, so cross-group and same-day dependence is preserved
Retained observations are "non-overlapping", never called independent.

REFERENCE. Either another event group, or scheduled controls labelled in both directions and
combined with the test group's long share: reference = p_long x long outcome + (1 - p_long) x
short outcome at each control time.

BASELINE (lab/baseline.py). Out-of-sample: predictions from an OLS fit on controls whose labels
matured before the prediction's UTC day; added value = test residuals minus reference residuals.

PROMOTION ("supported") requires, at a scheduled look, ALL of:
  data quality    the pass is "available"; incomplete labels <= 10% of scorable ones; the primary
                  variant is not descriptive-only
  maturity/count  retained test observations >= min_retained_observations and test-bearing
                  dependence blocks >= min_dependence_blocks
  looks           evaluated only at checkpoints of 1, 1.5, 2 and 3 x min_retained_observations, on
                  the first N retained test observations (no continuous peeking)
  effect          the multiplicity-adjusted interval of test - reference excludes zero in the
                  hypothesised direction; alpha = 0.10 / (variants tried in the family x 4 looks)
                  (Bonferroni; the variant count includes every version and the legacy lab-1.0)
  baseline        the baseline is identifiable for >= 80% of retained test observations and the
                  adjusted interval of the residual difference excludes zero the same way
  comparability   for event-group references, median severity within 25% between the groups
  stability       the same sign in both chronological halves of the look sample
A look whose adjusted effect interval lies wholly on the wrong side retires the version.
"supported" means these descriptive criteria were met on prospective replays; it is not a claim of
significance or of profitability, and it is the only status that allows a skill-change proposal.
"""
import hashlib
import json
from pathlib import Path

from lab import outcomes, stats, versioning
from lab.asof import Known
from lab.baseline import FEATURES, Baseline, features_at
from lab.common import DAY, H, LAB_VERSION, MINUTE, ROOT, append, atomic_json, iso, read_dir, read_json
from lab.events import collapse

REGISTRY = "state/lab_registrations.json"
LOOKS = (1.0, 1.5, 2.0, 3.0)
ALPHA = 0.10
STATUS_RULES = {
    "exploratory": "not registered, no evaluation observations yet, or reconstruction-only evidence",
    "under prospective evaluation": "registered; evaluation observations accumulating, or a look did not meet "
                                    "every promotion criterion",
    "supported": "at a scheduled look every promotion criterion held (data quality, counts, adjusted effect, "
                 "out-of-sample baseline added value, comparability, stability) - see lab/experiments.py",
    "retired": "superseded version, or a look's adjusted effect interval lay wholly on the wrong side",
    "blocked": "evaluation cannot be identified: a required input (baseline, quality) is missing",
}


def design_files(base):
    return sorted((Path(base) / "lab/designs").glob("*.json"))


def load_design(path):
    raw = Path(path).read_bytes()
    d = json.loads(raw)
    d["_sha256"] = hashlib.sha256(raw).hexdigest()
    d["_file"] = "lab/designs/" + Path(path).name
    return d


def attach_version(base, design):
    """The version binds the design file (read from `base`) to the code that is actually running
    (hashed from this checkout's ROOT, not from a data directory)."""
    comp = versioning.components(ROOT, design)
    design["_components"] = comp
    design["_version"] = versioning.version_id(comp)
    return design


def register(base, designs, now, write=True):
    """{design id: registration record} for each design's CURRENT version; stamps new versions."""
    path = Path(base) / REGISTRY
    reg = read_json(path, {})
    changed = False
    out = {}
    for d in designs:
        key = f"{d['id']}@{d['_version']}"
        if key not in reg:
            reg[key] = {"design": d["id"], "version": d["_version"], "registered": now,
                        "design_sha256": d["_sha256"], "components": d["_components"], "lab_version": LAB_VERSION}
            changed = True
        out[d["id"]] = reg[key]
    if changed and write:
        atomic_json(path, reg)
    return out


def superseded_versions(base, design_id, current):
    reg = read_json(Path(base) / REGISTRY, {})
    return sorted(v["version"] for k, v in reg.items() if v["design"] == design_id and v["version"] != current)


def ns(design):
    return f"research/v2/{design['id']}/{design['_version']}"


# ---- labelling ----------------------------------------------------------------------------------
def label_all(obs, bars, now, horizons, funding, snaps, known_funding):
    """[(event, {h: label}, baseline_features)] plus counts of immature/incomplete labels."""
    out, immature, incomplete = [], 0, 0
    for e in obs:
        hs = None
        if snaps and e["basis"].startswith("as-of"):
            hs, _ = outcomes.half_spread_bp(snaps, e["t_available"])
        lab = outcomes.label(e["t_available"], e["direction"], bars, now, horizons, funding, hs)
        immature += sum(1 for v in lab.values() if v["status"] == "immature")
        incomplete += sum(1 for v in lab.values() if v["status"] == "incomplete")
        out.append((e, lab, features_at(bars, known_funding, e["t_available"], e["direction"])))
    return out, immature, incomplete


def _in_phase(e, phase, registered):
    """Phase membership of an event or control (see PHASES)."""
    reg = registered["registered"] if registered else None
    if phase == "exploratory":
        return True
    if e.get("live_status") == "late_replay":
        return False
    if phase == "reanalysis":
        return reg is None or e["t_available"] < reg
    if reg is None or e["t_available"] < reg:
        return False
    return e["group"].startswith("control") or e.get("t_persisted") is not None


def _rows(labelled, groups, h, phase, registered):
    items = []
    for e, lab, bf in labelled:
        if e["group"] not in groups or not _in_phase(e, phase, registered):
            continue
        v = lab.get(h) or lab.get(str(h))
        if not v or v["status"] != "complete":
            continue
        items.append(dict(bf or {k: None for k in FEATURES}, entry_t=v["entry_t"], exit_t=v["exit_t"], y=v["ret_net"],
                          d=e["direction"], t_event=e["t_event"], event_id=e["event_id"],
                          severity=(e.get("features") or {}).get("severity")))
    return items


def _counts(labelled, groups, h, phase, registered, raw_firings):
    eps = [e for e, lab, _ in labelled if e["group"] in groups and _in_phase(e, phase, registered)]
    comp = [e for e, lab, _ in labelled if e["group"] in groups and _in_phase(e, phase, registered)
            and (lab.get(h) or {}).get("status") == "complete"]
    return {"firings": sum(raw_firings.get(g, 0) for g in groups), "episodes": len(eps), "scorable": len(comp)}


def _combine_controls(longs, shorts, w):
    by_s = {r["t_event"]: r for r in shorts}
    out = []
    for r in longs:
        s = by_s.get(r["t_event"])
        if s is None:
            continue
        out.append(dict(r, y=w * r["y"] + (1 - w) * s["y"], _long=r, _short=s, event_id=r["event_id"]))
    return out


def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def summarize(labelled, design, registered, phase, raw_firings, baseline, n_variants, regime_of=None):
    test_g = design["comparison"]["test_group"]
    test_g = set(test_g) if isinstance(test_g, list) else {test_g}
    ref_g = design["comparison"]["reference_group"]
    sign = design["comparison"]["hypothesised_sign"]
    adj = ALPHA / max(1, n_variants * len(LOOKS))
    out = {}
    for h in design["outcome"]["horizons_min"]:
        test_all = _rows(labelled, test_g, h, phase, registered)
        test, test_drop = stats.nonoverlap_intervals(test_all)
        p_long = sum(1 for r in test if r["d"] > 0) / len(test) if test else 0.5
        if ref_g == "control":
            ref_all = _combine_controls(_rows(labelled, {"control_long"}, h, phase, registered),
                                        _rows(labelled, {"control_short"}, h, phase, registered), p_long)
            ref_counts = _counts(labelled, {"control_long"}, h, phase, registered, raw_firings)
        else:
            ref_all = _rows(labelled, {ref_g}, h, phase, registered)
            ref_counts = _counts(labelled, {ref_g}, h, phase, registered, raw_firings)
        ref, ref_drop = stats.nonoverlap_intervals(ref_all)
        n_blocks = stats.dependence_blocks(test + ref)
        test_blocks = len({r["block"] for r in test})
        diff = stats.block_bootstrap(test, ref, alphas=(ALPHA, adj))
        # out-of-sample baseline residuals
        def resid(rows, combined=False):
            got, missing = [], {}
            for r in rows:
                if combined:
                    pl, el = baseline.predict(r["_long"])
                    ps, es = baseline.predict(r["_short"])
                    p, err = (p_long * pl + (1 - p_long) * ps, None) if pl is not None and ps is not None else (None, el or es)
                else:
                    p, err = baseline.predict(r)
                if p is None:
                    missing[err] = missing.get(err, 0) + 1
                    continue
                got.append(dict(r, y=r["y"] - p))
            return got, missing
        rt, miss_t = resid(test)
        rr, miss_r = resid(ref, combined=(ref_g == "control"))
        rdiff = stats.block_bootstrap(rt, rr, alphas=(ALPHA, adj))
        halves = None
        if n_blocks >= 4 and test and ref:
            cut = n_blocks // 2
            h1 = (_mean([r["y"] for r in test if r["block"] < cut]), _mean([r["y"] for r in ref if r["block"] < cut]))
            h2 = (_mean([r["y"] for r in test if r["block"] >= cut]), _mean([r["y"] for r in ref if r["block"] >= cut]))
            halves = [None if None in h1 else h1[0] - h1[1], None if None in h2 else h2[0] - h2[1]]
        sev = None
        if ref_g != "control":
            st = sorted(r["severity"] for r in test if r["severity"] is not None)
            sr = sorted(r["severity"] for r in ref if r["severity"] is not None)
            sev = {"test_median": st[len(st) // 2] if st else None, "reference_median": sr[len(sr) // 2] if sr else None}
        reg_split = None
        if regime_of:
            reg_split = {}
            for r in test:
                reg_split.setdefault(regime_of(r["entry_t"]), []).append(r["y"])
            reg_split = {k: stats.describe(v) for k, v in sorted(reg_split.items())}
        out[str(h)] = {
            "counts": {"test": dict(_counts(labelled, test_g, h, phase, registered, raw_firings),
                                    retained=len(test), dropped_overlap=test_drop, blocks=test_blocks),
                       "reference": dict(ref_counts, retained=len(ref), dropped_overlap=ref_drop,
                                         blocks=len({r["block"] for r in ref})),
                       "dependence_blocks": n_blocks},
            "test": stats.describe([r["y"] for r in test]), "reference": stats.describe([r["y"] for r in ref]),
            "test_share_long": p_long if test else None,
            "diff_test_minus_reference": {"alpha_0.10": diff[ALPHA] if diff else None,
                                          "adjusted": diff[adj] if diff else None, "adjusted_alpha": adj},
            "baseline": {"method": "OLS on controls matured before each UTC day (out-of-sample)",
                         "predictors": list(FEATURES), "test_residual": stats.describe([r["y"] for r in rt]),
                         "reference_residual": stats.describe([r["y"] for r in rr]),
                         "identifiable_share_test": len(rt) / len(test) if test else None,
                         "unidentified": {"test": miss_t, "reference": miss_r},
                         "residual_diff": {"alpha_0.10": rdiff[ALPHA] if rdiff else None,
                                           "adjusted": rdiff[adj] if rdiff else None}},
            "chronological_halves": halves, "severity": sev, "by_regime": reg_split,
            "hypothesised_sign": sign,
            "period": [iso(test[0]["entry_t"]), iso(test[-1]["entry_t"])] if test else None,
            "_test": test, "_ref": ref,
        }
    return out


def _excludes(ci, sign):
    return ci is not None and ((sign < 0 and ci[1] < 0) or (sign > 0 and ci[0] > 0))


def _wrong(ci, sign):
    return ci is not None and ((sign < 0 and ci[0] > 0) or (sign > 0 and ci[1] < 0))


def evaluate_look(design, summary_h, n, baseline, n_variants):
    """Promotion checks on the first n retained test observations (chronological)."""
    sign = design["comparison"]["hypothesised_sign"]
    adj = ALPHA / max(1, n_variants * len(LOOKS))
    test = summary_h["_test"][:n]
    cutoff = test[-1]["exit_t"]
    ref = [r for r in summary_h["_ref"] if r["entry_t"] < cutoff]
    blocks = stats.dependence_blocks(test + ref)
    test_blocks = len({r["block"] for r in test})
    diff = stats.block_bootstrap(test, ref, alphas=(adj,))
    p_long = sum(1 for r in test if r["d"] > 0) / len(test)

    def res(rows, combined):
        out = []
        for r in rows:
            if combined:
                pl, _ = baseline.predict(r["_long"])
                ps, _ = baseline.predict(r["_short"])
                p = p_long * pl + (1 - p_long) * ps if pl is not None and ps is not None else None
            else:
                p, _ = baseline.predict(r)
            if p is not None:
                out.append(dict(r, y=r["y"] - p))
        return out
    combined = design["comparison"]["reference_group"] == "control"
    rt, rr = res(test, False), res(ref, combined)
    rdiff = stats.block_bootstrap(rt, rr, alphas=(adj,))
    cut = blocks // 2
    halves = [_mean([r["y"] for r in test if r["block"] < cut]), _mean([r["y"] for r in ref if r["block"] < cut]),
              _mean([r["y"] for r in test if r["block"] >= cut]), _mean([r["y"] for r in ref if r["block"] >= cut])]
    same_sign = None not in halves and (halves[0] - halves[1]) * sign > 0 and (halves[2] - halves[3]) * sign > 0
    checks = {
        "blocks": {"ok": test_blocks >= design.get("min_dependence_blocks", 20),
                   "value": test_blocks, "need": design.get("min_dependence_blocks", 20)},
        "effect_adjusted": {"ok": _excludes(diff[adj] if diff else None, sign), "interval": diff[adj] if diff else None,
                            "alpha": adj},
        "baseline_identifiable": {"ok": len(rt) >= 0.8 * len(test), "share": len(rt) / len(test)},
        "baseline_added_value": {"ok": _excludes(rdiff[adj] if rdiff else None, sign),
                                 "interval": rdiff[adj] if rdiff else None},
        "stability": {"ok": same_sign, "halves": halves},
    }
    sev = summary_h.get("severity")
    if sev is not None:
        a, b = sev.get("test_median"), sev.get("reference_median")
        ok = a is not None and b not in (None, 0) and abs(a / b - 1) <= design.get("severity_balance_max", 0.25)
        checks["comparability"] = {"ok": ok, "test_median": a, "reference_median": b}
    wrong = _wrong(diff[adj] if diff else None, sign)
    return checks, wrong


def status(design, pass_state, summary_eval, quality, baseline, n_variants, superseded=False):
    """(status, reason, look record)."""
    if superseded:
        return "retired", "superseded by a newer evaluation version", None
    h = str(design["outcome"]["primary_horizon"])
    s = (summary_eval or {}).get(h)
    retained = s["counts"]["test"]["retained"] if s else 0
    if not s or retained == 0:
        return "exploratory", "no evaluation observations yet", None
    if design.get("descriptive_only"):
        return "blocked", "descriptive-only design: not eligible for promotion", None
    if pass_state != "available":
        return "under prospective evaluation", f"data state {pass_state}; promotion requires 'available'", None
    if quality.get("incomplete_share", 0) > 0.10:
        return "blocked", f"{quality['incomplete_share']:.0%} of labels incomplete (missing bars); limit 10%", None
    need = design["min_retained_observations"]
    points = [int(need * f) for f in LOOKS]
    done = [p for p in points if retained >= p]
    if not done:
        return "under prospective evaluation", f"{retained}/{need} retained test observations before the first look", None
    last = None
    for n in done:
        checks, wrong = evaluate_look(design, s, n, baseline, n_variants)
        last = {"n": n, "checks": checks}
        if wrong:
            return "retired", f"look at n={n}: adjusted effect interval wholly on the wrong side", last
        if all(c["ok"] for c in checks.values()):
            return "supported", f"every promotion criterion met at the look n={n}", last
    missing = [k for k, c in last["checks"].items() if not c["ok"]]
    if "baseline_identifiable" in missing:
        return "blocked", "baseline not identifiable for enough observations", last
    nxt = next((p for p in points if p > retained), None)
    return ("under prospective evaluation",
            f"look n={last['n']} failed: {', '.join(missing)}" + (f"; next look at {nxt}" if nxt else "; no looks left"),
            last)


# ---- running a design ---------------------------------------------------------------------------
def regime_fn(bars):
    """Descriptive regime label at t: trailing-24h realised volatility above/below the window median
    and trailing-24h return sign. The median uses the whole window, so it is descriptive only."""
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


def load_frozen(base, design):
    return {e["decision_key"]: e for e in read_dir(base, f"{ns(design)}/events")}


def freeze(lab, design, events, frozen, last_cutoff):
    """Merge recomputed firings with frozen decisions (see PHASES). Returns (merged, new, audit)."""
    merged, new = [], []
    audit = {"frozen_used": 0, "revised_since_frozen": 0, "not_reproduced": 0, "late_replay": 0, "new": 0}
    seen = set()
    for e in events:
        k = e["decision_key"]
        seen.add(k)
        f = frozen.get(k)
        if f is not None:
            if (f["group"], f["features"]) != (e["group"], e["features"]):
                audit["revised_since_frozen"] += 1
            audit["frozen_used"] += 1
            merged.append(dict(f))
        elif last_cutoff is not None and e["t_available"] <= last_cutoff:
            audit["late_replay"] += 1
            merged.append(dict(e, live_status="late_replay"))
        else:
            e = dict(e, t_persisted=lab.now, decision_lag_ms=lab.now - e["t_available"])
            audit["new"] += 1
            merged.append(e)
            new.append(e)
    for k, f in frozen.items():
        if k not in seen:
            audit["not_reproduced"] += 1
            merged.append(dict(f))
    return merged, new, audit


def run_design(lab, design, module, registration, n_variants, superseded=False, run_state=None):
    """Run every variant; returns (result, ledger rows). Persists frozen decisions and outcomes of the
    primary variant's prospective pass when lab.write."""
    horizons = design["outcome"]["horizons_min"]
    funding = lab.store.funding_events()
    known = Known(lab.store.funding_known())
    known_assumed = Known([(t, r, t) for t, r, _ in lab.store.funding_known()])
    snaps = lab.store.snaps()
    last_cutoff = (run_state or {}).get("last_cutoff")
    variants, ledger, audits = [], [], {}
    for variant in design["variants"]:
        res = module.run(lab, variant["params"])
        vout = {"name": variant["name"], "params": variant["params"], "descriptive": bool(variant.get("descriptive")),
                "passes": []}
        for p in res["passes"]:
            events = [dict(e) for e in p["events"]]
            primary_pro = variant["name"] == design["primary_variant"] and p["basis"] == "prospective"
            audit = None
            if primary_pro:
                events, new, audit = freeze(lab, design, events, load_frozen(lab.base, design), last_cutoff)
                audits[p["basis"]] = audit
            raw = {}
            for e in events:
                raw[e["group"]] = raw.get(e["group"], 0) + 1
            heads = collapse(events, design["collapse_ms"],
                             key=lambda e: (e["detector"], e["direction"], e.get("live_status")))
            controls = [dict(c, group=g, direction=dr, event_id=c["event_id"] + sfx, episode_head=True, episode_size=1)
                        for c in p["controls"] for g, dr, sfx in (("control_long", 1, "L"), ("control_short", -1, "S"))]
            raw["control_long"] = len(controls) // 2
            is_pro = p["basis"] == "prospective"
            labelled, immature, incomplete = label_all(heads + controls, p["bars"], lab.now, horizons, funding,
                                                       snaps if is_pro else (), known if is_pro else known_assumed)
            ctl_train = []
            for e, labs, bf in labelled:
                if e["group"].startswith("control") and bf:
                    v = labs.get(design["outcome"]["primary_horizon"])
                    if v and v["status"] == "complete":
                        ctl_train.append(dict(bf, entry_t=v["entry_t"], exit_t=v["exit_t"], y=v["ret_net"]))
            baseline = Baseline(ctl_train)
            reg = regime_fn(p["bars"])
            scorable = sum(1 for _, labs, _ in labelled for v in labs.values() if v["status"] != "immature")
            quality = {"incomplete_share": incomplete / scorable if scorable else 0.0,
                       "immature_labels": immature, "incomplete_labels": incomplete}
            if is_pro:
                phases = {"reanalysis": summarize(labelled, design, registration, "reanalysis", raw, baseline, n_variants, reg),
                          "evaluation": summarize(labelled, design, registration, "evaluation", raw, baseline, n_variants, reg)}
            else:
                phases = {"exploratory": summarize(labelled, design, None, "exploratory", raw, baseline, n_variants, reg)}
            if primary_pro and lab.write:
                persist(lab, design, variant, events, labelled)
            st = None
            if primary_pro:
                st = status(design, p["state"], phases["evaluation"], quality, baseline, n_variants, superseded)
            vout["passes"].append({"basis": p["basis"], "state": p["state"], "reasons": p["reasons"],
                                   "coverage": p["coverage"], "firings": sum(v for k, v in raw.items() if k != "control_long"),
                                   "episodes": len(heads), "controls": len(controls) // 2, "quality": quality,
                                   "freeze_audit": audit, "data_sha256": p.get("data_sha256"), "phases": phases,
                                   "status": st,
                                   "window": [iso(min(p["bars"])) if p["bars"] else None,
                                              iso(max(p["bars"])) if p["bars"] else None]})
            prim = phases.get("evaluation", phases.get("exploratory")).get(str(design["outcome"]["primary_horizon"]), {})
            ledger.append({"t": lab.now, "design": design["id"], "version": design["_version"],
                           "design_sha256": design["_sha256"], "variant": variant["name"], "basis": p["basis"],
                           "family": design["family"], "episodes": len(heads),
                           "retained_test": ((prim.get("counts") or {}).get("test") or {}).get("retained"),
                           "diff_alpha_0.10": (prim.get("diff_test_minus_reference") or {}).get("alpha_0.10"),
                           "lab_version": LAB_VERSION})
        variants.append(vout)
    primary = next(v for v in variants if v["name"] == design["primary_variant"])
    pro = next((p for p in primary["passes"] if p["basis"] == "prospective"), None)
    st, why, look = pro["status"] if pro and pro["status"] else ("exploratory", "no prospective pass", None)
    return {"t": lab.now, "design": design["id"], "version": design["_version"], "design_sha256": design["_sha256"],
            "registered": registration["registered"] if registration else None, "module": design["module"],
            "status": st, "status_reason": why, "look": look, "variants": variants, "lab_version": LAB_VERSION,
            "code_sha256": lab.code, "cost_model": outcomes.COST_MODEL, "n_variants_family": n_variants}, ledger


def persist(lab, design, variant, firings, labelled):
    """Frozen decisions - every firing, head or not (first write wins, keyed by decision_key) - and
    the complete outcome labels of episode heads, under the version namespace. Late replays and
    controls are not stored."""
    evs, outs = [], []
    for e in firings:
        if e.get("live_status") == "late_replay" or e.get("t_persisted") is None:
            continue
        evs.append({k: v for k, v in dict(e, design=design["id"], version=design["_version"],
                                          variant=variant["name"]).items()
                    if k not in ("episode_id", "episode_head", "episode_size")})
    for e, labs, _ in labelled:
        if e["group"].startswith("control") or e.get("live_status") == "late_replay" or e.get("t_persisted") is None:
            continue
        for h, v in labs.items():
            if v["status"] == "complete":
                outs.append({"t_event": e["t_event"], "event_id": e["event_id"], "decision_key": e["decision_key"],
                             "design": design["id"], "version": design["_version"], "variant": variant["name"],
                             "horizon_min": int(h), "group": e["group"], "direction": e["direction"],
                             "t_available": e["t_available"], "label": v,
                             "cost_model": outcomes.COST_MODEL["version"], "lab_version": LAB_VERSION})
    n_e = append(lab.base, f"{ns(design)}/events", evs, key=lambda r: (r["decision_key"],))
    n_o = append(lab.base, f"{ns(design)}/outcomes", outs,
                 key=lambda r: (r["decision_key"], r["horizon_min"], r["cost_model"]))
    return n_e, n_o
