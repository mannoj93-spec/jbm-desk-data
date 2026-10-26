# Market studies

Generated 2026-10-26T11:46:16.558Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 10 | 8 | 8 |
| range | collecting (descriptive) | 10 | 2 | 0 |
| state | collecting (descriptive) | 42 | 22 | 18 |
| paired | collecting (descriptive) | 168 | 84 | 79 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.5511 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00664427 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0102848 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.40% | 12.55% | 52.72% | 0.73% | 221.4 | 97.5299 |
| ordinary/B2_10 | -0.33% | 12.39% | 54.18% | 0.68% | 170.139 | 74.9863 |
| ordinary/VOL_05 | -0.28% | 10.60% | 47.54% | 0.57% | 118.495 | 52.2225 |
| ordinary/VOL_10 | -0.28% | 10.60% | 47.54% | 0.57% | 118.495 | 52.2225 |
| stressed/B2_05 | -0.48% | 12.22% | 52.72% | 0.75% | 221.675 | 177.395 |
| stressed/B2_10 | -0.40% | 12.01% | 54.21% | 0.69% | 170.362 | 136.413 |
| stressed/VOL_05 | -0.32% | 10.28% | 47.56% | 0.57% | 118.645 | 94.9864 |
| stressed/VOL_10 | -0.32% | 10.28% | 47.56% | 0.57% | 118.645 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 79 | 45 | 34 | 53.33% |
| 60m | perp_synchronized_clock | 79 | 45 | 34 | 53.33% |
| 60m | combined_synchronized_clock | 79 | 46 | 33 | 50.00% |
| 15m | perp_original_clock | 79 | 45 | 34 | 35.56% |
| 15m | perp_synchronized_clock | 79 | 45 | 34 | 35.56% |
| 15m | combined_synchronized_clock | 79 | 46 | 33 | 34.78% |

## Data usability pilots

- Options: 42 captures; usable 7d RR25 in 42, usable 30d RR25 in 42; 41 valid hourly changes.
- Liquidations: 32 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 81}`.
- Exchange stress: 84/84 scheduled records. Capture states: `{"missed": 39, "ok": 45}`. Ratings: `{"low": 45}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
