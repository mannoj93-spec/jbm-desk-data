# Market studies

Generated 2026-11-20T16:52:04.166Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 162 | 126 | 126 |
| range | collecting (descriptive) | 162 | 119 | 113 |
| state | collecting (descriptive) | 647 | 365 | 365 |
| paired | collecting (descriptive) | 2588 | 2490 | 2485 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0503222 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00466713 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00076659 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000754527 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.10% | 14.85% | 49.81% | 12.39% | 91.2887 | 902.969 |
| ordinary/B2_10 | -11.73% | 14.29% | 48.53% | 12.04% | 66.7245 | 815.177 |
| ordinary/VOL_05 | -10.10% | 16.32% | 37.75% | 10.72% | 12.6422 | 98.0562 |
| ordinary/VOL_10 | -9.85% | 15.67% | 38.92% | 10.42% | 8.44844 | 65.5761 |
| stressed/B2_05 | -12.62% | 14.83% | 49.81% | 12.86% | 91.3736 | 1470.45 |
| stressed/B2_10 | -12.11% | 14.25% | 48.54% | 12.37% | 66.7872 | 1229.59 |
| stressed/VOL_05 | -10.18% | 16.30% | 37.75% | 10.75% | 12.649 | 178.068 |
| stressed/VOL_10 | -9.90% | 15.66% | 38.94% | 10.43% | 8.45928 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.03% | 0.0360084 |
| calibrated | 69.03% | 0.0353608 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2485 | 1454 | 1031 | 47.94% |
| 60m | perp_synchronized_clock | 2485 | 1454 | 1031 | 47.94% |
| 60m | combined_synchronized_clock | 2485 | 1432 | 1053 | 47.97% |
| 15m | perp_original_clock | 2485 | 1454 | 1031 | 48.42% |
| 15m | perp_synchronized_clock | 2485 | 1454 | 1031 | 48.42% |
| 15m | combined_synchronized_clock | 2485 | 1432 | 1053 | 47.42% |

## Data usability pilots

- Options: 647 captures; usable 7d RR25 in 545, usable 30d RR25 in 304; 494 valid hourly changes.
- Liquidations: 1821 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 11, "missed": 66, "ok": 2482}`.
- Exchange stress: 1294/1294 scheduled records. Capture states: `{"missed": 45, "ok": 1249}`. Ratings: `{"low": 1249}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
