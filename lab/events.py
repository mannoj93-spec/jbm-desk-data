"""Event records, episode collapse and scheduled controls.

A detector fires at t_event using only inputs available by t_available. Firings of the same
detector and direction closer together than the collapse window form one EPISODE; only the
first firing (the head) is an independent decision, and its episode records how many firings it
absorbed. Adaptive sampling and cascades therefore cannot multiply the sample count. Controls are
ordinary scheduled observations (every hour on the hour by default) labelled with the same
outcome code, and are never selected by the detector.
"""
from lab.common import H, LAB_VERSION, digest


def event_record(detector, version, t_event, t_first_observed, t_available, direction, group, features,
                 inputs_sha256, basis, coverage, quality, code):
    rec = {"detector": detector, "detector_version": version, "lab_version": LAB_VERSION, "code_sha256": code,
           "t_event": t_event, "t_first_observed": t_first_observed, "t_available": t_available,
           "direction": direction, "group": group, "features": features, "inputs_sha256": inputs_sha256,
           "basis": basis, "coverage": coverage, "quality": quality}
    if t_available < t_event:
        raise ValueError("an event cannot be available before it happens")
    rec["event_id"] = digest([detector, version, t_event, direction, group])[:16]
    return rec


def collapse(events, window_ms, key=lambda e: (e["detector"], e["direction"])):
    """Assign episode ids; returns the list of heads (one per episode). Chronological, causal: an
    event joins the running episode if it fires within window_ms of the episode's LAST firing."""
    heads, open_ep = [], {}
    for e in sorted(events, key=lambda x: (x["t_event"], x["event_id"])):
        k = key(e)
        ep = open_ep.get(k)
        if ep and e["t_event"] - ep["last"] <= window_ms:
            ep["last"] = e["t_event"]
            ep["head"]["episode_size"] += 1
            e["episode_id"] = ep["head"]["event_id"]
            e["episode_head"] = False
            continue
        e["episode_id"] = e["event_id"]
        e["episode_head"] = True
        e["episode_size"] = 1
        open_ep[k] = {"last": e["t_event"], "head": e}
        heads.append(e)
    return heads


def control_times(start, end, every=H):
    first = -(-start // every) * every
    return list(range(first, end, every))


def hourly_controls(bars, detector, version, code, basis, direction=1):
    """Controls at every stored hour boundary: availability is the bar's own availability."""
    from lab.common import PROCESSING_LATENCY_MS
    out = []
    for t in sorted(bars):
        if (t + 60_000) % H == 0:
            b = bars[t]
            out.append(event_record(detector + ":control", version, t + 60_000, b["avail"],
                                    b["avail"] + PROCESSING_LATENCY_MS, direction, "control", {}, digest([t]), basis,
                                    {}, {}, code))
    return out
