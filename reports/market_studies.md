# Market studies

Generated 2026-11-19T22:47:27.189Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 157 | 121 | 121 |
| range | collecting (descriptive) | 157 | 114 | 108 |
| state | collecting (descriptive) | 629 | 364 | 363 |
| paired | collecting (descriptive) | 2516 | 2418 | 2413 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0241131 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00448446 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000757033 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000699337 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.98% | 14.66% | 50.53% | 11.28% | 93.9725 | 902.969 |
| ordinary/B2_10 | -10.84% | 14.28% | 49.39% | 11.16% | 68.6963 | 815.177 |
| ordinary/VOL_05 | -9.06% | 16.28% | 38.16% | 9.69% | 13.0195 | 98.0562 |
| ordinary/VOL_10 | -8.62% | 15.43% | 39.24% | 9.20% | 8.70122 | 65.5761 |
| stressed/B2_05 | -11.51% | 14.65% | 50.53% | 11.75% | 94.0518 | 1470.45 |
| stressed/B2_10 | -11.23% | 14.24% | 49.40% | 11.49% | 68.7568 | 1229.59 |
| stressed/VOL_05 | -9.14% | 16.27% | 38.17% | 9.72% | 13.0264 | 178.068 |
| stressed/VOL_10 | -8.67% | 15.42% | 39.25% | 9.21% | 8.71237 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.52% | 0.0353719 |
| calibrated | 67.59% | 0.0342892 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2413 | 1418 | 995 | 47.88% |
| 60m | perp_synchronized_clock | 2413 | 1418 | 995 | 47.88% |
| 60m | combined_synchronized_clock | 2413 | 1395 | 1018 | 47.89% |
| 15m | perp_original_clock | 2413 | 1418 | 995 | 48.03% |
| 15m | perp_synchronized_clock | 2413 | 1418 | 995 | 48.03% |
| 15m | combined_synchronized_clock | 2413 | 1395 | 1018 | 46.95% |

## Data usability pilots

- Options: 629 captures; usable 7d RR25 in 530, usable 30d RR25 in 293; 482 valid hourly changes.
- Liquidations: 1767 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2411}`.
- Exchange stress: 1258/1258 scheduled records. Capture states: `{"missed": 45, "ok": 1213}`. Ratings: `{"low": 1213}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
