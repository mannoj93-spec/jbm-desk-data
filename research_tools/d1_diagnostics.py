"""D1 (active TWAP) rejection funnel - measured reasons, read-only (d1-diagnostics-1.0.0, repo 2.29; brief section 11).

Separates universe scarcity from missed detection, missing data and rule rejection, per program, using the frozen
module's own program reconstruction (lab/modules/twap.programs) without changing it (editing the module would start a
new D1 evaluation version and restart its clock). Reasons, first that applies:
  not-btc                     the program's coin is not BTC (universe)
  fills-only                  seen only through TWAP-slice fills, never in twapHistory (no lifecycle observed)
  first-seen-not-active       first observation already finished/terminated: started and ended between polls
                              (missed detection by polling cadence) - not evidence the program was small
  price-unavailable           no BTC perp bar available at first observation (missing data)
  below-min-notional          active BTC program under the variant's min_notional_usd (rule rejection)
  qualifying                  would be a D1 event (the module then applies its decision-time rule)
The polling limit (each fixed-cohort account about every 8 hours) and the cohort size bound what can be seen; a
stream cannot create programs the eligible universe does not run.
"""
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VERSION = "d1-diagnostics-1.0.0"


def classify(progs, bars, min_notional_usd):
    out, rows = Counter(), []
    avails = sorted((b["avail"], t) for t, b in bars.items())
    import bisect
    keys = [a for a, _ in avails]
    for (user, tid), p in sorted(progs.items(), key=lambda kv: kv[1]["first_seen"]):
        first = p["statuses"][0][1] if p.get("statuses") else None
        if p.get("coin") != "BTC":
            r = "not-btc"
        elif p.get("from_fills_only") and not p.get("statuses"):
            r = "fills-only"
        elif first != "activated":
            r = "first-seen-not-active"
        else:
            i = bisect.bisect_right(keys, p["first_seen_avail"])
            px = bars[max(t for _, t in avails[max(0, i - 2000):i])]["c"] if i else None
            try:
                notional = float(p["sz"]) * px if px and p.get("sz") else None
            except (TypeError, ValueError):
                notional = None
            if px is None or notional is None:
                r = "price-unavailable"
            elif notional < min_notional_usd:
                r = "below-min-notional"
            else:
                r = "qualifying"
        out[r] += 1
        if p.get("coin") == "BTC":
            rows.append({"user_tail": str(user)[-6:], "twap_id": tid, "first_seen": p["first_seen"], "reason": r,
                         "first_status": first})
    return {"version": VERSION, "min_notional_usd": min_notional_usd, "programs": sum(out.values()),
            "reasons": dict(out), "btc_programs": rows}


def run(base=ROOT, cutoff=None):
    from lab.data import Store
    from lab.modules import twap
    st = Store(base, cutoff=cutoff)
    progs = twap.programs(st)
    bars = st.bars("binance_klines_1m_BTCUSDT_perp")
    checks = sum(1 for rec in st.hl_enrich() for q in rec.get("requests", [])
                 if q.get("kind") == "twap" and q.get("status") == "ok")
    return {"cutoff_ms": st.cutoff, "twap_checks": checks,
            "variants": {name: classify(progs, bars, mn) for name, mn in (("n1m", 1e6), ("n250k", 2.5e5))}}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=1, default=str))
