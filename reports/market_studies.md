# Market studies

Generated 2026-11-26T22:17:58.189Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 199 | 162 | 162 |
| range | collecting (descriptive) | 199 | 154 | 148 |
| state | collecting (descriptive) | 797 | 395 | 393 |
| paired | collecting (descriptive) | 3186 | 3088 | 3083 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.308151 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00242112 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00115848 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00160152 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.77% | 15.98% | 44.78% | 13.92% | 84.8764 | 990.918 |
| ordinary/B2_10 | -11.33% | 14.63% | 43.39% | 13.13% | 55.0477 | 815.177 |
| ordinary/VOL_05 | -9.64% | 16.70% | 35.23% | 11.99% | 10.4158 | 98.0562 |
| ordinary/VOL_10 | -9.30% | 17.01% | 36.98% | 11.91% | 6.95981 | 65.5761 |
| stressed/B2_05 | -12.36% | 15.99% | 44.79% | 14.39% | 84.9706 | 1629.05 |
| stressed/B2_10 | -11.71% | 14.61% | 43.40% | 13.45% | 55.1173 | 1229.59 |
| stressed/VOL_05 | -9.71% | 16.69% | 35.23% | 12.02% | 10.4218 | 178.068 |
| stressed/VOL_10 | -9.35% | 17.01% | 36.99% | 11.93% | 6.96881 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.57% | 0.0398104 |
| calibrated | 70.27% | 0.0431853 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3083 | 1734 | 1349 | 47.98% |
| 60m | perp_synchronized_clock | 3083 | 1734 | 1349 | 47.98% |
| 60m | combined_synchronized_clock | 3083 | 1699 | 1384 | 48.26% |
| 15m | perp_original_clock | 3083 | 1734 | 1349 | 48.67% |
| 15m | perp_synchronized_clock | 3083 | 1734 | 1349 | 48.67% |
| 15m | combined_synchronized_clock | 3083 | 1699 | 1384 | 47.56% |

## Data usability pilots

- Options: 796 captures; usable 7d RR25 in 685, usable 30d RR25 in 413; 625 valid hourly changes.
- Liquidations: 2268 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3079}`.
- Exchange stress: 1593/1593 scheduled records. Capture states: `{"missed": 45, "ok": 1548}`. Ratings: `{"low": 1548}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
