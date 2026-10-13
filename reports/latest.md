# JBM desk report — 2026-10-13 07:12Z
Window 2026-10-06 07:12Z → 2026-10-13 07:12Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-13 07:12Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-13 07:02Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-13 07:03Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-13 07:02Z | 10 min |
| snapshots | 2026-10-13 07:01Z | 11 min |
| 1-minute prices (BTC perp) | 2026-10-13 07:02Z | 10 min |
| Deribit options | 2026-10-13 07:01Z | 11 min |
| Hyperliquid account sample | 2026-10-13 07:02Z | 10 min |
| Hyperliquid enrichment | 2026-10-13 07:02Z | 10 min |
| OKX insurance fund | 2026-10-13 07:02Z | 10 min |
| OKX liquidation orders | 2026-10-13 06:43Z | 29 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-13 07:03Z | 9 min |

## 1. Collection health
1150 routine runs in window, by trigger: schedule 592, workflow_dispatch 558.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-06 07:12Z → 2026-10-13 07:12Z | `7,22,37,52 * * * *` | 671 | 592 (88%) | 670/671 slot intervals | 5/1150 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.9, p90 22.8, max 41.7.
Actual interval between stored snapshots, all triggers (min): median 8.7, p90 15.0, max 25.7.
Runtime per routine run (s): median 105, p90 114, max 237; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1150 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 1150/1150 | ok |
| binance_BTCUSDC | 1150/1150 | ok |
| binance_BTCUSDT | 1150/1150 | ok |
| binance_BTCUSD_PERP | 1150/1150 | ok |
| binance_coinm_prem | 1150/1150 | ok |
| binance_usdc_prem | 1150/1150 | ok |
| binance_usdt_prem | 1150/1150 | ok |
| bingx | 1150/1150 | ok |
| bitfinex_margin | 1150/1150 | ok |
| bitget_USDC | 1150/1150 | ok |
| bitget_USDT | 1150/1150 | ok |
| cross_binance_ETHUSDT | 1150/1150 | ok |
| cross_binance_SOLUSDT | 1150/1150 | ok |
| cross_hl_ETH | 1149/1150 | ok |
| cross_hl_SOL | 1149/1150 | ok |
| depth_binance_usdt | 1150/1150 | ok |
| depth_okx_usdt_swap | 1150/1150 | ok |
| deribit | 1150/1150 | ok |
| dydx | 1150/1150 | ok |
| gate | 1150/1150 | ok |
| hl_predicted_fundings | 1149/1150 | ok |
| htx | 1147/1150 | ok |
| hyperliquid | 1149/1150 | ok |
| kraken | 1149/1150 | RuntimeError: HTTP 503; deadline reached |
| kucoin | 1150/1150 | ok |
| okx_BTC-USD-SWAP | 1150/1150 | ok |
| okx_BTC-USDT-SWAP | 1150/1150 | ok |
| paradex | 1150/1150 | ok |
| premium_parts | 1150/1150 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-13 00:00Z | 331 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-13 00:00Z | 331 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-13 06:00Z | 1236 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-13 06:55Z | 14836 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-13 06:00Z | 1236 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-13 06:55Z | 14836 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-13 06:00Z | 1237 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-13 06:55Z | 14836 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-13 06:00Z | 1236 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-13 06:55Z | 14836 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-13 06:00Z | 1236 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-13 06:55Z | 14835 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-13 06:00Z | 3373 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-13 06:00Z | 1212 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-13 00:00Z | 339 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-13 06:00Z | 3372 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-13 06:00Z | 3372 | 0 | 0 |

## 3. Forced-flow retention and revision
34122 distinct liquidation observations; 25 retained boundary probes.
- 2026-10-09 00:13Z: 0.93 days, 35 pages (observed source boundary).
- 2026-10-10 00:12Z: 0.95 days, 14 pages (observed source boundary).
- 2026-10-11 00:12Z: 0.99 days, 4 pages (observed source boundary).
- 2026-10-12 00:12Z: 0.94 days, 9 pages (observed source boundary).
- 2026-10-13 00:00Z: 0.98 days, 23 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 8.1%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 1150 stored snapshots in 169 distinct hours from 2026-10-06 07:18Z to 2026-10-13 07:00Z; latest 747 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 1150 stored snapshots in 169 distinct hours from 2026-10-06 07:18Z to 2026-10-13 07:00Z; latest 19 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10067 bars 2026-10-06 07:13Z → 2026-10-13 06:59Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10067 bars 2026-10-06 07:13Z → 2026-10-13 06:59Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10067 bars 2026-10-06 07:13Z → 2026-10-13 06:59Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10067 bars 2026-10-06 07:13Z → 2026-10-13 06:59Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10067 bars 2026-10-06 07:13Z → 2026-10-13 06:59Z; 0 missing minutes inside the span.
- Deribit options schema 2: 1150 runs; latest 747 with OI, 141 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 1150 snapshots; account checks by state failed 5, ok_btc 25098, ok_flat 169637, ok_other 23760; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 302, ledger ok 1452, twap not_attempted 5, twap ok 9741.
- OKX insurance fund rows: regular_update 1151.
- Research lab: 28 runs in window; latest 2026-10-13 07:03Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-12.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot kraken: 1/1150 routine run(s), 2026-10-13 07:00Z; latest: RuntimeError: HTTP 503; deadline reached
- snapshot htx: 3/1150 routine run(s), 2026-10-06 13:50Z → 2026-10-12 21:27Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot hyperliquid: 1/1150 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/1150 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/1150 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/1150 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- forward book hl_positions: 1/1150 routine run(s), 2026-10-10 08:17Z; latest: degraded: 5/190 accounts failed, malformed or not attempted; absent from the latest run
- Latest kraken snapshot unavailable: RuntimeError: HTTP 503; deadline reached
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
