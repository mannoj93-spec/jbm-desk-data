"""Event records, episode collapse and scheduled controls.

A detector fires at t_event using only inputs available by t_inputs (see lab/asof.py for every
time field). Firings of the same detector, direction and decision key closer together than the
collapse window form one EPISODE; only its first firing (the head) is a decision, and the episode
records how many firings it absorbed. Episodes are the unit that is labelled; they are NOT
independent observations - overlap and dependence are handled later, on the label intervals
(lab/experiments.py). Controls are scheduled observations (every hour on the hour), never
selected by a detector.
"""
from lab.asof import ASSUMED_PROCESSING_MS
from lab.common import H, LAB_VERSION, digest


def event_record(detector, version, t_event, t_first_observed, t_available, direction, group, features,
                 inputs_sha256, basis, coverage, quality, code, t_inputs=None, key=None):
    """`t_available` is the assumed decision time (t_inputs + ASSUMED_PROCESSING_MS when t_inputs is
    given). `key` distinguishes simultaneous decisions of one detector (e.g. the alt in module G);
    the event's decision_key does not include its group, so a later recomputation that would put
    the same decision in a different group is recognised as a revision of that decision."""
    if t_available is None or t_available < t_event:
        raise ValueError("an event cannot be available before it happens")
    rec = {"detector": detector, "detector_version": version, "lab_version": LAB_VERSION, "code_sha256": code,
           "t_event": t_event, "t_first_observed": t_first_observed, "t_inputs": t_inputs,
           "t_available": t_available, "assumed_processing_ms": ASSUMED_PROCESSING_MS if t_inputs is not None else None,
           "direction": direction, "group": group, "features": features, "inputs_sha256": inputs_sha256,
           "basis": basis, "coverage": coverage, "quality": quality}
    rec["decision_key"] = digest([detector, version, t_event, direction, key])[:16]
    rec["event_id"] = digest([detector, version, t_event, direction, group, key])[:16]
    return rec


def collapse(events, window_ms, key=lambda e: (e["detector"], e["direction"])):
    """Assign episode ids; returns the list of heads (one per episode). Chronological, causal: an
    event joins the running episode if it fires within window_ms of the episode's LAST firing.
    Ties are broken by event_id, never by anything outcome-related."""
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


def collapse_as_known(events, window_ms, key, known):
    """Episodes built in the order the decisions became KNOWN (lab-2.1): events are taken by
    (known(e), t_event, event_id); an event joins an existing episode of its key when its t_event
    lies within window_ms of that episode's firings ([first - window, last + window]; within an
    episode consecutive firings are at most window_ms apart), otherwise it heads a new episode. When
    every event has the same knowledge time this is exactly collapse(). A decision learned later -
    e.g. one whose inputs arrived late, frozen by a later lab run - can join an episode but never
    displaces its head, merges two episodes, or removes an observation that was already known."""
    heads, eps = [], {}
    for e in sorted(events, key=lambda x: (known(x), x["t_event"], x["event_id"])):
        k, t = key(e), e["t_event"]
        ep = next((x for x in eps.get(k, []) if x["first"] - window_ms <= t <= x["last"] + window_ms), None)
        if ep is not None:
            ep["first"], ep["last"] = min(ep["first"], t), max(ep["last"], t)
            ep["head"]["episode_size"] += 1
            e["episode_id"] = ep["head"]["event_id"]
            e["episode_head"] = False
            continue
        e["episode_id"] = e["event_id"]
        e["episode_head"] = True
        e["episode_size"] = 1
        eps.setdefault(k, []).append({"first": t, "last": t, "head": e})
        heads.append(e)
    return sorted(heads, key=lambda x: (x["t_event"], x["event_id"]))


def control_times(start, end, every=H):
    first = -(-start // every) * every
    return list(range(first, end, every))


def hourly_controls(bars, detector, version, code, basis, direction=1):
    """Controls at every stored hour boundary. Their only input is the bar that closes at the hour,
    so t_inputs is that bar's availability."""
    out = []
    for t in sorted(bars):
        if (t + 60_000) % H == 0:
            b = bars[t]
            t_in = max(b["avail"], t + 60_000)
            out.append(event_record(detector + ":control", version, t + 60_000, b["avail"],
                                    t_in + ASSUMED_PROCESSING_MS, direction, "control", {}, digest([t]), basis,
                                    {}, {}, code, t_inputs=t_in))
    return out
