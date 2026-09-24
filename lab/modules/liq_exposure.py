"""Module C - moving liquidation exposure (sampled Hyperliquid accounts).

This is SAMPLED exposure: positions of the accounts the collector checked in that run, never the
market's liquidation inventory. Liquidation prices are Hyperliquid's own, which already reflect
cross-margin and other-asset effects at the time of the check.

Per snapshot: BTC mark (the same run's Hyperliquid context), and the notional of sampled long
positions whose liquidation price lies within d% below mark and short positions within d% above,
for d in DISTANCES. Between consecutive observations of the same account, each BTC position is
classified: persist, reduce, disappear; disappearances are then classified with evidence that is
filtered transaction by transaction to the interval (t0, t1] and matched to the account, the BTC
coin and the position's side (lab/hlevidence.py):
  confirmed_liquidation  a ledger liquidation naming BTC, or a BTC liquidation fill of this account
                         on this position's side, inside the interval
  account_liquidation_unattributed  a ledger liquidation inside the interval that names no positions
  voluntary_exit         a BTC closing fill on this position's side inside the interval
  sample_removal         the account was not sampled in the next run (rotating cohort)
  missing_data           the next check failed or was not attempted
  unclassified           fills fully covered the interval and showed none of the above
  evidence_partial / evidence_failed / evidence_not_attempted / evidence_unchecked
                         the interval was not adequately covered: unknown, not "no liquidation"
Each classification carries the evidence's observed_at (later confirmation, not knowledge at t1).
Event: sampled long (short) notional within `distance_pct` of mark exceeds `min_notional_usd`
-> direction -1 (+1): price moving toward the cluster. Reference: hourly controls, one per UTC hour of
required-input availability (lab/controls.py; C-3). A control needs the account observation and
the same run's Hyperliquid mark.
"""
from lab import controls as controls_mod
from lab import hlevidence
from lab.asof import decide
from lab.common import BASIS_PROSPECTIVE, MINUTE, hash_inputs
from lab.events import event_record

ID = "liq_exposure"
VERSION = "C-3"
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
            out[s["t"]] = (h["mark"], s.get("observed_at"))
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


def transitions(store, recs):
    cs = hlevidence.checks(store)
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
                ex = hlevidence.position_exit(cs, addr, r0["t"], r1["t"], p[2])
                out.append({"address": addr, "t": r1["t"], "kind": ex["kind"], "liq_px": p[4], "szi": p[2],
                            "evidence_time": ex["evidence_time"], "evidence_observed_at": ex["observed_at"]})
                continue
            out.append({"address": addr, "t": r1["t"], "kind": kind, "liq_px": p[4], "szi": p[2]})
    return out


def run(lab, params):
    recs = lab.store.hl_accounts()
    mk = marks(lab.store)
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    events, cands = [], []
    d, floor = params["distance_pct"], params["min_notional_usd"]
    for rec in recs:
        mark, mark_seen = mk.get(rec["t"], (None, None))
        if not mark or mark_seen is None:
            # not a candidate: a control requires the account observation AND the same run's mark
            cands.append(controls_mod.candidate(rec["t"], rec["t"], rec["observed_at"], rec["observed_at"], None,
                                                missing="same-run Hyperliquid mark"))
            continue
        feats, rows = exposure(rec, mark)
        t_inputs = max(rec["observed_at"], mark_seen)          # positions AND the same run's mark
        feats["mark"] = mark
        ih = hash_inputs(rows)

        def build(avail, rec=rec, feats=feats, ih=ih, t_inputs=t_inputs):
            return event_record(ID + ":control", VERSION, rec["t"], rec["observed_at"], avail, 1, "control",
                                dict(feats), ih, BASIS_PROSPECTIVE, {}, {}, lab.code, t_inputs=t_inputs)
        cands.append(controls_mod.candidate(rec["t"], rec["t"], rec["observed_at"], t_inputs, build))
        avail, excluded = decide(rec["t"], t_inputs)
        if excluded:
            continue
        for side, direction in (("long", -1), ("short", 1)):
            if feats[f"{side}_within_{d:g}pct_usd"] >= floor:
                events.append(event_record(ID, VERSION, rec["t"], rec["observed_at"], avail, direction,
                                           f"{side}_cluster", dict(feats, severity=feats[f"{side}_within_{d:g}pct_usd"]),
                                           ih, BASIS_PROSPECTIVE, {"positions_with_liq_px": len(rows)},
                                           {"sample": rec["policy"]}, lab.code, t_inputs=t_inputs, key=side))
    controls, comparison = controls_mod.apply(lab, cands, min((r["observed_at"] for r in recs), default=None))
    tr = transitions(lab.store, recs)
    kinds = {}
    for x in tr:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    need = params.get("min_snapshots", 96 * 14)
    state = "available" if len(recs) >= need else "insufficient_data"
    reasons = [] if state == "available" else [f"{len(recs)} sampled snapshots; the design needs {need}"]
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"snapshots": len(recs), "with_mark": sum(1 for r in recs if r["t"] in mk),
                                                   "position_transitions": kinds, "comparison": comparison},
                                      "bars": bars, "state": state, "reasons": reasons}]}
