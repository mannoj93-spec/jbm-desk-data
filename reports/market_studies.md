# Market studies

Generated 2026-11-14T05:32:04.672Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 123 | 87 | 87 |
| range | collecting (descriptive) | 123 | 81 | 75 |
| state | collecting (descriptive) | 492 | 318 | 316 |
| paired | collecting (descriptive) | 1967 | 1872 | 1867 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.197711 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00423416 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00044668 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000234333 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 68.00% | 0.0318727 |
| calibrated | 66.67% | 0.0281055 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1867 | 1128 | 739 | 48.76% |
| 60m | perp_synchronized_clock | 1867 | 1128 | 739 | 48.76% |
| 60m | combined_synchronized_clock | 1867 | 1115 | 752 | 48.52% |
| 15m | perp_original_clock | 1867 | 1128 | 739 | 47.34% |
| 15m | perp_synchronized_clock | 1867 | 1128 | 739 | 47.34% |
| 15m | combined_synchronized_clock | 1867 | 1115 | 752 | 46.73% |

## Data usability pilots

- Options: 492 captures; usable 7d RR25 in 412, usable 30d RR25 in 162; 381 valid hourly changes.
- Liquidations: 1356 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1863}`.
- Exchange stress: 984/984 scheduled records. Capture states: `{"missed": 44, "ok": 940}`. Ratings: `{"low": 940}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
