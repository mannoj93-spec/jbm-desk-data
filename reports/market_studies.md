# Market studies

Generated 2026-11-24T12:23:40.424Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 185 | 148 | 148 |
| range | collecting (descriptive) | 185 | 141 | 134 |
| state | collecting (descriptive) | 739 | 383 | 381 |
| paired | collecting (descriptive) | 2954 | 2856 | 2851 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.397831 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000807105 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00178539 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00127148 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.83% | 16.40% | 46.40% | 13.92% | 89.6077 | 979.787 |
| ordinary/B2_10 | -11.46% | 15.00% | 45.09% | 13.13% | 58.9489 | 815.177 |
| ordinary/VOL_05 | -9.79% | 17.14% | 36.07% | 11.99% | 11.1589 | 98.0562 |
| ordinary/VOL_10 | -9.47% | 17.36% | 37.63% | 11.91% | 7.4565 | 65.5761 |
| stressed/B2_05 | -12.41% | 16.40% | 46.41% | 14.39% | 89.6923 | 1609.25 |
| stressed/B2_10 | -11.84% | 14.98% | 45.10% | 13.45% | 59.017 | 1229.59 |
| stressed/VOL_05 | -9.86% | 17.13% | 36.07% | 12.02% | 11.1652 | 178.068 |
| stressed/VOL_10 | -9.53% | 17.35% | 37.64% | 11.93% | 7.46612 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.42% | 0.0378552 |
| calibrated | 68.66% | 0.039385 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2851 | 1620 | 1231 | 48.27% |
| 60m | perp_synchronized_clock | 2851 | 1620 | 1231 | 48.27% |
| 60m | combined_synchronized_clock | 2851 | 1594 | 1257 | 48.49% |
| 15m | perp_original_clock | 2851 | 1620 | 1231 | 48.83% |
| 15m | perp_synchronized_clock | 2851 | 1620 | 1231 | 48.83% |
| 15m | combined_synchronized_clock | 2851 | 1594 | 1257 | 47.99% |

## Data usability pilots

- Options: 738 captures; usable 7d RR25 in 635, usable 30d RR25 in 394; 582 valid hourly changes.
- Liquidations: 2094 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2847}`.
- Exchange stress: 1477/1477 scheduled records. Capture states: `{"missed": 45, "ok": 1432}`. Ratings: `{"low": 1432}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
