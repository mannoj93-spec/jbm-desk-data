# Market studies

Generated 2026-11-26T00:05:18.362Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 194 | 156 | 156 |
| range | collecting (descriptive) | 194 | 148 | 143 |
| state | collecting (descriptive) | 775 | 391 | 391 |
| paired | collecting (descriptive) | 3097 | 2999 | 2994 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.396555 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00173119 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00123163 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 67.13% | 0.0392203 |
| calibrated | 69.93% | 0.0419796 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2994 | 1685 | 1309 | 48.19% |
| 60m | perp_synchronized_clock | 2994 | 1685 | 1309 | 48.19% |
| 60m | combined_synchronized_clock | 2994 | 1654 | 1340 | 48.37% |
| 15m | perp_original_clock | 2994 | 1685 | 1309 | 48.61% |
| 15m | perp_synchronized_clock | 2994 | 1685 | 1309 | 48.61% |
| 15m | combined_synchronized_clock | 2994 | 1654 | 1340 | 47.58% |

## Data usability pilots

- Options: 773 captures; usable 7d RR25 in 665, usable 30d RR25 in 413; 608 valid hourly changes.
- Liquidations: 2202 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2991}`.
- Exchange stress: 1549/1549 scheduled records. Capture states: `{"missed": 45, "ok": 1504}`. Ratings: `{"low": 1504}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
