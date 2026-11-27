# Market studies

Generated 2026-11-27T00:47:27.220Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 200 | 163 | 163 |
| range | collecting (descriptive) | 200 | 155 | 148 |
| state | collecting (descriptive) | 799 | 396 | 394 |
| paired | collecting (descriptive) | 3196 | 3098 | 3093 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.293817 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00242112 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00107081 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00149531 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.81% | 15.93% | 44.71% | 13.92% | 85.0832 | 996.551 |
| ordinary/B2_10 | -11.35% | 14.58% | 43.28% | 13.13% | 54.7879 | 815.177 |
| ordinary/VOL_05 | -9.66% | 16.65% | 35.18% | 11.99% | 10.3663 | 98.0562 |
| ordinary/VOL_10 | -9.33% | 16.96% | 36.94% | 11.91% | 6.92671 | 65.5761 |
| stressed/B2_05 | -12.40% | 15.94% | 44.71% | 14.39% | 85.1771 | 1639.22 |
| stressed/B2_10 | -11.74% | 14.56% | 43.29% | 13.45% | 54.8575 | 1229.59 |
| stressed/VOL_05 | -9.74% | 16.64% | 35.18% | 12.02% | 10.3723 | 178.068 |
| stressed/VOL_10 | -9.38% | 16.96% | 36.95% | 11.93% | 6.93567 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.57% | 0.0398104 |
| calibrated | 70.27% | 0.0431853 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3093 | 1738 | 1355 | 48.04% |
| 60m | perp_synchronized_clock | 3093 | 1738 | 1355 | 48.04% |
| 60m | combined_synchronized_clock | 3093 | 1704 | 1389 | 48.30% |
| 15m | perp_original_clock | 3093 | 1738 | 1355 | 48.68% |
| 15m | perp_synchronized_clock | 3093 | 1738 | 1355 | 48.68% |
| 15m | combined_synchronized_clock | 3093 | 1704 | 1389 | 47.54% |

## Data usability pilots

- Options: 798 captures; usable 7d RR25 in 687, usable 30d RR25 in 413; 626 valid hourly changes.
- Liquidations: 2274 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3087}`.
- Exchange stress: 1598/1598 scheduled records. Capture states: `{"missed": 45, "ok": 1553}`. Ratings: `{"low": 1553}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
