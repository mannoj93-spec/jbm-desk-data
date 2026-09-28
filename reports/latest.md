# JBM desk report — 2026-09-28 06:54Z
Window 2026-09-21 06:54Z → 2026-09-28 06:54Z. report-2.6-2026-09-24.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-28 06:54Z by report-2.6-2026-09-24 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-28 06:52Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-28 06:54Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-28 06:52Z | 2 min |
| snapshots | 2026-09-28 06:51Z | 3 min |
| 1-minute prices (BTC perp) | 2026-09-28 06:52Z | 2 min |
| Deribit options | 2026-09-28 06:52Z | 3 min |
| Hyperliquid account sample | 2026-09-28 06:52Z | 2 min |
| Hyperliquid enrichment | 2026-09-28 06:52Z | 2 min |
| OKX insurance fund | 2026-09-28 06:52Z | 2 min |
| OKX liquidation orders | 2026-09-28 06:23Z | 31 min |
| research lab (lab-2.2-2026-09-24) | 2026-09-28 06:54Z | 1 min |

## 1. Collection health
456 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 431, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-28 06:54Z | `7,22,37,52 * * * *` | 442 | 431 (98%) | 432/443 slot intervals | 3/432 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 13.9, p90 21.0, max 30.5; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.0, p90 22.5, max 256.0.
Runtime per routine run (s): median 103, p90 113, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 432 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 456/456 | ok |
| binance_BTCUSDC | 456/456 | ok |
| binance_BTCUSDT | 456/456 | ok |
| binance_BTCUSD_PERP | 456/456 | ok |
| binance_coinm_prem | 456/456 | ok |
| binance_usdc_prem | 456/456 | ok |
| binance_usdt_prem | 456/456 | ok |
| bingx | 456/456 | ok |
| bitfinex_margin | 456/456 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 456/456 | ok |
| bitget_USDT | 456/456 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 415/415 | ok |
| cross_binance_SOLUSDT | 415/415 | ok |
| cross_hl_ETH | 415/415 | ok |
| cross_hl_SOL | 415/415 | ok |
| depth_binance_usdt | 456/456 | ok |
| depth_okx_usdt_swap | 456/456 | ok |
| deribit | 456/456 | ok |
| dydx | 456/456 | ok |
| gate | 456/456 | ok |
| hl_predicted_fundings | 456/456 | ok |
| htx | 453/456 | ok |
| hyperliquid | 456/456 | ok |
| kraken | 456/456 | ok |
| kucoin | 456/456 | ok |
| okx_BTC-USD-SWAP | 456/456 | ok |
| okx_BTC-USDT-SWAP | 456/456 | ok |
| paradex | 456/456 | ok |
| premium_parts | 456/456 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-28 00:00Z | 286 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-28 00:00Z | 286 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-28 06:00Z | 876 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-28 06:45Z | 10514 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-28 06:00Z | 876 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-28 06:45Z | 10514 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-28 05:00Z | 876 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-28 06:45Z | 10514 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-28 06:00Z | 876 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-28 06:45Z | 10514 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-28 06:00Z | 876 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-28 06:45Z | 10513 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-28 05:00Z | 3012 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-28 05:00Z | 851 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-28 00:00Z | 294 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-28 05:00Z | 3011 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-28 05:00Z | 3011 | 0 | 0 |

## 3. Forced-flow retention and revision
11085 distinct liquidation observations; 10 retained boundary probes.
- 2026-09-24 00:21Z: 1.0 days, 32 pages (observed source boundary).
- 2026-09-25 00:22Z: 0.96 days, 24 pages (observed source boundary).
- 2026-09-26 00:20Z: 0.98 days, 17 pages (observed source boundary).
- 2026-09-27 00:22Z: 1.0 days, 4 pages (observed source boundary).
- 2026-09-28 00:24Z: 0.94 days, 10 pages (observed source boundary).
Observed later revision after first live capture: n=21 active hours; mean 4.8%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 452 stored snapshots in 127 distinct hours from 2026-09-23 00:23Z to 2026-09-28 06:51Z; latest 802 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 452 stored snapshots in 127 distinct hours from 2026-09-23 00:23Z to 2026-09-28 06:51Z; latest 19 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 7883 bars 2026-09-22 19:28Z → 2026-09-28 06:50Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 7883 bars 2026-09-22 19:28Z → 2026-09-28 06:50Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 7883 bars 2026-09-22 19:28Z → 2026-09-28 06:50Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 7883 bars 2026-09-22 19:28Z → 2026-09-28 06:50Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 7883 bars 2026-09-22 19:28Z → 2026-09-28 06:50Z; 0 missing minutes inside the span.
- Deribit options schema 2: 415 runs; latest 802 with OI, 190 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata refreshed.
- Deribit hourly quote records: 107.
- Hyperliquid sample v2: 415 snapshots; account checks by state ok_btc 9121, ok_flat 61298, ok_other 8431; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 134, ledger ok 549, twap not_attempted 2, twap ok 3465.
- OKX insurance fund rows: regular_update 415.
- Research lab: 24 runs in window; latest 2026-09-28 06:54Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-28.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.94 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot htx: 3/456 routine run(s), 2026-09-25 23:41Z → 2026-09-28 05:30Z; latest: RuntimeError: TimeoutError: request not complete by the deadline (connect, headers or body); d; absent from the latest run
- snapshot bitget_COIN: 4/456 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/456 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
