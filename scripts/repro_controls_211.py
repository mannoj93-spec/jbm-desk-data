#!/usr/bin/env python3
"""Before/after reproductions of the two control-selection defects fixed in 2.11, for any code tree.

  python scripts/repro_controls_211.py [CODE_ROOT]

CODE_ROOT defaults to this checkout; point it at a checkout of 8432df0 (2.10) to reproduce the
reviewed behaviour. The lab code comes from CODE_ROOT; the synthetic collection records come from
this checkout's regression/test_rev210.py. Only interfaces present in both versions are driven
(module.run, controls.persist_selections / load_selections, outcomes.label). Writes happen only in
temporary directories. Prints one JSON object per reproduction.
"""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE).resolve()
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("rev210", HERE / "regression/test_rev210.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
from lab import controls, outcomes                                   # noqa: E402
from lab.modules import liq_exposure, options_disagreement           # noqa: E402

H, M, S, T0 = t.H, t.MINUTE, 1000, t.T0
iso = lambda ms: None if ms is None else __import__("datetime").datetime.fromtimestamp(ms / 1000, __import__("datetime").timezone.utc).strftime("%H:%M:%S")


def run_module(mod, runs, now, ctx=None, base=None, write=False):
    lab = t.lab_(runs, now, ctx)
    lab.base, lab.write = base, write
    with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rr"]}), \
            patch.object(options_disagreement, "panel_quality", lambda rec: {"rr25_7d_quotes": "unknown"}):
        try:
            p = mod.run(lab, t.PARAMS[mod.ID])["passes"][0]
        except Exception as exc:
            return None, f"{type(exc).__name__}: {exc}"
    return p["controls"], p["coverage"].get("comparison") or {}


def repro_cutoff():
    """Inputs available 09:59:30; decision 10:00:30 (60 s assumed processing)."""
    ten = T0 + 10 * H
    runs = [t.run_(ten - 90 * S, 60 * S)]                 # source 09:58:30, inputs 09:59:30
    out = {"repro": "decision-time cutoff"}
    for name, mod in (("liq_exposure", liq_exposure), ("options_disagreement", options_disagreement)):
        row = {}
        for label, now in (("10:00:00.000", ten), ("10:00:29.999", ten + 30 * S - 1), ("10:00:30.000", ten + 30 * S)):
            ctl, diag = run_module(mod, runs, now)
            row[label] = [{"hour": iso(c["t_inputs"] // H * H), "inputs": iso(c["t_inputs"]), "decision": iso(c["t_available"]),
                           "decision_after_cutoff": c["t_available"] > now} for c in ctl or []] or \
                         {"returned": 0, "pending": [iso(h) for h, _ in (diag.get("pending_processing") or [])]}
        out[name] = row
    return out


def repro_authority():
    """Writer A stores the :20 observation for 10:00; worker B, with a stale empty context, proposes :10."""
    ten = T0 + 10 * H
    rec20, rec10 = t.run_(ten + 20 * M, 30 * S), t.run_(ten + 10 * M, 30 * S)
    # the two observations lead to different prices / outcomes
    bars = {ten + i * M: {"t": ten + i * M, "o": 100.0 + (5.0 if i >= 15 else 0.0), "h": 106.0, "l": 99.0,
                          "c": 100.0 + (5.0 if i >= 15 else 0.0), "avail": ten + (i + 1) * M} for i in range(600)}
    design = {"id": "C1", "_version": "ev-repro"}
    with tempfile.TemporaryDirectory() as base:
        ctx_a = {"frozen": {}, "last_cutoff": None, "new": [], "design": design}
        run_module(liq_exposure, [rec20], ten + 25 * M, ctx_a, base, write=True)       # writer A stores :20
        ctx_b = {"frozen": {}, "last_cutoff": None, "new": [], "design": design}      # worker B: stale context
        ctl, diag = run_module(liq_exposure, [rec10, rec20], ten + 40 * M, ctx_b, base, write=True)
        stored = controls.load_selections(base, design)
    s = stored.get(ten)
    lab = lambda c: outcomes.label(c["t_available"], 1, bars, ten + 10 * H, (60,))[60].get("ret_net")
    used = (ctl or [None])[0] if isinstance(ctl, list) else None
    return {"repro": "authoritative stored selection", "stored_winner_source": iso(s["t_event"]) if s else None,
            "stored_winner_t_persisted": iso(s.get("t_persisted")) if s else None,
            "returned_control_source": iso(used["t_event"]) if used else diag,
            "returned_t_persisted": iso(used.get("t_persisted")) if used else None,
            "returned_equals_stored": bool(used and s and json.dumps(used, sort_keys=True) == json.dumps(s, sort_keys=True)),
            "label_60m_of_returned": round(lab(used), 6) if used else None,
            "label_60m_of_stored_winner": round(lab(s), 6) if s else None,
            "context_after_B_names_winner": (ctx_b.get("frozen") or {}).get(ten, {}).get("t_event") == (s or {}).get("t_event"),
            "diag": {k: diag.get(k) for k in ("proposals_accepted", "proposals_superseded", "used_equals_stored")}
            if isinstance(diag, dict) else diag}


if __name__ == "__main__":
    print(json.dumps({"code_root": str(ROOT), "policy": controls.POLICY}))
    for f in (repro_cutoff, repro_authority):
        try:
            print(json.dumps(f(), default=str))
        except Exception as exc:
            print(json.dumps({"repro": f.__name__, "error": f"{type(exc).__name__}: {exc}"}))
