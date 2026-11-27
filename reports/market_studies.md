# Market studies

Generated 2026-11-27T06:32:40.385Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 201 | 164 | 164 |
| range | collecting (descriptive) | 201 | 156 | 150 |
| state | collecting (descriptive) | 805 | 398 | 396 |
| paired | collecting (descriptive) | 3219 | 3121 | 3116 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.366283 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00267031 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00112878 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00168485 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.45% | 15.98% | 44.63% | 13.92% | 84.6853 | 996.551 |
| ordinary/B2_10 | -11.09% | 14.59% | 43.17% | 13.13% | 54.53 | 815.177 |
| ordinary/VOL_05 | -9.36% | 16.66% | 35.12% | 11.99% | 10.3172 | 98.0562 |
| ordinary/VOL_10 | -8.97% | 16.99% | 36.90% | 11.91% | 6.89386 | 65.5761 |
| stressed/B2_05 | -12.05% | 15.99% | 44.63% | 14.39% | 84.78 | 1639.22 |
| stressed/B2_10 | -11.48% | 14.57% | 43.18% | 13.45% | 54.5997 | 1229.59 |
| stressed/VOL_05 | -9.43% | 16.65% | 35.13% | 12.02% | 10.3232 | 178.068 |
| stressed/VOL_10 | -9.02% | 16.98% | 36.91% | 11.93% | 6.90278 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.00% | 0.0400526 |
| calibrated | 70.67% | 0.043664 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3116 | 1755 | 1361 | 48.15% |
| 60m | perp_synchronized_clock | 3116 | 1755 | 1361 | 48.15% |
| 60m | combined_synchronized_clock | 3116 | 1719 | 1397 | 48.46% |
| 15m | perp_original_clock | 3116 | 1755 | 1361 | 48.66% |
| 15m | perp_synchronized_clock | 3116 | 1755 | 1361 | 48.66% |
| 15m | combined_synchronized_clock | 3116 | 1719 | 1397 | 47.59% |

## Data usability pilots

- Options: 804 captures; usable 7d RR25 in 693, usable 30d RR25 in 413; 632 valid hourly changes.
- Liquidations: 2292 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3111}`.
- Exchange stress: 1610/1610 scheduled records. Capture states: `{"missed": 45, "ok": 1565}`. Ratings: `{"low": 1565}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
