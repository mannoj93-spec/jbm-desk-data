# JBM desk report — 2026-09-24 22:12Z
Window 2026-09-17 22:12Z → 2026-09-24 22:12Z. report-2.6-2026-09-24.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-24 22:12Z by report-2.6-2026-09-24 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-24 21:54Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-24 22:12Z, lab-2.2-2026-09-24. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-24 21:54Z | 18 min |
| snapshots | 2026-09-24 21:53Z | 19 min |
| 1-minute prices (BTC perp) | 2026-09-24 21:54Z | 18 min |
| Deribit options | 2026-09-24 21:53Z | 19 min |
| Hyperliquid account sample | 2026-09-24 21:54Z | 18 min |
| Hyperliquid enrichment | 2026-09-24 21:54Z | 18 min |
| OKX insurance fund | 2026-09-24 21:54Z | 18 min |
| OKX liquidation orders | 2026-09-24 20:31Z | 101 min |
| research lab (lab-2.2-2026-09-24) | 2026-09-24 22:12Z | 0 min |

## 1. Collection health
141 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 116, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-24 22:12Z | `7,22,37,52 * * * *` | 120 | 116 (97%) | 117/120 slot intervals | 0/117 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 13.7, p90 21.9, max 28.6; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.0, p90 55.1, max 256.0.
Runtime per routine run (s): median 103, p90 114, max 133; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 117 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 141/141 | ok |
| binance_BTCUSDC | 141/141 | ok |
| binance_BTCUSDT | 141/141 | ok |
| binance_BTCUSD_PERP | 141/141 | ok |
| binance_coinm_prem | 141/141 | ok |
| binance_usdc_prem | 141/141 | ok |
| binance_usdt_prem | 141/141 | ok |
| bingx | 141/141 | ok |
| bitfinex_margin | 141/141 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 141/141 | ok |
| bitget_USDT | 141/141 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 100/100 | ok |
| cross_binance_SOLUSDT | 100/100 | ok |
| cross_hl_ETH | 100/100 | ok |
| cross_hl_SOL | 100/100 | ok |
| depth_binance_usdt | 141/141 | ok |
| depth_okx_usdt_swap | 141/141 | ok |
| deribit | 141/141 | ok |
| dydx | 141/141 | ok |
| gate | 141/141 | ok |
| hl_predicted_fundings | 141/141 | ok |
| htx | 141/141 | ok |
| hyperliquid | 141/141 | ok |
| kraken | 141/141 | ok |
| kucoin | 141/141 | ok |
| okx_BTC-USD-SWAP | 141/141 | ok |
| okx_BTC-USDT-SWAP | 141/141 | ok |
| paradex | 141/141 | ok |
| premium_parts | 141/141 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-24 16:00Z | 276 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-24 16:00Z | 276 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-24 21:00Z | 795 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-24 21:45Z | 9542 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-24 21:00Z | 795 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-24 21:45Z | 9542 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-24 20:00Z | 795 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-24 21:45Z | 9542 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-24 21:00Z | 795 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-24 21:45Z | 9542 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-24 21:00Z | 795 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-24 21:45Z | 9541 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-24 20:00Z | 2931 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-24 20:00Z | 770 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-24 16:00Z | 284 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-24 20:00Z | 2930 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-24 20:00Z | 2930 | 0 | 0 |

## 3. Forced-flow retention and revision
7757 distinct liquidation observations; 6 retained boundary probes.
- 2026-09-23 00:01Z: 0.97 days, 20 pages (observed source boundary).
- 2026-09-23 00:23Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 16:14Z: 1.0 days, 32 pages (observed source boundary).
- 2026-09-24 00:21Z: 1.0 days, 32 pages (observed source boundary).
Observed later revision after first live capture: n=9 active hours; mean 4.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 137 stored snapshots in 46 distinct hours from 2026-09-23 00:23Z to 2026-09-24 21:52Z; latest 891 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 137 stored snapshots in 46 distinct hours from 2026-09-23 00:23Z to 2026-09-24 21:52Z; latest 25 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 3024 bars 2026-09-22 19:28Z → 2026-09-24 21:51Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 3024 bars 2026-09-22 19:28Z → 2026-09-24 21:51Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 3024 bars 2026-09-22 19:28Z → 2026-09-24 21:51Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 3024 bars 2026-09-22 19:28Z → 2026-09-24 21:51Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 3024 bars 2026-09-22 19:28Z → 2026-09-24 21:51Z; 0 missing minutes inside the span.
- Deribit options schema 2: 100 runs; latest 891 with OI, 187 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata cached.
- Deribit hourly quote records: 26.
- Hyperliquid sample v2: 100 snapshots; account checks by state ok_btc 2181, ok_flat 14708, ok_other 2111; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 34, ledger ok 134, twap not_attempted 2, twap ok 830.
- OKX insurance fund rows: regular_update 100.
- Research lab: 7 runs in window; latest 2026-09-24 22:12Z: exploratory 8 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot bitget_COIN: 4/141 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/141 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
