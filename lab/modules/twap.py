"""Module D - TWAP lifecycle (Hyperliquid, predefined fixed-cohort sample).

Sources, both public and rate-limit compliant (collector hl_enrich, at most ENRICH_MAX requests per
run, weight-capped): `twapHistory` for three fixed-cohort accounts per run in rotation (each account
about every 8 hours), and `userFillsByTime` fills whose `twapId` is set (TWAP slices).

Observability is recorded, not assumed: a program is OBSERVED at the first check that returned it
(`first_seen`). Its start time, size and progress come from the history the venue returned; using
those to place the program earlier than first_seen is historical reconstruction and is labelled so.
Events are dated at first_seen + processing latency, never at the program's reported start.

Event: a BTC program observed with status activated (not yet finished/terminated) and notional
>= min_notional_usd; direction = its side. Outcome and baseline as elsewhere; conditioned on the
surrounding flow via the flow_norm feature where 1-minute bars exist.
"""
from lab.asof import decide
from lab.common import BASIS_PROSPECTIVE, hash_inputs
from lab.events import event_record, hourly_controls

ID = "twap_lifecycle"
VERSION = "D-2"
SPEC = {"module": "D", "id": ID, "version": VERSION, "title": "TWAP lifecycle",
        "hypothesis": "Price behaves differently while an observed large BTC TWAP is active than at controls, "
                      "conditional on surrounding flow.",
        "inputs": ["data/hl_enrich twapHistory (fixed-cohort rotation)", "data/hl_enrich fills with twapId"],
        "event": "active BTC TWAP first observed with notional >= min_notional_usd; dated at first observation",
        "outcome": "net log return in the program's direction",
        "baseline": "hourly controls",
        "exclusions": ["programs first seen already finished (lifecycle reconstructed, not observed live)",
                       "coins other than BTC"]}


def programs(store):
    """{(user, twap_id): {...}} with first_seen times and every observed status."""
    progs = {}
    for rec in store.hl_enrich():
        for q in rec.get("requests", []):
            if q.get("status") != "ok":
                continue
            if q["kind"] == "twap":
                for item in q.get("twap_history") or []:
                    if not isinstance(item, dict):
                        continue
                    state = item.get("state") if isinstance(item.get("state"), dict) else {}
                    status = item.get("status")
                    status = status.get("status") if isinstance(status, dict) else status
                    tid = item.get("twapId", state.get("twapId")) or (state.get("timestamp"), state.get("coin"))
                    key = (q["user"], str(tid))
                    p = progs.setdefault(key, {"user": q["user"], "coin": state.get("coin"), "side": state.get("side"),
                                               "sz": state.get("sz"), "executed_sz": state.get("executedSz"),
                                               "executed_ntl": state.get("executedNtl"),
                                               "minutes": state.get("minutes"), "reported_start": state.get("timestamp"),
                                               "first_seen": rec["t"], "first_seen_avail": rec["observed_at"],
                                               "statuses": []})
                    p["statuses"].append([rec["t"], status])
            if q["kind"] == "fills":
                for f in q.get("fills", []):
                    if f[11] is not None:
                        key = (q["user"], str(f[11]))
                        p = progs.setdefault(key, {"user": q["user"], "coin": f[1], "side": f[4], "first_seen": rec["t"],
                                                   "first_seen_avail": rec["observed_at"], "statuses": [],
                                                   "from_fills_only": True})
                        p.setdefault("slices", []).append([f[0], f[2], f[3]])
    return progs


def run(lab, params):
    progs = programs(lab.store)
    bars = lab.store.bars("binance_klines_1m_BTCUSDT_perp")
    events = []
    for (user, tid), p in sorted(progs.items(), key=lambda kv: kv[1]["first_seen"]):
        first = p["statuses"][0][1] if p["statuses"] else None
        if p.get("coin") != "BTC" or first != "activated":
            continue
        try:                                        # price known at first observation, never later
            known = [t for t, b in bars.items() if b["avail"] <= p["first_seen_avail"]]
            px = bars[max(known)]["c"] if known else None
            notional = float(p["sz"]) * px if px and p.get("sz") else None
        except (TypeError, ValueError):
            notional = None
        if notional is None or notional < params["min_notional_usd"]:
            continue
        direction = 1 if p.get("side") in ("B", "buy", True) else -1
        avail, excluded = decide(p["first_seen"], p["first_seen_avail"])   # price: bars known by then
        if excluded:
            continue
        events.append(event_record(ID, VERSION, p["first_seen"], p["first_seen_avail"],
                                   avail, direction, "active_twap",
                                   {"notional_usd_est": notional, "minutes": p.get("minutes"),
                                    "reported_start": p.get("reported_start"),
                                    "reported_start_basis": "historical reconstruction from twapHistory"},
                                   hash_inputs([user, tid]), BASIS_PROSPECTIVE, {}, {"observability": "first_seen"},
                                   lab.code, t_inputs=p["first_seen_avail"], key=f"{user}:{tid}"))
    checks = sum(1 for rec in lab.store.hl_enrich() for q in rec.get("requests", [])
                 if q.get("kind") == "twap" and q.get("status") == "ok")
    btc = sum(1 for p in progs.values() if p.get("coin") == "BTC")
    need = params.get("min_programs", 30)
    state = "available" if len(events) >= need else "insufficient_data"
    reasons = [] if state == "available" else [
        f"{checks} twapHistory checks, {len(progs)} programs observed ({btc} BTC), {len(events)} qualifying; "
        f"the design needs {need} active BTC programs"]
    controls = hourly_controls(bars, ID, VERSION, lab.code, BASIS_PROSPECTIVE)
    return {"module": ID, "passes": [{"basis": "prospective", "events": events, "controls": controls,
                                      "coverage": {"twap_checks": checks, "programs": len(progs), "btc_programs": btc},
                                      "bars": bars, "state": state, "reasons": reasons}]}
