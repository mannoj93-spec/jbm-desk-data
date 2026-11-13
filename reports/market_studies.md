# Market studies

Generated 2026-11-13T18:25:56.845Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 120 | 84 | 84 |
| range | collecting (descriptive) | 120 | 78 | 72 |
| state | collecting (descriptive) | 481 | 313 | 312 |
| paired | collecting (descriptive) | 1922 | 1827 | 1822 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.262665 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0040475 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000143014 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000308727 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -7.66% | 13.91% | 57.65% | 8.02% | 105.274 | 783.304 |
| ordinary/B2_10 | -7.78% | 14.30% | 57.03% | 8.24% | 80.2505 | 704.79 |
| ordinary/VOL_05 | -6.43% | 16.94% | 41.44% | 7.08% | 14.7182 | 86.1552 |
| ordinary/VOL_10 | -5.94% | 15.36% | 42.06% | 6.53% | 11.2145 | 65.5761 |
| stressed/B2_05 | -8.13% | 13.89% | 57.65% | 8.44% | 105.312 | 1279.72 |
| stressed/B2_10 | -8.14% | 14.24% | 57.04% | 8.53% | 80.2869 | 1082.57 |
| stressed/VOL_05 | -6.50% | 16.91% | 41.44% | 7.10% | 14.7274 | 156.448 |
| stressed/VOL_10 | -5.99% | 15.34% | 42.08% | 6.54% | 11.2286 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.44% | 0.0315437 |
| calibrated | 68.06% | 0.0276582 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1822 | 1100 | 722 | 48.64% |
| 60m | perp_synchronized_clock | 1822 | 1100 | 722 | 48.64% |
| 60m | combined_synchronized_clock | 1822 | 1089 | 733 | 48.39% |
| 15m | perp_original_clock | 1822 | 1100 | 722 | 47.64% |
| 15m | perp_synchronized_clock | 1822 | 1100 | 722 | 47.64% |
| 15m | combined_synchronized_clock | 1822 | 1089 | 733 | 46.92% |

## Data usability pilots

- Options: 481 captures; usable 7d RR25 in 401, usable 30d RR25 in 151; 370 valid hourly changes.
- Liquidations: 1323 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1819}`.
- Exchange stress: 961/961 scheduled records. Capture states: `{"missed": 44, "ok": 917}`. Ratings: `{"low": 917}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
