# Market studies

Generated 2026-11-08T12:18:46.540Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 89 | 53 | 53 |
| range | collecting (descriptive) | 89 | 47 | 40 |
| state | collecting (descriptive) | 355 | 257 | 253 |
| paired | collecting (descriptive) | 1418 | 1324 | 1319 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.101007 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00379383 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00172707 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00104246 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.71% | 13.12% | 65.31% | 4.13% | 108.953 | 518.09 |
| ordinary/B2_10 | -4.19% | 14.28% | 64.93% | 4.63% | 88.7909 | 467.869 |
| ordinary/VOL_05 | -2.89% | 17.99% | 43.95% | 3.74% | 17.9182 | 78.3691 |
| ordinary/VOL_10 | -2.74% | 16.55% | 45.31% | 3.54% | 15.0178 | 65.5761 |
| stressed/B2_05 | -4.09% | 13.05% | 65.31% | 4.40% | 108.956 | 904.701 |
| stressed/B2_10 | -4.50% | 14.19% | 64.94% | 4.84% | 88.7903 | 782.71 |
| stressed/VOL_05 | -2.95% | 17.95% | 43.96% | 3.75% | 17.9286 | 142.3 |
| stressed/VOL_10 | -2.80% | 16.53% | 45.33% | 3.54% | 15.0361 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 75.00% | 0.0288747 |
| calibrated | 72.50% | 0.0230752 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1319 | 814 | 505 | 48.28% |
| 60m | perp_synchronized_clock | 1319 | 814 | 505 | 48.28% |
| 60m | combined_synchronized_clock | 1319 | 808 | 511 | 48.51% |
| 15m | perp_original_clock | 1319 | 814 | 505 | 46.81% |
| 15m | perp_synchronized_clock | 1319 | 814 | 505 | 46.81% |
| 15m | combined_synchronized_clock | 1319 | 808 | 511 | 46.29% |

## Data usability pilots

- Options: 355 captures; usable 7d RR25 in 300, usable 30d RR25 in 86; 276 valid hourly changes.
- Liquidations: 952 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1322}`.
- Exchange stress: 709/709 scheduled records. Capture states: `{"missed": 43, "ok": 666}`. Ratings: `{"low": 666}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
