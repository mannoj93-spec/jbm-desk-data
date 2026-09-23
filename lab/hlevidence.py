"""Hyperliquid enrichment evidence, attributed transaction by transaction (lab-2.0).

A position TRANSITION is the change between two observations of one account at snapshot times
t0 < t1. Its evidence interval is (t0, t1]: a ledger entry or fill counts if t0 < time <= t1.
(An entry exactly at t0 belongs to the previous transition; the collector's snapshot time is the
run start, so this rule assigns every millisecond to exactly one interval.)

Coverage of an interval by the checks of ONE account and ONE query kind (ledger or fills):
  covered        an ok check whose window contains [t0, t1] and whose result was not truncated
  partial        ok checks exist but none covers the whole interval, or the covering one was
                 truncated at the source (the venue caps results), so absence proves nothing
  failed         only failed checks touch the interval
  not_attempted  only checks skipped for budget touch the interval
  unchecked      no check touched the interval
"none_observed" is reported ONLY when the interval is covered. A positive finding (a transfer or a
liquidation inside the interval) stands even under partial coverage.

Knowledge time: every check carries the collector's observed_at. `known_by` restricts evidence to
what had been written by a decision time (contemporaneous knowledge); without it the result is the
final, possibly later, confirmation. Both are reported where a module uses them.

Transfer types that can move perp margin: deposit, withdraw, internalTransfer,
subAccountTransfer, accountClassTransfer (spot<->perp), vaultDeposit, vaultWithdraw, and `send`
unless both sides are the spot dex. spotTransfer is stored only as a count without times
(collector 2.7 compaction) and never moves perp margin, so it is not attributed to any interval;
cStakingTransfer is staking, not margin.
Liquidation of a SPECIFIC BTC position needs either a ledger `liquidation` entry whose
liquidatedPositions list names BTC (with the position's sign when sizes are given), or a BTC fill
inside the interval marked as a liquidation of this account (liquidatedUser equal to the account
when the venue reports it) on the position's side. A ledger liquidation that names no positions is
"account_liquidation_unattributed"; an unrelated fill proves nothing.
"""

PERP_TRANSFER_TYPES = {"deposit", "withdraw", "internalTransfer", "subAccountTransfer", "accountClassTransfer",
                       "vaultDeposit", "vaultWithdraw", "send"}
FILL = {name: i for i, name in enumerate(["time", "coin", "px", "sz", "side", "dir", "start_position", "closed_pnl",
                                          "crossed", "fee", "oid", "twap_id", "liquidation"])}


def checks(store):
    """Every enrichment request as a flat record, with its observation time."""
    out = []
    for rec in store.hl_enrich():
        for q in rec.get("requests", []):
            if q.get("kind") not in ("ledger", "fills"):
                continue
            w = q.get("window") or [None, None]
            out.append({"kind": q["kind"], "user": q.get("user"), "start": w[0], "end": w[1],
                        "status": q.get("status"), "truncated": bool(q.get("truncated_at_source")),
                        "observed_at": rec.get("observed_at"), "ledger": q.get("ledger") or [],
                        "fills": q.get("fills") or []})
    return out


def _relevant(cs, user, kind, t0, t1, known_by):
    return [c for c in cs if c["user"] == user and c["kind"] == kind and c["start"] is not None
            and c["end"] is not None and c["start"] < t1 and c["end"] > t0
            and (known_by is None or (c["observed_at"] is not None and c["observed_at"] <= known_by))]


def coverage(cs, user, kind, t0, t1, known_by=None):
    rel = _relevant(cs, user, kind, t0, t1, known_by)
    ok = [c for c in rel if c["status"] == "ok"]
    if any(c["start"] <= t0 and c["end"] >= t1 and not c["truncated"] for c in ok):
        return "covered"
    if ok:
        return "partial"
    if any(c["status"] == "failed" for c in rel):
        return "failed"
    if rel:
        return "not_attempted"
    return "unchecked"


def affects_perp(entry_type, delta):
    if entry_type not in PERP_TRANSFER_TYPES:
        return False
    if entry_type == "send" and isinstance(delta, dict):
        return not (delta.get("sourceDex") == "spot" and delta.get("destinationDex") == "spot")
    return True


def transfers(cs, user, t0, t1, known_by=None):
    """{'state': confirmed|none_observed|partial|failed|not_attempted|unchecked, 'entries': [...],
    'observed_at': latest observed_at of the evidence used, 'spot_transfers_untimed': count}"""
    found, seen, spot = [], [], 0
    for c in _relevant(cs, user, "ledger", t0, t1, known_by):
        if c["status"] != "ok":
            continue
        seen.append(c["observed_at"])
        for time, typ, delta in c["ledger"]:
            if time is not None and t0 < time <= t1 and affects_perp(typ, delta):
                found.append({"time": time, "type": typ, "observed_at": c["observed_at"]})
    state = "confirmed" if found else coverage(cs, user, "ledger", t0, t1, known_by)
    if state == "covered":
        state = "none_observed"
    uniq = {(f["time"], f["type"]): f for f in found}
    return {"state": state, "entries": sorted(uniq.values(), key=lambda f: f["time"]),
            "observed_at": max([x for x in seen if x is not None], default=None)}


def position_exit(cs, user, t0, t1, szi, known_by=None):
    """Why a BTC position of signed size `szi` observed at t0 was gone at t1."""
    side = "Long" if szi > 0 else "Short"
    evidence = []
    for c in _relevant(cs, user, "ledger", t0, t1, known_by):
        if c["status"] != "ok":
            continue
        for time, typ, delta in c["ledger"]:
            if typ != "liquidation" or time is None or not t0 < time <= t1:
                continue
            positions = (delta or {}).get("liquidatedPositions") if isinstance(delta, dict) else None
            if positions is None:
                evidence.append(("account_liquidation_unattributed", time, c["observed_at"]))
                continue
            for p in positions:
                if p.get("coin") != "BTC":
                    continue
                try:
                    same_side = float(p.get("szi")) * szi > 0
                except (TypeError, ValueError):
                    same_side = True               # size not reported: the coin match is the evidence
                if same_side:
                    evidence.append(("confirmed_liquidation", time, c["observed_at"]))
    for c in _relevant(cs, user, "fills", t0, t1, known_by):
        if c["status"] != "ok":
            continue
        for f in c["fills"]:
            time, coin, direction = f[FILL["time"]], f[FILL["coin"]], f[FILL["dir"]] or ""
            if coin != "BTC" or time is None or not t0 < time <= t1 or side not in direction:
                continue
            liq = f[FILL["liquidation"]]
            liquidated_user = liq.get("liquidatedUser") if isinstance(liq, dict) else None
            if (liq or "iquidat" in direction) and (liquidated_user in (None, user)):
                evidence.append(("confirmed_liquidation", time, c["observed_at"]))
            elif direction.startswith("Close"):
                evidence.append(("voluntary_exit", time, c["observed_at"]))
    for kind in ("confirmed_liquidation", "voluntary_exit", "account_liquidation_unattributed"):
        hits = [e for e in evidence if e[0] == kind]
        if hits:
            return {"kind": kind, "evidence_time": hits[0][1], "observed_at": max(h[2] or 0 for h in hits) or None}
    cov = coverage(cs, user, "fills", t0, t1, known_by)
    return {"kind": "unclassified" if cov == "covered" else f"evidence_{cov}", "evidence_time": None,
            "observed_at": None}
