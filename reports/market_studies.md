# Market studies

Generated 2026-11-25T21:03:13.125Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 193 | 156 | 156 |
| range | collecting (descriptive) | 193 | 148 | 142 |
| state | collecting (descriptive) | 772 | 391 | 391 |
| paired | collecting (descriptive) | 3085 | 2987 | 2982 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.396555 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00159471 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00129946 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.91% | 16.23% | 45.47% | 13.92% | 86.1534 | 979.787 |
| ordinary/B2_10 | -11.52% | 14.83% | 44.08% | 13.13% | 56.6612 | 815.177 |
| ordinary/VOL_05 | -9.86% | 16.94% | 35.57% | 11.99% | 10.7232 | 98.0562 |
| ordinary/VOL_10 | -9.57% | 17.24% | 37.24% | 11.91% | 7.16542 | 65.5761 |
| stressed/B2_05 | -12.49% | 16.24% | 45.48% | 14.39% | 86.2456 | 1609.25 |
| stressed/B2_10 | -11.91% | 14.81% | 44.09% | 13.45% | 56.7303 | 1229.59 |
| stressed/VOL_05 | -9.94% | 16.93% | 35.57% | 12.02% | 10.7294 | 178.068 |
| stressed/VOL_10 | -9.62% | 17.23% | 37.25% | 11.93% | 7.17468 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.90% | 0.0390949 |
| calibrated | 69.72% | 0.041725 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2982 | 1678 | 1304 | 48.33% |
| 60m | perp_synchronized_clock | 2982 | 1678 | 1304 | 48.33% |
| 60m | combined_synchronized_clock | 2982 | 1648 | 1334 | 48.54% |
| 15m | perp_original_clock | 2982 | 1678 | 1304 | 48.57% |
| 15m | perp_synchronized_clock | 2982 | 1678 | 1304 | 48.57% |
| 15m | combined_synchronized_clock | 2982 | 1648 | 1334 | 47.63% |

## Data usability pilots

- Options: 770 captures; usable 7d RR25 in 662, usable 30d RR25 in 413; 607 valid hourly changes.
- Liquidations: 2193 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2979}`.
- Exchange stress: 1543/1543 scheduled records. Capture states: `{"missed": 45, "ok": 1498}`. Ratings: `{"low": 1498}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
