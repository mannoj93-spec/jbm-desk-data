# JBM desk report — 2026-09-24 18:48Z
Window 2026-09-17 18:48Z → 2026-09-24 18:48Z. report-2.5-2026-09-23.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-24 18:48Z by report-2.5-2026-09-23 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-24 18:35Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-24 18:48Z, lab-2.1-2026-09-23. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-24 18:35Z | 12 min |
| snapshots | 2026-09-24 18:35Z | 13 min |
| 1-minute prices (BTC perp) | 2026-09-24 18:35Z | 12 min |
| Deribit options | 2026-09-24 18:35Z | 13 min |
| Hyperliquid account sample | 2026-09-24 18:35Z | 13 min |
| Hyperliquid enrichment | 2026-09-24 18:35Z | 13 min |
| OKX insurance fund | 2026-09-24 18:35Z | 12 min |
| OKX liquidation orders | 2026-09-24 18:34Z | 13 min |
| research lab (lab-2.0) | 2026-09-24 18:48Z | 0 min |

## 1. Collection health
127 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 102, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-24 18:48Z | `7,22,37,52 * * * *` | 106 | 102 (96%) | 103/106 slot intervals | 0/103 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 13.8, p90 21.9, max 28.6; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.4, p90 57.1, max 256.0.
Runtime per routine run (s): median 103, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 103 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 127/127 | ok |
| binance_BTCUSDC | 127/127 | ok |
| binance_BTCUSDT | 127/127 | ok |
| binance_BTCUSD_PERP | 127/127 | ok |
| binance_coinm_prem | 127/127 | ok |
| binance_usdc_prem | 127/127 | ok |
| binance_usdt_prem | 127/127 | ok |
| bingx | 127/127 | ok |
| bitfinex_margin | 127/127 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 127/127 | ok |
| bitget_USDT | 127/127 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 86/86 | ok |
| cross_binance_SOLUSDT | 86/86 | ok |
| cross_hl_ETH | 86/86 | ok |
| cross_hl_SOL | 86/86 | ok |
| depth_binance_usdt | 127/127 | ok |
| depth_okx_usdt_swap | 127/127 | ok |
| deribit | 127/127 | ok |
| dydx | 127/127 | ok |
| gate | 127/127 | ok |
| hl_predicted_fundings | 127/127 | ok |
| htx | 127/127 | ok |
| hyperliquid | 127/127 | ok |
| kraken | 127/127 | ok |
| kucoin | 127/127 | ok |
| okx_BTC-USD-SWAP | 127/127 | ok |
| okx_BTC-USDT-SWAP | 127/127 | ok |
| paradex | 127/127 | ok |
| premium_parts | 127/127 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-24 16:00Z | 276 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-24 16:00Z | 276 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-24 18:00Z | 792 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-24 18:25Z | 9502 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-24 18:00Z | 792 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-24 18:25Z | 9502 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-24 17:00Z | 792 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-24 18:25Z | 9502 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-24 18:00Z | 792 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-24 18:25Z | 9502 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-24 18:00Z | 792 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-24 18:25Z | 9501 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-24 17:00Z | 2928 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-24 17:00Z | 767 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-24 16:00Z | 284 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-24 17:00Z | 2927 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-24 17:00Z | 2927 | 0 | 0 |

## 3. Forced-flow retention and revision
7733 distinct liquidation observations; 6 retained boundary probes.
- 2026-09-23 00:01Z: 0.97 days, 20 pages (observed source boundary).
- 2026-09-23 00:23Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 16:14Z: 1.0 days, 32 pages (observed source boundary).
- 2026-09-24 00:21Z: 1.0 days, 32 pages (observed source boundary).
Observed later revision after first live capture: n=8 active hours; mean 4.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 123 stored snapshots in 43 distinct hours from 2026-09-23 00:23Z to 2026-09-24 18:34Z; latest 887 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 123 stored snapshots in 43 distinct hours from 2026-09-23 00:23Z to 2026-09-24 18:34Z; latest 23 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 2826 bars 2026-09-22 19:28Z → 2026-09-24 18:33Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 2826 bars 2026-09-22 19:28Z → 2026-09-24 18:33Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 2826 bars 2026-09-22 19:28Z → 2026-09-24 18:33Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 2826 bars 2026-09-22 19:28Z → 2026-09-24 18:33Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 2826 bars 2026-09-22 19:28Z → 2026-09-24 18:33Z; 0 missing minutes inside the span.
- Deribit options schema 2: 86 runs; latest 887 with OI, 191 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 23.
- Hyperliquid sample v2: 86 snapshots; account checks by state ok_btc 1870, ok_flat 12652, ok_other 1818; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 29, ledger ok 115, twap not_attempted 2, twap ok 714.
- OKX insurance fund rows: regular_update 86.
- Research lab: 6 runs in window; latest 2026-09-24 18:48Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot bitget_COIN: 4/127 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/127 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
