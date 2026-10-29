# Market studies

Generated 2026-10-29T22:32:53.417Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 31 | 29 | 29 |
| range | collecting (descriptive) | 31 | 23 | 17 |
| state | collecting (descriptive) | 125 | 87 | 86 |
| paired | collecting (descriptive) | 499 | 413 | 408 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.292169 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00648338 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00356555 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00291054 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.21% | 13.27% | 46.62% | 0.95% | 150.335 | 224.563 |
| ordinary/B2_10 | -0.32% | 13.19% | 47.33% | 0.90% | 91.8643 | 137.307 |
| ordinary/VOL_05 | -0.06% | 15.89% | 48.89% | 0.88% | 39.1413 | 58.5665 |
| ordinary/VOL_10 | -0.04% | 14.60% | 47.54% | 0.79% | 34.9016 | 52.2225 |
| stressed/B2_05 | -0.39% | 13.26% | 46.63% | 1.06% | 150.416 | 408.054 |
| stressed/B2_10 | -0.44% | 13.09% | 47.34% | 0.95% | 91.9344 | 249.621 |
| stressed/VOL_05 | -0.11% | 15.84% | 48.91% | 0.88% | 39.1764 | 106.48 |
| stressed/VOL_10 | -0.09% | 14.56% | 47.56% | 0.79% | 34.9474 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 94.12% | 0.0322052 |
| calibrated | 94.12% | 0.0256805 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 408 | 251 | 157 | 50.20% |
| 60m | perp_synchronized_clock | 408 | 251 | 157 | 50.20% |
| 60m | combined_synchronized_clock | 408 | 252 | 156 | 51.19% |
| 15m | perp_original_clock | 408 | 251 | 157 | 43.82% |
| 15m | perp_synchronized_clock | 408 | 251 | 157 | 43.82% |
| 15m | combined_synchronized_clock | 408 | 252 | 156 | 44.84% |

## Data usability pilots

- Options: 125 captures; usable 7d RR25 in 102, usable 30d RR25 in 86; 94 valid hourly changes.
- Liquidations: 277 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 413}`.
- Exchange stress: 250/250 scheduled records. Capture states: `{"missed": 39, "ok": 211}`. Ratings: `{"low": 211}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
