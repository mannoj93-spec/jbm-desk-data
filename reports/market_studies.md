# Market studies

Generated 2026-11-21T07:03:11.510Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 165 | 128 | 128 |
| range | collecting (descriptive) | 165 | 121 | 116 |
| state | collecting (descriptive) | 662 | 369 | 368 |
| paired | collecting (descriptive) | 2645 | 2547 | 2542 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.110854 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00285916 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000914909 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000811369 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -13.63% | 16.03% | 49.31% | 13.92% | 92.2414 | 922.603 |
| ordinary/B2_10 | -12.81% | 14.76% | 48.02% | 13.13% | 65.5739 | 815.177 |
| ordinary/VOL_05 | -11.38% | 16.91% | 37.50% | 11.99% | 12.4231 | 98.0562 |
| ordinary/VOL_10 | -11.36% | 16.59% | 38.73% | 11.91% | 8.30206 | 65.5761 |
| stressed/B2_05 | -14.16% | 16.03% | 49.31% | 14.39% | 92.3227 | 1505.93 |
| stressed/B2_10 | -13.19% | 14.73% | 48.03% | 13.45% | 65.637 | 1229.59 |
| stressed/VOL_05 | -11.46% | 16.89% | 37.50% | 12.02% | 12.4298 | 178.068 |
| stressed/VOL_10 | -11.41% | 16.58% | 38.74% | 11.93% | 8.31271 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.24% | 0.0363398 |
| calibrated | 68.97% | 0.0359353 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2542 | 1476 | 1066 | 48.10% |
| 60m | perp_synchronized_clock | 2542 | 1476 | 1066 | 48.10% |
| 60m | combined_synchronized_clock | 2542 | 1455 | 1087 | 48.18% |
| 15m | perp_original_clock | 2542 | 1476 | 1066 | 48.71% |
| 15m | perp_synchronized_clock | 2542 | 1476 | 1066 | 48.71% |
| 15m | combined_synchronized_clock | 2542 | 1455 | 1087 | 47.70% |

## Data usability pilots

- Options: 660 captures; usable 7d RR25 in 557, usable 30d RR25 in 316; 504 valid hourly changes.
- Liquidations: 1864 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 13, "missed": 66, "ok": 2540}`.
- Exchange stress: 1323/1323 scheduled records. Capture states: `{"missed": 45, "ok": 1278}`. Ratings: `{"low": 1278}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
