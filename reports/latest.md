# JBM desk report — 2026-10-07 18:57Z
Window 2026-09-30 18:57Z → 2026-10-07 18:57Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-07 18:57Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-07 18:43Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-07 18:55Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-07 18:43Z | 14 min |
| snapshots | 2026-10-07 18:42Z | 15 min |
| 1-minute prices (BTC perp) | 2026-10-07 18:43Z | 14 min |
| Deribit options | 2026-10-07 18:42Z | 15 min |
| Hyperliquid account sample | 2026-10-07 18:43Z | 14 min |
| Hyperliquid enrichment | 2026-10-07 18:43Z | 14 min |
| OKX insurance fund | 2026-10-07 18:43Z | 14 min |
| OKX liquidation orders | 2026-10-07 17:50Z | 67 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-07 18:55Z | 2 min |

## 1. Collection health
702 routine runs in window, by trigger: schedule 480, workflow_dispatch 222.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-30 18:57Z → 2026-10-07 18:57Z | `7,22,37,52 * * * *` | 671 | 480 (72%) | 518/671 slot intervals | 6/702 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.8, p90 23.9, max 413.3.
Actual interval between stored snapshots, all triggers (min): median 11.1, p90 19.1, max 413.3.
Runtime per routine run (s): median 105, p90 112, max 276; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 702 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 702/702 | ok |
| binance_BTCUSDC | 702/702 | ok |
| binance_BTCUSDT | 702/702 | ok |
| binance_BTCUSD_PERP | 702/702 | ok |
| binance_coinm_prem | 702/702 | ok |
| binance_usdc_prem | 702/702 | ok |
| binance_usdt_prem | 702/702 | ok |
| bingx | 702/702 | ok |
| bitfinex_margin | 702/702 | ok |
| bitget_USDC | 702/702 | ok |
| bitget_USDT | 702/702 | ok |
| cross_binance_ETHUSDT | 702/702 | ok |
| cross_binance_SOLUSDT | 702/702 | ok |
| cross_hl_ETH | 702/702 | ok |
| cross_hl_SOL | 702/702 | ok |
| depth_binance_usdt | 702/702 | ok |
| depth_okx_usdt_swap | 701/702 | ok |
| deribit | 702/702 | ok |
| dydx | 702/702 | ok |
| gate | 702/702 | ok |
| hl_predicted_fundings | 702/702 | ok |
| htx | 699/702 | ok |
| hyperliquid | 702/702 | ok |
| kraken | 700/702 | ok |
| kucoin | 702/702 | ok |
| okx_BTC-USD-SWAP | 701/702 | ok |
| okx_BTC-USDT-SWAP | 701/702 | ok |
| paradex | 702/702 | ok |
| premium_parts | 701/702 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-07 16:00Z | 315 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-07 16:00Z | 315 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-07 18:00Z | 1104 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-07 18:35Z | 13248 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-07 18:00Z | 1104 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-07 18:35Z | 13248 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-07 17:00Z | 1104 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-07 18:35Z | 13248 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-07 18:00Z | 1104 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-07 18:35Z | 13248 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-07 18:00Z | 1104 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-07 18:35Z | 13247 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-07 17:00Z | 3240 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-07 17:00Z | 1079 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-07 16:00Z | 323 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-07 17:00Z | 3239 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-07 17:00Z | 3239 | 0 | 0 |

## 3. Forced-flow retention and revision
25083 distinct liquidation observations; 19 retained boundary probes.
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
- 2026-10-04 00:14Z: 0.99 days, 3 pages (observed source boundary).
- 2026-10-05 00:12Z: 1.0 days, 11 pages (observed source boundary).
- 2026-10-06 00:13Z: 0.99 days, 16 pages (observed source boundary).
- 2026-10-07 00:12Z: 0.97 days, 11 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 8.2%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 702 stored snapshots in 144 distinct hours from 2026-09-30 19:17Z to 2026-10-07 18:41Z; latest 791 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 702 stored snapshots in 144 distinct hours from 2026-09-30 19:17Z to 2026-10-07 18:41Z; latest 21 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10063 bars 2026-09-30 18:58Z → 2026-10-07 18:40Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10063 bars 2026-09-30 18:58Z → 2026-10-07 18:40Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10063 bars 2026-09-30 18:58Z → 2026-10-07 18:40Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10063 bars 2026-09-30 18:58Z → 2026-10-07 18:40Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10063 bars 2026-09-30 18:58Z → 2026-10-07 18:40Z; 0 missing minutes inside the span.
- Deribit options schema 2: 702 runs; latest 791 with OI, 159 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 144.
- Hyperliquid sample v2: 702 snapshots; account checks by state ok_btc 15549, ok_flat 103173, ok_other 14658; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 219, ledger ok 921, twap not_attempted 1, twap ok 5879.
- OKX insurance fund rows: regular_update 702.
- Research lab: 25 runs in window; latest 2026-10-07 18:55Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.97 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/702 routine run(s), 2026-10-03 08:59Z → 2026-10-06 13:50Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 2/702 routine run(s), 2026-10-01 07:03Z → 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot okx_BTC-USD-SWAP: 1/702 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot okx_BTC-USDT-SWAP: 1/702 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: URLError: <urlopen error [Errno 104] Connection reset by peer>; deadline reached; absent from the latest run
- snapshot depth_okx_usdt_swap: 1/702 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot premium_parts: 1/702 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
