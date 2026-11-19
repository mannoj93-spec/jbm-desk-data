# Market studies

Generated 2026-11-19T10:02:31.857Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 154 | 118 | 118 |
| range | collecting (descriptive) | 154 | 111 | 105 |
| state | collecting (descriptive) | 617 | 363 | 362 |
| paired | collecting (descriptive) | 2465 | 2367 | 2362 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.115711 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00436257 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000733259 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000582134 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.40% | 14.76% | 50.97% | 11.22% | 95.6764 | 902.969 |
| ordinary/B2_10 | -10.38% | 14.41% | 49.93% | 11.12% | 69.946 | 815.177 |
| ordinary/VOL_05 | -8.52% | 16.42% | 38.41% | 9.64% | 13.259 | 98.0562 |
| ordinary/VOL_10 | -7.98% | 15.52% | 39.42% | 9.14% | 8.86199 | 65.5761 |
| stressed/B2_05 | -10.93% | 14.75% | 50.98% | 11.70% | 95.7518 | 1470.45 |
| stressed/B2_10 | -10.77% | 14.38% | 49.94% | 11.45% | 70.0049 | 1229.59 |
| stressed/VOL_05 | -8.60% | 16.41% | 38.42% | 9.67% | 13.266 | 178.068 |
| stressed/VOL_10 | -8.03% | 15.51% | 39.44% | 9.15% | 8.87332 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.62% | 0.034931 |
| calibrated | 66.67% | 0.0335674 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2362 | 1391 | 971 | 47.88% |
| 60m | perp_synchronized_clock | 2362 | 1391 | 971 | 47.88% |
| 60m | combined_synchronized_clock | 2362 | 1369 | 993 | 47.85% |
| 15m | perp_original_clock | 2362 | 1391 | 971 | 48.02% |
| 15m | perp_synchronized_clock | 2362 | 1391 | 971 | 48.02% |
| 15m | combined_synchronized_clock | 2362 | 1369 | 993 | 46.97% |

## Data usability pilots

- Options: 616 captures; usable 7d RR25 in 523, usable 30d RR25 in 286; 476 valid hourly changes.
- Liquidations: 1731 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2363}`.
- Exchange stress: 1233/1233 scheduled records. Capture states: `{"missed": 45, "ok": 1188}`. Ratings: `{"low": 1188}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
