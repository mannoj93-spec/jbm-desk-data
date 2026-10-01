# JBM desk report — 2026-10-01 00:58Z
Window 2026-09-24 00:58Z → 2026-10-01 00:58Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-01 00:58Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-01 00:53Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-10-01 00:55Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-01 00:53Z | 6 min |
| snapshots | 2026-10-01 00:52Z | 6 min |
| 1-minute prices (BTC perp) | 2026-10-01 00:53Z | 6 min |
| Deribit options | 2026-10-01 00:52Z | 6 min |
| Hyperliquid account sample | 2026-10-01 00:53Z | 6 min |
| Hyperliquid enrichment | 2026-10-01 00:53Z | 6 min |
| OKX insurance fund | 2026-10-01 00:53Z | 6 min |
| OKX liquidation orders | 2026-10-01 00:25Z | 33 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-01 00:55Z | 4 min |

## 1. Collection health
648 routine runs in window, by trigger: schedule 648.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-24 00:58Z → 2026-10-01 00:58Z | `7,22,37,52 * * * *` | 671 | 648 (97%) | 647/671 slot intervals | 6/648 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.2, p90 20.9, max 30.5.
Actual interval between stored snapshots, all triggers (min): median 14.2, p90 20.9, max 30.5.
Runtime per routine run (s): median 105, p90 113, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 648 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 648/648 | ok |
| binance_BTCUSDC | 648/648 | ok |
| binance_BTCUSDT | 648/648 | ok |
| binance_BTCUSD_PERP | 648/648 | ok |
| binance_coinm_prem | 648/648 | ok |
| binance_usdc_prem | 648/648 | ok |
| binance_usdt_prem | 648/648 | ok |
| bingx | 648/648 | ok |
| bitfinex_margin | 648/648 | ok |
| bitget_USDC | 648/648 | ok |
| bitget_USDT | 648/648 | ok |
| cross_binance_ETHUSDT | 648/648 | ok |
| cross_binance_SOLUSDT | 648/648 | ok |
| cross_hl_ETH | 648/648 | ok |
| cross_hl_SOL | 648/648 | ok |
| depth_binance_usdt | 648/648 | ok |
| depth_okx_usdt_swap | 648/648 | ok |
| deribit | 648/648 | ok |
| dydx | 648/648 | ok |
| gate | 648/648 | ok |
| hl_predicted_fundings | 648/648 | ok |
| htx | 642/648 | ok |
| hyperliquid | 648/648 | ok |
| kraken | 648/648 | ok |
| kucoin | 648/648 | ok |
| okx_BTC-USD-SWAP | 648/648 | ok |
| okx_BTC-USDT-SWAP | 648/648 | ok |
| paradex | 648/648 | ok |
| premium_parts | 648/648 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-01 00:00Z | 295 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-01 00:00Z | 295 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-01 00:00Z | 942 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-01 00:45Z | 11306 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-01 00:00Z | 942 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-01 00:45Z | 11306 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-30 23:00Z | 942 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-01 00:45Z | 11306 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-01 00:00Z | 942 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-01 00:45Z | 11306 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-01 00:00Z | 942 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-01 00:45Z | 11305 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-30 23:00Z | 3078 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-30 23:00Z | 917 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-01 00:00Z | 303 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-30 23:00Z | 3077 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-30 23:00Z | 3077 | 0 | 0 |

## 3. Forced-flow retention and revision
15451 distinct liquidation observations; 13 retained boundary probes.
- 2026-09-27 00:22Z: 1.0 days, 4 pages (observed source boundary).
- 2026-09-28 00:24Z: 0.94 days, 10 pages (observed source boundary).
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
- 2026-09-30 00:23Z: 0.98 days, 13 pages (observed source boundary).
- 2026-10-01 00:25Z: 0.98 days, 22 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 5.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 648 stored snapshots in 168 distinct hours from 2026-09-24 01:14Z to 2026-10-01 00:51Z; latest 795 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 648 stored snapshots in 168 distinct hours from 2026-09-24 01:14Z to 2026-10-01 00:51Z; latest 21 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10072 bars 2026-09-24 00:59Z → 2026-10-01 00:50Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10072 bars 2026-09-24 00:59Z → 2026-10-01 00:50Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10072 bars 2026-09-24 00:59Z → 2026-10-01 00:50Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10072 bars 2026-09-24 00:59Z → 2026-10-01 00:50Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10072 bars 2026-09-24 00:59Z → 2026-10-01 00:50Z; 0 missing minutes inside the span.
- Deribit options schema 2: 648 runs; latest 795 with OI, 153 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 648 snapshots; account checks by state ok_btc 14255, ok_flat 95750, ok_other 13115; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 238, ledger ok 886, twap not_attempted 5, twap ok 5351.
- OKX insurance fund rows: regular_update 648.
- Research lab: 32 runs in window; latest 2026-10-01 00:55Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 6/648 routine run(s), 2026-09-25 23:41Z → 2026-09-29 19:44Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
