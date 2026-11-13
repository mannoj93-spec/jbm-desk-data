# Market studies

Generated 2026-11-13T08:21:39.395Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 118 | 82 | 82 |
| range | collecting (descriptive) | 118 | 76 | 69 |
| state | collecting (descriptive) | 471 | 312 | 311 |
| paired | collecting (descriptive) | 1882 | 1787 | 1782 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.125387 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00367776 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000112411 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000315657 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -7.72% | 13.95% | 58.29% | 8.02% | 105.405 | 774.472 |
| ordinary/B2_10 | -7.91% | 14.28% | 57.59% | 8.24% | 78.5901 | 688.033 |
| ordinary/VOL_05 | -6.38% | 16.81% | 41.48% | 7.03% | 14.9558 | 86.1552 |
| ordinary/VOL_10 | -5.90% | 15.30% | 42.25% | 6.49% | 11.3965 | 65.5761 |
| stressed/B2_05 | -8.18% | 13.92% | 58.30% | 8.44% | 105.443 | 1263.75 |
| stressed/B2_10 | -8.26% | 14.22% | 57.61% | 8.53% | 78.6309 | 1052.22 |
| stressed/VOL_05 | -6.45% | 16.78% | 41.49% | 7.05% | 14.9651 | 156.448 |
| stressed/VOL_10 | -5.95% | 15.29% | 42.26% | 6.51% | 11.4108 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 72.46% | 0.0312477 |
| calibrated | 71.01% | 0.0272271 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1782 | 1080 | 702 | 48.43% |
| 60m | perp_synchronized_clock | 1782 | 1080 | 702 | 48.43% |
| 60m | combined_synchronized_clock | 1782 | 1069 | 713 | 48.18% |
| 15m | perp_original_clock | 1782 | 1080 | 702 | 47.50% |
| 15m | perp_synchronized_clock | 1782 | 1080 | 702 | 47.50% |
| 15m | combined_synchronized_clock | 1782 | 1069 | 713 | 46.77% |

## Data usability pilots

- Options: 471 captures; usable 7d RR25 in 391, usable 30d RR25 in 144; 360 valid hourly changes.
- Liquidations: 1293 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1779}`.
- Exchange stress: 941/941 scheduled records. Capture states: `{"missed": 44, "ok": 897}`. Ratings: `{"low": 897}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
