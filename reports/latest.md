# JBM desk report — 2026-10-22 19:34Z
Window 2026-10-15 19:34Z → 2026-10-22 19:34Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-22 19:34Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-22 18:58Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-22 19:14Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-22 18:58Z | 36 min |
| snapshots | 2026-10-22 18:57Z | 37 min |
| 1-minute prices (BTC perp) | 2026-10-22 18:58Z | 36 min |
| Deribit options | 2026-10-22 18:57Z | 37 min |
| Hyperliquid account sample | 2026-10-22 18:58Z | 36 min |
| Hyperliquid enrichment | 2026-10-22 18:58Z | 36 min |
| OKX insurance fund | 2026-10-22 18:58Z | 36 min |
| OKX liquidation orders | 2026-10-22 18:43Z | 51 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-22 19:14Z | 20 min |

## 1. Collection health
874 routine runs in window, by trigger: schedule 326, workflow_dispatch 548.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-15 19:34Z → 2026-10-22 19:34Z | `7,22,37,52 * * * *` | 671 | 326 (49%) | 666/669 slot intervals; 2 not yet assessed (after the input cutoff) | 1/874 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-22 18:56Z; report clock 2026-10-22 19:34Z: wall-clock lag 38 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 30.2, p90 39.3, max 74.9.
Actual interval between stored snapshots, all triggers (min): median 12.3, p90 16.6, max 30.0.
Runtime per routine run (s): median 105, p90 114, max 147; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 874 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 874/874 | ok |
| binance_BTCUSDC | 874/874 | ok |
| binance_BTCUSDT | 874/874 | ok |
| binance_BTCUSD_PERP | 874/874 | ok |
| binance_coinm_prem | 874/874 | ok |
| binance_usdc_prem | 874/874 | ok |
| binance_usdt_prem | 874/874 | ok |
| bingx | 874/874 | ok |
| bitfinex_margin | 874/874 | ok |
| bitget_USDC | 874/874 | ok |
| bitget_USDT | 874/874 | ok |
| cross_binance_ETHUSDT | 874/874 | ok |
| cross_binance_SOLUSDT | 874/874 | ok |
| cross_hl_ETH | 874/874 | ok |
| cross_hl_SOL | 874/874 | ok |
| depth_binance_usdt | 874/874 | ok |
| depth_okx_usdt_swap | 874/874 | ok |
| deribit | 874/874 | ok |
| dydx | 874/874 | ok |
| gate | 874/874 | ok |
| hl_predicted_fundings | 874/874 | ok |
| htx | 873/874 | ok |
| hyperliquid | 874/874 | ok |
| kraken | 874/874 | ok |
| kucoin | 874/874 | ok |
| okx_BTC-USD-SWAP | 874/874 | ok |
| okx_BTC-USDT-SWAP | 874/874 | ok |
| paradex | 874/874 | ok |
| premium_parts | 874/874 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-22 16:00Z | 360 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-22 16:00Z | 360 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-22 18:00Z | 1464 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-22 18:50Z | 17571 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-22 18:00Z | 1462 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-22 18:50Z | 17555 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-22 17:00Z | 1464 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-22 18:50Z | 17571 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-22 18:00Z | 1464 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-22 18:50Z | 17571 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-22 18:00Z | 1464 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-22 18:50Z | 17570 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-22 17:00Z | 3600 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-22 17:00Z | 1439 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-22 16:00Z | 368 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-22 17:00Z | 3599 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-22 17:00Z | 3599 | 0 | 0 |

## 3. Forced-flow retention and revision
49506 distinct liquidation observations; 34 retained boundary probes.
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
Observed later revision after first live capture: n=21 active hours; mean 6.7%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 874 stored snapshots in 168 distinct hours from 2026-10-15 19:42Z to 2026-10-22 18:56Z; latest 779 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 874 stored snapshots in 168 distinct hours from 2026-10-15 19:42Z to 2026-10-22 18:56Z; latest 16 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10041 bars 2026-10-15 19:35Z → 2026-10-22 18:55Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10041 bars 2026-10-15 19:35Z → 2026-10-22 18:55Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10041 bars 2026-10-15 19:35Z → 2026-10-22 18:55Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10041 bars 2026-10-15 19:35Z → 2026-10-22 18:55Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10041 bars 2026-10-15 19:35Z → 2026-10-22 18:55Z; 0 missing minutes inside the span.
- Deribit options schema 2: 874 runs; latest 779 with OI, 155 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 874 snapshots; account checks by state ok_btc 18904, ok_flat 129426, ok_other 17730; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 279, ledger ok 1153, twap not_attempted 2, twap ok 7306.
- OKX insurance fund rows: regular_update 874.
- Research lab: 28 runs in window; latest 2026-10-22 19:14Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 1/874 routine run(s), 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
