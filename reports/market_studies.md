# Market studies

Generated 2026-11-19T00:20:25.255Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 152 | 116 | 116 |
| range | collecting (descriptive) | 152 | 109 | 102 |
| state | collecting (descriptive) | 607 | 360 | 359 |
| paired | collecting (descriptive) | 2426 | 2328 | 2323 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.00257471 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00423351 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000609052 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000672622 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.83% | 14.76% | 51.28% | 11.22% | 96.8398 | 902.969 |
| ordinary/B2_10 | -10.73% | 14.44% | 50.30% | 11.12% | 70.8 | 815.177 |
| ordinary/VOL_05 | -8.93% | 16.47% | 38.59% | 9.64% | 13.4227 | 98.0562 |
| ordinary/VOL_10 | -8.46% | 15.53% | 39.56% | 9.14% | 8.97181 | 65.5761 |
| stressed/B2_05 | -11.36% | 14.75% | 51.29% | 11.70% | 96.9124 | 1470.45 |
| stressed/B2_10 | -11.11% | 14.40% | 50.31% | 11.45% | 70.8577 | 1229.59 |
| stressed/VOL_05 | -9.00% | 16.46% | 38.59% | 9.67% | 13.4298 | 178.068 |
| stressed/VOL_10 | -8.51% | 15.52% | 39.57% | 9.15% | 8.98328 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.0344892 |
| calibrated | 65.69% | 0.0328281 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2323 | 1371 | 952 | 48.21% |
| 60m | perp_synchronized_clock | 2323 | 1371 | 952 | 48.21% |
| 60m | combined_synchronized_clock | 2323 | 1350 | 973 | 48.22% |
| 15m | perp_original_clock | 2323 | 1371 | 952 | 48.07% |
| 15m | perp_synchronized_clock | 2323 | 1371 | 952 | 48.07% |
| 15m | combined_synchronized_clock | 2323 | 1350 | 973 | 47.04% |

## Data usability pilots

- Options: 607 captures; usable 7d RR25 in 514, usable 30d RR25 in 277; 467 valid hourly changes.
- Liquidations: 1701 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2323}`.
- Exchange stress: 1213/1213 scheduled records. Capture states: `{"missed": 45, "ok": 1168}`. Ratings: `{"low": 1168}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
