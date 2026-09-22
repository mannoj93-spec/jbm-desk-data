# JBM desk report — 2026-09-22 20:37Z
Window 2026-09-15 20:37Z → 2026-09-22 20:37Z. report-2.0-2026-09-22.
Stored observations are research inputs. Missing observations never count as a failed forecast.

## 1. Collection health
3 hourly runs in window. No GitHub deployment evidence in stored run records.

| Source | OK / observed | Latest status |
|---|---:|---|
| backpack | 3/3 | ok |
| binance_BTCUSDC | 3/3 | ok |
| binance_BTCUSDT | 3/3 | ok |
| binance_BTCUSD_PERP | 3/3 | ok |
| binance_coinm_prem | 3/3 | ok |
| binance_usdc_prem | 3/3 | ok |
| binance_usdt_prem | 3/3 | ok |
| bingx | 3/3 | ok |
| bitfinex_margin | 3/3 | ok |
| bitget_COIN | 0/3 | RuntimeError: HTTP 400 |
| bitget_USDC | 3/3 | ok |
| bitget_USDT | 3/3 | ok |
| bitmex | 1/3 | RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z |
| depth_binance_usdt | 3/3 | ok |
| depth_okx_usdt_swap | 3/3 | ok |
| deribit | 3/3 | ok |
| dydx | 3/3 | ok |
| gate | 3/3 | ok |
| hl_predicted_fundings | 3/3 | ok |
| htx | 3/3 | ok |
| hyperliquid | 3/3 | ok |
| kraken | 3/3 | ok |
| kucoin | 3/3 | ok |
| okx_BTC-USD-SWAP | 3/3 | ok |
| okx_BTC-USDT-SWAP | 3/3 | ok |
| paradex | 3/3 | ok |
| premium_parts | 3/3 | ok |

## 2. History held
Counts are unique timestamps per instrument; gaps are not independent research samples.

| Series / instrument | First | Last | Unique rows | Missing intervals | Duplicate rows |
|---|---|---|---:|---:|---:|
| binance_funding_settled / BTCUSDC | 2026-06-25 00:00Z | 2026-09-22 16:00Z | 270 | variable cadence | 0 |
| binance_funding_settled / BTCUSDT | 2026-06-25 00:00Z | 2026-09-22 16:00Z | 270 | variable cadence | 0 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 0 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8933 | 0 | 0 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 0 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8933 | 0 | 0 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-22 18:00Z | 744 | 1 | 0 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8916 | 17 | 0 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 0 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8933 | 0 | 0 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 0 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-22 19:00Z | 8932 | 0 | 0 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-22 18:00Z | 2881 | 0 | 3 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-22 18:00Z | 720 | 0 | 0 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-22 16:00Z | 278 | variable cadence | 0 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-22 18:00Z | 2880 | 0 | 0 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-22 18:00Z | 2880 | 0 | 0 |

## 3. Forced-flow retention and revision
2402 distinct liquidation observations; 1 retained boundary probes.
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
