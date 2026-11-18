# Market studies

Generated 2026-11-18T11:02:08.704Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 148 | 112 | 112 |
| range | collecting (descriptive) | 148 | 105 | 99 |
| state | collecting (descriptive) | 594 | 355 | 352 |
| paired | collecting (descriptive) | 2373 | 2275 | 2270 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0463953 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00409663 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000566835 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000825991 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.07% | 14.58% | 51.92% | 10.57% | 98.4819 | 897.363 |
| ordinary/B2_10 | -10.12% | 14.43% | 51.07% | 10.65% | 72.5759 | 815.177 |
| ordinary/VOL_05 | -8.22% | 16.43% | 38.95% | 9.09% | 13.7635 | 98.0562 |
| ordinary/VOL_10 | -7.63% | 15.31% | 39.82% | 8.49% | 9.20059 | 65.5761 |
| stressed/B2_05 | -10.59% | 14.57% | 51.93% | 11.04% | 98.5497 | 1460.41 |
| stressed/B2_10 | -10.51% | 14.39% | 51.08% | 10.98% | 72.6311 | 1229.59 |
| stressed/VOL_05 | -8.29% | 16.42% | 38.95% | 9.12% | 13.7707 | 178.068 |
| stressed/VOL_10 | -7.68% | 15.30% | 39.84% | 8.50% | 9.21234 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.66% | 0.0340105 |
| calibrated | 64.65% | 0.0320339 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2270 | 1348 | 922 | 48.15% |
| 60m | perp_synchronized_clock | 2270 | 1348 | 922 | 48.15% |
| 60m | combined_synchronized_clock | 2270 | 1326 | 944 | 48.19% |
| 15m | perp_original_clock | 2270 | 1348 | 922 | 47.85% |
| 15m | perp_synchronized_clock | 2270 | 1348 | 922 | 47.85% |
| 15m | combined_synchronized_clock | 2270 | 1326 | 944 | 46.76% |

## Data usability pilots

- Options: 593 captures; usable 7d RR25 in 507, usable 30d RR25 in 263; 463 valid hourly changes.
- Liquidations: 1662 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2271}`.
- Exchange stress: 1187/1187 scheduled records. Capture states: `{"missed": 45, "ok": 1142}`. Ratings: `{"low": 1142}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
