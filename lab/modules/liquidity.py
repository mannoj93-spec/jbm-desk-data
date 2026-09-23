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

Timing contract (lab-2.0; the service's own sampling is described in stream/README.md):
  slot      every stored 1-second sample is assigned to the nearest whole second,
            slot = round(t / 1000), and kept only if |t - slot x 1000| <= SLOT_TOLERANCE_MS (250 ms).
            The service wakes on the second boundary, so real samples carry a few ms of jitter.
  duplicates two samples in one slot: the one closest to the slot boundary wins (then the earlier
            t, then the earlier book timestamp) - deterministic, independent of file order.
  freshness a sample whose book_age_ms exceeds FRESH_MS (2 s) is stale and treated as missing,
            as is a sample without book_age_ms. Missing slots are never filled from neighbours.
  availability a sample can be used from t + FLUSH_ASSUMED_MS (5 s, the service's flush interval,
            an assumption); a decision's t_inputs is the latest such time among the samples read.
  controls  the slot on each whole hour.
Original t, book_ts and book_age_ms of the samples an event used are kept in its features.
"""
import gzip
import json
import os
from pathlib import Path

from lab.asof import decide
from lab.common import BASIS_PROSPECTIVE, H, MINUTE, hash_inputs
from lab.events import event_record

ID = "liquidity_recovery"
SLOT_TOLERANCE_MS = 250
FRESH_MS = 2000
FLUSH_ASSUMED_MS = 5000
VERSION = "E-2"
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


def read_rows(root, venue, inst):
    base = root / "derived/book1s" / venue / inst
    rows = []
    for p in sorted(base.glob("*/*.jsonl.gz")):
        try:
            text = gzip.decompress(p.read_bytes()).decode()
        except (OSError, EOFError):
            text = _salvage(p)                     # a partition being written: keep the complete members
        rows.extend(json.loads(line) for line in text.splitlines() if line.strip())
    return rows


def slot_samples(rows, tolerance_ms=SLOT_TOLERANCE_MS, fresh_ms=FRESH_MS):
    """({slot_second: sample}, counts). See the timing contract in the module docstring."""
    counts = {"rows": len(rows), "unslotted": 0, "stale": 0, "duplicates": 0}
    best = {}
    for r in rows:
        slot = (r["t"] + 500) // 1000
        off = abs(r["t"] - slot * 1000)
        if off > tolerance_ms:
            counts["unslotted"] += 1
            continue
        age = r.get("book_age_ms")
        if age is None or age > fresh_ms:
            counts["stale"] += 1
            continue
        rank = (off, r["t"], r.get("book_ts") or 0)
        if slot in best:
            counts["duplicates"] += 1
            if rank >= best[slot][0]:
                continue
        best[slot] = (rank, r)
    return {k: v[1] for k, v in best.items()}, counts


def load_samples(root, venue, inst):
    return slot_samples(read_rows(root, venue, inst))


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


def build(slots, gaps, params, code, basis=BASIS_PROSPECTIVE):
    """`slots` maps whole seconds to samples (slot_samples). Returns (events, controls, coverage)."""
    import bisect
    shock, recover, rec_s = params["shock_frac"], params["recover_frac"], params["recovery_s"]
    secs = sorted(slots)
    depth = {k: (slots[k]["bid_depth_10bp"] or 0) + (slots[k]["ask_depth_10bp"] or 0) for k in secs}
    events, controls = [], []
    cov = {"samples": len(secs), "shocks": 0, "skipped_coverage": 0, "skipped_gap": 0, "late_inputs": 0,
           "events": 0, "controls": 0}
    window = 1800
    last_event_end = None
    meds = {}
    avail = lambda k: slots[k]["t"] + FLUSH_ASSUMED_MS

    def medians(minute_s):
        """(total, bid, ask) medians, sample count and latest availability over [minute - 30 min, minute)."""
        if minute_s not in meds:
            a, b = bisect.bisect_left(secs, minute_s - window), bisect.bisect_left(secs, minute_s)
            w = secs[a:b]
            if len(w) < 0.9 * window:
                meds[minute_s] = None
            else:
                mid = len(w) // 2
                meds[minute_s] = (sorted(depth[x] for x in w)[mid],
                                  sorted(slots[x]["bid_depth_10bp"] or 0 for x in w)[mid],
                                  sorted(slots[x]["ask_depth_10bp"] or 0 for x in w)[mid], len(w),
                                  max(avail(x) for x in w))
        return meds[minute_s]
    for k in secs:
        m = medians(k // 60 * 60)
        if m is None:
            continue
        med, bid_med, ask_med, n_prior, med_avail = m
        s = slots[k]
        if k % 3600 == 0:
            t_av, excluded = decide(k * 1000, max(avail(k), med_avail))
            if not excluded:
                controls.append(event_record(ID + ":control", VERSION, k * 1000, s["t"], t_av, 1, "control",
                                             {"depth_ratio": depth[k] / med if med else None, "sample_t": s["t"]},
                                             hash_inputs([k, depth[k]]), basis, {}, {}, code,
                                             t_inputs=max(avail(k), med_avail)))
                cov["controls"] += 1
        if med <= 0 or depth[k] >= shock * med or (last_event_end is not None and k <= last_event_end):
            continue
        cov["shocks"] += 1
        end = k + rec_s
        need = list(range(k + 1, end + 1))
        if any(x not in slots for x in need):
            cov["skipped_coverage"] += 1            # a missing or stale second is missing, never quiet
            last_event_end = end
            continue
        if any(gs is not None and ge is not None and gs <= end * 1000 and ge >= (k - window) * 1000
               for gs, ge in gaps):
            cov["skipped_gap"] += 1
            last_event_end = end
            continue
        t_inputs = max([med_avail, avail(k)] + [avail(x) for x in need])
        t_av, excluded = decide(end * 1000, t_inputs)
        if excluded:
            cov["late_inputs"] += 1
            last_event_end = end
            continue
        rec_at = next((x for x in need if depth[x] >= recover * med), None)
        bid_loss = 1 - (s["bid_depth_10bp"] or 0) / bid_med if bid_med else 0
        ask_loss = 1 - (s["ask_depth_10bp"] or 0) / ask_med if ask_med else 0
        direction = -1 if bid_loss >= ask_loss else 1
        feats = {"depth_ratio": depth[k] / med, "median_depth_30m": med, "bid_loss": bid_loss, "ask_loss": ask_loss,
                 "recovery_s": (rec_at - k) if rec_at else None, "severity": 1 - depth[k] / med,
                 "spread_bp": (s["ask"] - s["bid"]) / s["mid"] * 1e4,
                 "shock_sample": {"t": s["t"], "book_ts": s.get("book_ts"), "book_age_ms": s.get("book_age_ms")}}
        events.append(event_record(ID, VERSION, end * 1000, s["t"], t_av, direction,
                                   "fast" if rec_at else "slow", feats,
                                   hash_inputs([[x, depth[x]] for x in [k] + need]), basis,
                                   {"trailing_samples": n_prior}, {"book": "valid, fresh samples only"}, code,
                                   t_inputs=t_inputs))
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
    slots, counts = load_samples(root, venue, inst)
    gaps = load_gaps(root, venue, inst)
    events, controls, cov = build(slots, gaps, params, lab.code)
    cov.update(counts, venue=venue, instrument=inst, recorded_gaps=len(gaps))
    reasons = []
    span_h = (max(slots) - min(slots)) / 3600 if slots else 0
    if span_h < 24 * 7:
        reasons.append(f"{span_h:.1f} hours of 1-second samples; a first read needs about a week")
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls, "bars": bars,
                                      "coverage": cov, "state": "available" if not reasons else "insufficient_data",
                                      "reasons": reasons}]}
