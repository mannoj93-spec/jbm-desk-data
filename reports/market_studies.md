# Market studies

Generated 2026-11-21T08:20:03.263Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 166 | 129 | 129 |
| range | collecting (descriptive) | 166 | 122 | 116 |
| state | collecting (descriptive) | 663 | 369 | 368 |
| paired | collecting (descriptive) | 2650 | 2552 | 2547 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.171287 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00285916 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000914909 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000809776 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.94% | 16.38% | 49.15% | 13.92% | 92.5024 | 928.525 |
| ordinary/B2_10 | -12.22% | 15.05% | 47.85% | 13.13% | 65.217 | 815.177 |
| ordinary/VOL_05 | -10.68% | 17.21% | 37.41% | 11.99% | 12.3551 | 98.0562 |
| ordinary/VOL_10 | -10.53% | 17.04% | 38.66% | 11.91% | 8.25678 | 65.5761 |
| stressed/B2_05 | -13.48% | 16.38% | 49.16% | 14.39% | 92.5827 | 1516.64 |
| stressed/B2_10 | -12.60% | 15.01% | 47.86% | 13.45% | 65.2805 | 1229.59 |
| stressed/VOL_05 | -10.75% | 17.20% | 37.41% | 12.02% | 12.3618 | 178.068 |
| stressed/VOL_10 | -10.58% | 17.03% | 38.67% | 11.93% | 8.26738 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.24% | 0.0363398 |
| calibrated | 68.97% | 0.0359353 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2547 | 1478 | 1069 | 48.11% |
| 60m | perp_synchronized_clock | 2547 | 1478 | 1069 | 48.11% |
| 60m | combined_synchronized_clock | 2547 | 1457 | 1090 | 48.18% |
| 15m | perp_original_clock | 2547 | 1478 | 1069 | 48.71% |
| 15m | perp_synchronized_clock | 2547 | 1478 | 1069 | 48.71% |
| 15m | combined_synchronized_clock | 2547 | 1457 | 1090 | 47.70% |

## Data usability pilots

- Options: 662 captures; usable 7d RR25 in 559, usable 30d RR25 in 318; 506 valid hourly changes.
- Liquidations: 1867 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 13, "missed": 66, "ok": 2544}`.
- Exchange stress: 1325/1325 scheduled records. Capture states: `{"missed": 45, "ok": 1280}`. Ratings: `{"low": 1280}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
