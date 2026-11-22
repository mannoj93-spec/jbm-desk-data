# Market studies

Generated 2026-11-22T16:08:43.441Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 174 | 137 | 137 |
| range | collecting (descriptive) | 174 | 130 | 123 |
| state | collecting (descriptive) | 695 | 374 | 373 |
| paired | collecting (descriptive) | 2777 | 2679 | 2674 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.30033 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.000411166 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00189999 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00114529 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.77% | 16.68% | 47.99% | 13.92% | 89.2376 | 933.517 |
| ordinary/B2_10 | -11.23% | 15.24% | 46.61% | 13.13% | 62.4542 | 815.177 |
| ordinary/VOL_05 | -9.52% | 17.41% | 36.80% | 11.99% | 11.8278 | 98.0562 |
| ordinary/VOL_10 | -9.17% | 17.49% | 38.19% | 11.91% | 7.90428 | 65.5761 |
| stressed/B2_05 | -12.32% | 16.68% | 47.99% | 14.39% | 89.3244 | 1525.65 |
| stressed/B2_10 | -11.62% | 15.21% | 46.62% | 13.45% | 62.5201 | 1229.59 |
| stressed/VOL_05 | -9.60% | 17.40% | 36.80% | 12.02% | 11.8344 | 178.068 |
| stressed/VOL_10 | -9.22% | 17.48% | 38.20% | 11.93% | 7.91445 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.04% | 0.0364042 |
| calibrated | 66.67% | 0.0365207 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2674 | 1542 | 1132 | 48.25% |
| 60m | perp_synchronized_clock | 2674 | 1542 | 1132 | 48.25% |
| 60m | combined_synchronized_clock | 2674 | 1513 | 1161 | 48.38% |
| 15m | perp_original_clock | 2674 | 1542 | 1132 | 48.90% |
| 15m | perp_synchronized_clock | 2674 | 1542 | 1132 | 48.90% |
| 15m | combined_synchronized_clock | 2674 | 1513 | 1161 | 47.98% |

## Data usability pilots

- Options: 693 captures; usable 7d RR25 in 590, usable 30d RR25 in 349; 537 valid hourly changes.
- Liquidations: 1962 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2671}`.
- Exchange stress: 1389/1389 scheduled records. Capture states: `{"missed": 45, "ok": 1344}`. Ratings: `{"low": 1344}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
