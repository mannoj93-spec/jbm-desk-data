# JBM desk report — 2026-10-21 07:32Z
Window 2026-10-14 07:32Z → 2026-10-21 07:32Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-21 07:32Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-21 07:14Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-21 07:22Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-21 07:14Z | 17 min |
| snapshots | 2026-10-21 07:13Z | 18 min |
| 1-minute prices (BTC perp) | 2026-10-21 07:14Z | 17 min |
| Deribit options | 2026-10-21 07:13Z | 18 min |
| Hyperliquid account sample | 2026-10-21 07:14Z | 17 min |
| Hyperliquid enrichment | 2026-10-21 07:14Z | 17 min |
| OKX insurance fund | 2026-10-21 07:14Z | 17 min |
| OKX liquidation orders | 2026-10-21 05:58Z | 94 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-21 07:22Z | 9 min |

## 1. Collection health
878 routine runs in window, by trigger: schedule 329, workflow_dispatch 549.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-14 07:32Z → 2026-10-21 07:32Z | `7,22,37,52 * * * *` | 671 | 329 (49%) | 668/670 slot intervals; 1 not yet assessed (after the input cutoff) | 7/878 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-21 07:12Z; report clock 2026-10-21 07:32Z: wall-clock lag 19 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 30.0, p90 38.9, max 74.9.
Actual interval between stored snapshots, all triggers (min): median 12.3, p90 16.5, max 30.0.
Runtime per routine run (s): median 105, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 878 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 878/878 | ok |
| binance_BTCUSDC | 878/878 | ok |
| binance_BTCUSDT | 878/878 | ok |
| binance_BTCUSD_PERP | 878/878 | ok |
| binance_coinm_prem | 878/878 | ok |
| binance_usdc_prem | 878/878 | ok |
| binance_usdt_prem | 878/878 | ok |
| bingx | 878/878 | ok |
| bitfinex_margin | 878/878 | ok |
| bitget_USDC | 878/878 | ok |
| bitget_USDT | 878/878 | ok |
| cross_binance_ETHUSDT | 878/878 | ok |
| cross_binance_SOLUSDT | 878/878 | ok |
| cross_hl_ETH | 878/878 | ok |
| cross_hl_SOL | 878/878 | ok |
| depth_binance_usdt | 878/878 | ok |
| depth_okx_usdt_swap | 878/878 | ok |
| deribit | 878/878 | ok |
| dydx | 878/878 | ok |
| gate | 878/878 | ok |
| hl_predicted_fundings | 878/878 | ok |
| htx | 875/878 | ok |
| hyperliquid | 878/878 | ok |
| kraken | 874/878 | ok |
| kucoin | 878/878 | ok |
| okx_BTC-USD-SWAP | 878/878 | ok |
| okx_BTC-USDT-SWAP | 878/878 | ok |
| paradex | 878/878 | ok |
| premium_parts | 878/878 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-21 00:00Z | 355 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-21 00:00Z | 355 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-21 07:00Z | 1429 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-21 07:05Z | 17142 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-21 07:00Z | 1427 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-21 07:05Z | 17126 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-21 06:00Z | 1429 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-21 07:05Z | 17142 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-21 07:00Z | 1429 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-21 07:05Z | 17142 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-21 07:00Z | 1429 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-21 07:05Z | 17141 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-21 06:00Z | 3565 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-21 06:00Z | 1404 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-21 00:00Z | 363 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-21 06:00Z | 3564 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-21 06:00Z | 3564 | 0 | 0 |

## 3. Forced-flow retention and revision
45944 distinct liquidation observations; 33 retained boundary probes.
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 878 stored snapshots in 169 distinct hours from 2026-10-14 07:38Z to 2026-10-21 07:12Z; latest 743 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 878 stored snapshots in 169 distinct hours from 2026-10-14 07:38Z to 2026-10-21 07:12Z; latest 21 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10059 bars 2026-10-14 07:33Z → 2026-10-21 07:11Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10059 bars 2026-10-14 07:33Z → 2026-10-21 07:11Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10059 bars 2026-10-14 07:33Z → 2026-10-21 07:11Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10059 bars 2026-10-14 07:33Z → 2026-10-21 07:11Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10059 bars 2026-10-14 07:33Z → 2026-10-21 07:11Z; 0 missing minutes inside the span.
- Deribit options schema 2: 878 runs; latest 743 with OI, 143 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 878 snapshots; account checks by state ok_btc 19125, ok_flat 129939, ok_other 17756; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 268, ledger ok 1146, twap not_attempted 2, twap ok 7364.
- OKX insurance fund rows: regular_update 878.
- Research lab: 28 runs in window; latest 2026-10-21 07:22Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/878 routine run(s), 2026-10-14 08:50Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/878 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/878 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/878 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/878 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 4/878 routine run(s), 2026-10-15 07:01Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
