# Market studies

Generated 2026-11-27T20:22:46.711Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 205 | 168 | 168 |
| range | collecting (descriptive) | 205 | 160 | 153 |
| state | collecting (descriptive) | 819 | 402 | 401 |
| paired | collecting (descriptive) | 3274 | 3176 | 3171 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.354784 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00303188 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000750741 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00175418 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.02% | 15.95% | 44.20% | 13.92% | 84.2371 | 1007.18 |
| ordinary/B2_10 | -11.62% | 14.56% | 42.74% | 13.13% | 53.518 | 815.177 |
| ordinary/VOL_05 | -9.98% | 16.63% | 34.92% | 11.99% | 10.1245 | 98.0562 |
| ordinary/VOL_10 | -9.70% | 17.02% | 36.75% | 11.91% | 6.76485 | 65.5761 |
| stressed/B2_05 | -12.63% | 15.96% | 44.20% | 14.39% | 84.3314 | 1658.42 |
| stressed/B2_10 | -12.00% | 14.54% | 42.75% | 13.45% | 53.5878 | 1229.59 |
| stressed/VOL_05 | -10.05% | 16.62% | 34.92% | 12.02% | 10.1304 | 178.068 |
| stressed/VOL_10 | -9.75% | 17.02% | 36.76% | 11.93% | 6.77362 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.63% | 0.0403701 |
| calibrated | 71.24% | 0.0443245 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3171 | 1781 | 1390 | 48.34% |
| 60m | perp_synchronized_clock | 3171 | 1781 | 1390 | 48.34% |
| 60m | combined_synchronized_clock | 3171 | 1744 | 1427 | 48.68% |
| 15m | perp_original_clock | 3171 | 1781 | 1390 | 48.68% |
| 15m | perp_synchronized_clock | 3171 | 1781 | 1390 | 48.68% |
| 15m | combined_synchronized_clock | 3171 | 1744 | 1427 | 47.71% |

## Data usability pilots

- Options: 818 captures; usable 7d RR25 in 707, usable 30d RR25 in 413; 644 valid hourly changes.
- Liquidations: 2334 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3167}`.
- Exchange stress: 1637/1637 scheduled records. Capture states: `{"missed": 45, "ok": 1592}`. Ratings: `{"low": 1592}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
