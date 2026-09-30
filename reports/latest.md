# JBM desk report — 2026-09-30 12:56Z
Window 2026-09-23 12:56Z → 2026-09-30 12:56Z. report-2.6-2026-09-24.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-30 12:56Z by report-2.6-2026-09-24 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-30 12:54Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-30 12:56Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-30 12:54Z | 3 min |
| snapshots | 2026-09-30 12:53Z | 3 min |
| 1-minute prices (BTC perp) | 2026-09-30 12:54Z | 3 min |
| Deribit options | 2026-09-30 12:53Z | 3 min |
| Hyperliquid account sample | 2026-09-30 12:54Z | 3 min |
| Hyperliquid enrichment | 2026-09-30 12:54Z | 3 min |
| OKX insurance fund | 2026-09-30 12:54Z | 3 min |
| OKX liquidation orders | 2026-09-30 12:53Z | 4 min |
| research lab (lab-2.2-2026-09-24) | 2026-09-30 12:56Z | 0 min |

## 1. Collection health
643 routine runs in window, by trigger: not recorded (github) 3, schedule 639, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-23 12:56Z → 2026-09-23 16:06Z | `7 * * * *` | 3 | 3 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 3/3, an upper bound (manual runs indistinguishable) | 2/2 slot intervals | 0/3 |
| 2026-09-23 16:06Z → 2026-09-30 12:56Z | `7,22,37,52 * * * *` | 658 | 639 (97%) | 638/659 slot intervals | 6/640 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 14.2, p90 20.9, max 30.5; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.2, p90 20.9, max 59.7.
Runtime per routine run (s): median 104, p90 113, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 640 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 643/643 | ok |
| binance_BTCUSDC | 643/643 | ok |
| binance_BTCUSDT | 643/643 | ok |
| binance_BTCUSD_PERP | 643/643 | ok |
| binance_coinm_prem | 643/643 | ok |
| binance_usdc_prem | 643/643 | ok |
| binance_usdt_prem | 643/643 | ok |
| bingx | 643/643 | ok |
| bitfinex_margin | 643/643 | ok |
| bitget_USDC | 643/643 | ok |
| bitget_USDT | 643/643 | ok |
| cross_binance_ETHUSDT | 623/623 | ok |
| cross_binance_SOLUSDT | 623/623 | ok |
| cross_hl_ETH | 623/623 | ok |
| cross_hl_SOL | 623/623 | ok |
| depth_binance_usdt | 643/643 | ok |
| depth_okx_usdt_swap | 643/643 | ok |
| deribit | 643/643 | ok |
| dydx | 643/643 | ok |
| gate | 643/643 | ok |
| hl_predicted_fundings | 643/643 | ok |
| htx | 637/643 | ok |
| hyperliquid | 643/643 | ok |
| kraken | 643/643 | ok |
| kucoin | 643/643 | ok |
| okx_BTC-USD-SWAP | 643/643 | ok |
| okx_BTC-USDT-SWAP | 643/643 | ok |
| paradex | 643/643 | ok |
| premium_parts | 643/643 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-30 08:00Z | 293 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-30 08:00Z | 293 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-30 12:00Z | 930 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-30 12:45Z | 11162 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-30 12:00Z | 930 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-30 12:45Z | 11162 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-30 11:00Z | 930 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-30 12:45Z | 11162 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-30 12:00Z | 930 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-30 12:45Z | 11162 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-30 12:00Z | 930 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-30 12:45Z | 11161 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-30 11:00Z | 3066 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-30 11:00Z | 905 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-30 08:00Z | 301 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-30 11:00Z | 3065 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-30 11:00Z | 3065 | 0 | 0 |

## 3. Forced-flow retention and revision
14419 distinct liquidation observations; 12 retained boundary probes.
- 2026-09-26 00:20Z: 0.98 days, 17 pages (observed source boundary).
- 2026-09-27 00:22Z: 1.0 days, 4 pages (observed source boundary).
- 2026-09-28 00:24Z: 0.94 days, 10 pages (observed source boundary).
- 2026-09-29 00:22Z: 0.99 days, 23 pages (observed source boundary).
- 2026-09-30 00:23Z: 0.98 days, 13 pages (observed source boundary).
Observed later revision after first live capture: n=29 active hours; mean 6.1%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 643 stored snapshots in 168 distinct hours from 2026-09-23 13:23Z to 2026-09-30 12:52Z; latest 779 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 643 stored snapshots in 168 distinct hours from 2026-09-23 13:23Z to 2026-09-30 12:52Z; latest 20 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 10075 bars 2026-09-23 12:57Z → 2026-09-30 12:51Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 10075 bars 2026-09-23 12:57Z → 2026-09-30 12:51Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 10075 bars 2026-09-23 12:57Z → 2026-09-30 12:51Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 10075 bars 2026-09-23 12:57Z → 2026-09-30 12:51Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 10075 bars 2026-09-23 12:57Z → 2026-09-30 12:51Z; 0 missing minutes inside the span.
- Deribit options schema 2: 623 runs; latest 779 with OI, 167 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata refreshed.
- Deribit hourly quote records: 161.
- Hyperliquid sample v2: 623 snapshots; account checks by state ok_btc 13718, ok_flat 92042, ok_other 12610; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 223, ledger ok 846, twap not_attempted 2, twap ok 5159.
- OKX insurance fund rows: regular_update 623.
- Research lab: 33 runs in window; latest 2026-09-30 12:56Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.98 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 6/643 routine run(s), 2026-09-25 23:41Z → 2026-09-29 19:44Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
