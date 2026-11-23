# Market studies

Generated 2026-11-23T12:47:40.861Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 179 | 142 | 142 |
| range | collecting (descriptive) | 179 | 135 | 128 |
| state | collecting (descriptive) | 715 | 378 | 377 |
| paired | collecting (descriptive) | 2860 | 2762 | 2757 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.320455 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000172186 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00198816 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00124683 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.63% | 16.44% | 47.26% | 13.92% | 88.187 | 944.385 |
| ordinary/B2_10 | -11.14% | 15.02% | 45.89% | 13.13% | 60.7992 | 815.177 |
| ordinary/VOL_05 | -9.41% | 17.15% | 36.45% | 11.99% | 11.5119 | 98.0562 |
| ordinary/VOL_10 | -9.03% | 17.24% | 37.92% | 11.91% | 7.69282 | 65.5761 |
| stressed/B2_05 | -12.19% | 16.44% | 47.26% | 14.39% | 88.2756 | 1545.29 |
| stressed/B2_10 | -11.52% | 14.99% | 45.90% | 13.45% | 60.8663 | 1229.59 |
| stressed/VOL_05 | -9.49% | 17.14% | 36.46% | 12.02% | 11.5183 | 178.068 |
| stressed/VOL_10 | -9.08% | 17.24% | 37.93% | 11.93% | 7.70273 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.41% | 0.0369942 |
| calibrated | 67.97% | 0.0376735 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2757 | 1574 | 1183 | 48.35% |
| 60m | perp_synchronized_clock | 2757 | 1574 | 1183 | 48.35% |
| 60m | combined_synchronized_clock | 2757 | 1547 | 1210 | 48.55% |
| 15m | perp_original_clock | 2757 | 1574 | 1183 | 48.92% |
| 15m | perp_synchronized_clock | 2757 | 1574 | 1183 | 48.92% |
| 15m | combined_synchronized_clock | 2757 | 1547 | 1210 | 48.03% |

## Data usability pilots

- Options: 714 captures; usable 7d RR25 in 611, usable 30d RR25 in 370; 558 valid hourly changes.
- Liquidations: 2022 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2751}`.
- Exchange stress: 1430/1430 scheduled records. Capture states: `{"missed": 45, "ok": 1385}`. Ratings: `{"low": 1385}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
