# JBM desk report — 2026-11-01 18:23Z
Window 2026-10-25 18:23Z → 2026-11-01 18:23Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-01 18:23Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-01 17:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-01 18:04Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-01 17:59Z | 24 min |
| snapshots | 2026-11-01 17:58Z | 24 min |
| 1-minute prices (BTC perp) | 2026-11-01 17:59Z | 24 min |
| Deribit options | 2026-11-01 17:58Z | 24 min |
| Hyperliquid account sample | 2026-11-01 17:59Z | 24 min |
| Hyperliquid enrichment | 2026-11-01 17:59Z | 24 min |
| OKX insurance fund | 2026-11-01 17:59Z | 24 min |
| OKX liquidation orders | 2026-11-01 12:28Z | 355 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-01 18:04Z | 19 min |

## 1. Collection health
682 routine runs in window, by trigger: schedule 35, workflow_dispatch 647.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-25 18:23Z → 2026-11-01 18:23Z | `7,22,37,52 * * * *` | 670 | 35 (5%) | 660/669 slot intervals; 2 not yet assessed (after the input cutoff) | 7/682 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-01 17:58Z; report clock 2026-11-01 18:23Z: wall-clock lag 25 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 296.9, p90 405.3, max 434.6.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.2, max 66.4.
Runtime per routine run (s): median 108, p90 117, max 170; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 682 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 682/682 | ok |
| binance_BTCUSDC | 682/682 | ok |
| binance_BTCUSDT | 682/682 | ok |
| binance_BTCUSD_PERP | 682/682 | ok |
| binance_coinm_prem | 682/682 | ok |
| binance_usdc_prem | 682/682 | ok |
| binance_usdt_prem | 682/682 | ok |
| bingx | 682/682 | ok |
| bitfinex_margin | 682/682 | ok |
| bitget_USDC | 681/682 | ok |
| bitget_USDT | 681/682 | ok |
| cross_binance_ETHUSDT | 682/682 | ok |
| cross_binance_SOLUSDT | 682/682 | ok |
| cross_hl_ETH | 682/682 | ok |
| cross_hl_SOL | 682/682 | ok |
| depth_binance_usdt | 682/682 | ok |
| depth_okx_usdt_swap | 682/682 | ok |
| deribit | 682/682 | ok |
| dydx | 681/682 | ok |
| gate | 682/682 | ok |
| hl_predicted_fundings | 682/682 | ok |
| htx | 681/682 | ok |
| hyperliquid | 682/682 | ok |
| kraken | 678/682 | ok |
| kucoin | 682/682 | ok |
| okx_BTC-USD-SWAP | 682/682 | ok |
| okx_BTC-USDT-SWAP | 682/682 | ok |
| paradex | 682/682 | ok |
| premium_parts | 681/682 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-01 16:00Z | 390 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-01 16:00Z | 390 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-01 17:00Z | 1703 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-01 17:50Z | 20439 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-01 17:00Z | 1701 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-01 17:50Z | 20423 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-01 16:00Z | 1703 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-01 17:50Z | 20439 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-01 17:00Z | 1703 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-01 17:50Z | 20439 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-01 17:00Z | 1703 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-01 17:50Z | 20438 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-01 16:00Z | 3839 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-01 16:00Z | 1678 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-01 16:00Z | 398 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-01 16:00Z | 3838 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-01 16:00Z | 3838 | 0 | 0 |

## 3. Forced-flow retention and revision
66082 distinct liquidation observations; 44 retained boundary probes.
- 2026-10-28 00:04Z: 1.0 days, 10 pages (observed source boundary).
- 2026-10-29 00:13Z: 0.99 days, 13 pages (observed source boundary).
- 2026-10-30 00:13Z: 0.98 days, 40 pages (observed source boundary).
- 2026-10-31 00:09Z: 1.0 days, 46 pages (observed source boundary).
- 2026-11-01 00:13Z: 1.0 days, 4 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 5.4%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 682 stored snapshots in 168 distinct hours from 2026-10-25 18:28Z to 2026-11-01 17:58Z; latest 762 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 682 stored snapshots in 168 distinct hours from 2026-10-25 18:28Z to 2026-11-01 17:58Z; latest 21 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10054 bars 2026-10-25 18:24Z → 2026-11-01 17:57Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10054 bars 2026-10-25 18:24Z → 2026-11-01 17:57Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10054 bars 2026-10-25 18:24Z → 2026-11-01 17:57Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10054 bars 2026-10-25 18:24Z → 2026-11-01 17:57Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10054 bars 2026-10-25 18:24Z → 2026-11-01 17:57Z; 0 missing minutes inside the span.
- Deribit options schema 2: 682 runs; latest 762 with OI, 194 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 682 snapshots; account checks by state ok_btc 14546, ok_flat 101631, ok_other 13403; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 218, ledger ok 900, twap ok 5702.
- OKX insurance fund rows: regular_update 682.
- Research lab: 22 runs in window; latest 2026-11-01 18:04Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-26.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-11-01 16:06Z, over 90 minutes before this report.
- snapshot premium_parts: 1/682 routine run(s), 2026-10-31 21:43Z; latest: RuntimeError: deadline reached; absent from the latest run
- snapshot kraken: 4/682 routine run(s), 2026-10-30 02:28Z → 2026-10-30 03:04Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot dydx: 1/682 routine run(s), 2026-10-29 09:13Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot bitget_USDC: 1/682 routine run(s), 2026-10-27 08:28Z; latest: RuntimeError: circuit open: api.bitget.com failed earlier in this stage (TimeoutError: request; absent from the latest run
- snapshot bitget_USDT: 1/682 routine run(s), 2026-10-27 08:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot htx: 1/682 routine run(s), 2026-10-26 04:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
