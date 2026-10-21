# JBM desk report — 2026-10-21 13:41Z
Window 2026-10-14 13:41Z → 2026-10-21 13:41Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-21 13:41Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-21 13:14Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-21 13:20Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-21 13:14Z | 26 min |
| snapshots | 2026-10-21 13:13Z | 27 min |
| 1-minute prices (BTC perp) | 2026-10-21 13:14Z | 26 min |
| Deribit options | 2026-10-21 13:13Z | 27 min |
| Hyperliquid account sample | 2026-10-21 13:14Z | 26 min |
| Hyperliquid enrichment | 2026-10-21 13:14Z | 26 min |
| OKX insurance fund | 2026-10-21 13:14Z | 26 min |
| OKX liquidation orders | 2026-10-21 13:13Z | 27 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-21 13:20Z | 21 min |

## 1. Collection health
873 routine runs in window, by trigger: schedule 327, workflow_dispatch 546.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-14 13:41Z → 2026-10-21 13:41Z | `7,22,37,52 * * * *` | 670 | 327 (49%) | 666/669 slot intervals; 2 not yet assessed (after the input cutoff) | 6/873 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-21 13:13Z; report clock 2026-10-21 13:41Z: wall-clock lag 28 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 30.0, p90 39.0, max 74.9.
Actual interval between stored snapshots, all triggers (min): median 12.3, p90 16.6, max 30.0.
Runtime per routine run (s): median 105, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 873 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 873/873 | ok |
| binance_BTCUSDC | 873/873 | ok |
| binance_BTCUSDT | 873/873 | ok |
| binance_BTCUSD_PERP | 873/873 | ok |
| binance_coinm_prem | 873/873 | ok |
| binance_usdc_prem | 873/873 | ok |
| binance_usdt_prem | 873/873 | ok |
| bingx | 873/873 | ok |
| bitfinex_margin | 873/873 | ok |
| bitget_USDC | 873/873 | ok |
| bitget_USDT | 873/873 | ok |
| cross_binance_ETHUSDT | 873/873 | ok |
| cross_binance_SOLUSDT | 873/873 | ok |
| cross_hl_ETH | 873/873 | ok |
| cross_hl_SOL | 873/873 | ok |
| depth_binance_usdt | 873/873 | ok |
| depth_okx_usdt_swap | 873/873 | ok |
| deribit | 873/873 | ok |
| dydx | 873/873 | ok |
| gate | 873/873 | ok |
| hl_predicted_fundings | 873/873 | ok |
| htx | 871/873 | ok |
| hyperliquid | 873/873 | ok |
| kraken | 869/873 | ok |
| kucoin | 873/873 | ok |
| okx_BTC-USD-SWAP | 873/873 | ok |
| okx_BTC-USDT-SWAP | 873/873 | ok |
| paradex | 873/873 | ok |
| premium_parts | 873/873 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-21 08:00Z | 356 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-21 08:00Z | 356 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-21 13:00Z | 1435 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-21 13:05Z | 17214 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-21 13:00Z | 1433 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-21 13:05Z | 17198 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-21 12:00Z | 1435 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-21 13:05Z | 17214 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-21 13:00Z | 1435 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-21 13:05Z | 17214 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-21 13:00Z | 1435 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-21 13:05Z | 17213 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-21 12:00Z | 3571 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-21 12:00Z | 1410 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-21 08:00Z | 364 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-21 12:00Z | 3570 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-21 12:00Z | 3570 | 0 | 0 |

## 3. Forced-flow retention and revision
46384 distinct liquidation observations; 33 retained boundary probes.
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
Observed later revision after first live capture: n=25 active hours; mean 6.6%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 873 stored snapshots in 169 distinct hours from 2026-10-14 13:42Z to 2026-10-21 13:13Z; latest 728 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 873 stored snapshots in 169 distinct hours from 2026-10-14 13:42Z to 2026-10-21 13:13Z; latest 22 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10051 bars 2026-10-14 13:42Z → 2026-10-21 13:12Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10051 bars 2026-10-14 13:42Z → 2026-10-21 13:12Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10051 bars 2026-10-14 13:42Z → 2026-10-21 13:12Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10051 bars 2026-10-14 13:42Z → 2026-10-21 13:12Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10051 bars 2026-10-14 13:42Z → 2026-10-21 13:12Z; 0 missing minutes inside the span.
- Deribit options schema 2: 873 runs; latest 728 with OI, 160 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 873 snapshots; account checks by state ok_btc 18996, ok_flat 129230, ok_other 17644; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 263, ledger ok 1136, twap not_attempted 2, twap ok 7329.
- OKX insurance fund rows: regular_update 873.
- Research lab: 28 runs in window; latest 2026-10-21 13:20Z: exploratory 3, not run 2, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 2/873 routine run(s), 2026-10-15 01:45Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/873 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/873 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/873 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/873 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 4/873 routine run(s), 2026-10-15 07:01Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
