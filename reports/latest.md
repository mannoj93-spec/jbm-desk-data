# JBM desk report — 2026-09-24 12:51Z
Window 2026-09-17 12:51Z → 2026-09-24 12:51Z. report-2.5-2026-09-23.
Stored observations are research inputs. Missing observations never count as a failed forecast.

Generated 2026-09-24 12:51Z by report-2.5-2026-09-23 (coverage refresh; forecast scoring and research tests are in the weekly report). Input cutoff: 2026-09-24 12:40Z (latest collector run written, collector-2.7-2026-09-23). Research lab: last run 2026-09-24 12:51Z, lab-2.1-2026-09-23. This file is refreshed every 6 hours by the Research lab workflow; if the generation time is older than that, the refresh has stopped.

| Dataset | Latest observation written | Age |
|---|---|---:|
| collector runs | 2026-09-24 12:40Z | 11 min |
| snapshots | 2026-09-24 12:39Z | 12 min |
| 1-minute prices (BTC perp) | 2026-09-24 12:40Z | 11 min |
| Deribit options | 2026-09-24 12:39Z | 12 min |
| Hyperliquid account sample | 2026-09-24 12:40Z | 11 min |
| Hyperliquid enrichment | 2026-09-24 12:40Z | 11 min |
| OKX insurance fund | 2026-09-24 12:40Z | 11 min |
| OKX liquidation orders | 2026-09-24 12:39Z | 12 min |
| research lab (lab-2.0) | 2026-09-24 12:51Z | 0 min |

## 1. Collection health
104 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, schedule 79, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-24 12:51Z | `7,22,37,52 * * * *` | 82 | 79 (96%) | 79/82 slot intervals | 0/80 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between scheduled starts under the current 15-minute cadence (min): median 13.7, p90 21.9, max 28.6; includes pre-2.6 GitHub runs, whose trigger is unrecorded.
Actual interval between stored snapshots, all triggers (min): median 14.6, p90 58.9, max 256.0.
Runtime per routine run (s): median 102, p90 110, max 125; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 80 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 104/104 | ok |
| binance_BTCUSDC | 104/104 | ok |
| binance_BTCUSDT | 104/104 | ok |
| binance_BTCUSD_PERP | 104/104 | ok |
| binance_coinm_prem | 104/104 | ok |
| binance_usdc_prem | 104/104 | ok |
| binance_usdt_prem | 104/104 | ok |
| bingx | 104/104 | ok |
| bitfinex_margin | 104/104 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 104/104 | ok |
| bitget_USDT | 104/104 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| cross_binance_ETHUSDT | 63/63 | ok |
| cross_binance_SOLUSDT | 63/63 | ok |
| cross_hl_ETH | 63/63 | ok |
| cross_hl_SOL | 63/63 | ok |
| depth_binance_usdt | 104/104 | ok |
| depth_okx_usdt_swap | 104/104 | ok |
| deribit | 104/104 | ok |
| dydx | 104/104 | ok |
| gate | 104/104 | ok |
| hl_predicted_fundings | 104/104 | ok |
| htx | 104/104 | ok |
| hyperliquid | 104/104 | ok |
| kraken | 104/104 | ok |
| kucoin | 104/104 | ok |
| okx_BTC-USD-SWAP | 104/104 | ok |
| okx_BTC-USDT-SWAP | 104/104 | ok |
| paradex | 104/104 | ok |
| premium_parts | 104/104 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-24 08:00Z | 275 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-24 08:00Z | 275 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-24 12:00Z | 786 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-24 12:30Z | 9431 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-24 12:00Z | 786 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-24 12:30Z | 9431 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-24 11:00Z | 786 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-24 12:30Z | 9431 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-24 12:00Z | 786 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-24 12:30Z | 9431 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-24 12:00Z | 786 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-24 12:30Z | 9430 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-24 11:00Z | 2922 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-24 11:00Z | 761 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-24 08:00Z | 283 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-24 11:00Z | 2921 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-24 11:00Z | 2921 | 0 | 0 |

## 3. Forced-flow retention and revision
6620 distinct liquidation observations; 6 retained boundary probes.
- 2026-09-23 00:01Z: 0.97 days, 20 pages (observed source boundary).
- 2026-09-23 00:23Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 16:14Z: 1.0 days, 32 pages (observed source boundary).
- 2026-09-24 00:21Z: 1.0 days, 32 pages (observed source boundary).
Observed later revision after first live capture: n=8 active hours; mean 4.3%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 100 stored snapshots in 37 distinct hours from 2026-09-23 00:23Z to 2026-09-24 12:38Z; latest 851 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 100 stored snapshots in 37 distinct hours from 2026-09-23 00:23Z to 2026-09-24 12:38Z; latest 20 BTC positions in top 190; 0 degraded snapshot(s).

## 3c. Research datasets (collector 2.7)
Coverage of stored inputs only. These are samples and summaries, not trading results.
- binance_klines_1m_BTCUSDT_perp: 2470 bars 2026-09-22 19:28Z → 2026-09-24 12:37Z; 0 missing minutes inside the span.
- binance_markklines_1m_BTCUSDT_perp: 2470 bars 2026-09-22 19:28Z → 2026-09-24 12:37Z; 0 missing minutes inside the span.
- binance_klines_1m_BTCUSDT_spot: 2470 bars 2026-09-22 19:28Z → 2026-09-24 12:37Z; 0 missing minutes inside the span.
- binance_klines_1m_ETHUSDT_perp: 2470 bars 2026-09-22 19:28Z → 2026-09-24 12:37Z; 0 missing minutes inside the span.
- binance_klines_1m_SOLUSDT_perp: 2470 bars 2026-09-22 19:28Z → 2026-09-24 12:37Z; 0 missing minutes inside the span.
- Deribit options schema 2: 63 runs; latest 851 with OI, 225 zero OI, 0 absent, 0 past expiry; panel 12/12 tickers; metadata refreshed.
- Deribit hourly quote records: 17.
- Hyperliquid sample v2: 63 snapshots; account checks by state ok_btc 1370, ok_flat 9257, ok_other 1343; fixed cohort F-hl-sample-v2-1790195337162 (100), rotating 90 per run.
- Hyperliquid enrichment requests: fills ok 21, ledger ok 84, twap not_attempted 2, twap ok 523.
- OKX insurance fund rows: regular_update 63.
- Research lab: 5 runs in window; latest 2026-09-24 12:51Z: exploratory 7, under prospective evaluation 1 (statuses per design; see reports/research.md).

## 4. Forecast registry
Not run in the coverage refresh (scoring writes evidence); see the weekly report reports/2026-09-23.md.

## 5. Pre-registered research tests
Not run in the coverage refresh; see the weekly report.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot bitget_COIN: 4/104 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/104 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
