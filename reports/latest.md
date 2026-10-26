# JBM desk report — 2026-10-26 01:20Z
Window 2026-10-19 01:20Z → 2026-10-26 01:20Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-26 01:20Z by report-2.6.2-2026-10-19 (weekly report; desk range forecasts are scored hourly by range-score.yml and only summarised here). Input cutoff: 2026-10-26 01:14Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-25 21:11Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-26 01:14Z | 6 min |
| snapshots | 2026-10-26 01:13Z | 7 min |
| 1-minute prices (BTC perp) | 2026-10-26 01:14Z | 6 min |
| Deribit options | 2026-10-26 01:13Z | 7 min |
| Hyperliquid account sample | 2026-10-26 01:14Z | 6 min |
| Hyperliquid enrichment | 2026-10-26 01:14Z | 6 min |
| OKX insurance fund | 2026-10-26 01:14Z | 6 min |
| OKX liquidation orders | 2026-10-26 01:13Z | 7 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-25 21:11Z | 249 min |

## 1. Collection health
803 routine runs in window, by trigger: schedule 186, workflow_dispatch 617.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-19 01:20Z → 2026-10-26 01:20Z | `7,22,37,52 * * * *` | 671 | 186 (28%) | 666/671 slot intervals | 0/803 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-26 01:13Z; report clock 2026-10-26 01:20Z: wall-clock lag 7 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 32.8, p90 132.7, max 327.7.
Actual interval between stored snapshots, all triggers (min): median 14.9, p90 15.1, max 30.1.
Runtime per routine run (s): median 106, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 803 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 803/803 | ok |
| binance_BTCUSDC | 803/803 | ok |
| binance_BTCUSDT | 803/803 | ok |
| binance_BTCUSD_PERP | 803/803 | ok |
| binance_coinm_prem | 803/803 | ok |
| binance_usdc_prem | 803/803 | ok |
| binance_usdt_prem | 803/803 | ok |
| bingx | 803/803 | ok |
| bitfinex_margin | 803/803 | ok |
| bitget_USDC | 803/803 | ok |
| bitget_USDT | 803/803 | ok |
| cross_binance_ETHUSDT | 803/803 | ok |
| cross_binance_SOLUSDT | 803/803 | ok |
| cross_hl_ETH | 803/803 | ok |
| cross_hl_SOL | 803/803 | ok |
| depth_binance_usdt | 803/803 | ok |
| depth_okx_usdt_swap | 803/803 | ok |
| deribit | 803/803 | ok |
| dydx | 803/803 | ok |
| gate | 803/803 | ok |
| hl_predicted_fundings | 803/803 | ok |
| htx | 803/803 | ok |
| hyperliquid | 803/803 | ok |
| kraken | 803/803 | ok |
| kucoin | 803/803 | ok |
| okx_BTC-USD-SWAP | 803/803 | ok |
| okx_BTC-USDT-SWAP | 803/803 | ok |
| paradex | 803/803 | ok |
| premium_parts | 803/803 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-26 00:00Z | 370 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-26 00:00Z | 370 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-26 01:00Z | 1543 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-26 01:05Z | 18510 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-26 01:00Z | 1541 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-26 01:05Z | 18494 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-26 00:00Z | 1543 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-26 01:05Z | 18510 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-26 01:00Z | 1543 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-26 01:05Z | 18510 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-26 01:00Z | 1543 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-26 01:05Z | 18509 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-26 00:00Z | 3679 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-26 00:00Z | 1518 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-26 00:00Z | 378 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-26 00:00Z | 3678 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-26 00:00Z | 3678 | 0 | 0 |

## 3. Forced-flow retention and revision
53729 distinct liquidation observations; 38 retained boundary probes.
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
- 2026-10-25 00:09Z: 1.0 days, 18 pages (observed source boundary).
- 2026-10-26 00:08Z: 0.96 days, 9 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 8.0%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 803 stored snapshots in 169 distinct hours from 2026-10-19 01:27Z to 2026-10-26 01:13Z; latest 753 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 803 stored snapshots in 169 distinct hours from 2026-10-19 01:27Z to 2026-10-26 01:13Z; latest 19 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10072 bars 2026-10-19 01:21Z → 2026-10-26 01:12Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10072 bars 2026-10-19 01:21Z → 2026-10-26 01:12Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10072 bars 2026-10-19 01:21Z → 2026-10-26 01:12Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10072 bars 2026-10-19 01:21Z → 2026-10-26 01:12Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10072 bars 2026-10-19 01:21Z → 2026-10-26 01:12Z; 0 missing minutes inside the span.
- Deribit options schema 2: 803 runs; latest 753 with OI, 167 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 168.
- Hyperliquid sample v2: 803 snapshots; account checks by state ok_btc 17203, ok_flat 119159, ok_other 16208; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 277, ledger ok 1080, twap ok 6673.
- OKX insurance fund rows: regular_update 803.
- Research lab: 27 runs in window; latest 2026-10-25 21:11Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Scored: 485 total; 0 this report. Pending/retryable: 25. Late registrations: 0.

## 5. Pre-registered research tests
Post-registration labels describe timing only. Custom test code can bypass context helpers; leakage, episode independence and causal validity require review.
No research tests completed successfully.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.96 days. This is not a guarantee of future availability.

## 7. Alerts
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
