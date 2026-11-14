# Market studies

Generated 2026-11-14T10:47:29.498Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 124 | 88 | 88 |
| range | collecting (descriptive) | 124 | 82 | 76 |
| state | collecting (descriptive) | 497 | 321 | 318 |
| paired | collecting (descriptive) | 1988 | 1893 | 1888 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.13199 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00437048 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000410742 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000297934 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -8.38% | 14.32% | 56.85% | 8.86% | 106.058 | 807.014 |
| ordinary/B2_10 | -8.45% | 14.44% | 56.07% | 8.92% | 80.5442 | 721.026 |
| ordinary/VOL_05 | -7.01% | 17.11% | 41.26% | 7.82% | 15.1402 | 91.4039 |
| ordinary/VOL_10 | -6.48% | 15.50% | 41.71% | 7.21% | 10.8703 | 65.5761 |
| stressed/B2_05 | -8.87% | 14.31% | 56.86% | 9.30% | 106.099 | 1322.62 |
| stressed/B2_10 | -8.82% | 14.40% | 56.08% | 9.24% | 80.5833 | 1111.98 |
| stressed/VOL_05 | -7.08% | 17.09% | 41.26% | 7.84% | 15.1488 | 165.985 |
| stressed/VOL_10 | -6.53% | 15.48% | 41.73% | 7.23% | 10.884 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.11% | 0.0319396 |
| calibrated | 65.79% | 0.0282087 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1888 | 1137 | 751 | 48.90% |
| 60m | perp_synchronized_clock | 1888 | 1137 | 751 | 48.90% |
| 60m | combined_synchronized_clock | 1888 | 1126 | 762 | 48.67% |
| 15m | perp_original_clock | 1888 | 1137 | 751 | 47.41% |
| 15m | perp_synchronized_clock | 1888 | 1137 | 751 | 47.41% |
| 15m | combined_synchronized_clock | 1888 | 1126 | 762 | 46.80% |

## Data usability pilots

- Options: 497 captures; usable 7d RR25 in 417, usable 30d RR25 in 167; 386 valid hourly changes.
- Liquidations: 1371 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1883}`.
- Exchange stress: 994/994 scheduled records. Capture states: `{"missed": 44, "ok": 950}`. Ratings: `{"low": 950}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
