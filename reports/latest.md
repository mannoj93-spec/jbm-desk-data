# JBM desk report — 2026-10-22 01:32Z
Window 2026-10-15 01:32Z → 2026-10-22 01:32Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-22 01:32Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-22 00:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-22 01:14Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-22 00:59Z | 32 min |
| snapshots | 2026-10-22 00:58Z | 33 min |
| 1-minute prices (BTC perp) | 2026-10-22 00:59Z | 32 min |
| Deribit options | 2026-10-22 00:58Z | 33 min |
| Hyperliquid account sample | 2026-10-22 00:59Z | 32 min |
| Hyperliquid enrichment | 2026-10-22 00:59Z | 32 min |
| OKX insurance fund | 2026-10-22 00:59Z | 32 min |
| OKX liquidation orders | 2026-10-22 00:13Z | 78 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-22 01:14Z | 18 min |

## 1. Collection health
875 routine runs in window, by trigger: schedule 327, workflow_dispatch 548.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-15 01:32Z → 2026-10-22 01:32Z | `7,22,37,52 * * * *` | 671 | 327 (49%) | 666/669 slot intervals; 2 not yet assessed (after the input cutoff) | 6/875 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-22 00:57Z; report clock 2026-10-22 01:32Z: wall-clock lag 34 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 29.9, p90 39.0, max 74.9.
Actual interval between stored snapshots, all triggers (min): median 12.3, p90 16.6, max 30.0.
Runtime per routine run (s): median 105, p90 114, max 147; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 875 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 875/875 | ok |
| binance_BTCUSDC | 875/875 | ok |
| binance_BTCUSDT | 875/875 | ok |
| binance_BTCUSD_PERP | 875/875 | ok |
| binance_coinm_prem | 875/875 | ok |
| binance_usdc_prem | 875/875 | ok |
| binance_usdt_prem | 875/875 | ok |
| bingx | 875/875 | ok |
| bitfinex_margin | 875/875 | ok |
| bitget_USDC | 875/875 | ok |
| bitget_USDT | 875/875 | ok |
| cross_binance_ETHUSDT | 875/875 | ok |
| cross_binance_SOLUSDT | 875/875 | ok |
| cross_hl_ETH | 875/875 | ok |
| cross_hl_SOL | 875/875 | ok |
| depth_binance_usdt | 875/875 | ok |
| depth_okx_usdt_swap | 875/875 | ok |
| deribit | 875/875 | ok |
| dydx | 875/875 | ok |
| gate | 875/875 | ok |
| hl_predicted_fundings | 875/875 | ok |
| htx | 873/875 | ok |
| hyperliquid | 875/875 | ok |
| kraken | 871/875 | ok |
| kucoin | 875/875 | ok |
| okx_BTC-USD-SWAP | 875/875 | ok |
| okx_BTC-USDT-SWAP | 875/875 | ok |
| paradex | 875/875 | ok |
| premium_parts | 875/875 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-22 00:00Z | 358 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-22 00:00Z | 358 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-22 00:00Z | 1446 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-22 00:50Z | 17355 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-22 00:00Z | 1444 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-22 00:50Z | 17339 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-21 23:00Z | 1446 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-22 00:50Z | 17355 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-22 00:00Z | 1446 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-22 00:50Z | 17355 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-22 00:00Z | 1446 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-22 00:50Z | 17354 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-21 23:00Z | 3582 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-21 23:00Z | 1421 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-22 00:00Z | 366 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-21 23:00Z | 3581 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-21 23:00Z | 3581 | 0 | 0 |

## 3. Forced-flow retention and revision
47542 distinct liquidation observations; 34 retained boundary probes.
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 8.2%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 875 stored snapshots in 168 distinct hours from 2026-10-15 01:42Z to 2026-10-22 00:57Z; latest 757 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 875 stored snapshots in 168 distinct hours from 2026-10-15 01:42Z to 2026-10-22 00:57Z; latest 24 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10044 bars 2026-10-15 01:33Z → 2026-10-22 00:56Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10044 bars 2026-10-15 01:33Z → 2026-10-22 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10044 bars 2026-10-15 01:33Z → 2026-10-22 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10044 bars 2026-10-15 01:33Z → 2026-10-22 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10044 bars 2026-10-15 01:33Z → 2026-10-22 00:56Z; 0 missing minutes inside the span.
- Deribit options schema 2: 875 runs; latest 757 with OI, 145 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 875 snapshots; account checks by state ok_btc 18999, ok_flat 129541, ok_other 17710; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 271, ledger ok 1146, twap not_attempted 2, twap ok 7331.
- OKX insurance fund rows: regular_update 875.
- Research lab: 28 runs in window; latest 2026-10-22 01:14Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 2/875 routine run(s), 2026-10-15 01:45Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/875 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/875 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/875 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/875 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 4/875 routine run(s), 2026-10-15 07:01Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
