# Market studies

Generated 2026-11-25T14:32:55.825Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 191 | 154 | 154 |
| range | collecting (descriptive) | 191 | 147 | 141 |
| state | collecting (descriptive) | 765 | 391 | 391 |
| paired | collecting (descriptive) | 3059 | 2961 | 2956 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.368924 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0014563 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00131089 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.46% | 16.11% | 45.70% | 13.92% | 86.9889 | 979.787 |
| ordinary/B2_10 | -12.01% | 14.73% | 44.33% | 13.13% | 57.2147 | 815.177 |
| ordinary/VOL_05 | -10.43% | 16.84% | 35.69% | 11.99% | 10.8285 | 98.0562 |
| ordinary/VOL_10 | -10.24% | 17.07% | 37.34% | 11.91% | 7.23574 | 65.5761 |
| stressed/B2_05 | -13.04% | 16.12% | 45.71% | 14.39% | 87.0793 | 1609.25 |
| stressed/B2_10 | -12.39% | 14.71% | 44.34% | 13.45% | 57.2836 | 1229.59 |
| stressed/VOL_05 | -10.51% | 16.83% | 35.70% | 12.02% | 10.8347 | 178.068 |
| stressed/VOL_10 | -10.29% | 17.06% | 37.35% | 11.93% | 7.24509 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.038953 |
| calibrated | 69.50% | 0.041452 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2956 | 1669 | 1287 | 48.41% |
| 60m | perp_synchronized_clock | 2956 | 1669 | 1287 | 48.41% |
| 60m | combined_synchronized_clock | 2956 | 1639 | 1317 | 48.63% |
| 15m | perp_original_clock | 2956 | 1669 | 1287 | 48.71% |
| 15m | perp_synchronized_clock | 2956 | 1669 | 1287 | 48.71% |
| 15m | combined_synchronized_clock | 2956 | 1639 | 1317 | 47.77% |

## Data usability pilots

- Options: 764 captures; usable 7d RR25 in 660, usable 30d RR25 in 413; 606 valid hourly changes.
- Liquidations: 2172 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2951}`.
- Exchange stress: 1530/1530 scheduled records. Capture states: `{"missed": 45, "ok": 1485}`. Ratings: `{"low": 1485}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
