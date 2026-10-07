# JBM desk report — 2026-10-07 13:00Z
Window 2026-09-30 13:00Z → 2026-10-07 13:00Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-07 13:00Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-07 12:56Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-07 12:58Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-07 12:56Z | 4 min |
| snapshots | 2026-10-07 12:55Z | 5 min |
| 1-minute prices (BTC perp) | 2026-10-07 12:56Z | 4 min |
| Deribit options | 2026-10-07 12:55Z | 5 min |
| Hyperliquid account sample | 2026-10-07 12:56Z | 4 min |
| Hyperliquid enrichment | 2026-10-07 12:56Z | 4 min |
| OKX insurance fund | 2026-10-07 12:56Z | 4 min |
| OKX liquidation orders | 2026-10-07 12:55Z | 5 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-07 12:58Z | 2 min |

## 1. Collection health
687 routine runs in window, by trigger: schedule 483, workflow_dispatch 204.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-30 13:00Z → 2026-10-07 13:00Z | `7,22,37,52 * * * *` | 671 | 483 (72%) | 516/671 slot intervals | 6/687 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.8, p90 23.8, max 413.3.
Actual interval between stored snapshots, all triggers (min): median 11.5, p90 19.4, max 413.3.
Runtime per routine run (s): median 105, p90 112, max 276; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 687 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 687/687 | ok |
| binance_BTCUSDC | 687/687 | ok |
| binance_BTCUSDT | 687/687 | ok |
| binance_BTCUSD_PERP | 687/687 | ok |
| binance_coinm_prem | 687/687 | ok |
| binance_usdc_prem | 687/687 | ok |
| binance_usdt_prem | 687/687 | ok |
| bingx | 687/687 | ok |
| bitfinex_margin | 687/687 | ok |
| bitget_USDC | 687/687 | ok |
| bitget_USDT | 687/687 | ok |
| cross_binance_ETHUSDT | 687/687 | ok |
| cross_binance_SOLUSDT | 687/687 | ok |
| cross_hl_ETH | 687/687 | ok |
| cross_hl_SOL | 687/687 | ok |
| depth_binance_usdt | 687/687 | ok |
| depth_okx_usdt_swap | 686/687 | ok |
| deribit | 687/687 | ok |
| dydx | 687/687 | ok |
| gate | 687/687 | ok |
| hl_predicted_fundings | 687/687 | ok |
| htx | 684/687 | ok |
| hyperliquid | 687/687 | ok |
| kraken | 685/687 | ok |
| kucoin | 687/687 | ok |
| okx_BTC-USD-SWAP | 686/687 | ok |
| okx_BTC-USDT-SWAP | 686/687 | ok |
| paradex | 687/687 | ok |
| premium_parts | 686/687 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-07 08:00Z | 314 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-07 08:00Z | 314 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-07 12:00Z | 1098 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-07 12:45Z | 13178 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-07 12:00Z | 1098 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-07 12:45Z | 13178 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-07 11:00Z | 1098 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-07 12:45Z | 13178 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-07 12:00Z | 1098 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-07 12:45Z | 13178 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-07 12:00Z | 1098 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-07 12:45Z | 13177 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-07 11:00Z | 3234 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-07 11:00Z | 1073 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-07 08:00Z | 322 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-07 11:00Z | 3233 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-07 11:00Z | 3233 | 0 | 0 |

## 3. Forced-flow retention and revision
24198 distinct liquidation observations; 19 retained boundary probes.
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
- 2026-10-04 00:14Z: 0.99 days, 3 pages (observed source boundary).
- 2026-10-05 00:12Z: 1.0 days, 11 pages (observed source boundary).
- 2026-10-06 00:13Z: 0.99 days, 16 pages (observed source boundary).
- 2026-10-07 00:12Z: 0.97 days, 11 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 7.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 687 stored snapshots in 144 distinct hours from 2026-09-30 13:20Z to 2026-10-07 12:54Z; latest 780 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 687 stored snapshots in 144 distinct hours from 2026-09-30 13:20Z to 2026-10-07 12:54Z; latest 24 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10073 bars 2026-09-30 13:01Z → 2026-10-07 12:53Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10073 bars 2026-09-30 13:01Z → 2026-10-07 12:53Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10073 bars 2026-09-30 13:01Z → 2026-10-07 12:53Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10073 bars 2026-09-30 13:01Z → 2026-10-07 12:53Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10073 bars 2026-09-30 13:01Z → 2026-10-07 12:53Z; 0 missing minutes inside the span.
- Deribit options schema 2: 687 runs; latest 780 with OI, 164 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 144.
- Hyperliquid sample v2: 687 snapshots; account checks by state ok_btc 15206, ok_flat 100983, ok_other 14341; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 217, ledger ok 904, twap not_attempted 4, twap ok 5745.
- OKX insurance fund rows: regular_update 687.
- Research lab: 25 runs in window; latest 2026-10-07 12:58Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.97 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/687 routine run(s), 2026-10-03 08:59Z → 2026-10-06 13:50Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 2/687 routine run(s), 2026-10-01 07:03Z → 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot okx_BTC-USD-SWAP: 1/687 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot okx_BTC-USDT-SWAP: 1/687 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: URLError: <urlopen error [Errno 104] Connection reset by peer>; deadline reached; absent from the latest run
- snapshot depth_okx_usdt_swap: 1/687 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot premium_parts: 1/687 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
