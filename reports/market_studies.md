# Market studies

Generated 2026-11-06T16:47:53.036Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 78 | 42 | 42 |
| range | collecting (descriptive) | 78 | 36 | 35 |
| state | collecting (descriptive) | 311 | 218 | 215 |
| paired | collecting (descriptive) | 1244 | 1150 | 1145 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0235272 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -8.73406e-05 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00131004 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.76% | 14.48% | 64.95% | 4.07% | 77.8301 | 341.778 |
| ordinary/B2_10 | -4.18% | 15.81% | 64.78% | 4.52% | 57.5254 | 301.736 |
| ordinary/VOL_05 | -3.08% | 20.20% | 45.44% | 3.74% | 17.8993 | 68.8516 |
| ordinary/VOL_10 | -2.93% | 18.57% | 46.99% | 3.54% | 13.6055 | 52.2225 |
| stressed/B2_05 | -3.99% | 14.44% | 64.96% | 4.26% | 77.874 | 585.407 |
| stressed/B2_10 | -4.35% | 15.73% | 64.80% | 4.64% | 57.5571 | 481.77 |
| stressed/VOL_05 | -3.13% | 20.16% | 45.45% | 3.75% | 17.9119 | 125.006 |
| stressed/VOL_10 | -2.97% | 18.55% | 47.01% | 3.54% | 13.6235 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1145 | 690 | 455 | 50.14% |
| 60m | perp_synchronized_clock | 1145 | 690 | 455 | 50.14% |
| 60m | combined_synchronized_clock | 1145 | 674 | 471 | 50.30% |
| 15m | perp_original_clock | 1145 | 690 | 455 | 47.25% |
| 15m | perp_synchronized_clock | 1145 | 690 | 455 | 47.25% |
| 15m | combined_synchronized_clock | 1145 | 674 | 471 | 46.88% |

## Data usability pilots

- Options: 311 captures; usable 7d RR25 in 256, usable 30d RR25 in 86; 232 valid hourly changes.
- Liquidations: 821 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1147}`.
- Exchange stress: 622/622 scheduled records. Capture states: `{"missed": 43, "ok": 579}`. Ratings: `{"low": 579}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
