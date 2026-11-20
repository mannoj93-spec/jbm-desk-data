# Market studies

Generated 2026-11-20T07:32:35.692Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 159 | 123 | 123 |
| range | collecting (descriptive) | 159 | 116 | 110 |
| state | collecting (descriptive) | 638 | 364 | 364 |
| paired | collecting (descriptive) | 2551 | 2453 | 2448 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0147071 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00456202 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00071554 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000765931 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.19% | 14.55% | 50.24% | 11.49% | 92.8822 | 902.969 |
| ordinary/B2_10 | -11.01% | 14.17% | 49.04% | 11.33% | 67.8955 | 815.177 |
| ordinary/VOL_05 | -9.26% | 16.15% | 37.99% | 9.89% | 12.8662 | 98.0562 |
| ordinary/VOL_10 | -8.85% | 15.32% | 39.11% | 9.43% | 8.59847 | 65.5761 |
| stressed/B2_05 | -11.72% | 14.54% | 50.24% | 11.96% | 92.9638 | 1470.45 |
| stressed/B2_10 | -11.39% | 14.13% | 49.05% | 11.66% | 67.9569 | 1229.59 |
| stressed/VOL_05 | -9.33% | 16.14% | 38.00% | 9.92% | 12.873 | 178.068 |
| stressed/VOL_10 | -8.90% | 15.31% | 39.12% | 9.44% | 8.60949 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.09% | 0.0356536 |
| calibrated | 68.18% | 0.0347498 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2448 | 1436 | 1012 | 47.98% |
| 60m | perp_synchronized_clock | 2448 | 1436 | 1012 | 47.98% |
| 60m | combined_synchronized_clock | 2448 | 1414 | 1034 | 48.02% |
| 15m | perp_original_clock | 2448 | 1436 | 1012 | 48.26% |
| 15m | perp_synchronized_clock | 2448 | 1436 | 1012 | 48.26% |
| 15m | combined_synchronized_clock | 2448 | 1414 | 1034 | 47.24% |

## Data usability pilots

- Options: 638 captures; usable 7d RR25 in 537, usable 30d RR25 in 296; 488 valid hourly changes.
- Liquidations: 1794 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2447}`.
- Exchange stress: 1276/1276 scheduled records. Capture states: `{"missed": 45, "ok": 1231}`. Ratings: `{"low": 1231}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
