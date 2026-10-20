# JBM desk report — 2026-10-20 01:31Z
Window 2026-10-13 01:31Z → 2026-10-20 01:31Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-20 01:31Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-20 00:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-20 01:15Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-20 00:59Z | 31 min |
| snapshots | 2026-10-20 00:58Z | 32 min |
| 1-minute prices (BTC perp) | 2026-10-20 00:59Z | 31 min |
| Deribit options | 2026-10-20 00:58Z | 32 min |
| Hyperliquid account sample | 2026-10-20 00:59Z | 31 min |
| Hyperliquid enrichment | 2026-10-20 00:59Z | 31 min |
| OKX insurance fund | 2026-10-20 00:59Z | 31 min |
| OKX liquidation orders | 2026-10-20 00:58Z | 33 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-20 01:15Z | 16 min |

## 1. Collection health
874 routine runs in window, by trigger: schedule 344, workflow_dispatch 530.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-13 01:31Z → 2026-10-20 01:31Z | `7,22,37,52 * * * *` | 671 | 344 (51%) | 668/669 slot intervals; 2 not yet assessed (after the input cutoff) | 12/874 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-20 00:57Z; report clock 2026-10-20 01:31Z: wall-clock lag 33 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 28.6, p90 37.9, max 56.7.
Actual interval between stored snapshots, all triggers (min): median 12.2, p90 17.0, max 26.0.
Runtime per routine run (s): median 105, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 874 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 874/874 | ok |
| binance_BTCUSDC | 874/874 | ok |
| binance_BTCUSDT | 874/874 | ok |
| binance_BTCUSD_PERP | 874/874 | ok |
| binance_coinm_prem | 874/874 | ok |
| binance_usdc_prem | 874/874 | ok |
| binance_usdt_prem | 874/874 | ok |
| bingx | 874/874 | ok |
| bitfinex_margin | 874/874 | ok |
| bitget_USDC | 874/874 | ok |
| bitget_USDT | 874/874 | ok |
| cross_binance_ETHUSDT | 874/874 | ok |
| cross_binance_SOLUSDT | 874/874 | ok |
| cross_hl_ETH | 874/874 | ok |
| cross_hl_SOL | 874/874 | ok |
| depth_binance_usdt | 874/874 | ok |
| depth_okx_usdt_swap | 874/874 | ok |
| deribit | 871/874 | ok |
| dydx | 874/874 | ok |
| gate | 874/874 | ok |
| hl_predicted_fundings | 874/874 | ok |
| htx | 871/874 | ok |
| hyperliquid | 874/874 | ok |
| kraken | 868/874 | ok |
| kucoin | 874/874 | ok |
| okx_BTC-USD-SWAP | 874/874 | ok |
| okx_BTC-USDT-SWAP | 874/874 | ok |
| paradex | 874/874 | ok |
| premium_parts | 874/874 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-20 00:00Z | 352 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-20 00:00Z | 352 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-20 00:00Z | 1398 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-20 00:50Z | 16779 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-20 00:00Z | 1396 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-20 00:50Z | 16763 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-19 23:00Z | 1398 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-20 00:50Z | 16779 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-20 00:00Z | 1398 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-20 00:50Z | 16779 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-20 00:00Z | 1398 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-20 00:50Z | 16778 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-19 23:00Z | 3534 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-19 23:00Z | 1373 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-20 00:00Z | 360 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-19 23:00Z | 3533 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-19 23:00Z | 3533 | 0 | 0 |

## 3. Forced-flow retention and revision
44483 distinct liquidation observations; 32 retained boundary probes.
- 2026-10-16 00:12Z: 0.97 days, 36 pages (observed source boundary).
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 7.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 871 stored snapshots in 168 distinct hours from 2026-10-13 01:39Z to 2026-10-20 00:57Z; latest 732 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 874 stored snapshots in 168 distinct hours from 2026-10-13 01:39Z to 2026-10-20 00:57Z; latest 21 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10045 bars 2026-10-13 01:32Z → 2026-10-20 00:56Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10045 bars 2026-10-13 01:32Z → 2026-10-20 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10045 bars 2026-10-13 01:32Z → 2026-10-20 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10045 bars 2026-10-13 01:32Z → 2026-10-20 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10045 bars 2026-10-13 01:32Z → 2026-10-20 00:56Z; 0 missing minutes inside the span.
- Deribit options schema 2: 871 runs; latest 732 with OI, 152 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 874 snapshots; account checks by state failed 1, ok_btc 19014, ok_flat 129263, ok_other 17782; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 272, ledger ok 1146, twap not_attempted 4, twap ok 7318.
- OKX insurance fund rows: regular_update 874.
- Research lab: 28 runs in window; latest 2026-10-20 01:15Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/874 routine run(s), 2026-10-14 08:50Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/874 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/874 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/874 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/874 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 6/874 routine run(s), 2026-10-13 07:00Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book hl_positions: 1/874 routine run(s), 2026-10-14 01:12Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- history deribit_dvol_1h: 3/874 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/874 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/874 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
