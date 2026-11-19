# Market studies

Generated 2026-11-19T13:02:31.895Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 155 | 119 | 119 |
| range | collecting (descriptive) | 155 | 112 | 105 |
| state | collecting (descriptive) | 620 | 363 | 363 |
| paired | collecting (descriptive) | 2477 | 2379 | 2374 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.115386 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00436257 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000757033 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000579191 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.40% | 14.70% | 50.82% | 11.22% | 95.101 | 902.969 |
| ordinary/B2_10 | -10.38% | 14.35% | 49.75% | 11.12% | 69.5241 | 815.177 |
| ordinary/VOL_05 | -8.52% | 16.35% | 38.33% | 9.64% | 13.1781 | 98.0562 |
| ordinary/VOL_10 | -7.98% | 15.45% | 39.36% | 9.14% | 8.80768 | 65.5761 |
| stressed/B2_05 | -10.93% | 14.69% | 50.83% | 11.70% | 95.1778 | 1470.45 |
| stressed/B2_10 | -10.77% | 14.32% | 49.76% | 11.45% | 69.5835 | 1229.59 |
| stressed/VOL_05 | -8.60% | 16.34% | 38.33% | 9.67% | 13.1851 | 178.068 |
| stressed/VOL_10 | -8.03% | 15.44% | 39.37% | 9.15% | 8.81895 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.62% | 0.034931 |
| calibrated | 66.67% | 0.0335674 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2374 | 1401 | 973 | 48.04% |
| 60m | perp_synchronized_clock | 2374 | 1401 | 973 | 48.04% |
| 60m | combined_synchronized_clock | 2374 | 1379 | 995 | 48.01% |
| 15m | perp_original_clock | 2374 | 1401 | 973 | 48.04% |
| 15m | perp_synchronized_clock | 2374 | 1401 | 973 | 48.04% |
| 15m | combined_synchronized_clock | 2374 | 1379 | 995 | 46.99% |

## Data usability pilots

- Options: 619 captures; usable 7d RR25 in 526, usable 30d RR25 in 289; 479 valid hourly changes.
- Liquidations: 1740 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2375}`.
- Exchange stress: 1239/1239 scheduled records. Capture states: `{"missed": 45, "ok": 1194}`. Ratings: `{"low": 1194}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
