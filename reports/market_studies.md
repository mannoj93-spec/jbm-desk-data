# Market studies

Generated 2026-10-27T01:03:37.742Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 14 | 12 | 12 |
| range | collecting (descriptive) | 14 | 6 | 0 |
| state | collecting (descriptive) | 56 | 32 | 27 |
| paired | collecting (descriptive) | 221 | 135 | 132 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.35849 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00042012 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0118371 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.26% | 10.72% | 49.35% | 0.73% | 169.876 | 108.911 |
| ordinary/B2_10 | -0.20% | 10.62% | 50.62% | 0.71% | 116.903 | 74.9863 |
| ordinary/VOL_05 | -0.13% | 9.58% | 47.50% | 0.60% | 81.3975 | 52.2225 |
| ordinary/VOL_10 | -0.13% | 9.58% | 47.50% | 0.60% | 81.3975 | 52.2225 |
| stressed/B2_05 | -0.35% | 10.56% | 49.36% | 0.76% | 170.064 | 198.066 |
| stressed/B2_10 | -0.26% | 10.39% | 50.64% | 0.72% | 117.064 | 136.413 |
| stressed/VOL_05 | -0.17% | 9.40% | 47.52% | 0.60% | 81.5024 | 94.9864 |
| stressed/VOL_10 | -0.17% | 9.40% | 47.52% | 0.60% | 81.5024 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 132 | 77 | 55 | 53.25% |
| 60m | perp_synchronized_clock | 132 | 77 | 55 | 53.25% |
| 60m | combined_synchronized_clock | 132 | 82 | 50 | 50.00% |
| 15m | perp_original_clock | 132 | 77 | 55 | 44.16% |
| 15m | perp_synchronized_clock | 132 | 77 | 55 | 44.16% |
| 15m | combined_synchronized_clock | 132 | 82 | 50 | 42.68% |

## Data usability pilots

- Options: 55 captures; usable 7d RR25 in 55, usable 30d RR25 in 55; 52 valid hourly changes.
- Liquidations: 70 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 137}`.
- Exchange stress: 111/111 scheduled records. Capture states: `{"missed": 39, "ok": 72}`. Ratings: `{"low": 72}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
