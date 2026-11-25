# Market studies

Generated 2026-11-25T11:33:07.518Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 190 | 153 | 153 |
| range | collecting (descriptive) | 190 | 146 | 140 |
| state | collecting (descriptive) | 762 | 391 | 390 |
| paired | collecting (descriptive) | 3047 | 2949 | 2944 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.376115 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00131592 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00142633 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00133747 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.29% | 16.16% | 45.82% | 13.92% | 87.4129 | 979.787 |
| ordinary/B2_10 | -11.86% | 14.78% | 44.45% | 13.13% | 57.4955 | 815.177 |
| ordinary/VOL_05 | -10.26% | 16.89% | 35.75% | 11.99% | 10.882 | 98.0562 |
| ordinary/VOL_10 | -10.03% | 17.12% | 37.39% | 11.91% | 7.27145 | 65.5761 |
| stressed/B2_05 | -12.87% | 16.16% | 45.82% | 14.39% | 87.5024 | 1609.25 |
| stressed/B2_10 | -12.24% | 14.75% | 44.46% | 13.45% | 57.5643 | 1229.59 |
| stressed/VOL_05 | -10.34% | 16.88% | 35.76% | 12.02% | 10.8882 | 178.068 |
| stressed/VOL_10 | -10.08% | 17.11% | 37.40% | 11.93% | 7.28084 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.43% | 0.0387855 |
| calibrated | 69.29% | 0.0411517 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2944 | 1661 | 1283 | 48.46% |
| 60m | perp_synchronized_clock | 2944 | 1661 | 1283 | 48.46% |
| 60m | combined_synchronized_clock | 2944 | 1634 | 1310 | 48.71% |
| 15m | perp_original_clock | 2944 | 1661 | 1283 | 48.71% |
| 15m | perp_synchronized_clock | 2944 | 1661 | 1283 | 48.71% |
| 15m | combined_synchronized_clock | 2944 | 1634 | 1310 | 47.86% |

## Data usability pilots

- Options: 761 captures; usable 7d RR25 in 657, usable 30d RR25 in 413; 603 valid hourly changes.
- Liquidations: 2163 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2939}`.
- Exchange stress: 1524/1524 scheduled records. Capture states: `{"missed": 45, "ok": 1479}`. Ratings: `{"low": 1479}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
