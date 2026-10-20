"""Replenishment / recovery speed after depth depletion: adapter and feature contract (replenishment-0.1.0, repo 2.30;
PREPARED - brief section 14, family 3). The E1 recorder (stream/) is not commissioned, so no live data exists; this
module fixes what the feature means and how it is read, and is tested on fixtures in the recorder's own format.

Why a contract, not a panel feature: true replenishment needs sequence-valid order-book evidence at second scale.
The collector's depth snapshots (~12 minutes apart) cannot show how fast depth refills, so read() refuses a source
whose sampling is sparser than MAX_SAMPLE_GAP_S or that does not come from a sequence-checked book.

Source (stream/ recorder layout): derived/book1s/<venue>/<instrument>/<day>/<HH>.jsonl.gz rows
{t, mid, bid_depth_10bp, ask_depth_10bp, book_age_ms}; derived/gaps/<day>.jsonl (disconnects, sequence gaps,
restarts). Acceptance of the underlying data is stream/pilot_acceptance.py (raw replay, clock, gaps).

Definition (CONTRACT, hashed into every output), per side (bid, ask):
  baseline      median depth within 10 bp over the BASELINE_S seconds before the event
  depletion     depth falls to <= (1 - DEPLETION) x baseline within DEPLETION_WINDOW_S seconds
  recovery_s    seconds from the depletion trough until depth is back to >= RECOVERY x baseline; censored (state
                'not-recovered') after MAX_RECOVERY_S
  states        ok | not-recovered | gap-in-window (any recorder gap or missing/stale second inside baseline,
                depletion or recovery) | insufficient-baseline | source-not-sequence-valid
  units         seconds; depth in BTC within 10 bp of mid
"""
import gzip
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research_tools import evidence_contract as E  # noqa: E402

VERSION = "replenishment-0.1.0"
CONTRACT = {"baseline_s": 300, "depletion": 0.5, "depletion_window_s": 30, "recovery": 0.9, "max_recovery_s": 600,
            "max_book_age_ms": 2000, "max_sample_gap_s": 2, "band": "10 bp of mid", "sides": ["bid", "ask"]}
MAX_SAMPLE_GAP_S = CONTRACT["max_sample_gap_s"]


def contract_sha256():
    return E.content_sha256(CONTRACT)


def read(root, venue, instrument, day, hours=None, sequence_checked=True):
    """{second: (bid_depth, ask_depth)} of fresh samples, the gap intervals, and a source state. A source that is
    not a sequence-checked book, or whose samples are sparser than MAX_SAMPLE_GAP_S, is refused."""
    if not sequence_checked:
        return {"state": "source-not-sequence-valid", "samples": {}, "gaps": []}
    base = Path(root) / "derived/book1s" / venue / instrument / day
    samples = {}
    for p in sorted(base.glob("*.jsonl.gz")):
        if hours is not None and p.name[:2] not in hours:
            continue
        for line in gzip.decompress(p.read_bytes()).decode().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("book_age_ms") is None or r["book_age_ms"] > CONTRACT["max_book_age_ms"]:
                continue
            b, bs = E.number(r.get("bid_depth_10bp"), "nonneg")
            a, as_ = E.number(r.get("ask_depth_10bp"), "nonneg")
            if bs == "ok" and as_ == "ok":
                samples[int(round(r["t"] / 1000))] = (b, a)
    gaps = []
    gp = Path(root) / "derived/gaps" / f"{day}.jsonl"
    if gp.exists():
        for line in gp.read_text().splitlines():
            g = json.loads(line)
            if g.get("venue") in ("service", venue) and g.get("instrument") in (None, instrument):
                s, e = g.get("start") or g.get("end"), g.get("end") or g.get("start")
                gaps.append((int(s) // 1000, int(e) // 1000))
    ts = sorted(samples)
    sparse = sum(1 for a, b in zip(ts, ts[1:]) if b - a > MAX_SAMPLE_GAP_S)
    if ts and sparse > 0.5 * len(ts):
        return {"state": "source-not-sequence-valid", "reason": "samples too sparse for second-scale recovery",
                "samples": samples, "gaps": gaps}
    return {"state": "ok", "samples": samples, "gaps": gaps}


def _complete(src, a, b):
    s = src["samples"]
    if any(t not in s for t in range(a, b + 1)):
        return False
    return not any(g0 <= b and g1 >= a for g0, g1 in src["gaps"])


def recovery(src, t_event, side):
    """(state, record) for one depletion candidate at second t_event on one side."""
    c = CONTRACT
    k = 0 if side == "bid" else 1
    if src["state"] != "ok":
        return src["state"], None
    b0, b1 = t_event - c["baseline_s"], t_event - 1
    if not _complete(src, b0, b1):
        return "insufficient-baseline" if not all(t in src["samples"] for t in range(b0, b1 + 1)) else "gap-in-window", None
    base = statistics.median(src["samples"][t][k] for t in range(b0, b1 + 1))
    if base <= 0:
        return "insufficient-baseline", None
    if not _complete(src, t_event, t_event + c["depletion_window_s"]):
        return "gap-in-window", None
    window = [(t, src["samples"][t][k]) for t in range(t_event, t_event + c["depletion_window_s"] + 1)]
    trough_t, trough = min(window, key=lambda x: x[1])
    if trough > (1 - c["depletion"]) * base:
        return "no-depletion", None
    for t in range(trough_t, trough_t + c["max_recovery_s"] + 1):
        if t not in src["samples"] or any(g0 <= t <= g1 for g0, g1 in src["gaps"]):
            return "gap-in-window", None
        if src["samples"][t][k] >= c["recovery"] * base:
            return "ok", {"side": side, "baseline_btc": round(base, 4), "trough_btc": round(trough, 4),
                          "trough_t": trough_t, "recovery_s": t - trough_t, "contract_sha256": contract_sha256()}
    return "not-recovered", {"side": side, "baseline_btc": round(base, 4), "censored_at_s": c["max_recovery_s"]}
