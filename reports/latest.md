# JBM desk report — 2026-11-11 07:41Z
Window 2026-11-04 07:41Z → 2026-11-11 07:41Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-11-11 07:41Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-11-11 06:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-11-11 07:02Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-11-11 06:59Z | 42 min |
| snapshots | 2026-11-11 06:59Z | 42 min |
| 1-minute prices (BTC perp) | 2026-11-11 06:59Z | 42 min |
| Deribit options | 2026-11-11 06:59Z | 42 min |
| Hyperliquid account sample | 2026-11-11 06:59Z | 42 min |
| Hyperliquid enrichment | 2026-11-11 06:59Z | 42 min |
| OKX insurance fund | 2026-11-11 06:59Z | 42 min |
| OKX liquidation orders | 2026-11-11 06:58Z | 43 min |
| research lab (lab-2.2-2026-09-24) | 2026-11-11 07:02Z | 39 min |

## 1. Collection health
673 routine runs in window, by trigger: schedule 27, workflow_dispatch 646.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-11-04 07:41Z → 2026-11-11 07:41Z | `7,22,37,52 * * * *` | 670 | 27 (4%) | 658/668 slot intervals; 3 not yet assessed (after the input cutoff) | 2/673 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-11-11 06:58Z; report clock 2026-11-11 07:41Z: wall-clock lag 43 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 358.0, p90 475.3, max 630.8.
Actual interval between stored snapshots, all triggers (min): median 15.0, p90 15.2, max 50.5.
Runtime per routine run (s): median 105, p90 114, max 199; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 673 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 673/673 | ok |
| binance_BTCUSDC | 673/673 | ok |
| binance_BTCUSDT | 673/673 | ok |
| binance_BTCUSD_PERP | 673/673 | ok |
| binance_coinm_prem | 673/673 | ok |
| binance_usdc_prem | 673/673 | ok |
| binance_usdt_prem | 673/673 | ok |
| bingx | 673/673 | ok |
| bitfinex_margin | 673/673 | ok |
| bitget_USDC | 673/673 | ok |
| bitget_USDT | 673/673 | ok |
| cross_binance_ETHUSDT | 673/673 | ok |
| cross_binance_SOLUSDT | 673/673 | ok |
| cross_hl_ETH | 673/673 | ok |
| cross_hl_SOL | 673/673 | ok |
| depth_binance_usdt | 673/673 | ok |
| depth_okx_usdt_swap | 673/673 | ok |
| deribit | 671/673 | ok |
| dydx | 673/673 | ok |
| gate | 673/673 | ok |
| hl_predicted_fundings | 673/673 | ok |
| htx | 673/673 | ok |
| hyperliquid | 673/673 | ok |
| kraken | 673/673 | ok |
| kucoin | 673/673 | ok |
| okx_BTC-USD-SWAP | 673/673 | ok |
| okx_BTC-USDT-SWAP | 673/673 | ok |
| paradex | 673/673 | ok |
| premium_parts | 673/673 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-11-11 00:00Z | 418 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-11-11 00:00Z | 418 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-11 06:00Z | 1932 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-11 06:50Z | 23187 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-11-11 06:00Z | 1930 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-11-11 06:50Z | 23171 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-11-11 05:00Z | 1932 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-11-11 06:50Z | 23187 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-11-11 06:00Z | 1932 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-11-11 06:50Z | 23187 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-11-11 06:00Z | 1932 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-11-11 06:50Z | 23186 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-11-11 05:00Z | 4068 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-11-11 05:00Z | 1907 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-11-11 00:00Z | 426 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-11-11 05:00Z | 4067 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-11-11 05:00Z | 4067 | 0 | 0 |

## 3. Forced-flow retention and revision
87392 distinct liquidation observations; 54 retained boundary probes.
- 2026-11-07 00:09Z: 0.99 days, 19 pages (observed source boundary).
- 2026-11-08 00:13Z: 0.97 days, 4 pages (observed source boundary).
- 2026-11-09 00:13Z: 0.62 days, 16 pages (observed source boundary).
- 2026-11-10 00:13Z: 1.0 days, 21 pages (observed source boundary).
- 2026-11-11 00:13Z: 1.0 days, 23 pages (observed source boundary).
Observed later revision after first live capture: n=30 active hours; mean 6.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 671 stored snapshots in 168 distinct hours from 2026-11-04 07:43Z to 2026-11-11 06:58Z; latest 741 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 673 stored snapshots in 168 distinct hours from 2026-11-04 07:43Z to 2026-11-11 06:58Z; latest 20 BTC positions in top 190; 1 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10036 bars 2026-11-04 07:42Z → 2026-11-11 06:57Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10036 bars 2026-11-04 07:42Z → 2026-11-11 06:57Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10036 bars 2026-11-04 07:42Z → 2026-11-11 06:57Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10036 bars 2026-11-04 07:42Z → 2026-11-11 06:57Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10036 bars 2026-11-04 07:42Z → 2026-11-11 06:57Z; 0 missing minutes inside the span.
- Deribit options schema 2: 671 runs; latest 741 with OI, 137 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 673 snapshots; account checks by state failed 1, ok_btc 14377, ok_flat 100382, ok_other 13110; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 204, ledger ok 877, twap not_attempted 5, twap ok 5644.
- OKX insurance fund rows: regular_update 673.
- Research lab: 16 runs in window; latest 2026-11-11 07:02Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-11-09.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-11-11 02:57Z, over 90 minutes before this report.
- history deribit_dvol_1h: 2/673 routine run(s), 2026-11-10 09:13Z → 2026-11-10 09:28Z; latest: HTTP 404; absent from the latest run
- snapshot deribit: 2/673 routine run(s), 2026-11-10 09:13Z → 2026-11-10 09:28Z; latest: RuntimeError: HTTP 404; absent from the latest run
- forward book deribit_options: 2/673 routine run(s), 2026-11-10 09:13Z → 2026-11-10 09:28Z; latest: RuntimeError: HTTP 404; absent from the latest run
- forward book hl_positions: 1/673 routine run(s), 2026-11-07 23:43Z; latest: degraded: 1/190 accounts failed, malformed or not attempted; absent from the latest run
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
