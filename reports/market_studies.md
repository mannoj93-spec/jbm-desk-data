# Market studies

Generated 2026-11-17T17:47:46.733Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 144 | 108 | 108 |
| range | collecting (descriptive) | 144 | 101 | 96 |
| state | collecting (descriptive) | 576 | 349 | 347 |
| paired | collecting (descriptive) | 2304 | 2206 | 2200 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0607717 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00395119 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00056202 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000511364 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.20% | 14.74% | 52.74% | 10.56% | 100.044 | 890.73 |
| ordinary/B2_10 | -10.26% | 14.59% | 51.88% | 10.65% | 74.4428 | 815.177 |
| ordinary/VOL_05 | -8.38% | 16.62% | 39.32% | 9.09% | 14.1223 | 98.0562 |
| ordinary/VOL_10 | -7.81% | 15.43% | 40.10% | 8.49% | 9.44173 | 65.5761 |
| stressed/B2_05 | -10.72% | 14.73% | 52.75% | 11.01% | 100.108 | 1448.42 |
| stressed/B2_10 | -10.65% | 14.54% | 51.89% | 10.98% | 74.4949 | 1229.59 |
| stressed/VOL_05 | -8.45% | 16.61% | 39.33% | 9.12% | 14.1295 | 178.068 |
| stressed/VOL_10 | -7.86% | 15.42% | 40.11% | 8.50% | 9.45376 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.58% | 0.0336147 |
| calibrated | 63.54% | 0.0313029 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2200 | 1304 | 896 | 48.08% |
| 60m | perp_synchronized_clock | 2200 | 1304 | 896 | 48.08% |
| 60m | combined_synchronized_clock | 2200 | 1286 | 914 | 48.06% |
| 15m | perp_original_clock | 2200 | 1304 | 896 | 47.93% |
| 15m | perp_synchronized_clock | 2200 | 1304 | 896 | 47.93% |
| 15m | combined_synchronized_clock | 2200 | 1286 | 914 | 46.97% |

## Data usability pilots

- Options: 576 captures; usable 7d RR25 in 495, usable 30d RR25 in 246; 453 valid hourly changes.
- Liquidations: 1608 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2199}`.
- Exchange stress: 1152/1152 scheduled records. Capture states: `{"missed": 45, "ok": 1107}`. Ratings: `{"low": 1107}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
