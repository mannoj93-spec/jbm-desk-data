# JBM desk report — 2026-10-19 19:29Z
Window 2026-10-12 19:29Z → 2026-10-19 19:29Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-19 19:29Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-19 18:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-19 19:14Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-19 18:59Z | 31 min |
| snapshots | 2026-10-19 18:58Z | 31 min |
| 1-minute prices (BTC perp) | 2026-10-19 18:59Z | 31 min |
| Deribit options | 2026-10-19 18:58Z | 31 min |
| Hyperliquid account sample | 2026-10-19 18:59Z | 31 min |
| Hyperliquid enrichment | 2026-10-19 18:59Z | 31 min |
| OKX insurance fund | 2026-10-19 18:59Z | 31 min |
| OKX liquidation orders | 2026-10-19 18:28Z | 61 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-19 19:14Z | 16 min |

## 1. Collection health
888 routine runs in window, by trigger: schedule 354, workflow_dispatch 534.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-12 19:29Z → 2026-10-19 19:29Z | `7,22,37,52 * * * *` | 671 | 354 (53%) | 670/671 slot intervals | 13/888 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 27.9, p90 37.8, max 56.7.
Actual interval between stored snapshots, all triggers (min): median 12.0, p90 17.0, max 22.2.
Runtime per routine run (s): median 106, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 888 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 888/888 | ok |
| binance_BTCUSDC | 888/888 | ok |
| binance_BTCUSDT | 888/888 | ok |
| binance_BTCUSD_PERP | 888/888 | ok |
| binance_coinm_prem | 888/888 | ok |
| binance_usdc_prem | 888/888 | ok |
| binance_usdt_prem | 888/888 | ok |
| bingx | 888/888 | ok |
| bitfinex_margin | 888/888 | ok |
| bitget_USDC | 888/888 | ok |
| bitget_USDT | 888/888 | ok |
| cross_binance_ETHUSDT | 888/888 | ok |
| cross_binance_SOLUSDT | 888/888 | ok |
| cross_hl_ETH | 888/888 | ok |
| cross_hl_SOL | 888/888 | ok |
| depth_binance_usdt | 888/888 | ok |
| depth_okx_usdt_swap | 888/888 | ok |
| deribit | 885/888 | ok |
| dydx | 888/888 | ok |
| gate | 888/888 | ok |
| hl_predicted_fundings | 888/888 | ok |
| htx | 884/888 | ok |
| hyperliquid | 888/888 | ok |
| kraken | 882/888 | ok |
| kucoin | 888/888 | ok |
| okx_BTC-USD-SWAP | 888/888 | ok |
| okx_BTC-USDT-SWAP | 888/888 | ok |
| paradex | 888/888 | ok |
| premium_parts | 888/888 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-19 16:00Z | 351 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-19 16:00Z | 351 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-19 18:00Z | 1392 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-19 18:50Z | 16707 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-19 18:00Z | 1390 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-19 18:50Z | 16691 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-19 17:00Z | 1392 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-19 18:50Z | 16707 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-19 18:00Z | 1392 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-19 18:50Z | 16707 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-19 18:00Z | 1392 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-19 18:50Z | 16706 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-19 17:00Z | 3528 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-19 17:00Z | 1367 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-19 16:00Z | 359 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-19 17:00Z | 3527 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-19 17:00Z | 3527 | 0 | 0 |

## 3. Forced-flow retention and revision
44302 distinct liquidation observations; 31 retained boundary probes.
- 2026-10-15 00:12Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-16 00:12Z: 0.97 days, 36 pages (observed source boundary).
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 885 stored snapshots in 168 distinct hours from 2026-10-12 19:34Z to 2026-10-19 18:57Z; latest 731 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 888 stored snapshots in 168 distinct hours from 2026-10-12 19:34Z to 2026-10-19 18:57Z; latest 22 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10047 bars 2026-10-12 19:30Z → 2026-10-19 18:56Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10047 bars 2026-10-12 19:30Z → 2026-10-19 18:56Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10047 bars 2026-10-12 19:30Z → 2026-10-19 18:56Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10047 bars 2026-10-12 19:30Z → 2026-10-19 18:56Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10047 bars 2026-10-12 19:30Z → 2026-10-19 18:56Z; 0 missing minutes inside the span.
- Deribit options schema 2: 885 runs; latest 731 with OI, 153 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 888 snapshots; account checks by state failed 1, ok_btc 19296, ok_flat 131338, ok_other 18085; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 275, ledger ok 1163, twap not_attempted 9, twap ok 7433.
- OKX insurance fund rows: regular_update 888.
- Research lab: 28 runs in window; latest 2026-10-19 19:14Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 4/888 routine run(s), 2026-10-12 21:27Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/888 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/888 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/888 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/888 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 6/888 routine run(s), 2026-10-13 07:00Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book hl_positions: 1/888 routine run(s), 2026-10-14 01:12Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- history deribit_dvol_1h: 3/888 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/888 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/888 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
