"""Module B - account behaviour under pressure (Hyperliquid fixed cohort).

Hypothesis: when the stable (fixed) cohort of large sampled accounts adds to BTC positions that are
under water, subsequent BTC returns in the direction of those additions differ from additions made
while the same cohort's positions are in profit.

Inputs: hl_accounts snapshots (policy hl-sample-v2; FIXED cohort only, so membership is constant),
hl_enrich ledger checks (confirmed transfers), BTC mark from the same run's snapshot.
Per account, consecutive observations at most 30 minutes apart are compared:
  action   open / add / reduce / reverse / close / hold (BTC size change > 5%)
  pressure "drawdown" if the BTC unrealised PnL at the earlier observation was <= -2% of account
           value, "gain" if >= +2%, else "neutral"
  buffer   (cross account value - cross maintenance margin) / cross account value, and its change
  transfer per lab/hlevidence.py: "confirmed" only when an individual perp-margin transfer is
           timestamped inside this transition's interval (t0, t1]; "none_observed" only when an ok,
           untruncated ledger check covers the whole interval; otherwise partial / failed /
           not_attempted / unchecked. Reported twice: as known at the decision time (transfer_at_
           decision) and with all later evidence (transfer_final). Account-value changes are never
           read as deposits.
Cohort event at snapshot t: at least min_accounts fixed accounts added under drawdown (group
"underwater_adds") or under gain ("gain_adds"); direction = sign of the net BTC size those
accounts added. Large account value is a sampling criterion, not evidence of skill.
"""
from lab import hlevidence
from lab.asof import decide
from lab.common import BASIS_PROSPECTIVE, MINUTE, hash_inputs
from lab.events import event_record

ID = "account_behavior"
VERSION = "B-2"
TRANSFER_TYPES = hlevidence.PERP_TRANSFER_TYPES          # kept for callers of the 2.7 name
SPEC = {"module": "B", "id": ID, "version": VERSION, "title": "Account behaviour under pressure",
        "hypothesis": "Fixed-cohort additions to under-water BTC positions predict different subsequent BTC "
                      "returns (in the added direction) than additions made while in profit.",
        "inputs": ["data/hl_accounts (fixed cohort)", "data/hl_enrich ledger", "snap.oi.hyperliquid.mark"],
        "event": ">= min_accounts fixed-cohort accounts add to BTC under drawdown (test) or gain (reference)",
        "outcome": "net log return in the direction of the net additions",
        "baseline": "gain_adds events; hourly controls; regression on prior return, volatility and funding",
        "exclusions": ["rotating-cohort accounts", "observation gaps > 30 minutes", "failed or not-attempted checks",
                       "transfers are only 'confirmed' from ledger evidence"]}


def account_series(store):
    """{address: [(t, obs_dict)]} for fixed-cohort accounts, from checked snapshots only."""
    series = {}
    for rec in store.hl_accounts():
        ids = rec["address_of"]
        pos = {}
        for p in rec.get("positions", []):
            if p[1] == "BTC":
                pos[p[0]] = p
        fields = rec["account_fields"]
        for row in rec.get("accounts", []):
            a = dict(zip(fields, row))
            if not a["account_id"].startswith("F") or a["state"] not in ("ok_btc", "ok_other"):
                continue
            p = pos.get(a["account_id"])
            series.setdefault(ids.get(a["account_id"]), []).append((rec["t"], {
                "avail": rec["observed_at"], "szi": p[2] if p else 0.0, "upnl": p[8] if p else 0.0,
                "value": a["account_value"], "cross": a["cross_account_value"],
                "maint": a["cross_maintenance_margin_used"], "liq": p[4] if p else None}))
        for f in rec.get("flat", []):
            if f[0].startswith("F"):
                series.setdefault(ids.get(f[0]), []).append((rec["t"], {
                    "avail": rec["observed_at"], "szi": 0.0, "upnl": 0.0, "value": f[2], "cross": f[2],
                    "maint": 0.0, "liq": None}))
    return {a: sorted(v, key=lambda x: x[0]) for a, v in series.items() if a}


def classify(prev, cur):
    a, b = prev["szi"], cur["szi"]
    if a == 0 and b == 0:
        return "flat"
    if a == 0:
        return "open"
    if b == 0:
        return "close"
    if (a > 0) != (b > 0):
        return "reverse"
    if abs(b) > abs(a) * 1.05:
        return "add"
    if abs(b) < abs(a) * 0.95:
        return "reduce"
    return "hold"


def transitions(store):
    cs = hlevidence.checks(store)
    out = []
    for addr, obs in account_series(store).items():
        for (t0, a), (t1, b) in zip(obs, obs[1:]):
            if t1 - t0 > 30 * MINUTE:
                continue
            pressure = "neutral"
            if a["value"] and a["szi"]:
                r = a["upnl"] / a["value"]
                pressure = "drawdown" if r <= -0.02 else ("gain" if r >= 0.02 else "neutral")
            buf = lambda o: (o["cross"] - o["maint"]) / o["cross"] if o["cross"] else None
            decision = max(a["avail"], b["avail"])
            at_decision = hlevidence.transfers(cs, addr, t0, t1, known_by=decision)
            final = hlevidence.transfers(cs, addr, t0, t1)
            out.append({"address": addr, "t0": t0, "t": t1, "avail": decision, "action": classify(a, b),
                        "pressure": pressure, "d_szi": b["szi"] - a["szi"], "buffer0": buf(a), "buffer1": buf(b),
                        "transfer": final["state"], "transfer_at_decision": at_decision["state"],
                        "transfer_evidence_observed_at": final["observed_at"]})
    return out


def run(lab, params):
    tr = transitions(lab.store)
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    events, controls = [], []
    by_t = {}
    for x in tr:
        by_t.setdefault(x["t"], []).append(x)
    for t, xs in sorted(by_t.items()):
        t_inputs = max(x["avail"] for x in xs)
        avail, excluded = decide(t, t_inputs)
        if excluded:
            continue
        for group, pressure in (("underwater_adds", "drawdown"), ("gain_adds", "gain")):
            adds = [x for x in xs if x["action"] in ("add", "open") and x["pressure"] == pressure]
            if len(adds) >= params["min_accounts"]:
                net = sum(x["d_szi"] for x in adds)
                states = ("confirmed", "none_observed", "partial", "failed", "not_attempted", "unchecked")
                feats = {"accounts": len(adds), "net_btc_added": net, "severity": len(adds),
                         "transfers_at_decision": {k: sum(1 for x in adds if x["transfer_at_decision"] == k)
                                                   for k in states},
                         "transfers_final": {k: sum(1 for x in adds if x["transfer"] == k) for k in states}}
                events.append(event_record(ID, VERSION, t, min(x["avail"] for x in xs), avail, 1 if net >= 0 else -1,
                                           group, feats, hash_inputs(adds), BASIS_PROSPECTIVE,
                                           {"accounts_compared": len(xs)}, {"cohort": "fixed"}, lab.code,
                                           t_inputs=t_inputs))
        if t % (60 * MINUTE) < 15 * MINUTE:
            controls.append(event_record(ID + ":control", VERSION, t, min(x["avail"] for x in xs), avail, 1,
                                         "control", {"accounts": len(xs)}, hash_inputs([t]), BASIS_PROSPECTIVE,
                                         {}, {}, lab.code, t_inputs=t_inputs))
    counts = {}
    for x in tr:
        k = f"{x['pressure']}:{x['action']}"
        counts[k] = counts.get(k, 0) + 1
    snapshots = len({x["t"] for x in tr})
    need = params.get("min_snapshots", 96 * 14)
    state = "available" if snapshots >= need else "insufficient_data"
    reasons = [] if state == "available" else [f"{snapshots} snapshot transitions for the fixed cohort; "
                                                f"the design needs {need} (about two weeks at 15-minute cadence)"]
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"transitions": len(tr), "snapshots": snapshots,
                                                   "behaviour_counts": counts,
                                                   "transfer_evidence": {k: sum(1 for x in tr if x["transfer"] == k)
                                                                         for k in ("confirmed", "none_observed", "partial",
                                                                                   "failed", "not_attempted", "unchecked")}},
                                      "bars": bars, "state": state, "reasons": reasons}]}
