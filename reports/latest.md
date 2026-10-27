# JBM desk report — 2026-10-27 22:55Z
Window 2026-10-20 22:55Z → 2026-10-27 22:55Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-27 22:55Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-27 22:30Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-27 22:35Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-27 22:30Z | 25 min |
| snapshots | 2026-10-27 22:29Z | 26 min |
| 1-minute prices (BTC perp) | 2026-10-27 22:30Z | 25 min |
| Deribit options | 2026-10-27 22:29Z | 26 min |
| Hyperliquid account sample | 2026-10-27 22:30Z | 26 min |
| Hyperliquid enrichment | 2026-10-27 22:30Z | 26 min |
| OKX insurance fund | 2026-10-27 22:30Z | 25 min |
| OKX liquidation orders | 2026-10-27 21:43Z | 72 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-27 22:35Z | 20 min |

## 1. Collection health
746 routine runs in window, by trigger: schedule 114, workflow_dispatch 632.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-20 22:55Z → 2026-10-27 22:55Z | `7,22,37,52 * * * *` | 670 | 114 (17%) | 663/669 slot intervals; 2 not yet assessed (after the input cutoff) | 2/746 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-27 22:28Z; report clock 2026-10-27 22:55Z: wall-clock lag 27 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 35.0, p90 279.7, max 381.6.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.1, max 30.1.
Runtime per routine run (s): median 106, p90 114, max 170; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 746 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 746/746 | ok |
| binance_BTCUSDC | 746/746 | ok |
| binance_BTCUSDT | 746/746 | ok |
| binance_BTCUSD_PERP | 746/746 | ok |
| binance_coinm_prem | 746/746 | ok |
| binance_usdc_prem | 746/746 | ok |
| binance_usdt_prem | 746/746 | ok |
| bingx | 746/746 | ok |
| bitfinex_margin | 746/746 | ok |
| bitget_USDC | 745/746 | ok |
| bitget_USDT | 745/746 | ok |
| cross_binance_ETHUSDT | 746/746 | ok |
| cross_binance_SOLUSDT | 746/746 | ok |
| cross_hl_ETH | 746/746 | ok |
| cross_hl_SOL | 746/746 | ok |
| depth_binance_usdt | 746/746 | ok |
| depth_okx_usdt_swap | 746/746 | ok |
| deribit | 746/746 | ok |
| dydx | 746/746 | ok |
| gate | 746/746 | ok |
| hl_predicted_fundings | 746/746 | ok |
| htx | 745/746 | ok |
| hyperliquid | 746/746 | ok |
| kraken | 746/746 | ok |
| kucoin | 746/746 | ok |
| okx_BTC-USD-SWAP | 746/746 | ok |
| okx_BTC-USDT-SWAP | 746/746 | ok |
| paradex | 746/746 | ok |
| premium_parts | 746/746 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-27 16:00Z | 375 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-27 16:00Z | 375 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-27 22:00Z | 1588 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-27 22:20Z | 19053 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-27 22:00Z | 1586 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-27 22:20Z | 19037 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-27 21:00Z | 1588 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-27 22:20Z | 19053 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-27 22:00Z | 1588 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-27 22:20Z | 19053 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-27 22:00Z | 1588 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-27 22:20Z | 19052 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-27 21:00Z | 3724 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-27 21:00Z | 1563 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-27 16:00Z | 383 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-27 21:00Z | 3723 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-27 21:00Z | 3723 | 0 | 0 |

## 3. Forced-flow retention and revision
55953 distinct liquidation observations; 39 retained boundary probes.
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
- 2026-10-25 00:09Z: 1.0 days, 18 pages (observed source boundary).
- 2026-10-26 00:08Z: 0.96 days, 9 pages (observed source boundary).
- 2026-10-27 00:13Z: 0.99 days, 17 pages (observed source boundary).
Observed later revision after first live capture: n=26 active hours; mean 8.2%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 746 stored snapshots in 169 distinct hours from 2026-10-20 22:57Z to 2026-10-27 22:28Z; latest 746 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 746 stored snapshots in 169 distinct hours from 2026-10-20 22:57Z to 2026-10-27 22:28Z; latest 19 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10052 bars 2026-10-20 22:56Z → 2026-10-27 22:27Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10052 bars 2026-10-20 22:56Z → 2026-10-27 22:27Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10052 bars 2026-10-20 22:56Z → 2026-10-27 22:27Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10052 bars 2026-10-20 22:56Z → 2026-10-27 22:27Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10052 bars 2026-10-20 22:56Z → 2026-10-27 22:27Z; 0 missing minutes inside the span.
- Deribit options schema 2: 746 runs; latest 746 with OI, 134 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 746 snapshots; account checks by state ok_btc 15916, ok_flat 110803, ok_other 15021; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 245, ledger ok 991, twap ok 6224.
- OKX insurance fund rows: regular_update 746.
- Research lab: 27 runs in window; latest 2026-10-27 22:35Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-26.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-10-27 20:46Z, over 90 minutes before this report.
- snapshot bitget_USDC: 1/746 routine run(s), 2026-10-27 08:28Z; latest: RuntimeError: circuit open: api.bitget.com failed earlier in this stage (TimeoutError: request; absent from the latest run
- snapshot bitget_USDT: 1/746 routine run(s), 2026-10-27 08:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot htx: 1/746 routine run(s), 2026-10-26 04:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
