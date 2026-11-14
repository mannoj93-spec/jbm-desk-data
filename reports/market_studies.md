# Market studies

Generated 2026-11-14T04:02:17.745Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 123 | 86 | 86 |
| range | collecting (descriptive) | 123 | 80 | 74 |
| state | collecting (descriptive) | 491 | 318 | 315 |
| paired | collecting (descriptive) | 1961 | 1866 | 1861 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.156672 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00430495 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000312226 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000403009 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -7.79% | 13.88% | 57.15% | 8.10% | 106.397 | 799.511 |
| ordinary/B2_10 | -7.98% | 14.23% | 56.47% | 8.31% | 81.7707 | 721.026 |
| ordinary/VOL_05 | -6.51% | 16.94% | 41.39% | 7.15% | 14.4884 | 86.1552 |
| ordinary/VOL_10 | -6.00% | 15.32% | 41.89% | 6.60% | 11.0385 | 65.5761 |
| stressed/B2_05 | -8.28% | 13.85% | 57.16% | 8.53% | 106.436 | 1309.05 |
| stressed/B2_10 | -8.36% | 14.19% | 56.49% | 8.63% | 81.807 | 1111.98 |
| stressed/VOL_05 | -6.57% | 16.92% | 41.40% | 7.17% | 14.4975 | 156.448 |
| stressed/VOL_10 | -6.06% | 15.31% | 41.90% | 6.61% | 11.0524 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.57% | 0.0317241 |
| calibrated | 66.22% | 0.0279195 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1861 | 1126 | 735 | 48.85% |
| 60m | perp_synchronized_clock | 1861 | 1126 | 735 | 48.85% |
| 60m | combined_synchronized_clock | 1861 | 1114 | 747 | 48.56% |
| 15m | perp_original_clock | 1861 | 1126 | 735 | 47.42% |
| 15m | perp_synchronized_clock | 1861 | 1126 | 735 | 47.42% |
| 15m | combined_synchronized_clock | 1861 | 1114 | 747 | 46.77% |

## Data usability pilots

- Options: 490 captures; usable 7d RR25 in 410, usable 30d RR25 in 160; 379 valid hourly changes.
- Liquidations: 1353 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1859}`.
- Exchange stress: 981/981 scheduled records. Capture states: `{"missed": 44, "ok": 937}`. Ratings: `{"low": 937}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
