# JBM desk report — 2026-10-12 01:08Z
Window 2026-10-05 01:08Z → 2026-10-12 01:08Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-12 01:08Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-12 00:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-12 01:01Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-12 00:59Z | 9 min |
| snapshots | 2026-10-12 00:58Z | 10 min |
| 1-minute prices (BTC perp) | 2026-10-12 00:59Z | 9 min |
| Deribit options | 2026-10-12 00:58Z | 10 min |
| Hyperliquid account sample | 2026-10-12 00:59Z | 9 min |
| Hyperliquid enrichment | 2026-10-12 00:59Z | 9 min |
| OKX insurance fund | 2026-10-12 00:59Z | 9 min |
| OKX liquidation orders | 2026-10-12 00:58Z | 10 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-12 01:01Z | 8 min |

## 1. Collection health
1144 routine runs in window, by trigger: schedule 595, workflow_dispatch 549.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-05 01:08Z → 2026-10-12 01:08Z | `7,22,37,52 * * * *` | 670 | 595 (89%) | 660/671 slot intervals | 6/1144 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.7, p90 22.2, max 172.4.
Actual interval between stored snapshots, all triggers (min): median 8.6, p90 14.7, max 172.4.
Runtime per routine run (s): median 104, p90 113, max 276; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1144 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 1144/1144 | ok |
| binance_BTCUSDC | 1144/1144 | ok |
| binance_BTCUSDT | 1144/1144 | ok |
| binance_BTCUSD_PERP | 1144/1144 | ok |
| binance_coinm_prem | 1144/1144 | ok |
| binance_usdc_prem | 1144/1144 | ok |
| binance_usdt_prem | 1144/1144 | ok |
| bingx | 1144/1144 | ok |
| bitfinex_margin | 1144/1144 | ok |
| bitget_USDC | 1144/1144 | ok |
| bitget_USDT | 1144/1144 | ok |
| cross_binance_ETHUSDT | 1144/1144 | ok |
| cross_binance_SOLUSDT | 1144/1144 | ok |
| cross_hl_ETH | 1143/1144 | ok |
| cross_hl_SOL | 1143/1144 | ok |
| depth_binance_usdt | 1144/1144 | ok |
| depth_okx_usdt_swap | 1143/1144 | ok |
| deribit | 1144/1144 | ok |
| dydx | 1144/1144 | ok |
| gate | 1144/1144 | ok |
| hl_predicted_fundings | 1143/1144 | ok |
| htx | 1141/1144 | ok |
| hyperliquid | 1143/1144 | ok |
| kraken | 1143/1144 | ok |
| kucoin | 1144/1144 | ok |
| okx_BTC-USD-SWAP | 1143/1144 | ok |
| okx_BTC-USDT-SWAP | 1143/1144 | ok |
| paradex | 1144/1144 | ok |
| premium_parts | 1143/1144 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-12 00:00Z | 328 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-12 00:00Z | 328 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-12 00:00Z | 1206 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-12 00:50Z | 14475 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-12 00:00Z | 1206 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-12 00:50Z | 14475 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-11 23:00Z | 1206 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-12 00:50Z | 14475 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-12 00:00Z | 1206 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-12 00:50Z | 14475 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-12 00:00Z | 1206 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-12 00:50Z | 14474 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-11 23:00Z | 3342 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-11 23:00Z | 1181 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-12 00:00Z | 336 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-11 23:00Z | 3341 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-11 23:00Z | 3341 | 0 | 0 |

## 3. Forced-flow retention and revision
30864 distinct liquidation observations; 24 retained boundary probes.
- 2026-10-08 00:12Z: 0.95 days, 24 pages (observed source boundary).
- 2026-10-09 00:13Z: 0.93 days, 35 pages (observed source boundary).
- 2026-10-10 00:12Z: 0.95 days, 14 pages (observed source boundary).
- 2026-10-11 00:12Z: 0.99 days, 4 pages (observed source boundary).
- 2026-10-12 00:12Z: 0.94 days, 9 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 10.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 1144 stored snapshots in 166 distinct hours from 2026-10-05 01:12Z to 2026-10-12 00:57Z; latest 753 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 1144 stored snapshots in 166 distinct hours from 2026-10-05 01:12Z to 2026-10-12 00:57Z; latest 17 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10068 bars 2026-10-05 01:09Z → 2026-10-12 00:56Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10068 bars 2026-10-05 01:09Z → 2026-10-12 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10068 bars 2026-10-05 01:09Z → 2026-10-12 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10068 bars 2026-10-05 01:09Z → 2026-10-12 00:56Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10068 bars 2026-10-05 01:09Z → 2026-10-12 00:56Z; 0 missing minutes inside the span.
- Deribit options schema 2: 1144 runs; latest 753 with OI, 181 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 166.
- Hyperliquid sample v2: 1144 snapshots; account checks by state failed 5, ok_btc 25124, ok_flat 168601, ok_other 23630; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 301, ledger ok 1445, twap not_attempted 1, twap ok 9693.
- OKX insurance fund rows: regular_update 1144.
- Research lab: 27 runs in window; latest 2026-10-12 01:01Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-12.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.94 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot hyperliquid: 1/1144 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/1144 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/1144 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/1144 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- forward book hl_positions: 1/1144 routine run(s), 2026-10-10 08:17Z; latest: degraded: 5/190 accounts failed, malformed or not attempted; absent from the latest run
- snapshot htx: 3/1144 routine run(s), 2026-10-05 06:56Z → 2026-10-10 00:42Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 1/1144 routine run(s), 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot okx_BTC-USD-SWAP: 1/1144 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot okx_BTC-USDT-SWAP: 1/1144 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: URLError: <urlopen error [Errno 104] Connection reset by peer>; deadline reached; absent from the latest run
- snapshot depth_okx_usdt_swap: 1/1144 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot premium_parts: 1/1144 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
