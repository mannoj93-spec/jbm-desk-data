"""Hyperliquid account sampling, policy hl-sample-v2 (collector 2.7).

The per-run request budget is unchanged from 2.6: at most HL_TOP_N (200) info requests for
accounts inside HL_BUDGET_S (300 s). It is now allocated as
  * a FIXED cohort of 100 accounts, selected once and frozen in state/hl_cohort_fixed_v2.json;
  * a ROTATING cohort of 90 accounts taken in turn from the rest of the ranked universe;
  * up to 10 ENRICHMENT requests (fills, non-funding ledger, TWAP history) for sampled accounts.
Rate limits (Hyperliquid docs, verified 2026-09-23): 1200 weight per minute per IP;
clearinghouseState weighs 2; userFillsByTime, userNonFundingLedgerUpdates and twapHistory weigh 20
plus 1 per 20 items returned. 190 x 2 + at most ENRICH_WEIGHT keeps a run well under the limit.

Selection uses only what was known at selection time: the six-hourly leaderboard ranking by account
value cached in state (the same 6-hour cache as 2.6, widened from 200 to 1000 accounts). The fixed
cohort is the top FIXED_N of the first ranking seen under this policy; it is never re-selected, so
it cannot be refreshed toward accounts that later did well. Account value is a sampling criterion,
not evidence of skill. Every snapshot lists each sampled address once with its cohort and state:
  ok_btc        checked; holds a BTC position
  ok_other      checked; positions, none in BTC
  ok_flat       checked; no positions
  failed        request or validation failed (reason kept)
  not_attempted budget or rejection rule stopped the run first (reason kept)
Positions in DETAIL_COINS are kept in full; other coins are aggregated per account (count, long and
short notional, margin used, unrealized PnL) to bound storage. This is a sample of large accounts,
never the market's full position or liquidation inventory.
"""
import hashlib
import json
import math

POLICY = "hl-sample-v2"
FIXED_N = 100
ROTATING_N = 90
ENRICH_MAX = 10             # FIXED_N + ROTATING_N + ENRICH_MAX == 200 == the 2.6 HL_TOP_N budget
ENRICH_WEIGHT = 400         # estimated weight cap for enrichment requests per run
ENRICH_QUEUE_MAX = 40
UNIVERSE_N = 1000
DETAIL_COINS = ("BTC", "ETH", "SOL")
FIXED_PATH = "state/hl_cohort_fixed_v2.json"
# Rows identify an account by "F<i>" (index i into the frozen fixed cohort's members) or "R<j>"
# (index j into this record's rotating.members), which keeps each snapshot about half the size of
# repeating 42-character addresses. research.Ctx.hl_accounts() resolves ids back to addresses.
# Accounts checked and holding no position are listed compactly in `flat` (FLAT_FIELDS); every
# other sampled account is one `accounts` row. Clearinghouse times are stored as offsets from t.
FLAT_FIELDS = ["account_id", "clearinghouse_time_offset_ms", "account_value", "withdrawable"]
ACCOUNT_FIELDS = ["account_id", "state", "reason", "clearinghouse_time_offset_ms", "account_value", "total_ntl_pos",
                  "total_margin_used", "total_raw_usd", "cross_account_value", "cross_maintenance_margin_used",
                  "withdrawable", "n_positions", "other_n", "other_long_ntl", "other_short_ntl",
                  "other_margin_used", "other_unrealized_pnl"]
POSITION_FIELDS = ["account_id", "coin", "szi", "entry_px", "liquidation_px", "leverage_type", "leverage",
                   "position_value", "unrealized_pnl", "margin_used", "cum_funding_since_open", "max_leverage"]
FILL_FIELDS = ["time", "coin", "px", "sz", "side", "dir", "start_position", "closed_pnl", "crossed", "fee", "oid",
               "twap_id", "liquidation"]
POLICY_DOC = {"policy": POLICY, "fixed_n": FIXED_N, "rotating_n": ROTATING_N, "enrich_max": ENRICH_MAX,
              "universe_n": UNIVERSE_N, "detail_coins": list(DETAIL_COINS),
              "fixed_rule": "top fixed_n by leaderboard accountValue in the first ranking seen under this policy",
              "rotating_rule": "next rotating_n accounts, in rank order, of the current ranking minus the fixed "
                               "cohort; cursor persists across runs and ranking refreshes"}
POLICY_SHA256 = hashlib.sha256(json.dumps(POLICY_DOC, sort_keys=True).encode()).hexdigest()


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def universe(C, st, deadline):
    """Six-hour cached ranking, top UNIVERSE_N by account value; `addresses` keeps the 2.6 top-200."""
    cache = st.get("hl_top") or {}
    fresh = cache.get("t") and C.NOW - cache["t"] < C.HL_TOP_REFRESH
    if fresh and len(cache.get("universe") or []) >= FIXED_N + ROTATING_N:
        return cache
    js = C.need(C.get(C.HL_LEADERBOARD, tries=2, timeout=60, deadline=deadline))
    rows = js.get("leaderboardRows") if isinstance(js, dict) else None
    if not isinstance(rows, list) or len(rows) < FIXED_N + ROTATING_N:
        raise ValueError("Hyperliquid leaderboard missing or short")
    ranked = sorted(((C.f(r.get("accountValue")) or 0.0, r.get("ethAddress")) for r in rows
                     if isinstance(r.get("ethAddress"), str)), key=lambda x: (-x[0], x[1]))[:UNIVERSE_N]
    uni = [[a, round(v, 2)] for v, a in ranked]
    cache = {"t": C.NOW, "addresses": [a for a, _ in uni[:C.HL_TOP_N]],
             "min_account_value": uni[min(C.HL_TOP_N, len(uni)) - 1][1],
             "rank_basis": "leaderboard accountValue, descending", "universe": uni, "universe_sha256": sha(uni)}
    st["hl_top"] = cache
    return cache


def fixed_cohort(C, ranking):
    """Load the frozen fixed cohort, or select it now from the current ranking (first v2 run)."""
    path = C.os.path.join(C.BASE, FIXED_PATH)
    existing = C.read_json(path, None)
    if existing:
        if existing.get("policy") != POLICY:
            raise ValueError("fixed cohort file belongs to another policy; refusing to overwrite it")
        return existing, False
    uni = ranking["universe"]
    members = [[a, i + 1, v] for i, (a, v) in enumerate(uni[:FIXED_N])]
    cohort = {"policy": POLICY, "policy_sha256": POLICY_SHA256, "cohort_id": f"F-{POLICY}-{ranking['t']}",
              "selected_at": ranking["t"], "selected_by_run": C.NOW, "rule": POLICY_DOC["fixed_rule"],
              "ranking_sha256": ranking.get("universe_sha256") or sha(uni), "member_fields":
              ["address", "rank_at_selection", "account_value_at_selection"], "members": members,
              "members_sha256": sha([m[0] for m in members])}
    C.atomic_json(path, cohort)
    return cohort, True


def rotating(st, ranking, fixed_members):
    fixed = {m[0] for m in fixed_members}
    pool = [a for a, _ in ranking["universe"] if a not in fixed]
    rot = st.get("hl_rotation") or {}
    cursor = int(rot.get("cursor", 0)) % max(len(pool), 1)
    take = [pool[(cursor + i) % len(pool)] for i in range(min(ROTATING_N, len(pool)))] if pool else []
    st["hl_rotation"] = {"cursor": (cursor + len(take)) % max(len(pool), 1), "ranking_t": ranking["t"],
                         "pool_size": len(pool)}
    return take, cursor, len(pool)


def parse_account(C, js):
    """Validate one clearinghouseState response. Returns (account_row_tail, detail_positions, btc_rows)
    or raises ValueError. `{}` or anything without the documented structure is a failure, not a flat
    account."""
    if not isinstance(js, dict):
        raise ValueError("not an object")
    summary, cross, assets = js.get("marginSummary"), js.get("crossMarginSummary"), js.get("assetPositions")
    if not isinstance(summary, dict) or not isinstance(assets, list):
        raise ValueError("missing marginSummary/assetPositions")
    acct = C.f(summary.get("accountValue"))
    if acct is None or acct < 0:
        raise ValueError("invalid accountValue")
    detail, btc = [], []
    other = [0, 0.0, 0.0, 0.0, 0.0]
    for ap in assets:
        pos = ap.get("position") if isinstance(ap, dict) else None
        if not isinstance(pos, dict) or not isinstance(pos.get("coin"), str):
            raise ValueError("malformed asset position")
        coin = pos["coin"]
        szi, value = C.f(pos.get("szi")), C.f(pos.get("positionValue"))
        if not szi or value is None:
            raise ValueError(f"malformed {coin[:12]} position")
        if coin in DETAIL_COINS:
            lev = pos.get("leverage") if isinstance(pos.get("leverage"), dict) else {}
            entry, liq = C.positive(pos.get("entryPx")), pos.get("liquidationPx")
            liq_px = None if liq is None else C.positive(liq)
            if (entry is None or lev.get("type") not in C.HL_LEVERAGE_TYPES or C.positive(lev.get("value")) is None
                    or (liq is not None and liq_px is None)):
                raise ValueError(f"malformed {coin} position")
            cum = pos.get("cumFunding") if isinstance(pos.get("cumFunding"), dict) else {}
            detail.append([coin, szi, entry, liq_px, lev["type"], C.f(lev["value"]), value,
                           C.f(pos.get("unrealizedPnl")), C.f(pos.get("marginUsed")), C.f(cum.get("sinceOpen")),
                           C.f(pos.get("maxLeverage"))])
            if coin == "BTC":
                btc.append([acct, szi, entry, liq_px, lev["type"], C.f(lev["value"]), value,
                            C.f(pos.get("unrealizedPnl")), C.f(pos.get("marginUsed"))])
        else:
            other[0] += 1
            if szi > 0:
                other[1] += abs(value)
            else:
                other[2] += abs(value)
            other[3] += C.f(pos.get("marginUsed")) or 0.0
            other[4] += C.f(pos.get("unrealizedPnl")) or 0.0
    state = "ok_btc" if btc else ("ok_other" if assets else "ok_flat")
    cross = cross if isinstance(cross, dict) else {}
    tail = [state, None, js.get("time"), acct, C.f(summary.get("totalNtlPos")), C.f(summary.get("totalMarginUsed")),
            C.f(summary.get("totalRawUsd")), C.f(cross.get("accountValue")), C.f(js.get("crossMaintenanceMarginUsed")),
            C.f(js.get("withdrawable")), len(assets), other[0], round(other[1], 2), round(other[2], 2),
            round(other[3], 2), round(other[4], 2)]
    return tail, detail, btc


def btc_szi(detail):
    return sum(p[1] for p in detail if p[0] == "BTC")


def update_triggers(st, addr, now, szi, account_ok):
    """Queue a fills + ledger check when a fixed-cohort account's BTC position closed, flipped or
    more than halved since this account was last observed. The window is exactly
    [previous observation, this observation]; nothing later is used to decide."""
    last = st.setdefault("hl_last", {})
    queue = st.setdefault("hl_enrich_queue", [])
    if not account_ok:
        return
    prev = last.get(addr)
    last[addr] = [now, szi]
    if not prev or not prev[1]:
        return
    p = prev[1]
    reason = None
    if szi == 0:
        reason = "btc_position_closed"
    elif (p > 0) != (szi > 0):
        reason = "btc_position_flipped"
    elif abs(szi) <= 0.5 * abs(p):
        reason = "btc_position_halved"
    if reason:
        queue.append({"user": addr, "from": prev[0], "to": now, "reason": reason, "prev_szi": p, "szi": szi})
        if len(queue) > ENRICH_QUEUE_MAX:
            dropped = len(queue) - ENRICH_QUEUE_MAX
            del queue[:dropped]
            st["hl_enrich_dropped"] = st.get("hl_enrich_dropped", 0) + dropped


def compact_fill(C, x):
    liq = x.get("liquidation")
    return [x.get("time"), x.get("coin"), C.f(x.get("px")), C.f(x.get("sz")), x.get("side"), x.get("dir"),
            C.f(x.get("startPosition")), C.f(x.get("closedPnl")), x.get("crossed"), C.f(x.get("fee")), x.get("oid"),
            x.get("twapId"), liq if liq else None]


def compact_ledger(entries):
    """Keep every non-spot delta as returned; spot transfers are counted and summed (USDC value) only,
    because they are numerous and do not move perp margin."""
    kept, spot_n, spot_usd = [], 0, 0.0
    for e in entries:
        d = e.get("delta") if isinstance(e, dict) else None
        if not isinstance(d, dict):
            continue
        if d.get("type") == "spotTransfer":
            spot_n += 1
            try:
                spot_usd += float(d.get("usdcValue") or 0)
            except (TypeError, ValueError):
                pass
            continue
        kept.append([e.get("time"), d.get("type"), d])
    return kept, spot_n, round(spot_usd, 2)


def weight(items):
    return 20 + math.ceil(max(items, 0) / 20)


def enrich(C, st, fixed_members, deadline):
    """At most ENRICH_MAX requests and about ENRICH_WEIGHT weight. Queue first (confirmation of
    closes), then one ledger round-robin check, then TWAP history round-robin checks."""
    plan, queue = [], st.setdefault("hl_enrich_queue", [])
    slots = ENRICH_MAX
    while queue and slots >= 2 and len(plan) < 6:
        item = queue.pop(0)
        plan.append(("fills", item["user"], item["from"], item["to"], item["reason"]))
        plan.append(("ledger", item["user"], item["from"], item["to"], item["reason"]))
        slots -= 2
    members = [m[0] for m in fixed_members]
    if members and slots:
        cur = int(st.get("hl_ledger_cursor", 0)) % len(members)
        user = members[cur]
        since = (st.setdefault("hl_ledger_since", {}).get(user)) or C.NOW - 24 * C.H
        plan.append(("ledger", user, since, C.NOW, "round_robin"))
        st["hl_ledger_cursor"] = (cur + 1) % len(members)
        slots -= 1
    if members:
        cur = int(st.get("hl_twap_cursor", 0)) % len(members)
        for i in range(slots):
            plan.append(("twap", members[(cur + i) % len(members)], None, C.NOW, "round_robin"))
        st["hl_twap_cursor"] = (cur + slots) % len(members)
    out, used_weight, requests = [], 0, 0
    for kind, user, start, end, why in plan:
        rec = {"kind": kind, "user": user, "window": [start, end], "trigger": why}
        if used_weight >= ENRICH_WEIGHT or C.time.monotonic() >= deadline:
            rec.update(status="not_attempted", reason="weight or time budget")
            out.append(rec)
            continue
        body = ({"type": "userFillsByTime", "user": user, "startTime": start, "endTime": end} if kind == "fills" else
                {"type": "userNonFundingLedgerUpdates", "user": user, "startTime": start, "endTime": end}
                if kind == "ledger" else {"type": "twapHistory", "user": user})
        js, err = C.get(C.HL_INFO, body=body, tries=1, timeout=C.HL_REQUEST_TIMEOUT_S, deadline=deadline)
        requests += 1
        if err or not isinstance(js, list):
            rec.update(status="failed", reason=(err or "not a list")[:80])
            used_weight += 20
            out.append(rec)
            continue
        used_weight += weight(len(js))
        rec.update(status="ok", n_items=len(js), weight_est=weight(len(js)))
        if kind == "fills":
            rec["fill_fields"] = FILL_FIELDS
            rec["fills"] = [compact_fill(C, x) for x in js if isinstance(x, dict) and x.get("coin") in DETAIL_COINS]
            rec["other_coin_fills"] = sum(1 for x in js if isinstance(x, dict) and x.get("coin") not in DETAIL_COINS)
            rec["truncated_at_source"] = len(js) >= 2000
        elif kind == "ledger":
            rec["ledger"], rec["spot_transfers"], rec["spot_transfer_usdc"] = compact_ledger(js)
            rec["truncated_at_source"] = len(js) >= 500
            if why == "round_robin" and len(js) < 500:
                st.setdefault("hl_ledger_since", {})[user] = end
        else:
            rec["twap_history"] = js[:50]           # stored as returned (format not documented on the info page)
        out.append(rec)
    return out, used_weight, requests


def collect(C, st):
    """Fixed + rotating account map (schema hl_accounts/2), a schema-1 compatible BTC record for 2.6
    readers, and bounded enrichment. Half or more of the sampled accounts failing stores nothing."""
    started = C.time.monotonic()
    deadline = started + C.HL_BUDGET_S
    ranking = universe(C, st, deadline)
    cohort, selected_now = fixed_cohort(C, ranking)
    fixed = [m[0] for m in cohort["members"]]
    rot, cursor, pool = rotating(st, ranking, cohort["members"])
    fixed_set = set(fixed)
    rot = [a for a in rot if a not in fixed_set]
    sample = [(a, "F", f"F{i}") for i, a in enumerate(fixed)] + [(a, "R", f"R{j}") for j, a in enumerate(rot)]
    reject_at = (len(sample) + 1) // 2
    accounts, positions, btc_rows, failed, stopped, rate_limited = [], [], [], [], None, 0
    flat = []
    for i, (addr, cohort_tag, aid) in enumerate(sample):
        if len(failed) >= reject_at:
            stopped = "rejection inevitable"
        elif C.time.monotonic() >= deadline:
            stopped = "deadline"
        if stopped:
            for a, tag, a_id in sample[i:]:
                accounts.append([a_id, "not_attempted", stopped] + [None] * (len(ACCOUNT_FIELDS) - 3))
                failed.append([a, f"not attempted: {stopped}"])
            break
        js, err = C.get(C.HL_INFO, body={"type": "clearinghouseState", "user": addr}, tries=2, pause=0.05,
                        timeout=C.HL_REQUEST_TIMEOUT_S, deadline=deadline)
        if err and err.startswith("HTTP 429"):
            rate_limited += 1
            C.time.sleep(min(C.HL_RATE_LIMIT_BACKOFF_S, max(0.0, deadline - C.time.monotonic())))
            js, err = C.get(C.HL_INFO, body={"type": "clearinghouseState", "user": addr}, tries=1,
                            timeout=C.HL_REQUEST_TIMEOUT_S, deadline=deadline)
        try:
            if err:
                raise ValueError(err)
            tail, detail, btc = parse_account(C, js)
        except (ValueError, TypeError) as exc:
            reason = str(exc)[:60]
            accounts.append([aid, "failed", reason] + [None] * (len(ACCOUNT_FIELDS) - 3))
            failed.append([addr, reason])
            if cohort_tag == "F":
                update_triggers(st, addr, C.NOW, None, False)
            continue
        offset = (tail[2] - C.NOW) if isinstance(tail[2], int) else None
        if tail[0] == "ok_flat":
            flat.append([aid, offset, tail[3], tail[9]])
        else:
            accounts.append([aid] + tail[:2] + [offset] + tail[3:])
        positions.extend([aid] + p for p in detail)
        btc_rows.extend([addr] + p for p in btc)
        if cohort_tag == "F":
            update_triggers(st, addr, C.NOW, btc_szi(detail), True)
    elapsed = round(C.time.monotonic() - started, 1)
    counts = {"ok_flat": len(flat)} if flat else {}
    for row in accounts:
        counts[row[1]] = counts.get(row[1], 0) + 1
    if len(failed) >= reject_at:
        raise RuntimeError(f"{len(failed)}/{len(sample)} accounts failed or not attempted in {elapsed}s"
                           f"{'; stopped: ' + stopped if stopped else ''}; map not stored (first: {failed[:2]})")
    enrich_out, enrich_weight, enrich_requests = enrich(C, st, cohort["members"], deadline)
    status = "degraded" if failed else "complete"
    v2 = {"t": C.NOW, "schema": "hl_accounts/2", "policy": POLICY, "policy_sha256": POLICY_SHA256,
          "status": status, "fixed": {"cohort_id": cohort["cohort_id"], "selected_at": cohort["selected_at"],
                                      "members_sha256": cohort["members_sha256"], "size": len(fixed),
                                      "selected_this_run": selected_now},
          "rotating": {"ranking_t": ranking["t"], "ranking_sha256": ranking.get("universe_sha256"),
                       "cursor": cursor, "pool_size": pool, "size": len(rot), "members": rot},
          "counts": counts, "stopped": stopped, "elapsed_s": elapsed, "rate_limited": rate_limited,
          "account_fields": ACCOUNT_FIELDS, "accounts": accounts, "flat_fields": FLAT_FIELDS, "flat": flat,
          "position_fields": POSITION_FIELDS, "positions": positions,
          "enrich_requests": enrich_requests, "enrich_weight_est": enrich_weight}
    added = C.append_rows("hl_accounts", [v2], partition=C.day)
    if enrich_out:
        C.append_rows("hl_enrich", [{"t": C.NOW, "schema": "hl_enrich/1", "policy": POLICY, "requests": enrich_out,
                                     "weight_est": enrich_weight, "queue_left": len(st.get("hl_enrich_queue", [])),
                                     "queue_dropped_total": st.get("hl_enrich_dropped", 0)}], partition=C.day)
    v1 = {"t": C.NOW, "status": status, "accounts_ranked": len(sample), "accounts_failed": len(failed),
          "failed": failed, "stopped": stopped, "elapsed_s": elapsed, "rate_limited": rate_limited,
          "ranked_at": ranking["t"], "min_account_value": ranking["min_account_value"],
          "rank_basis": f"{POLICY}: fixed cohort {len(fixed)} + rotating {len(rot)} (see data/hl_accounts)",
          "sampling_policy": POLICY,
          "fields": ["address", "account_value", "szi_btc", "entry_px", "liquidation_px", "leverage_type",
                     "leverage", "position_value", "unrealized_pnl", "margin_used"],
          "positions": btc_rows}
    C.append_rows("hl_positions/btc", [v1], partition=C.day)
    return {"added": added, "status": status, "positions": len(btc_rows), "detail_positions": len(positions),
            "accounts": counts, "accounts_failed": len(failed), "stopped": stopped, "elapsed_s": elapsed,
            "rate_limited": rate_limited, "enrich_requests": enrich_requests, "enrich_weight_est": enrich_weight,
            "fixed_selected_this_run": selected_now,
            "err": (f"degraded: {len(failed)}/{len(sample)} accounts failed, malformed or not attempted"
                    + (f" (stopped: {stopped})" if stopped else "")) if failed else None}
