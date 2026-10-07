# JBM desk report — 2026-10-07 06:57Z
Window 2026-09-30 06:57Z → 2026-10-07 06:57Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-07 06:57Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-07 06:46Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-07 06:55Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-07 06:46Z | 11 min |
| snapshots | 2026-10-07 06:45Z | 12 min |
| 1-minute prices (BTC perp) | 2026-10-07 06:46Z | 11 min |
| Deribit options | 2026-10-07 06:46Z | 12 min |
| Hyperliquid account sample | 2026-10-07 06:46Z | 11 min |
| Hyperliquid enrichment | 2026-10-07 06:46Z | 11 min |
| OKX insurance fund | 2026-10-07 06:46Z | 11 min |
| OKX liquidation orders | 2026-10-07 06:45Z | 12 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-07 06:55Z | 2 min |

## 1. Collection health
666 routine runs in window, by trigger: schedule 484, workflow_dispatch 182.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-30 06:57Z → 2026-10-07 06:57Z | `7,22,37,52 * * * *` | 671 | 484 (72%) | 514/671 slot intervals | 6/666 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.6, p90 23.9, max 413.3.
Actual interval between stored snapshots, all triggers (min): median 11.8, p90 19.6, max 413.3.
Runtime per routine run (s): median 105, p90 112, max 276; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 666 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 666/666 | ok |
| binance_BTCUSDC | 666/666 | ok |
| binance_BTCUSDT | 666/666 | ok |
| binance_BTCUSD_PERP | 666/666 | ok |
| binance_coinm_prem | 666/666 | ok |
| binance_usdc_prem | 666/666 | ok |
| binance_usdt_prem | 666/666 | ok |
| bingx | 666/666 | ok |
| bitfinex_margin | 666/666 | ok |
| bitget_USDC | 666/666 | ok |
| bitget_USDT | 666/666 | ok |
| cross_binance_ETHUSDT | 666/666 | ok |
| cross_binance_SOLUSDT | 666/666 | ok |
| cross_hl_ETH | 666/666 | ok |
| cross_hl_SOL | 666/666 | ok |
| depth_binance_usdt | 666/666 | ok |
| depth_okx_usdt_swap | 665/666 | ok |
| deribit | 666/666 | ok |
| dydx | 666/666 | ok |
| gate | 666/666 | ok |
| hl_predicted_fundings | 666/666 | ok |
| htx | 663/666 | ok |
| hyperliquid | 666/666 | ok |
| kraken | 664/666 | ok |
| kucoin | 666/666 | ok |
| okx_BTC-USD-SWAP | 665/666 | ok |
| okx_BTC-USDT-SWAP | 665/666 | ok |
| paradex | 666/666 | ok |
| premium_parts | 665/666 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-07 00:00Z | 313 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-07 00:00Z | 313 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-07 06:00Z | 1092 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-07 06:40Z | 13105 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-07 06:00Z | 1092 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-07 06:40Z | 13105 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-07 05:00Z | 1092 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-07 06:35Z | 13104 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-07 06:00Z | 1092 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-07 06:40Z | 13105 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-07 06:00Z | 1092 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-07 06:40Z | 13104 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-07 05:00Z | 3228 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-07 05:00Z | 1067 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-07 00:00Z | 321 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-07 05:00Z | 3227 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-07 05:00Z | 3227 | 0 | 0 |

## 3. Forced-flow retention and revision
23872 distinct liquidation observations; 19 retained boundary probes.
- 2026-10-03 00:21Z: 0.95 days, 31 pages (observed source boundary).
- 2026-10-04 00:14Z: 0.99 days, 3 pages (observed source boundary).
- 2026-10-05 00:12Z: 1.0 days, 11 pages (observed source boundary).
- 2026-10-06 00:13Z: 0.99 days, 16 pages (observed source boundary).
- 2026-10-07 00:12Z: 0.97 days, 11 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 7.9%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 666 stored snapshots in 144 distinct hours from 2026-09-30 07:00Z to 2026-10-07 06:45Z; latest 788 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 666 stored snapshots in 144 distinct hours from 2026-09-30 07:00Z to 2026-10-07 06:45Z; latest 23 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10067 bars 2026-09-30 06:58Z → 2026-10-07 06:44Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10067 bars 2026-09-30 06:58Z → 2026-10-07 06:44Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10067 bars 2026-09-30 06:58Z → 2026-10-07 06:44Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10067 bars 2026-09-30 06:58Z → 2026-10-07 06:44Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10067 bars 2026-09-30 06:58Z → 2026-10-07 06:44Z; 0 missing minutes inside the span.
- Deribit options schema 2: 666 runs; latest 788 with OI, 158 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 144.
- Hyperliquid sample v2: 666 snapshots; account checks by state ok_btc 14724, ok_flat 97890, ok_other 13926; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 208, ledger ok 874, twap not_attempted 4, twap ok 5574.
- OKX insurance fund rows: regular_update 666.
- Research lab: 25 runs in window; latest 2026-10-07 06:55Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.97 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/666 routine run(s), 2026-10-03 08:59Z → 2026-10-06 13:50Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 2/666 routine run(s), 2026-10-01 07:03Z → 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot okx_BTC-USD-SWAP: 1/666 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot okx_BTC-USDT-SWAP: 1/666 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: URLError: <urlopen error [Errno 104] Connection reset by peer>; deadline reached; absent from the latest run
- snapshot depth_okx_usdt_swap: 1/666 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot premium_parts: 1/666 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
