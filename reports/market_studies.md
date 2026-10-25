# Market studies

Generated 2026-10-25T21:46:16.472Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 7 | 5 | 5 |
| range | registered; not launched | 7 | 0 | 0 |
| state | collecting (descriptive) | 28 | 10 | 9 |
| paired | collecting (descriptive) | 112 | 36 | 34 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 4.68301 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.0126124 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00919118 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.17% | 14.58% | 54.73% | 0.45% | 363.042 | 91.8244 |
| ordinary/B2_10 | 0.27% | 13.41% | 55.63% | 0.39% | 241.493 | 61.0952 |
| ordinary/VOL_05 | 0.23% | 11.47% | 47.56% | 0.33% | 206.463 | 52.2225 |
| ordinary/VOL_10 | 0.23% | 11.47% | 47.56% | 0.33% | 206.463 | 52.2225 |
| stressed/B2_05 | 0.09% | 14.32% | 54.74% | 0.46% | 363.472 | 167.024 |
| stressed/B2_10 | 0.22% | 12.98% | 55.66% | 0.39% | 241.801 | 111.125 |
| stressed/VOL_05 | 0.19% | 11.10% | 47.58% | 0.33% | 206.715 | 94.9864 |
| stressed/VOL_10 | 0.19% | 11.10% | 47.58% | 0.33% | 206.715 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 34 | 24 | 10 | 45.83% |
| 60m | perp_synchronized_clock | 34 | 24 | 10 | 45.83% |
| 60m | combined_synchronized_clock | 34 | 25 | 9 | 44.00% |
| 15m | perp_original_clock | 34 | 24 | 10 | 50.00% |
| 15m | perp_synchronized_clock | 34 | 24 | 10 | 50.00% |
| 15m | combined_synchronized_clock | 34 | 25 | 9 | 48.00% |

## Data usability pilots

- Options: 28 captures; usable 7d RR25 in 28, usable 30d RR25 in 28; 27 valid hourly changes.
- Liquidations: 8 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 54, "ok": 29}`.
- Exchange stress: 56/56 scheduled records. Capture states: `{"missed": 36, "ok": 20}`. Ratings: `{"low": 20}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
