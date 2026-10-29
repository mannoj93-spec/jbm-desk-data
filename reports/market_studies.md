# Market studies

Generated 2026-10-29T16:19:16.244Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 30 | 28 | 28 |
| range | collecting (descriptive) | 30 | 22 | 15 |
| state | collecting (descriptive) | 119 | 85 | 81 |
| paired | collecting (descriptive) | 474 | 388 | 383 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.337637 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.0064843 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00265089 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00179504 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.26% | 12.83% | 47.13% | 0.95% | 144.849 | 209.052 |
| ordinary/B2_10 | 0.25% | 12.36% | 47.56% | 0.90% | 95.0766 | 137.307 |
| ordinary/VOL_05 | 0.70% | 14.58% | 48.73% | 0.88% | 40.515 | 58.5665 |
| ordinary/VOL_10 | 0.63% | 13.49% | 47.53% | 0.79% | 36.1256 | 52.2225 |
| stressed/B2_05 | 0.09% | 12.79% | 47.14% | 1.06% | 144.944 | 379.909 |
| stressed/B2_10 | 0.14% | 12.27% | 47.57% | 0.95% | 95.1476 | 249.621 |
| stressed/VOL_05 | 0.65% | 14.53% | 48.74% | 0.88% | 40.5512 | 106.48 |
| stressed/VOL_10 | 0.59% | 13.45% | 47.55% | 0.79% | 36.173 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 93.33% | 0.0320994 |
| calibrated | 93.33% | 0.0255683 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 383 | 239 | 144 | 49.79% |
| 60m | perp_synchronized_clock | 383 | 239 | 144 | 49.79% |
| 60m | combined_synchronized_clock | 383 | 240 | 143 | 50.42% |
| 15m | perp_original_clock | 383 | 239 | 144 | 43.93% |
| 15m | perp_synchronized_clock | 383 | 239 | 144 | 43.93% |
| 15m | combined_synchronized_clock | 383 | 240 | 143 | 44.17% |

## Data usability pilots

- Options: 119 captures; usable 7d RR25 in 96, usable 30d RR25 in 86; 88 valid hourly changes.
- Liquidations: 259 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 389}`.
- Exchange stress: 237/237 scheduled records. Capture states: `{"missed": 39, "ok": 198}`. Ratings: `{"low": 198}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
