# JBM desk report — 2026-10-03 16:58Z
Window 2026-09-26 16:58Z → 2026-10-03 16:58Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-03 16:58Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-03 15:50Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-10-03 16:57Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-03 15:50Z | 68 min |
| snapshots | 2026-10-03 15:49Z | 69 min |
| 1-minute prices (BTC perp) | 2026-10-03 15:50Z | 68 min |
| Deribit options | 2026-10-03 15:49Z | 69 min |
| Hyperliquid account sample | 2026-10-03 15:50Z | 68 min |
| Hyperliquid enrichment | 2026-10-03 15:50Z | 68 min |
| OKX insurance fund | 2026-10-03 15:50Z | 68 min |
| OKX liquidation orders | 2026-10-03 15:49Z | 69 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-03 16:57Z | 2 min |

## 1. Collection health
616 routine runs in window, by trigger: schedule 615, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-26 16:58Z → 2026-10-03 16:58Z | `7,22,37,52 * * * *` | 671 | 615 (92%) | 615/671 slot intervals | 6/616 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.8, p90 21.2, max 142.9.
Actual interval between stored snapshots, all triggers (min): median 14.8, p90 21.2, max 142.9.
Runtime per routine run (s): median 105, p90 113, max 130; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 616 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 616/616 | ok |
| binance_BTCUSDC | 616/616 | ok |
| binance_BTCUSDT | 616/616 | ok |
| binance_BTCUSD_PERP | 616/616 | ok |
| binance_coinm_prem | 616/616 | ok |
| binance_usdc_prem | 616/616 | ok |
| binance_usdt_prem | 616/616 | ok |
| bingx | 616/616 | ok |
| bitfinex_margin | 616/616 | ok |
| bitget_USDC | 616/616 | ok |
| bitget_USDT | 616/616 | ok |
| cross_binance_ETHUSDT | 616/616 | ok |
| cross_binance_SOLUSDT | 616/616 | ok |
| cross_hl_ETH | 616/616 | ok |
| cross_hl_SOL | 616/616 | ok |
| depth_binance_usdt | 616/616 | ok |
| depth_okx_usdt_swap | 616/616 | ok |
| deribit | 616/616 | ok |
| dydx | 616/616 | ok |
| gate | 616/616 | ok |
| hl_predicted_fundings | 616/616 | ok |
| htx | 611/616 | ok |
| hyperliquid | 616/616 | ok |
| kraken | 615/616 | ok |
| kucoin | 616/616 | ok |
| okx_BTC-USD-SWAP | 616/616 | ok |
| okx_BTC-USDT-SWAP | 616/616 | ok |
| paradex | 616/616 | ok |
| premium_parts | 616/616 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-03 08:00Z | 302 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-03 08:00Z | 302 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-03 15:00Z | 1005 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-03 15:40Z | 12061 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-03 15:00Z | 1005 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-03 15:40Z | 12061 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-03 14:00Z | 1005 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-03 15:40Z | 12061 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-03 15:00Z | 1005 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-03 15:40Z | 12061 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-03 15:00Z | 1005 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-03 15:40Z | 12060 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-03 14:00Z | 3141 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-03 14:00Z | 980 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-03 08:00Z | 310 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-03 14:00Z | 3140 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-03 14:00Z | 3140 | 0 | 0 |

## 3. Forced-flow retention and revision
19625 distinct liquidation observations; 15 retained boundary probes.
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
- 2026-09-30 00:23Z: 0.98 days, 13 pages (observed source boundary).
- 2026-10-01 00:25Z: 0.98 days, 22 pages (observed source boundary).
- 2026-10-02 00:23Z: 0.9 days, 13 pages (observed source boundary).
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
Observed later revision after first live capture: n=31 active hours; mean 7.4%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 616 stored snapshots in 165 distinct hours from 2026-09-26 17:13Z to 2026-10-03 15:48Z; latest 810 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 616 stored snapshots in 165 distinct hours from 2026-09-26 17:13Z to 2026-10-03 15:48Z; latest 24 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10009 bars 2026-09-26 16:59Z → 2026-10-03 15:47Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10009 bars 2026-09-26 16:59Z → 2026-10-03 15:47Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10009 bars 2026-09-26 16:59Z → 2026-10-03 15:47Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10009 bars 2026-09-26 16:59Z → 2026-10-03 15:47Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10009 bars 2026-09-26 16:59Z → 2026-10-03 15:47Z; 0 missing minutes inside the span.
- Deribit options schema 2: 616 runs; latest 810 with OI, 192 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 165.
- Hyperliquid sample v2: 616 snapshots; account checks by state ok_btc 13585, ok_flat 90806, ok_other 12649; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 220, ledger ok 836, twap not_attempted 3, twap ok 5101.
- OKX insurance fund rows: regular_update 616.
- Research lab: 28 runs in window; latest 2026-10-03 16:57Z: exploratory 6, under prospective evaluation 2 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.95 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-10-03 13:27Z, over 90 minutes before this report.
- snapshot htx: 5/616 routine run(s), 2026-09-28 05:30Z → 2026-10-03 08:59Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 1/616 routine run(s), 2026-10-01 07:03Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
