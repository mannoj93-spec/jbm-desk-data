# JBM desk report — 2026-10-05 01:01Z
Window 2026-09-28 01:01Z → 2026-10-05 01:01Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-05 01:01Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-05 00:55Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-05 00:56Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-05 00:55Z | 6 min |
| snapshots | 2026-10-05 00:54Z | 7 min |
| 1-minute prices (BTC perp) | 2026-10-05 00:55Z | 6 min |
| Deribit options | 2026-10-05 00:54Z | 7 min |
| Hyperliquid account sample | 2026-10-05 00:55Z | 6 min |
| Hyperliquid enrichment | 2026-10-05 00:55Z | 6 min |
| OKX insurance fund | 2026-10-05 00:55Z | 6 min |
| OKX liquidation orders | 2026-10-05 00:54Z | 7 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-05 00:56Z | 5 min |

## 1. Collection health
524 routine runs in window, by trigger: schedule 509, workflow_dispatch 15.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-28 01:01Z → 2026-10-05 01:01Z | `7,22,37,52 * * * *` | 671 | 509 (76%) | 515/671 slot intervals | 6/524 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.1, p90 22.0, max 413.3.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 21.8, max 413.3.
Runtime per routine run (s): median 105, p90 114, max 130; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 524 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 524/524 | ok |
| binance_BTCUSDC | 524/524 | ok |
| binance_BTCUSDT | 524/524 | ok |
| binance_BTCUSD_PERP | 524/524 | ok |
| binance_coinm_prem | 524/524 | ok |
| binance_usdc_prem | 524/524 | ok |
| binance_usdt_prem | 524/524 | ok |
| bingx | 524/524 | ok |
| bitfinex_margin | 524/524 | ok |
| bitget_USDC | 524/524 | ok |
| bitget_USDT | 524/524 | ok |
| cross_binance_ETHUSDT | 524/524 | ok |
| cross_binance_SOLUSDT | 524/524 | ok |
| cross_hl_ETH | 524/524 | ok |
| cross_hl_SOL | 524/524 | ok |
| depth_binance_usdt | 524/524 | ok |
| depth_okx_usdt_swap | 524/524 | ok |
| deribit | 524/524 | ok |
| dydx | 524/524 | ok |
| gate | 524/524 | ok |
| hl_predicted_fundings | 524/524 | ok |
| htx | 519/524 | ok |
| hyperliquid | 524/524 | ok |
| kraken | 523/524 | ok |
| kucoin | 524/524 | ok |
| okx_BTC-USD-SWAP | 524/524 | ok |
| okx_BTC-USDT-SWAP | 524/524 | ok |
| paradex | 524/524 | ok |
| premium_parts | 524/524 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-05 00:00Z | 307 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-05 00:00Z | 307 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-05 00:00Z | 1038 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-05 00:45Z | 12458 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-05 00:00Z | 1038 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-05 00:45Z | 12458 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-04 23:00Z | 1038 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-05 00:45Z | 12458 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-05 00:00Z | 1038 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-05 00:45Z | 12458 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-05 00:00Z | 1038 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-05 00:45Z | 12457 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-04 23:00Z | 3174 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-04 23:00Z | 1013 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-05 00:00Z | 315 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-04 23:00Z | 3173 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-04 23:00Z | 3173 | 0 | 0 |

## 3. Forced-flow retention and revision
20482 distinct liquidation observations; 17 retained boundary probes.
- 2026-10-01 00:25Z: 0.98 days, 22 pages (observed source boundary).
- 2026-10-02 00:23Z: 0.9 days, 13 pages (observed source boundary).
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
- 2026-10-04 00:14Z: 0.99 days, 3 pages (observed source boundary).
- 2026-10-05 00:12Z: 1.0 days, 11 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 8.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 524 stored snapshots in 146 distinct hours from 2026-09-28 01:15Z to 2026-10-05 00:53Z; latest 812 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 524 stored snapshots in 146 distinct hours from 2026-09-28 01:15Z to 2026-10-05 00:53Z; latest 22 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10071 bars 2026-09-28 01:02Z → 2026-10-05 00:52Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10071 bars 2026-09-28 01:02Z → 2026-10-05 00:52Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10071 bars 2026-09-28 01:02Z → 2026-10-05 00:52Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10071 bars 2026-09-28 01:02Z → 2026-10-05 00:52Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10071 bars 2026-09-28 01:02Z → 2026-10-05 00:52Z; 0 missing minutes inside the span.
- Deribit options schema 2: 524 runs; latest 812 with OI, 188 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata refreshed.
- Deribit hourly quote records: 146.
- Hyperliquid sample v2: 524 snapshots; account checks by state ok_btc 11564, ok_flat 77193, ok_other 10803; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 183, ledger ok 707, twap not_attempted 3, twap ok 4347.
- OKX insurance fund rows: regular_update 524.
- Research lab: 26 runs in window; latest 2026-10-05 00:56Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 5/524 routine run(s), 2026-09-28 05:30Z → 2026-10-03 08:59Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 1/524 routine run(s), 2026-10-01 07:03Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
