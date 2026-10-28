# Market studies

Generated 2026-10-28T15:46:31.680Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 23 | 21 | 21 |
| range | collecting (descriptive) | 23 | 15 | 9 |
| state | collecting (descriptive) | 94 | 63 | 61 |
| paired | collecting (descriptive) | 376 | 290 | 285 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.81608 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00645201 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000368582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000877193 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.15% | 9.32% | 49.29% | 0.84% | 137.226 | 149.891 |
| ordinary/B2_10 | 0.26% | 9.10% | 49.76% | 0.77% | 81.3138 | 88.8705 |
| ordinary/VOL_05 | 0.35% | 8.58% | 47.51% | 0.67% | 47.7591 | 52.2225 |
| ordinary/VOL_10 | 0.35% | 8.58% | 47.51% | 0.67% | 47.7591 | 52.2225 |
| stressed/B2_05 | 0.03% | 9.29% | 49.30% | 0.88% | 137.36 | 272.506 |
| stressed/B2_10 | 0.19% | 8.99% | 49.77% | 0.78% | 81.4191 | 161.642 |
| stressed/VOL_05 | 0.31% | 8.49% | 47.53% | 0.67% | 47.8215 | 94.9864 |
| stressed/VOL_10 | 0.31% | 8.49% | 47.53% | 0.67% | 47.8215 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 88.89% | 0.0325896 |
| calibrated | 88.89% | 0.0260595 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 285 | 176 | 109 | 49.43% |
| 60m | perp_synchronized_clock | 285 | 176 | 109 | 49.43% |
| 60m | combined_synchronized_clock | 285 | 180 | 105 | 49.44% |
| 15m | perp_original_clock | 285 | 176 | 109 | 46.59% |
| 15m | perp_synchronized_clock | 285 | 176 | 109 | 46.59% |
| 15m | combined_synchronized_clock | 285 | 180 | 105 | 46.11% |

## Data usability pilots

- Options: 94 captures; usable 7d RR25 in 81, usable 30d RR25 in 86; 77 valid hourly changes.
- Liquidations: 184 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 289}`.
- Exchange stress: 188/188 scheduled records. Capture states: `{"missed": 39, "ok": 149}`. Ratings: `{"low": 149}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
