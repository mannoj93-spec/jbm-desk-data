# Market studies

Generated 2026-11-28T04:04:27.576Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 207 | 169 | 169 |
| range | collecting (descriptive) | 207 | 161 | 155 |
| state | collecting (descriptive) | 827 | 403 | 402 |
| paired | collecting (descriptive) | 3305 | 3207 | 3202 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.347045 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0032643 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00084154 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00167864 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.97% | 15.91% | 44.09% | 13.92% | 84.3996 | 1012.4 |
| ordinary/B2_10 | -11.57% | 14.52% | 42.63% | 13.13% | 53.2739 | 815.177 |
| ordinary/VOL_05 | -9.92% | 16.59% | 34.87% | 11.99% | 10.078 | 98.0562 |
| ordinary/VOL_10 | -9.63% | 16.98% | 36.71% | 11.91% | 6.73382 | 65.5761 |
| stressed/B2_05 | -12.58% | 15.91% | 44.10% | 14.39% | 84.4937 | 1667.83 |
| stressed/B2_10 | -11.95% | 14.51% | 42.64% | 13.45% | 53.3438 | 1229.59 |
| stressed/VOL_05 | -9.99% | 16.58% | 34.87% | 12.02% | 10.0839 | 178.068 |
| stressed/VOL_10 | -9.68% | 16.97% | 36.72% | 11.93% | 6.74255 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.03% | 0.0405009 |
| calibrated | 71.61% | 0.0446758 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3202 | 1800 | 1402 | 48.44% |
| 60m | perp_synchronized_clock | 3202 | 1800 | 1402 | 48.44% |
| 60m | combined_synchronized_clock | 3202 | 1762 | 1440 | 48.75% |
| 15m | perp_original_clock | 3202 | 1800 | 1402 | 48.72% |
| 15m | perp_synchronized_clock | 3202 | 1800 | 1402 | 48.72% |
| 15m | combined_synchronized_clock | 3202 | 1762 | 1440 | 47.79% |

## Data usability pilots

- Options: 825 captures; usable 7d RR25 in 714, usable 30d RR25 in 413; 649 valid hourly changes.
- Liquidations: 2358 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3199}`.
- Exchange stress: 1653/1653 scheduled records. Capture states: `{"missed": 45, "ok": 1608}`. Ratings: `{"low": 1608}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
