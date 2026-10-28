# JBM desk report — 2026-10-28 06:38Z
Window 2026-10-21 06:38Z → 2026-10-28 06:38Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-28 06:38Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-28 05:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-28 06:13Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-28 05:59Z | 39 min |
| snapshots | 2026-10-28 05:58Z | 40 min |
| 1-minute prices (BTC perp) | 2026-10-28 05:59Z | 39 min |
| Deribit options | 2026-10-28 05:58Z | 40 min |
| Hyperliquid account sample | 2026-10-28 05:59Z | 39 min |
| Hyperliquid enrichment | 2026-10-28 05:59Z | 39 min |
| OKX insurance fund | 2026-10-28 05:59Z | 39 min |
| OKX liquidation orders | 2026-10-28 03:43Z | 175 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-28 06:13Z | 25 min |

## 1. Collection health
733 routine runs in window, by trigger: schedule 101, workflow_dispatch 632.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-21 06:38Z → 2026-10-28 06:38Z | `7,22,37,52 * * * *` | 670 | 101 (15%) | 662/668 slot intervals; 3 not yet assessed (after the input cutoff) | 2/733 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-28 05:58Z; report clock 2026-10-28 06:38Z: wall-clock lag 41 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 37.5, p90 284.6, max 381.6.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.1, max 30.1.
Runtime per routine run (s): median 107, p90 114, max 170; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 733 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 733/733 | ok |
| binance_BTCUSDC | 733/733 | ok |
| binance_BTCUSDT | 733/733 | ok |
| binance_BTCUSD_PERP | 733/733 | ok |
| binance_coinm_prem | 733/733 | ok |
| binance_usdc_prem | 733/733 | ok |
| binance_usdt_prem | 733/733 | ok |
| bingx | 733/733 | ok |
| bitfinex_margin | 733/733 | ok |
| bitget_USDC | 732/733 | ok |
| bitget_USDT | 732/733 | ok |
| cross_binance_ETHUSDT | 733/733 | ok |
| cross_binance_SOLUSDT | 733/733 | ok |
| cross_hl_ETH | 733/733 | ok |
| cross_hl_SOL | 733/733 | ok |
| depth_binance_usdt | 733/733 | ok |
| depth_okx_usdt_swap | 733/733 | ok |
| deribit | 733/733 | ok |
| dydx | 733/733 | ok |
| gate | 733/733 | ok |
| hl_predicted_fundings | 733/733 | ok |
| htx | 732/733 | ok |
| hyperliquid | 733/733 | ok |
| kraken | 733/733 | ok |
| kucoin | 733/733 | ok |
| okx_BTC-USD-SWAP | 733/733 | ok |
| okx_BTC-USDT-SWAP | 733/733 | ok |
| paradex | 733/733 | ok |
| premium_parts | 733/733 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-28 00:00Z | 376 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-28 00:00Z | 376 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-28 05:00Z | 1595 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-28 05:50Z | 19143 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-28 05:00Z | 1593 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-28 05:50Z | 19127 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-28 04:00Z | 1595 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-28 05:50Z | 19143 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-28 05:00Z | 1595 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-28 05:50Z | 19143 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-28 05:00Z | 1595 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-28 05:50Z | 19142 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-28 04:00Z | 3731 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-28 04:00Z | 1570 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-28 00:00Z | 384 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-28 04:00Z | 3730 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-28 04:00Z | 3730 | 0 | 0 |

## 3. Forced-flow retention and revision
56033 distinct liquidation observations; 40 retained boundary probes.
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
- 2026-10-25 00:09Z: 1.0 days, 18 pages (observed source boundary).
- 2026-10-26 00:08Z: 0.96 days, 9 pages (observed source boundary).
- 2026-10-27 00:13Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-28 00:04Z: 1.0 days, 10 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 733 stored snapshots in 168 distinct hours from 2026-10-21 06:42Z to 2026-10-28 05:58Z; latest 747 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 733 stored snapshots in 168 distinct hours from 2026-10-21 06:42Z to 2026-10-28 05:58Z; latest 22 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10039 bars 2026-10-21 06:39Z → 2026-10-28 05:57Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10039 bars 2026-10-21 06:39Z → 2026-10-28 05:57Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10039 bars 2026-10-21 06:39Z → 2026-10-28 05:57Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10039 bars 2026-10-21 06:39Z → 2026-10-28 05:57Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10039 bars 2026-10-21 06:39Z → 2026-10-28 05:57Z; 0 missing minutes inside the span.
- Deribit options schema 2: 733 runs; latest 747 with OI, 133 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 733 snapshots; account checks by state ok_btc 15638, ok_flat 108876, ok_other 14756; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 239, ledger ok 972, twap ok 6119.
- OKX insurance fund rows: regular_update 733.
- Research lab: 27 runs in window; latest 2026-10-28 06:13Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-26.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot bitget_USDC: 1/733 routine run(s), 2026-10-27 08:28Z; latest: RuntimeError: circuit open: api.bitget.com failed earlier in this stage (TimeoutError: request; absent from the latest run
- snapshot bitget_USDT: 1/733 routine run(s), 2026-10-27 08:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot htx: 1/733 routine run(s), 2026-10-26 04:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
