"""PS1-T1 replay runner (ps1-t1-runner-1.0.0, repo 2.30; brief section 15). PREPARED successor; PS1 v3 is untouched.

turnover-1.0.0 applied a band to a sequence of TARGET weights from zero, ignoring that PS1 trades from the drifted
actual weight at the captured mid, fills against captured books with fees and slippage, never borrows or shorts,
marks equity at mid before each trade and measures intervals between actual fill times. A turnover result computed
that way is not a PS1 result. This runner replays PS1's own verified ledger with PS1's own functions:

  executions   desk/paper_ps1.ledger(): the verified chain, in fill order; only executions PS1 counted (its joint
               rule: an execution exists for every arm or none), so no candidate is selected by missing data
  fills        desk/paper_ps1.rebalance(state, w_target, book, cost, band) at each execution's captured book
               (desk/paper_ps1._quotes), per scenario's costs (ps1-costs-1 ordinary / stressed)
  schedule     'every' k: a decision off the schedule targets the arm's current weight (no trade)
  accounting   interval log return ln(equity_pre_n / equity_pre_{n-1}), elapsed hours between fill times,
               paper_ps1.sharpe_dw (8,760 h basis), turnover as traded notional / mean equity, annualized
  check        band = PS1's own rebalance_band and every = 1 must reproduce PS1's recorded w_after and equity_pre
               exactly (reproduces_ps1); otherwise the runner refuses to report
Results on PS1's existing ledger are DISCOVERY data (PS1-T1 is not registered): turnover arithmetic is not
prospective acceptance.
"""
import hashlib
import inspect
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "desk"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

VERSION = "ps1-t1-runner-1.0.0"


def identities():
    import paper_ps1 as P
    return {"ps1_protocol_sha256": hashlib.sha256(Path(P.PROTOCOL).read_bytes()).hexdigest(),
            "paper_ps1_sha256": hashlib.sha256(Path(P.__file__).read_bytes()).hexdigest(),
            "rebalance_source_sha256": hashlib.sha256(inspect.getsource(P.rebalance).encode()).hexdigest(),
            "sharpe_dw_source_sha256": hashlib.sha256(inspect.getsource(P.sharpe_dw).encode()).hexdigest(),
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "ps1_job": P.VERSION}


def _executions(base):
    import paper_ps1 as P
    rows, fails = P.ledger(base)
    by = {}
    for r in rows:
        by.setdefault(r["execution_id"], {})[(r["scenario"], r["arm"])] = r
    order = sorted(by, key=lambda e: min(r["fill_time_ms"] for r in by[e].values()))
    return [by[e] for e in order], fails


def replay(base, band, every, arm, scenario, proto=None, execs=None, quotes=None):
    import paper_ps1 as P
    proto = proto or P.load_protocol()
    execs = execs if execs is not None else _executions(base)[0]
    quotes = quotes if quotes is not None else P._quotes(base)
    state = {"cash": float(proto["capital"]["start_equity_usdt"]), "btc": 0.0}
    out, prev = [], None
    traded = 0.0
    for k, ex in enumerate(execs):
        r = ex.get((scenario, arm))
        if r is None:
            raise ValueError(f"execution {next(iter(ex.values()))['execution_id']} lacks {scenario}/{arm}: joint rule broken")
        book = quotes[r["quote_id"]]
        mid = (float(book["bids"][0][0]) + float(book["asks"][0][0])) / 2
        eq = state["cash"] + state["btc"] * mid
        w_now = state["btc"] * mid / eq if eq > 0 else 0.0
        target = r["w_target"] if k % every == 0 else w_now
        state, rec = P.rebalance(state, target, book, proto["costs"][scenario], band)
        traded += abs(rec["notional"])
        row = {"execution_id": r["execution_id"], "fill_time_ms": r["fill_time_ms"], "w_after": rec["w_after"],
               "equity_pre": rec["equity_pre"], "notional": rec["notional"]}
        if prev is not None:
            row.update(log_return=math.log(rec["equity_pre"] / prev["equity_pre"]),
                       dt_h=(r["fill_time_ms"] - prev["fill_time_ms"]) / 3.6e6)
        out.append(row)
        prev = row
    rs = [x["log_return"] for x in out if "log_return" in x]
    dts = [x["dt_h"] for x in out if "dt_h" in x]
    hours = sum(dts)
    mean_eq = sum(x["equity_pre"] for x in out) / len(out) if out else None
    return {"band": band, "every": every, "arm": arm, "scenario": scenario, "intervals": len(rs), "hours": round(hours, 3),
            "sharpe_dw": P.sharpe_dw(rs, dts) if rs else None,
            "net_log_return": round(sum(rs), 6) if rs else None,
            "turnover_annualized": round(traded / mean_eq * 8760 / hours, 3) if hours and mean_eq else None,
            "rows": out}


def reproduces_ps1(base):
    """band = PS1's rebalance_band, every = 1: every arm and scenario must match PS1's recorded rows exactly."""
    import paper_ps1 as P
    proto = P.load_protocol()
    band = proto["policy"]["rebalance_band"]
    execs, _ = _executions(base)
    quotes = P._quotes(base)
    bad = []
    for s in P.SCENARIOS:
        for a in P.ARMS:
            got = replay(base, band, 1, a, s, proto, execs, quotes)["rows"]
            for g, ex in zip(got, execs):
                r = ex[(s, a)]
                if abs(g["w_after"] - r["w_after"]) > 1e-12 or abs(g["equity_pre"] - r["equity_pre"]) > 1e-6:
                    bad.append(f"{s}/{a} {r['execution_id']}")
                    break
    return {"ps1_band": band, "executions": len(execs), "mismatches": bad, "ok": not bad}


def run_family(base, candidates):
    """Every candidate configuration and the B2-VOL / B2-FIXED Sharpe differences under stressed costs, with the
    family count. Refuses unless the band-at-PS1 replay reproduces PS1."""
    chk = reproduces_ps1(base)
    if not chk["ok"]:
        raise ValueError(f"the replay does not reproduce PS1 ({chk['mismatches'][:3]}): no result reported")
    import paper_ps1 as P
    proto = P.load_protocol()
    execs, _ = _executions(base)
    quotes = P._quotes(base)
    res = {}
    for band in candidates["bands_abs_weight"]:
        for every in candidates["rebalance_every_decisions"]:
            for arm in ("B2", "VOL", "FIXED"):
                r = replay(base, band, every, arm, "stressed", proto, execs, quotes)
                res[f"{arm}|{band}|{every}"] = {k: r[k] for k in ("sharpe_dw", "net_log_return", "turnover_annualized",
                                                                   "intervals", "hours")}
    pairs = {}
    for band in candidates["bands_abs_weight"]:
        for every in candidates["rebalance_every_decisions"]:
            for other in ("VOL", "FIXED"):
                a, b = res[f"B2|{band}|{every}"]["sharpe_dw"], res[f"{other}|{band}|{every}"]["sharpe_dw"]
                pairs[f"B2-{other}|{band}|{every}"] = None if a is None or b is None else round(a - b, 4)
    return {"version": VERSION, "identities": identities(), "reproduces_ps1": chk, "configurations": res,
            "comparisons": pairs, "family_count": len(pairs),
            "evidence_class": "discovery replay of PS1's existing ledger (PS1-T1 not registered); not acceptance"}


if __name__ == "__main__":
    proto = json.loads((ROOT / "research/registrations/ps1-t1-prepared/protocol.json").read_text())
    print(json.dumps({k: v for k, v in run_family(ROOT, proto["candidates"]).items()}, indent=1, default=str))
