# JBM desk report — 2026-10-13 19:14Z
Window 2026-10-06 19:14Z → 2026-10-13 19:14Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-13 19:14Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-13 19:02Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-13 19:05Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-13 19:02Z | 13 min |
| snapshots | 2026-10-13 19:01Z | 13 min |
| 1-minute prices (BTC perp) | 2026-10-13 19:02Z | 13 min |
| Deribit options | 2026-10-13 19:01Z | 13 min |
| Hyperliquid account sample | 2026-10-13 19:02Z | 13 min |
| Hyperliquid enrichment | 2026-10-13 19:02Z | 13 min |
| OKX insurance fund | 2026-10-13 19:02Z | 13 min |
| OKX liquidation orders | 2026-10-13 18:13Z | 61 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-13 19:05Z | 10 min |

## 1. Collection health
1128 routine runs in window, by trigger: schedule 579, workflow_dispatch 549.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-06 19:14Z → 2026-10-13 19:14Z | `7,22,37,52 * * * *` | 671 | 579 (86%) | 670/671 slot intervals | 8/1128 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 16.0, p90 23.9, max 41.7.
Actual interval between stored snapshots, all triggers (min): median 8.8, p90 15.2, max 25.7.
Runtime per routine run (s): median 105, p90 114, max 237; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1128 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 1128/1128 | ok |
| binance_BTCUSDC | 1128/1128 | ok |
| binance_BTCUSDT | 1128/1128 | ok |
| binance_BTCUSD_PERP | 1128/1128 | ok |
| binance_coinm_prem | 1128/1128 | ok |
| binance_usdc_prem | 1128/1128 | ok |
| binance_usdt_prem | 1128/1128 | ok |
| bingx | 1128/1128 | ok |
| bitfinex_margin | 1128/1128 | ok |
| bitget_USDC | 1128/1128 | ok |
| bitget_USDT | 1128/1128 | ok |
| cross_binance_ETHUSDT | 1128/1128 | ok |
| cross_binance_SOLUSDT | 1128/1128 | ok |
| cross_hl_ETH | 1127/1128 | ok |
| cross_hl_SOL | 1127/1128 | ok |
| depth_binance_usdt | 1128/1128 | ok |
| depth_okx_usdt_swap | 1128/1128 | ok |
| deribit | 1125/1128 | ok |
| dydx | 1128/1128 | ok |
| gate | 1128/1128 | ok |
| hl_predicted_fundings | 1127/1128 | ok |
| htx | 1126/1128 | ok |
| hyperliquid | 1127/1128 | ok |
| kraken | 1126/1128 | ok |
| kucoin | 1128/1128 | ok |
| okx_BTC-USD-SWAP | 1128/1128 | ok |
| okx_BTC-USDT-SWAP | 1128/1128 | ok |
| paradex | 1128/1128 | ok |
| premium_parts | 1128/1128 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-13 16:00Z | 333 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-13 16:00Z | 333 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-13 18:00Z | 1248 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-13 18:55Z | 14980 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-13 18:00Z | 1248 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-13 18:55Z | 14980 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-13 18:00Z | 1249 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-13 18:55Z | 14980 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-13 18:00Z | 1248 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-13 18:55Z | 14980 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-13 18:00Z | 1248 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-13 18:55Z | 14979 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-13 18:00Z | 3385 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-13 18:00Z | 1224 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-13 16:00Z | 341 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-13 18:00Z | 3384 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-13 18:00Z | 3384 | 0 | 0 |

## 3. Forced-flow retention and revision
34715 distinct liquidation observations; 25 retained boundary probes.
- 2026-10-09 00:13Z: 0.93 days, 35 pages (observed source boundary).
- 2026-10-10 00:12Z: 0.95 days, 14 pages (observed source boundary).
- 2026-10-11 00:12Z: 0.99 days, 4 pages (observed source boundary).
- 2026-10-12 00:12Z: 0.94 days, 9 pages (observed source boundary).
- 2026-10-13 00:00Z: 0.98 days, 23 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 8.7%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 1125 stored snapshots in 169 distinct hours from 2026-10-06 19:15Z to 2026-10-13 19:00Z; latest 744 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 1128 stored snapshots in 169 distinct hours from 2026-10-06 19:15Z to 2026-10-13 19:00Z; latest 17 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10065 bars 2026-10-06 19:15Z → 2026-10-13 18:59Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10065 bars 2026-10-06 19:15Z → 2026-10-13 18:59Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10065 bars 2026-10-06 19:15Z → 2026-10-13 18:59Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10065 bars 2026-10-06 19:15Z → 2026-10-13 18:59Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10065 bars 2026-10-06 19:15Z → 2026-10-13 18:59Z; 0 missing minutes inside the span.
- Deribit options schema 2: 1125 runs; latest 744 with OI, 144 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 1128 snapshots; account checks by state failed 5, ok_btc 24580, ok_flat 166432, ok_other 23303; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 298, ledger ok 1426, twap not_attempted 5, twap ok 9551.
- OKX insurance fund rows: regular_update 1128.
- Research lab: 28 runs in window; latest 2026-10-13 19:05Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-12.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot kraken: 2/1128 routine run(s), 2026-10-13 07:00Z → 2026-10-13 13:00Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- history deribit_dvol_1h: 3/1128 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/1128 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/1128 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- snapshot htx: 2/1128 routine run(s), 2026-10-10 00:42Z → 2026-10-12 21:27Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot hyperliquid: 1/1128 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/1128 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/1128 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/1128 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- forward book hl_positions: 1/1128 routine run(s), 2026-10-10 08:17Z; latest: degraded: 5/190 accounts failed, malformed or not attempted; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
