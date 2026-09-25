"""Versioned designs, sample accounting, out-of-sample baselines and recorded checkpoints (lab-2.1).

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

BASELINE (lab/baseline.py). One model per horizon, fitted on same-horizon control labels that were
available before the prediction's UTC day (and before a checkpoint's cutoff); added value = test
residuals minus reference residuals. A horizon without an identifiable baseline has no comparison.

CHECKPOINTS (lab-2.1). A verdict is only ever produced at a scheduled look, from a precisely bounded
dataset (checkpoint_sample): cutoff C = the earliest time at which the look's n retained test
observations were known (outcome available and decision frozen); test, reference, direction mix,
severity, blocks, baseline training rows and predictions, data quality and the multiplicity count
are all as of C. The look's manifest (every input row, prediction and criterion), its sha256, the
checks and the verdict are appended to research/v2/<design>/<version>/checkpoints.jsonl the first
time the look completes and are never recomputed: later data can be audited against the record
(drift) but never changes it. A look is PENDING until its n observations are known. Correcting a
completed checkpoint needs a new evaluation version (any semantic code or design change produces
one), which keeps the old version's records untouched.

PROMOTION ("supported") requires, at a scheduled look, ALL of:
  data quality    incomplete labels <= 10% of the test labels that ended by the cutoff; the design is
                  not descriptive-only
  maturity/count  retained test observations >= min_retained_observations and test-bearing
                  dependence blocks >= min_dependence_blocks
  looks           evaluated only at checkpoints of 1, 1.5, 2 and 3 x min_retained_observations, on
                  the first N retained test observations known by the cutoff (no continuous peeking)
  effect          the multiplicity-adjusted interval of test - reference excludes zero in the
                  hypothesised direction; alpha = 0.10 / (variants tried in the family x 4 looks)
                  (Bonferroni; the variant count, as of the cutoff, includes every version and the legacy lab-1.0)
  baseline        the baseline is identifiable for >= 80% of retained test observations and the
                  adjusted interval of the residual difference excludes zero the same way
  comparability   for event-group references, median severity within 25% between the groups
  stability       the same sign in both chronological halves of the look sample
A look whose adjusted effect interval lies wholly on the wrong side retires the version.

INPUT INTEGRITY (revision 2.12). A design whose comparison observations come from the hourly
collection-time control policy (HOURLY_CONTROL_MODULES, or any pass reporting that policy) is
evaluated only when input_integrity() passes on the primary prospective pass: the control policy
reports no unresolved conflict and no ready-but-unselected closed hour, a writing run's controls
equal the stored selections, and every labelled control equals the selection it came from
(controls.evidence_agreement), all checked AFTER labelling and BEFORE anything is persisted. A
failed or incomplete check BLOCKS the evaluation: no frozen decision or outcome is persisted, no
checkpoint look is computed or recorded (an earlier record is shown as history, never as the
current result), the status is "blocked" with the reasons, and lab/run.py does not advance the
design's watermark, so a later valid run evaluates the same observations as new (not as late
replays) and completes the unconsumed look. A recorded, re-verifying checkpoint cannot override
failed input integrity. Bar-based designs (controls at stored bar closes) have no such
requirement and report "not_required".
"supported" means these descriptive criteria were met on prospective replays; it is not a claim of
significance or of profitability, and it is the only status that allows a skill-change proposal.
"""
import hashlib
import json
from pathlib import Path

from storage import append_unique

from lab import controls as controls_mod
from lab import outcomes, stats, versioning
from lab.asof import Known
from lab import baseline as baseline_mod
from lab.baseline import FEATURES, Baseline, features_at
from lab.common import DAY, H, LAB_VERSION, MINUTE, ROOT, append, atomic_json, ceil_minute, iso, read_dir, read_json
from lab.events import collapse, collapse_as_known

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
                          label_available=v.get("label_available", v["exit_t"] + MINUTE),
                          known_at=max(v.get("label_available", v["exit_t"] + MINUTE), e.get("t_persisted") or 0),
                          d=e["direction"], t_event=e["t_event"], event_id=e["event_id"],
                          decision_key=e.get("decision_key"), severity=(e.get("features") or {}).get("severity")))
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


def summarize(labelled, design, registered, phase, raw_firings, baselines, n_variants, regime_of=None):
    """Descriptive per-horizon summary. `baselines` maps each horizon to its own Baseline (a single
    Baseline is accepted only for a one-horizon design). Verdicts never come from here: they come
    from recorded checkpoints (checkpoints())."""
    if not isinstance(baselines, dict):
        if len(design["outcome"]["horizons_min"]) != 1:
            raise ValueError("one baseline per horizon is required")
        baselines = {design["outcome"]["horizons_min"][0]: baselines}
    test_g = design["comparison"]["test_group"]
    test_g = set(test_g) if isinstance(test_g, list) else {test_g}
    ref_g = design["comparison"]["reference_group"]
    sign = design["comparison"]["hypothesised_sign"]
    adj = ALPHA / max(1, n_variants * len(LOOKS))
    out = {}
    for h in design["outcome"]["horizons_min"]:
        baseline = baselines.get(h)
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
            if baseline is None:
                return got, {"no baseline for this horizon": len(rows)}
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
            "baseline": {"method": "OLS on same-horizon controls known before each UTC day (out-of-sample)",
                         "model": baseline.describe() if baseline is not None else None,
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


# ---- checkpoints --------------------------------------------------------------------------------
CHECKPOINT_SCHEMA = "checkpoint/1"
TERMINAL = ("supported", "retired")


def checkpoint_sample(labelled, design, registered, n):
    """The precisely bounded dataset of a checkpoint that needs n retained test observations, or
    None while it is pending.

    Cutoff C = the earliest time at which n retained test observations were KNOWN: the smallest
    known_at (= max(label_available, t_persisted): the outcome was available AND the decision was
    frozen) such that the evaluation-phase test labels available by then retain >= n after
    interval thinning (all intervals of one horizon have equal length, so the retained count only
    grows as labels arrive). Everything else is bounded by C: reference or control labels
    available by C, the test group's direction mix, severity, dependence blocks, and the quality
    window (labels that ended by C). Nothing known after C can enter, so appending later
    observations - or changing later outcomes, directions, severities or controls - cannot change
    the sample."""
    h = design["outcome"]["primary_horizon"]
    test_g = design["comparison"]["test_group"]
    test_g = set(test_g) if isinstance(test_g, list) else {test_g}
    ref_g = design["comparison"]["reference_group"]
    rows = _rows(labelled, test_g, h, "evaluation", registered)
    times = sorted({r["known_at"] for r in rows})
    lo, hi, cut = 0, len(times) - 1, None
    while lo <= hi:                                              # smallest C with >= n retained
        mid = (lo + hi) // 2
        kept, _ = stats.nonoverlap_intervals([r for r in rows if r["known_at"] <= times[mid]])
        if len(kept) >= n:
            cut, hi = times[mid], mid - 1
        else:
            lo = mid + 1
    if cut is None:
        kept, _ = stats.nonoverlap_intervals(rows)
        return {"pending": True, "retained": len(kept), "need": n}
    test = [dict(r) for r in stats.nonoverlap_intervals([r for r in rows if r["known_at"] <= cut])[0][:n]]
    p_long = sum(1 for r in test if r["d"] > 0) / len(test)
    known = lambda rs: [dict(r) for r in rs if r["known_at"] <= cut]
    if ref_g == "control":
        ref_all = _combine_controls(known(_rows(labelled, {"control_long"}, h, "evaluation", registered)),
                                    known(_rows(labelled, {"control_short"}, h, "evaluation", registered)), p_long)
    else:
        ref_all = known(_rows(labelled, {ref_g}, h, "evaluation", registered))
    ref, _ = stats.nonoverlap_intervals(ref_all)
    ended = complete_known = 0                                   # quality window: test labels that ended by C
    for e, labs, _ in labelled:
        if e["group"] not in test_g or not _in_phase(e, "evaluation", registered):
            continue
        v = labs.get(h) or labs.get(str(h)) or {}
        end = v.get("exit_t") or (ceil_minute(e["t_available"]) + h * MINUTE)
        if end + MINUTE > cut or (e.get("t_persisted") or 0) > cut:
            continue
        ended += 1
        complete_known += v.get("status") == "complete" and v.get("label_available", end + MINUTE) <= cut
    return {"pending": False, "cutoff": cut, "test": test, "reference": ref, "p_long": p_long, "horizon": h,
            "quality": {"labels_ended_by_cutoff": ended, "complete_and_known": complete_known,
                        "incomplete_share": 1 - complete_known / ended if ended else 0.0}}


def _manifest_row(r, prediction, combined=False):
    row = {"key": r.get("decision_key") or r.get("event_id"), "t_event": r["t_event"], "entry_t": r["entry_t"],
           "exit_t": r["exit_t"], "label_available": r["label_available"], "known_at": r["known_at"],
           "y": r["y"], "d": r["d"],
           "severity": r.get("severity"), "prediction": prediction}
    if combined:
        row.update(y_long=r["_long"]["y"], y_short=r["_short"]["y"])
    return row


def build_manifest(design, sample, baseline, n_variants):
    """Everything a verdict depends on, with the out-of-sample predictions made as of the cutoff."""
    combined = design["comparison"]["reference_group"] == "control"
    p_long, cut = sample["p_long"], sample["cutoff"]
    reasons = {}

    def pred(r, comb):
        if baseline is None:
            reasons["no baseline for this horizon"] = reasons.get("no baseline for this horizon", 0) + 1
            return None
        if comb:
            pl, el = baseline.predict(r["_long"], cutoff=cut)
            ps, es = baseline.predict(r["_short"], cutoff=cut)
            if pl is None or ps is None:
                reasons[el or es] = reasons.get(el or es, 0) + 1
                return None
            return p_long * pl + (1 - p_long) * ps
        p, err = baseline.predict(r, cutoff=cut)
        if p is None:
            reasons[err] = reasons.get(err, 0) + 1
        return p
    return {"cutoff": cut, "horizon": sample["horizon"], "p_long": p_long, "quality": sample["quality"],
            "criteria": {"alpha": ALPHA, "n_variants": n_variants, "looks": len(LOOKS),
                         "adjusted_alpha": ALPHA / max(1, n_variants * len(LOOKS)),
                         "min_dependence_blocks": design.get("min_dependence_blocks", 20),
                         "severity_balance_max": design.get("severity_balance_max", 0.25),
                         "hypothesised_sign": design["comparison"]["hypothesised_sign"],
                         "severity_check": design["comparison"]["reference_group"] != "control",
                         "max_incomplete_share": 0.10, "min_baseline_share": 0.8},
            "baseline": dict(baseline.describe(cut) if baseline is not None else {"horizon_min": sample["horizon"]},
                             unidentified=reasons),
            "test": [_manifest_row(r, pred(r, False)) for r in sample["test"]],
            "reference": [_manifest_row(r, pred(r, combined), combined) for r in sample["reference"]]}


def evaluate_manifest(m):
    """(checks, verdict) from a manifest alone - so a recorded checkpoint can be re-verified."""
    c = m["criteria"]
    sign, adj = c["hypothesised_sign"], c["adjusted_alpha"]
    test = [dict(r) for r in m["test"]]
    ref = [dict(r) for r in m["reference"]]
    blocks = stats.dependence_blocks(test + ref)
    test_blocks = len({r["block"] for r in test})
    diff = stats.block_bootstrap(test, ref, alphas=(adj,))
    rt = [dict(r, y=r["y"] - r["prediction"]) for r in test if r["prediction"] is not None]
    rr = [dict(r, y=r["y"] - r["prediction"]) for r in ref if r["prediction"] is not None]
    rdiff = stats.block_bootstrap(rt, rr, alphas=(adj,))
    cut = blocks // 2
    halves = [_mean([r["y"] for r in test if r["block"] < cut]), _mean([r["y"] for r in ref if r["block"] < cut]),
              _mean([r["y"] for r in test if r["block"] >= cut]), _mean([r["y"] for r in ref if r["block"] >= cut])]
    same_sign = None not in halves and (halves[0] - halves[1]) * sign > 0 and (halves[2] - halves[3]) * sign > 0
    checks = {
        "quality": {"ok": m["quality"]["incomplete_share"] <= c["max_incomplete_share"], **m["quality"]},
        "blocks": {"ok": test_blocks >= c["min_dependence_blocks"], "value": test_blocks,
                   "need": c["min_dependence_blocks"]},
        "effect_adjusted": {"ok": _excludes(diff[adj] if diff else None, sign),
                            "interval": diff[adj] if diff else None, "alpha": adj},
        "baseline_identifiable": {"ok": len(rt) >= c["min_baseline_share"] * len(test), "share": len(rt) / len(test),
                                  "horizon_min": m["baseline"].get("horizon_min")},
        "baseline_added_value": {"ok": _excludes(rdiff[adj] if rdiff else None, sign),
                                 "interval": rdiff[adj] if rdiff else None},
        "stability": {"ok": same_sign, "halves": halves},
    }
    if c["severity_check"]:
        st = sorted(r["severity"] for r in test if r["severity"] is not None)
        sr = sorted(r["severity"] for r in ref if r["severity"] is not None)
        a = st[len(st) // 2] if st else None
        b = sr[len(sr) // 2] if sr else None
        checks["comparability"] = {"ok": a is not None and b not in (None, 0) and abs(a / b - 1) <= c["severity_balance_max"],
                                   "test_median": a, "reference_median": b}
    if _wrong(diff[adj] if diff else None, sign):
        verdict = "retired"
    elif all(x["ok"] for x in checks.values()):
        verdict = "supported"
    elif not checks["baseline_identifiable"]["ok"] or not checks["quality"]["ok"]:
        verdict = "blocked"
    else:
        verdict = "not_met"
    return checks, verdict


def manifest_sha(m):
    return hashlib.sha256(json.dumps(m, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_checkpoints(base, design):
    """Completed checkpoint records of this version, first record per look wins."""
    out = {}
    p = Path(base) / ns(design) / "checkpoints.jsonl"
    if p.exists():
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out.setdefault(r["look"], r)
    return out


def verify_checkpoint(record, design=None):
    """True when the stored manifest hashes to its recorded sha256, is internally consistent (n test
    rows, the record's cutoff, every row known by the cutoff, the adjusted alpha implied by its
    variant count and looks, the look's n for the design when given) and re-evaluates to the
    recorded verdict. The hash is tamper-EVIDENT against accidental change, not a signature: the
    repository history is the audit trail for deliberate edits."""
    m = record.get("manifest")
    if not m or manifest_sha(m) != record.get("manifest_sha256"):
        return False
    c = m.get("criteria") or {}
    try:
        ok = (record.get("n") == len(m["test"]) and record.get("cutoff") == m["cutoff"]
              and all(r["known_at"] <= m["cutoff"] for r in m["test"] + m["reference"])
              and abs(c["adjusted_alpha"] - c["alpha"] / max(1, c["n_variants"] * c["looks"])) < 1e-15
              and c["looks"] == len(LOOKS) and 1 <= record.get("look", 0) <= len(LOOKS))
        if ok and design is not None:
            ok = (record.get("n") == int(design["min_retained_observations"] * LOOKS[record["look"] - 1])
                  and record.get("version") == design["_version"] and m["horizon"] == design["outcome"]["primary_horizon"]
                  and c["hypothesised_sign"] == design["comparison"]["hypothesised_sign"])
    except (KeyError, TypeError):
        return False
    return ok and evaluate_manifest(m)[1] == record.get("verdict")


def _manifest_diff(a, b):
    """Which parts of two manifests differ (for the drift audit)."""
    out = {}
    for k in sorted(set(a) | set(b)):
        if k in ("test", "reference"):
            ra = {json.dumps(r, sort_keys=True) for r in a.get(k) or []}
            rb = {json.dumps(r, sort_keys=True) for r in b.get(k) or []}
            if ra != rb:
                out[k] = {"only_recorded": len(ra - rb), "only_current": len(rb - ra)}
        elif json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True):
            out[k] = "changed"
    return out


def checkpoints(lab, design, labelled, registered, baselines, variants_at, write):
    """Walk the scheduled looks in order. Completed looks come from the record and are never
    recomputed; the first look not yet recorded is computed from its bounded sample when that
    sample exists (and recorded), otherwise it is pending. A terminal verdict (supported /
    retired) ends the walk. Returns (records, pending, drift)."""
    done = load_checkpoints(lab.base, design)
    need = design["min_retained_observations"]
    h = design["outcome"]["primary_horizon"]
    records, pending, drift = [], None, []
    for k, factor in enumerate(LOOKS, 1):
        n = int(need * factor)
        rec = done.get(k)
        sample = checkpoint_sample(labelled, design, registered, n)
        if rec is not None:
            if not sample["pending"]:
                again = build_manifest(design, sample, baselines.get(h), rec["manifest"]["criteria"]["n_variants"])
                if manifest_sha(again) != rec["manifest_sha256"]:
                    drift.append({"look": k, "recorded_sha256": rec["manifest_sha256"], "current_sha256": manifest_sha(again),
                                  "differs": _manifest_diff(rec["manifest"], again),
                                  "note": "current data would give a different sample; the record stands"})
            else:
                drift.append({"look": k, "note": "the recorded sample is no longer reproducible from current data"})
            records.append(rec)
            if rec["verdict"] in TERMINAL:
                break
            continue
        if sample["pending"]:
            pending = {"look": k, "need": n, "retained": sample["retained"]}
            break
        m = build_manifest(design, sample, baselines.get(h), variants_at(sample["cutoff"]))
        checks, verdict = evaluate_manifest(m)
        rec = {"schema": CHECKPOINT_SCHEMA, "design": design["id"], "version": design["_version"], "look": k, "n": n,
               "cutoff": sample["cutoff"], "completed_at": lab.now, "lab_version": LAB_VERSION,
               "checks": checks, "verdict": verdict, "manifest": m, "manifest_sha256": manifest_sha(m)}
        if write:
            append_unique(Path(lab.base) / ns(design) / "checkpoints.jsonl", [rec], key=lambda r: (r["look"],))
            rec = load_checkpoints(lab.base, design).get(k, rec)      # a record already stored stands
            verdict = rec["verdict"]
        records.append(rec)
        if verdict in TERMINAL:
            break
    return records, pending, drift


def status(design, records, pending, superseded=False):
    """(status, reason) from recorded checkpoints only."""
    if superseded:
        return "retired", "superseded by a newer evaluation version"
    if design.get("descriptive_only"):
        return "blocked", "descriptive-only design: not eligible for promotion"
    for r in records:
        if r["verdict"] in TERMINAL and not verify_checkpoint(r, design):
            return "blocked", (f"checkpoint {r['look']} record fails re-verification (manifest hash or verdict); "
                               "no status is derived from it")
        if r["verdict"] == "supported":
            return "supported", f"checkpoint {r['look']} (n={r['n']}, cutoff {iso(r['cutoff'])}): every criterion met"
        if r["verdict"] == "retired":
            return "retired", f"checkpoint {r['look']} (n={r['n']}): adjusted effect interval wholly on the wrong side"
    if records:
        last = records[-1]
        missing = [k for k, c in last["checks"].items() if not c["ok"]]
        nxt = f"; next checkpoint needs {pending['need']} ({pending['retained']} so far)" if pending else "; no checkpoints left"
        st = "blocked" if last["verdict"] == "blocked" else "under prospective evaluation"
        return st, f"checkpoint {last['look']} {last['verdict']}: {', '.join(missing)} failed{nxt}"
    if pending and pending["retained"] > 0:
        return "under prospective evaluation", f"{pending['retained']}/{pending['need']} retained test observations before checkpoint 1"
    return "exploratory", "no evaluation observations yet"


# ---- input integrity (2.12) ----------------------------------------------------------------------
HOURLY_CONTROL_MODULES = ("account_behavior", "liq_exposure", "options_disagreement")
INTEGRITY_OK = ("passed", "not_required")


def evaluation_allowed(integrity):
    """THE publication rule shared by run_design (persist / checkpoints), lab/run.py (watermark,
    exit code, summary) and lab/evidence.py (card, report, proposals): an evaluation may be persisted
    and published only when its required input integrity passed or is not required. Missing ->
    not allowed."""
    return bool(integrity) and integrity.get("status") in INTEGRITY_OK


def next_run_state(prev, now, result):
    """The design version's evaluation watermark after a run (state/lab_run_state.json, read back as
    run_state["last_cutoff"] by freeze(), which marks decisions available by it as late replays).
    It advances only when the evaluation was allowed; a blocked run leaves it where it was, so the
    decisions that run saw are evaluated as new by the next valid run."""
    if not evaluation_allowed((result or {}).get("integrity")):
        return prev
    return {"last_cutoff": now, "runs": (prev or {}).get("runs", 0) + 1}


def input_integrity(lab, design, p, labelled):
    """Required-input integrity of a primary prospective pass, from the lab's own objects:
    the control policy diagnostics (p["coverage"]["comparison"]), the controls the pass used and the
    labels actually computed. status: not_required | passed | failed | incomplete; reasons name each
    failure. In a writing run the labelled controls must equal the STORED selections; in a read-only
    run, the controls the module returned (provisional)."""
    comp = (p.get("coverage") or {}).get("comparison")
    uses = design["module"] in HOURLY_CONTROL_MODULES or (comp or {}).get("policy") == controls_mod.POLICY
    out = {"required": uses, "policy": controls_mod.POLICY if uses else None, "status": "not_required",
           "reasons": [], "policy_failures": 0, "unresolved_conflicts": [], "ready_but_unselected": [],
           "evidence_agreement": None, "used_equals_stored": None, "controls_fingerprint": None,
           "stored_fingerprint": None, "ok": True}
    if not uses:
        return out
    reasons = []
    if not comp or comp.get("policy") != controls_mod.POLICY:
        reasons.append("incomplete: the pass reported no hourly control-policy diagnostics")
        return dict(out, status="incomplete", reasons=reasons, ok=False)
    windowed = comp.get("window") is not None
    unresolved = comp.get("unresolved_conflicts") or [] if windowed else []
    ready = comp.get("closed_hours_with_candidates_but_no_control") or [] if windowed else []
    # a malformed stored record is a conflict in a read-only replay too (a writing run already lists it
    # as unresolved); only "persisted after this cutoff" / "later stored selection differs" are
    # legitimate states of a replay at an earlier cutoff
    seen = {h for h, _ in unresolved}
    malformed = [(h, why) for h, why in (comp.get("withheld_stored") or [] if windowed else [])
                 if str(why).startswith("malformed") and h not in seen]
    for h, why in unresolved + malformed:
        reasons.append(f"unresolved stored control for hour {iso(h)}: {why}")
    for h in ready:
        reasons.append(f"closed hour {iso(h)} had an eligible candidate but no control")
    write = bool(getattr(lab, "write", False)) and getattr(lab, "control_context", None) is not None
    if write:
        expected = controls_mod.load_selections(lab.base, design)
        if windowed and comp.get("used_equals_stored") is not True:
            reasons.append("incomplete: the controls used were not confirmed equal to the stored selections"
                           if comp.get("used_equals_stored") is None else
                           "the controls used differ from the stored selections")
    else:
        expected = {c.get("control_hour"): c for c in p.get("controls") or []}
    labelled_controls = [e for e, _, _ in labelled if e.get("group") == "control_long"]
    if not windowed and (labelled_controls or (write and expected)):
        reasons.append("incomplete: controls exist but the pass reported no comparison window to validate them in")
    agree = controls_mod.evidence_agreement(labelled, expected)
    unpolicied = [e.get("control_hour") for e, _, _ in labelled
                  if e.get("group") == "control_long" and e.get("control_policy") != controls_mod.POLICY]
    if unpolicied:
        reasons.append(f"{len(unpolicied)} labelled controls carry no {controls_mod.POLICY} selection")
    for h in agree["mismatches"]:
        reasons.append(f"labelled control for hour {iso(h) if isinstance(h, int) else h} is not the selection it came from")
    failed = bool(unresolved or malformed or ready or agree["mismatches"] or unpolicied
                  or (write and windowed and comp.get("used_equals_stored") is False))
    incomplete = any(r.startswith("incomplete") for r in reasons)
    status = "failed" if failed else "incomplete" if incomplete else "passed"
    return dict(out, status=status, reasons=reasons, ok=status == "passed",
                policy_failures=comp.get("integrity_failures", 0) if windowed else 0,
                unresolved_conflicts=unresolved, ready_but_unselected=ready, evidence_agreement=agree,
                used_equals_stored=comp.get("used_equals_stored"),
                controls_fingerprint=comp.get("controls_fingerprint"), stored_fingerprint=comp.get("stored_fingerprint"))


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
    """Frozen decisions by decision_key; the FIRST stored record of a key wins (a duplicate line, e.g.
    from a merge, can never replace the original freeze)."""
    out = {}
    for e in read_dir(base, f"{ns(design)}/events"):
        out.setdefault(e["decision_key"], e)
    return out


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


def run_design(lab, design, module, registration, n_variants, superseded=False, run_state=None, variants_at=None):
    """Run every variant; returns (result, ledger rows). Persists frozen decisions, outcomes and newly
    completed checkpoints of the primary variant's prospective pass when lab.write. `variants_at(t)`
    gives the family's variant count as of t (default: n_variants), so a checkpoint's multiplicity is
    bounded by its cutoff."""
    variants_at = variants_at or (lambda t: n_variants)
    horizons = design["outcome"]["horizons_min"]
    funding = lab.store.funding_known()          # (t, rate, avail): labels use settlements with their availability
    known = Known(funding)
    funding_assumed = [(t, r, t) for t, r, _ in funding]     # reconstruction: settlement assumed known at t
    known_assumed = Known(funding_assumed)
    snaps = lab.store.snaps()
    last_cutoff = (run_state or {}).get("last_cutoff")
    variants, ledger, audits = [], [], {}
    deferred = None
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
            ckey = lambda e: (e["detector"], e["direction"], e.get("live_status"))
            if primary_pro:              # frozen decisions: episodes in the order decisions were known
                heads = collapse_as_known(events, design["collapse_ms"], ckey,
                                          known=lambda e: e["t_persisted"] if e.get("t_persisted") is not None
                                          else float("inf"))
            else:
                heads = collapse(events, design["collapse_ms"], key=ckey)
            controls = [dict(c, group=g, direction=dr, event_id=c["event_id"] + sfx, episode_head=True, episode_size=1)
                        for c in p["controls"] for g, dr, sfx in (("control_long", 1, "L"), ("control_short", -1, "S"))]
            raw["control_long"] = len(controls) // 2
            is_pro = p["basis"] == "prospective"
            labelled, immature, incomplete = label_all(heads + controls, p["bars"], lab.now, horizons,
                                                       funding if is_pro else funding_assumed,
                                                       snaps if is_pro else (), known if is_pro else known_assumed)
            baselines = baseline_mod.build(labelled, horizons)       # one per horizon, same-horizon controls
            reg = regime_fn(p["bars"])
            scorable = sum(1 for _, labs, _ in labelled for v in labs.values() if v["status"] != "immature")
            quality = {"incomplete_share": incomplete / scorable if scorable else 0.0,
                       "immature_labels": immature, "incomplete_labels": incomplete}
            if is_pro:
                phases = {"reanalysis": summarize(labelled, design, registration, "reanalysis", raw, baselines, n_variants, reg),
                          "evaluation": summarize(labelled, design, registration, "evaluation", raw, baselines, n_variants, reg)}
            else:
                phases = {"exploratory": summarize(labelled, design, None, "exploratory", raw, baselines, n_variants, reg)}
            st = cps = integrity = None
            if primary_pro:
                # 2.12: required input integrity is checked on the labels just computed, BEFORE any
                # frozen decision, outcome or checkpoint is persisted
                integrity = input_integrity(lab, design, p, labelled)
                allowed = evaluation_allowed(integrity)
                if allowed:
                    # computed now, WRITTEN only after every variant has run without error (below)
                    before = load_checkpoints(lab.base, design)
                    records, pending, drift = checkpoints(lab, design, labelled, registration, baselines,
                                                          variants_at, False)
                    st = status(design, records, pending, superseded)
                    if lab.write:
                        deferred = {"variant": variant, "events": events, "labelled": labelled, "pending": pending,
                                    "new": [r for r in records if r["look"] not in before]}
                else:
                    records = [r for _, r in sorted(load_checkpoints(lab.base, design).items())]
                    pending, drift = None, []
                    st = ("blocked", f"research integrity {integrity['status']}: "
                                     f"{'; '.join(integrity['reasons'][:3]) or 'no reason recorded'}"
                                     f"{'; ...' if len(integrity['reasons']) > 3 else ''}; this attempt evaluated and "
                                     "recorded no checkpoint and persisted no decision"
                                     + ("; earlier recorded checkpoints are history, not a current result" if records else ""))
                cps = {"records": records, "pending": pending, "drift": drift, "evaluated": allowed}
            vout["passes"].append({"basis": p["basis"], "state": p["state"], "reasons": p["reasons"],
                                   "coverage": p["coverage"], "firings": sum(v for k, v in raw.items() if k != "control_long"),
                                   "episodes": len(heads), "controls": len(controls) // 2, "quality": quality,
                                   "freeze_audit": audit, "data_sha256": p.get("data_sha256"), "phases": phases,
                                   "status": st, "checkpoints": cps, "integrity": integrity if primary_pro else None,
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
    if deferred is not None:
        # 2.12: nothing of the evaluation is written until the whole design has run; an exception in
        # any variant leaves no decision, outcome or checkpoint behind
        persist(lab, design, deferred["variant"], deferred["events"], deferred["labelled"])
        path = Path(lab.base) / ns(design) / "checkpoints.jsonl"
        stored = {}
        for rec in deferred["new"]:
            append_unique(path, [rec], key=lambda r: (r["look"],))
            stored = load_checkpoints(lab.base, design)
            if stored.get(rec["look"]) != rec:          # a record already stored stands; stop there
                break
        if deferred["new"]:
            kept = []
            for r in pro["checkpoints"]["records"]:
                kept.append(stored.get(r["look"], r))
                if kept[-1] != r:                         # another record stood: the walk ends there
                    break
            pending = deferred["pending"] if len(kept) == len(pro["checkpoints"]["records"]) else None
            pro["checkpoints"].update(records=kept, pending=pending)
            pro["status"] = status(design, kept, pending, superseded)
    if pro is not None and not evaluation_allowed(pro.get("integrity")):
        for row in ledger:                               # descriptive numbers from unvalidated inputs
            row.update(evaluation_blocked=True, retained_test=None, **{"diff_alpha_0.10": None})
    st, why = pro["status"] if pro and pro["status"] else ("exploratory", "no prospective pass")
    cps = (pro or {}).get("checkpoints") or {"records": [], "pending": None, "drift": []}
    integrity = (pro or {}).get("integrity") or {"required": None, "status": "incomplete", "ok": False,
                                                  "reasons": ["incomplete: no primary prospective pass"]}
    return {"t": lab.now, "design": design["id"], "version": design["_version"], "design_sha256": design["_sha256"],
            "registered": registration["registered"] if registration else None, "module": design["module"],
            "status": st, "status_reason": why, "checkpoints": cps, "variants": variants, "lab_version": LAB_VERSION,
            "code_sha256": lab.code, "cost_model": outcomes.COST_MODEL, "n_variants_family": n_variants,
            "integrity": integrity, "evaluation_blocked": not evaluation_allowed(integrity)}, ledger


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
