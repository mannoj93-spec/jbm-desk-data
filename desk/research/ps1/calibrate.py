#!/usr/bin/env python3
"""PS1 calibration - labelled TRAINING/CALIBRATION, not evidence (paper sizing protocol PS1 v1, repo 2.20).

Computes the three constants the frozen protocol (desk/research/ps1/protocol.json) uses to turn a forecast into
a 4-hour return standard deviation, from the repository's retained, hash-verified inputs only:

  k_b2      sigma_hat = k_b2 * point, where point = exp(p) is the B2 4h range forecast (ln(high/low) units)
  k_vol     sigma_hat = k_vol * sd_park_42, the Parkinson 4H sigma over the trailing 42 bars
  s_uncond  the unconditional 4H return scale over the calibration period (fixed arm)

Each k is the variance calibration  k^2 = mean(r^2 / x^2)  over the calibration decisions, where r is the
close-to-close log return of the 4H bar that follows the decision and x the arm's raw forecast. By construction
the calibrated forecast has unit mean standardized squared return in the calibration period; nothing is chosen
for trading returns, and no cost, weight cap, band or return statistic enters the constants.

Why a conversion: a range is not a standard deviation. For a driftless Brownian path the expected log range over
a window is 2*sqrt(2/pi)*sigma ~= 1.596*sigma, so the theoretical k for a range forecast is ~0.627; the fitted
point is a geometric-mean forecast of the range, and crypto returns are fat-tailed and bar-discretized, so the
constant is calibrated rather than assumed. The theoretical value is printed beside it.

Risk target: 15% annualized (sigma_star_4h = 0.15/sqrt(2190)). It was set from the weight distribution alone,
before any return, cost or turnover statistic existed: at 20% the unlevered cap (weight <= 1) bound in 5.7% of B2
decisions and 0% of VOL decisions, an asymmetry the comparison should not carry; at 15% it binds in ~1% of B2
decisions. The weights' levels differ by arm (Jensen: E[1/sigma_hat] depends on the forecast's dispersion), so the
primary metric is scale-free (protocol.json) and actual exposure is reported beside it.

B2 points are walk-forward: each month's forecasts use a fit on targets that matured before that month began
(range_contract.walk_forward, the O21 rule), so no calibration forecast used its own outcome.

Calibration decisions: 4H closes in [2024-09-23T00:00Z, 2026-09-23T00:00Z) whose following bar closed by the
cutoff 2026-09-23T00:00Z - the O21 validation and holdout years, already spent as evaluation periods. They are
calibration data here and cannot be a fresh holdout for PS1.

  python3 desk/research/ps1/calibrate.py            # print the result
  python3 desk/research/ps1/calibrate.py write      # write desk/research/ps1/calibration.json
  python3 desk/research/ps1/calibrate.py verify     # recompute and compare with the stored file (exact to 1e-12)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parents[1]
sys.path.insert(0, str(DESK))

import range_model as R          # noqa: E402
import range_contract as C       # noqa: E402

VERSION = "ps1-calibration-1"
START = "2024-09-23T00:00:00Z"
CUTOFF = "2026-09-23T00:00:00Z"            # nothing that closed after this instant is read
TARGET_ANNUAL_VOL = 0.15
BARS_PER_YEAR = 365 * 6
OUT = HERE / "calibration.json"


def load_history(cutoff=CUTOFF):
    """Retained O21 inputs (hash-verified) truncated at the cutoff: bars closed <= cutoff, DVOL available <= cutoff."""
    import retained as K
    k, d = K.load_o21_inputs(DESK / "research/o21")
    bars = [b for b in k["rows"] if b["close_utc"] <= cutoff]
    dvol = [r for r in d["rows"] if r["available_at_utc"] <= cutoff]
    return bars, dvol


def compute(bars, dvol, releases, start=START, cutoff=CUTOFF) -> dict:
    """The calibration from given inputs. Raises if any input closed after the cutoff (look-ahead guard)."""
    late = [b["close_utc"] for b in bars if b["close_utc"] > cutoff] + \
           [r["available_at_utc"] for r in dvol if r["available_at_utc"] > cutoff]
    if late:
        raise ValueError(f"calibration input after the cutoff {cutoff}: {sorted(late)[:3]}")
    panel = R.build_panel(bars, releases, dvol, horizons=("4h",))["4h"]
    fc = C.walk_forward(panel, "B2", start, cutoff)
    by_dec = {r["decision_utc"]: r for r in panel}
    close_at = {b["close_utc"]: b["close"] for b in bars}
    nxt = {b["open_utc"]: b for b in bars}
    rows = []
    for f in fc:
        row = by_dec[f["decision_utc"]]
        following = nxt.get(f["decision_utc"])
        if following is None or following["close_utc"] > cutoff:
            continue
        r = math.log(following["close"] / close_at[f["decision_utc"]])
        rows.append((f["decision_utc"], r, math.exp(f["point"]), row["sd_park_42"], f["refit_utc"]))
    if len(rows) < 1000:
        raise ValueError(f"too few calibration decisions: {len(rows)}")
    r2 = [x[1] ** 2 for x in rows]
    k_b2 = math.sqrt(statistics.fmean(a / (x[2] ** 2) for a, x in zip(r2, rows)))
    k_vol = math.sqrt(statistics.fmean(a / (x[3] ** 2) for a, x in zip(r2, rows)))
    s_unc = math.sqrt(statistics.fmean(r2))
    sigma_star = TARGET_ANNUAL_VOL / math.sqrt(BARS_PER_YEAR)
    w = {"B2": [min(1.0, sigma_star / (k_b2 * x[2])) for x in rows],
         "VOL": [min(1.0, sigma_star / (k_vol * x[3])) for x in rows]}
    return {
        "version": VERSION, "label": "TRAINING/CALIBRATION - not evidence, not a holdout",
        "window": {"first_decision_utc": rows[0][0], "last_decision_utc": rows[-1][0], "cutoff_utc": cutoff,
                   "decisions": len(rows), "refits": sorted({x[4] for x in rows})[:1] + sorted({x[4] for x in rows})[-1:],
                   "refit_months": len({x[4] for x in rows})},
        "constants": {"k_b2": round(k_b2, 12), "k_vol": round(k_vol, 12), "s_uncond": round(s_unc, 12),
                      "sigma_star_4h": round(sigma_star, 12), "target_annual_vol": TARGET_ANNUAL_VOL},
        "theory": {"k_range_brownian": round(1 / (2 * math.sqrt(2 / math.pi)), 6),
                   "k_parkinson_brownian": 1.0},
        "descriptive_only": {
            "note": "weights implied by the constants over the calibration decisions; reported, not used to choose "
                    "anything (no return, cost or turnover statistic was computed)",
            "mean_weight": {"FIXED": round(min(1.0, sigma_star / s_unc), 6),
                            "VOL": round(statistics.fmean(w["VOL"]), 6), "B2": round(statistics.fmean(w["B2"]), 6)},
            "share_capped": {k: round(sum(x >= 1.0 for x in v) / len(v), 6) for k, v in w.items()}},
        "inputs": {"source": "desk/research/o21 retained inputs (MANIFEST.json hashes)", "model": R.VERSION,
                   "contract_rule": "range_contract.walk_forward (monthly refits on matured targets)",
                   "return": "ln(close of the 4H bar opening at the decision / close at the decision)"},
    }


def run():
    import retained as K
    bars, dvol = load_history()
    releases = K.parse_calendar((DESK / "releases_2020_2026.csv").read_bytes())
    return compute(bars, dvol, releases)


def canonical(doc) -> bytes:
    return (json.dumps(doc, indent=1, sort_keys=True) + "\n").encode()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "print"
    doc = run()
    if cmd == "write":
        OUT.write_bytes(canonical(doc))
        print("wrote", OUT.name, hashlib.sha256(canonical(doc)).hexdigest()[:12])
    elif cmd == "verify":
        stored = json.loads(OUT.read_text())
        bad = [k for k in ("k_b2", "k_vol", "s_uncond", "sigma_star_4h")
               if abs(stored["constants"][k] - doc["constants"][k]) > 1e-12]
        print("calibration verify:", "PASS" if not bad else f"FAIL {bad}")
        raise SystemExit(1 if bad else 0)
    else:
        print(json.dumps(doc, indent=1, sort_keys=True))
