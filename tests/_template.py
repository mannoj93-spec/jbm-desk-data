"""Copy to tests/<id>.py; fill every META field before committing.

run(ctx) -> {"episodes": [...], "notes": "..."}
Each episode requires:
  {"t_decision": UTC_ms, "input_cutoff": UTC_ms, "outcome_at": UTC_ms,
   "group": "cond" or "base", "outcome": finite_number}

input_cutoff <= t_decision; outcome_at >= t_decision + horizon_h; all must be
mature at report time. At most one episode per (group, t_decision) is accepted.
Collapse contiguous hits yourself and describe the method in META.

Signal inputs: ctx.as_of(t_decision).series(name), .snaps(), .liq_orders().
Only stamped rows available by the cutoff are exposed. Legacy rows without an
observed_at stamp are excluded. ctx.as_of(t).klines_1h(a,b) returns t/h/l/c and
never includes a price hour closing after t (historical availability not proven).
Use ctx.klines_1h for mature outcome labels, never for future signal features.
Custom Python is trusted code and can bypass these helpers; review is required.
"""
META = {
    "id": "OXX-HORIZON-v1",
    "hypothesis": "",
    "condition_def": "",
    "decision_time": "",
    "outcome_def": "",
    "baseline_def": "",
    "episode_collapse": "",
    "horizon_h": 24,
}


def run(ctx):
    return {"episodes": [], "notes": "template; replace with a frozen design"}
