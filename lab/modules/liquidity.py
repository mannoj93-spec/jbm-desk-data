"""Module E - liquidity shock and recovery (needs the streaming service).

Input: the streaming collector's 1-second top-of-book samples
  $STREAM_DATA_DIR/derived/book1s/<venue>/<instrument>/<YYYY-MM-DD>/<HH>.jsonl.gz
(bid, ask, displayed depth within 10 bp of mid on each side, book timestamp) and its gap log
  $STREAM_DATA_DIR/derived/gaps/<YYYY-MM-DD>.jsonl.
Samples are written only while the reconstructed book is valid and fresh, so a missing second is
MISSING (a disconnect, sequence gap or stale book), never a quiet book. The 15-minute GitHub
collector cannot observe second-scale depth, so without the streaming service this module reports
"unavailable" and produces nothing.

Displayed depth is advertisement, not transacted liquidity; nothing here infers intent or hidden
orders from it.
Event: at second s, total depth within 10 bp (bid + ask) falls below shock_frac x its trailing
30-minute median (recomputed at each minute boundary from samples strictly before that minute, so
it never includes s itself). The decision is made at
t_event = s + recovery_s, when it is known whether depth recovered to >= recover_frac x that
median within recovery_s: group "slow" (not recovered; the test group) or "fast" (recovered).
Direction: -1 when the bid side lost the larger share of its median depth, +1 when the ask side did.
A shock needs >= 90% of the trailing 30 minutes and every second of the recovery window present,
and no recorded gap overlapping them; otherwise it is skipped and counted.
Outcome: the lab's standard labels on Binance USD-M BTCUSDT 1-minute bars stored by the collector.
"""
import gzip
import json
import os
from pathlib import Path

from lab.common import BASIS_PROSPECTIVE, H, MINUTE, PROCESSING_LATENCY_MS, hash_inputs
from lab.events import event_record

ID = "liquidity_recovery"
VERSION = "E-1"
SPEC = {"module": "E", "id": ID, "version": VERSION, "title": "Liquidity shock and recovery",
        "hypothesis": "After a displayed-depth shock, books that fail to refill within a minute are followed by "
                      "different returns (in the depleted side's direction) than books that refill quickly.",
        "inputs": ["streaming service derived/book1s (1-second top of book, depth within 10 bp)",
                   "streaming service derived/gaps", "binance_klines_1m_BTCUSDT_perp (outcomes)"],
        "event": "depth within 10 bp < shock_frac x trailing 30-min median; slow if not back to recover_frac "
                 "x median within recovery_s",
        "outcome": "net log return in the depleted side's direction",
        "baseline": "fast-recovery shocks; hourly controls from the same samples; regression on prior 60m "
                    "return and volatility",
        "exclusions": ["shocks whose trailing window is < 90% covered or whose recovery window has any "
                       "missing second or recorded gap", "Hyperliquid books (pushed every ~5 s; not second-scale)"]}


def stream_root():
    root = os.environ.get("STREAM_DATA_DIR")
    return Path(root) if root else None


def load_samples(root, venue, inst, start=None, end=None):
    """{t_ms: sample} for one book, from every hourly partition present."""
    base = root / "derived/book1s" / venue / inst
    out = {}
    for p in sorted(base.glob("*/*.jsonl.gz")):
        try:
            text = gzip.decompress(p.read_bytes()).decode()
        except (OSError, EOFError):
            text = _salvage(p)                     # a partition being written: keep the complete members
        for line in text.splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if (start is None or r["t"] >= start) and (end is None or r["t"] < end):
                out[r["t"]] = r
    return out


def _salvage(p):
    lines = []
    try:
        with gzip.open(p, "rt") as fh:
            for line in fh:
                lines.append(line)
    except (OSError, EOFError):
        pass
    return "".join(l for l in lines if l.endswith("\n"))


def load_gaps(root, venue, inst):
    gaps = []
    for p in sorted((root / "derived/gaps").glob("*.jsonl")):
        for line in p.read_text().splitlines():
            if not line.strip():
                continue
            g = json.loads(line)
            if g["venue"] in (venue, "service") and g.get("instrument") in (None, inst):
                s, e = g.get("start"), g.get("end")
                gaps.append((s if s is not None else e, e if e is not None else s))
    return gaps


def build(samples, gaps, params, code, basis=BASIS_PROSPECTIVE):
    shock, recover, rec_s = params["shock_frac"], params["recover_frac"], params["recovery_s"]
    ts = sorted(samples)
    depth = {t: (samples[t]["bid_depth_10bp"] or 0) + (samples[t]["ask_depth_10bp"] or 0) for t in ts}
    events, controls = [], []
    cov = {"samples": len(ts), "shocks": 0, "skipped_coverage": 0, "skipped_gap": 0, "events": 0, "controls": 0}
    window = 1800
    last_event_end = None
    import bisect
    meds = {}

    def medians(minute):
        """(total, bid, ask) medians and sample count over [minute - 30 min, minute)."""
        if minute not in meds:
            a, b = bisect.bisect_left(ts, minute - window * 1000), bisect.bisect_left(ts, minute)
            w = ts[a:b]
            if len(w) < 0.9 * window:
                meds[minute] = None
            else:
                mid = len(w) // 2
                meds[minute] = (sorted(depth[x] for x in w)[mid],
                                sorted(samples[x]["bid_depth_10bp"] or 0 for x in w)[mid],
                                sorted(samples[x]["ask_depth_10bp"] or 0 for x in w)[mid], len(w))
        return meds[minute]
    for t in ts:
        m = medians(t // MINUTE * MINUTE)
        if m is None:
            continue
        med, bid_med, ask_med, n_prior = m
        s = samples[t]
        if t % H == 0:
            controls.append(event_record(ID + ":control", VERSION, t, t, t + PROCESSING_LATENCY_MS, 1, "control",
                                         {"depth_ratio": depth[t] / med if med else None}, hash_inputs([t, depth[t]]),
                                         basis, {}, {}, code))
            cov["controls"] += 1
        if med <= 0 or depth[t] >= shock * med or (last_event_end is not None and t <= last_event_end):
            continue
        cov["shocks"] += 1
        end = t + rec_s * 1000
        need = [t + k * 1000 for k in range(1, rec_s + 1)]
        if any(x not in samples for x in need):
            cov["skipped_coverage"] += 1
            last_event_end = end
            continue
        if any(gs is not None and ge is not None and gs <= end and ge >= t - window * 1000 for gs, ge in gaps):
            cov["skipped_gap"] += 1
            last_event_end = end
            continue
        rec_at = next((x for x in need if depth[x] >= recover * med), None)
        bid_loss = 1 - (s["bid_depth_10bp"] or 0) / bid_med if bid_med else 0
        ask_loss = 1 - (s["ask_depth_10bp"] or 0) / ask_med if ask_med else 0
        direction = -1 if bid_loss >= ask_loss else 1
        feats = {"depth_ratio": depth[t] / med, "median_depth_30m": med, "bid_loss": bid_loss, "ask_loss": ask_loss,
                 "recovery_s": (rec_at - t) / 1000 if rec_at else None,
                 "spread_bp": (s["ask"] - s["bid"]) / s["mid"] * 1e4}
        events.append(event_record(ID, VERSION, end, t, end + PROCESSING_LATENCY_MS, direction,
                                   "fast" if rec_at else "slow", feats,
                                   hash_inputs([[x, depth[x]] for x in [t] + need]), basis,
                                   {"trailing_samples": n_prior}, {"book": "valid, fresh samples only"}, code))
        cov["events"] += 1
        last_event_end = end
    return events, controls, cov


def run(lab, params):
    root = stream_root()
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    venue, inst = params.get("venue", "bybit"), params.get("instrument", "BTCUSDT")
    if root is None or not (root / "derived/book1s").exists():
        return {"module": ID, "passes": [{"basis": "prospective", "events": [], "controls": [], "bars": bars,
                                          "coverage": {"stream_data_dir": str(root) if root else None},
                                          "state": "unavailable",
                                          "reasons": ["streaming service not deployed or its data not mounted "
                                                      "(STREAM_DATA_DIR); second-scale depth is not observable "
                                                      "by the 15-minute collector"]}]}
    samples = load_samples(root, venue, inst)
    gaps = load_gaps(root, venue, inst)
    events, controls, cov = build(samples, gaps, params, lab.code)
    cov.update(venue=venue, instrument=inst, recorded_gaps=len(gaps))
    reasons = []
    span_h = (max(samples) - min(samples)) / H if samples else 0
    if span_h < 24 * 7:
        reasons.append(f"{span_h:.1f} hours of 1-second samples; a first read needs about a week")
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls, "bars": bars,
                                      "coverage": cov, "state": "available" if not reasons else "insufficient_data",
                                      "reasons": reasons}]}
