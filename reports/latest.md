# JBM desk report — 2026-11-03 20:25Z
Window 2026-10-27 20:25Z → 2026-11-03 20:25Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-03 20:25Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-03 19:33Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-03 19:47Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-03 19:33Z | 52 min |
| snapshots | 2026-11-03 19:32Z | 53 min |
| 1-minute prices (BTC perp) | 2026-11-03 19:33Z | 52 min |
| Deribit options | 2026-11-03 19:32Z | 53 min |
| Hyperliquid account sample | 2026-11-03 19:33Z | 52 min |
| Hyperliquid enrichment | 2026-11-03 19:33Z | 52 min |
| OKX insurance fund | 2026-11-03 19:33Z | 52 min |
| OKX liquidation orders | 2026-11-03 18:45Z | 101 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-03 19:47Z | 39 min |

## 1. Collection health
683 routine runs in window, by trigger: schedule 32, workflow_dispatch 651.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-27 20:25Z → 2026-11-03 20:25Z | `7,22,37,52 * * * *` | 670 | 32 (5%) | 662/667 slot intervals; 4 not yet assessed (after the input cutoff) | 5/683 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-03 19:31Z; report clock 2026-11-03 20:25Z: wall-clock lag 54 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 325.6, p90 435.3, max 606.0.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.2, max 66.4.
Runtime per routine run (s): median 107, p90 117, max 149; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 683 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

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
| deribit | 683/683 | ok |
| dydx | 682/683 | ok |
| gate | 683/683 | ok |
| hl_predicted_fundings | 683/683 | ok |
| htx | 683/683 | ok |
| hyperliquid | 683/683 | ok |
| kraken | 679/683 | ok |
| kucoin | 683/683 | ok |
| okx_BTC-USD-SWAP | 683/683 | ok |
| okx_BTC-USDT-SWAP | 683/683 | ok |
| paradex | 683/683 | ok |
| premium_parts | 682/683 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-03 16:00Z | 396 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-03 16:00Z | 396 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-03 19:00Z | 1753 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-03 19:25Z | 21034 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-03 19:00Z | 1751 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-03 19:25Z | 21018 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-03 18:00Z | 1753 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-03 19:25Z | 21034 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-03 19:00Z | 1753 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-03 19:25Z | 21034 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-03 19:00Z | 1753 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-03 19:25Z | 21033 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-03 18:00Z | 3889 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-03 18:00Z | 1728 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-03 16:00Z | 404 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-03 18:00Z | 3888 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-03 18:00Z | 3888 | 0 | 0 |

## 3. Forced-flow retention and revision
69295 distinct liquidation observations; 46 retained boundary probes.
- 2026-10-30 00:13Z: 0.98 days, 40 pages (observed source boundary).
- 2026-10-31 00:09Z: 1.0 days, 46 pages (observed source boundary).
- 2026-11-01 00:13Z: 1.0 days, 4 pages (observed source boundary).
- 2026-11-02 00:13Z: 0.94 days, 8 pages (observed source boundary).
- 2026-11-03 00:17Z: 1.0 days, 19 pages (observed source boundary).
Observed later revision after first live capture: n=26 active hours; mean 7.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 683 stored snapshots in 168 distinct hours from 2026-10-27 20:28Z to 2026-11-03 19:31Z; latest 742 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 683 stored snapshots in 168 distinct hours from 2026-10-27 20:28Z to 2026-11-03 19:31Z; latest 26 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10025 bars 2026-10-27 20:26Z → 2026-11-03 19:30Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10025 bars 2026-10-27 20:26Z → 2026-11-03 19:30Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10025 bars 2026-10-27 20:26Z → 2026-11-03 19:30Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10025 bars 2026-10-27 20:26Z → 2026-11-03 19:30Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10025 bars 2026-10-27 20:26Z → 2026-11-03 19:30Z; 0 missing minutes inside the span.
- Deribit options schema 2: 683 runs; latest 742 with OI, 158 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 683 snapshots; account checks by state ok_btc 14515, ok_flat 101833, ok_other 13422; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 203, ledger ok 886, twap ok 5741.
- OKX insurance fund rows: regular_update 683.
- Research lab: 20 runs in window; latest 2026-11-03 19:47Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-11-02.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-11-03 17:40Z, over 90 minutes before this report.
- snapshot premium_parts: 1/683 routine run(s), 2026-10-31 21:43Z; latest: RuntimeError: deadline reached; absent from the latest run
- snapshot kraken: 4/683 routine run(s), 2026-10-30 02:28Z → 2026-10-30 03:04Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot dydx: 1/683 routine run(s), 2026-10-29 09:13Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
