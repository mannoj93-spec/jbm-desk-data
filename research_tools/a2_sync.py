"""A2 synchronized spot/perp flow: the join and timeout on actual arrival clocks (a2-sync-0.1.0, repo 2.30; PREPARED
successor of A1, brief section 15). A1 is frozen and unchanged: a spot observation that arrives after A1's decision
clock stays ineligible under A1.

Clocks are the collector's own: a 1m bar's availability is max(batch observed_at, bar close) (lab/data.Store 'avail').
For each decision window (the same WINDOW closed minutes on both venues, open-time aligned):
  perp_avail     the latest availability of the window's perp bars
  spot_avail     the latest availability of the window's spot bars (None if any spot bar is missing)
  synchronized   spot_avail - perp_avail <= join_timeout_ms: t_decision = max(perp_avail, spot_avail)
  timeout        spot later than the timeout, or missing: t_decision = perp_avail + join_timeout_ms; the decision is
                 a perp-only decision in its own labelled group, never pooled with synchronized ones
Signal (both groups): combined taker imbalance I = sum(2 tbv - v) over the window (perp + spot when synchronized,
perp only otherwise) relative to the window's traded volume; |I| >= signal_threshold gives direction sign(I).
Outcome: the sign of the forward log return over horizon_min from the open of the first perp bar at or after
t_decision + processing_assumed_ms. The processing delay is ASSUMED (protocol value), never measured here; measured
inference/publication time is a separate object.
Matched control: the perp-only signal for the SAME window evaluated at perp_avail (what A1's clock would have used),
so the comparison isolates information gained against delay paid.
Report: share synchronized, the delay distribution (t_decision - perp_avail), hit rates of synchronized combined
signals versus their matched perp-only controls on the same windows, and the timeout group separately.
"""
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "a2-sync-0.1.0"
MIN = 60_000
DEFAULTS = {"window_min": 5, "join_timeout_ms": 5000, "signal_threshold": 0.15, "horizon_min": 15,
            "processing_assumed_ms": 60_000}


def join(perp, spot, start_ms, end_ms, p=None):
    """Decisions for every window start in [start, end) stepping by the window. perp/spot: {open_ms: bar} with
    keys o, c, v, tbv, avail (lab/data.Store.bars)."""
    p = dict(DEFAULTS, **(p or {}))
    w = p["window_min"]
    out = []
    t = (start_ms + w * MIN - 1) // (w * MIN) * (w * MIN)
    while t + w * MIN <= end_ms:
        pb = [perp.get(t + k * MIN) for k in range(w)]
        sb = [spot.get(t + k * MIN) for k in range(w)]
        if any(b is None or b.get("avail") is None for b in pb):
            out.append({"t": t, "group": "perp-missing", "decision": None})
            t += w * MIN
            continue
        pa = max(b["avail"] for b in pb)
        sa = None if any(b is None or b.get("avail") is None for b in sb) else max(b["avail"] for b in sb)
        if sa is not None and sa - pa <= p["join_timeout_ms"]:
            group, td = "synchronized", max(pa, sa)
        else:
            group, td = ("timeout" if sa is not None else "spot-missing"), pa + p["join_timeout_ms"]
        out.append({"t": t, "group": group, "perp_avail": pa, "spot_avail": sa, "t_decision": td,
                    "delay_ms": td - pa, "signal": _signal(pb, sb if group == "synchronized" else None, p),
                    "control_signal": _signal(pb, None, p)})
        t += w * MIN
    return out


def _signal(pb, sb, p):
    bars = pb + (sb or [])
    vol = sum(b["v"] for b in bars)
    if vol <= 0:
        return 0
    imb = sum(2 * b["tbv"] - b["v"] for b in bars) / vol
    return (1 if imb > 0 else -1) if abs(imb) >= p["signal_threshold"] else 0


def outcome(perp, t_ms, p=None):
    p = dict(DEFAULTS, **(p or {}))
    t0 = (t_ms + p["processing_assumed_ms"] + MIN - 1) // MIN * MIN
    a, b = perp.get(t0), perp.get(t0 + (p["horizon_min"] - 1) * MIN)
    if a is None or b is None:
        return None
    r = math.log(b["c"] / a["o"])
    return 1 if r > 0 else -1 if r < 0 else 0


def evaluate(decisions, perp, p=None):
    """Information gained versus delay paid."""
    p = dict(DEFAULTS, **(p or {}))
    groups = {}
    for d in decisions:
        groups[d["group"]] = groups.get(d["group"], 0) + 1
    sync = [d for d in decisions if d["group"] == "synchronized"]
    delays = sorted(d["delay_ms"] for d in decisions if d.get("delay_ms") is not None)

    def hits(rows, key, clock):
        h = n = 0
        for d in rows:
            s = d[key]
            if not s:
                continue
            o = outcome(perp, d[clock], p)
            if o is None:
                continue
            n += 1
            h += (o == s)
        return {"n": n, "hit_rate": round(h / n, 4) if n else None}
    return {"version": VERSION, "params": p, "groups": groups,
            "share_synchronized": round(len(sync) / len(decisions), 4) if decisions else None,
            "delay_ms": {"median": delays[len(delays) // 2] if delays else None, "max": delays[-1] if delays else None},
            "synchronized_combined": hits(sync, "signal", "t_decision"),
            "matched_perp_only_control": hits(sync, "control_signal", "perp_avail"),
            "timeout_group_perp_only": hits([d for d in decisions if d["group"] in ("timeout", "spot-missing")],
                                            "signal", "t_decision"),
            "note": "processing delay assumed, not measured; windows overlap in outcome horizon: not independent"}
