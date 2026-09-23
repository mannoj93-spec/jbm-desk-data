# JBM desk report — 2026-09-23 02:26Z
Window 2026-09-16 02:26Z → 2026-09-23 02:26Z. report-2.2-2026-09-23.
Stored observations are research inputs. Missing observations never count as a failed forecast.

## 1. Collection health
GitHub hourly slots observed: 3/3; 11 hourly runs in window (all runners). Slot counts approximate scheduled collection, not guaranteed uptime.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 11/11 | ok |
| binance_BTCUSDC | 11/11 | ok |
| binance_BTCUSDT | 11/11 | ok |
| binance_BTCUSD_PERP | 11/11 | ok |
| binance_coinm_prem | 11/11 | ok |
| binance_usdc_prem | 11/11 | ok |
| binance_usdt_prem | 11/11 | ok |
| bingx | 11/11 | ok |
| bitfinex_margin | 11/11 | ok |
| bitget_COIN | 0/4 | retired: absent from the latest snapshot (see collector.py) |
| bitget_USDC | 11/11 | ok |
| bitget_USDT | 11/11 | ok |
| bitmex | 1/4 | retired: absent from the latest snapshot (see collector.py) |
| depth_binance_usdt | 11/11 | ok |
| depth_okx_usdt_swap | 11/11 | ok |
| deribit | 11/11 | ok |
| dydx | 11/11 | ok |
| gate | 11/11 | ok |
| hl_predicted_fundings | 11/11 | ok |
| htx | 11/11 | ok |
| hyperliquid | 11/11 | ok |
| kraken | 11/11 | ok |
| kucoin | 11/11 | ok |
| okx_BTC-USD-SWAP | 11/11 | ok |
| okx_BTC-USDT-SWAP | 11/11 | ok |
| paradex | 11/11 | ok |
| premium_parts | 11/11 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-23 00:00Z | 271 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-23 00:00Z | 271 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-23 02:00Z | 752 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-23 02:15Z | 9020 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-23 02:00Z | 752 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-23 02:15Z | 9020 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-23 01:00Z | 752 | 0 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-23 02:15Z | 9020 | 0 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-23 02:00Z | 752 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-23 02:15Z | 9020 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-23 02:00Z | 752 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-23 02:15Z | 9019 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-23 01:00Z | 2888 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-23 01:00Z | 727 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-23 00:00Z | 279 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-23 01:00Z | 2887 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-23 01:00Z | 2887 | 0 | 0 |

## 3. Forced-flow retention and revision
2674 distinct liquidation observations; 4 retained boundary probes.
- 2026-09-22 18:36Z: 0.97 days, 26 pages (observed source boundary).
- 2026-09-23 00:01Z: 0.97 days, 20 pages (observed source boundary).
- 2026-09-23 00:23Z: 0.99 days, 20 pages (observed source boundary).
- 2026-09-23 00:26Z: 0.99 days, 20 pages (observed source boundary).
Insufficient live capture/follow-up evidence to estimate revision.

## 3b. Forward-only books (requirement 50)
Value starts on the first stored run; no source retains these books.
- Deribit BTC options, per-strike OI: 3 hourly runs from 2026-09-23 00:23Z to 2026-09-23 02:24Z; latest 850 strikes with OI; 0 degraded snapshot(s).
- Hyperliquid BTC position map: 3 hourly runs from 2026-09-23 00:23Z to 2026-09-23 02:24Z; latest 29 BTC positions in top 200; 0 degraded snapshot(s).

## 4. Forecast registry
Scored: 0 total; 0 this report. Pending/retryable: 0. Late registrations: 0.

## 5. Pre-registered research tests
Post-registration labels describe timing only. Custom test code can bypass context helpers; leakage, episode independence and causal validity require review.
No research tests completed successfully.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.99 days. This is not a guarantee of future availability.

## 7. Alerts
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
