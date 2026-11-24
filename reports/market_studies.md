# Market studies

Generated 2026-11-24T09:33:24.527Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 184 | 147 | 147 |
| range | collecting (descriptive) | 184 | 140 | 134 |
| state | collecting (descriptive) | 736 | 382 | 380 |
| paired | collecting (descriptive) | 2943 | 2845 | 2840 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.410799 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000807105 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00190249 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00127641 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.79% | 16.45% | 46.52% | 13.92% | 89.2482 | 972.794 |
| ordinary/B2_10 | -11.43% | 15.05% | 45.22% | 13.13% | 59.2481 | 815.177 |
| ordinary/VOL_05 | -9.75% | 17.20% | 36.13% | 11.99% | 11.2159 | 98.0562 |
| ordinary/VOL_10 | -9.44% | 17.41% | 37.68% | 11.91% | 7.49465 | 65.5761 |
| stressed/B2_05 | -12.37% | 16.46% | 46.53% | 14.39% | 89.3333 | 1596.61 |
| stressed/B2_10 | -11.81% | 15.03% | 45.23% | 13.45% | 59.3161 | 1229.59 |
| stressed/VOL_05 | -9.83% | 17.19% | 36.14% | 12.02% | 11.2222 | 178.068 |
| stressed/VOL_10 | -9.49% | 17.41% | 37.69% | 11.93% | 7.50432 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.42% | 0.0378552 |
| calibrated | 68.66% | 0.039385 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2840 | 1614 | 1226 | 48.33% |
| 60m | perp_synchronized_clock | 2840 | 1614 | 1226 | 48.33% |
| 60m | combined_synchronized_clock | 2840 | 1588 | 1252 | 48.55% |
| 15m | perp_original_clock | 2840 | 1614 | 1226 | 48.82% |
| 15m | perp_synchronized_clock | 2840 | 1614 | 1226 | 48.82% |
| 15m | combined_synchronized_clock | 2840 | 1588 | 1252 | 47.98% |

## Data usability pilots

- Options: 735 captures; usable 7d RR25 in 632, usable 30d RR25 in 391; 579 valid hourly changes.
- Liquidations: 2085 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2835}`.
- Exchange stress: 1472/1472 scheduled records. Capture states: `{"missed": 45, "ok": 1427}`. Ratings: `{"low": 1427}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
