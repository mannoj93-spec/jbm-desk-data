# JBM desk report — 2026-11-13 20:03Z
Window 2026-11-06 20:03Z → 2026-11-13 20:03Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-13 20:03Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-13 19:45Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-13 19:59Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-13 19:45Z | 18 min |
| snapshots | 2026-11-13 19:44Z | 19 min |
| 1-minute prices (BTC perp) | 2026-11-13 19:45Z | 18 min |
| Deribit options | 2026-11-13 19:44Z | 19 min |
| Hyperliquid account sample | 2026-11-13 19:45Z | 18 min |
| Hyperliquid enrichment | 2026-11-13 19:45Z | 18 min |
| OKX insurance fund | 2026-11-13 19:45Z | 18 min |
| OKX liquidation orders | 2026-11-13 19:29Z | 34 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-13 19:59Z | 4 min |

## 1. Collection health
680 routine runs in window, by trigger: schedule 28, workflow_dispatch 652.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-11-06 20:03Z → 2026-11-13 20:03Z | `7,22,37,52 * * * *` | 671 | 28 (4%) | 666/670 slot intervals; 1 not yet assessed (after the input cutoff) | 5/680 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-13 19:43Z; report clock 2026-11-13 20:03Z: wall-clock lag 20 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 381.8, p90 460.3, max 630.8.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.2, max 49.6.
Runtime per routine run (s): median 106, p90 115, max 216; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 680 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 680/680 | ok |
| binance_BTCUSDC | 680/680 | ok |
| binance_BTCUSDT | 680/680 | ok |
| binance_BTCUSD_PERP | 680/680 | ok |
| binance_coinm_prem | 680/680 | ok |
| binance_usdc_prem | 680/680 | ok |
| binance_usdt_prem | 680/680 | ok |
| bingx | 680/680 | ok |
| bitfinex_margin | 680/680 | ok |
| bitget_USDC | 680/680 | ok |
| bitget_USDT | 680/680 | ok |
| cross_binance_ETHUSDT | 680/680 | ok |
| cross_binance_SOLUSDT | 680/680 | ok |
| cross_hl_ETH | 679/680 | ok |
| cross_hl_SOL | 679/680 | ok |
| depth_binance_usdt | 680/680 | ok |
| depth_okx_usdt_swap | 680/680 | ok |
| deribit | 678/680 | ok |
| dydx | 680/680 | ok |
| gate | 679/680 | ok |
| hl_predicted_fundings | 679/680 | ok |
| htx | 680/680 | ok |
| hyperliquid | 679/680 | ok |
| kraken | 679/680 | ok |
| kucoin | 680/680 | ok |
| okx_BTC-USD-SWAP | 680/680 | ok |
| okx_BTC-USDT-SWAP | 680/680 | ok |
| paradex | 680/680 | ok |
| premium_parts | 680/680 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-13 16:00Z | 426 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-13 16:00Z | 426 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-13 19:00Z | 1993 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-13 19:35Z | 23916 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-13 19:00Z | 1991 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-13 19:35Z | 23900 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-13 18:00Z | 1993 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-13 19:35Z | 23916 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-13 19:00Z | 1993 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-13 19:35Z | 23916 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-13 19:00Z | 1993 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-13 19:35Z | 23915 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-13 18:00Z | 4129 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-13 18:00Z | 1968 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-13 16:00Z | 434 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-13 18:00Z | 4128 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-13 18:00Z | 4128 | 0 | 0 |

## 3. Forced-flow retention and revision
96263 distinct liquidation observations; 56 retained boundary probes.
- 2026-11-09 00:13Z: 0.62 days, 16 pages (observed source boundary).
- 2026-11-10 00:13Z: 1.0 days, 21 pages (observed source boundary).
- 2026-11-11 00:13Z: 1.0 days, 23 pages (observed source boundary).
- 2026-11-12 00:13Z: 0.99 days, 15 pages (observed source boundary).
- 2026-11-13 00:13Z: 1.0 days, 26 pages (observed source boundary).
Observed later revision after first live capture: n=26 active hours; mean 4.4%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 678 stored snapshots in 168 distinct hours from 2026-11-06 20:13Z to 2026-11-13 19:43Z; latest 808 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 680 stored snapshots in 168 distinct hours from 2026-11-06 20:13Z to 2026-11-13 19:43Z; latest 25 BTC positions in top 190; 2 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10059 bars 2026-11-06 20:04Z → 2026-11-13 19:42Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10059 bars 2026-11-06 20:04Z → 2026-11-13 19:42Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10059 bars 2026-11-06 20:04Z → 2026-11-13 19:42Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10059 bars 2026-11-06 20:04Z → 2026-11-13 19:42Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10059 bars 2026-11-06 20:04Z → 2026-11-13 19:42Z; 0 missing minutes inside the span.
- Deribit options schema 2: 678 runs; latest 808 with OI, 170 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 680 snapshots; account checks by state failed 9, ok_btc 14563, ok_flat 101619, ok_other 13009; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 194, ledger ok 874, twap not_attempted 6, twap ok 5726.
- OKX insurance fund rows: regular_update 680.
- Research lab: 16 runs in window; latest 2026-11-13 19:59Z: exploratory 1, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-11-09.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-11-13 17:37Z, over 90 minutes before this report.
- forward book hl_positions: 2/680 routine run(s), 2026-11-07 23:43Z → 2026-11-12 10:43Z; latest: degraded: 8/190 accounts failed, malformed or not attempted; absent from the latest run
- snapshot hyperliquid: 1/680 routine run(s), 2026-11-12 10:43Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/680 routine run(s), 2026-11-12 10:43Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/680 routine run(s), 2026-11-12 10:43Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/680 routine run(s), 2026-11-12 10:43Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot kraken: 1/680 routine run(s), 2026-11-11 22:28Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot gate: 1/680 routine run(s), 2026-11-11 18:03Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- history deribit_dvol_1h: 2/680 routine run(s), 2026-11-10 09:13Z → 2026-11-10 09:28Z; latest: HTTP 404; absent from the latest run
- snapshot deribit: 2/680 routine run(s), 2026-11-10 09:13Z → 2026-11-10 09:28Z; latest: RuntimeError: HTTP 404; absent from the latest run
- forward book deribit_options: 2/680 routine run(s), 2026-11-10 09:13Z → 2026-11-10 09:28Z; latest: RuntimeError: HTTP 404; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
