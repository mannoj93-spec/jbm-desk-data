# Market studies

Generated 2026-11-12T04:48:15.302Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 111 | 75 | 75 |
| range | collecting (descriptive) | 111 | 69 | 63 |
| state | collecting (descriptive) | 443 | 303 | 301 |
| paired | collecting (descriptive) | 1772 | 1677 | 1672 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.00377662 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00389047 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00133801 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 3.73804e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.24% | 12.63% | 59.76% | 5.64% | 105.234 | 739.372 |
| ordinary/B2_10 | -5.69% | 13.49% | 59.15% | 6.11% | 83.3102 | 688.033 |
| ordinary/VOL_05 | -3.83% | 15.81% | 41.79% | 4.58% | 14.4319 | 78.3691 |
| ordinary/VOL_10 | -3.68% | 14.66% | 42.87% | 4.38% | 12.0937 | 65.5761 |
| stressed/B2_05 | -5.68% | 12.62% | 59.76% | 6.03% | 105.269 | 1200.26 |
| stressed/B2_10 | -6.04% | 13.43% | 59.16% | 6.41% | 83.3407 | 1052.22 |
| stressed/VOL_05 | -3.89% | 15.77% | 41.80% | 4.60% | 14.441 | 142.3 |
| stressed/VOL_10 | -3.73% | 14.65% | 42.89% | 4.39% | 12.1088 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 71.43% | 0.030713 |
| calibrated | 69.84% | 0.0263834 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1672 | 1021 | 651 | 48.87% |
| 60m | perp_synchronized_clock | 1672 | 1021 | 651 | 48.87% |
| 60m | combined_synchronized_clock | 1672 | 1010 | 662 | 48.71% |
| 15m | perp_original_clock | 1672 | 1021 | 651 | 46.91% |
| 15m | perp_synchronized_clock | 1672 | 1021 | 651 | 46.91% |
| 15m | combined_synchronized_clock | 1672 | 1010 | 662 | 46.24% |

## Data usability pilots

- Options: 443 captures; usable 7d RR25 in 369, usable 30d RR25 in 130; 341 valid hourly changes.
- Liquidations: 1209 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1667}`.
- Exchange stress: 886/886 scheduled records. Capture states: `{"missed": 44, "ok": 842}`. Ratings: `{"low": 842}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
