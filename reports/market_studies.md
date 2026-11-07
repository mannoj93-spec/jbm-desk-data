# Market studies

Generated 2026-11-07T00:46:48.828Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 80 | 44 | 44 |
| range | collecting (descriptive) | 80 | 38 | 35 |
| state | collecting (descriptive) | 319 | 224 | 221 |
| paired | collecting (descriptive) | 1276 | 1182 | 1177 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0170279 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000325346 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000902719 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.65% | 14.17% | 64.22% | 4.07% | 93.2958 | 409.665 |
| ordinary/B2_10 | -4.07% | 15.47% | 63.96% | 4.52% | 71.2617 | 360.876 |
| ordinary/VOL_05 | -2.91% | 19.77% | 45.15% | 3.74% | 19.8987 | 78.3691 |
| ordinary/VOL_10 | -2.76% | 18.17% | 46.66% | 3.54% | 16.6799 | 65.5761 |
| stressed/B2_05 | -3.94% | 14.11% | 64.23% | 4.26% | 93.3114 | 708.479 |
| stressed/B2_10 | -4.30% | 15.38% | 63.97% | 4.64% | 71.274 | 589.091 |
| stressed/VOL_05 | -2.97% | 19.72% | 45.16% | 3.75% | 19.9097 | 142.3 |
| stressed/VOL_10 | -2.81% | 18.15% | 46.68% | 3.54% | 16.6998 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1177 | 710 | 467 | 49.30% |
| 60m | perp_synchronized_clock | 1177 | 710 | 467 | 49.30% |
| 60m | combined_synchronized_clock | 1177 | 697 | 480 | 49.35% |
| 15m | perp_original_clock | 1177 | 710 | 467 | 46.90% |
| 15m | perp_synchronized_clock | 1177 | 710 | 467 | 46.90% |
| 15m | combined_synchronized_clock | 1177 | 697 | 480 | 46.34% |

## Data usability pilots

- Options: 319 captures; usable 7d RR25 in 264, usable 30d RR25 in 86; 240 valid hourly changes.
- Liquidations: 845 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1179}`.
- Exchange stress: 638/638 scheduled records. Capture states: `{"missed": 43, "ok": 595}`. Ratings: `{"low": 595}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
