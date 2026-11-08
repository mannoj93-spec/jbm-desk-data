# Market studies

Generated 2026-11-08T21:03:00.757Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 91 | 55 | 55 |
| range | collecting (descriptive) | 91 | 49 | 43 |
| state | collecting (descriptive) | 364 | 264 | 260 |
| paired | collecting (descriptive) | 1453 | 1359 | 1354 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0835832 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00331593 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00188527 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000784712 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.79% | 12.93% | 65.55% | 4.13% | 106.621 | 518.09 |
| ordinary/B2_10 | -4.25% | 14.05% | 64.98% | 4.63% | 86.9008 | 467.869 |
| ordinary/VOL_05 | -2.92% | 17.66% | 43.72% | 3.74% | 17.5302 | 78.3691 |
| ordinary/VOL_10 | -2.78% | 16.24% | 45.05% | 3.54% | 14.6923 | 65.5761 |
| stressed/B2_05 | -4.17% | 12.86% | 65.56% | 4.43% | 106.633 | 904.701 |
| stressed/B2_10 | -4.56% | 13.96% | 65.00% | 4.85% | 86.9064 | 782.71 |
| stressed/VOL_05 | -2.99% | 17.62% | 43.73% | 3.75% | 17.5405 | 142.3 |
| stressed/VOL_10 | -2.83% | 16.22% | 45.06% | 3.54% | 14.7103 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.77% | 0.0282907 |
| calibrated | 67.44% | 0.0226386 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1354 | 840 | 514 | 48.10% |
| 60m | perp_synchronized_clock | 1354 | 840 | 514 | 48.10% |
| 60m | combined_synchronized_clock | 1354 | 835 | 519 | 48.26% |
| 15m | perp_original_clock | 1354 | 840 | 514 | 46.90% |
| 15m | perp_synchronized_clock | 1354 | 840 | 514 | 46.90% |
| 15m | combined_synchronized_clock | 1354 | 835 | 519 | 46.35% |

## Data usability pilots

- Options: 363 captures; usable 7d RR25 in 308, usable 30d RR25 in 86; 284 valid hourly changes.
- Liquidations: 979 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1358}`.
- Exchange stress: 727/727 scheduled records. Capture states: `{"missed": 43, "ok": 684}`. Ratings: `{"low": 684}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
