# JBM desk report — 2026-10-01 06:56Z
Window 2026-09-24 06:56Z → 2026-10-01 06:56Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-01 06:56Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-01 06:53Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-10-01 06:55Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-01 06:53Z | 3 min |
| snapshots | 2026-10-01 06:52Z | 4 min |
| 1-minute prices (BTC perp) | 2026-10-01 06:53Z | 3 min |
| Deribit options | 2026-10-01 06:52Z | 4 min |
| Hyperliquid account sample | 2026-10-01 06:53Z | 3 min |
| Hyperliquid enrichment | 2026-10-01 06:53Z | 3 min |
| OKX insurance fund | 2026-10-01 06:53Z | 3 min |
| OKX liquidation orders | 2026-10-01 06:23Z | 33 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-01 06:55Z | 1 min |

## 1. Collection health
649 routine runs in window, by trigger: schedule 649.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-24 06:56Z → 2026-10-01 06:56Z | `7,22,37,52 * * * *` | 670 | 649 (97%) | 647/671 slot intervals | 6/649 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.2, p90 20.9, max 30.5.
Actual interval between stored snapshots, all triggers (min): median 14.2, p90 20.9, max 30.5.
Runtime per routine run (s): median 105, p90 113, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 649 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 649/649 | ok |
| binance_BTCUSDC | 649/649 | ok |
| binance_BTCUSDT | 649/649 | ok |
| binance_BTCUSD_PERP | 649/649 | ok |
| binance_coinm_prem | 649/649 | ok |
| binance_usdc_prem | 649/649 | ok |
| binance_usdt_prem | 649/649 | ok |
| bingx | 649/649 | ok |
| bitfinex_margin | 649/649 | ok |
| bitget_USDC | 649/649 | ok |
| bitget_USDT | 649/649 | ok |
| cross_binance_ETHUSDT | 649/649 | ok |
| cross_binance_SOLUSDT | 649/649 | ok |
| cross_hl_ETH | 649/649 | ok |
| cross_hl_SOL | 649/649 | ok |
| depth_binance_usdt | 649/649 | ok |
| depth_okx_usdt_swap | 649/649 | ok |
| deribit | 649/649 | ok |
| dydx | 649/649 | ok |
| gate | 649/649 | ok |
| hl_predicted_fundings | 649/649 | ok |
| htx | 643/649 | ok |
| hyperliquid | 649/649 | ok |
| kraken | 649/649 | ok |
| kucoin | 649/649 | ok |
| okx_BTC-USD-SWAP | 649/649 | ok |
| okx_BTC-USDT-SWAP | 649/649 | ok |
| paradex | 649/649 | ok |
| premium_parts | 649/649 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-01 00:00Z | 295 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-01 00:00Z | 295 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-01 06:00Z | 948 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-01 06:45Z | 11378 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-01 06:00Z | 948 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-01 06:45Z | 11378 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-01 05:00Z | 948 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-01 06:45Z | 11378 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-01 06:00Z | 948 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-01 06:45Z | 11378 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-01 06:00Z | 948 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-01 06:45Z | 11377 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-01 05:00Z | 3084 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-01 05:00Z | 923 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-01 00:00Z | 303 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-01 05:00Z | 3083 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-01 05:00Z | 3083 | 0 | 0 |

## 3. Forced-flow retention and revision
15554 distinct liquidation observations; 13 retained boundary probes.
- 2026-09-27 00:22Z: 1.0 days, 4 pages (observed source boundary).
- 2026-09-28 00:24Z: 0.94 days, 10 pages (observed source boundary).
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
- 2026-09-30 00:23Z: 0.98 days, 13 pages (observed source boundary).
- 2026-10-01 00:25Z: 0.98 days, 22 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 5.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 649 stored snapshots in 169 distinct hours from 2026-09-24 06:58Z to 2026-10-01 06:51Z; latest 797 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 649 stored snapshots in 169 distinct hours from 2026-09-24 06:58Z to 2026-10-01 06:51Z; latest 19 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10074 bars 2026-09-24 06:57Z → 2026-10-01 06:50Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10074 bars 2026-09-24 06:57Z → 2026-10-01 06:50Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10074 bars 2026-09-24 06:57Z → 2026-10-01 06:50Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10074 bars 2026-09-24 06:57Z → 2026-10-01 06:50Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10074 bars 2026-09-24 06:57Z → 2026-10-01 06:50Z; 0 missing minutes inside the span.
- Deribit options schema 2: 649 runs; latest 797 with OI, 151 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 649 snapshots; account checks by state ok_btc 14272, ok_flat 95894, ok_other 13144; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 239, ledger ok 888, twap not_attempted 5, twap ok 5358.
- OKX insurance fund rows: regular_update 649.
- Research lab: 32 runs in window; latest 2026-10-01 06:55Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 6/649 routine run(s), 2026-09-25 23:41Z → 2026-09-29 19:44Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
