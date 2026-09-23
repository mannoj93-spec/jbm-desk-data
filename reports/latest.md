# JBM desk report — 2026-09-23 22:22Z
Window 2026-09-16 22:22Z → 2026-09-23 22:22Z. report-2.5-2026-09-23.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-23 22:22Z by report-2.5-2026-09-23 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-23 22:17Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-23 22:19Z, lab-2.0-2026-09-23. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-23 22:17Z | 5 min |
| snapshots | 2026-09-23 22:16Z | 6 min |
| 1-minute prices (BTC perp) | 2026-09-23 22:17Z | 5 min |
| Deribit options | 2026-09-23 22:16Z | 6 min |
| Hyperliquid account sample | 2026-09-23 22:17Z | 5 min |
| Hyperliquid enrichment | 2026-09-23 22:17Z | 5 min |
| OKX insurance fund | 2026-09-23 22:17Z | 5 min |
| OKX liquidation orders | 2026-09-23 22:16Z | 6 min |
| research lab (lab-2.0) | 2026-09-23 22:19Z | 3 min |

## 1. Collection health
49 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 24, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-23 22:22Z | `7,22,37,52 * * * *` | 24 | 24 (100%) | 25/25 slot intervals | 0/25 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 13.3, p90 22.5, max 26.3; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 21.8, p90 59.8, max 256.0.
Runtime per routine run (s): median 99, p90 109, max 125; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 25 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 49/49 | ok |
| binance_BTCUSDC | 49/49 | ok |
| binance_BTCUSDT | 49/49 | ok |
| binance_BTCUSD_PERP | 49/49 | ok |
| binance_coinm_prem | 49/49 | ok |
| binance_usdc_prem | 49/49 | ok |
| binance_usdt_prem | 49/49 | ok |
| bingx | 49/49 | ok |
| bitfinex_margin | 49/49 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 49/49 | ok |
| bitget_USDT | 49/49 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 8/8 | ok |
| cross_binance_SOLUSDT | 8/8 | ok |
| cross_hl_ETH | 8/8 | ok |
| cross_hl_SOL | 8/8 | ok |
| depth_binance_usdt | 49/49 | ok |
| depth_okx_usdt_swap | 49/49 | ok |
| deribit | 49/49 | ok |
| dydx | 49/49 | ok |
| gate | 49/49 | ok |
| hl_predicted_fundings | 49/49 | ok |
| htx | 49/49 | ok |
| hyperliquid | 49/49 | ok |
| kraken | 49/49 | ok |
| kucoin | 49/49 | ok |
| okx_BTC-USD-SWAP | 49/49 | ok |
| okx_BTC-USDT-SWAP | 49/49 | ok |
| paradex | 49/49 | ok |
| premium_parts | 49/49 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-23 16:00Z | 273 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-23 16:00Z | 273 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-23 22:00Z | 772 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-23 22:10Z | 9259 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-23 22:00Z | 772 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-23 22:10Z | 9259 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-23 21:00Z | 772 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-23 22:10Z | 9259 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-23 22:00Z | 772 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-23 22:10Z | 9259 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-23 22:00Z | 772 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-23 22:10Z | 9258 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-23 21:00Z | 2908 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-23 21:00Z | 747 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-23 16:00Z | 281 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-23 21:00Z | 2907 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-23 21:00Z | 2907 | 0 | 0 |

## 3. Forced-flow retention and revision
5590 distinct liquidation observations; 5 retained boundary probes.
- 2026-09-22 18:36Z: 0.97 days, 26 pages (observed source boundary).
- 2026-09-23 00:01Z: 0.97 days, 20 pages (observed source boundary).
- 2026-09-23 00:23Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 16:14Z: 1.0 days, 32 pages (observed source boundary).
Observed later revision after first live capture: n=5 active hours; mean 3.1%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 45 stored snapshots in 23 distinct hours from 2026-09-23 00:23Z to 2026-09-23 22:15Z; latest 851 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 45 stored snapshots in 23 distinct hours from 2026-09-23 00:23Z to 2026-09-23 22:15Z; latest 17 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 1607 bars 2026-09-22 19:28Z → 2026-09-23 22:14Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 1607 bars 2026-09-22 19:28Z → 2026-09-23 22:14Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 1607 bars 2026-09-22 19:28Z → 2026-09-23 22:14Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 1607 bars 2026-09-22 19:28Z → 2026-09-23 22:14Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 1607 bars 2026-09-22 19:28Z → 2026-09-23 22:14Z; 0 missing minutes inside the span.
- Deribit options schema 2: 8 runs; latest 851 with OI, 123 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 3.
- Hyperliquid sample v2: 8 snapshots; account checks by state ok_btc 172, ok_flat 1183, ok_other 165; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 1, ledger ok 9, twap ok 70.
- OKX insurance fund rows: regular_update 8.
- Research lab: 1 runs in window; latest 2026-09-23 22:19Z: exploratory 8 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot bitget_COIN: 4/49 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/49 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
