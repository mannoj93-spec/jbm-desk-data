# JBM desk report — 2026-10-25 17:10Z
Window 2026-10-18 17:10Z → 2026-10-25 17:10Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-25 17:10Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-25 16:44Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-25 16:47Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-25 16:44Z | 25 min |
| snapshots | 2026-10-25 16:43Z | 26 min |
| 1-minute prices (BTC perp) | 2026-10-25 16:44Z | 25 min |
| Deribit options | 2026-10-25 16:43Z | 26 min |
| Hyperliquid account sample | 2026-10-25 16:44Z | 25 min |
| Hyperliquid enrichment | 2026-10-25 16:44Z | 25 min |
| OKX insurance fund | 2026-10-25 16:44Z | 25 min |
| OKX liquidation orders | 2026-10-25 15:13Z | 116 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-25 16:47Z | 23 min |

## 1. Collection health
814 routine runs in window, by trigger: schedule 203, workflow_dispatch 611.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-18 17:10Z → 2026-10-25 17:10Z | `7,22,37,52 * * * *` | 670 | 203 (30%) | 665/669 slot intervals; 2 not yet assessed (after the input cutoff) | 0/814 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-25 16:43Z; report clock 2026-10-25 17:10Z: wall-clock lag 27 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 31.8, p90 47.9, max 327.7.
Actual interval between stored snapshots, all triggers (min): median 14.9, p90 15.1, max 30.1.
Runtime per routine run (s): median 105, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 814 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 814/814 | ok |
| binance_BTCUSDC | 814/814 | ok |
| binance_BTCUSDT | 814/814 | ok |
| binance_BTCUSD_PERP | 814/814 | ok |
| binance_coinm_prem | 814/814 | ok |
| binance_usdc_prem | 814/814 | ok |
| binance_usdt_prem | 814/814 | ok |
| bingx | 814/814 | ok |
| bitfinex_margin | 814/814 | ok |
| bitget_USDC | 814/814 | ok |
| bitget_USDT | 814/814 | ok |
| cross_binance_ETHUSDT | 814/814 | ok |
| cross_binance_SOLUSDT | 814/814 | ok |
| cross_hl_ETH | 814/814 | ok |
| cross_hl_SOL | 814/814 | ok |
| depth_binance_usdt | 814/814 | ok |
| depth_okx_usdt_swap | 814/814 | ok |
| deribit | 814/814 | ok |
| dydx | 814/814 | ok |
| gate | 814/814 | ok |
| hl_predicted_fundings | 814/814 | ok |
| htx | 814/814 | ok |
| hyperliquid | 814/814 | ok |
| kraken | 814/814 | ok |
| kucoin | 814/814 | ok |
| okx_BTC-USD-SWAP | 814/814 | ok |
| okx_BTC-USDT-SWAP | 814/814 | ok |
| paradex | 814/814 | ok |
| premium_parts | 814/814 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-25 16:00Z | 369 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-25 16:00Z | 369 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-25 16:00Z | 1534 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-25 16:35Z | 18408 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-25 16:00Z | 1532 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-25 16:35Z | 18392 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-25 15:00Z | 1534 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-25 16:35Z | 18408 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-25 16:00Z | 1534 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-25 16:35Z | 18408 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-25 16:00Z | 1534 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-25 16:35Z | 18407 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-25 15:00Z | 3670 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-25 15:00Z | 1509 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-25 16:00Z | 377 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-25 15:00Z | 3669 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-25 15:00Z | 3669 | 0 | 0 |

## 3. Forced-flow retention and revision
53419 distinct liquidation observations; 37 retained boundary probes.
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
- 2026-10-25 00:09Z: 1.0 days, 18 pages (observed source boundary).
Observed later revision after first live capture: n=28 active hours; mean 7.8%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 814 stored snapshots in 168 distinct hours from 2026-10-18 17:12Z to 2026-10-25 16:43Z; latest 740 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 814 stored snapshots in 168 distinct hours from 2026-10-18 17:12Z to 2026-10-25 16:43Z; latest 24 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10052 bars 2026-10-18 17:11Z → 2026-10-25 16:42Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10052 bars 2026-10-18 17:11Z → 2026-10-25 16:42Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10052 bars 2026-10-18 17:11Z → 2026-10-25 16:42Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10052 bars 2026-10-18 17:11Z → 2026-10-25 16:42Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10052 bars 2026-10-18 17:11Z → 2026-10-25 16:42Z; 0 missing minutes inside the span.
- Deribit options schema 2: 814 runs; latest 740 with OI, 180 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 814 snapshots; account checks by state ok_btc 17463, ok_flat 120777, ok_other 16420; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 288, ledger ok 1102, twap ok 6750.
- OKX insurance fund rows: regular_update 814.
- Research lab: 28 runs in window; latest 2026-10-25 16:47Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-10-25 13:52Z, over 90 minutes before this report.
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
