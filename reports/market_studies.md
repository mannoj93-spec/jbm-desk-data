# Market studies

Generated 2026-10-28T04:40:25.613Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 21 | 19 | 19 |
| range | collecting (descriptive) | 21 | 13 | 6 |
| state | collecting (descriptive) | 83 | 54 | 49 |
| paired | collecting (descriptive) | 331 | 245 | 240 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.3503 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00635542 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00123844 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00442708 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.14% | 9.66% | 48.76% | 0.84% | 138.234 | 137.08 |
| ordinary/B2_10 | 0.22% | 9.43% | 49.16% | 0.77% | 89.5688 | 88.8705 |
| ordinary/VOL_05 | 0.31% | 8.93% | 47.49% | 0.67% | 52.6098 | 52.2225 |
| ordinary/VOL_10 | 0.31% | 8.93% | 47.49% | 0.67% | 52.6098 | 52.2225 |
| stressed/B2_05 | 0.03% | 9.61% | 48.76% | 0.88% | 138.373 | 249.236 |
| stressed/B2_10 | 0.14% | 9.31% | 49.17% | 0.78% | 89.6831 | 161.642 |
| stressed/VOL_05 | 0.27% | 8.83% | 47.51% | 0.67% | 52.6785 | 94.9864 |
| stressed/VOL_10 | 0.27% | 8.83% | 47.51% | 0.67% | 52.6785 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 83.33% | 0.0329508 |
| calibrated | 83.33% | 0.0264782 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 240 | 150 | 90 | 50.67% |
| 60m | perp_synchronized_clock | 240 | 150 | 90 | 50.67% |
| 60m | combined_synchronized_clock | 240 | 155 | 85 | 49.68% |
| 15m | perp_original_clock | 240 | 150 | 90 | 47.33% |
| 15m | perp_synchronized_clock | 240 | 150 | 90 | 47.33% |
| 15m | combined_synchronized_clock | 240 | 155 | 85 | 47.10% |

## Data usability pilots

- Options: 83 captures; usable 7d RR25 in 78, usable 30d RR25 in 83; 74 valid hourly changes.
- Liquidations: 151 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 245}`.
- Exchange stress: 166/166 scheduled records. Capture states: `{"missed": 39, "ok": 127}`. Ratings: `{"low": 127}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
