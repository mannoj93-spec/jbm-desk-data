# Market studies

Generated 2026-11-28T00:21:43.974Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 206 | 169 | 169 |
| range | collecting (descriptive) | 206 | 161 | 154 |
| state | collecting (descriptive) | 823 | 402 | 402 |
| paired | collecting (descriptive) | 3290 | 3192 | 3187 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.347045 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00314927 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00084154 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00168654 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 68.83% | 0.0404357 |
| calibrated | 71.43% | 0.0445015 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3187 | 1789 | 1398 | 48.35% |
| 60m | perp_synchronized_clock | 3187 | 1789 | 1398 | 48.35% |
| 60m | combined_synchronized_clock | 3187 | 1751 | 1436 | 48.66% |
| 15m | perp_original_clock | 3187 | 1789 | 1398 | 48.74% |
| 15m | perp_synchronized_clock | 3187 | 1789 | 1398 | 48.74% |
| 15m | combined_synchronized_clock | 3187 | 1751 | 1436 | 47.80% |

## Data usability pilots

- Options: 822 captures; usable 7d RR25 in 711, usable 30d RR25 in 413; 647 valid hourly changes.
- Liquidations: 2346 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3183}`.
- Exchange stress: 1645/1645 scheduled records. Capture states: `{"missed": 45, "ok": 1600}`. Ratings: `{"low": 1600}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
