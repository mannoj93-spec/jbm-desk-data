# JBM desk report — 2026-09-22 23:39Z
Window 2026-09-15 23:39Z → 2026-09-22 23:39Z. report-2.0-2026-09-22.
Stored observations are research inputs. Missing observations never count as a failed forecast.

## 1. Collection health
GitHub hourly slots observed: 0/0; 4 hourly runs in window (all runners). Slot counts approximate scheduled collection, not guaranteed uptime.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 4/4 | ok |
| binance_BTCUSDC | 4/4 | ok |
| binance_BTCUSDT | 4/4 | ok |
| binance_BTCUSD_PERP | 4/4 | ok |
| binance_coinm_prem | 4/4 | ok |
| binance_usdc_prem | 4/4 | ok |
| binance_usdt_prem | 4/4 | ok |
| bingx | 4/4 | ok |
| bitfinex_margin | 4/4 | ok |
| bitget_COIN | 0/4 | RuntimeError: HTTP 400 |
| bitget_USDC | 4/4 | ok |
| bitget_USDT | 4/4 | ok |
| bitmex | 1/4 | RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z |
| depth_binance_usdt | 4/4 | ok |
| depth_okx_usdt_swap | 4/4 | ok |
| deribit | 4/4 | ok |
| dydx | 4/4 | ok |
| gate | 4/4 | ok |
| hl_predicted_fundings | 4/4 | ok |
| htx | 4/4 | ok |
| hyperliquid | 4/4 | ok |
| kraken | 4/4 | ok |
| kucoin | 4/4 | ok |
| okx_BTC-USD-SWAP | 4/4 | ok |
| okx_BTC-USDT-SWAP | 4/4 | ok |
| paradex | 4/4 | ok |
| premium_parts | 4/4 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-22 16:00Z | 270 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-22 16:00Z | 270 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-22 22:00Z | 748 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-22 23:15Z | 8984 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-22 22:00Z | 748 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-22 23:15Z | 8984 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-22 22:00Z | 748 | 1 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-22 23:15Z | 8967 | 17 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-22 22:00Z | 748 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-22 23:15Z | 8984 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-22 22:00Z | 748 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-22 23:15Z | 8983 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-22 22:00Z | 2885 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-22 22:00Z | 724 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-22 16:00Z | 278 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-22 22:00Z | 2884 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-22 22:00Z | 2884 | 0 | 0 |

## 3. Forced-flow retention and revision
2543 distinct liquidation observations; 1 retained boundary probes.
- 2026-09-22 18:36Z: 0.97 days, 26 pages (observed source boundary).
Insufficient live capture/follow-up evidence to estimate revision.

## 4. Forecast registry
Scored: 0 total; 0 this report. Pending/retryable: 0. Late registrations: 0.

## 5. Pre-registered research tests
Post-registration labels describe timing only. Custom test code can bypass context helpers; leakage, episode independence and causal validity require review.
No research tests completed successfully.

## 6. Fold candidates
Human review required before changing the skill package.
- Review measured liquidation retention: latest probe 0.97 days. This is not a guarantee of future availability.

## 7. Alerts
- Latest bitget_COIN snapshot unavailable: RuntimeError: HTTP 400
- Latest bitmex snapshot unavailable: RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z
- binance_takerlongshortRatio_1h: 1 missing intervals; retry backfill while source retention permits.
- binance_takerlongshortRatio_5m: 17 missing intervals; retry backfill while source retention permits.
- deribit_dvol_1h: 3 legacy duplicate rows; storage bytes preserved, counts deduplicated.
