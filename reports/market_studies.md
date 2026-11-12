# Market studies

Generated 2026-11-12T08:51:29.126Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 112 | 76 | 76 |
| range | collecting (descriptive) | 112 | 70 | 64 |
| state | collecting (descriptive) | 447 | 305 | 303 |
| paired | collecting (descriptive) | 1788 | 1693 | 1688 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.042675 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00381754 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00116245 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000222156 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.32% | 12.55% | 59.58% | 5.64% | 105.521 | 745.871 |
| ordinary/B2_10 | -5.76% | 13.40% | 58.92% | 6.11% | 82.5949 | 688.033 |
| ordinary/VOL_05 | -3.89% | 15.70% | 41.71% | 4.58% | 14.3058 | 78.3691 |
| ordinary/VOL_10 | -3.75% | 14.56% | 42.78% | 4.38% | 11.9879 | 65.5761 |
| stressed/B2_05 | -5.78% | 12.53% | 59.58% | 6.04% | 105.557 | 1212.01 |
| stressed/B2_10 | -6.11% | 13.34% | 58.93% | 6.41% | 82.6271 | 1052.22 |
| stressed/VOL_05 | -3.96% | 15.67% | 41.72% | 4.60% | 14.3148 | 142.3 |
| stressed/VOL_10 | -3.80% | 14.55% | 42.80% | 4.39% | 12.0029 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 71.88% | 0.0308109 |
| calibrated | 70.31% | 0.0265369 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1688 | 1029 | 659 | 48.49% |
| 60m | perp_synchronized_clock | 1688 | 1029 | 659 | 48.49% |
| 60m | combined_synchronized_clock | 1688 | 1019 | 669 | 48.28% |
| 15m | perp_original_clock | 1688 | 1029 | 659 | 46.65% |
| 15m | perp_synchronized_clock | 1688 | 1029 | 659 | 46.65% |
| 15m | combined_synchronized_clock | 1688 | 1019 | 669 | 45.93% |

## Data usability pilots

- Options: 447 captures; usable 7d RR25 in 373, usable 30d RR25 in 134; 345 valid hourly changes.
- Liquidations: 1221 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1683}`.
- Exchange stress: 894/894 scheduled records. Capture states: `{"missed": 44, "ok": 850}`. Ratings: `{"low": 850}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
