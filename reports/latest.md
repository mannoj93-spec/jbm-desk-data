# JBM desk report — 2026-11-05 07:49Z
Window 2026-10-29 07:49Z → 2026-11-05 07:49Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-05 07:49Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-05 07:14Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-05 07:19Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-05 07:14Z | 35 min |
| snapshots | 2026-11-05 07:13Z | 36 min |
| 1-minute prices (BTC perp) | 2026-11-05 07:14Z | 35 min |
| Deribit options | 2026-11-05 07:14Z | 36 min |
| Hyperliquid account sample | 2026-11-05 07:14Z | 35 min |
| Hyperliquid enrichment | 2026-11-05 07:14Z | 35 min |
| OKX insurance fund | 2026-11-05 07:14Z | 35 min |
| OKX liquidation orders | 2026-11-05 06:43Z | 66 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-05 07:19Z | 30 min |

## 1. Collection health
676 routine runs in window, by trigger: schedule 29, workflow_dispatch 647.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-29 07:49Z → 2026-11-05 07:49Z | `7,22,37,52 * * * *` | 671 | 29 (4%) | 659/669 slot intervals; 2 not yet assessed (after the input cutoff) | 19/676 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-05 07:13Z; report clock 2026-11-05 07:49Z: wall-clock lag 37 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 325.6, p90 453.4, max 915.1.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.2, max 66.4.
Runtime per routine run (s): median 107, p90 118, max 149; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 676 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 676/676 | ok |
| binance_BTCUSDC | 676/676 | ok |
| binance_BTCUSDT | 676/676 | ok |
| binance_BTCUSD_PERP | 676/676 | ok |
| binance_coinm_prem | 676/676 | ok |
| binance_usdc_prem | 676/676 | ok |
| binance_usdt_prem | 676/676 | ok |
| bingx | 676/676 | ok |
| bitfinex_margin | 676/676 | ok |
| bitget_USDC | 676/676 | ok |
| bitget_USDT | 676/676 | ok |
| cross_binance_ETHUSDT | 676/676 | ok |
| cross_binance_SOLUSDT | 676/676 | ok |
| cross_hl_ETH | 676/676 | ok |
| cross_hl_SOL | 676/676 | ok |
| depth_binance_usdt | 676/676 | ok |
| depth_okx_usdt_swap | 676/676 | ok |
| deribit | 676/676 | ok |
| dydx | 675/676 | ok |
| gate | 676/676 | ok |
| hl_predicted_fundings | 676/676 | ok |
| htx | 676/676 | ok |
| hyperliquid | 676/676 | ok |
| kraken | 672/676 | ok |
| kucoin | 676/676 | ok |
| okx_BTC-USD-SWAP | 676/676 | ok |
| okx_BTC-USDT-SWAP | 676/676 | ok |
| paradex | 662/676 | ok |
| premium_parts | 675/676 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-05 00:00Z | 400 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-05 00:00Z | 400 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-05 07:00Z | 1789 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-05 07:05Z | 21462 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-05 07:00Z | 1787 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-05 07:05Z | 21446 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-05 06:00Z | 1789 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-05 07:05Z | 21462 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-05 07:00Z | 1789 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-05 07:05Z | 21462 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-05 07:00Z | 1789 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-05 07:05Z | 21461 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-05 06:00Z | 3925 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-05 06:00Z | 1764 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-05 00:00Z | 408 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-05 06:00Z | 3924 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-05 06:00Z | 3924 | 0 | 0 |

## 3. Forced-flow retention and revision
74596 distinct liquidation observations; 48 retained boundary probes.
- 2026-11-01 00:13Z: 1.0 days, 4 pages (observed source boundary).
- 2026-11-02 00:13Z: 0.94 days, 8 pages (observed source boundary).
- 2026-11-03 00:17Z: 1.0 days, 19 pages (observed source boundary).
- 2026-11-04 00:13Z: 0.99 days, 15 pages (observed source boundary).
- 2026-11-05 00:13Z: 1.0 days, 48 pages (observed source boundary).
Observed later revision after first live capture: n=32 active hours; mean 7.1%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 676 stored snapshots in 169 distinct hours from 2026-10-29 07:58Z to 2026-11-05 07:13Z; latest 769 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 676 stored snapshots in 169 distinct hours from 2026-10-29 07:58Z to 2026-11-05 07:13Z; latest 21 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10043 bars 2026-10-29 07:50Z → 2026-11-05 07:12Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10043 bars 2026-10-29 07:50Z → 2026-11-05 07:12Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10043 bars 2026-10-29 07:50Z → 2026-11-05 07:12Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10043 bars 2026-10-29 07:50Z → 2026-11-05 07:12Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10043 bars 2026-10-29 07:50Z → 2026-11-05 07:12Z; 0 missing minutes inside the span.
- Deribit options schema 2: 676 runs; latest 769 with OI, 153 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 676 snapshots; account checks by state ok_btc 14445, ok_flat 100700, ok_other 13295; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 181, ledger ok 857, twap ok 5722.
- OKX insurance fund rows: regular_update 676.
- Research lab: 18 runs in window; latest 2026-11-05 07:19Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-11-02.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-11-05 03:40Z, over 90 minutes before this report.
- snapshot paradex: 14/676 routine run(s), 2026-11-04 03:13Z → 2026-11-04 06:28Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot premium_parts: 1/676 routine run(s), 2026-10-31 21:43Z; latest: RuntimeError: deadline reached; absent from the latest run
- snapshot kraken: 4/676 routine run(s), 2026-10-30 02:28Z → 2026-10-30 03:04Z; latest: RuntimeError: HTTP 503; deadline reached; absent from the latest run
- snapshot dydx: 1/676 routine run(s), 2026-10-29 09:13Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
