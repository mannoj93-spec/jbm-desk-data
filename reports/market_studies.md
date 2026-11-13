# Market studies

Generated 2026-11-13T16:02:35.823Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 120 | 83 | 83 |
| range | collecting (descriptive) | 120 | 77 | 71 |
| state | collecting (descriptive) | 479 | 313 | 312 |
| paired | collecting (descriptive) | 1913 | 1818 | 1813 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.274265 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00392772 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000143014 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000310259 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -7.47% | 13.98% | 58.00% | 8.02% | 104.573 | 774.472 |
| ordinary/B2_10 | -7.58% | 14.36% | 57.38% | 8.24% | 77.9692 | 688.033 |
| ordinary/VOL_05 | -5.98% | 16.90% | 41.46% | 7.03% | 14.8363 | 86.1552 |
| ordinary/VOL_10 | -5.57% | 15.35% | 42.15% | 6.49% | 11.3049 | 65.5761 |
| stressed/B2_05 | -7.93% | 13.95% | 58.01% | 8.44% | 104.613 | 1263.75 |
| stressed/B2_10 | -7.93% | 14.31% | 57.39% | 8.53% | 78.0112 | 1052.22 |
| stressed/VOL_05 | -6.04% | 16.87% | 41.46% | 7.05% | 14.8455 | 156.448 |
| stressed/VOL_10 | -5.62% | 15.34% | 42.17% | 6.51% | 11.3191 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 70.42% | 0.0313719 |
| calibrated | 69.01% | 0.0274426 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1813 | 1098 | 715 | 48.54% |
| 60m | perp_synchronized_clock | 1813 | 1098 | 715 | 48.54% |
| 60m | combined_synchronized_clock | 1813 | 1087 | 726 | 48.30% |
| 15m | perp_original_clock | 1813 | 1098 | 715 | 47.63% |
| 15m | perp_synchronized_clock | 1813 | 1098 | 715 | 47.63% |
| 15m | combined_synchronized_clock | 1813 | 1087 | 726 | 46.92% |

## Data usability pilots

- Options: 478 captures; usable 7d RR25 in 398, usable 30d RR25 in 148; 367 valid hourly changes.
- Liquidations: 1317 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1811}`.
- Exchange stress: 957/957 scheduled records. Capture states: `{"missed": 44, "ok": 913}`. Ratings: `{"low": 913}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
