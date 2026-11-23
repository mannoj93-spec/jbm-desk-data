# Market studies

Generated 2026-11-23T11:02:40.231Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 178 | 141 | 141 |
| range | collecting (descriptive) | 178 | 134 | 128 |
| state | collecting (descriptive) | 714 | 378 | 377 |
| paired | collecting (descriptive) | 2853 | 2755 | 2750 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.321486 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000172186 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00198816 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00125 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.64% | 16.49% | 47.41% | 13.92% | 88.6515 | 944.385 |
| ordinary/B2_10 | -11.14% | 15.07% | 46.03% | 13.13% | 61.1221 | 815.177 |
| ordinary/VOL_05 | -9.41% | 17.21% | 36.52% | 11.99% | 11.5736 | 98.0562 |
| ordinary/VOL_10 | -9.04% | 17.30% | 37.97% | 11.91% | 7.73408 | 65.5761 |
| stressed/B2_05 | -12.19% | 16.50% | 47.42% | 14.39% | 88.7391 | 1545.29 |
| stressed/B2_10 | -11.52% | 15.04% | 46.04% | 13.45% | 61.189 | 1229.59 |
| stressed/VOL_05 | -9.49% | 17.20% | 36.52% | 12.02% | 11.58 | 178.068 |
| stressed/VOL_10 | -9.09% | 17.30% | 37.99% | 11.93% | 7.74404 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.41% | 0.0369942 |
| calibrated | 67.97% | 0.0376735 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2750 | 1570 | 1180 | 48.28% |
| 60m | perp_synchronized_clock | 2750 | 1570 | 1180 | 48.28% |
| 60m | combined_synchronized_clock | 2750 | 1543 | 1207 | 48.48% |
| 15m | perp_original_clock | 2750 | 1570 | 1180 | 48.92% |
| 15m | perp_synchronized_clock | 2750 | 1570 | 1180 | 48.92% |
| 15m | combined_synchronized_clock | 2750 | 1543 | 1207 | 48.02% |

## Data usability pilots

- Options: 712 captures; usable 7d RR25 in 609, usable 30d RR25 in 368; 556 valid hourly changes.
- Liquidations: 2019 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2747}`.
- Exchange stress: 1427/1427 scheduled records. Capture states: `{"missed": 45, "ok": 1382}`. Ratings: `{"low": 1382}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
