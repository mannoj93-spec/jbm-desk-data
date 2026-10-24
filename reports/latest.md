# JBM desk report — 2026-10-24 11:54Z
Window 2026-10-17 11:54Z → 2026-10-24 11:54Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-24 11:54Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-24 11:29Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-24 11:32Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-24 11:29Z | 24 min |
| snapshots | 2026-10-24 11:28Z | 25 min |
| 1-minute prices (BTC perp) | 2026-10-24 11:29Z | 25 min |
| Deribit options | 2026-10-24 11:28Z | 25 min |
| Hyperliquid account sample | 2026-10-24 11:29Z | 25 min |
| Hyperliquid enrichment | 2026-10-24 11:29Z | 25 min |
| OKX insurance fund | 2026-10-24 11:29Z | 24 min |
| OKX liquidation orders | 2026-10-24 10:58Z | 56 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-24 11:32Z | 22 min |

## 1. Collection health
840 routine runs in window, by trigger: schedule 260, workflow_dispatch 580.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-17 11:54Z → 2026-10-24 11:54Z | `7,22,37,52 * * * *` | 670 | 260 (39%) | 665/669 slot intervals; 2 not yet assessed (after the input cutoff) | 0/840 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-24 11:28Z; report clock 2026-10-24 11:54Z: wall-clock lag 26 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 30.7, p90 41.8, max 327.7.
Actual interval between stored snapshots, all triggers (min): median 14.1, p90 15.7, max 30.1.
Runtime per routine run (s): median 105, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 840 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 840/840 | ok |
| binance_BTCUSDC | 840/840 | ok |
| binance_BTCUSDT | 840/840 | ok |
| binance_BTCUSD_PERP | 840/840 | ok |
| binance_coinm_prem | 840/840 | ok |
| binance_usdc_prem | 840/840 | ok |
| binance_usdt_prem | 840/840 | ok |
| bingx | 840/840 | ok |
| bitfinex_margin | 840/840 | ok |
| bitget_USDC | 840/840 | ok |
| bitget_USDT | 840/840 | ok |
| cross_binance_ETHUSDT | 840/840 | ok |
| cross_binance_SOLUSDT | 840/840 | ok |
| cross_hl_ETH | 840/840 | ok |
| cross_hl_SOL | 840/840 | ok |
| depth_binance_usdt | 840/840 | ok |
| depth_okx_usdt_swap | 840/840 | ok |
| deribit | 840/840 | ok |
| dydx | 840/840 | ok |
| gate | 840/840 | ok |
| hl_predicted_fundings | 840/840 | ok |
| htx | 840/840 | ok |
| hyperliquid | 840/840 | ok |
| kraken | 840/840 | ok |
| kucoin | 840/840 | ok |
| okx_BTC-USD-SWAP | 840/840 | ok |
| okx_BTC-USDT-SWAP | 840/840 | ok |
| paradex | 840/840 | ok |
| premium_parts | 840/840 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-24 08:00Z | 365 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-24 08:00Z | 365 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-24 11:00Z | 1505 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-24 11:20Z | 18057 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-24 11:00Z | 1503 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-24 11:20Z | 18041 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-24 10:00Z | 1505 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-24 11:20Z | 18057 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-24 11:00Z | 1505 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-24 11:20Z | 18057 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-24 11:00Z | 1505 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-24 11:20Z | 18056 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-24 10:00Z | 3641 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-24 10:00Z | 1480 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-24 08:00Z | 373 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-24 10:00Z | 3640 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-24 10:00Z | 3640 | 0 | 0 |

## 3. Forced-flow retention and revision
51436 distinct liquidation observations; 36 retained boundary probes.
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.6%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 840 stored snapshots in 169 distinct hours from 2026-10-17 11:54Z to 2026-10-24 11:28Z; latest 736 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 840 stored snapshots in 169 distinct hours from 2026-10-17 11:54Z to 2026-10-24 11:28Z; latest 20 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10053 bars 2026-10-17 11:55Z → 2026-10-24 11:27Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10053 bars 2026-10-17 11:55Z → 2026-10-24 11:27Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10053 bars 2026-10-17 11:55Z → 2026-10-24 11:27Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10053 bars 2026-10-17 11:55Z → 2026-10-24 11:27Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10053 bars 2026-10-17 11:55Z → 2026-10-24 11:27Z; 0 missing minutes inside the span.
- Deribit options schema 2: 840 runs; latest 736 with OI, 186 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 840 snapshots; account checks by state ok_btc 18093, ok_flat 124552, ok_other 16955; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 285, ledger ok 1125, twap ok 6990.
- OKX insurance fund rows: regular_update 840.
- Research lab: 28 runs in window; latest 2026-10-24 11:32Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.96 days. This is not a guarantee of future availability.

## 7. Alerts
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
