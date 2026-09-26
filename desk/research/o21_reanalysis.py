#!/usr/bin/env python3
"""O21 replay and reanalysis (crypto-desk 12.0). Offline: reads only desk/research/o21/.

  replay      rebuild the original O21 result (range_model.run_o21, frozen spec) from the retained inputs
              and compare it with original/o21_holdout.json. Verifies input hashes first.
  reanalysis  the same data under contract RC1 with the corrected protocol: rows belong to a period only if
              decision AND target maturity fall inside it; losses through range_contract.losses; Holm across
              the O21 row's selection family. Also measures: the 2.14 live median (q50) as the point, the
              coherence raise, and the rescheduled-release sensitivity. This is REANALYSIS of data already
              inspected - not a new holdout. Writes research/o21/reanalysis_12.0.json(.gz for rows).

Run: python3 desk/research/o21_reanalysis.py replay|reanalysis
"""
import datetime as dt
import gzip
import hashlib
import json
import math
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parent
sys.path[:0] = [str(DESK), str(DESK.parent)]

import range_contract as C      # noqa: E402
import range_model as R         # noqa: E402

O21 = HERE / "o21"
UTC = dt.timezone.utc


def load_inputs():
    """The retained O21 inputs, verified by the same loader the monthly refit chain uses (retained.py)."""
    import retained
    return retained.load_o21_inputs(O21)


def replay():
    if R.spec_sha256() != C._COMMON["model_spec_sha256"]:
        raise SystemExit("range_model.py is not the frozen O21 specification")
    k, d = load_inputs()
    rel = R.load_calendar(str(DESK / "releases_2020_2026.csv"))
    panel = R.build_panel(k["rows"], rel, d["rows"])
    res = R.run_o21(panel, open_holdout=True)
    orig = json.loads((O21 / "original/o21_holdout.json").read_text())
    got = json.loads(json.dumps(res, default=str))
    for key in ("run_utc", "data"):
        orig.pop(key, None)
    diffs = []

    def walk(a, b, path):
        if isinstance(a, dict):
            for key in set(a) | set(b):
                walk(a.get(key), b.get(key), f"{path}.{key}")
        elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, f"{path}[{i}]")
        elif isinstance(a, float) and isinstance(b, float):
            if abs(a - b) > 1e-12 * max(1.0, abs(a)):
                diffs.append((path, a, b))
        elif a != b:
            diffs.append((path, a, b))
    walk(orig, got, "o21")
    print(f"replay: {len(diffs)} differences from the original O21 result" + (f"; first {diffs[:3]}" if diffs else ""))
    return diffs


def compare(fm, fb, horizon):
    bmap = {r["decision_utc"]: r for r in fb}
    pairs = [(a, bmap[a["decision_utc"]]) for a in fm if a["decision_utc"] in bmap]
    lm = [a["abs_error_log_lr"] for a, _ in pairs]
    lb = [b["abs_error_log_lr"] for _, b in pairs]
    lag = max(R.HORIZON_BARS[horizon], R.NW_MIN_LAG)
    md, z, p = R.diebold_mariano(lm, lb, lag)
    lo, hi = R.block_bootstrap_skill(lm, lb)
    return {"n": len(pairs), "mae_model": statistics.fmean(lm), "mae_base": statistics.fmean(lb),
            "skill": 1 - statistics.fmean(lm) / statistics.fmean(lb), "skill_ci95": [lo, hi], "dm_z": z, "dm_p": p,
            "qlike_model": statistics.fmean(a["qlike"] for a, _ in pairs),
            "qlike_base": statistics.fmean(b["qlike"] for _, b in pairs),
            "coverage_10_90": statistics.fmean(a["covered_80"] for a, _ in pairs)}


def reanalysis():
    t0 = time.time()
    k, d = load_inputs()
    rel = R.load_calendar(str(DESK / "releases_2020_2026.csv"))
    panel = R.build_panel(k["rows"], rel, d["rows"])
    V, H = C.PERIODS["validation"], C.PERIODS["holdout"]
    out = {"contract": C.contract_id("RC1"), "protocol": "reanalysis of already inspected data; maturity-bounded splits",
           "periods": C.PERIODS, "inputs": json.loads((O21 / "MANIFEST.json").read_text())["files"],
           "calendar_sha256": hashlib.sha256((DESK / "releases_2020_2026.csv").read_bytes()).hexdigest(),
           "code": {"range_model": R.VERSION, "spec_sha256": R.spec_sha256(), "range_contract": C.VERSION},
           "horizons": {}, "exclusions": {}}
    rows_out, family = [], {}
    fc_cache = {}
    for h, rows in panel.items():
        old_val = [r for r in rows if "2024-09-23T00:00:00Z" <= r["decision_utc"] <= "2025-09-22T23:59:59Z" and r["y"] is not None]
        old_hol = [r for r in rows if "2025-09-23T00:00:00Z" <= r["decision_utc"] <= "2026-09-22T23:59:59Z" and r["y"] is not None]
        out["exclusions"][h] = {
            "validation_rows_maturing_in_holdout": sum(r["target_close_utc"] > V[1] for r in old_val),
            "holdout_rows_maturing_after_holdout_end": sum(r["target_close_utc"] > H[1] for r in old_hol)}
        fc = {}
        for m in ("B0", "B1", "B2"):
            fc[(m, "val")] = C.loss_rows(C.walk_forward(rows, m, *V))
            fc[(m, "hol")] = C.loss_rows(C.walk_forward(rows, m, *H))
        fc_cache[h] = fc
        c10, c21, c20 = compare(fc[("B1", "val")], fc[("B0", "val")], h), compare(fc[("B2", "val")], fc[("B1", "val")], h), \
            compare(fc[("B2", "val")], fc[("B0", "val")], h)
        family[f"{h}:B1_vs_B0"] = c10["dm_p"]
        sel = "B1" if c10["skill"] > 0 and c10["dm_p"] < 0.05 else "B0"
        step = c21 if sel == "B1" else c20
        family[f"{h}:B2_vs_{sel}"] = step["dm_p"]
        if step["skill"] > 0 and step["dm_p"] < 0.05:
            sel = "B2"
        out["horizons"][h] = {"validation": {"B1_vs_B0": c10, "B2_vs_B1": c21, "B2_vs_B0": c20}, "selected_unadjusted": sel,
                              "holdout": {"B2_vs_B0": compare(fc[("B2", "hol")], fc[("B0", "hol")], h),
                                          "B1_vs_B0": compare(fc[("B1", "hol")], fc[("B0", "hol")], h)}}
        for (m, per), lst in fc.items():
            rows_out += [{"h": h, "model": m, "period": per, **{k2: r[k2] for k2 in (
                "decision_utc", "target_close_utc", "y", "point", "q", "refit_utc", "abs_error_log_lr", "qlike", "covered_80")}}
                for r in lst]
    # Stage 1 family members (4h targets never cross a boundary; the O21 stage-1 comparisons stand)
    orig = json.loads((O21 / "original/o21_holdout.json").read_text())
    for e, v in orig["stage1"]["validation"].items():
        if "vs_c2c" in v:
            family[f"stage1:{e}_vs_c2c"] = v["vs_c2c"]["dm_p"]
    adj = C.holm(family)
    out["holm"] = {"family": family, "adjusted": adj, "family_size": len(family)}
    for h in panel:
        sel_u = out["horizons"][h]["selected_unadjusted"]
        a10 = adj[f"{h}:B1_vs_B0"]
        v = out["horizons"][h]["validation"]
        sel = "B1" if v["B1_vs_B0"]["skill"] > 0 and a10 < 0.05 else "B0"
        key = f"{h}:B2_vs_{sel}"
        p2 = adj.get(key)
        if p2 is None:       # the Holm path's step comparison is outside the family the unadjusted path built
            step = v["B2_vs_B1"] if sel == "B1" else v["B2_vs_B0"]
            p2 = min(1.0, step["dm_p"] * len(family))
            out.setdefault("holm_fallback", {})[h] = {
                "comparison": key, "raw_p": step["dm_p"], "adjusted_p": p2,
                "method": f"Bonferroni at the family size ({len(family)}): conservative; the comparison was not a "
                          "family member because the unadjusted path had kept B1"}
        step = v["B2_vs_B1"] if sel == "B1" else v["B2_vs_B0"]
        if step["skill"] > 0 and p2 < 0.05:
            sel = "B2"
        out["horizons"][h]["selected_holm"] = sel
        out["horizons"][h]["selection_changed_vs_o21"] = sel != "B2" or sel_u != "B2"
    # Diagnostics on the holdout
    diag = {}
    fits = {}
    for h, rows in panel.items():
        fc = fc_cache[h]
        b2, b0 = fc[("B2", "hol")], {r["decision_utc"]: r for r in fc[("B0", "hol")]}
        # (a) 2.14 live contract: q50 (point + residual median) as the loss-bearing forecast
        med = [abs((r["q"][1]) - r["y"]) for r in b2]
        b0med = [abs((b0[r["decision_utc"]]["q"][1]) - b0[r["decision_utc"]]["y"]) for r in b2 if b0[r["decision_utc"]]["q"]]
        diag[h] = {"mae_point": statistics.fmean(r["abs_error_log_lr"] for r in b2), "mae_q50": statistics.fmean(med),
                   "mae_b0_point": statistics.fmean(b0[r["decision_utc"]]["abs_error_log_lr"] for r in b2),
                   "mae_b0_q50": statistics.fmean(b0med) if b0med else None,
                   "median_gap_lr_pct": 100 * (math.exp(statistics.fmean(r["q"][1] - r["point"] for r in b2)) - 1)}
        fits[h] = {r["decision_utc"]: r for r in b2}
    # (b) coherence: how often a raise would bind, and its effect on MAE where it binds
    binds, delta = {"24h<4h": 0, "72h<24h": 0}, {"24h": [], "72h": []}
    common = set(fits["4h"]) & set(fits["24h"]) & set(fits["72h"])
    for dstr in sorted(common):
        p4, p24, p72 = fits["4h"][dstr]["point"], fits["24h"][dstr]["point"], fits["72h"][dstr]["point"]
        c4, c24, c72, _ = R.coherent(p4, p24, p72)
        for h, p, c in (("24h", p24, c24), ("72h", p72, c72)):
            if c != p:
                binds["24h<4h" if h == "24h" else "72h<24h"] += 1
                y = fits[h][dstr]["y"]
                delta[h].append(abs(c - y) - abs(p - y))
    diag["coherence"] = {"decisions": len(common), "binds": binds,
                         "mean_abs_error_change_where_binding": {h: (statistics.fmean(v) if v else None) for h, v in delta.items()}}
    # (c) rescheduled releases (Oct 1 - Dec 15 2025 lapse in appropriations): drop them from the features
    import csv
    with open(DESK / "releases_2020_2026.csv", encoding="utf-8") as f:
        kinds = {R._t(r["release_utc"]): r["event"] for r in csv.DictReader(x for x in f if not x.startswith("#"))}
    # BLS releases (CPI, NFP, PPI) actually published during and after the lapse in appropriations; FOMC kept.
    lapse = [r for r in rel if dt.datetime(2025, 10, 1, tzinfo=UTC) <= r < dt.datetime(2025, 12, 16, tzinfo=UTC)
             and kinds.get(r) != "FOMC"]
    rel2 = [r for r in rel if r not in lapse]
    panel2 = R.build_panel(k["rows"], rel2, d["rows"])
    sens = {}
    for h, rows in panel2.items():
        a = C.loss_rows(C.walk_forward(rows, "B2", *H))
        b = C.loss_rows(C.walk_forward(rows, "B0", *H))
        sens[h] = {"skill_without_lapse_releases": compare(a, b, h)["skill"],
                   "skill_with": out["horizons"][h]["holdout"]["B2_vs_B0"]["skill"]}
    diag["calendar_sensitivity"] = {"releases_removed": [f"{C.iso(r)} {kinds[r]}" for r in lapse], "result": sens,
                                    "assumption": "schedule vintages not retained; actual release times used at every decision; "
                                                  "originally scheduled dates that were moved or cancelled are not in the calendar"}
    out["diagnostics"] = diag
    out["run_seconds"] = round(time.time() - t0, 1)
    rows_blob = gzip.compress(C.canonical(rows_out), 9, mtime=0)
    (O21 / "reanalysis_12.0_rows.json.gz").write_bytes(rows_blob)
    out["rows_file"] = {"path": "reanalysis_12.0_rows.json.gz", "sha256_uncompressed": hashlib.sha256(C.canonical(rows_out)).hexdigest(),
                        "rows": len(rows_out)}
    (O21 / "reanalysis_12.0.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({h: {"sel": out["horizons"][h]["selected_holm"],
                          "hol_skill": round(out["horizons"][h]["holdout"]["B2_vs_B0"]["skill"], 4),
                          "ci": [round(x, 4) for x in out["horizons"][h]["holdout"]["B2_vs_B0"]["skill_ci95"]],
                          "n": out["horizons"][h]["holdout"]["B2_vs_B0"]["n"],
                          "cov": round(out["horizons"][h]["holdout"]["B2_vs_B0"]["coverage_10_90"], 3)}
                      for h in panel}, indent=1))
    return out


def _numeric_diff(a, b, path="", out=None):
    """(max abs diff, max rel diff, structural mismatches) between two JSON values."""
    out = out if out is not None else {"abs": 0.0, "rel": 0.0, "where": None, "struct": []}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k in ("run_seconds", "code") and not path:
                continue                                   # provenance labels, compared separately
            if k not in a or k not in b:
                out["struct"].append(f"{path}.{k}")
            else:
                _numeric_diff(a[k], b[k], f"{path}.{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out["struct"].append(f"{path} length")
        for i, (x, y) in enumerate(zip(a, b)):
            _numeric_diff(x, y, f"{path}[{i}]", out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        d = abs(a - b)
        if d > out["abs"]:
            out["abs"], out["where"] = d, path
        out["rel"] = max(out["rel"], d / max(abs(a), abs(b), 1e-300) if d else 0.0)
    elif a != b:
        out["struct"].append(path)
    return out


TOL = {"abs": 1e-9, "rel": 1e-9}     # declared numerical-replay tolerance (floating-point order effects only)


def verify():
    """Two different checks. Stored-byte integrity: the retained inputs and the stored reanalysis files hash to
    their recorded values. Numerical reproducibility: re-running the reanalysis in memory reproduces every
    stored number within TOL (serialized bytes may differ at ~1e-12 from summation order; conclusions cannot)."""
    t0 = time.time()
    load_inputs()                                                   # raises on any input byte change
    stored = json.loads((O21 / "reanalysis_12.0.json").read_text())
    rows_raw = gzip.decompress((O21 / stored["rows_file"]["path"]).read_bytes())
    if hashlib.sha256(rows_raw).hexdigest() != stored["rows_file"]["sha256_uncompressed"]:
        raise SystemExit("stored reanalysis rows altered: hash mismatch")
    import tempfile
    saved = O21
    tmp = Path(tempfile.mkdtemp())
    for sub in ("inputs", "original"):
        (tmp / sub).mkdir()
        for f in (O21 / sub).iterdir():
            (tmp / sub / f.name).write_bytes(f.read_bytes())
    (tmp / "MANIFEST.json").write_bytes((O21 / "MANIFEST.json").read_bytes())
    globals()["O21"] = tmp
    try:
        fresh = reanalysis()
    finally:
        globals()["O21"] = saved
    fresh.pop("holm_fallback", None)
    diff = _numeric_diff(stored, json.loads(json.dumps(fresh)))
    ok = not diff["struct"] and (diff["abs"] <= TOL["abs"] or diff["rel"] <= TOL["rel"])
    res = {"stored_bytes": "verified", "numerical": "within tolerance" if ok else "OUT OF TOLERANCE",
           "max_abs_diff": diff["abs"], "max_rel_diff": diff["rel"], "at": diff["where"],
           "structural_mismatches": diff["struct"][:5], "tolerance": TOL, "runtime_s": round(time.time() - t0, 1),
           "code_then": stored.get("code"), "code_now": fresh.get("code")}
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    {"replay": replay, "reanalysis": reanalysis, "verify": verify}[sys.argv[1]]()
