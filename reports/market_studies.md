# Market studies

Generated 2026-11-21T04:47:31.791Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 165 | 128 | 128 |
| range | collecting (descriptive) | 165 | 121 | 115 |
| state | collecting (descriptive) | 659 | 369 | 367 |
| paired | collecting (descriptive) | 2636 | 2538 | 2533 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.110854 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00357922 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00105 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000937623 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 67.83% | 0.0362588 |
| calibrated | 69.57% | 0.0357747 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2533 | 1474 | 1059 | 48.03% |
| 60m | perp_synchronized_clock | 2533 | 1474 | 1059 | 48.03% |
| 60m | combined_synchronized_clock | 2533 | 1452 | 1081 | 48.14% |
| 15m | perp_original_clock | 2533 | 1474 | 1059 | 48.64% |
| 15m | perp_synchronized_clock | 2533 | 1474 | 1059 | 48.64% |
| 15m | combined_synchronized_clock | 2533 | 1452 | 1081 | 47.59% |

## Data usability pilots

- Options: 658 captures; usable 7d RR25 in 555, usable 30d RR25 in 314; 502 valid hourly changes.
- Liquidations: 1855 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 13, "missed": 66, "ok": 2528}`.
- Exchange stress: 1318/1318 scheduled records. Capture states: `{"missed": 45, "ok": 1273}`. Ratings: `{"low": 1273}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
