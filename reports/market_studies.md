# Market studies

Generated 2026-11-21T13:47:35.767Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 167 | 130 | 130 |
| range | collecting (descriptive) | 167 | 123 | 118 |
| state | collecting (descriptive) | 668 | 370 | 369 |
| paired | collecting (descriptive) | 2672 | 2574 | 2569 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.189461 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00145566 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.0015057 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000608213 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.71% | 16.38% | 49.00% | 13.92% | 92.0012 | 928.525 |
| ordinary/B2_10 | -12.01% | 15.04% | 47.68% | 13.13% | 64.859 | 815.177 |
| ordinary/VOL_05 | -10.44% | 17.20% | 37.33% | 11.99% | 12.2869 | 98.0562 |
| ordinary/VOL_10 | -10.25% | 17.04% | 38.59% | 11.91% | 8.21122 | 65.5761 |
| stressed/B2_05 | -13.24% | 16.38% | 49.00% | 14.39% | 92.0827 | 1516.64 |
| stressed/B2_10 | -12.39% | 15.01% | 47.69% | 13.45% | 64.9228 | 1229.59 |
| stressed/VOL_05 | -10.51% | 17.19% | 37.33% | 12.02% | 12.2936 | 178.068 |
| stressed/VOL_10 | -10.30% | 17.04% | 38.61% | 11.93% | 8.22177 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.10% | 0.0363473 |
| calibrated | 67.80% | 0.036098 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2569 | 1487 | 1082 | 48.08% |
| 60m | perp_synchronized_clock | 2569 | 1487 | 1082 | 48.08% |
| 60m | combined_synchronized_clock | 2569 | 1466 | 1103 | 48.09% |
| 15m | perp_original_clock | 2569 | 1487 | 1082 | 48.76% |
| 15m | perp_synchronized_clock | 2569 | 1487 | 1082 | 48.76% |
| 15m | combined_synchronized_clock | 2569 | 1466 | 1103 | 47.82% |

## Data usability pilots

- Options: 667 captures; usable 7d RR25 in 564, usable 30d RR25 in 323; 511 valid hourly changes.
- Liquidations: 1881 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2563}`.
- Exchange stress: 1336/1336 scheduled records. Capture states: `{"missed": 45, "ok": 1291}`. Ratings: `{"low": 1291}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
