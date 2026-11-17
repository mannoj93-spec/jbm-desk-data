# Market studies

Generated 2026-11-17T10:02:28.053Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 142 | 106 | 106 |
| range | collecting (descriptive) | 142 | 99 | 94 |
| state | collecting (descriptive) | 569 | 346 | 345 |
| paired | collecting (descriptive) | 2273 | 2175 | 2170 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0766108 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00384669 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000722684 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000604839 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.03% | 14.79% | 53.08% | 10.56% | 101.355 | 890.73 |
| ordinary/B2_10 | -10.13% | 14.67% | 52.30% | 10.65% | 75.4196 | 815.177 |
| ordinary/VOL_05 | -8.23% | 16.72% | 39.52% | 9.09% | 14.3102 | 98.0562 |
| ordinary/VOL_10 | -7.64% | 15.49% | 40.24% | 8.49% | 9.56808 | 65.5761 |
| stressed/B2_05 | -10.56% | 14.78% | 53.08% | 11.01% | 101.415 | 1448.42 |
| stressed/B2_10 | -10.52% | 14.63% | 52.31% | 10.98% | 75.47 | 1229.59 |
| stressed/VOL_05 | -8.31% | 16.71% | 39.52% | 9.12% | 14.3175 | 178.068 |
| stressed/VOL_10 | -7.69% | 15.48% | 40.25% | 8.50% | 9.58026 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 63.83% | 0.0332957 |
| calibrated | 62.77% | 0.0307461 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2170 | 1286 | 884 | 48.21% |
| 60m | perp_synchronized_clock | 2170 | 1286 | 884 | 48.21% |
| 60m | combined_synchronized_clock | 2170 | 1269 | 901 | 48.23% |
| 15m | perp_original_clock | 2170 | 1286 | 884 | 48.21% |
| 15m | perp_synchronized_clock | 2170 | 1286 | 884 | 48.21% |
| 15m | combined_synchronized_clock | 2170 | 1269 | 901 | 47.28% |

## Data usability pilots

- Options: 568 captures; usable 7d RR25 in 488, usable 30d RR25 in 238; 446 valid hourly changes.
- Liquidations: 1587 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2171}`.
- Exchange stress: 1137/1137 scheduled records. Capture states: `{"missed": 45, "ok": 1092}`. Ratings: `{"low": 1092}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
