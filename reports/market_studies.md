# Market studies

Generated 2026-11-11T20:20:26.600Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 109 | 73 | 73 |
| range | collecting (descriptive) | 109 | 67 | 60 |
| state | collecting (descriptive) | 435 | 300 | 298 |
| paired | collecting (descriptive) | 1738 | 1644 | 1639 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0323215 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00411027 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00140127 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000152532 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.91% | 12.77% | 60.24% | 5.64% | 107.101 | 739.372 |
| ordinary/B2_10 | -5.36% | 13.64% | 59.62% | 6.11% | 84.7829 | 688.033 |
| ordinary/VOL_05 | -3.50% | 15.99% | 41.95% | 4.58% | 14.6918 | 78.3691 |
| ordinary/VOL_10 | -3.36% | 14.82% | 43.06% | 4.38% | 12.3116 | 65.5761 |
| stressed/B2_05 | -5.36% | 12.75% | 60.24% | 6.03% | 107.13 | 1200.26 |
| stressed/B2_10 | -5.72% | 13.58% | 59.63% | 6.41% | 84.8097 | 1052.22 |
| stressed/VOL_05 | -3.56% | 15.96% | 41.96% | 4.60% | 14.7009 | 142.3 |
| stressed/VOL_10 | -3.41% | 14.81% | 43.07% | 4.39% | 12.327 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 70.00% | 0.0303136 |
| calibrated | 68.33% | 0.0257928 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1639 | 1006 | 633 | 49.01% |
| 60m | perp_synchronized_clock | 1639 | 1006 | 633 | 49.01% |
| 60m | combined_synchronized_clock | 1639 | 994 | 645 | 48.89% |
| 15m | perp_original_clock | 1639 | 1006 | 633 | 46.92% |
| 15m | perp_synchronized_clock | 1639 | 1006 | 633 | 46.92% |
| 15m | combined_synchronized_clock | 1639 | 994 | 645 | 46.18% |

## Data usability pilots

- Options: 435 captures; usable 7d RR25 in 363, usable 30d RR25 in 122; 336 valid hourly changes.
- Liquidations: 1185 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1635}`.
- Exchange stress: 869/869 scheduled records. Capture states: `{"missed": 43, "ok": 826}`. Ratings: `{"low": 826}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
