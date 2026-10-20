"""Calibration harness for the exact proposed DIR1 evaluator (calibration-harness-1.0.0, repo 2.30; brief section 13).

calibration.py diagnoses coarse multiplicity-adjusted bootstrap tails and shows that a naive test has a high
false-positive rate. That does not validate the method proposed for promotion. This harness simulates the proposed
evaluator itself - EVALUATOR below, the DIR1 prepared protocol's primary comparison: paired Brier difference,
statistical minus baseline, on the pair-specific intersection of on-time graded forecasts, percentile block bootstrap
with 4-hour blocks, checkpoints at 500, 1,000 and 2,000 scheduled opportunities, alpha 0.10 / (comparisons x looks),
promotion when the interval's upper end is below zero at any look - under dependence-preserving nulls and declared
alternatives, and reports:

  - any-look (family-level) false-positive rate with a Wilson 95% simulation interval, and by look;
  - power against prespecified Brier improvements;
  - block sensitivity (4, 8 and 24-hour blocks) - hourly decisions on 4-hour returns overlap across adjacent 4-hour
    blocks, so block labels alone do not establish independence;
  - numerical tail resolution for the adjusted alpha at the actual B, under ONE tail-draw policy (>= 10 expected
    draws in each tail, calibration.MIN_TAIL_DRAWS, now also block_bootstrap_ci's default);
  - rows, distinct 4-hour outcome windows and resampling blocks separately - more resamples improve numerical
    precision, not independent market evidence, and twenty blocks certify nothing by themselves.

Nulls: hourly returns with Markov volatility regimes, persistent volatility, common jump shocks hitting every arm's
target, clustered outages (per arm and joint), overlapping 4-hour targets; both arms' forecasts are functions of past
noise only, identically distributed and serially dependent, so the expected paired difference is exactly zero.
Alternatives add information about the future target to the statistical arm, scaled to a declared Brier improvement.

Acceptance criteria are fixed BEFORE a run (research/calibration/<evaluator>/criteria.json, with its own hash) and
every run is appended to attempts.jsonl whether it passes or fails; a failing method is revised as a new evaluator
version with the attempt history disclosed, never tuned until one seed passes. A green calibration is necessary for
promotion, not sufficient: promotion still needs the registered prospective evidence.
"""
import hashlib
import inspect
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import calibration as C  # noqa: E402
from research_tools import evidence_contract as E  # noqa: E402

VERSION = "calibration-harness-1.0.0"
EVALUATOR = {"id": "dir1-primary-v1", "metric": "paired Brier difference, statistical - baseline",
             "pairing": "pair-specific intersection of on-time graded forecasts", "blocks_h": 4,
             "looks": [500, 1000, 2000], "alpha": 0.10, "comparisons": 1, "B": 2000, "min_blocks": 20,
             "min_tail_draws": C.MIN_TAIL_DRAWS, "interval": "percentile block bootstrap (calibration.block_bootstrap_ci)",
             "decision": "promote when the adjusted two-sided interval's upper end is below 0 at any look",
             "source": "research/registrations/dir1-prepared/protocol.json revision 2 (prepared)"}


def evaluator_sha256(ev=EVALUATOR):
    src = inspect.getsource(decide) + inspect.getsource(C.block_bootstrap_ci)
    return hashlib.sha256((E.canon(ev) + src).encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ the world
def simulate(n, rnd, p):
    """One synthetic schedule of n hourly opportunities: per opportunity the realized 4-hour target sign, each arm's
    forecast (or None when that arm is out) and the block id. p: scenario parameters."""
    m = n + 4
    vol, reg, rets = [], 0, []
    for _ in range(m):
        if rnd.random() < p["regime_switch"]:
            reg = 1 - reg
        s = p["vol_low"] if reg == 0 else p["vol_high"]
        r = rnd.gauss(0, s)
        if rnd.random() < p["jump_rate"]:
            r += rnd.choice((-1, 1)) * p["jump_size"]                  # common shock: every arm's target moves
        rets.append(r)
    targets = [1 if sum(rets[i + 1:i + 5]) > 0 else 0 for i in range(n)]     # overlapping 4-hour horizons
    z = {"baseline": 0.0, "statistical": 0.0}
    out_state = {"baseline": False, "statistical": False, "joint": False}
    rows = []
    for i in range(n):
        f = {}
        for arm in ("baseline", "statistical"):
            z[arm] = p["phi"] * z[arm] + math.sqrt(1 - p["phi"] ** 2) * rnd.gauss(0, 1)
        for k in out_state:
            q = p["outage_start"] if not out_state[k] else 1 - p["outage_stay"]
            if rnd.random() < q:
                out_state[k] = not out_state[k]
        for arm in ("baseline", "statistical"):
            if out_state[arm] or out_state["joint"]:
                f[arm] = None
                continue
            x = p["spread"] * z[arm]
            if arm == "statistical" and p.get("skill"):
                x += p["skill"] * (1 if targets[i] else -1)
            f[arm] = min(0.98, max(0.02, 0.5 + x))
        rows.append({"t": i, "target": targets[i], "f": f, "block_h": i})
    return rows


SCENARIOS = {
    "null-dependent": {"regime_switch": 0.01, "vol_low": 0.004, "vol_high": 0.012, "jump_rate": 0.01, "jump_size": 0.03,
                       "phi": 0.9, "spread": 0.06, "outage_start": 0.01, "outage_stay": 0.9, "skill": 0.0},
}


def alternative(delta_brier, base="null-dependent"):
    """The null's world with the statistical arm informed about the target: skill chosen so the expected Brier
    improvement is about delta_brier (Brier(p) - Brier(p') = 2 s (2y-1)... averaged: improvement ~ 2 s^2 + 2 s E|..|)."""
    p = dict(SCENARIOS[base])
    s = abs(delta_brier) / 2 / 0.5                                      # first-order: E[improvement] = 2 * s * 0.5
    p["skill"] = s
    return p


# ------------------------------------------------------------------------------------------------ evaluator
def decide(rows, ev=EVALUATOR, blocks_h=None, seed=0):
    """The proposed evaluator on one schedule: at each look, the first n scheduled opportunities, the pair-specific
    intersection, the paired Brier differences with their blocks, the adjusted percentile interval. Returns
    {"declared": bool, "first_look": n | None, "looks": [...]}"""
    bh = blocks_h or ev["blocks_h"]
    a = ev["alpha"] / (ev["comparisons"] * len(ev["looks"]))
    looks = []
    declared, first = False, None
    for n in ev["looks"]:
        sub = rows[:n]
        d, b = [], []
        for r in sub:
            pa, pb = r["f"].get("statistical"), r["f"].get("baseline")
            if pa is None or pb is None:
                continue
            d.append((pa - r["target"]) ** 2 - (pb - r["target"]) ** 2)
            b.append(r["block_h"] // bh)
        ci = C.block_bootstrap_ci(d, b, a, B=ev["B"], seed=seed * 7919 + n, min_blocks=ev["min_blocks"],
                                  min_tail_draws=ev["min_tail_draws"])
        hit = ci["state"] == "ok" and ci["hi"] < 0
        looks.append({"n_scheduled": n, "n_pair": len(d), "blocks": len(set(b)), "state": ci["state"],
                      "mean": round(sum(d) / len(d), 6) if d else None, "hi": ci.get("hi"), "declared": hit})
        if hit and not declared:
            declared, first = True, n
    return {"declared": declared, "first_look": first, "looks": looks}


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    ph = k / n
    den = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / den
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def run(sims_null=400, sims_alt=200, seed=33, alternatives=(-0.01, -0.005), block_sensitivity=(4, 8, 24), ev=EVALUATOR):
    rnd = random.Random(seed)
    n = max(ev["looks"])
    res = {"version": VERSION, "evaluator": ev, "evaluator_sha256": evaluator_sha256(ev), "seed": seed,
           "scenario": SCENARIOS["null-dependent"], "resolution": C.resolution(ev["B"], ev["alpha"], ev["comparisons"],
                                                                             len(ev["looks"]))}
    fp = {bh: 0 for bh in block_sensitivity}
    by_look = {bh: [0] * len(ev["looks"]) for bh in block_sensitivity}
    rows_seen = pairs_seen = blocks_seen = 0
    for k in range(sims_null):
        rows = simulate(n, rnd, SCENARIOS["null-dependent"])
        for bh in block_sensitivity:
            d = decide(rows, ev, bh, seed=k)
            fp[bh] += d["declared"]
            for j, lk in enumerate(d["looks"]):
                by_look[bh][j] += lk["declared"]
            if bh == ev["blocks_h"]:
                rows_seen += len(rows)
                pairs_seen += d["looks"][-1]["n_pair"]
                blocks_seen += d["looks"][-1]["blocks"]
    res["null"] = {str(bh): {"any_look_fpr": round(fp[bh] / sims_null, 4), "wilson95": wilson(fp[bh], sims_null),
                             "by_look": [round(x / sims_null, 4) for x in by_look[bh]]} for bh in block_sensitivity}
    res["null"]["sims"] = sims_null
    res["evidence_units_per_schedule"] = {"rows": rows_seen // max(1, sims_null),
                                          "pairs_at_final_look": pairs_seen // max(1, sims_null),
                                          "distinct_4h_windows": n // 4,
                                          "blocks_at_final_look": blocks_seen // max(1, sims_null),
                                          "note": "rows are not independent; blocks are a dependence device, not a count "
                                                  "of independent market events"}
    res["power"] = {}
    for delta in alternatives:
        p = alternative(delta)
        hits, firsts, means = 0, [], []
        for k in range(sims_alt):
            rows = simulate(n, rnd, p)
            d = decide(rows, ev, ev["blocks_h"], seed=10_000 + k)
            hits += d["declared"]
            firsts.append(d["first_look"])
            means.append(d["looks"][-1]["mean"])
        res["power"][str(delta)] = {"power_any_look": round(hits / sims_alt, 4), "wilson95": wilson(hits, sims_alt),
                                    "realized_mean_diff": round(sum(m for m in means if m is not None) / len(means), 5),
                                    "first_look_counts": {str(x): firsts.count(x) for x in sorted(set(firsts), key=str)},
                                    "sims": sims_alt}
    return res


def judge(res, criteria):
    """Verdict against criteria fixed before the run."""
    fails = []
    main = res["null"][str(res["evaluator"]["blocks_h"])]
    if main["any_look_fpr"] > criteria["max_any_look_fpr"]:
        fails.append(f"any-look FPR {main['any_look_fpr']} > {criteria['max_any_look_fpr']}")
    if main["wilson95"][1] > criteria["max_fpr_upper95"]:
        fails.append(f"FPR upper 95% bound {main['wilson95'][1]} > {criteria['max_fpr_upper95']}")
    for bh in criteria.get("sensitivity_blocks_h", []):
        v = res["null"].get(str(bh))
        if v and v["any_look_fpr"] > criteria["max_sensitivity_fpr"]:
            fails.append(f"{bh}h-block FPR {v['any_look_fpr']} > {criteria['max_sensitivity_fpr']}")
    pw = res["power"].get(str(criteria["power_delta"]))
    if pw is None or pw["power_any_look"] < criteria["min_power"]:
        fails.append(f"power at {criteria['power_delta']} below {criteria['min_power']}")
    if res["resolution"]["expected_tail_draws"] < criteria["min_tail_draws"]:
        fails.append("numerical tail resolution below the policy")
    return {"verdict": "pass" if not fails else "fail", "failures": fails}


def record_attempt(folder, res, criteria):
    folder = Path(folder)
    crit_sha = E.content_sha256(criteria)
    j = judge(res, criteria)
    rec = {"schema": "calibration-attempt/1", "harness": VERSION, "evaluator": res["evaluator"]["id"],
           "evaluator_sha256": res["evaluator_sha256"], "criteria_sha256": crit_sha, "seed": res["seed"],
           "results_sha256": E.content_sha256(res), "verdict": j["verdict"], "failures": j["failures"],
           "summary": {"null": res["null"], "power": {k: v["power_any_look"] for k, v in res["power"].items()}}}
    p = folder / "attempts.jsonl"
    prev = None
    if p.exists():
        lines = [x for x in p.read_text().splitlines() if x.strip()]
        prev = json.loads(lines[-1])["sha256"] if lines else None
    body = dict(rec, prev_sha256=prev)
    body["sha256"] = E.content_sha256(body)
    folder.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(E.canon(body) + "\n")
    (folder / f"results-{res['seed']}.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    return body


def _main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(prog="research_tools.calibration_harness")
    ap.add_argument("folder", help="research/calibration/<evaluator id>/ holding criteria.json")
    ap.add_argument("--seed", type=int, default=33)
    ap.add_argument("--sims-null", type=int, default=400)
    ap.add_argument("--sims-alt", type=int, default=200)
    a = ap.parse_args(argv)
    crit = json.loads((Path(a.folder) / "criteria.json").read_text())
    if crit.get("evaluator_sha256") != evaluator_sha256():
        print("criteria were fixed for another evaluator version; declare new criteria for this one", file=sys.stderr)
        return 2
    res = run(a.sims_null, a.sims_alt, a.seed)
    rec = record_attempt(a.folder, res, crit)
    print(json.dumps({k: rec[k] for k in ("verdict", "failures", "summary")}, indent=1))
    return 0 if rec["verdict"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(_main())
