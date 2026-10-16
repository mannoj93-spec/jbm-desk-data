# JBM desk report — 2026-10-16 19:20Z
Window 2026-10-09 19:20Z → 2026-10-16 19:20Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-16 19:20Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-16 18:54Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-16 19:07Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-16 18:54Z | 25 min |
| snapshots | 2026-10-16 18:53Z | 26 min |
| 1-minute prices (BTC perp) | 2026-10-16 18:54Z | 26 min |
| Deribit options | 2026-10-16 18:53Z | 26 min |
| Hyperliquid account sample | 2026-10-16 18:54Z | 26 min |
| Hyperliquid enrichment | 2026-10-16 18:54Z | 26 min |
| OKX insurance fund | 2026-10-16 18:54Z | 25 min |
| OKX liquidation orders | 2026-10-16 18:53Z | 27 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-16 19:07Z | 12 min |

## 1. Collection health
1015 routine runs in window, by trigger: schedule 459, workflow_dispatch 556.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-09 19:20Z → 2026-10-16 19:20Z | `7,22,37,52 * * * *` | 671 | 459 (68%) | 671/671 slot intervals | 14/1015 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 19.1, p90 34.4, max 56.7.
Actual interval between stored snapshots, all triggers (min): median 10.4, p90 15.5, max 20.5.
Runtime per routine run (s): median 105, p90 115, max 237; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1015 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 1015/1015 | ok |
| binance_BTCUSDC | 1015/1015 | ok |
| binance_BTCUSDT | 1015/1015 | ok |
| binance_BTCUSD_PERP | 1015/1015 | ok |
| binance_coinm_prem | 1015/1015 | ok |
| binance_usdc_prem | 1015/1015 | ok |
| binance_usdt_prem | 1015/1015 | ok |
| bingx | 1015/1015 | ok |
| bitfinex_margin | 1015/1015 | ok |
| bitget_USDC | 1015/1015 | ok |
| bitget_USDT | 1015/1015 | ok |
| cross_binance_ETHUSDT | 1015/1015 | ok |
| cross_binance_SOLUSDT | 1015/1015 | ok |
| cross_hl_ETH | 1014/1015 | ok |
| cross_hl_SOL | 1014/1015 | ok |
| depth_binance_usdt | 1015/1015 | ok |
| depth_okx_usdt_swap | 1015/1015 | ok |
| deribit | 1012/1015 | ok |
| dydx | 1015/1015 | ok |
| gate | 1015/1015 | ok |
| hl_predicted_fundings | 1014/1015 | ok |
| htx | 1011/1015 | ok |
| hyperliquid | 1014/1015 | ok |
| kraken | 1009/1015 | ok |
| kucoin | 1015/1015 | ok |
| okx_BTC-USD-SWAP | 1015/1015 | ok |
| okx_BTC-USDT-SWAP | 1015/1015 | ok |
| paradex | 1015/1015 | ok |
| premium_parts | 1015/1015 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-16 16:00Z | 342 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-16 16:00Z | 342 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-16 18:00Z | 1320 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-16 18:45Z | 15842 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-16 18:00Z | 1318 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-16 18:45Z | 15826 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-16 17:00Z | 1320 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-16 18:45Z | 15842 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-16 18:00Z | 1320 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-16 18:45Z | 15842 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-16 18:00Z | 1320 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-16 18:45Z | 15841 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-16 17:00Z | 3456 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-16 17:00Z | 1295 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-16 16:00Z | 350 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-16 17:00Z | 3455 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-16 17:00Z | 3455 | 0 | 0 |

## 3. Forced-flow retention and revision
41559 distinct liquidation observations; 28 retained boundary probes.
- 2026-10-12 00:12Z: 0.94 days, 9 pages (observed source boundary).
- 2026-10-13 00:00Z: 0.98 days, 23 pages (observed source boundary).
- 2026-10-14 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-15 00:12Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-16 00:12Z: 0.97 days, 36 pages (observed source boundary).
Observed later revision after first live capture: n=25 active hours; mean 7.6%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 1012 stored snapshots in 168 distinct hours from 2026-10-09 19:27Z to 2026-10-16 18:52Z; latest 772 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 1015 stored snapshots in 168 distinct hours from 2026-10-09 19:27Z to 2026-10-16 18:52Z; latest 22 BTC positions in top 190; 2 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10051 bars 2026-10-09 19:21Z → 2026-10-16 18:51Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10051 bars 2026-10-09 19:21Z → 2026-10-16 18:51Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10051 bars 2026-10-09 19:21Z → 2026-10-16 18:51Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10051 bars 2026-10-09 19:21Z → 2026-10-16 18:51Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10051 bars 2026-10-09 19:21Z → 2026-10-16 18:51Z; 0 missing minutes inside the span.
- Deribit options schema 2: 1012 runs; latest 772 with OI, 170 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 1015 snapshots; account checks by state failed 6, ok_btc 21830, ok_flat 150013, ok_other 21001; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 302, ledger ok 1317, twap not_attempted 9, twap ok 8522.
- OKX insurance fund rows: regular_update 1015.
- Research lab: 28 runs in window; latest 2026-10-16 19:07Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-12.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.97 days. This is not a guarantee of future availability.

## 7. Alerts
- run gap_binance_openInterestHist_5m: 2/1015 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/1015 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/1015 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/1015 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 6/1015 routine run(s), 2026-10-13 07:00Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot htx: 4/1015 routine run(s), 2026-10-10 00:42Z → 2026-10-15 01:45Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- forward book hl_positions: 2/1015 routine run(s), 2026-10-10 08:17Z → 2026-10-14 01:12Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- history deribit_dvol_1h: 3/1015 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/1015 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/1015 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- snapshot hyperliquid: 1/1015 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/1015 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/1015 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/1015 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
