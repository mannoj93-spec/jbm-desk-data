# Market studies

Generated 2026-11-17T04:47:17.074Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 141 | 105 | 105 |
| range | collecting (descriptive) | 141 | 98 | 92 |
| state | collecting (descriptive) | 563 | 345 | 343 |
| paired | collecting (descriptive) | 2252 | 2154 | 2148 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.117497 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00373764 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000508254 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00055284 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.87% | 14.85% | 53.25% | 10.56% | 102.025 | 890.73 |
| ordinary/B2_10 | -10.01% | 14.74% | 52.52% | 10.65% | 75.9188 | 815.177 |
| ordinary/VOL_05 | -8.09% | 16.80% | 39.61% | 9.09% | 14.4063 | 98.0562 |
| ordinary/VOL_10 | -7.47% | 15.55% | 40.31% | 8.49% | 9.63271 | 65.5761 |
| stressed/B2_05 | -10.39% | 14.84% | 53.25% | 11.01% | 102.084 | 1448.42 |
| stressed/B2_10 | -10.40% | 14.70% | 52.53% | 10.98% | 75.9683 | 1229.59 |
| stressed/VOL_05 | -8.16% | 16.78% | 39.62% | 9.12% | 14.4135 | 178.068 |
| stressed/VOL_10 | -7.52% | 15.54% | 40.33% | 8.50% | 9.64497 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 63.04% | 0.0329825 |
| calibrated | 61.96% | 0.0301848 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2148 | 1274 | 874 | 48.19% |
| 60m | perp_synchronized_clock | 2148 | 1274 | 874 | 48.19% |
| 60m | combined_synchronized_clock | 2148 | 1259 | 889 | 48.21% |
| 15m | perp_original_clock | 2148 | 1274 | 874 | 48.12% |
| 15m | perp_synchronized_clock | 2148 | 1274 | 874 | 48.12% |
| 15m | combined_synchronized_clock | 2148 | 1259 | 889 | 47.18% |

## Data usability pilots

- Options: 563 captures; usable 7d RR25 in 483, usable 30d RR25 in 233; 441 valid hourly changes.
- Liquidations: 1569 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2147}`.
- Exchange stress: 1126/1126 scheduled records. Capture states: `{"missed": 45, "ok": 1081}`. Ratings: `{"low": 1081}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
