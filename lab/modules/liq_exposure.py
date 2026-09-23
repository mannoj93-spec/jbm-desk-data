"""Module C - moving liquidation exposure (sampled Hyperliquid accounts).

This is SAMPLED exposure: positions of the accounts the collector checked in that run, never the
market's liquidation inventory. Liquidation prices are Hyperliquid's own, which already reflect
cross-margin and other-asset effects at the time of the check.

Per snapshot: BTC mark (the same run's Hyperliquid context), and the notional of sampled long
positions whose liquidation price lies within d% below mark and short positions within d% above,
for d in DISTANCES. Between consecutive observations of the same account, each BTC position is
classified: persist, reduce, disappear; disappearances are then classified with evidence:
  confirmed_liquidation  a ledger "liquidation" delta or a fill carrying a liquidation marker
                         (or a "Liquidat..." direction) inside the interval
  voluntary_exit         closing fills inside the interval without a liquidation marker
  sample_removal         the account was not sampled in the next run (rotating cohort)
  missing_data           the next check failed or was not attempted
  unclassified           none of the above could be established (no enrichment check yet)
Event: sampled long (short) notional within `distance_pct` of mark exceeds `min_notional_usd`
-> direction -1 (+1): price moving toward the cluster. Reference: hourly controls.
"""
from lab.common import BASIS_PROSPECTIVE, MINUTE, PROCESSING_LATENCY_MS, hash_inputs
from lab.events import event_record

ID = "liq_exposure"
VERSION = "C-1"
DISTANCES = (1.0, 2.0, 5.0)
SPEC = {"module": "C", "id": ID, "version": VERSION, "title": "Moving liquidation exposure (sampled)",
        "hypothesis": "Large sampled liquidation exposure close to mark predicts moves toward it more often "
                      "than hourly controls.",
        "inputs": ["data/hl_accounts positions (BTC, liquidation_px)", "snap.oi.hyperliquid.mark",
                   "data/hl_enrich fills and ledger (classification)"],
        "event": "sampled long (short) notional within distance_pct of mark >= min_notional_usd",
        "outcome": "net log return toward the cluster (short for longs' cluster)",
        "baseline": "hourly controls; regression on prior return, volatility, funding",
        "exclusions": ["positions without a liquidation price", "snapshots without a Hyperliquid mark"]}


def marks(store):
    out = {}
    for s in store.snaps():
        h = (s.get("oi") or {}).get("hyperliquid") or {}
        if h.get("st") == "ok" and h.get("mark"):
            out[s["t"]] = h["mark"]
    return out


def exposure(rec, mark):
    ids, rows = rec["address_of"], []
    for p in rec.get("positions", []):
        if p[1] != "BTC" or p[4] is None:
            continue
        rows.append((ids.get(p[0]), p[2], p[4], abs(p[7] or 0.0)))
    out = {}
    for d in DISTANCES:
        out[f"long_within_{d:g}pct_usd"] = sum(v for _, szi, liq, v in rows if szi > 0 and 0 <= (mark - liq) / mark <= d / 100)
        out[f"short_within_{d:g}pct_usd"] = sum(v for _, szi, liq, v in rows if szi < 0 and 0 <= (liq - mark) / mark <= d / 100)
    return out, rows


def evidence(store):
    """{address: [(start, end, kind)]} where kind is 'liquidation' or 'close_fill'."""
    out = {}
    for rec in store.hl_enrich():
        for q in rec.get("requests", []):
            if q.get("status") != "ok":
                continue
            u, (a, b) = q["user"], q["window"]
            if q["kind"] == "ledger" and any(e[1] == "liquidation" for e in q.get("ledger", [])):
                out.setdefault(u, []).append((a, b, "liquidation"))
            if q["kind"] == "fills":
                for f in q.get("fills", []):
                    if f[1] != "BTC":
                        continue
                    if f[12] or (isinstance(f[5], str) and "iquidat" in f[5]):
                        out.setdefault(u, []).append((a, b, "liquidation"))
                    elif isinstance(f[5], str) and f[5].startswith("Close"):
                        out.setdefault(u, []).append((a, b, "close_fill"))
    return out


def transitions(store, recs):
    ev = evidence(store)
    out = []
    for r0, r1 in zip(recs, recs[1:]):
        if r1["t"] - r0["t"] > 30 * MINUTE:
            continue
        p0 = {r0["address_of"].get(p[0]): p for p in r0.get("positions", []) if p[1] == "BTC"}
        p1 = {r1["address_of"].get(p[0]): p for p in r1.get("positions", []) if p[1] == "BTC"}
        state1 = {}
        for row in r1.get("accounts", []):
            state1[r1["address_of"].get(row[0])] = row[1]
        for f in r1.get("flat", []):
            state1[r1["address_of"].get(f[0])] = "ok_flat"
        for addr, p in p0.items():
            if addr in p1:
                kind = "persist" if abs(p1[addr][2]) >= abs(p[2]) * 0.95 else "reduce"
            elif addr not in state1:
                kind = "sample_removal"
            elif state1[addr] in ("failed", "not_attempted"):
                kind = "missing_data"
            else:
                marks_ = [k for a, b, k in ev.get(addr, []) if a <= r0["t"] and b >= r1["t"]]
                kind = ("confirmed_liquidation" if "liquidation" in marks_ else
                        "voluntary_exit" if "close_fill" in marks_ else "unclassified")
            out.append({"address": addr, "t": r1["t"], "kind": kind, "liq_px": p[4], "szi": p[2]})
    return out


def run(lab, params):
    recs = lab.store.hl_accounts()
    mk = marks(lab.store)
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    events, controls = [], []
    d, floor = params["distance_pct"], params["min_notional_usd"]
    for rec in recs:
        mark = mk.get(rec["t"])
        if not mark:
            continue
        feats, rows = exposure(rec, mark)
        avail = rec["observed_at"]
        feats["mark"] = mark
        ih = hash_inputs(rows)
        for side, direction in (("long", -1), ("short", 1)):
            if feats[f"{side}_within_{d:g}pct_usd"] >= floor:
                events.append(event_record(ID, VERSION, rec["t"], avail, avail + PROCESSING_LATENCY_MS, direction,
                                           f"{side}_cluster", feats, ih, BASIS_PROSPECTIVE,
                                           {"positions_with_liq_px": len(rows)}, {"sample": rec["policy"]}, lab.code))
        if rec["t"] % (60 * MINUTE) < 15 * MINUTE:
            controls.append(event_record(ID + ":control", VERSION, rec["t"], avail, avail + PROCESSING_LATENCY_MS,
                                         -1 if feats[f"long_within_{d:g}pct_usd"] >= feats[f"short_within_{d:g}pct_usd"] else 1,
                                         "control", feats, ih, BASIS_PROSPECTIVE, {}, {}, lab.code))
    tr = transitions(lab.store, recs)
    kinds = {}
    for x in tr:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    need = params.get("min_snapshots", 96 * 14)
    state = "available" if len(recs) >= need else "insufficient_data"
    reasons = [] if state == "available" else [f"{len(recs)} sampled snapshots; the design needs {need}"]
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"snapshots": len(recs), "with_mark": sum(1 for r in recs if r["t"] in mk),
                                                   "position_transitions": kinds},
                                      "bars": bars, "state": state, "reasons": reasons}]}
