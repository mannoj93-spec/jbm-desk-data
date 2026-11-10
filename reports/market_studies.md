# Market studies

Generated 2026-11-10T12:20:14.942Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 101 | 65 | 65 |
| range | collecting (descriptive) | 101 | 59 | 52 |
| state | collecting (descriptive) | 403 | 286 | 281 |
| paired | collecting (descriptive) | 1610 | 1516 | 1511 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0194724 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00486312 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000275773 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00049636 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.08% | 13.34% | 62.55% | 5.43% | 108.157 | 704.412 |
| ordinary/B2_10 | -5.52% | 14.28% | 61.96% | 5.95% | 86.2408 | 645.645 |
| ordinary/VOL_05 | -3.58% | 16.76% | 42.67% | 4.35% | 15.8285 | 78.3691 |
| ordinary/VOL_10 | -3.43% | 15.51% | 43.87% | 4.14% | 13.2649 | 65.5761 |
| stressed/B2_05 | -5.50% | 13.31% | 62.55% | 5.78% | 108.176 | 1137.05 |
| stressed/B2_10 | -5.85% | 14.21% | 61.97% | 6.23% | 86.257 | 990.266 |
| stressed/VOL_05 | -3.64% | 16.72% | 42.68% | 4.36% | 15.8382 | 142.3 |
| stressed/VOL_10 | -3.49% | 15.49% | 43.88% | 4.15% | 13.2813 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.31% | 0.0285525 |
| calibrated | 63.46% | 0.0234324 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1511 | 931 | 580 | 48.44% |
| 60m | perp_synchronized_clock | 1511 | 931 | 580 | 48.44% |
| 60m | combined_synchronized_clock | 1511 | 919 | 592 | 48.42% |
| 15m | perp_original_clock | 1511 | 931 | 580 | 47.05% |
| 15m | perp_synchronized_clock | 1511 | 931 | 580 | 47.05% |
| 15m | combined_synchronized_clock | 1511 | 919 | 592 | 46.35% |

## Data usability pilots

- Options: 403 captures; usable 7d RR25 in 343, usable 30d RR25 in 90; 317 valid hourly changes.
- Liquidations: 1089 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1507}`.
- Exchange stress: 805/805 scheduled records. Capture states: `{"missed": 43, "ok": 762}`. Ratings: `{"low": 762}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
