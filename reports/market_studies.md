# Market studies

Generated 2026-10-31T01:31:36.513Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 38 | 36 | 36 |
| range | collecting (descriptive) | 38 | 30 | 24 |
| state | collecting (descriptive) | 152 | 104 | 99 |
| paired | collecting (descriptive) | 607 | 521 | 516 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.541271 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00929861 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00489176 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000847868 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 75.00% | 0.033152 |
| calibrated | 70.83% | 0.0266413 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 516 | 309 | 207 | 53.72% |
| 60m | perp_synchronized_clock | 516 | 309 | 207 | 53.72% |
| 60m | combined_synchronized_clock | 516 | 306 | 210 | 53.92% |
| 15m | perp_original_clock | 516 | 309 | 207 | 46.93% |
| 15m | perp_synchronized_clock | 516 | 309 | 207 | 46.93% |
| 15m | combined_synchronized_clock | 516 | 306 | 210 | 47.06% |

## Data usability pilots

- Options: 152 captures; usable 7d RR25 in 129, usable 30d RR25 in 86; 121 valid hourly changes.
- Liquidations: 358 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 521}`.
- Exchange stress: 304/304 scheduled records. Capture states: `{"missed": 39, "ok": 265}`. Ratings: `{"low": 265}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
