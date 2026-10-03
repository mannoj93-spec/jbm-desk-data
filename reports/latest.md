# JBM desk report — 2026-10-03 07:03Z
Window 2026-09-26 07:03Z → 2026-10-03 07:03Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-03 07:03Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-03 07:01Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-10-03 07:01Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-03 07:01Z | 2 min |
| snapshots | 2026-10-03 07:00Z | 3 min |
| 1-minute prices (BTC perp) | 2026-10-03 07:01Z | 3 min |
| Deribit options | 2026-10-03 07:00Z | 3 min |
| Hyperliquid account sample | 2026-10-03 07:01Z | 3 min |
| Hyperliquid enrichment | 2026-10-03 07:01Z | 3 min |
| OKX insurance fund | 2026-10-03 07:01Z | 2 min |
| OKX liquidation orders | 2026-10-03 07:00Z | 3 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-03 07:01Z | 2 min |

## 1. Collection health
639 routine runs in window, by trigger: schedule 639.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-26 07:03Z → 2026-10-03 07:03Z | `7,22,37,52 * * * *` | 671 | 639 (95%) | 637/671 slot intervals | 5/639 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.7, p90 21.1, max 33.8.
Actual interval between stored snapshots, all triggers (min): median 14.7, p90 21.1, max 33.8.
Runtime per routine run (s): median 105, p90 113, max 130; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 639 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 639/639 | ok |
| binance_BTCUSDC | 639/639 | ok |
| binance_BTCUSDT | 639/639 | ok |
| binance_BTCUSD_PERP | 639/639 | ok |
| binance_coinm_prem | 639/639 | ok |
| binance_usdc_prem | 639/639 | ok |
| binance_usdt_prem | 639/639 | ok |
| bingx | 639/639 | ok |
| bitfinex_margin | 639/639 | ok |
| bitget_USDC | 639/639 | ok |
| bitget_USDT | 639/639 | ok |
| cross_binance_ETHUSDT | 639/639 | ok |
| cross_binance_SOLUSDT | 639/639 | ok |
| cross_hl_ETH | 639/639 | ok |
| cross_hl_SOL | 639/639 | ok |
| depth_binance_usdt | 639/639 | ok |
| depth_okx_usdt_swap | 639/639 | ok |
| deribit | 639/639 | ok |
| dydx | 639/639 | ok |
| gate | 639/639 | ok |
| hl_predicted_fundings | 639/639 | ok |
| htx | 635/639 | ok |
| hyperliquid | 639/639 | ok |
| kraken | 638/639 | ok |
| kucoin | 639/639 | ok |
| okx_BTC-USD-SWAP | 639/639 | ok |
| okx_BTC-USDT-SWAP | 639/639 | ok |
| paradex | 639/639 | ok |
| premium_parts | 639/639 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-03 00:00Z | 301 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-03 00:00Z | 301 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-03 06:00Z | 996 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-03 06:50Z | 11955 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-03 06:00Z | 996 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-03 06:50Z | 11955 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-03 05:00Z | 996 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-03 06:50Z | 11955 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-03 06:00Z | 996 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-03 06:50Z | 11955 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-03 06:00Z | 996 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-03 06:50Z | 11954 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-03 05:00Z | 3132 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-03 05:00Z | 971 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-03 00:00Z | 309 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-03 06:00Z | 3132 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-03 06:00Z | 3132 | 0 | 0 |

## 3. Forced-flow retention and revision
19599 distinct liquidation observations; 15 retained boundary probes.
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
- 2026-09-30 00:23Z: 0.98 days, 13 pages (observed source boundary).
- 2026-10-01 00:25Z: 0.98 days, 22 pages (observed source boundary).
- 2026-10-02 00:23Z: 0.9 days, 13 pages (observed source boundary).
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
Observed later revision after first live capture: n=31 active hours; mean 7.4%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 639 stored snapshots in 168 distinct hours from 2026-09-26 07:14Z to 2026-10-03 06:59Z; latest 835 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 639 stored snapshots in 168 distinct hours from 2026-09-26 07:14Z to 2026-10-03 06:59Z; latest 28 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10075 bars 2026-09-26 07:04Z → 2026-10-03 06:58Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10075 bars 2026-09-26 07:04Z → 2026-10-03 06:58Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10075 bars 2026-09-26 07:04Z → 2026-10-03 06:58Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10075 bars 2026-09-26 07:04Z → 2026-10-03 06:58Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10075 bars 2026-09-26 07:04Z → 2026-10-03 06:58Z; 0 missing minutes inside the span.
- Deribit options schema 2: 639 runs; latest 835 with OI, 171 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 639 snapshots; account checks by state ok_btc 14082, ok_flat 94241, ok_other 13087; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 223, ledger ok 862, twap not_attempted 3, twap ok 5302.
- OKX insurance fund rows: regular_update 639.
- Research lab: 28 runs in window; latest 2026-10-03 07:01Z: exploratory 6, under prospective evaluation 2 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.95 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot kraken: 1/639 routine run(s), 2026-10-01 07:03Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot htx: 4/639 routine run(s), 2026-09-28 05:30Z → 2026-09-29 19:44Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
