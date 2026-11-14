# Market studies

Generated 2026-11-14T04:21:49.909Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 123 | 87 | 87 |
| range | collecting (descriptive) | 123 | 81 | 74 |
| state | collecting (descriptive) | 491 | 318 | 315 |
| paired | collecting (descriptive) | 1962 | 1867 | 1861 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.197711 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00430495 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000312226 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000403009 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -8.56% | 14.34% | 57.01% | 8.86% | 106.859 | 807.014 |
| ordinary/B2_10 | -8.60% | 14.48% | 56.27% | 8.92% | 81.1542 | 721.026 |
| ordinary/VOL_05 | -7.17% | 17.17% | 41.33% | 7.82% | 15.256 | 91.4039 |
| ordinary/VOL_10 | -6.63% | 15.55% | 41.80% | 7.21% | 10.9539 | 65.5761 |
| stressed/B2_05 | -9.05% | 14.32% | 57.01% | 9.30% | 106.898 | 1322.62 |
| stressed/B2_10 | -8.97% | 14.43% | 56.28% | 9.24% | 81.1919 | 1111.98 |
| stressed/VOL_05 | -7.25% | 17.15% | 41.33% | 7.84% | 15.2645 | 165.985 |
| stressed/VOL_10 | -6.68% | 15.54% | 41.82% | 7.23% | 10.9677 | 119.284 |

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

- Options: 491 captures; usable 7d RR25 in 411, usable 30d RR25 in 161; 380 valid hourly changes.
- Liquidations: 1353 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1859}`.
- Exchange stress: 981/981 scheduled records. Capture states: `{"missed": 44, "ok": 937}`. Ratings: `{"low": 937}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
