# Market studies

Generated 2026-11-21T00:25:29.004Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 164 | 127 | 127 |
| range | collecting (descriptive) | 164 | 120 | 114 |
| state | collecting (descriptive) | 655 | 367 | 365 |
| paired | collecting (descriptive) | 2618 | 2520 | 2514 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0402558 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00418212 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00076659 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000745823 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 68.42% | 0.036139 |
| calibrated | 69.30% | 0.0355738 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2514 | 1463 | 1051 | 47.98% |
| 60m | perp_synchronized_clock | 2514 | 1463 | 1051 | 47.98% |
| 60m | combined_synchronized_clock | 2514 | 1441 | 1073 | 48.02% |
| 15m | perp_original_clock | 2514 | 1463 | 1051 | 48.67% |
| 15m | perp_synchronized_clock | 2514 | 1463 | 1051 | 48.67% |
| 15m | combined_synchronized_clock | 2514 | 1441 | 1073 | 47.61% |

## Data usability pilots

- Options: 654 captures; usable 7d RR25 in 551, usable 30d RR25 in 310; 498 valid hourly changes.
- Liquidations: 1843 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 13, "missed": 66, "ok": 2512}`.
- Exchange stress: 1309/1309 scheduled records. Capture states: `{"missed": 45, "ok": 1264}`. Ratings: `{"low": 1264}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
