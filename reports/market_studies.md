# Market studies

Generated 2026-11-22T01:17:11.450Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 170 | 133 | 133 |
| range | collecting (descriptive) | 170 | 126 | 120 |
| state | collecting (descriptive) | 680 | 371 | 370 |
| paired | collecting (descriptive) | 2718 | 2620 | 2615 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.242097 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 9.89405e-05 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00154758 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000645315 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.05% | 16.45% | 48.56% | 13.92% | 90.5153 | 928.525 |
| ordinary/B2_10 | -11.45% | 15.08% | 47.21% | 13.13% | 63.7995 | 815.177 |
| ordinary/VOL_05 | -9.78% | 17.23% | 37.09% | 11.99% | 12.0846 | 98.0562 |
| ordinary/VOL_10 | -9.46% | 17.15% | 38.41% | 11.91% | 8.07603 | 65.5761 |
| stressed/B2_05 | -12.59% | 16.46% | 48.57% | 14.39% | 90.6 | 1516.64 |
| stressed/B2_10 | -11.83% | 15.05% | 47.22% | 13.45% | 63.8642 | 1229.59 |
| stressed/VOL_05 | -9.85% | 17.22% | 37.10% | 12.02% | 12.0913 | 178.068 |
| stressed/VOL_10 | -9.51% | 17.15% | 38.42% | 11.93% | 8.08641 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.00% | 0.036287 |
| calibrated | 66.67% | 0.0361877 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2615 | 1509 | 1106 | 48.24% |
| 60m | perp_synchronized_clock | 2615 | 1509 | 1106 | 48.24% |
| 60m | combined_synchronized_clock | 2615 | 1486 | 1129 | 48.25% |
| 15m | perp_original_clock | 2615 | 1509 | 1106 | 48.71% |
| 15m | perp_synchronized_clock | 2615 | 1509 | 1106 | 48.71% |
| 15m | combined_synchronized_clock | 2615 | 1486 | 1129 | 47.78% |

## Data usability pilots

- Options: 679 captures; usable 7d RR25 in 576, usable 30d RR25 in 335; 523 valid hourly changes.
- Liquidations: 1917 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2611}`.
- Exchange stress: 1359/1359 scheduled records. Capture states: `{"missed": 45, "ok": 1314}`. Ratings: `{"low": 1314}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
