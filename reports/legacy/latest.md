# JBM desk collector report — 2026-09-22 19:10Z
Window 2026-09-15 19:10Z → 2026-09-22 19:10Z (7d). Report report-1.1-2026-09-22; collector versions in window: collector-2.0-2026-09-22. Every figure below is computed from the repository's stored data by this version; nothing is carried from a prior report.

## 1. Collection health
Runs: 3 of ~1 expected (300%). Gaps over 90 minutes: 0. Runs with a critical Binance share failure: 0. Median run time 53s.

| source | ok / pulled | most common failure |
|---|---|---|
| backpack | 3/3 |  |
| binance_BTCUSDC | 3/3 |  |
| binance_BTCUSDT | 3/3 |  |
| binance_BTCUSD_PERP | 3/3 |  |
| binance_coinm_prem | 3/3 |  |
| binance_usdc_prem | 3/3 |  |
| binance_usdt_prem | 3/3 |  |
| bingx | 3/3 |  |
| bitfinex_margin | 3/3 |  |
| bitget_COIN | 0/3 | RuntimeError: HTTP 400 |
| bitget_USDC | 3/3 |  |
| bitget_USDT | 3/3 |  |
| bitmex | 1/3 | RuntimeError: instrument state Settled, settle 2026-09-16T12:00:00.000Z |
| depth_binance_usdt | 3/3 |  |
| depth_okx_usdt_swap | 3/3 |  |
| deribit | 3/3 |  |
| dydx | 3/3 |  |
| gate | 3/3 |  |
| hl_predicted_fundings | 3/3 |  |
| htx | 3/3 |  |
| hyperliquid | 3/3 |  |
| kraken | 3/3 |  |
| kucoin | 3/3 |  |
| okx_BTC-USD-SWAP | 3/3 |  |
| okx_BTC-USDT-SWAP | 3/3 |  |
| paradex | 3/3 |  |
| premium_parts | 3/3 |  |

## 2. History held
Rows are closed intervals only. 'Missing' counts intervals absent between the first and last stored row. Independent windows are the non-overlapping ceiling (days × 24 ÷ horizon), before episode collapse (M-18).

| series | first | last | rows | missing | days held | 4h / 12h / 24h / 72h windows |
|---|---|---|---|---|---|---|
| binance_funding_settled (BTCUSDC; also BTCUSDT) | 2026-06-25 00:00Z | 2026-09-22 16:00Z | 270 | — | 89.7 | 538 / 179 / 89 / 29 |
| binance_globalLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 31.0 | 185 / 61 / 30 / 10 |
| binance_globalLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8933 | 0 | 31.0 | 186 / 62 / 31 / 10 |
| binance_openInterestHist_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 31.0 | 185 / 61 / 30 / 10 |
| binance_openInterestHist_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8933 | 0 | 31.0 | 186 / 62 / 31 / 10 |
| binance_takerlongshortRatio_1h | 2026-08-22 18:00Z | 2026-09-22 18:00Z | 744 | 1 | 31.0 | 186 / 62 / 31 / 10 |
| binance_takerlongshortRatio_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8916 | 17 | 31.0 | 186 / 62 / 31 / 10 |
| binance_topLongShortAccountRatio_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 31.0 | 185 / 61 / 30 / 10 |
| binance_topLongShortAccountRatio_5m | 2026-08-22 18:40Z | 2026-09-22 19:00Z | 8933 | 0 | 31.0 | 186 / 62 / 31 / 10 |
| binance_topLongShortPositionRatio_1h | 2026-08-22 19:00Z | 2026-09-22 18:00Z | 744 | 0 | 31.0 | 185 / 61 / 30 / 10 |
| binance_topLongShortPositionRatio_5m | 2026-08-22 18:45Z | 2026-09-22 19:00Z | 8932 | 0 | 31.0 | 186 / 62 / 31 / 10 |
| deribit_dvol_1h | 2026-05-25 18:00Z | 2026-09-22 18:00Z | 2881 | 0 | 120.0 | 720 / 240 / 120 / 40 |
| okx_acct_ratio_1h | 2026-08-23 19:00Z | 2026-09-22 18:00Z | 720 | 0 | 30.0 | 179 / 59 / 29 / 9 |
| okx_funding_settled | 2026-06-22 08:00Z | 2026-09-22 16:00Z | 278 | — | 92.3 | 554 / 184 / 92 / 30 |
| okx_index_1h | 2026-05-25 19:00Z | 2026-09-22 18:00Z | 2880 | 0 | 120.0 | 719 / 239 / 119 / 39 |
| okx_mark_1h | 2026-05-25 19:00Z | 2026-09-22 18:00Z | 2880 | 0 | 120.0 | 719 / 239 / 119 / 39 |

## 3. Forced-flow feed — OKX BTC-USDT-SWAP (O14)
Retention probes (paged to the boundary): 2026-09-22 0.97d over 26 pages.
No active hours captured live in the window yet — revision not measurable.
Orders stored: 2402; hours covered: 23.

## 4. Forecast registry (baserates §4)
Scored to date: 0; scored this report: 0; pending horizon: 0; late or unseen registrations: 0. A forecast counts only if the collector saw its exact content before its start.

## 5. Pre-registered tests
A test grades only decisions made after the collector first saw its exact content. Earlier decisions are reported separately as in-sample.

No tests registered. Tests are written in a skill thread from a frozen O-row design and committed to tests/.

## 6. Fold candidates
Mechanical lines derived from the data above. A skill thread decides what folds; nothing here edits the package.

- runbook §B retention and O14: the OKX REST liquidation feed pages back 0.97 days (2026-09-22, 26 pages); 1 probes on file.

## 7. Alerts
None.
