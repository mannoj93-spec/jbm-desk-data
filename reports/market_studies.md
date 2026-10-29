# Market studies

Generated 2026-10-29T09:46:40.154Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 28 | 26 | 26 |
| range | collecting (descriptive) | 28 | 20 | 14 |
| state | collecting (descriptive) | 112 | 79 | 75 |
| paired | collecting (descriptive) | 448 | 362 | 356 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.911088 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00648485 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.001649 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00210674 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.57% | 10.99% | 47.44% | 0.95% | 151.461 | 203.444 |
| ordinary/B2_10 | -0.49% | 10.93% | 48.09% | 0.90% | 102.158 | 137.307 |
| ordinary/VOL_05 | -0.29% | 12.38% | 48.40% | 0.88% | 43.5369 | 58.5665 |
| ordinary/VOL_10 | -0.24% | 11.66% | 47.54% | 0.79% | 38.8214 | 52.2225 |
| stressed/B2_05 | -0.73% | 10.93% | 47.44% | 1.06% | 151.559 | 369.736 |
| stressed/B2_10 | -0.60% | 10.79% | 48.10% | 0.95% | 102.231 | 249.621 |
| stressed/VOL_05 | -0.33% | 12.31% | 48.41% | 0.88% | 43.5756 | 106.48 |
| stressed/VOL_10 | -0.28% | 11.60% | 47.56% | 0.79% | 38.8723 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 92.86% | 0.0320743 |
| calibrated | 92.86% | 0.0255392 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 356 | 220 | 136 | 48.64% |
| 60m | perp_synchronized_clock | 356 | 220 | 136 | 48.64% |
| 60m | combined_synchronized_clock | 356 | 224 | 132 | 49.55% |
| 15m | perp_original_clock | 356 | 220 | 136 | 44.55% |
| 15m | perp_synchronized_clock | 356 | 220 | 136 | 44.55% |
| 15m | combined_synchronized_clock | 356 | 224 | 132 | 45.09% |

## Data usability pilots

- Options: 112 captures; usable 7d RR25 in 94, usable 30d RR25 in 86; 87 valid hourly changes.
- Liquidations: 238 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 361}`.
- Exchange stress: 224/224 scheduled records. Capture states: `{"missed": 39, "ok": 185}`. Ratings: `{"low": 185}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
