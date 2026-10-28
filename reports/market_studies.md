# Market studies

Generated 2026-10-28T00:18:48.010Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 20 | 18 | 18 |
| range | collecting (descriptive) | 20 | 12 | 5 |
| state | collecting (descriptive) | 79 | 50 | 46 |
| paired | collecting (descriptive) | 314 | 228 | 223 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.947885 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00629747 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 4.45046e-05 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00532511 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.02% | 9.86% | 48.76% | 0.84% | 137.459 | 129.407 |
| ordinary/B2_10 | 0.07% | 9.58% | 48.81% | 0.77% | 94.3471 | 88.8705 |
| ordinary/VOL_05 | 0.18% | 9.11% | 47.49% | 0.67% | 55.4188 | 52.2225 |
| ordinary/VOL_10 | 0.18% | 9.11% | 47.49% | 0.67% | 55.4188 | 52.2225 |
| stressed/B2_05 | -0.09% | 9.81% | 48.77% | 0.88% | 137.607 | 235.296 |
| stressed/B2_10 | -0.01% | 9.44% | 48.83% | 0.78% | 94.4665 | 161.642 |
| stressed/VOL_05 | 0.14% | 9.00% | 47.51% | 0.67% | 55.491 | 94.9864 |
| stressed/VOL_10 | 0.14% | 9.00% | 47.51% | 0.67% | 55.491 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 80.00% | 0.0331598 |
| calibrated | 80.00% | 0.0267218 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 223 | 138 | 85 | 50.72% |
| 60m | perp_synchronized_clock | 223 | 138 | 85 | 50.72% |
| 60m | combined_synchronized_clock | 223 | 145 | 78 | 49.66% |
| 15m | perp_original_clock | 223 | 138 | 85 | 47.10% |
| 15m | perp_synchronized_clock | 223 | 138 | 85 | 47.10% |
| 15m | combined_synchronized_clock | 223 | 145 | 78 | 46.90% |

## Data usability pilots

- Options: 79 captures; usable 7d RR25 in 74, usable 30d RR25 in 79; 70 valid hourly changes.
- Liquidations: 139 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 229}`.
- Exchange stress: 157/157 scheduled records. Capture states: `{"missed": 39, "ok": 118}`. Ratings: `{"low": 118}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
