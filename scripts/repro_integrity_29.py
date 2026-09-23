#!/usr/bin/env python3
"""Before/after reproductions of the three issues fixed in 2.9 (lab-2.1), runnable against any tree.

  python scripts/repro_integrity_29.py [CODE_ROOT]

CODE_ROOT defaults to this checkout; point it at a checkout of c9fff86 (2.8) to reproduce the
reviewed behaviour. The lab code is imported from CODE_ROOT; the synthetic scenarios come from
this checkout's regression/test_rev29.py and drive only interfaces present in both versions
(experiments.run_design, options_disagreement.run). Prints one JSON object per issue. Synthetic
data only, in temporary directories.
"""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE).resolve()
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("rev29", HERE / "regression/test_rev29.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)


def issue1():
    """100 short decisions, then 100 long ones; the n=100 checkpoint before and after appending."""
    first, later, controls, y = t.scenario()
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        a = t.Harness(d1, t.design(), y)
        r1 = a.run(t.CheckpointTests.now1, first + later, controls)
        r2 = a.run(t.T0 + 1300 * t.H, first + later, controls, run_state={"last_cutoff": t.CheckpointTests.now1})
        fresh = t.Harness(d2, t.design(), y).run(t.T0 + 1300 * t.H, first + later, controls)
    out = {"issue": 1, "first_100_known": r1["status"], "after_100_more_appended": r2["status"],
           "single_run_with_all_200": fresh["status"]}
    rec = ((r2.get("checkpoints") or {}).get("records") or [None])[0]
    if rec:
        out["recorded_checkpoint"] = {"look": rec["look"], "n": rec["n"], "cutoff": rec["cutoff"],
                                      "p_long": rec["manifest"]["p_long"], "verdict": rec["verdict"],
                                      "manifest_sha256": rec["manifest_sha256"][:16]}
    return out


def issue2():
    """The 09:30 record's funding snapshot is first observed at 10:00; the 09:45 decision is at 09:47."""
    c = t.OptionsAvailabilityTests()
    out = {"issue": 2}
    for policy in ("qualified", "mark_only"):
        got = {}
        for f in (0.0001, 0.5):
            evs = c.at(c.module_run(policy, f_prev=f), t.T_EVT)
            got[f"future_funding_{f}"] = [{"group": e["group"], "funding_z": round(e["features"]["funding_z"], 3),
                                           "t_inputs_min_after_0945": (e["t_inputs"] - t.T_EVT) / t.MINUTE}
                                          for e in evs]
        out[policy] = got
    return out


def issue3():
    """Outcomes depend on the prior return with a different slope per horizon (30m +2, 60m -3, 240m
    +0.5); the 480m control labels are all incomplete."""
    h = t.HorizonBaselineTests()
    tests, controls = h.data()
    ctl_t = {c["t_available"] for c in controls}
    status = lambda ta, d, hh: "incomplete" if (hh == 480 and ta in ctl_t) else "complete"
    with tempfile.TemporaryDirectory() as dd:
        res = t.Harness(dd, t.design(h.H4, 60, ref="control", min_n=100), t.horizon_y, status).run(
            t.T0 + 30 * t.DAY, tests, controls)
    ev = res["variants"][0]["passes"][0]["phases"]["evaluation"]
    return {"issue": 3, "test_residual_mean_bp": {k: round(ev[k]["baseline"]["test_residual"]["mean"] * 1e4, 2)
                                                  for k in ("30", "60", "240")},
            "480_identifiable_share": ev["480"]["baseline"]["identifiable_share_test"],
            "480_residual_diff_adjusted": ev["480"]["baseline"]["residual_diff"]["adjusted"]}


if __name__ == "__main__":
    print(json.dumps({"code_root": str(ROOT), "lab_version": __import__("lab.common").common.LAB_VERSION}))
    for f in (issue1, issue2, issue3):
        try:
            print(json.dumps(f(), default=str))
        except Exception as exc:
            print(json.dumps({"issue": f.__name__, "error": f"{type(exc).__name__}: {exc}"}))
