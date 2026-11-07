# Market studies

Generated 2026-11-07T20:07:59.551Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 85 | 49 | 49 |
| range | collecting (descriptive) | 85 | 43 | 36 |
| state | collecting (descriptive) | 339 | 243 | 239 |
| paired | collecting (descriptive) | 1353 | 1259 | 1254 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.102339 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00459879 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00175336 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00154506 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.80% | 13.62% | 64.69% | 4.13% | 98.3086 | 452.864 |
| ordinary/B2_10 | -4.27% | 14.83% | 64.41% | 4.63% | 78.5735 | 408.474 |
| ordinary/VOL_05 | -2.96% | 18.73% | 44.46% | 3.74% | 18.7541 | 78.3691 |
| ordinary/VOL_10 | -2.81% | 17.22% | 45.88% | 3.54% | 15.7192 | 65.5761 |
| stressed/B2_05 | -4.12% | 13.56% | 64.70% | 4.40% | 98.3275 | 786.552 |
| stressed/B2_10 | -4.53% | 14.75% | 64.42% | 4.84% | 78.583 | 675.012 |
| stressed/VOL_05 | -3.02% | 18.69% | 44.46% | 3.75% | 18.7648 | 142.3 |
| stressed/VOL_10 | -2.87% | 17.20% | 45.90% | 3.54% | 15.7382 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 75.00% | 0.0301162 |
| calibrated | 72.22% | 0.0241027 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1254 | 766 | 488 | 49.09% |
| 60m | perp_synchronized_clock | 1254 | 766 | 488 | 49.09% |
| 60m | combined_synchronized_clock | 1254 | 755 | 499 | 49.40% |
| 15m | perp_original_clock | 1254 | 766 | 488 | 47.13% |
| 15m | perp_synchronized_clock | 1254 | 766 | 488 | 47.13% |
| 15m | combined_synchronized_clock | 1254 | 755 | 499 | 46.62% |

## Data usability pilots

- Options: 338 captures; usable 7d RR25 in 283, usable 30d RR25 in 86; 259 valid hourly changes.
- Liquidations: 905 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1259}`.
- Exchange stress: 677/677 scheduled records. Capture states: `{"missed": 43, "ok": 634}`. Ratings: `{"low": 634}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
