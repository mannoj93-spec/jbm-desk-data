# Market studies

Generated 2026-10-26T21:35:22.972Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 13 | 11 | 11 |
| range | collecting (descriptive) | 13 | 5 | 0 |
| state | collecting (descriptive) | 52 | 28 | 26 |
| paired | collecting (descriptive) | 207 | 123 | 118 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.94801 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00184943 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0132415 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.40% | 11.00% | 50.43% | 0.73% | 184.291 | 108.911 |
| ordinary/B2_10 | -0.36% | 10.82% | 51.29% | 0.71% | 126.822 | 74.9863 |
| ordinary/VOL_05 | -0.30% | 9.63% | 47.51% | 0.60% | 88.3065 | 52.2225 |
| ordinary/VOL_10 | -0.30% | 9.63% | 47.51% | 0.60% | 88.3065 | 52.2225 |
| stressed/B2_05 | -0.49% | 10.80% | 50.43% | 0.76% | 184.491 | 198.066 |
| stressed/B2_10 | -0.42% | 10.55% | 51.31% | 0.72% | 126.995 | 136.413 |
| stressed/VOL_05 | -0.35% | 9.41% | 47.54% | 0.60% | 88.42 | 94.9864 |
| stressed/VOL_10 | -0.35% | 9.41% | 47.54% | 0.60% | 88.42 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 118 | 66 | 52 | 53.03% |
| 60m | perp_synchronized_clock | 118 | 66 | 52 | 53.03% |
| 60m | combined_synchronized_clock | 118 | 71 | 47 | 49.30% |
| 15m | perp_original_clock | 118 | 66 | 52 | 42.42% |
| 15m | perp_synchronized_clock | 118 | 66 | 52 | 42.42% |
| 15m | combined_synchronized_clock | 118 | 71 | 47 | 42.25% |

## Data usability pilots

- Options: 52 captures; usable 7d RR25 in 52, usable 30d RR25 in 52; 49 valid hourly changes.
- Liquidations: 58 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 121}`.
- Exchange stress: 104/104 scheduled records. Capture states: `{"missed": 39, "ok": 65}`. Ratings: `{"low": 65}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
