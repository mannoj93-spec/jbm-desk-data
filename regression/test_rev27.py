"""Regression tests for collector 2.7: option schema 2, Hyperliquid sampling policy v2 with bounded
enrichment, 1-minute price batches, the OKX insurance fund and cross-asset snapshot sources.

Recorded fixtures (regression/fixtures/*.json) are trimmed live responses captured 2026-09-23; they
are read into temporary directories only and never written to data/. Offline.
"""
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import collector
import enrich
import hlsample
import optionsbook
import research
import storage

FIX = Path(__file__).resolve().parent / "fixtures"
MIN = 60_000
H = 60 * MIN


def fixture(name):
    return json.loads((FIX / name).read_text())["response"]


class Env:
    """A temporary repository and a routed fake `get` with request accounting."""
    def __init__(self, now, routes):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name
        self.now, self.routes, self.calls = now, routes, []

    def get(self, url, body=None, **kw):
        self.calls.append((url, body))
        for match, answer in self.routes:
            if match(url, body):
                return answer(url, body) if callable(answer) else answer
        return None, "HTTP 404"

    def __enter__(self):
        self.stack = [patch.object(collector, "BASE", self.base), patch.object(collector, "NOW", self.now),
                      patch.object(collector, "get", side_effect=self.get), patch("collector.time.sleep")]
        for p in self.stack:
            p.start()
        return self

    def __exit__(self, *exc):
        for p in reversed(self.stack):
            p.stop()
        self.tmp.cleanup()

    def rows(self, rel):
        out = []
        for path in sorted(Path(self.base, "data", rel).glob("*.jsonl")):
            out.extend(storage.read_rows(path))
        return out


def url_has(text):
    return lambda url, body: text in url


def body_type(kind):
    return lambda url, body: isinstance(body, dict) and body.get("type") == kind


SUMMARY = fixture("deribit_book_summary_btc_option.json")
INSTRUMENTS = fixture("deribit_instruments_btc_option.json")
TICKER = fixture("deribit_ticker_option.json")
NOW = max(x["creation_timestamp"] for x in SUMMARY["result"]) + 30_000


def option_routes(instruments=INSTRUMENTS):
    return [(url_has("get_book_summary_by_currency"), (SUMMARY, None)),
            (url_has("get_instruments"), (instruments, None)),
            (url_has("/ticker?"), (TICKER, None))]


class OptionSchema2Tests(unittest.TestCase):
    def test_rows_keep_schema1_columns_and_states_are_distinct(self):
        with Env(NOW, option_routes()) as env:
            st = {}
            out = optionsbook.collect(collector, st)
            rec = env.rows("options/deribit_btc")[0]
            quotes = env.rows("options/deribit_btc_quotes")[0]
        self.assertEqual(rec["fields"], ["instrument", "open_interest_btc", "mark_iv"])
        self.assertTrue(all(len(r) == 3 for r in rec["rows"]))           # schema-1 readers unaffected
        zero = [x["instrument_name"] for x in SUMMARY["result"] if x["open_interest"] == 0]
        self.assertEqual(rec["zero_oi"], sorted(zero))
        self.assertEqual(rec["zero_oi_omitted"], len(zero))
        listed = {x["instrument_name"] for x in SUMMARY["result"]}
        absent = sorted(x["instrument_name"] for x in INSTRUMENTS["result"]
                        if x["instrument_name"] not in listed and x["expiration_timestamp"] > NOW)
        self.assertEqual(rec["absent"], absent)
        self.assertTrue(absent)                                           # the fixture holds absent instruments
        nobid = {x["instrument_name"] for x in SUMMARY["result"] if x.get("bid_price") is None and x["open_interest"] > 0}
        by_name = {r[0]: r for r in quotes["rows"]}
        for name in nobid:
            self.assertIsNone(by_name[name][3])                           # missing quote stays null, not 0
        self.assertIn("rolling 24h", quotes["unit"])
        self.assertEqual(quotes["fields"][6], "volume_24h_rolling_btc")
        self.assertEqual(out["zero_oi"], len(zero))
        self.assertLessEqual(len(rec["panel"]), optionsbook.PANEL_MAX)

    def test_quotes_are_hourly_and_reruns_are_idempotent(self):
        with Env(NOW, option_routes()) as env:
            st = {}
            optionsbook.collect(collector, st)
            optionsbook.collect(collector, st)                            # same run time: nothing new
            with patch.object(collector, "NOW", NOW + 15 * MIN):
                optionsbook.collect(collector, st)
            runs, quotes = env.rows("options/deribit_btc"), env.rows("options/deribit_btc_quotes")
        self.assertEqual(len(runs), 2)
        expected = 1 if (NOW + 15 * MIN) // H == NOW // H else 2
        self.assertEqual(len(quotes), expected)

    def test_expiry_and_listing_changes(self):
        first = dict(INSTRUMENTS, result=INSTRUMENTS["result"][:-1])
        with Env(NOW, option_routes(first)) as env:
            st = {}
            optionsbook.collect(collector, st)
            later = NOW + 24 * H
            other = Env(later, option_routes())
            with patch.object(collector, "NOW", later), patch.object(collector, "get", side_effect=other.get):
                rec = optionsbook.collect(collector, st)
            other.tmp.cleanup()
            listing = env.rows("options/deribit_btc_listing")
            runs = env.rows("options/deribit_btc")
        self.assertEqual(listing[0]["added"], [INSTRUMENTS["result"][-1]["instrument_name"]])
        expired = [n for n, m in st["deribit_meta"]["instruments"].items() if m[0] <= later]
        self.assertEqual(sorted(runs[-1]["past_expiry"]), sorted(n for n in expired if n in {x["instrument_name"] for x in SUMMARY["result"]}))
        self.assertTrue(rec["listing_change"])

    def test_metadata_refresh_failure_keeps_the_book(self):
        routes = [(url_has("get_instruments"), (None, "HTTP 503"))] + option_routes()   # first match wins
        with Env(NOW, routes) as env:
            out = optionsbook.collect(collector, {})
            rec = env.rows("options/deribit_btc")[0]
        self.assertTrue(out["meta"].startswith("refresh failed"))
        self.assertEqual(rec["absent"], [])
        self.assertGreater(len(rec["rows"]), 0)

    def test_panel_selection_is_deterministic_and_bounded(self):
        meta = {x["instrument_name"]: [x["expiration_timestamp"]] for x in INSTRUMENTS["result"]}
        rows = [[x["instrument_name"], x["open_interest"], x["mark_iv"]] for x in SUMMARY["result"]
                if x["open_interest"] > 0 and x.get("mark_iv")]
        und = {x["instrument_name"].split("-")[1]: x["underlying_price"] for x in SUMMARY["result"]}
        a = optionsbook.select_panel(rows, und, meta, NOW)
        self.assertEqual(a, optionsbook.select_panel(list(reversed(rows)), und, meta, NOW))
        self.assertLessEqual(len(a), optionsbook.PANEL_MAX)

    def test_black76_delta_convention(self):
        self.assertAlmostEqual(optionsbook.black76_delta(100, 100, 50, 1.0, "C"), 0.5987, places=4)
        c, p = optionsbook.black76_delta(100, 110, 60, 0.5, "C"), optionsbook.black76_delta(100, 110, 60, 0.5, "P")
        self.assertAlmostEqual(c - p, 1.0, places=12)                     # forward delta put-call parity
        self.assertIsNone(optionsbook.black76_delta(100, 100, 50, 0, "C"))


def hl_routes(n_universe=400, accounts=None):
    board = {"leaderboardRows": [{"ethAddress": f"0x{i:040x}", "accountValue": str(10_000_000 - i)}
                                 for i in range(n_universe)]}
    multi, flat = fixture("hl_clearinghouse_multi.json"), fixture("hl_clearinghouse_flat.json")

    def account(url, body):
        user = body["user"]
        if accounts and user in accounts:
            return accounts[user]
        return (multi, None) if int(user, 16) % 7 == 0 else (flat, None)
    return [(url_has("leaderboard"), (board, None)),
            (body_type("clearinghouseState"), account),
            (body_type("userFillsByTime"), (fixture("hl_user_fills_by_time.json"), None)),
            (body_type("userNonFundingLedgerUpdates"), (fixture("hl_ledger_updates.json"), None)),
            (body_type("twapHistory"), ([], None))]


class HyperliquidSamplingTests(unittest.TestCase):
    def run_once(self, env, st):
        return hlsample.collect(collector, st)

    def test_budget_membership_and_states(self):
        with Env(NOW, hl_routes()) as env:
            st = {}
            out = self.run_once(env, st)
            rec = env.rows("hl_accounts")[0]
            v1 = env.rows("hl_positions/btc")[0]
            cohort = json.loads(Path(env.base, hlsample.FIXED_PATH).read_text())
            info_calls = [c for c in env.calls if c[1] is not None]
        self.assertLessEqual(len(info_calls), 200)                        # the 2.6 per-run account budget
        self.assertEqual(len([c for c in info_calls if c[1]["type"] == "clearinghouseState"]), 190)
        self.assertLessEqual(out["enrich_requests"], hlsample.ENRICH_MAX)
        ids = [a[0] for a in rec["accounts"]] + [f[0] for f in rec["flat"]]
        self.assertEqual(len(ids), 190)
        self.assertEqual(len(set(ids)), 190)                              # every sampled account exactly once
        self.assertEqual(len(cohort["members"]), 100)
        self.assertEqual(cohort["members"][0][0], f"0x{0:040x}")          # top by account value at selection
        self.assertEqual(len(rec["rotating"]["members"]), 90)
        self.assertFalse(set(rec["rotating"]["members"]) & {m[0] for m in cohort["members"]})
        states = {a[1] for a in rec["accounts"]}
        self.assertTrue(states <= {"ok_btc", "ok_other", "failed", "not_attempted"})
        self.assertEqual(rec["counts"]["ok_flat"], len(rec["flat"]))
        self.assertTrue(all(p[1] in hlsample.DETAIL_COINS for p in rec["positions"]))
        self.assertEqual(v1["sampling_policy"], hlsample.POLICY)          # 2.6 readers still get BTC rows
        self.assertTrue(all(len(p) == 10 for p in v1["positions"]))

    def test_fixed_cohort_is_frozen_and_rotation_advances(self):
        with Env(NOW, hl_routes()) as env:
            st = {}
            self.run_once(env, st)
            first = json.loads(Path(env.base, hlsample.FIXED_PATH).read_text())
            later = NOW + 7 * H                                           # ranking refresh with a new order
            reordered = [(url_has("leaderboard"), ({"leaderboardRows": [
                {"ethAddress": f"0x{i:040x}", "accountValue": str(i)} for i in range(400)]}, None))] + hl_routes()[1:]
            env2 = Env(later, reordered)
            with patch.object(collector, "NOW", later), patch.object(collector, "get", side_effect=env2.get):
                self.run_once(env, st)
            env2.tmp.cleanup()
            second = json.loads(Path(env.base, hlsample.FIXED_PATH).read_text())
            recs = env.rows("hl_accounts")
        self.assertEqual(first, second)                                   # never re-selected
        self.assertNotEqual(recs[0]["rotating"]["members"], recs[1]["rotating"]["members"])
        self.assertEqual(recs[1]["rotating"]["cursor"], 90)
        self.assertFalse(recs[1]["fixed"]["selected_this_run"])

    def test_malformed_and_failed_accounts_are_failures_not_flat(self):
        bad = {f"0x{1:040x}": ({}, None), f"0x{2:040x}": (None, "HTTP 503")}
        with Env(NOW, hl_routes(accounts=bad)) as env:
            self.run_once(env, {})
            rec = env.rows("hl_accounts")[0]
        failed = {a[0]: a[2] for a in rec["accounts"] if a[1] == "failed"}
        self.assertEqual(set(failed), {"F1", "F2"})
        self.assertIn("missing marginSummary", failed["F1"])

    def test_deadline_marks_not_attempted(self):
        clock = {"t": 0.0}

        def tick():
            clock["t"] += 2.0                                            # 150 accounts fit in 300 s
            return clock["t"]
        with Env(NOW, hl_routes()) as env, patch("collector.time.monotonic", side_effect=tick):
            out = self.run_once(env, {})
            rec = env.rows("hl_accounts")[0]
        self.assertEqual(out["stopped"], "deadline")
        self.assertTrue(any(a[1] == "not_attempted" for a in rec["accounts"]))

    def test_close_flip_and_halving_queue_confirmation_checks(self):
        st = {}
        hlsample.update_triggers(st, "a", 1, 2.0, True)
        hlsample.update_triggers(st, "a", 2, 0.0, True)
        hlsample.update_triggers(st, "b", 1, 2.0, True)
        hlsample.update_triggers(st, "b", 2, -1.0, True)
        hlsample.update_triggers(st, "c", 1, 2.0, True)
        hlsample.update_triggers(st, "c", 2, 0.9, True)
        hlsample.update_triggers(st, "d", 1, 2.0, True)
        hlsample.update_triggers(st, "d", 2, 1.5, True)                  # -25%: no trigger
        hlsample.update_triggers(st, "e", 1, 2.0, True)
        hlsample.update_triggers(st, "e", 2, None, False)                 # failed check: never a close
        reasons = {q["user"]: q["reason"] for q in st["hl_enrich_queue"]}
        self.assertEqual(reasons, {"a": "btc_position_closed", "b": "btc_position_flipped", "c": "btc_position_halved"})
        self.assertEqual(st["hl_enrich_queue"][0]["from"], 1)             # window starts at the prior observation

    def test_enrichment_is_bounded_and_records_ledger_types(self):
        st = {"hl_enrich_queue": [{"user": f"0x{i:040x}", "from": NOW - H, "to": NOW, "reason": "btc_position_closed"}
                                  for i in range(8)]}
        with Env(NOW, hl_routes()) as env:
            out, weight, requests = hlsample.enrich(collector, st, [[f"0x{i:040x}", i, 1.0] for i in range(100)],
                                                    collector.time.monotonic() + 100)
        self.assertLessEqual(requests, hlsample.ENRICH_MAX)
        self.assertLessEqual(len(out), hlsample.ENRICH_MAX)
        self.assertEqual(len(st["hl_enrich_queue"]), 5)                   # 3 items served, the rest wait
        ledger = next(r for r in out if r["kind"] == "ledger")
        kinds = {e[1] for e in ledger["ledger"]}
        self.assertNotIn("spotTransfer", kinds)
        self.assertIn("deposit", kinds)
        fills = next(r for r in out if r["kind"] == "fills")
        self.assertEqual(len(fills["fills"][0]), len(hlsample.FILL_FIELDS))

    def test_v1_policy_is_a_reversible_switch(self):
        with patch.dict(os.environ, {"HL_SAMPLING_POLICY": "v1", "OPTIONS_SCHEMA": "1"}), \
             patch.object(collector, "collect_hl_positions", return_value={"v": 1}) as v1, \
             patch.object(collector, "collect_deribit_options", return_value={"o": 1}) as o1, \
             patch.dict(collector.RUN, {"forward": {}}):
            collector.collect_forward({})
        v1.assert_called_once()
        o1.assert_called_once()


def klines(start, n, bad=False):
    out = []
    for i in range(n):
        t = start + i * MIN
        out.append([t, "100", "101", "99", "100.5", "2", t + MIN - 1, "200", 5, "1", "100", "0"])
    if bad:
        out[1][2] = "90"                                                  # high below open: malformed
    return out


class PriceBatchTests(unittest.TestCase):
    def test_only_closed_bars_checkpointed_and_idempotent(self):
        now = 1_790_000_000_000 // MIN * MIN + 30_000                     # half a minute into a bar
        start = now // MIN * MIN - 10 * MIN

        def answer(url, body):
            s = int(url.split("startTime=")[1].split("&")[0])
            e = int(url.split("endTime=")[1].split("&")[0])
            n = max(0, min((now // MIN * MIN - s) // MIN + 1, 1500))      # includes the open bar
            return [k for k in klines(s, n) if k[0] <= e], None
        with Env(now, [(url_has("klines"), answer)]) as env:
            st = {"series": {"binance_klines_1m_BTCUSDT_perp": start}}
            out = enrich.klines(collector, st, "binance_klines_1m_BTCUSDT_perp")
            again = enrich.klines(collector, st, "binance_klines_1m_BTCUSDT_perp")
            batches = env.rows("prices/binance_klines_1m_BTCUSDT_perp")
            ctx = research.Ctx(env.base, None, now)
            bars = ctx.prices("binance_klines_1m_BTCUSDT_perp")
            early = research.Ctx(env.base, None, batches[0]["observed_at"] - 1).prices("binance_klines_1m_BTCUSDT_perp")
        self.assertEqual(out["added"], 9)                                 # start+1m .. now-1m-open bar excluded
        self.assertEqual(again["added"], 0)
        self.assertEqual(len(batches), 1)
        self.assertEqual(st["series"]["binance_klines_1m_BTCUSDT_perp"], now // MIN * MIN - MIN)
        self.assertTrue(all(b["t"] + MIN <= now for b in bars))
        self.assertEqual(early, [])                                       # not visible before it was written

    def test_malformed_page_is_rejected_and_checkpoint_kept(self):
        now = 1_790_000_000_000
        with Env(now, [(url_has("klines"), (klines(now - 20 * MIN, 5, bad=True), None))]) as env:
            st = {"series": {"binance_klines_1m_BTCUSDT_perp": now - 21 * MIN}}
            out = enrich.klines(collector, st, "binance_klines_1m_BTCUSDT_perp")
        self.assertEqual(out["err"], "malformed kline")
        self.assertEqual(st["series"]["binance_klines_1m_BTCUSDT_perp"], now - 21 * MIN)

    def test_duplicate_bars_across_batches_first_observation_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "data/prices/binance_klines_1m_BTCUSDT_perp/2026-09.jsonl")
            b1 = {"t": 0, "t_last": MIN, "fields": ["t", "o", "h", "l", "c"], "bars": [[0, 1, 1, 1, 1], [MIN, 2, 2, 2, 2]],
                  "observed_at": 3 * MIN}
            b2 = {"t": MIN, "t_last": 2 * MIN, "fields": ["t", "o", "h", "l", "c"],
                  "bars": [[MIN, 9, 9, 9, 9], [2 * MIN, 3, 3, 3, 3]], "observed_at": 4 * MIN}
            storage.append_unique(path, [b1, b2], lambda r: (r["t"], r["t_last"]))
            bars = research.Ctx(tmp, None, 10 * MIN).prices("binance_klines_1m_BTCUSDT_perp")
        self.assertEqual([b["o"] for b in bars], [1, 2, 3])


class InsuranceTests(unittest.TestCase):
    def test_only_newer_event_rows_are_added(self):
        latest = fixture("okx_insurance_fund.json")
        event = {"code": "0", "data": [{"details": [{"ts": "1790000000000", "type": "bankruptcy_loss", "amt": "-5",
                                                     "balance": "10", "adlType": ""}], "total": "1"}]}
        empty = {"code": "0", "data": [{"details": [], "total": "1"}]}
        routes = [(lambda u, b: "type=bankruptcy_loss" in u, (event, None)),
                  (lambda u, b: "type=" in u, (empty, None)),
                  (url_has("insurance-fund"), (latest, None))]
        with Env(NOW, routes) as env:
            st = {}
            first = enrich.insurance(collector, st)
            second = enrich.insurance(collector, st)
            rows = env.rows("okx_insurance")
        self.assertEqual(first["added"], 2)
        self.assertEqual(second["added"], 0)
        self.assertEqual({r["type"] for r in rows}, {"regular_update", "bankruptcy_loss"})


class CrossAssetTests(unittest.TestCase):
    def test_units_and_quote_currencies_are_normalised(self):
        meta = fixture("hl_meta_asset_ctxs.json")
        prem = {"ETHUSDT": {"markPrice": "2500.5", "indexPrice": "2501", "lastFundingRate": "0.0001",
                            "nextFundingTime": 1, "time": 5},
                "SOLUSDT": {"markPrice": "114.2", "indexPrice": "114.3", "lastFundingRate": "-0.00005",
                            "nextFundingTime": 1, "time": 5}}
        routes = [(body_type("metaAndAssetCtxs"), (meta, None)),
                  (lambda u, b: "premiumIndex?symbol=ETHUSDT" in u, (prem["ETHUSDT"], None)),
                  (lambda u, b: "premiumIndex?symbol=SOLUSDT" in u, (prem["SOLUSDT"], None)),
                  (lambda u, b: "openInterest?symbol=ETHUSDT" in u, ({"openInterest": "1000", "time": 6}, None)),
                  (lambda u, b: "openInterest?symbol=SOLUSDT" in u, ({"openInterest": "10", "time": 6}, None))]
        with Env(NOW, routes):
            S = collector.snapshot()
        eth = S["cross_binance_ETHUSDT"]
        self.assertEqual((eth["st"], eth["quote"], eth["funding_interval_h"]), ("ok", "USDT", 8))
        self.assertAlmostEqual(eth["oi_quote"], 1000 * 2500.5)
        hl = S["cross_hl_ETH"]
        uni = meta[0]["universe"]
        ctx = meta[1][next(i for i, u in enumerate(uni) if u["name"] == "ETH")]
        self.assertEqual((hl["st"], hl["quote"], hl["funding_interval_h"]), ("ok", "USD", 1))
        self.assertAlmostEqual(hl["oi_quote"], round(float(ctx["openInterest"]) * float(ctx["markPx"]), 2))
        self.assertNotIn("cross_hl_ETH", S["oi"])                         # never counted as a BTC book


class IsolationTests(unittest.TestCase):
    def test_enrichment_failure_never_blocks_the_run_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "registry").mkdir()
            storage.atomic_json(Path(tmp) / "state/checkpoints.json", {"series": {}, "liq_last_ts": None})
            fresh = {"series": {}, "liq": {}, "snap": {}, "errors": {}, "forward": {},
                     "http": {"requests": 0, "failed": 0, "rate_limited": 0, "rate_limited_by_host": {},
                              "deadline_skipped": 0, "circuit_skipped": 0}}
            with patch.object(collector, "BASE", tmp), patch.object(collector, "STATE", str(Path(tmp) / "state/checkpoints.json")), \
                 patch.object(collector, "get", return_value=(None, "HTTP 503")), patch("collector.time.sleep"), \
                 patch.object(enrich, "collect", side_effect=RuntimeError("boom")), \
                 patch.dict(collector.RUN, fresh), patch("sys.stdout", io.StringIO()):
                with self.assertRaises(SystemExit):
                    collector.main()
            runs = storage.read_rows(next(Path(tmp, "data/runs").glob("*.jsonl")))
        self.assertIn("boom", runs[0]["enrich"]["err"])
        self.assertIn("enrich", runs[0]["stage_s"])

    def test_enrich_stage_share_is_bounded(self):
        self.assertLessEqual(sum(collector.STAGE_SHARE.values()), 0.9)    # enrich runs after the forward books, capped
        self.assertEqual(collector.STAGE_SHARE["enrich"], 0.10)


if __name__ == "__main__":
    unittest.main()
