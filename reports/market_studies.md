# Market studies

Generated 2026-11-20T14:32:33.572Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 161 | 125 | 125 |
| range | collecting (descriptive) | 161 | 118 | 112 |
| state | collecting (descriptive) | 645 | 365 | 365 |
| paired | collecting (descriptive) | 2579 | 2481 | 2476 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0254042 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00463682 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00076659 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00075727 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.26% | 14.44% | 49.95% | 11.55% | 91.8138 | 902.969 |
| ordinary/B2_10 | -11.06% | 14.06% | 48.70% | 11.38% | 67.1104 | 815.177 |
| ordinary/VOL_05 | -9.32% | 16.03% | 37.83% | 9.95% | 12.716 | 98.0562 |
| ordinary/VOL_10 | -8.92% | 15.20% | 38.99% | 9.50% | 8.49787 | 65.5761 |
| stressed/B2_05 | -11.78% | 14.43% | 49.95% | 12.02% | 91.8976 | 1470.45 |
| stressed/B2_10 | -11.44% | 14.02% | 48.71% | 11.71% | 67.1727 | 1229.59 |
| stressed/VOL_05 | -9.39% | 16.02% | 37.83% | 9.98% | 12.7228 | 178.068 |
| stressed/VOL_10 | -8.97% | 15.19% | 39.00% | 9.51% | 8.50876 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.64% | 0.0358715 |
| calibrated | 68.75% | 0.03514 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2476 | 1450 | 1026 | 47.86% |
| 60m | perp_synchronized_clock | 2476 | 1450 | 1026 | 47.86% |
| 60m | combined_synchronized_clock | 2476 | 1428 | 1048 | 47.90% |
| 15m | perp_original_clock | 2476 | 1450 | 1026 | 48.34% |
| 15m | perp_synchronized_clock | 2476 | 1450 | 1026 | 48.34% |
| 15m | combined_synchronized_clock | 2476 | 1428 | 1048 | 47.34% |

## Data usability pilots

- Options: 645 captures; usable 7d RR25 in 544, usable 30d RR25 in 303; 493 valid hourly changes.
- Liquidations: 1815 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2475}`.
- Exchange stress: 1290/1290 scheduled records. Capture states: `{"missed": 45, "ok": 1245}`. Ratings: `{"low": 1245}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
