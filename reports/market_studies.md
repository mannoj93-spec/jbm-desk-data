# Market studies

Generated 2026-11-14T08:20:02.199Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 124 | 88 | 88 |
| range | collecting (descriptive) | 124 | 82 | 75 |
| state | collecting (descriptive) | 495 | 319 | 318 |
| paired | collecting (descriptive) | 1978 | 1883 | 1878 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.13199 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00423416 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000410742 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000232961 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 68.00% | 0.0318727 |
| calibrated | 66.67% | 0.0281055 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1878 | 1131 | 747 | 48.81% |
| 60m | perp_synchronized_clock | 1878 | 1131 | 747 | 48.81% |
| 60m | combined_synchronized_clock | 1878 | 1118 | 760 | 48.57% |
| 15m | perp_original_clock | 1878 | 1131 | 747 | 47.21% |
| 15m | perp_synchronized_clock | 1878 | 1131 | 747 | 47.21% |
| 15m | combined_synchronized_clock | 1878 | 1118 | 760 | 46.60% |

## Data usability pilots

- Options: 495 captures; usable 7d RR25 in 415, usable 30d RR25 in 165; 384 valid hourly changes.
- Liquidations: 1365 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1875}`.
- Exchange stress: 989/989 scheduled records. Capture states: `{"missed": 44, "ok": 945}`. Ratings: `{"low": 945}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
