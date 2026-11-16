# Market studies

Generated 2026-11-16T23:17:06.030Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 139 | 103 | 103 |
| range | collecting (descriptive) | 139 | 96 | 91 |
| state | collecting (descriptive) | 558 | 343 | 342 |
| paired | collecting (descriptive) | 2230 | 2132 | 2127 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0866222 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00368132 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000480419 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000411378 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.90% | 14.95% | 53.61% | 10.56% | 102.492 | 885.399 |
| ordinary/B2_10 | -10.02% | 14.85% | 52.93% | 10.65% | 76.8642 | 815.177 |
| ordinary/VOL_05 | -8.09% | 16.93% | 39.80% | 9.09% | 14.5885 | 98.0562 |
| ordinary/VOL_10 | -7.48% | 15.66% | 40.45% | 8.49% | 9.75531 | 65.5761 |
| stressed/B2_05 | -10.42% | 14.94% | 53.61% | 11.01% | 102.548 | 1438.78 |
| stressed/B2_10 | -10.41% | 14.81% | 52.94% | 10.98% | 76.9117 | 1229.59 |
| stressed/VOL_05 | -8.17% | 16.91% | 39.81% | 9.12% | 14.5958 | 178.068 |
| stressed/VOL_10 | -7.53% | 15.64% | 40.47% | 8.50% | 9.76771 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 62.64% | 0.0327853 |
| calibrated | 61.54% | 0.0298595 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2127 | 1263 | 864 | 48.30% |
| 60m | perp_synchronized_clock | 2127 | 1263 | 864 | 48.30% |
| 60m | combined_synchronized_clock | 2127 | 1249 | 878 | 48.28% |
| 15m | perp_original_clock | 2127 | 1263 | 864 | 47.98% |
| 15m | perp_synchronized_clock | 2127 | 1263 | 864 | 47.98% |
| 15m | combined_synchronized_clock | 2127 | 1249 | 878 | 47.08% |

## Data usability pilots

- Options: 558 captures; usable 7d RR25 in 478, usable 30d RR25 in 228; 436 valid hourly changes.
- Liquidations: 1554 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2127}`.
- Exchange stress: 1115/1115 scheduled records. Capture states: `{"missed": 45, "ok": 1070}`. Ratings: `{"low": 1070}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
