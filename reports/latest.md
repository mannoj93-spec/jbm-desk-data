# JBM desk report — 2026-10-26 05:37Z
Window 2026-10-19 05:37Z → 2026-10-26 05:37Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-26 05:37Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-26 04:54Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-26 05:14Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-26 04:54Z | 43 min |
| snapshots | 2026-10-26 04:53Z | 44 min |
| 1-minute prices (BTC perp) | 2026-10-26 04:54Z | 44 min |
| Deribit options | 2026-10-26 04:53Z | 44 min |
| Hyperliquid account sample | 2026-10-26 04:54Z | 44 min |
| Hyperliquid enrichment | 2026-10-26 04:54Z | 44 min |
| OKX insurance fund | 2026-10-26 04:54Z | 43 min |
| OKX liquidation orders | 2026-10-26 04:53Z | 44 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-26 05:14Z | 24 min |

## 1. Collection health
795 routine runs in window, by trigger: schedule 179, workflow_dispatch 616.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-19 05:37Z → 2026-10-26 05:37Z | `7,22,37,52 * * * *` | 670 | 179 (27%) | 663/668 slot intervals; 3 not yet assessed (after the input cutoff) | 1/795 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-26 04:52Z; report clock 2026-10-26 05:37Z: wall-clock lag 45 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 33.1, p90 137.2, max 327.7.
Actual interval between stored snapshots, all triggers (min): median 14.9, p90 15.1, max 30.1.
Runtime per routine run (s): median 106, p90 114, max 170; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 795 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 795/795 | ok |
| binance_BTCUSDC | 795/795 | ok |
| binance_BTCUSDT | 795/795 | ok |
| binance_BTCUSD_PERP | 795/795 | ok |
| binance_coinm_prem | 795/795 | ok |
| binance_usdc_prem | 795/795 | ok |
| binance_usdt_prem | 795/795 | ok |
| bingx | 795/795 | ok |
| bitfinex_margin | 795/795 | ok |
| bitget_USDC | 795/795 | ok |
| bitget_USDT | 795/795 | ok |
| cross_binance_ETHUSDT | 795/795 | ok |
| cross_binance_SOLUSDT | 795/795 | ok |
| cross_hl_ETH | 795/795 | ok |
| cross_hl_SOL | 795/795 | ok |
| depth_binance_usdt | 795/795 | ok |
| depth_okx_usdt_swap | 795/795 | ok |
| deribit | 795/795 | ok |
| dydx | 795/795 | ok |
| gate | 795/795 | ok |
| hl_predicted_fundings | 795/795 | ok |
| htx | 794/795 | ok |
| hyperliquid | 795/795 | ok |
| kraken | 795/795 | ok |
| kucoin | 795/795 | ok |
| okx_BTC-USD-SWAP | 795/795 | ok |
| okx_BTC-USDT-SWAP | 795/795 | ok |
| paradex | 795/795 | ok |
| premium_parts | 795/795 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-26 00:00Z | 370 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-26 00:00Z | 370 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-26 04:00Z | 1546 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-26 04:45Z | 18554 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-26 04:00Z | 1544 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-26 04:45Z | 18538 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-26 03:00Z | 1546 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-26 04:45Z | 18554 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-26 04:00Z | 1546 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-26 04:45Z | 18554 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-26 04:00Z | 1546 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-26 04:45Z | 18553 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-26 03:00Z | 3682 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-26 03:00Z | 1521 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-26 00:00Z | 378 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-26 03:00Z | 3681 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-26 03:00Z | 3681 | 0 | 0 |

## 3. Forced-flow retention and revision
54180 distinct liquidation observations; 38 retained boundary probes.
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
- 2026-10-25 00:09Z: 1.0 days, 18 pages (observed source boundary).
- 2026-10-26 00:08Z: 0.96 days, 9 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 8.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 795 stored snapshots in 168 distinct hours from 2026-10-19 05:42Z to 2026-10-26 04:52Z; latest 758 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 795 stored snapshots in 168 distinct hours from 2026-10-19 05:42Z to 2026-10-26 04:52Z; latest 27 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10034 bars 2026-10-19 05:38Z → 2026-10-26 04:51Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10034 bars 2026-10-19 05:38Z → 2026-10-26 04:51Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10034 bars 2026-10-19 05:38Z → 2026-10-26 04:51Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10034 bars 2026-10-19 05:38Z → 2026-10-26 04:51Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10034 bars 2026-10-19 05:38Z → 2026-10-26 04:51Z; 0 missing minutes inside the span.
- Deribit options schema 2: 795 runs; latest 758 with OI, 162 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 795 snapshots; account checks by state ok_btc 17035, ok_flat 117974, ok_other 16041; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 269, ledger ok 1064, twap ok 6617.
- OKX insurance fund rows: regular_update 795.
- Research lab: 28 runs in window; latest 2026-10-26 05:14Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-26.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.96 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 1/795 routine run(s), 2026-10-26 04:28Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
