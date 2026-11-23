# Market studies

Generated 2026-11-23T23:02:37.453Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 181 | 144 | 144 |
| range | collecting (descriptive) | 181 | 137 | 131 |
| state | collecting (descriptive) | 726 | 379 | 378 |
| paired | collecting (descriptive) | 2901 | 2803 | 2798 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.434206 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000597404 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00189481 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00129557 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.48% | 16.60% | 46.97% | 13.92% | 88.94 | 958.471 |
| ordinary/B2_10 | -11.16% | 15.19% | 45.62% | 13.13% | 60.1692 | 815.177 |
| ordinary/VOL_05 | -9.44% | 17.35% | 36.32% | 11.99% | 11.3916 | 98.0562 |
| ordinary/VOL_10 | -9.06% | 17.56% | 37.83% | 11.91% | 7.61224 | 65.5761 |
| stressed/B2_05 | -12.05% | 16.60% | 46.98% | 14.39% | 89.0261 | 1570.74 |
| stressed/B2_10 | -11.54% | 15.16% | 45.63% | 13.45% | 60.2367 | 1229.59 |
| stressed/VOL_05 | -9.51% | 17.34% | 36.33% | 12.02% | 11.398 | 178.068 |
| stressed/VOL_10 | -9.11% | 17.55% | 37.84% | 11.93% | 7.62205 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.41% | 0.037432 |
| calibrated | 67.94% | 0.0385164 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2798 | 1591 | 1207 | 48.33% |
| 60m | perp_synchronized_clock | 2798 | 1591 | 1207 | 48.33% |
| 60m | combined_synchronized_clock | 2798 | 1565 | 1233 | 48.56% |
| 15m | perp_original_clock | 2798 | 1591 | 1207 | 48.84% |
| 15m | perp_synchronized_clock | 2798 | 1591 | 1207 | 48.84% |
| 15m | combined_synchronized_clock | 2798 | 1565 | 1233 | 47.99% |

## Data usability pilots

- Options: 724 captures; usable 7d RR25 in 621, usable 30d RR25 in 380; 568 valid hourly changes.
- Liquidations: 2055 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2795}`.
- Exchange stress: 1451/1451 scheduled records. Capture states: `{"missed": 45, "ok": 1406}`. Ratings: `{"low": 1406}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
