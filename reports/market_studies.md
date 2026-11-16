# Market studies

Generated 2026-11-16T06:58:48.461Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 135 | 99 | 99 |
| range | collecting (descriptive) | 135 | 93 | 87 |
| state | collecting (descriptive) | 541 | 336 | 335 |
| paired | collecting (descriptive) | 2164 | 2068 | 2062 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0341603 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00374158 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000554556 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000363725 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.94% | 15.14% | 54.51% | 10.56% | 103.554 | 873.64 |
| ordinary/B2_10 | -10.01% | 15.06% | 53.87% | 10.65% | 79.0276 | 815.177 |
| ordinary/VOL_05 | -8.08% | 17.17% | 40.24% | 9.09% | 15.0051 | 98.0562 |
| ordinary/VOL_10 | -7.47% | 15.83% | 40.77% | 8.49% | 10.0355 | 65.5761 |
| stressed/B2_05 | -10.45% | 15.13% | 54.51% | 11.01% | 103.606 | 1417.53 |
| stressed/B2_10 | -10.40% | 15.01% | 53.88% | 10.98% | 79.0709 | 1229.59 |
| stressed/VOL_05 | -8.16% | 17.16% | 40.25% | 9.12% | 15.0124 | 178.068 |
| stressed/VOL_10 | -7.52% | 15.82% | 40.79% | 8.50% | 10.0483 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 60.92% | 0.0319134 |
| calibrated | 59.77% | 0.028744 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2062 | 1228 | 834 | 48.29% |
| 60m | perp_synchronized_clock | 2062 | 1228 | 834 | 48.29% |
| 60m | combined_synchronized_clock | 2062 | 1216 | 846 | 48.27% |
| 15m | perp_original_clock | 2062 | 1228 | 834 | 47.56% |
| 15m | perp_synchronized_clock | 2062 | 1228 | 834 | 47.56% |
| 15m | combined_synchronized_clock | 2062 | 1216 | 846 | 46.79% |

## Data usability pilots

- Options: 541 captures; usable 7d RR25 in 461, usable 30d RR25 in 211; 424 valid hourly changes.
- Liquidations: 1503 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2059}`.
- Exchange stress: 1082/1082 scheduled records. Capture states: `{"missed": 44, "ok": 1038}`. Ratings: `{"low": 1038}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
