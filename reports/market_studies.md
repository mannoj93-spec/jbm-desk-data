# Market studies

Generated 2026-11-08T05:05:47.291Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 87 | 51 | 51 |
| range | collecting (descriptive) | 87 | 45 | 38 |
| state | collecting (descriptive) | 348 | 251 | 247 |
| paired | collecting (descriptive) | 1389 | 1295 | 1290 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.120701 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00418759 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00161817 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00140504 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.73% | 13.37% | 65.15% | 4.13% | 109.114 | 508.442 |
| ordinary/B2_10 | -4.20% | 14.55% | 64.88% | 4.63% | 90.7544 | 467.869 |
| ordinary/VOL_05 | -2.90% | 18.35% | 44.19% | 3.74% | 18.322 | 78.3691 |
| ordinary/VOL_10 | -2.75% | 16.88% | 45.58% | 3.54% | 15.3567 | 65.5761 |
| stressed/B2_05 | -4.10% | 13.30% | 65.16% | 4.40% | 109.115 | 887.257 |
| stressed/B2_10 | -4.51% | 14.46% | 64.89% | 4.84% | 90.7468 | 782.71 |
| stressed/VOL_05 | -2.96% | 18.31% | 44.20% | 3.75% | 18.3326 | 142.3 |
| stressed/VOL_10 | -2.80% | 16.86% | 45.60% | 3.54% | 15.3753 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.68% | 0.0294718 |
| calibrated | 71.05% | 0.0235613 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1290 | 793 | 497 | 48.68% |
| 60m | perp_synchronized_clock | 1290 | 793 | 497 | 48.68% |
| 60m | combined_synchronized_clock | 1290 | 784 | 506 | 48.98% |
| 15m | perp_original_clock | 1290 | 793 | 497 | 47.16% |
| 15m | perp_synchronized_clock | 1290 | 793 | 497 | 47.16% |
| 15m | combined_synchronized_clock | 1290 | 784 | 506 | 46.68% |

## Data usability pilots

- Options: 347 captures; usable 7d RR25 in 292, usable 30d RR25 in 86; 268 valid hourly changes.
- Liquidations: 931 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1294}`.
- Exchange stress: 695/695 scheduled records. Capture states: `{"missed": 43, "ok": 652}`. Ratings: `{"low": 652}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
