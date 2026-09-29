# JBM desk report — 2026-09-29 00:56Z
Window 2026-09-22 00:56Z → 2026-09-29 00:56Z. report-2.6-2026-09-24.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-29 00:56Z by report-2.6-2026-09-24 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-29 00:51Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-29 00:53Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-29 00:51Z | 5 min |
| snapshots | 2026-09-29 00:50Z | 6 min |
| 1-minute prices (BTC perp) | 2026-09-29 00:51Z | 5 min |
| Deribit options | 2026-09-29 00:50Z | 6 min |
| Hyperliquid account sample | 2026-09-29 00:51Z | 5 min |
| Hyperliquid enrichment | 2026-09-29 00:51Z | 5 min |
| OKX insurance fund | 2026-09-29 00:51Z | 5 min |
| OKX liquidation orders | 2026-09-29 00:23Z | 33 min |
| research lab (lab-2.2-2026-09-24) | 2026-09-29 00:53Z | 4 min |

## 1. Collection health
526 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 501, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-29 00:56Z | `7,22,37,52 * * * *` | 514 | 501 (97%) | 502/515 slot intervals | 4/502 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.0, p90 20.9, max 30.5; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.0, p90 22.3, max 256.0.
Runtime per routine run (s): median 104, p90 113, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 502 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 526/526 | ok |
| binance_BTCUSDC | 526/526 | ok |
| binance_BTCUSDT | 526/526 | ok |
| binance_BTCUSD_PERP | 526/526 | ok |
| binance_coinm_prem | 526/526 | ok |
| binance_usdc_prem | 526/526 | ok |
| binance_usdt_prem | 526/526 | ok |
| bingx | 526/526 | ok |
| bitfinex_margin | 526/526 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 526/526 | ok |
| bitget_USDT | 526/526 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 485/485 | ok |
| cross_binance_SOLUSDT | 485/485 | ok |
| cross_hl_ETH | 485/485 | ok |
| cross_hl_SOL | 485/485 | ok |
| depth_binance_usdt | 526/526 | ok |
| depth_okx_usdt_swap | 526/526 | ok |
| deribit | 526/526 | ok |
| dydx | 526/526 | ok |
| gate | 526/526 | ok |
| hl_predicted_fundings | 526/526 | ok |
| htx | 522/526 | ok |
| hyperliquid | 526/526 | ok |
| kraken | 526/526 | ok |
| kucoin | 526/526 | ok |
| okx_BTC-USD-SWAP | 526/526 | ok |
| okx_BTC-USDT-SWAP | 526/526 | ok |
| paradex | 526/526 | ok |
| premium_parts | 526/526 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-29 00:00Z | 289 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-29 00:00Z | 289 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-29 00:00Z | 894 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-29 00:40Z | 10729 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-29 00:00Z | 894 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-29 00:40Z | 10729 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-28 23:00Z | 894 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-29 00:40Z | 10729 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-29 00:00Z | 894 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-29 00:40Z | 10729 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-29 00:00Z | 894 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-29 00:40Z | 10728 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-28 23:00Z | 3030 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-28 23:00Z | 869 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-29 00:00Z | 297 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-28 23:00Z | 3029 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-28 23:00Z | 3029 | 0 | 0 |

## 3. Forced-flow retention and revision
12339 distinct liquidation observations; 11 retained boundary probes.
- 2026-09-25 00:22Z: 0.96 days, 24 pages (observed source boundary).
- 2026-09-26 00:20Z: 0.98 days, 17 pages (observed source boundary).
- 2026-09-27 00:22Z: 1.0 days, 4 pages (observed source boundary).
- 2026-09-28 00:24Z: 0.94 days, 10 pages (observed source boundary).
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
Observed later revision after first live capture: n=30 active hours; mean 5.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 522 stored snapshots in 145 distinct hours from 2026-09-23 00:23Z to 2026-09-29 00:49Z; latest 790 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 522 stored snapshots in 145 distinct hours from 2026-09-23 00:23Z to 2026-09-29 00:49Z; latest 18 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 8961 bars 2026-09-22 19:28Z → 2026-09-29 00:48Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 8961 bars 2026-09-22 19:28Z → 2026-09-29 00:48Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 8961 bars 2026-09-22 19:28Z → 2026-09-29 00:48Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 8961 bars 2026-09-22 19:28Z → 2026-09-29 00:48Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 8961 bars 2026-09-22 19:28Z → 2026-09-29 00:48Z; 0 missing minutes inside the span.
- Deribit options schema 2: 485 runs; latest 790 with OI, 156 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 125.
- Hyperliquid sample v2: 485 snapshots; account checks by state ok_btc 10685, ok_flat 71651, ok_other 9814; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 164, ledger ok 649, twap not_attempted 2, twap ok 4035.
- OKX insurance fund rows: regular_update 485.
- Research lab: 27 runs in window; latest 2026-09-29 00:53Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 4/526 routine run(s), 2026-09-25 23:41Z → 2026-09-28 14:35Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot bitget_COIN: 4/526 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/526 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
