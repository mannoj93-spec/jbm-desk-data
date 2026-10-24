# JBM desk report — 2026-10-24 16:35Z
Window 2026-10-17 16:35Z → 2026-10-24 16:35Z. report-2.6.2-2026-10-19.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-10-24 16:35Z by report-2.6.2-2026-10-19 (coverage refresh; desk range forecasts are scored hourly (range-score.yml, reports/range.md), research designs run in the 6-hourly lab (reports/research.md), other registered forecasts are scored in the weekly report). Input cutoff: 2026-10-24 15:59Z (latest collector run written, collector-2.8-2026-10-04). Research lab: last run 2026-10-24 16:13Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-10-24 15:59Z | 36 min |
| snapshots | 2026-10-24 15:58Z | 37 min |
| 1-minute prices (BTC perp) | 2026-10-24 15:59Z | 36 min |
| Deribit options | 2026-10-24 15:58Z | 37 min |
| Hyperliquid account sample | 2026-10-24 15:59Z | 36 min |
| Hyperliquid enrichment | 2026-10-24 15:59Z | 36 min |
| OKX insurance fund | 2026-10-24 15:59Z | 36 min |
| OKX liquidation orders | 2026-10-24 15:58Z | 37 min |
| research lab (lab-2.2-2026-09-24) | 2026-10-24 16:13Z | 22 min |

## 1. Collection health
836 routine runs in window, by trigger: schedule 250, workflow_dispatch 586.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-10-17 16:35Z → 2026-10-24 16:35Z | `7,22,37,52 * * * *` | 671 | 250 (37%) | 665/669 slot intervals; 2 not yet assessed (after the input cutoff) | 0/836 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Input cutoff 2026-10-24 15:58Z; report clock 2026-10-24 16:35Z: wall-clock lag 38 min. Lag is not a collection gap; intervals after the cutoff are not yet assessed (refresh the inputs to assess them).
Actual interval between scheduled starts under the current 15-minute cadence (min): median 30.9, p90 42.4, max 327.7.
Actual interval between stored snapshots, all triggers (min): median 14.4, p90 15.6, max 30.1.
Runtime per routine run (s): median 105, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 836 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 836/836 | ok |
| binance_BTCUSDC | 836/836 | ok |
| binance_BTCUSDT | 836/836 | ok |
| binance_BTCUSD_PERP | 836/836 | ok |
| binance_coinm_prem | 836/836 | ok |
| binance_usdc_prem | 836/836 | ok |
| binance_usdt_prem | 836/836 | ok |
| bingx | 836/836 | ok |
| bitfinex_margin | 836/836 | ok |
| bitget_USDC | 836/836 | ok |
| bitget_USDT | 836/836 | ok |
| cross_binance_ETHUSDT | 836/836 | ok |
| cross_binance_SOLUSDT | 836/836 | ok |
| cross_hl_ETH | 836/836 | ok |
| cross_hl_SOL | 836/836 | ok |
| depth_binance_usdt | 836/836 | ok |
| depth_okx_usdt_swap | 836/836 | ok |
| deribit | 836/836 | ok |
| dydx | 836/836 | ok |
| gate | 836/836 | ok |
| hl_predicted_fundings | 836/836 | ok |
| htx | 836/836 | ok |
| hyperliquid | 836/836 | ok |
| kraken | 836/836 | ok |
| kucoin | 836/836 | ok |
| okx_BTC-USD-SWAP | 836/836 | ok |
| okx_BTC-USDT-SWAP | 836/836 | ok |
| paradex | 836/836 | ok |
| premium_parts | 836/836 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-10-24 08:00Z | 365 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-10-24 08:00Z | 365 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-24 15:00Z | 1509 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-24 15:50Z | 18111 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-10-24 15:00Z | 1507 | 2 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-10-24 15:50Z | 18095 | 16 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-10-24 14:00Z | 1509 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-10-24 15:50Z | 18111 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-10-24 15:00Z | 1509 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-10-24 15:50Z | 18111 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-10-24 15:00Z | 1509 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-10-24 15:50Z | 18110 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-10-24 14:00Z | 3645 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-10-24 14:00Z | 1484 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-10-24 08:00Z | 373 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-10-24 14:00Z | 3644 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-10-24 14:00Z | 3644 | 0 | 0 |

## 3. Forced-flow retention and revision
52561 distinct liquidation observations; 36 retained boundary probes.
- 2026-10-20 00:12Z: 0.98 days, 12 pages (observed source boundary).
- 2026-10-21 00:12Z: 1.0 days, 19 pages (observed source boundary).
- 2026-10-22 00:12Z: 0.99 days, 17 pages (observed source boundary).
- 2026-10-23 00:13Z: 0.97 days, 22 pages (observed source boundary).
- 2026-10-24 00:12Z: 0.96 days, 18 pages (observed source boundary).
Observed later revision after first live capture: n=27 active hours; mean 7.6%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 836 stored snapshots in 168 distinct hours from 2026-10-17 16:42Z to 2026-10-24 15:58Z; latest 757 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 836 stored snapshots in 168 distinct hours from 2026-10-17 16:42Z to 2026-10-24 15:58Z; latest 23 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10042 bars 2026-10-17 16:36Z → 2026-10-24 15:57Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10042 bars 2026-10-17 16:36Z → 2026-10-24 15:57Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10042 bars 2026-10-17 16:36Z → 2026-10-24 15:57Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10042 bars 2026-10-17 16:36Z → 2026-10-24 15:57Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10042 bars 2026-10-17 16:36Z → 2026-10-24 15:57Z; 0 missing minutes inside the span.
- Deribit options schema 2: 836 runs; latest 757 with OI, 167 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 167.
- Hyperliquid sample v2: 836 snapshots; account checks by state ok_btc 17998, ok_flat 123966, ok_other 16876; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 291, ledger ok 1127, twap ok 6942.
- OKX insurance fund rows: regular_update 836.
- Research lab: 28 runs in window; latest 2026-10-24 16:13Z: exploratory 4, under prospective evaluation 4 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-10-19.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.96 days. This is not a guarantee of future availability.

## 7. Alerts
- Collector stale: last scheduled run 2026-10-24 14:35Z, over 90 minutes before this report.
- binance_openInterestHist_1h: 2 missing intervals; retry backfill while source retention permits.
- binance_openInterestHist_5m: 16 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
