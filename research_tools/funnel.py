"""Per-feature admission funnel (funnel-1.0.0, repo 2.29; brief section 9).

For every decision time and every input a feature reads, one stage is recorded - the first one that fails, or
'retained':
  source-missing          no stored record for that event time at all ("missing entirely")
  invalid-capture         a record exists but its value is malformed (desk evidence contract)
  availability-unknown    the record carries no observed_at: never admitted, never back-dated to its event time
  arrived-after-decision  stored, valid, but first available after the decision cutoff (A1's optional spot flow)
  transform-ineligible    available, but the transformation cannot use it (window incomplete, denominator invalid)
  retained                used by the decision
Distributions, not examples: arrival_lags() gives the full distribution of one dataset's availability minus
another's for the same event minute (spot after perp), with counts and cutoffs.

A1 stays frozen. Nothing here admits a later spot observation into an A1 decision; the funnel only measures why
stored data was ineligible. A synchronized-input successor is a separate registration (research/registrations/
a2-synchronized-prepared/).
"""
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lab.common import MINUTE, iso  # noqa: E402
from research_tools import evidence_contract as E  # noqa: E402

VERSION = "funnel-1.0.0"
STAGES = ("source-missing", "invalid-capture", "availability-unknown", "arrived-after-decision",
          "transform-ineligible", "retained")


def _q(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def summarize(values):
    return {"n": len(values), "median": _q(values, 0.5), "p10": _q(values, 0.1), "p90": _q(values, 0.9),
            "min": min(values) if values else None, "max": max(values) if values else None}


def stage(record, decision_cutoff, field=None, domain=None, transform_ok=True):
    """The funnel stage of one input record for one decision. record: a stored row with 'avail' (lab/data.Store)
    or None."""
    if record is None:
        return "source-missing"
    if field is not None:
        _, st = E.number(record.get(field), domain)
        if st != "ok":
            return "invalid-capture"
    if record.get("avail") is None:
        return "availability-unknown"
    if record["avail"] > decision_cutoff:
        return "arrived-after-decision"
    if not transform_ok:
        return "transform-ineligible"
    return "retained"


def funnel(decisions, inputs):
    """decisions: [(decision_id, cutoff_ms, {input_name: (record_or_None, field, domain, transform_ok)})].
    Returns per-input stage counts and the precise exclusion reason per decision."""
    counts = {name: Counter() for name in inputs}
    rows = []
    for did, cutoff, recs in decisions:
        row = {"decision": did, "cutoff_utc": iso(cutoff)}
        for name in inputs:
            rec, field, domain, ok = recs.get(name, (None, None, None, True))
            s = stage(rec, cutoff, field, domain, ok)
            counts[name][s] += 1
            row[name] = s
        rows.append(row)
    return {"version": VERSION, "stages": STAGES, "counts": {k: dict(v) for k, v in counts.items()}, "rows": rows}


def arrival_lags(bars_a, bars_b, start, end):
    """Availability of dataset b minus dataset a for each event minute both hold in [start, end) (ms). From
    lab/data.Store.bars() maps. Positive: b arrived later."""
    lags = [bars_b[t]["avail"] - bars_a[t]["avail"] for t in range(start, end, MINUTE) if t in bars_a and t in bars_b]
    only_a = sum(1 for t in range(start, end, MINUTE) if t in bars_a and t not in bars_b)
    only_b = sum(1 for t in range(start, end, MINUTE) if t in bars_b and t not in bars_a)
    s = summarize(lags)
    s.update(later_share=(sum(1 for x in lags if x > 0) / len(lags)) if lags else None, only_first=only_a,
             only_second=only_b, window=[iso(start), iso(end)])
    return s


def a1_spot_funnel(store, start, end, window=5):
    """For each minute in [start, end): would A1's optional spot flow over the last `window` minutes have been
    eligible when the required perp window was? Mirrors the frozen rule in lab/modules/flow_absorption.py
    (spot used only if every spot bar it reads was available by the perp inputs' time); measures, never changes it."""
    perp = store.bars("binance_klines_1m_BTCUSDT_perp")
    spot = store.bars("binance_klines_1m_BTCUSDT_spot")
    counts, delays = Counter(), []
    for t in range(start + window * MINUTE, end, MINUTE):
        pw = [perp.get(t - k * MINUTE) for k in range(window)]
        if any(b is None for b in pw):
            counts["perp-window-incomplete (no decision)"] += 1
            continue
        t_inputs = max(b["avail"] for b in pw)
        sw = [spot.get(t - k * MINUTE) for k in range(window)]
        if any(b is None for b in sw):
            counts["source-missing"] += 1
            continue
        late = max(b["avail"] for b in sw)
        if late > t_inputs:
            counts["arrived-after-decision"] += 1
            delays.append(late - t_inputs)
        else:
            counts["retained"] += 1
    return {"version": VERSION, "rule": "A1 frozen optional-spot rule (flow_absorption.py lines 111-114)",
            "window": [iso(start), iso(end)], "counts": dict(counts),
            "spot_delay_after_decision_ms": summarize(delays)}
