# JBM desk report — 2026-10-19 01:08Z
Window 2026-10-12 01:08Z → 2026-10-19 01:08Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-19 01:08Z by report-2.6.1-2026-09-30 (weekly report; desk range forecasts are scored hourly by range-score.yml and only summarised here). Input cutoff: 2026-10-19 00:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-18 19:01Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-19 00:59Z | 9 min |
| snapshots | 2026-10-19 00:58Z | 10 min |
| 1-minute prices (BTC perp) | 2026-10-19 00:59Z | 9 min |
| Deribit options | 2026-10-19 00:58Z | 10 min |
| Hyperliquid account sample | 2026-10-19 00:59Z | 9 min |
| Hyperliquid enrichment | 2026-10-19 00:59Z | 9 min |
| OKX insurance fund | 2026-10-19 00:59Z | 9 min |
| OKX liquidation orders | 2026-10-19 00:58Z | 10 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-18 19:01Z | 367 min |

## 1. Collection health
900 routine runs in window, by trigger: schedule 374, workflow_dispatch 526.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-12 01:08Z → 2026-10-19 01:08Z | `7,22,37,52 * * * *` | 670 | 374 (56%) | 671/671 slot intervals | 13/900 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 26.7, p90 36.4, max 56.7.
Actual interval between stored snapshots, all triggers (min): median 11.8, p90 17.1, max 20.6.
Runtime per routine run (s): median 106, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 900 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 900/900 | ok |
| binance_BTCUSDC | 900/900 | ok |
| binance_BTCUSDT | 900/900 | ok |
| binance_BTCUSD_PERP | 900/900 | ok |
| binance_coinm_prem | 900/900 | ok |
| binance_usdc_prem | 900/900 | ok |
| binance_usdt_prem | 900/900 | ok |
| bingx | 900/900 | ok |
| bitfinex_margin | 900/900 | ok |
| bitget_USDC | 900/900 | ok |
| bitget_USDT | 900/900 | ok |
| cross_binance_ETHUSDT | 900/900 | ok |
| cross_binance_SOLUSDT | 900/900 | ok |
| cross_hl_ETH | 900/900 | ok |
| cross_hl_SOL | 900/900 | ok |
| depth_binance_usdt | 900/900 | ok |
| depth_okx_usdt_swap | 900/900 | ok |
| deribit | 897/900 | ok |
| dydx | 900/900 | ok |
| gate | 900/900 | ok |
| hl_predicted_fundings | 900/900 | ok |
| htx | 896/900 | ok |
| hyperliquid | 900/900 | ok |
| kraken | 894/900 | ok |
| kucoin | 900/900 | ok |
| okx_BTC-USD-SWAP | 900/900 | ok |
| okx_BTC-USDT-SWAP | 900/900 | ok |
| paradex | 900/900 | ok |
| premium_parts | 900/900 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-19 00:00Z | 349 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-19 00:00Z | 349 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-19 00:00Z | 1374 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-19 00:50Z | 16491 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-19 00:00Z | 1372 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-19 00:50Z | 16475 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-18 23:00Z | 1374 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-19 00:50Z | 16491 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-19 00:00Z | 1374 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-19 00:50Z | 16491 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-19 00:00Z | 1374 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-19 00:50Z | 16490 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-18 23:00Z | 3510 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-18 23:00Z | 1349 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-19 00:00Z | 357 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-18 23:00Z | 3509 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-18 23:00Z | 3509 | 0 | 0 |

## 3. Forced-flow retention and revision
43394 distinct liquidation observations; 31 retained boundary probes.
- 2026-10-15 00:12Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-16 00:12Z: 0.97 days, 36 pages (observed source boundary).
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
Observed later revision after first live capture: n=30 active hours; mean 7.2%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 897 stored snapshots in 168 distinct hours from 2026-10-12 01:12Z to 2026-10-19 00:57Z; latest 750 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 900 stored snapshots in 168 distinct hours from 2026-10-12 01:12Z to 2026-10-19 00:57Z; latest 18 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10068 bars 2026-10-12 01:09Z → 2026-10-19 00:56Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10068 bars 2026-10-12 01:09Z → 2026-10-19 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10068 bars 2026-10-12 01:09Z → 2026-10-19 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10068 bars 2026-10-12 01:09Z → 2026-10-19 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10068 bars 2026-10-12 01:09Z → 2026-10-19 00:56Z; 0 missing minutes inside the span.
- Deribit options schema 2: 897 runs; latest 750 with OI, 178 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 900 snapshots; account checks by state failed 1, ok_btc 19501, ok_flat 133091, ok_other 18407; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 276, ledger ok 1176, twap not_attempted 9, twap ok 7539.
- OKX insurance fund rows: regular_update 900.
- Research lab: 27 runs in window; latest 2026-10-18 19:01Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Scored: 359 total; 3 this report. Pending/retryable: 25. Late registrations: 0.
- range-rc1d-24h-20261018T0000Z: scored; forecast SHA-256 0fccb62ec41b6a7d1d876a38b05c062979399da3b90c573ba3d7f282f90f1920.
  - B2 range model range-11.1.0: realized ln(H/L) 0.02022; inside q10-q90: True; pinball q10/q50/q90 0.00077/0.00016/0.00180; |q50 - realized| 0.00107; |ln q50 - ln realized| 0.0518 (E2 primary); QLIKE 0.0052.
  - B0 persistence baseline: realized ln(H/L) 0.02022; inside q10-q90: True; pinball q10/q50/q90 0.00066/0.00243/0.00299; |q50 - realized| 0.00560; |ln q50 - ln realized| 0.2445 (E2 primary); QLIKE 0.1022.
- range-rc1d-4h-20261018T2000Z: scored; forecast SHA-256 f23628e3d71852d5a4f936ec37e2425032585065e14c3ac5a900476b4ecf48f6.
  - B2 range model range-11.1.0: realized ln(H/L) 0.01770; inside q10-q90: False; pinball q10/q50/q90 0.00135/0.00521/0.00274; |q50 - realized| 0.01010; |ln q50 - ln realized| 0.8450 (E2 primary); QLIKE 2.7291.
  - B0 persistence baseline: realized ln(H/L) 0.01770; inside q10-q90: True; pinball q10/q50/q90 0.00132/0.00451/0.00016; |q50 - realized| 0.00865; |ln q50 - ln realized| 0.6704 (E2 primary); QLIKE 1.4812.
- range-rc1d-72h-20261016T0000Z: scored; forecast SHA-256 2a44790983d50110230a879131d7241b19b980b0fe1fb654e94097e8b7fb6136.
  - B2 range model range-11.1.0: realized ln(H/L) 0.02787; inside q10-q90: True; pinball q10/q50/q90 0.00021/0.00623/0.00449; |q50 - realized| 0.01443; |ln q50 - ln realized| 0.4172 (E2 primary); QLIKE 0.2685.
  - B0 persistence baseline: realized ln(H/L) 0.02787; inside q10-q90: True; pinball q10/q50/q90 0.00058/0.00445/0.00448; |q50 - realized| 0.01078; |ln q50 - ln realized| 0.3271 (E2 primary); QLIKE 0.1740.

## 5. Pre-registered research tests
Post-registration labels describe timing only. Custom test code can bypass context helpers; leakage, episode independence and causal validity require review.
No research tests completed successfully.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.
- Review newly scored forecasts and retained evidence. A small sample is not calibration.

## 7. Alerts
- snapshot htx: 4/900 routine run(s), 2026-10-12 21:27Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/900 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/900 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/900 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/900 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 6/900 routine run(s), 2026-10-13 07:00Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book hl_positions: 1/900 routine run(s), 2026-10-14 01:12Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- history deribit_dvol_1h: 3/900 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/900 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/900 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
