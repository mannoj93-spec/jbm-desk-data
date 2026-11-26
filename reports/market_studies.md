# Market studies

Generated 2026-11-26T09:34:29.770Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 196 | 159 | 159 |
| range | collecting (descriptive) | 196 | 151 | 146 |
| state | collecting (descriptive) | 784 | 392 | 391 |
| paired | collecting (descriptive) | 3135 | 3037 | 3031 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.310274 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00212668 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.0012166 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.78% | 16.13% | 45.11% | 13.92% | 86.1122 | 990.918 |
| ordinary/B2_10 | -11.34% | 14.76% | 43.73% | 13.13% | 55.8545 | 815.177 |
| ordinary/VOL_05 | -9.65% | 16.85% | 35.40% | 11.99% | 10.5695 | 98.0562 |
| ordinary/VOL_10 | -9.31% | 17.17% | 37.11% | 11.91% | 7.06259 | 65.5761 |
| stressed/B2_05 | -12.37% | 16.14% | 45.12% | 14.39% | 86.204 | 1629.05 |
| stressed/B2_10 | -11.72% | 14.74% | 43.74% | 13.45% | 55.9239 | 1229.59 |
| stressed/VOL_05 | -9.72% | 16.84% | 35.40% | 12.02% | 10.5756 | 178.068 |
| stressed/VOL_10 | -9.36% | 17.17% | 37.12% | 11.93% | 7.07173 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.81% | 0.0395272 |
| calibrated | 70.55% | 0.0426609 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3031 | 1707 | 1324 | 48.15% |
| 60m | perp_synchronized_clock | 3031 | 1707 | 1324 | 48.15% |
| 60m | combined_synchronized_clock | 3031 | 1676 | 1355 | 48.33% |
| 15m | perp_original_clock | 3031 | 1707 | 1324 | 48.39% |
| 15m | perp_synchronized_clock | 3031 | 1707 | 1324 | 48.39% |
| 15m | combined_synchronized_clock | 3031 | 1676 | 1355 | 47.32% |

## Data usability pilots

- Options: 783 captures; usable 7d RR25 in 674, usable 30d RR25 in 413; 616 valid hourly changes.
- Liquidations: 2229 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3027}`.
- Exchange stress: 1568/1568 scheduled records. Capture states: `{"missed": 45, "ok": 1523}`. Ratings: `{"low": 1523}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
