# JBM desk report — 2026-11-24 00:24Z
Window 2026-11-17 00:24Z → 2026-11-24 00:24Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-24 00:24Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-24 00:15Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-24 00:18Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-24 00:15Z | 9 min |
| snapshots | 2026-11-24 00:14Z | 10 min |
| 1-minute prices (BTC perp) | 2026-11-24 00:15Z | 9 min |
| Deribit options | 2026-11-24 00:14Z | 9 min |
| Hyperliquid account sample | 2026-11-24 00:15Z | 9 min |
| Hyperliquid enrichment | 2026-11-24 00:15Z | 9 min |
| OKX insurance fund | 2026-11-24 00:15Z | 9 min |
| OKX liquidation orders | 2026-11-24 00:14Z | 10 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-24 00:18Z | 6 min |

## 1. Collection health
683 routine runs in window, by trigger: schedule 23, workflow_dispatch 660.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-11-17 00:24Z → 2026-11-24 00:24Z | `7,22,37,52 * * * *` | 670 | 23 (3%) | 670/670 slot intervals; 1 not yet assessed (after the input cutoff) | 9/683 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-24 00:13Z; report clock 2026-11-24 00:24Z: wall-clock lag 11 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 432.1, p90 533.1, max 723.6.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.3, max 22.7.
Runtime per routine run (s): median 108, p90 127, max 286; 0 run(s) reached the network budget.
Rate-limit incidents: www.deribit.com 1395, api.hyperliquid.xyz 11 across 683 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 4.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 683/683 | ok |
| binance_BTCUSDC | 683/683 | ok |
| binance_BTCUSDT | 683/683 | ok |
| binance_BTCUSD_PERP | 683/683 | ok |
| binance_coinm_prem | 683/683 | ok |
| binance_usdc_prem | 683/683 | ok |
| binance_usdt_prem | 683/683 | ok |
| bingx | 683/683 | ok |
| bitfinex_margin | 683/683 | ok |
| bitget_USDC | 683/683 | ok |
| bitget_USDT | 683/683 | ok |
| cross_binance_ETHUSDT | 683/683 | ok |
| cross_binance_SOLUSDT | 683/683 | ok |
| cross_hl_ETH | 683/683 | ok |
| cross_hl_SOL | 683/683 | ok |
| depth_binance_usdt | 683/683 | ok |
| depth_okx_usdt_swap | 683/683 | ok |
| deribit | 675/683 | ok |
| dydx | 683/683 | ok |
| gate | 683/683 | ok |
| hl_predicted_fundings | 683/683 | ok |
| htx | 682/683 | ok |
| hyperliquid | 683/683 | ok |
| kraken | 683/683 | ok |
| kucoin | 683/683 | ok |
| okx_BTC-USD-SWAP | 683/683 | ok |
| okx_BTC-USDT-SWAP | 683/683 | ok |
| paradex | 683/683 | ok |
| premium_parts | 683/683 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-24 00:00Z | 457 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-24 00:00Z | 457 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-24 00:00Z | 2238 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-24 00:05Z | 26850 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-24 00:00Z | 2236 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-24 00:05Z | 26834 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-23 23:00Z | 2238 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-24 00:05Z | 26850 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-24 00:00Z | 2238 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-24 00:05Z | 26850 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-24 00:00Z | 2238 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-24 00:05Z | 26849 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-20 18:00Z | 4297 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-23 23:00Z | 2213 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-24 00:00Z | 465 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-23 23:00Z | 4373 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-23 23:00Z | 4373 | 0 | 0 |

## 3. Forced-flow retention and revision
147893 distinct liquidation observations; 67 retained boundary probes.
- 2026-11-20 00:13Z: 1.0 days, 35 pages (observed source boundary).
- 2026-11-21 00:13Z: 1.0 days, 79 pages (observed source boundary).
- 2026-11-22 00:13Z: 0.96 days, 73 pages (observed source boundary).
- 2026-11-23 00:13Z: 0.98 days, 36 pages (observed source boundary).
- 2026-11-24 00:13Z: 0.99 days, 60 pages (observed source boundary).
Observed later revision after first live capture: n=60 active hours; mean 6.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 679 stored snapshots in 168 distinct hours from 2026-11-17 00:28Z to 2026-11-24 00:13Z; latest 842 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 683 stored snapshots in 169 distinct hours from 2026-11-17 00:28Z to 2026-11-24 00:13Z; latest 17 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10068 bars 2026-11-17 00:25Z → 2026-11-24 00:12Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10068 bars 2026-11-17 00:25Z → 2026-11-24 00:12Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10068 bars 2026-11-17 00:25Z → 2026-11-24 00:12Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10068 bars 2026-11-17 00:25Z → 2026-11-24 00:12Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10068 bars 2026-11-17 00:25Z → 2026-11-24 00:12Z; 0 missing minutes inside the span.
- Deribit options schema 2: 679 runs; latest 842 with OI, 130 zero OI, 0 absent, 0 past expiry; panel 8/12 tickers; 4 failed or out of time; metadata refreshed.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 683 snapshots; account checks by state failed 3, ok_btc 14449, ok_flat 104039, ok_other 11279; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 310, ledger ok 993, twap not_attempted 4, twap ok 5523.
- OKX insurance fund rows: regular_update 683.
- Research lab: 14 runs in window; latest 2026-11-24 00:18Z: exploratory 1, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-11-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-11-23 19:08Z, over 90 minutes before this report.
- history deribit_dvol_1h: 311/683 routine run(s), 2026-11-20 20:13Z → 2026-11-24 00:13Z; latest: DVOL: incomplete DVOL day; checkpoint retained
- rate limit www.deribit.com: 307/683 routine run(s), 2026-11-20 21:13Z → 2026-11-24 00:13Z; latest: 4 rate-limited response(s)
- snapshot deribit: 8/683 routine run(s), 2026-11-20 19:28Z → 2026-11-20 21:13Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 4/683 routine run(s), 2026-11-20 20:13Z → 2026-11-20 20:58Z; latest: RuntimeError: HTTP 503; absent from the latest run
- snapshot htx: 1/683 routine run(s), 2026-11-18 04:13Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- forward book hl_positions: 1/683 routine run(s), 2026-11-17 02:43Z; latest: degraded: 3/190 accounts failed, malformed or not attempted; absent from the latest run
- rate limit api.hyperliquid.xyz: 1/683 routine run(s), 2026-11-17 02:43Z; latest: 11 rate-limited response(s); absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
- deribit_dvol_1h: stale; last observation 2026-11-20 18:00Z
