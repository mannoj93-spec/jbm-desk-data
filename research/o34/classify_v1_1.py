"""O34 classification v1.1 - the Holm-gated filing rule (package 12.4.16).

Supersedes only the filing branch of run_o34.py (v1), which classified on the unadjusted validation interval
although protocol.json declared the nine-variant Holm family. v1's protocol, runner, results and its recorded
classification stay exactly as they are (hashes below); this file reads results_v1.json and applies:

  family   the nine (k, H) variants, validation period, primary k = 0.7, H = 6 bars
  test     two-sided stationary-block-bootstrap p-value as computed by v1 (p_two_sided), Holm-adjusted within the
           family (range_contract.holm, as v1 already stored in p_holm)
  alpha    0.05 on the Holm-adjusted p-value
  gate     validation: Holm-adjusted p < alpha AND the unadjusted 95 % interval excludes 0
  holdout  then holdout-consistent only if the holdout interval excludes 0 with the same sign
Statuses: 'no demonstrated difference', 'validation only, not holdout-consistent',
'exploratory, holdout-consistent (D < 0 | D > 0)'.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

VERSION = "o34-classify-1.1.0"
HERE = Path(__file__).resolve().parent
V1 = {"protocol.json": "8b7fb0f1dc295b8aaed11bd746e7672f6a2304213ffd37df7178727ed3adc2c4",
      "run_o34.py": "107f1fe5e9a5237599faba00749c3d9b27d5da5f1dcfde1fda7dc510b4e3ddfb",
      "results_v1.json": "5efc7d92921ad7152e12d2816e84776788833fbe98a6e39397ddb658b7e955eb"}
ALPHA = 0.05
PRIMARY = "k0.7_H6"
FAMILY = tuple(f"k{k}_H{h}" for k in (0.7, 1.0, 1.5) for h in (2, 6, 18))


def v1_intact(folder: Path = HERE) -> list[str]:
    probs = []
    for f, want in V1.items():
        got = hashlib.sha256((folder / f).read_bytes()).hexdigest()
        if got != want:
            probs.append(f"{f}: sha256 {got[:12]} differs from the v1 record {want[:12]}")
    return probs


def _excl0(ci) -> bool:
    return ci[0] > 0 or ci[1] < 0


def classify(results: dict, primary: str = PRIMARY) -> dict:
    fam = results["variants"]
    missing = [v for v in FAMILY if v not in fam]
    if missing:
        raise ValueError(f"family incomplete: {missing}")
    val, ho = fam[primary]["validation"], fam[primary]["holdout"]
    p_adj = val.get("p_holm")
    if p_adj is None:
        raise ValueError("validation Holm-adjusted p-value missing")
    gate = p_adj < ALPHA and _excl0(val["ci95_bp"])
    if not gate:
        status = "no demonstrated difference"
    elif _excl0(ho["ci95_bp"]) and (val["mean_D_bp"] > 0) == (ho["mean_D_bp"] > 0):
        status = f"exploratory, holdout-consistent (D {'<' if val['mean_D_bp'] < 0 else '>'} 0)"
    else:
        status = "validation only, not holdout-consistent"
    return {"version": VERSION, "primary": primary, "status": status, "alpha": ALPHA, "validation_p_holm": p_adj,
            "validation_ci95_bp": val["ci95_bp"], "holdout_ci95_bp": ho["ci95_bp"],
            "v1_recorded_status": results.get("primary", {}).get("filing_status")}


if __name__ == "__main__":
    probs = v1_intact()
    if probs:
        raise SystemExit("v1 record altered: " + "; ".join(probs))
    print(json.dumps(classify(json.loads((HERE / "results_v1.json").read_text())), indent=1))
