# Market studies

Generated 2026-11-17T08:23:31.076Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 142 | 106 | 106 |
| range | collecting (descriptive) | 142 | 99 | 93 |
| state | collecting (descriptive) | 567 | 346 | 344 |
| paired | collecting (descriptive) | 2266 | 2168 | 2163 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0766108 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00379275 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000566108 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000780166 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 63.44% | 0.0331435 |
| calibrated | 62.37% | 0.0304712 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2163 | 1280 | 883 | 48.20% |
| 60m | perp_synchronized_clock | 2163 | 1280 | 883 | 48.20% |
| 60m | combined_synchronized_clock | 2163 | 1265 | 898 | 48.30% |
| 15m | perp_original_clock | 2163 | 1280 | 883 | 48.20% |
| 15m | perp_synchronized_clock | 2163 | 1280 | 883 | 48.20% |
| 15m | combined_synchronized_clock | 2163 | 1265 | 898 | 47.35% |

## Data usability pilots

- Options: 567 captures; usable 7d RR25 in 487, usable 30d RR25 in 237; 445 valid hourly changes.
- Liquidations: 1581 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2163}`.
- Exchange stress: 1133/1133 scheduled records. Capture states: `{"missed": 45, "ok": 1088}`. Ratings: `{"low": 1088}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
