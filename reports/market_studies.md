# Market studies

Generated 2026-11-26T04:13:17.252Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 195 | 158 | 158 |
| range | collecting (descriptive) | 195 | 150 | 144 |
| state | collecting (descriptive) | 779 | 391 | 391 |
| paired | collecting (descriptive) | 3113 | 3015 | 3010 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.311795 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00186485 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00122508 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.68% | 16.18% | 45.22% | 13.92% | 86.5232 | 990.918 |
| ordinary/B2_10 | -11.25% | 14.81% | 43.85% | 13.13% | 56.1229 | 815.177 |
| ordinary/VOL_05 | -9.55% | 16.90% | 35.45% | 11.99% | 10.6206 | 98.0562 |
| ordinary/VOL_10 | -9.19% | 17.22% | 37.16% | 11.91% | 7.09681 | 65.5761 |
| stressed/B2_05 | -12.28% | 16.19% | 45.23% | 14.39% | 86.6141 | 1629.05 |
| stressed/B2_10 | -11.64% | 14.78% | 43.86% | 13.45% | 56.1922 | 1229.59 |
| stressed/VOL_05 | -9.62% | 16.90% | 35.46% | 12.02% | 10.6267 | 178.068 |
| stressed/VOL_10 | -9.24% | 17.22% | 37.17% | 11.93% | 7.10599 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.36% | 0.0393223 |
| calibrated | 70.14% | 0.0422082 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3010 | 1696 | 1314 | 48.23% |
| 60m | perp_synchronized_clock | 3010 | 1696 | 1314 | 48.23% |
| 60m | combined_synchronized_clock | 3010 | 1665 | 1345 | 48.41% |
| 15m | perp_original_clock | 3010 | 1696 | 1314 | 48.53% |
| 15m | perp_synchronized_clock | 3010 | 1696 | 1314 | 48.53% |
| 15m | combined_synchronized_clock | 3010 | 1665 | 1345 | 47.51% |

## Data usability pilots

- Options: 777 captures; usable 7d RR25 in 668, usable 30d RR25 in 413; 610 valid hourly changes.
- Liquidations: 2214 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3007}`.
- Exchange stress: 1557/1557 scheduled records. Capture states: `{"missed": 45, "ok": 1512}`. Ratings: `{"low": 1512}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
