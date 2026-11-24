# Market studies

Generated 2026-11-24T00:47:36.164Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 182 | 145 | 145 |
| range | collecting (descriptive) | 182 | 138 | 132 |
| state | collecting (descriptive) | 727 | 379 | 378 |
| paired | collecting (descriptive) | 2908 | 2810 | 2805 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.431413 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000751807 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00189481 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00129234 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.47% | 16.54% | 46.81% | 13.92% | 88.4822 | 958.471 |
| ordinary/B2_10 | -11.15% | 15.14% | 45.49% | 13.13% | 59.8578 | 815.177 |
| ordinary/VOL_05 | -9.43% | 17.29% | 36.26% | 11.99% | 11.3322 | 98.0562 |
| ordinary/VOL_10 | -9.05% | 17.50% | 37.78% | 11.91% | 7.57246 | 65.5761 |
| stressed/B2_05 | -12.04% | 16.55% | 46.81% | 14.39% | 88.5693 | 1570.74 |
| stressed/B2_10 | -11.54% | 15.11% | 45.50% | 13.45% | 59.9254 | 1229.59 |
| stressed/VOL_05 | -9.50% | 17.28% | 36.26% | 12.02% | 11.3386 | 178.068 |
| stressed/VOL_10 | -9.11% | 17.49% | 37.79% | 11.93% | 7.58223 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.0375735 |
| calibrated | 68.18% | 0.0388086 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2805 | 1595 | 1210 | 48.28% |
| 60m | perp_synchronized_clock | 2805 | 1595 | 1210 | 48.28% |
| 60m | combined_synchronized_clock | 2805 | 1569 | 1236 | 48.50% |
| 15m | perp_original_clock | 2805 | 1595 | 1210 | 48.78% |
| 15m | perp_synchronized_clock | 2805 | 1595 | 1210 | 48.78% |
| 15m | combined_synchronized_clock | 2805 | 1569 | 1236 | 47.93% |

## Data usability pilots

- Options: 726 captures; usable 7d RR25 in 623, usable 30d RR25 in 382; 570 valid hourly changes.
- Liquidations: 2058 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2799}`.
- Exchange stress: 1454/1454 scheduled records. Capture states: `{"missed": 45, "ok": 1409}`. Ratings: `{"low": 1409}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
