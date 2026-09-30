# JBM desk report — 2026-09-30 06:54Z
Window 2026-09-23 06:54Z → 2026-09-30 06:54Z. report-2.6-2026-09-24.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-30 06:54Z by report-2.6-2026-09-24 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-30 06:43Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-30 06:53Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-30 06:43Z | 11 min |
| snapshots | 2026-09-30 06:42Z | 12 min |
| 1-minute prices (BTC perp) | 2026-09-30 06:43Z | 11 min |
| Deribit options | 2026-09-30 06:42Z | 12 min |
| Hyperliquid account sample | 2026-09-30 06:43Z | 11 min |
| Hyperliquid enrichment | 2026-09-30 06:43Z | 11 min |
| OKX insurance fund | 2026-09-30 06:43Z | 11 min |
| OKX liquidation orders | 2026-09-30 06:41Z | 12 min |
| research lab (lab-2.2-2026-09-24) | 2026-09-30 06:53Z | 1 min |

## 1. Collection health
626 routine runs in window, by trigger: not recorded (github) 9, schedule 616, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-23 06:54Z → 2026-09-23 16:06Z | `7 * * * *` | 9 | 9 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 9/9, an upper bound (manual runs indistinguishable) | 8/8 slot intervals | 0/9 |
| 2026-09-23 16:06Z → 2026-09-30 06:54Z | `7,22,37,52 * * * *` | 634 | 616 (97%) | 616/635 slot intervals | 6/617 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.1, p90 20.9, max 30.5; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.2, p90 21.1, max 65.2.
Runtime per routine run (s): median 104, p90 113, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 617 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 626/626 | ok |
| binance_BTCUSDC | 626/626 | ok |
| binance_BTCUSDT | 626/626 | ok |
| binance_BTCUSD_PERP | 626/626 | ok |
| binance_coinm_prem | 626/626 | ok |
| binance_usdc_prem | 626/626 | ok |
| binance_usdt_prem | 626/626 | ok |
| bingx | 626/626 | ok |
| bitfinex_margin | 626/626 | ok |
| bitget_USDC | 626/626 | ok |
| bitget_USDT | 626/626 | ok |
| cross_binance_ETHUSDT | 600/600 | ok |
| cross_binance_SOLUSDT | 600/600 | ok |
| cross_hl_ETH | 600/600 | ok |
| cross_hl_SOL | 600/600 | ok |
| depth_binance_usdt | 626/626 | ok |
| depth_okx_usdt_swap | 626/626 | ok |
| deribit | 626/626 | ok |
| dydx | 626/626 | ok |
| gate | 626/626 | ok |
| hl_predicted_fundings | 626/626 | ok |
| htx | 620/626 | ok |
| hyperliquid | 626/626 | ok |
| kraken | 626/626 | ok |
| kucoin | 626/626 | ok |
| okx_BTC-USD-SWAP | 626/626 | ok |
| okx_BTC-USDT-SWAP | 626/626 | ok |
| paradex | 626/626 | ok |
| premium_parts | 626/626 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-30 00:00Z | 292 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-30 00:00Z | 292 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-30 06:00Z | 924 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-30 06:35Z | 11088 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-30 06:00Z | 924 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-30 06:35Z | 11088 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-30 05:00Z | 924 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-30 06:35Z | 11088 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-30 06:00Z | 924 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-30 06:35Z | 11088 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-30 06:00Z | 924 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-30 06:35Z | 11087 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-30 05:00Z | 3060 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-30 05:00Z | 899 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-30 00:00Z | 300 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-30 05:00Z | 3059 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-30 05:00Z | 3059 | 0 | 0 |

## 3. Forced-flow retention and revision
13486 distinct liquidation observations; 12 retained boundary probes.
- 2026-09-26 00:20Z: 0.98 days, 17 pages (observed source boundary).
- 2026-09-27 00:22Z: 1.0 days, 4 pages (observed source boundary).
- 2026-09-28 00:24Z: 0.94 days, 10 pages (observed source boundary).
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
- 2026-09-30 00:23Z: 0.98 days, 13 pages (observed source boundary).
Observed later revision after first live capture: n=32 active hours; mean 5.7%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 626 stored snapshots in 168 distinct hours from 2026-09-23 07:22Z to 2026-09-30 06:41Z; latest 789 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 626 stored snapshots in 168 distinct hours from 2026-09-23 07:22Z to 2026-09-30 06:41Z; latest 20 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10066 bars 2026-09-23 06:55Z → 2026-09-30 06:40Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10066 bars 2026-09-23 06:55Z → 2026-09-30 06:40Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10066 bars 2026-09-23 06:55Z → 2026-09-30 06:40Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10066 bars 2026-09-23 06:55Z → 2026-09-30 06:40Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10066 bars 2026-09-23 06:55Z → 2026-09-30 06:40Z; 0 missing minutes inside the span.
- Deribit options schema 2: 600 runs; latest 789 with OI, 157 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 155.
- Hyperliquid sample v2: 600 snapshots; account checks by state ok_btc 13210, ok_flat 88642, ok_other 12148; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 218, ledger ok 818, twap not_attempted 2, twap ok 4962.
- OKX insurance fund rows: regular_update 600.
- Research lab: 32 runs in window; latest 2026-09-30 06:53Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 6/626 routine run(s), 2026-09-25 23:41Z → 2026-09-29 19:44Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
