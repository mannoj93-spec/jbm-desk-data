# Market studies

Generated 2026-10-31T18:01:50.097Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 42 | 40 | 40 |
| range | collecting (descriptive) | 42 | 34 | 28 |
| state | collecting (descriptive) | 169 | 117 | 114 |
| paired | collecting (descriptive) | 673 | 587 | 582 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.775268 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00704502 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000916291 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00214777 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.34% | 14.80% | 45.08% | 1.95% | 134.559 | 317.374 |
| ordinary/B2_10 | -1.77% | 16.19% | 44.97% | 2.36% | 95.7562 | 276.217 |
| ordinary/VOL_05 | -1.91% | 20.72% | 47.56% | 2.93% | 33.6903 | 68.8516 |
| ordinary/VOL_10 | -1.66% | 19.05% | 47.31% | 2.66% | 25.6109 | 52.2225 |
| stressed/B2_05 | -1.56% | 14.77% | 45.08% | 2.09% | 134.641 | 541.139 |
| stressed/B2_10 | -1.93% | 16.12% | 44.98% | 2.45% | 95.8137 | 435.443 |
| stressed/VOL_05 | -1.96% | 20.68% | 47.58% | 2.94% | 33.7139 | 125.006 |
| stressed/VOL_10 | -1.70% | 19.03% | 47.33% | 2.66% | 25.6446 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 78.57% | 0.0326497 |
| calibrated | 75.00% | 0.0261439 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 582 | 350 | 232 | 52.57% |
| 60m | perp_synchronized_clock | 582 | 350 | 232 | 52.57% |
| 60m | combined_synchronized_clock | 582 | 346 | 236 | 53.18% |
| 15m | perp_original_clock | 582 | 350 | 232 | 47.71% |
| 15m | perp_synchronized_clock | 582 | 350 | 232 | 47.71% |
| 15m | combined_synchronized_clock | 582 | 346 | 236 | 47.98% |

## Data usability pilots

- Options: 168 captures; usable 7d RR25 in 145, usable 30d RR25 in 86; 137 valid hourly changes.
- Liquidations: 409 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 589}`.
- Exchange stress: 337/337 scheduled records. Capture states: `{"missed": 39, "ok": 298}`. Ratings: `{"low": 298}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
