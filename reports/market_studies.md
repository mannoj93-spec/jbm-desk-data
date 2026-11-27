# Market studies

Generated 2026-11-27T10:53:41.874Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 202 | 165 | 165 |
| range | collecting (descriptive) | 202 | 157 | 151 |
| state | collecting (descriptive) | 809 | 399 | 398 |
| paired | collecting (descriptive) | 3236 | 3138 | 3133 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.358257 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00279243 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00103052 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00177545 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.28% | 15.95% | 44.53% | 13.92% | 84.8763 | 1002.09 |
| ordinary/B2_10 | -10.93% | 14.57% | 43.06% | 13.13% | 54.2724 | 815.177 |
| ordinary/VOL_05 | -9.17% | 16.63% | 35.07% | 11.99% | 10.2681 | 98.0562 |
| ordinary/VOL_10 | -8.75% | 16.97% | 36.86% | 11.91% | 6.86101 | 65.5761 |
| stressed/B2_05 | -11.88% | 15.96% | 44.53% | 14.39% | 84.9699 | 1649.22 |
| stressed/B2_10 | -11.32% | 14.56% | 43.07% | 13.45% | 54.3421 | 1229.59 |
| stressed/VOL_05 | -9.25% | 16.62% | 35.08% | 12.02% | 10.2741 | 178.068 |
| stressed/VOL_10 | -8.80% | 16.96% | 36.87% | 11.93% | 6.86989 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.21% | 0.0401607 |
| calibrated | 70.86% | 0.043888 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3133 | 1763 | 1370 | 48.21% |
| 60m | perp_synchronized_clock | 3133 | 1763 | 1370 | 48.21% |
| 60m | combined_synchronized_clock | 3133 | 1726 | 1407 | 48.55% |
| 15m | perp_original_clock | 3133 | 1763 | 1370 | 48.55% |
| 15m | perp_synchronized_clock | 3133 | 1763 | 1370 | 48.55% |
| 15m | combined_synchronized_clock | 3133 | 1726 | 1407 | 47.51% |

## Data usability pilots

- Options: 808 captures; usable 7d RR25 in 697, usable 30d RR25 in 413; 634 valid hourly changes.
- Liquidations: 2304 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3127}`.
- Exchange stress: 1618/1618 scheduled records. Capture states: `{"missed": 45, "ok": 1573}`. Ratings: `{"low": 1573}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
