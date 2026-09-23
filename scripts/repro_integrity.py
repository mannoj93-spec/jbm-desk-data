#!/usr/bin/env python3
"""Before/after reproductions of the 2.7 research-integrity review, runnable against any code tree.

  python scripts/repro_integrity.py [CODE_ROOT]

CODE_ROOT defaults to this checkout; point it at a checkout of 900d0b1 to reproduce the reviewed
behaviour. Only APIs present in both versions are used (module run/build functions, account
transitions, the streaming Recorder); the lab-2.0 summary is reached through a small adapter.
Prints one JSON object per finding. Synthetic data only, in temporary directories.
"""
import gzip
import inspect
import json
import math
import os
from pathlib import Path
import random
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from lab import experiments, outcomes  # noqa: E402
from lab.events import event_record  # noqa: E402
from lab.modules import accounts, cross_asset, liquidity, options_disagreement  # noqa: E402
from stream import service, storage  # noqa: E402
from stream.books import BybitBook  # noqa: E402

T0 = 1_790_121_600_000
MIN, H = 60_000, 3_600_000
NEW = "t_inputs" in inspect.signature(event_record).parameters


def bars(prices, start=T0):
    out, prev = {}, prices[0]
    for i, p in enumerate(prices):
        t = start + i * MIN
        out[t] = {"t": t, "o": prev, "h": max(prev, p) * 1.0001, "l": min(prev, p) * 0.9999, "c": p, "v": 10.0,
                  "tbv": 5.0, "avail": t + MIN}
        prev = p
    return out


def walk(n, seed):
    rng, p, out = random.Random(seed), 100.0, []
    for _ in range(n):
        p *= math.exp(rng.gauss(0, 0.0005))
        out.append(p)
    return out


def ev(t, avail, group="test"):
    return event_record("d", "v", t, t, avail, 1, group, {"severity": 1.0}, "h", "as-of replay: repro", {}, {}, "c")


def finding2():
    """Two events an hour apart whose inputs arrive together."""
    b = bars(walk(3000, 1))
    avail = T0 + 2 * H + 30_000
    evs = [ev(T0, avail), ev(T0 + H, avail)]
    now = T0 + 2900 * MIN
    design = {"id": "T", "outcome": {"metric": "ret_net", "horizons_min": [30, 60, 240, 480], "primary_horizon": 30},
              "comparison": {"test_group": "test", "reference_group": "reference", "hypothesised_sign": 1},
              "baseline_predictors": [], "min_retained_observations": 100, "_version": "x"}
    entries = [outcomes.label(e["t_available"], 1, b, now, (30,))[30]["entry_t"] for e in evs]
    if NEW:
        from lab.baseline import Baseline
        rows = [(e, outcomes.label(e["t_available"], 1, b, now), None) for e in evs]
        s = experiments.summarize(rows, design, None, "reanalysis", {}, Baseline([]), 1)
        got = {h: s[str(h)]["counts"]["test"]["retained"] for h in (30, 60, 240, 480)}
    else:
        rows = [(e, outcomes.label(e["t_available"], 1, b, now)) for e in evs]
        s = experiments.summarize(rows, design, None, "exploratory")
        got = {h: s[str(h)]["independent_test_episodes"] for h in (30, 60, 240, 480)}
    return {"finding": 2, "same_entry_bar": entries[0] == entries[1], "counted_as_separate_observations": got}


def finding3():
    """Delay a prior BTC bar used in the sigma window by 49 minutes."""
    def data():
        d = {a: bars(walk(2880, s)) for a, s in (("BTC", 11), ("ETH", 12), ("SOL", 13))}
        for k in range(5):
            t = T0 + (1500 + k) * MIN
            d["ETH"][t]["c"] = d["ETH"][t]["o"] * 0.996
            d["ETH"][t + MIN]["o"] = d["ETH"][t]["c"]
        return d
    params = {"k_sigma": 3.0}
    base = [e for e in cross_asset.build(data(), "as-of replay: repro", params, "c")[0] if e["features"].get("alt") == "ETH"]
    e0 = base[0]
    d = data()
    prior = e0["t_event"] - 40 * MIN
    d["BTC"][prior]["avail"] = e0["t_event"] + 49 * MIN
    got = [e for e in cross_asset.build(d, "as-of replay: repro", params, "c")[0]
           if e["t_event"] == e0["t_event"] and e["features"].get("alt") == "ETH"]
    e1 = got[0] if got else None
    return {"finding": 3, "delayed_input_available_at": d["BTC"][prior]["avail"],
            "event_t_available": e1["t_available"] if e1 else None,
            "minutes_event_precedes_input": round((d["BTC"][prior]["avail"] - e1["t_available"]) / MIN, 1) if e1 else None}


ACC = ["account_id", "state", "reason", "clearinghouse_time_offset_ms", "account_value", "total_ntl_pos",
       "total_margin_used", "total_raw_usd", "cross_account_value", "cross_maintenance_margin_used", "withdrawable",
       "n_positions", "other_n", "other_long_ntl", "other_short_ntl", "other_margin_used", "other_unrealized_pnl"]


def finding5():
    """Ledger query covers minutes 0-80 with a deposit at minute 5; transition over minutes 60-75."""
    def rec(t, szi):
        return {"t": t, "observed_at": t + MIN, "address_of": {"F0": "0xa"}, "account_fields": ACC,
                "accounts": [["F0", "ok_btc", None, 0, 1e6, 0, 0, 0, 1e6, 1e4, 0, 1, 0, 0, 0, 0, 0]],
                "positions": [["F0", "BTC", szi, 100.0, 50.0, "cross", 5, 1e5, -3e4, 1e4, 0, 40]], "flat": []}

    class S:
        def hl_accounts(self):
            return [rec(T0 + 60 * MIN, 1.0), rec(T0 + 75 * MIN, 2.0)]

        def hl_enrich(self):
            return [{"t": T0 + 80 * MIN, "observed_at": T0 + 81 * MIN, "requests": [
                {"kind": "ledger", "user": "0xa", "window": [T0, T0 + 80 * MIN], "status": "ok",
                 "ledger": [[T0 + 5 * MIN, "deposit", {"type": "deposit"}]], "truncated_at_source": False}]}]
    return {"finding": 5, "transition_transfer_label": accounts.transitions(S())[0]["transfer"]}


def finding6():
    """A complete synthetic stream, exact timestamps versus 1-2 ms of jitter, through the Recorder."""
    def run(jitter):
        with tempfile.TemporaryDirectory() as root:
            store = storage.LocalStore(root)
            rec = service.Recorder({"sample_max_age_ms": 20000}, store)
            book = BybitBook("BTCUSDT")
            rng = random.Random(5)
            for s in range(7200):
                bid, ask = (1.0, 4.0) if 4000 <= s < 4070 else ((5.0, 0.5) if 5000 <= s < 5005 else (10.0, 10.0))
                t = T0 + s * 1000 + (rng.choice([1, 2]) if jitter else 0)
                book.apply({"type": "snapshot", "ts": t - 50,
                            "data": {"u": s + 1, "b": [["100.00", str(bid)]], "a": [["100.01", str(ask)]]}})
                rec.sample(book, t)
            store.flush()
            with patch.dict(os.environ, {"STREAM_DATA_DIR": root}):
                lab = type("L", (), {"code": "c", "store": type("S", (), {"bars": lambda s, n: {}})()})()
                p = liquidity.run(lab, {"shock_frac": 0.3, "recover_frac": 0.8, "recovery_s": 60})["passes"][0]
            return {"events": len(p["events"]), "controls": len(p["controls"])}
    return {"finding": 6, "exact": run(False), "jitter_1_2ms": run(True)}


def finding7():
    """All panel quotes stale: does anything change beyond counters?"""
    fields = ["instrument", "timestamp", "best_bid_price", "best_bid_amount", "best_ask_price", "best_ask_amount",
              "mark_price", "mark_iv", "bid_iv", "ask_iv", "delta"]

    def run(offset_ms):
        recs, snaps = [], []
        for k in range(40):
            t = T0 + k * 15 * MIN
            rr = -5.0 if k == 39 else 0.1 * (k % 3)
            panel = [["BTC-30SEP26-90000-C", t + offset_ms, 0.010, 5, 0.011, 5, 0.0105, 50.0, 49.0, 51.0, 0.25],
                     ["BTC-30SEP26-70000-P", t + offset_ms, 0.010, 5, 0.011, 5, 0.0105, 55.0, 54.0, 56.0, -0.25]]
            recs.append({"t": t, "t_event": t, "observed_at": t + MIN, "rr": rr, "panel_fields": fields, "panel": panel,
                         "rows": [], "underlying": {}})
            snaps.append({"t": t, "observed_at": t + MIN, "binance_usdt_prem": {
                "st": "ok", "funding_live_predicted_8h": 0.0001 * (k % 3) if k < 39 else 0.01}})

        class S:
            def options(self):
                return recs

            def snaps(self):
                return snaps

            def bars(self, name):
                return {}
        lab = type("L", (), {"store": S(), "code": "c"})()
        with patch.object(options_disagreement, "surface", lambda rec: {"rr25_7d": rec["rr"]}):
            p = options_disagreement.run(lab, {"z": 2.0, "z_window": 30, "min_records": 10})["passes"][0]
        return {"event_groups": [e["group"] for e in p["events"]],
                "rr25_7d_of_event": [e["features"]["rr25_7d"] for e in p["events"]],
                "panel_counters": {k: v for k, v in (p["events"][0]["features"] if p["events"] else {}).items()
                                   if k.startswith("panel_") or k.startswith("rr25_7d_q")}}
    return {"finding": 7, "fresh_quotes": run(-1000), "all_quotes_stale": run(-3 * H)}


if __name__ == "__main__":
    print(json.dumps({"code_root": str(ROOT), "lab_version": __import__("lab.common").common.LAB_VERSION}))
    for f in (finding2, finding3, finding5, finding6, finding7):
        try:
            print(json.dumps(f(), default=str))
        except Exception as exc:                         # report, do not hide, an API mismatch
            print(json.dumps({"finding": f.__name__, "error": f"{type(exc).__name__}: {exc}"}))
