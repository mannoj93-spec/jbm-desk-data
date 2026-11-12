# Market studies

Generated 2026-11-12T22:50:25.192Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 115 | 79 | 79 |
| range | collecting (descriptive) | 115 | 73 | 67 |
| state | collecting (descriptive) | 461 | 309 | 307 |
| paired | collecting (descriptive) | 1844 | 1749 | 1744 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.198834 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00361181 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000696243 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000680906 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -6.33% | 12.75% | 58.97% | 6.64% | 104.624 | 755.634 |
| ordinary/B2_10 | -6.64% | 13.42% | 58.25% | 6.97% | 80.5264 | 688.033 |
| ordinary/VOL_05 | -4.81% | 15.66% | 41.54% | 5.47% | 15.3299 | 86.1552 |
| ordinary/VOL_10 | -4.62% | 14.56% | 42.52% | 5.22% | 11.6823 | 65.5761 |
| stressed/B2_05 | -6.79% | 12.73% | 58.97% | 7.05% | 104.662 | 1229.67 |
| stressed/B2_10 | -6.99% | 13.36% | 58.26% | 7.26% | 80.5632 | 1052.22 |
| stressed/VOL_05 | -4.88% | 15.63% | 41.54% | 5.49% | 15.3394 | 156.448 |
| stressed/VOL_10 | -4.68% | 14.54% | 42.53% | 5.24% | 11.697 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.13% | 0.0310758 |
| calibrated | 71.64% | 0.0269584 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1744 | 1058 | 686 | 48.49% |
| 60m | perp_synchronized_clock | 1744 | 1058 | 686 | 48.49% |
| 60m | combined_synchronized_clock | 1744 | 1049 | 695 | 48.14% |
| 15m | perp_original_clock | 1744 | 1058 | 686 | 47.07% |
| 15m | perp_synchronized_clock | 1744 | 1058 | 686 | 47.07% |
| 15m | combined_synchronized_clock | 1744 | 1049 | 695 | 46.43% |

## Data usability pilots

- Options: 461 captures; usable 7d RR25 in 383, usable 30d RR25 in 142; 354 valid hourly changes.
- Liquidations: 1263 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1739}`.
- Exchange stress: 922/922 scheduled records. Capture states: `{"missed": 44, "ok": 878}`. Ratings: `{"low": 878}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
