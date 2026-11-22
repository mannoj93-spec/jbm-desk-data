# Market studies

Generated 2026-11-22T06:17:20.713Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 171 | 134 | 134 |
| range | collecting (descriptive) | 171 | 127 | 121 |
| state | collecting (descriptive) | 685 | 373 | 371 |
| paired | collecting (descriptive) | 2738 | 2640 | 2635 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.226516 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.0005626 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00161747 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000877609 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.40% | 16.44% | 48.42% | 13.92% | 90.0291 | 928.525 |
| ordinary/B2_10 | -11.74% | 15.06% | 47.05% | 13.13% | 63.4531 | 815.177 |
| ordinary/VOL_05 | -10.12% | 17.22% | 37.02% | 11.99% | 12.0185 | 98.0562 |
| ordinary/VOL_10 | -9.87% | 17.16% | 38.35% | 11.91% | 8.03179 | 65.5761 |
| stressed/B2_05 | -12.93% | 16.44% | 48.43% | 14.39% | 90.1149 | 1516.64 |
| stressed/B2_10 | -12.13% | 15.03% | 47.06% | 13.45% | 63.5182 | 1229.59 |
| stressed/VOL_05 | -10.20% | 17.21% | 37.02% | 12.02% | 12.0251 | 178.068 |
| stressed/VOL_10 | -9.92% | 17.16% | 38.37% | 11.93% | 8.04211 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.46% | 0.0362896 |
| calibrated | 66.12% | 0.0362634 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2635 | 1521 | 1114 | 48.26% |
| 60m | perp_synchronized_clock | 2635 | 1521 | 1114 | 48.26% |
| 60m | combined_synchronized_clock | 2635 | 1496 | 1139 | 48.33% |
| 15m | perp_original_clock | 2635 | 1521 | 1114 | 48.72% |
| 15m | perp_synchronized_clock | 2635 | 1521 | 1114 | 48.72% |
| 15m | combined_synchronized_clock | 2635 | 1496 | 1139 | 47.86% |

## Data usability pilots

- Options: 684 captures; usable 7d RR25 in 581, usable 30d RR25 in 340; 528 valid hourly changes.
- Liquidations: 1932 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2631}`.
- Exchange stress: 1369/1369 scheduled records. Capture states: `{"missed": 45, "ok": 1324}`. Ratings: `{"low": 1324}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
