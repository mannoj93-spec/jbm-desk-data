# JBM desk report — 2026-09-23 16:17Z
Window 2026-09-16 16:17Z → 2026-09-23 16:17Z. report-2.3-2026-09-23.
Stored observations are research inputs. Missing observations never count as a failed forecast.

## 1. Collection health
25 routine runs in window, by trigger: not recorded (container) 2, not recorded (github) 21, not recorded (local) 1, workflow_dispatch 1.

| Cadence period (UTC) | Schedule | Nominal slots | Scheduled starts | Snapshot coverage | Degraded snapshots |
|---|---|---:|---|---|---:|
| 2026-09-22 23:19Z → 2026-09-23 16:06Z | `7 * * * *` | 16 | 21 GitHub runs, trigger not recorded (pre-2.6); slots with a run: 16/16, an upper bound (manual runs indistinguishable) | 15/15 slot intervals | 1/21 |
| 2026-09-23 16:06Z → 2026-09-23 16:17Z | `7,22,37,52 * * * *` | 0 | 0 | no complete interval | 0/1 |
Starts are counted, never matched to slots: GitHub starts scheduled runs late by an unrecorded amount and can drop them, so a start time does not identify its slot (edges can shift a count by one). Slots in the last 20 minutes are not yet due. Manual runs never count as scheduled starts; they do count toward snapshot coverage, which measures data held rather than scheduler behaviour.
Actual interval between stored snapshots, all triggers (min): median 58.5, p90 65.2, max 256.0.
Runtime per routine run (s): median 96, p90 106, max 114; 0 run(s) reached the network budget.
Rate-limit incidents: none recorded across 1 run(s) that record them (2.6+); Hyperliquid accounts retried after a 429: 0.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 25/25 | ok |
| binance_BTCUSDC | 25/25 | ok |
| binance_BTCUSDT | 25/25 | ok |
| binance_BTCUSD_PERP | 25/25 | ok |
| binance_coinm_prem | 25/25 | ok |
| binance_usdc_prem | 25/25 | ok |
| binance_usdt_prem | 25/25 | ok |
| bingx | 25/25 | ok |
| bitfinex_margin | 25/25 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 25/25 | ok |
| bitget_USDT | 25/25 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| depth_binance_usdt | 25/25 | ok |
| depth_okx_usdt_swap | 25/25 | ok |
| deribit | 25/25 | ok |
| dydx | 25/25 | ok |
| gate | 25/25 | ok |
| hl_predicted_fundings | 25/25 | ok |
| htx | 25/25 | ok |
| hyperliquid | 25/25 | ok |
| kraken | 25/25 | ok |
| kucoin | 25/25 | ok |
| okx_BTC-USD-SWAP | 25/25 | ok |
| okx_BTC-USDT-SWAP | 25/25 | ok |
| paradex | 25/25 | ok |
| premium_parts | 25/25 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-23 16:00Z | 273 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-23 16:00Z | 273 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-23 16:00Z | 766 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-23 16:05Z | 9186 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-23 16:00Z | 766 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-23 16:05Z | 9186 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-23 15:00Z | 766 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-23 16:05Z | 9186 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-23 16:00Z | 766 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-23 16:05Z | 9186 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-23 16:00Z | 766 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-23 16:05Z | 9185 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-23 15:00Z | 2902 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-23 15:00Z | 741 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-23 16:00Z | 281 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-23 15:00Z | 2901 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-23 15:00Z | 2901 | 0 | 0 |

## 3. Forced-flow retention and revision
5318 distinct liquidation observations; 5 retained boundary probes.
- 2026-09-22 18:36Z: 0.97 days, 26 pages (observed source boundary).
- 2026-09-23 00:01Z: 0.97 days, 20 pages (observed source boundary).
- 2026-09-23 00:23Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 16:14Z: 1.0 days, 32 pages (observed source boundary).
Observed later revision after first live capture: n=3 active hours; mean 1.7%. Requires a covering follow-up at least six hours after close; latest stored totals are not guaranteed final.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 21 stored snapshots in 17 distinct hours from 2026-09-23 00:23Z to 2026-09-23 16:14Z; latest 848 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 21 stored snapshots in 17 distinct hours from 2026-09-23 00:23Z to 2026-09-23 16:14Z; latest 30 BTC positions in top 200; 0 degraded snapshot(s).

## 4. Forecast registry
Scored: 0 total; 0 this report. Pending/retryable: 0. Late registrations: 0.

## 5. Pre-registered research tests
Post-registration labels describe timing only. Custom test code can bypass context helpers; leakage, episode independence and causal validity require review.
No research tests completed successfully.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 1.0 days. This is not a guarantee of future availability.

## 7. Alerts
- snapshot bitget_COIN: 4/25 routine run(s), 2026-09-22 18:44Z → 2026-09-22 23:24Z; latest: RuntimeError: HTTP 400; absent from the latest run
- snapshot bitmex: 3/25 routine run(s), 2026-09-22 18:46Z → 2026-09-22 23:24Z; latest: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z; absent from the latest run
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
