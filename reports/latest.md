# JBM desk report — 2026-10-11 13:02Z
Window 2026-10-04 13:02Z → 2026-10-11 13:02Z. report-2.6.1-2026-09-30.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-11 13:02Z by report-2.6.1-2026-09-30 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-11 12:44Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-11 12:55Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-11 12:44Z | 18 min |
| snapshots | 2026-10-11 12:43Z | 19 min |
| 1-minute prices (BTC perp) | 2026-10-11 12:44Z | 19 min |
| Deribit options | 2026-10-11 12:43Z | 19 min |
| Hyperliquid account sample | 2026-10-11 12:44Z | 19 min |
| Hyperliquid enrichment | 2026-10-11 12:44Z | 19 min |
| OKX insurance fund | 2026-10-11 12:44Z | 18 min |
| OKX liquidation orders | 2026-10-11 12:21Z | 41 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-11 12:55Z | 7 min |

## 1. Collection health
1082 routine runs in window, by trigger: schedule 564, workflow_dispatch 518.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-04 13:02Z → 2026-10-11 13:02Z | `7,22,37,52 * * * *` | 671 | 564 (84%) | 631/671 slot intervals | 6/1082 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 15.8, p90 23.0, max 189.2.
Actual interval between stored snapshots, all triggers (min): median 8.7, p90 14.9, max 172.4.
Runtime per routine run (s): median 104, p90 112, max 276; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1082 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 1082/1082 | ok |
| binance_BTCUSDC | 1082/1082 | ok |
| binance_BTCUSDT | 1082/1082 | ok |
| binance_BTCUSD_PERP | 1082/1082 | ok |
| binance_coinm_prem | 1082/1082 | ok |
| binance_usdc_prem | 1082/1082 | ok |
| binance_usdt_prem | 1082/1082 | ok |
| bingx | 1082/1082 | ok |
| bitfinex_margin | 1082/1082 | ok |
| bitget_USDC | 1082/1082 | ok |
| bitget_USDT | 1082/1082 | ok |
| cross_binance_ETHUSDT | 1082/1082 | ok |
| cross_binance_SOLUSDT | 1082/1082 | ok |
| cross_hl_ETH | 1081/1082 | ok |
| cross_hl_SOL | 1081/1082 | ok |
| depth_binance_usdt | 1082/1082 | ok |
| depth_okx_usdt_swap | 1081/1082 | ok |
| deribit | 1082/1082 | ok |
| dydx | 1082/1082 | ok |
| gate | 1082/1082 | ok |
| hl_predicted_fundings | 1081/1082 | ok |
| htx | 1079/1082 | ok |
| hyperliquid | 1081/1082 | ok |
| kraken | 1081/1082 | ok |
| kucoin | 1082/1082 | ok |
| okx_BTC-USD-SWAP | 1081/1082 | ok |
| okx_BTC-USDT-SWAP | 1081/1082 | ok |
| paradex | 1082/1082 | ok |
| premium_parts | 1081/1082 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-11 08:00Z | 326 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-11 08:00Z | 326 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-11 12:00Z | 1194 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-11 12:35Z | 14328 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-11 12:00Z | 1194 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-11 12:35Z | 14328 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-11 11:00Z | 1194 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-11 12:35Z | 14328 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-11 12:00Z | 1194 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-11 12:35Z | 14328 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-11 12:00Z | 1194 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-11 12:35Z | 14327 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-11 11:00Z | 3330 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-11 11:00Z | 1169 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-11 08:00Z | 334 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-11 11:00Z | 3329 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-11 11:00Z | 3329 | 0 | 0 |

## 3. Forced-flow retention and revision
30184 distinct liquidation observations; 23 retained boundary probes.
- 2026-10-07 00:12Z: 0.97 days, 11 pages (observed source boundary).
- 2026-10-08 00:12Z: 0.95 days, 24 pages (observed source boundary).
- 2026-10-09 00:13Z: 0.93 days, 35 pages (observed source boundary).
- 2026-10-10 00:12Z: 0.95 days, 14 pages (observed source boundary).
- 2026-10-11 00:12Z: 0.99 days, 4 pages (observed source boundary).
Observed later revision after first live capture: n=30 active hours; mean 10.1%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 1082 stored snapshots in 160 distinct hours from 2026-10-04 18:01Z to 2026-10-11 12:42Z; latest 738 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 1082 stored snapshots in 160 distinct hours from 2026-10-04 18:01Z to 2026-10-11 12:42Z; latest 20 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10059 bars 2026-10-04 13:03Z → 2026-10-11 12:41Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10059 bars 2026-10-04 13:03Z → 2026-10-11 12:41Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10059 bars 2026-10-04 13:03Z → 2026-10-11 12:41Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10059 bars 2026-10-04 13:03Z → 2026-10-11 12:41Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10059 bars 2026-10-04 13:03Z → 2026-10-11 12:41Z; 0 missing minutes inside the span.
- Deribit options schema 2: 1082 runs; latest 738 with OI, 192 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 160.
- Hyperliquid sample v2: 1082 snapshots; account checks by state failed 5, ok_btc 23834, ok_flat 159422, ok_other 22319; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 291, ledger ok 1373, twap not_attempted 1, twap ok 9155.
- OKX insurance fund rows: regular_update 1082.
- Research lab: 28 runs in window; latest 2026-10-11 12:55Z: exploratory 5, under prospective evaluation 3 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-05.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot hyperliquid: 1/1082 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- snapshot cross_hl_ETH: 1/1082 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot cross_hl_SOL: 1/1082 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: Hyperliquid metaAndAssetCtxs unavailable in this run; absent from the latest run
- snapshot hl_predicted_fundings: 1/1082 routine run(s), 2026-10-10 08:17Z; latest: RuntimeError: HTTP 502; deadline reached; absent from the latest run
- forward book hl_positions: 1/1082 routine run(s), 2026-10-10 08:17Z; latest: degraded: 5/190 accounts failed, malformed or not attempted; absent from the latest run
- snapshot htx: 3/1082 routine run(s), 2026-10-05 06:56Z → 2026-10-10 00:42Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot kraken: 1/1082 routine run(s), 2026-10-06 07:01Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot okx_BTC-USD-SWAP: 1/1082 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot okx_BTC-USDT-SWAP: 1/1082 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: URLError: <urlopen error [Errno 104] Connection reset by peer>; deadline reached; absent from the latest run
- snapshot depth_okx_usdt_swap: 1/1082 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- snapshot premium_parts: 1/1082 routine run(s), 2026-10-05 16:52Z; latest: RuntimeError: circuit open: www.okx.com failed earlier in this stage (URLError: <urlopen error; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
