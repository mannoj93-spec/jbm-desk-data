# Market studies

Generated 2026-11-21T03:47:28.880Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 164 | 127 | 127 |
| range | collecting (descriptive) | 164 | 120 | 115 |
| state | collecting (descriptive) | 658 | 368 | 367 |
| paired | collecting (descriptive) | 2632 | 2534 | 2529 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0402558 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00357922 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00105 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000864966 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.24% | 14.79% | 49.42% | 12.53% | 91.2205 | 910.735 |
| ordinary/B2_10 | -11.88% | 14.23% | 48.19% | 12.19% | 65.9395 | 815.177 |
| ordinary/VOL_05 | -10.28% | 16.25% | 37.58% | 10.90% | 12.4929 | 98.0562 |
| ordinary/VOL_10 | -10.06% | 15.61% | 38.79% | 10.62% | 8.34866 | 65.5761 |
| stressed/B2_05 | -12.77% | 14.78% | 49.43% | 13.00% | 91.3029 | 1484.48 |
| stressed/B2_10 | -12.26% | 14.19% | 48.20% | 12.52% | 66.0022 | 1229.59 |
| stressed/VOL_05 | -10.35% | 16.24% | 37.58% | 10.93% | 12.4996 | 178.068 |
| stressed/VOL_10 | -10.11% | 15.60% | 38.81% | 10.63% | 8.35938 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.83% | 0.0362588 |
| calibrated | 69.57% | 0.0357747 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2529 | 1472 | 1057 | 48.03% |
| 60m | perp_synchronized_clock | 2529 | 1472 | 1057 | 48.03% |
| 60m | combined_synchronized_clock | 2529 | 1449 | 1080 | 48.10% |
| 15m | perp_original_clock | 2529 | 1472 | 1057 | 48.71% |
| 15m | perp_synchronized_clock | 2529 | 1472 | 1057 | 48.71% |
| 15m | combined_synchronized_clock | 2529 | 1449 | 1080 | 47.62% |

## Data usability pilots

- Options: 657 captures; usable 7d RR25 in 554, usable 30d RR25 in 313; 501 valid hourly changes.
- Liquidations: 1852 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 13, "missed": 66, "ok": 2524}`.
- Exchange stress: 1316/1316 scheduled records. Capture states: `{"missed": 45, "ok": 1271}`. Ratings: `{"low": 1271}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
