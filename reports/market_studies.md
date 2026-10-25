# Market studies

Generated 2026-10-25T12:01:04.022Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 5 | 4 | 4 |
| range | registered; not launched | 5 | 0 | 0 |
| state | collecting (descriptive) | 19 | 7 | 5 |
| paired | collecting (descriptive) | 73 | 24 | 22 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 3.86594 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.0170617 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.12% | 16.62% | 56.34% | 0.45% | 544.665 | 81.1008 |
| ordinary/B2_10 | -0.04% | 15.26% | 55.67% | 0.39% | 410.286 | 61.0952 |
| ordinary/VOL_05 | -0.04% | 13.05% | 47.60% | 0.33% | 350.801 | 52.2225 |
| ordinary/VOL_10 | -0.04% | 13.05% | 47.60% | 0.33% | 350.801 | 52.2225 |
| stressed/B2_05 | -0.18% | 15.99% | 56.35% | 0.46% | 545.384 | 147.534 |
| stressed/B2_10 | -0.09% | 14.42% | 55.70% | 0.39% | 410.792 | 111.125 |
| stressed/VOL_05 | -0.08% | 12.33% | 47.62% | 0.33% | 351.217 | 94.9864 |
| stressed/VOL_10 | -0.08% | 12.33% | 47.62% | 0.33% | 351.217 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 22 | 16 | 6 | 31.25% |
| 60m | perp_synchronized_clock | 22 | 16 | 6 | 31.25% |
| 60m | combined_synchronized_clock | 22 | 16 | 6 | 31.25% |
| 15m | perp_original_clock | 22 | 16 | 6 | 43.75% |
| 15m | perp_synchronized_clock | 22 | 16 | 6 | 43.75% |
| 15m | combined_synchronized_clock | 22 | 16 | 6 | 43.75% |

## Data usability pilots

- Options: 18 captures; usable 7d RR25 in 18, usable 30d RR25 in 18; 17 valid hourly changes.
- Liquidations: 4 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 30, "ok": 17}`.
- Exchange stress: 37/37 scheduled records. Capture states: `{"missed": 25, "ok": 12}`. Ratings: `{"low": 12}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
