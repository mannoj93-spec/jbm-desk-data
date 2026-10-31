# Market studies

Generated 2026-10-31T05:01:38.350Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 39 | 37 | 37 |
| range | collecting (descriptive) | 39 | 31 | 24 |
| state | collecting (descriptive) | 156 | 108 | 103 |
| paired | collecting (descriptive) | 621 | 535 | 529 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.666241 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00929861 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.0036314 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000827032 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.60% | 15.31% | 43.79% | 1.95% | 137.362 | 302.795 |
| ordinary/B2_10 | -2.01% | 16.76% | 43.78% | 2.36% | 96.1782 | 262.932 |
| ordinary/VOL_05 | -2.10% | 21.52% | 47.92% | 2.93% | 36.3074 | 68.8516 |
| ordinary/VOL_10 | -1.87% | 19.77% | 47.37% | 2.66% | 27.6045 | 52.2225 |
| stressed/B2_05 | -1.81% | 15.28% | 43.80% | 2.09% | 137.447 | 514.703 |
| stressed/B2_10 | -2.16% | 16.68% | 43.79% | 2.45% | 96.2401 | 411.339 |
| stressed/VOL_05 | -2.16% | 21.48% | 47.94% | 2.94% | 36.3325 | 125.006 |
| stressed/VOL_10 | -1.91% | 19.75% | 47.39% | 2.66% | 27.6409 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 75.00% | 0.033152 |
| calibrated | 70.83% | 0.0266413 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 529 | 320 | 209 | 54.06% |
| 60m | perp_synchronized_clock | 529 | 320 | 209 | 54.06% |
| 60m | combined_synchronized_clock | 529 | 317 | 212 | 54.26% |
| 15m | perp_original_clock | 529 | 320 | 209 | 46.88% |
| 15m | perp_synchronized_clock | 529 | 320 | 209 | 46.88% |
| 15m | combined_synchronized_clock | 529 | 317 | 212 | 47.00% |

## Data usability pilots

- Options: 155 captures; usable 7d RR25 in 132, usable 30d RR25 in 86; 124 valid hourly changes.
- Liquidations: 370 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 537}`.
- Exchange stress: 311/311 scheduled records. Capture states: `{"missed": 39, "ok": 272}`. Ratings: `{"low": 272}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
