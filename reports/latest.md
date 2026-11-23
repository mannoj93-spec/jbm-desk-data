# JBM desk report — 2026-11-23 08:13Z
Window 2026-11-16 08:13Z → 2026-11-23 08:13Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-23 08:13Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-23 08:00Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-23 08:08Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-23 08:00Z | 13 min |
| snapshots | 2026-11-23 07:59Z | 14 min |
| 1-minute prices (BTC perp) | 2026-11-23 08:00Z | 13 min |
| Deribit options | 2026-11-23 07:59Z | 14 min |
| Hyperliquid account sample | 2026-11-23 08:00Z | 13 min |
| Hyperliquid enrichment | 2026-11-23 08:00Z | 13 min |
| OKX insurance fund | 2026-11-23 08:00Z | 13 min |
| OKX liquidation orders | 2026-11-23 06:44Z | 89 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-23 08:08Z | 5 min |

## 1. Collection health
678 routine runs in window, by trigger: schedule 24, workflow_dispatch 654.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-11-16 08:13Z → 2026-11-23 08:13Z | `7,22,37,52 * * * *` | 671 | 24 (4%) | 664/670 slot intervals; 1 not yet assessed (after the input cutoff) | 9/678 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-23 07:58Z; report clock 2026-11-23 08:13Z: wall-clock lag 14 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 427.5, p90 533.1, max 610.1.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.4, max 30.7.
Runtime per routine run (s): median 107, p90 122, max 180; 0 run(s) reached the network budget.
Rate-limit incidents: www.deribit.com 1108, api.hyperliquid.xyz 11 across 678 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 4.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 678/678 | ok |
| binance_BTCUSDC | 678/678 | ok |
| binance_BTCUSDT | 678/678 | ok |
| binance_BTCUSD_PERP | 678/678 | ok |
| binance_coinm_prem | 678/678 | ok |
| binance_usdc_prem | 678/678 | ok |
| binance_usdt_prem | 678/678 | ok |
| bingx | 678/678 | ok |
| bitfinex_margin | 678/678 | ok |
| bitget_USDC | 678/678 | ok |
| bitget_USDT | 678/678 | ok |
| cross_binance_ETHUSDT | 678/678 | ok |
| cross_binance_SOLUSDT | 678/678 | ok |
| cross_hl_ETH | 678/678 | ok |
| cross_hl_SOL | 678/678 | ok |
| depth_binance_usdt | 678/678 | ok |
| depth_okx_usdt_swap | 678/678 | ok |
| deribit | 670/678 | ok |
| dydx | 678/678 | ok |
| gate | 678/678 | ok |
| hl_predicted_fundings | 678/678 | ok |
| htx | 677/678 | ok |
| hyperliquid | 678/678 | ok |
| kraken | 678/678 | ok |
| kucoin | 678/678 | ok |
| okx_BTC-USD-SWAP | 678/678 | ok |
| okx_BTC-USDT-SWAP | 678/678 | ok |
| paradex | 678/678 | ok |
| premium_parts | 678/678 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-23 00:00Z | 454 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-23 00:00Z | 454 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-23 07:00Z | 2221 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-23 07:50Z | 26655 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-23 07:00Z | 2219 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-23 07:50Z | 26639 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-23 06:00Z | 2221 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-23 07:50Z | 26655 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-23 07:00Z | 2221 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-23 07:50Z | 26655 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-23 07:00Z | 2221 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-23 07:50Z | 26654 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-20 18:00Z | 4297 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-23 06:00Z | 2196 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-23 00:00Z | 462 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-23 06:00Z | 4356 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-23 06:00Z | 4356 | 0 | 0 |

## 3. Forced-flow retention and revision
142585 distinct liquidation observations; 66 retained boundary probes.
- 2026-11-19 00:13Z: 0.99 days, 33 pages (observed source boundary).
- 2026-11-20 00:13Z: 1.0 days, 35 pages (observed source boundary).
- 2026-11-21 00:13Z: 1.0 days, 79 pages (observed source boundary).
- 2026-11-22 00:13Z: 0.96 days, 73 pages (observed source boundary).
- 2026-11-23 00:13Z: 0.98 days, 36 pages (observed source boundary).
Observed later revision after first live capture: n=56 active hours; mean 5.5%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 674 stored snapshots in 167 distinct hours from 2026-11-16 08:13Z to 2026-11-23 07:58Z; latest 862 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 678 stored snapshots in 168 distinct hours from 2026-11-16 08:13Z to 2026-11-23 07:58Z; latest 18 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10064 bars 2026-11-16 08:14Z → 2026-11-23 07:57Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10064 bars 2026-11-16 08:14Z → 2026-11-23 07:57Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10064 bars 2026-11-16 08:14Z → 2026-11-23 07:57Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10064 bars 2026-11-16 08:14Z → 2026-11-23 07:57Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10064 bars 2026-11-16 08:14Z → 2026-11-23 07:57Z; 0 missing minutes inside the span.
- Deribit options schema 2: 674 runs; latest 862 with OI, 156 zero OI, 0 absent, 0 past expiry; panel 8/12 tickers; 4 failed or out of time; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 678 snapshots; account checks by state failed 3, ok_btc 14462, ok_flat 103217, ok_other 11138; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 322, ledger ok 1000, twap not_attempted 4, twap ok 5454.
- OKX insurance fund rows: regular_update 678.
- Research lab: 13 runs in window; latest 2026-11-23 08:08Z: exploratory 1, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-11-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- history deribit_dvol_1h: 246/678 routine run(s), 2026-11-20 20:13Z → 2026-11-23 07:58Z; latest: DVOL: incomplete DVOL day; checkpoint retained
- rate limit www.deribit.com: 242/678 routine run(s), 2026-11-20 21:13Z → 2026-11-23 07:58Z; latest: 4 rate-limited response(s)
- snapshot deribit: 8/678 routine run(s), 2026-11-20 19:28Z → 2026-11-20 21:13Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 4/678 routine run(s), 2026-11-20 20:13Z → 2026-11-20 20:58Z; latest: RuntimeError: HTTP 503; absent from the latest run
- snapshot htx: 1/678 routine run(s), 2026-11-18 04:13Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- forward book hl_positions: 1/678 routine run(s), 2026-11-17 02:43Z; latest: degraded: 3/190 accounts failed, malformed or not attempted; absent from the latest run
- rate limit api.hyperliquid.xyz: 1/678 routine run(s), 2026-11-17 02:43Z; latest: 11 rate-limited response(s); absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
- deribit_dvol_1h: stale; last observation 2026-11-20 18:00Z
