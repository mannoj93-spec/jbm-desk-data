# JBM desk report — 2026-10-10 07:00Z
Window 2026-10-03 07:00Z → 2026-10-10 07:00Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-10 07:00Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-10 06:43Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-10 06:55Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-10 06:43Z | 17 min |
| snapshots | 2026-10-10 06:42Z | 18 min |
| 1-minute prices (BTC perp) | 2026-10-10 06:43Z | 17 min |
| Deribit options | 2026-10-10 06:43Z | 18 min |
| Hyperliquid account sample | 2026-10-10 06:43Z | 17 min |
| Hyperliquid enrichment | 2026-10-10 06:43Z | 17 min |
| OKX insurance fund | 2026-10-10 06:43Z | 17 min |
| OKX liquidation orders | 2026-10-10 06:13Z | 48 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-10 06:55Z | 6 min |

## 1. Collection health
891 routine runs in window, by trigger: schedule 470, workflow_dispatch 421.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-03 07:00Z → 2026-10-10 07:00Z | `7,22,37,52 * * * *` | 671 | 470 (70%) | 535/671 slot intervals | 6/891 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 16.0, p90 24.5, max 413.3.
Actual interval between stored snapshots, all triggers (min): median 8.7, p90 15.7, max 413.3.
Runtime per routine run (s): median 105, p90 113, max 276; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 891 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 891/891 | ok |
| binance_BTCUSDC | 891/891 | ok |
| binance_BTCUSDT | 891/891 | ok |
| binance_BTCUSD_PERP | 891/891 | ok |
| binance_coinm_prem | 891/891 | ok |
| binance_usdc_prem | 891/891 | ok |
| binance_usdt_prem | 891/891 | ok |
| bingx | 891/891 | ok |
| bitfinex_margin | 891/891 | ok |
| bitget_USDC | 891/891 | ok |
| bitget_USDT | 891/891 | ok |
| cross_binance_ETHUSDT | 891/891 | ok |
| cross_binance_SOLUSDT | 891/891 | ok |
| cross_hl_ETH | 891/891 | ok |
| cross_hl_SOL | 891/891 | ok |
| depth_binance_usdt | 891/891 | ok |
| depth_okx_usdt_swap | 890/891 | ok |
| deribit | 891/891 | ok |
| dydx | 891/891 | ok |
| gate | 891/891 | ok |
| hl_predicted_fundings | 891/891 | ok |
| htx | 887/891 | ok |
| hyperliquid | 891/891 | ok |
| kraken | 890/891 | ok |
| kucoin | 891/891 | ok |
| okx_BTC-USD-SWAP | 890/891 | ok |
| okx_BTC-USDT-SWAP | 890/891 | ok |
| paradex | 891/891 | ok |
| premium_parts | 890/891 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-10 00:00Z | 322 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-10 00:00Z | 322 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-10 06:00Z | 1164 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-10 06:35Z | 13968 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-10 06:00Z | 1164 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-10 06:35Z | 13968 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-10 05:00Z | 1164 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-10 06:35Z | 13968 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-10 06:00Z | 1164 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-10 06:35Z | 13968 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-10 06:00Z | 1164 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-10 06:35Z | 13967 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-10 05:00Z | 3300 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-10 05:00Z | 1139 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-10 00:00Z | 330 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-10 05:00Z | 3299 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-10 05:00Z | 3299 | 0 | 0 |

## 3. Forced-flow retention and revision
30047 distinct liquidation observations; 22 retained boundary probes.
- 2026-10-06 00:13Z: 0.99 days, 16 pages (observed source boundary).
- 2026-10-07 00:12Z: 0.97 days, 11 pages (observed source boundary).
- 2026-10-08 00:12Z: 0.95 days, 24 pages (observed source boundary).
- 2026-10-09 00:13Z: 0.93 days, 35 pages (observed source boundary).
- 2026-10-10 00:12Z: 0.95 days, 14 pages (observed source boundary).
Observed later revision after first live capture: n=30 active hours; mean 10.1%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 891 stored snapshots in 144 distinct hours from 2026-10-03 07:18Z to 2026-10-10 06:42Z; latest 783 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 891 stored snapshots in 144 distinct hours from 2026-10-03 07:18Z to 2026-10-10 06:42Z; latest 20 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10061 bars 2026-10-03 07:01Z → 2026-10-10 06:41Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10061 bars 2026-10-03 07:01Z → 2026-10-10 06:41Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10061 bars 2026-10-03 07:01Z → 2026-10-10 06:41Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10061 bars 2026-10-03 07:01Z → 2026-10-10 06:41Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10061 bars 2026-10-03 07:01Z → 2026-10-10 06:41Z; 0 missing minutes inside the span.
- Deribit options schema 2: 891 runs; latest 783 with OI, 167 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 144.
- Hyperliquid sample v2: 891 snapshots; account checks by state ok_btc 19760, ok_flat 131254, ok_other 18276; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 252, ledger ok 1143, twap not_attempted 1, twap ok 7514.
- OKX insurance fund rows: regular_update 891.
- Research lab: 26 runs in window; latest 2026-10-10 06:55Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.95 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 4/891 routine run(s), 2026-10-03 08:59Z → 2026-10-10 00:42Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 1/891 routine run(s), 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot okx_BTC-USD-SWAP: 1/891 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot okx_BTC-USDT-SWAP: 1/891 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: URLError: <urlopen error [Errno 104] Connection reset by peer>; deadline reached; absent from the latest run
- snapshot depth_okx_usdt_swap: 1/891 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot premium_parts: 1/891 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
