# Market studies

Generated 2026-11-16T20:58:43.450Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 139 | 103 | 103 |
| range | collecting (descriptive) | 139 | 96 | 90 |
| state | collecting (descriptive) | 555 | 342 | 340 |
| paired | collecting (descriptive) | 2220 | 2122 | 2118 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0866222 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00369588 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000612259 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000354108 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.90% | 14.95% | 53.61% | 10.56% | 102.492 | 885.399 |
| ordinary/B2_10 | -10.02% | 14.85% | 52.93% | 10.65% | 76.8642 | 815.177 |
| ordinary/VOL_05 | -8.09% | 16.93% | 39.80% | 9.09% | 14.5885 | 98.0562 |
| ordinary/VOL_10 | -7.48% | 15.66% | 40.45% | 8.49% | 9.75531 | 65.5761 |
| stressed/B2_05 | -10.42% | 14.94% | 53.61% | 11.01% | 102.548 | 1438.78 |
| stressed/B2_10 | -10.41% | 14.81% | 52.94% | 10.98% | 76.9117 | 1229.59 |
| stressed/VOL_05 | -8.17% | 16.91% | 39.81% | 9.12% | 14.5958 | 178.068 |
| stressed/VOL_10 | -7.53% | 15.64% | 40.47% | 8.50% | 9.76771 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 62.22% | 0.0325681 |
| calibrated | 61.11% | 0.0295834 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2118 | 1256 | 862 | 48.33% |
| 60m | perp_synchronized_clock | 2118 | 1256 | 862 | 48.33% |
| 60m | combined_synchronized_clock | 2118 | 1244 | 874 | 48.31% |
| 15m | perp_original_clock | 2118 | 1256 | 862 | 47.93% |
| 15m | perp_synchronized_clock | 2118 | 1256 | 862 | 47.93% |
| 15m | combined_synchronized_clock | 2118 | 1244 | 874 | 47.11% |

## Data usability pilots

- Options: 555 captures; usable 7d RR25 in 475, usable 30d RR25 in 225; 434 valid hourly changes.
- Liquidations: 1545 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2115}`.
- Exchange stress: 1110/1110 scheduled records. Capture states: `{"missed": 45, "ok": 1065}`. Ratings: `{"low": 1065}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
