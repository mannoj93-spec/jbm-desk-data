#!/usr/bin/env python3
"""Before/after replay of the hourly comparison observations (controls) of modules B, C and F.

  python scripts/replay_controls_210.py CODE_ROOT DATA_ROOT CUTOFF_MS [WINDOW_START_MS]

Runs the modules of CODE_ROOT (e.g. a checkout of 934bb25 for the reviewed behaviour, or this
checkout) read-only over the collected data in DATA_ROOT, as known at CUTOFF_MS, and prints per
design: the hours in the window, the hours in which at least one record had its required inputs
available and in time (eligibility derived from the data with the 2.10 definition, independent of
the code being replayed), and every selected control with its source, required-input availability
and assumed decision times. Nothing is written. Defaults: window from 2026-09-24 00:00 UTC.
"""
import datetime as dt
import importlib
import json
import os
from pathlib import Path
import sys

code, data, cutoff = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
start = int(sys.argv[4]) if len(sys.argv) > 4 else 1_790_208_000_000
sys.path.insert(0, str(code))
os.chdir(code)
from lab import experiments                                  # noqa: E402
from lab.asof import decide                                  # noqa: E402
from lab.run import Lab, MODULES                             # noqa: E402

H = 3_600_000
hm = lambda ms: dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).strftime("%H:%M:%S")


def eligible_hours(lab, module):
    """Hours (by required-input availability) with at least one eligible candidate - from the raw
    records, with the 2.10 definitions, so the expected count does not come from either policy."""
    st, out = lab.store, {}
    if module == "liq_exposure":
        marks = {s["t"]: s.get("observed_at") for s in st.snaps()
                 if ((s.get("oi") or {}).get("hyperliquid") or {}).get("st") == "ok"
                 and ((s.get("oi") or {}).get("hyperliquid") or {}).get("mark")}
        cands = [(r["t"], max(r["observed_at"], marks[r["t"]])) for r in st.hl_accounts()
                 if marks.get(r["t"]) is not None]
    elif module == "options_disagreement":
        cands = [(r["t"], r["observed_at"]) for r in st.options()]
    else:
        from lab.modules import accounts
        by = {}
        for x in accounts.transitions(st):
            by[x["t"]] = max(by.get(x["t"], 0), x["avail"])
        cands = sorted(by.items())
    for t, a in cands:
        if a >= start and not decide(t, a)[1]:
            out.setdefault(a // H * H, []).append((t, a))
    return out


lab = Lab(data, cutoff, write=False)
hours = list(range(start // H * H, cutoff // H * H + H, H))
closed = [h for h in hours if h + H <= cutoff]
print(json.dumps({"code_root": str(code), "lab_version": __import__("lab.common").common.LAB_VERSION,
                  "data_root": str(data), "cutoff": dt.datetime.fromtimestamp(cutoff / 1000, dt.timezone.utc).isoformat(),
                  "window_hours": len(hours), "closed_hours": len(closed)}))
for path in experiments.design_files(code):
    d = experiments.load_design(path)
    if d["module"] not in ("liq_exposure", "options_disagreement", "account_behavior"):
        continue
    mod = importlib.import_module(MODULES[d["module"]])
    v = next(v for v in d["variants"] if v["name"] == d["primary_variant"])
    p = mod.run(lab, v["params"])["passes"][0]
    ctl = sorted((c for c in p["controls"] if (c.get("t_inputs") or c["t_event"]) >= start), key=lambda c: c["t_event"])
    elig = eligible_hours(lab, d["module"])
    sel_hours = {(c.get("t_inputs") or c["t_event"]) // H * H for c in ctl}
    missing = [hm(h)[:5] for h in closed if h not in sel_hours]
    diag = (p.get("coverage") or {}).get("comparison") or {}
    print(json.dumps({"design": d["id"], "module_version": mod.VERSION, "controls": len(ctl),
                      "hours_with_eligible_candidates": len([h for h in hours if h in elig]),
                      "closed_hours_with_eligible_candidates": len([h for h in closed if h in elig]),
                      "closed_eligible_hours_without_control": [hm(h)[:5] for h in closed if h in elig and h not in sel_hours],
                      "selected (source / inputs available / assumed decision)":
                          [f"{hm(c['t_event'])} / {hm(c.get('t_inputs') or 0)} / {hm(c['t_available'])}" for c in ctl],
                      "closed_hours_without_control": missing,
                      "missing_reasons": [[hm(h)[:5], why] for h, why in diag.get("missing_closed_hours", [])]}))
