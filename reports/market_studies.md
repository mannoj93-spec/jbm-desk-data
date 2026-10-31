# Market studies

Generated 2026-10-31T00:18:53.222Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 38 | 36 | 36 |
| range | collecting (descriptive) | 38 | 30 | 23 |
| state | collecting (descriptive) | 151 | 103 | 99 |
| paired | collecting (descriptive) | 602 | 516 | 511 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.541271 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00998448 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00489176 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000611546 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.46% | 15.51% | 43.57% | 1.95% | 129.921 | 239.455 |
| ordinary/B2_10 | -1.83% | 16.97% | 43.56% | 2.31% | 83.1242 | 153.491 |
| ordinary/VOL_05 | -2.05% | 21.84% | 48.06% | 2.93% | 37.2883 | 68.8516 |
| ordinary/VOL_10 | -1.81% | 20.06% | 47.39% | 2.66% | 28.3518 | 52.2225 |
| stressed/B2_05 | -1.66% | 15.48% | 43.58% | 2.09% | 130.005 | 434.795 |
| stressed/B2_10 | -1.96% | 16.88% | 43.57% | 2.37% | 83.1816 | 278.561 |
| stressed/VOL_05 | -2.10% | 21.79% | 48.08% | 2.94% | 37.3139 | 125.006 |
| stressed/VOL_10 | -1.85% | 20.04% | 47.41% | 2.66% | 28.3891 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.91% | 0.0326878 |
| calibrated | 69.57% | 0.0261756 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 511 | 306 | 205 | 53.59% |
| 60m | perp_synchronized_clock | 511 | 306 | 205 | 53.59% |
| 60m | combined_synchronized_clock | 511 | 305 | 206 | 53.77% |
| 15m | perp_original_clock | 511 | 306 | 205 | 46.73% |
| 15m | perp_synchronized_clock | 511 | 306 | 205 | 46.73% |
| 15m | combined_synchronized_clock | 511 | 305 | 206 | 47.21% |

## Data usability pilots

- Options: 151 captures; usable 7d RR25 in 128, usable 30d RR25 in 86; 120 valid hourly changes.
- Liquidations: 355 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 517}`.
- Exchange stress: 301/301 scheduled records. Capture states: `{"missed": 39, "ok": 262}`. Ratings: `{"low": 262}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
