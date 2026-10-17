# JBM desk report — 2026-10-17 13:21Z
Window 2026-10-10 13:21Z → 2026-10-17 13:21Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-17 13:21Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-17 13:05Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-17 13:07Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-17 13:05Z | 15 min |
| snapshots | 2026-10-17 13:05Z | 16 min |
| 1-minute prices (BTC perp) | 2026-10-17 13:05Z | 15 min |
| Deribit options | 2026-10-17 13:05Z | 16 min |
| Hyperliquid account sample | 2026-10-17 13:05Z | 15 min |
| Hyperliquid enrichment | 2026-10-17 13:05Z | 15 min |
| OKX insurance fund | 2026-10-17 13:05Z | 15 min |
| OKX liquidation orders | 2026-10-17 13:04Z | 16 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-17 13:07Z | 13 min |

## 1. Collection health
974 routine runs in window, by trigger: schedule 428, workflow_dispatch 546.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-10 13:21Z → 2026-10-17 13:21Z | `7,22,37,52 * * * *` | 671 | 428 (64%) | 671/671 slot intervals | 13/974 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 22.2, p90 35.4, max 56.7.
Actual interval between stored snapshots, all triggers (min): median 10.9, p90 15.9, max 20.6.
Runtime per routine run (s): median 106, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 974 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 974/974 | ok |
| binance_BTCUSDC | 974/974 | ok |
| binance_BTCUSDT | 974/974 | ok |
| binance_BTCUSD_PERP | 974/974 | ok |
| binance_coinm_prem | 974/974 | ok |
| binance_usdc_prem | 974/974 | ok |
| binance_usdt_prem | 974/974 | ok |
| bingx | 974/974 | ok |
| bitfinex_margin | 974/974 | ok |
| bitget_USDC | 974/974 | ok |
| bitget_USDT | 974/974 | ok |
| cross_binance_ETHUSDT | 974/974 | ok |
| cross_binance_SOLUSDT | 974/974 | ok |
| cross_hl_ETH | 974/974 | ok |
| cross_hl_SOL | 974/974 | ok |
| depth_binance_usdt | 974/974 | ok |
| depth_okx_usdt_swap | 974/974 | ok |
| deribit | 971/974 | ok |
| dydx | 974/974 | ok |
| gate | 974/974 | ok |
| hl_predicted_fundings | 974/974 | ok |
| htx | 970/974 | ok |
| hyperliquid | 974/974 | ok |
| kraken | 968/974 | ok |
| kucoin | 974/974 | ok |
| okx_BTC-USD-SWAP | 974/974 | ok |
| okx_BTC-USDT-SWAP | 974/974 | ok |
| paradex | 974/974 | ok |
| premium_parts | 974/974 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-17 08:00Z | 344 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-17 08:00Z | 344 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-17 12:00Z | 1338 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-17 12:55Z | 16060 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-17 12:00Z | 1336 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-17 12:55Z | 16044 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-17 12:00Z | 1339 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-17 12:55Z | 16060 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-17 12:00Z | 1338 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-17 12:55Z | 16060 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-17 12:00Z | 1338 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-17 12:55Z | 16059 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-17 12:00Z | 3475 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-17 12:00Z | 1314 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-17 08:00Z | 352 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-17 12:00Z | 3474 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-17 12:00Z | 3474 | 0 | 0 |

## 3. Forced-flow retention and revision
41637 distinct liquidation observations; 29 retained boundary probes.
- 2026-10-13 00:00Z: 0.98 days, 23 pages (observed source boundary).
- 2026-10-14 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-15 00:12Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-16 00:12Z: 0.97 days, 36 pages (observed source boundary).
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 7.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 971 stored snapshots in 169 distinct hours from 2026-10-10 13:27Z to 2026-10-17 13:04Z; latest 745 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 974 stored snapshots in 169 distinct hours from 2026-10-10 13:27Z to 2026-10-17 13:04Z; latest 26 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10062 bars 2026-10-10 13:22Z → 2026-10-17 13:03Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10062 bars 2026-10-10 13:22Z → 2026-10-17 13:03Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10062 bars 2026-10-10 13:22Z → 2026-10-17 13:03Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10062 bars 2026-10-10 13:22Z → 2026-10-17 13:03Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10062 bars 2026-10-10 13:22Z → 2026-10-17 13:03Z; 0 missing minutes inside the span.
- Deribit options schema 2: 971 runs; latest 745 with OI, 193 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 974 snapshots; account checks by state failed 1, ok_btc 20985, ok_flat 143955, ok_other 20119; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 286, ledger ok 1260, twap not_attempted 9, twap ok 8185.
- OKX insurance fund rows: regular_update 974.
- Research lab: 28 runs in window; latest 2026-10-17 13:07Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-12.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 4/974 routine run(s), 2026-10-12 21:27Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/974 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/974 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/974 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/974 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 6/974 routine run(s), 2026-10-13 07:00Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book hl_positions: 1/974 routine run(s), 2026-10-14 01:12Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- history deribit_dvol_1h: 3/974 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/974 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/974 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
