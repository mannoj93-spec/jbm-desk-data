# Market studies

Generated 2026-11-16T19:47:17.910Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 138 | 102 | 102 |
| range | collecting (descriptive) | 138 | 96 | 90 |
| state | collecting (descriptive) | 554 | 342 | 339 |
| paired | collecting (descriptive) | 2216 | 2118 | 2113 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0879538 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00369588 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000877867 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000354946 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.04% | 14.99% | 53.85% | 10.56% | 102.493 | 880.327 |
| ordinary/B2_10 | -10.15% | 14.89% | 53.18% | 10.65% | 77.4414 | 815.177 |
| ordinary/VOL_05 | -8.25% | 16.98% | 39.92% | 9.09% | 14.6994 | 98.0562 |
| ordinary/VOL_10 | -7.66% | 15.69% | 40.54% | 8.49% | 9.82991 | 65.5761 |
| stressed/B2_05 | -10.55% | 14.98% | 53.85% | 11.01% | 102.549 | 1429.62 |
| stressed/B2_10 | -10.54% | 14.85% | 53.19% | 10.98% | 77.488 | 1229.59 |
| stressed/VOL_05 | -8.33% | 16.96% | 39.93% | 9.12% | 14.7068 | 178.068 |
| stressed/VOL_10 | -7.71% | 15.68% | 40.55% | 8.50% | 9.84241 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 62.22% | 0.0325681 |
| calibrated | 61.11% | 0.0295834 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2113 | 1255 | 858 | 48.37% |
| 60m | perp_synchronized_clock | 2113 | 1255 | 858 | 48.37% |
| 60m | combined_synchronized_clock | 2113 | 1243 | 870 | 48.35% |
| 15m | perp_original_clock | 2113 | 1255 | 858 | 47.97% |
| 15m | perp_synchronized_clock | 2113 | 1255 | 858 | 47.97% |
| 15m | combined_synchronized_clock | 2113 | 1243 | 870 | 47.14% |

## Data usability pilots

- Options: 554 captures; usable 7d RR25 in 474, usable 30d RR25 in 224; 433 valid hourly changes.
- Liquidations: 1542 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2111}`.
- Exchange stress: 1108/1108 scheduled records. Capture states: `{"missed": 45, "ok": 1063}`. Ratings: `{"low": 1063}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
