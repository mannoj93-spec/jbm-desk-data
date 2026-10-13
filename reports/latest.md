# JBM desk report — 2026-10-13 01:06Z
Window 2026-10-06 01:06Z → 2026-10-13 01:06Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-13 01:06Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-13 00:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-13 01:02Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-13 00:59Z | 8 min |
| snapshots | 2026-10-13 00:58Z | 8 min |
| 1-minute prices (BTC perp) | 2026-10-13 00:59Z | 8 min |
| Deribit options | 2026-10-13 00:58Z | 8 min |
| Hyperliquid account sample | 2026-10-13 00:59Z | 8 min |
| Hyperliquid enrichment | 2026-10-13 00:59Z | 8 min |
| OKX insurance fund | 2026-10-13 00:59Z | 8 min |
| OKX liquidation orders | 2026-10-13 00:58Z | 8 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-13 01:02Z | 5 min |

## 1. Collection health
1160 routine runs in window, by trigger: schedule 597, workflow_dispatch 563.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-06 01:06Z → 2026-10-13 01:06Z | `7,22,37,52 * * * *` | 671 | 597 (89%) | 670/671 slot intervals | 5/1160 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.8, p90 22.6, max 41.7.
Actual interval between stored snapshots, all triggers (min): median 8.6, p90 14.8, max 25.7.
Runtime per routine run (s): median 104, p90 113, max 237; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1160 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 1160/1160 | ok |
| binance_BTCUSDC | 1160/1160 | ok |
| binance_BTCUSDT | 1160/1160 | ok |
| binance_BTCUSD_PERP | 1160/1160 | ok |
| binance_coinm_prem | 1160/1160 | ok |
| binance_usdc_prem | 1160/1160 | ok |
| binance_usdt_prem | 1160/1160 | ok |
| bingx | 1160/1160 | ok |
| bitfinex_margin | 1160/1160 | ok |
| bitget_USDC | 1160/1160 | ok |
| bitget_USDT | 1160/1160 | ok |
| cross_binance_ETHUSDT | 1160/1160 | ok |
| cross_binance_SOLUSDT | 1160/1160 | ok |
| cross_hl_ETH | 1159/1160 | ok |
| cross_hl_SOL | 1159/1160 | ok |
| depth_binance_usdt | 1160/1160 | ok |
| depth_okx_usdt_swap | 1160/1160 | ok |
| deribit | 1160/1160 | ok |
| dydx | 1160/1160 | ok |
| gate | 1160/1160 | ok |
| hl_predicted_fundings | 1159/1160 | ok |
| htx | 1157/1160 | ok |
| hyperliquid | 1159/1160 | ok |
| kraken | 1159/1160 | ok |
| kucoin | 1160/1160 | ok |
| okx_BTC-USD-SWAP | 1160/1160 | ok |
| okx_BTC-USDT-SWAP | 1160/1160 | ok |
| paradex | 1160/1160 | ok |
| premium_parts | 1160/1160 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-13 00:00Z | 331 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-13 00:00Z | 331 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-13 00:00Z | 1230 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-13 00:50Z | 14763 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-13 00:00Z | 1230 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-13 00:50Z | 14763 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-12 23:00Z | 1230 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-13 00:50Z | 14763 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-13 00:00Z | 1230 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-13 00:50Z | 14763 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-13 00:00Z | 1230 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-13 00:50Z | 14762 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-12 23:00Z | 3366 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-12 23:00Z | 1205 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-13 00:00Z | 339 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-12 23:00Z | 3365 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-12 23:00Z | 3365 | 0 | 0 |

## 3. Forced-flow retention and revision
33426 distinct liquidation observations; 25 retained boundary probes.
- 2026-10-09 00:13Z: 0.93 days, 35 pages (observed source boundary).
- 2026-10-10 00:12Z: 0.95 days, 14 pages (observed source boundary).
- 2026-10-11 00:12Z: 0.99 days, 4 pages (observed source boundary).
- 2026-10-12 00:12Z: 0.94 days, 9 pages (observed source boundary).
- 2026-10-13 00:00Z: 0.98 days, 23 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 10.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 1160 stored snapshots in 168 distinct hours from 2026-10-06 01:12Z to 2026-10-13 00:57Z; latest 745 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 1160 stored snapshots in 168 distinct hours from 2026-10-06 01:12Z to 2026-10-13 00:57Z; latest 20 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10070 bars 2026-10-06 01:07Z → 2026-10-13 00:56Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10070 bars 2026-10-06 01:07Z → 2026-10-13 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10070 bars 2026-10-06 01:07Z → 2026-10-13 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10070 bars 2026-10-06 01:07Z → 2026-10-13 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10070 bars 2026-10-06 01:07Z → 2026-10-13 00:56Z; 0 missing minutes inside the span.
- Deribit options schema 2: 1160 runs; latest 745 with OI, 143 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 1160 snapshots; account checks by state failed 5, ok_btc 25346, ok_flat 171072, ok_other 23977; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 303, ledger ok 1463, twap not_attempted 5, twap ok 9829.
- OKX insurance fund rows: regular_update 1160.
- Research lab: 28 runs in window; latest 2026-10-13 01:02Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-12.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/1160 routine run(s), 2026-10-06 13:50Z → 2026-10-12 21:27Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot hyperliquid: 1/1160 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/1160 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/1160 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/1160 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- forward book hl_positions: 1/1160 routine run(s), 2026-10-10 08:17Z; latest: degraded: 5/190 accounts failed, malformed or not attempted; absent from the latest run
- snapshot kraken: 1/1160 routine run(s), 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
