# JBM desk report — 2026-10-19 13:38Z
Window 2026-10-12 13:38Z → 2026-10-19 13:38Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-19 13:38Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-19 13:14Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-19 13:21Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-19 13:14Z | 24 min |
| snapshots | 2026-10-19 13:13Z | 25 min |
| 1-minute prices (BTC perp) | 2026-10-19 13:14Z | 24 min |
| Deribit options | 2026-10-19 13:13Z | 25 min |
| Hyperliquid account sample | 2026-10-19 13:14Z | 24 min |
| Hyperliquid enrichment | 2026-10-19 13:14Z | 24 min |
| OKX insurance fund | 2026-10-19 13:14Z | 24 min |
| OKX liquidation orders | 2026-10-19 13:13Z | 25 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-19 13:21Z | 17 min |

## 1. Collection health
896 routine runs in window, by trigger: schedule 362, workflow_dispatch 534.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-12 13:38Z → 2026-10-19 13:38Z | `7,22,37,52 * * * *` | 670 | 362 (54%) | 670/671 slot intervals | 13/896 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 27.4, p90 37.1, max 56.7.
Actual interval between stored snapshots, all triggers (min): median 11.9, p90 17.0, max 20.6.
Runtime per routine run (s): median 106, p90 115, max 171; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 896 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 896/896 | ok |
| binance_BTCUSDC | 896/896 | ok |
| binance_BTCUSDT | 896/896 | ok |
| binance_BTCUSD_PERP | 896/896 | ok |
| binance_coinm_prem | 896/896 | ok |
| binance_usdc_prem | 896/896 | ok |
| binance_usdt_prem | 896/896 | ok |
| bingx | 896/896 | ok |
| bitfinex_margin | 896/896 | ok |
| bitget_USDC | 896/896 | ok |
| bitget_USDT | 896/896 | ok |
| cross_binance_ETHUSDT | 896/896 | ok |
| cross_binance_SOLUSDT | 896/896 | ok |
| cross_hl_ETH | 896/896 | ok |
| cross_hl_SOL | 896/896 | ok |
| depth_binance_usdt | 896/896 | ok |
| depth_okx_usdt_swap | 896/896 | ok |
| deribit | 893/896 | ok |
| dydx | 896/896 | ok |
| gate | 896/896 | ok |
| hl_predicted_fundings | 896/896 | ok |
| htx | 892/896 | ok |
| hyperliquid | 896/896 | ok |
| kraken | 890/896 | ok |
| kucoin | 896/896 | ok |
| okx_BTC-USD-SWAP | 896/896 | ok |
| okx_BTC-USDT-SWAP | 896/896 | ok |
| paradex | 896/896 | ok |
| premium_parts | 896/896 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-19 08:00Z | 350 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-19 08:00Z | 350 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-19 13:00Z | 1387 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-19 13:05Z | 16638 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-19 13:00Z | 1385 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-19 13:05Z | 16622 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-19 12:00Z | 1387 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-19 13:05Z | 16638 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-19 13:00Z | 1387 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-19 13:05Z | 16638 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-19 13:00Z | 1387 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-19 13:05Z | 16637 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-19 12:00Z | 3523 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-19 12:00Z | 1362 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-19 08:00Z | 358 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-19 12:00Z | 3522 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-19 12:00Z | 3522 | 0 | 0 |

## 3. Forced-flow retention and revision
43957 distinct liquidation observations; 31 retained boundary probes.
- 2026-10-15 00:12Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-16 00:12Z: 0.97 days, 36 pages (observed source boundary).
- 2026-10-17 00:01Z: 0.99 days, 18 pages (observed source boundary).
- 2026-10-18 00:00Z: 0.96 days, 7 pages (observed source boundary).
- 2026-10-19 00:02Z: 0.99 days, 14 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.8%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 893 stored snapshots in 169 distinct hours from 2026-10-12 13:42Z to 2026-10-19 13:12Z; latest 730 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 896 stored snapshots in 169 distinct hours from 2026-10-12 13:42Z to 2026-10-19 13:12Z; latest 23 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10053 bars 2026-10-12 13:39Z → 2026-10-19 13:11Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10053 bars 2026-10-12 13:39Z → 2026-10-19 13:11Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10053 bars 2026-10-12 13:39Z → 2026-10-19 13:11Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10053 bars 2026-10-12 13:39Z → 2026-10-19 13:11Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10053 bars 2026-10-12 13:39Z → 2026-10-19 13:11Z; 0 missing minutes inside the span.
- Deribit options schema 2: 893 runs; latest 730 with OI, 152 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 896 snapshots; account checks by state failed 1, ok_btc 19447, ok_flat 132491, ok_other 18301; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 274, ledger ok 1170, twap not_attempted 9, twap ok 7507.
- OKX insurance fund rows: regular_update 896.
- Research lab: 28 runs in window; latest 2026-10-19 13:21Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 4/896 routine run(s), 2026-10-12 21:27Z → 2026-10-16 22:00Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- run gap_binance_openInterestHist_5m: 2/896 routine run(s), 2026-10-15 13:29Z → 2026-10-15 16:57Z; latest: 9 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_5m: 17/896 routine run(s), 2026-10-15 13:00Z → 2026-10-15 16:42Z; latest: misaligned history timestamp; absent from the latest run
- run gap_binance_openInterestHist_1h: 1/896 routine run(s), 2026-10-15 15:12Z; latest: 2 absent intervals in source response; retained rows, review report and retry --backfill; absent from the latest run
- history binance_openInterestHist_1h: 6/896 routine run(s), 2026-10-15 14:12Z → 2026-10-15 14:57Z; latest: history did not advance despite overdue intervals; absent from the latest run
- snapshot kraken: 6/896 routine run(s), 2026-10-13 07:00Z → 2026-10-15 07:39Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book hl_positions: 1/896 routine run(s), 2026-10-14 01:12Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- history deribit_dvol_1h: 3/896 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: HTTP 503; absent from the latest run
- snapshot deribit: 3/896 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- forward book deribit_options: 3/896 routine run(s), 2026-10-13 09:04Z → 2026-10-13 09:23Z; latest: RuntimeError: HTTP 503; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
