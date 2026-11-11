# Market studies

Generated 2026-11-11T10:32:03.503Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 106 | 70 | 70 |
| range | collecting (descriptive) | 106 | 64 | 58 |
| state | collecting (descriptive) | 425 | 295 | 292 |
| paired | collecting (descriptive) | 1699 | 1605 | 1600 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.00444243 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00425071 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000859901 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00046875 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.14% | 12.97% | 60.99% | 5.64% | 110.029 | 739.372 |
| ordinary/B2_10 | -5.60% | 13.87% | 60.36% | 6.11% | 87.0927 | 688.033 |
| ordinary/VOL_05 | -3.73% | 16.29% | 42.21% | 4.58% | 15.0999 | 78.3691 |
| ordinary/VOL_10 | -3.59% | 15.10% | 43.34% | 4.38% | 12.6538 | 65.5761 |
| stressed/B2_05 | -5.59% | 12.95% | 61.00% | 6.03% | 110.048 | 1200.26 |
| stressed/B2_10 | -5.95% | 13.80% | 60.37% | 6.41% | 87.1133 | 1052.22 |
| stressed/VOL_05 | -3.80% | 16.26% | 42.21% | 4.60% | 15.1092 | 142.3 |
| stressed/VOL_10 | -3.64% | 15.08% | 43.36% | 4.39% | 12.6695 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.97% | 0.0299309 |
| calibrated | 67.24% | 0.0252529 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1600 | 986 | 614 | 48.88% |
| 60m | perp_synchronized_clock | 1600 | 986 | 614 | 48.88% |
| 60m | combined_synchronized_clock | 1600 | 974 | 626 | 48.87% |
| 15m | perp_original_clock | 1600 | 986 | 614 | 47.06% |
| 15m | perp_synchronized_clock | 1600 | 986 | 614 | 47.06% |
| 15m | combined_synchronized_clock | 1600 | 974 | 626 | 46.30% |

## Data usability pilots

- Options: 425 captures; usable 7d RR25 in 357, usable 30d RR25 in 112; 330 valid hourly changes.
- Liquidations: 1155 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1595}`.
- Exchange stress: 850/850 scheduled records. Capture states: `{"missed": 43, "ok": 807}`. Ratings: `{"low": 807}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
