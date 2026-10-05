# JBM desk report — 2026-10-05 07:01Z
Window 2026-09-28 07:01Z → 2026-10-05 07:01Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-05 07:01Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-05 06:58Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-05 06:59Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-05 06:58Z | 3 min |
| snapshots | 2026-10-05 06:57Z | 4 min |
| 1-minute prices (BTC perp) | 2026-10-05 06:58Z | 3 min |
| Deribit options | 2026-10-05 06:57Z | 4 min |
| Hyperliquid account sample | 2026-10-05 06:58Z | 3 min |
| Hyperliquid enrichment | 2026-10-05 06:58Z | 3 min |
| OKX insurance fund | 2026-10-05 06:58Z | 3 min |
| OKX liquidation orders | 2026-10-05 06:56Z | 5 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-05 06:59Z | 2 min |

## 1. Collection health
536 routine runs in window, by trigger: schedule 504, workflow_dispatch 32.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-28 07:01Z → 2026-10-05 07:01Z | `7,22,37,52 * * * *` | 671 | 504 (75%) | 516/671 slot intervals | 6/536 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.2, p90 22.7, max 413.3.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 21.5, max 413.3.
Runtime per routine run (s): median 105, p90 113, max 130; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 536 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 536/536 | ok |
| binance_BTCUSDC | 536/536 | ok |
| binance_BTCUSDT | 536/536 | ok |
| binance_BTCUSD_PERP | 536/536 | ok |
| binance_coinm_prem | 536/536 | ok |
| binance_usdc_prem | 536/536 | ok |
| binance_usdt_prem | 536/536 | ok |
| bingx | 536/536 | ok |
| bitfinex_margin | 536/536 | ok |
| bitget_USDC | 536/536 | ok |
| bitget_USDT | 536/536 | ok |
| cross_binance_ETHUSDT | 536/536 | ok |
| cross_binance_SOLUSDT | 536/536 | ok |
| cross_hl_ETH | 536/536 | ok |
| cross_hl_SOL | 536/536 | ok |
| depth_binance_usdt | 536/536 | ok |
| depth_okx_usdt_swap | 536/536 | ok |
| deribit | 536/536 | ok |
| dydx | 536/536 | ok |
| gate | 536/536 | ok |
| hl_predicted_fundings | 536/536 | ok |
| htx | 531/536 | RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d |
| hyperliquid | 536/536 | ok |
| kraken | 535/536 | ok |
| kucoin | 536/536 | ok |
| okx_BTC-USD-SWAP | 536/536 | ok |
| okx_BTC-USDT-SWAP | 536/536 | ok |
| paradex | 536/536 | ok |
| premium_parts | 536/536 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-05 00:00Z | 307 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-05 00:00Z | 307 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-05 06:00Z | 1044 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-05 06:50Z | 12531 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-05 06:00Z | 1044 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-05 06:50Z | 12531 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-05 05:00Z | 1044 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-05 06:50Z | 12531 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-05 06:00Z | 1044 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-05 06:50Z | 12531 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-05 06:00Z | 1044 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-05 06:50Z | 12530 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-05 05:00Z | 3180 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-05 05:00Z | 1019 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-05 00:00Z | 315 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-05 05:00Z | 3179 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-05 05:00Z | 3179 | 0 | 0 |

## 3. Forced-flow retention and revision
21052 distinct liquidation observations; 17 retained boundary probes.
- 2026-10-01 00:25Z: 0.98 days, 22 pages (observed source boundary).
- 2026-10-02 00:23Z: 0.9 days, 13 pages (observed source boundary).
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
- 2026-10-04 00:14Z: 0.99 days, 3 pages (observed source boundary).
- 2026-10-05 00:12Z: 1.0 days, 11 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 536 stored snapshots in 146 distinct hours from 2026-09-28 07:02Z to 2026-10-05 06:56Z; latest 818 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 536 stored snapshots in 146 distinct hours from 2026-09-28 07:02Z to 2026-10-05 06:56Z; latest 20 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10074 bars 2026-09-28 07:02Z → 2026-10-05 06:55Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10074 bars 2026-09-28 07:02Z → 2026-10-05 06:55Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10074 bars 2026-09-28 07:02Z → 2026-10-05 06:55Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10074 bars 2026-09-28 07:02Z → 2026-10-05 06:55Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10074 bars 2026-09-28 07:02Z → 2026-10-05 06:55Z; 0 missing minutes inside the span.
- Deribit options schema 2: 536 runs; latest 818 with OI, 184 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 146.
- Hyperliquid sample v2: 536 snapshots; account checks by state ok_btc 11826, ok_flat 78918, ok_other 11096; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 193, ledger ok 729, twap not_attempted 3, twap ok 4435.
- OKX insurance fund rows: regular_update 536.
- Research lab: 26 runs in window; latest 2026-10-05 06:59Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 5/536 routine run(s), 2026-09-28 14:35Z → 2026-10-05 06:56Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d
- snapshot kraken: 1/536 routine run(s), 2026-10-01 07:03Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- Latest htx snapshot unavailable: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
