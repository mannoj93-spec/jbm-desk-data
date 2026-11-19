# Market studies

Generated 2026-11-19T17:17:37.852Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 156 | 120 | 120 |
| range | collecting (descriptive) | 156 | 113 | 107 |
| state | collecting (descriptive) | 624 | 363 | 363 |
| paired | collecting (descriptive) | 2494 | 2396 | 2390 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0734864 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00444459 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000757033 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000575314 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.65% | 14.67% | 50.68% | 11.22% | 94.5316 | 902.969 |
| ordinary/B2_10 | -10.58% | 14.31% | 49.57% | 11.12% | 69.1065 | 815.177 |
| ordinary/VOL_05 | -8.75% | 16.30% | 38.24% | 9.64% | 13.0981 | 98.0562 |
| ordinary/VOL_10 | -8.26% | 15.42% | 39.30% | 9.14% | 8.75395 | 65.5761 |
| stressed/B2_05 | -11.18% | 14.66% | 50.68% | 11.70% | 94.6096 | 1470.45 |
| stressed/B2_10 | -10.96% | 14.27% | 49.58% | 11.45% | 69.1665 | 1229.59 |
| stressed/VOL_05 | -8.83% | 16.29% | 38.25% | 9.67% | 13.105 | 178.068 |
| stressed/VOL_10 | -8.31% | 15.41% | 39.31% | 9.15% | 8.76515 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.22% | 0.0352185 |
| calibrated | 67.29% | 0.0340439 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2390 | 1406 | 984 | 47.94% |
| 60m | perp_synchronized_clock | 2390 | 1406 | 984 | 47.94% |
| 60m | combined_synchronized_clock | 2390 | 1384 | 1006 | 47.90% |
| 15m | perp_original_clock | 2390 | 1406 | 984 | 48.01% |
| 15m | perp_synchronized_clock | 2390 | 1406 | 984 | 48.01% |
| 15m | combined_synchronized_clock | 2390 | 1384 | 1006 | 46.97% |

## Data usability pilots

- Options: 624 captures; usable 7d RR25 in 530, usable 30d RR25 in 293; 482 valid hourly changes.
- Liquidations: 1752 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2391}`.
- Exchange stress: 1247/1247 scheduled records. Capture states: `{"missed": 45, "ok": 1202}`. Ratings: `{"low": 1202}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
