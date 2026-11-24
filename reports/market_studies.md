# Market studies

Generated 2026-11-24T06:32:49.394Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 183 | 146 | 146 |
| range | collecting (descriptive) | 183 | 139 | 133 |
| state | collecting (descriptive) | 733 | 381 | 380 |
| paired | collecting (descriptive) | 2931 | 2833 | 2828 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.41235 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000903887 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00190249 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00128182 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.75% | 16.51% | 46.68% | 13.92% | 88.8931 | 965.876 |
| ordinary/B2_10 | -11.39% | 15.11% | 45.36% | 13.13% | 59.5498 | 815.177 |
| ordinary/VOL_05 | -9.71% | 17.26% | 36.20% | 11.99% | 11.2734 | 98.0562 |
| ordinary/VOL_10 | -9.38% | 17.48% | 37.73% | 11.91% | 7.53313 | 65.5761 |
| stressed/B2_05 | -12.32% | 16.52% | 46.69% | 14.39% | 88.9797 | 1584.12 |
| stressed/B2_10 | -11.77% | 15.08% | 45.36% | 13.45% | 59.6176 | 1229.59 |
| stressed/VOL_05 | -9.78% | 17.25% | 36.20% | 12.02% | 11.2798 | 178.068 |
| stressed/VOL_10 | -9.43% | 17.47% | 37.74% | 11.93% | 7.54284 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.92% | 0.0377374 |
| calibrated | 68.42% | 0.039121 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2828 | 1609 | 1219 | 48.35% |
| 60m | perp_synchronized_clock | 2828 | 1609 | 1219 | 48.35% |
| 60m | combined_synchronized_clock | 2828 | 1583 | 1245 | 48.58% |
| 15m | perp_original_clock | 2828 | 1609 | 1219 | 48.79% |
| 15m | perp_synchronized_clock | 2828 | 1609 | 1219 | 48.79% |
| 15m | combined_synchronized_clock | 2828 | 1583 | 1245 | 47.95% |

## Data usability pilots

- Options: 732 captures; usable 7d RR25 in 629, usable 30d RR25 in 388; 576 valid hourly changes.
- Liquidations: 2076 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2823}`.
- Exchange stress: 1466/1466 scheduled records. Capture states: `{"missed": 45, "ok": 1421}`. Ratings: `{"low": 1421}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
