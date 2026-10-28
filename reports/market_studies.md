# Market studies

Generated 2026-10-28T05:17:15.442Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 21 | 19 | 19 |
| range | collecting (descriptive) | 21 | 13 | 7 |
| state | collecting (descriptive) | 84 | 55 | 50 |
| paired | collecting (descriptive) | 334 | 248 | 243 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.3503 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00639681 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00150133 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00437243 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.14% | 9.66% | 48.76% | 0.84% | 138.234 | 137.08 |
| ordinary/B2_10 | 0.22% | 9.43% | 49.16% | 0.77% | 89.5688 | 88.8705 |
| ordinary/VOL_05 | 0.31% | 8.93% | 47.49% | 0.67% | 52.6098 | 52.2225 |
| ordinary/VOL_10 | 0.31% | 8.93% | 47.49% | 0.67% | 52.6098 | 52.2225 |
| stressed/B2_05 | 0.03% | 9.61% | 48.76% | 0.88% | 138.373 | 249.236 |
| stressed/B2_10 | 0.14% | 9.31% | 49.17% | 0.78% | 89.6831 | 161.642 |
| stressed/VOL_05 | 0.27% | 8.83% | 47.51% | 0.67% | 52.6785 | 94.9864 |
| stressed/VOL_10 | 0.27% | 8.83% | 47.51% | 0.67% | 52.6785 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 85.71% | 0.0329395 |
| calibrated | 85.71% | 0.0264422 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 243 | 152 | 91 | 50.66% |
| 60m | perp_synchronized_clock | 243 | 152 | 91 | 50.66% |
| 60m | combined_synchronized_clock | 243 | 157 | 86 | 49.68% |
| 15m | perp_original_clock | 243 | 152 | 91 | 47.37% |
| 15m | perp_synchronized_clock | 243 | 152 | 91 | 47.37% |
| 15m | combined_synchronized_clock | 243 | 157 | 86 | 47.13% |

## Data usability pilots

- Options: 84 captures; usable 7d RR25 in 79, usable 30d RR25 in 84; 75 valid hourly changes.
- Liquidations: 154 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 249}`.
- Exchange stress: 167/167 scheduled records. Capture states: `{"missed": 39, "ok": 128}`. Ratings: `{"low": 128}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
