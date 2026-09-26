# JBM desk report — 2026-09-26 18:48Z
Window 2026-09-19 18:48Z → 2026-09-26 18:48Z. report-2.6-2026-09-24.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-26 18:48Z by report-2.6-2026-09-24 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-26 18:46Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-26 18:48Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-26 18:46Z | 2 min |
| snapshots | 2026-09-26 18:45Z | 3 min |
| 1-minute prices (BTC perp) | 2026-09-26 18:46Z | 2 min |
| Deribit options | 2026-09-26 18:45Z | 3 min |
| Hyperliquid account sample | 2026-09-26 18:46Z | 2 min |
| Hyperliquid enrichment | 2026-09-26 18:46Z | 2 min |
| OKX insurance fund | 2026-09-26 18:46Z | 2 min |
| OKX liquidation orders | 2026-09-26 16:16Z | 152 min |
| research lab (lab-2.2-2026-09-24) | 2026-09-26 18:48Z | 0 min |

## 1. Collection health
316 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 291, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-26 18:48Z | `7,22,37,52 * * * *` | 298 | 291 (98%) | 291/298 slot intervals | 2/292 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 13.8, p90 20.9, max 30.1; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.0, p90 23.2, max 256.0.
Runtime per routine run (s): median 103, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 292 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 316/316 | ok |
| binance_BTCUSDC | 316/316 | ok |
| binance_BTCUSDT | 316/316 | ok |
| binance_BTCUSD_PERP | 316/316 | ok |
| binance_coinm_prem | 316/316 | ok |
| binance_usdc_prem | 316/316 | ok |
| binance_usdt_prem | 316/316 | ok |
| bingx | 316/316 | ok |
| bitfinex_margin | 316/316 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 316/316 | ok |
| bitget_USDT | 316/316 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 275/275 | ok |
| cross_binance_SOLUSDT | 275/275 | ok |
| cross_hl_ETH | 275/275 | ok |
| cross_hl_SOL | 275/275 | ok |
| depth_binance_usdt | 316/316 | ok |
| depth_okx_usdt_swap | 316/316 | ok |
| deribit | 316/316 | ok |
| dydx | 316/316 | ok |
| gate | 316/316 | ok |
| hl_predicted_fundings | 316/316 | ok |
| htx | 314/316 | ok |
| hyperliquid | 316/316 | ok |
| kraken | 316/316 | ok |
| kucoin | 316/316 | ok |
| okx_BTC-USD-SWAP | 316/316 | ok |
| okx_BTC-USDT-SWAP | 316/316 | ok |
| paradex | 316/316 | ok |
| premium_parts | 316/316 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-26 16:00Z | 282 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-26 16:00Z | 282 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-26 18:00Z | 840 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-26 18:35Z | 10080 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-26 18:00Z | 840 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-26 18:35Z | 10080 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-26 17:00Z | 840 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-26 18:35Z | 10080 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-26 18:00Z | 840 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-26 18:35Z | 10080 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-26 18:00Z | 840 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-26 18:35Z | 10079 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-26 17:00Z | 2976 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-26 17:00Z | 815 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-26 16:00Z | 290 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-26 17:00Z | 2975 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-26 17:00Z | 2975 | 0 | 0 |

## 3. Forced-flow retention and revision
9366 distinct liquidation observations; 8 retained boundary probes.
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 16:14Z: 1.0 days, 32 pages (observed source boundary).
- 2026-09-24 00:21Z: 1.0 days, 32 pages (observed source boundary).
- 2026-09-25 00:22Z: 0.96 days, 24 pages (observed source boundary).
- 2026-09-26 00:20Z: 0.98 days, 17 pages (observed source boundary).
Observed later revision after first live capture: n=19 active hours; mean 5.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 312 stored snapshots in 91 distinct hours from 2026-09-23 00:23Z to 2026-09-26 18:44Z; latest 795 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 312 stored snapshots in 91 distinct hours from 2026-09-23 00:23Z to 2026-09-26 18:44Z; latest 18 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 5716 bars 2026-09-22 19:28Z → 2026-09-26 18:43Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 5716 bars 2026-09-22 19:28Z → 2026-09-26 18:43Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 5716 bars 2026-09-22 19:28Z → 2026-09-26 18:43Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 5716 bars 2026-09-22 19:28Z → 2026-09-26 18:43Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 5716 bars 2026-09-22 19:28Z → 2026-09-26 18:43Z; 0 missing minutes inside the span.
- Deribit options schema 2: 275 runs; latest 795 with OI, 197 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 71.
- Hyperliquid sample v2: 275 snapshots; account checks by state ok_btc 6044, ok_flat 40597, ok_other 5609; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 84, ledger ok 359, twap not_attempted 2, twap ok 2305.
- OKX insurance fund rows: regular_update 275.
- Research lab: 18 runs in window; latest 2026-09-26 18:48Z: exploratory 8 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 2/316 routine run(s), 2026-09-25 23:41Z → 2026-09-26 03:14Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot bitget_COIN: 4/316 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/316 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
