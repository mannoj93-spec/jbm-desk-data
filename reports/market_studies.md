# Market studies

Generated 2026-11-08T07:08:35.716Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 87 | 51 | 51 |
| range | collecting (descriptive) | 87 | 45 | 39 |
| state | collecting (descriptive) | 350 | 253 | 249 |
| paired | collecting (descriptive) | 1397 | 1303 | 1298 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.120701 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00398566 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.0016888 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00115562 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 74.36% | 0.0291518 |
| calibrated | 71.79% | 0.0232982 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1298 | 799 | 499 | 48.44% |
| 60m | perp_synchronized_clock | 1298 | 799 | 499 | 48.44% |
| 60m | combined_synchronized_clock | 1298 | 791 | 507 | 48.67% |
| 15m | perp_original_clock | 1298 | 799 | 499 | 47.06% |
| 15m | perp_synchronized_clock | 1298 | 799 | 499 | 47.06% |
| 15m | combined_synchronized_clock | 1298 | 791 | 507 | 46.52% |

## Data usability pilots

- Options: 350 captures; usable 7d RR25 in 295, usable 30d RR25 in 86; 271 valid hourly changes.
- Liquidations: 937 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1302}`.
- Exchange stress: 699/699 scheduled records. Capture states: `{"missed": 43, "ok": 656}`. Ratings: `{"low": 656}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
