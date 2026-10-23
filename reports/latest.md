# JBM desk report — 2026-10-23 21:49Z
Window 2026-10-16 21:49Z → 2026-10-23 21:49Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-23 21:49Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-23 21:29Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-23 21:37Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-23 21:29Z | 20 min |
| snapshots | 2026-10-23 21:28Z | 21 min |
| 1-minute prices (BTC perp) | 2026-10-23 21:29Z | 20 min |
| Deribit options | 2026-10-23 21:28Z | 21 min |
| Hyperliquid account sample | 2026-10-23 21:29Z | 20 min |
| Hyperliquid enrichment | 2026-10-23 21:29Z | 20 min |
| OKX insurance fund | 2026-10-23 21:29Z | 20 min |
| OKX liquidation orders | 2026-10-23 20:58Z | 51 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-23 21:37Z | 12 min |

## 1. Collection health
849 routine runs in window, by trigger: schedule 285, workflow_dispatch 564.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-16 21:49Z → 2026-10-23 21:49Z | `7,22,37,52 * * * *` | 671 | 285 (42%) | 666/670 slot intervals; 1 not yet assessed (after the input cutoff) | 1/849 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-23 21:28Z; report clock 2026-10-23 21:49Z: wall-clock lag 21 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 30.5, p90 40.6, max 327.7.
Actual interval between stored snapshots, all triggers (min): median 13.0, p90 16.1, max 30.1.
Runtime per routine run (s): median 105, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 849 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 849/849 | ok |
| binance_BTCUSDC | 849/849 | ok |
| binance_BTCUSDT | 849/849 | ok |
| binance_BTCUSD_PERP | 849/849 | ok |
| binance_coinm_prem | 849/849 | ok |
| binance_usdc_prem | 849/849 | ok |
| binance_usdt_prem | 849/849 | ok |
| bingx | 849/849 | ok |
| bitfinex_margin | 849/849 | ok |
| bitget_USDC | 849/849 | ok |
| bitget_USDT | 849/849 | ok |
| cross_binance_ETHUSDT | 849/849 | ok |
| cross_binance_SOLUSDT | 849/849 | ok |
| cross_hl_ETH | 849/849 | ok |
| cross_hl_SOL | 849/849 | ok |
| depth_binance_usdt | 849/849 | ok |
| depth_okx_usdt_swap | 849/849 | ok |
| deribit | 849/849 | ok |
| dydx | 849/849 | ok |
| gate | 849/849 | ok |
| hl_predicted_fundings | 849/849 | ok |
| htx | 848/849 | ok |
| hyperliquid | 849/849 | ok |
| kraken | 849/849 | ok |
| kucoin | 849/849 | ok |
| okx_BTC-USD-SWAP | 849/849 | ok |
| okx_BTC-USDT-SWAP | 849/849 | ok |
| paradex | 849/849 | ok |
| premium_parts | 849/849 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-23 16:00Z | 363 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-23 16:00Z | 363 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-23 21:00Z | 1491 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-23 21:20Z | 17889 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-23 21:00Z | 1489 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-23 21:20Z | 17873 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-23 20:00Z | 1491 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-23 21:20Z | 17889 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-23 21:00Z | 1491 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-23 21:20Z | 17889 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-23 21:00Z | 1491 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-23 21:20Z | 17888 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-23 20:00Z | 3627 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-23 20:00Z | 1466 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-23 16:00Z | 371 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-23 20:00Z | 3626 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-23 20:00Z | 3626 | 0 | 0 |

## 3. Forced-flow retention and revision
50573 distinct liquidation observations; 35 retained boundary probes.
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
Observed later revision after first live capture: n=24 active hours; mean 7.6%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 849 stored snapshots in 169 distinct hours from 2026-10-16 21:57Z to 2026-10-23 21:28Z; latest 762 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 849 stored snapshots in 169 distinct hours from 2026-10-16 21:57Z to 2026-10-23 21:28Z; latest 22 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10058 bars 2026-10-16 21:50Z → 2026-10-23 21:27Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10058 bars 2026-10-16 21:50Z → 2026-10-23 21:27Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10058 bars 2026-10-16 21:50Z → 2026-10-23 21:27Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10058 bars 2026-10-16 21:50Z → 2026-10-23 21:27Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10058 bars 2026-10-16 21:50Z → 2026-10-23 21:27Z; 0 missing minutes inside the span.
- Deribit options schema 2: 849 runs; latest 762 with OI, 168 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 849 snapshots; account checks by state ok_btc 18313, ok_flat 125825, ok_other 17172; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 268, ledger ok 1117, twap ok 7105.
- OKX insurance fund rows: regular_update 849.
- Research lab: 28 runs in window; latest 2026-10-23 21:37Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.97 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-10-23 20:07Z, over 90 minutes before this report.
- snapshot htx: 1/849 routine run(s), 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
