# Market studies

Generated 2026-11-07T02:10:03.523Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 80 | 44 | 44 |
| range | collecting (descriptive) | 80 | 38 | 35 |
| state | collecting (descriptive) | 321 | 226 | 222 |
| paired | collecting (descriptive) | 1281 | 1187 | 1182 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0170279 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000561996 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.0008989 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| 60m | perp_original_clock | 1182 | 715 | 467 | 49.23% |
| 60m | perp_synchronized_clock | 1182 | 715 | 467 | 49.23% |
| 60m | combined_synchronized_clock | 1182 | 702 | 480 | 49.29% |
| 15m | perp_original_clock | 1182 | 715 | 467 | 46.85% |
| 15m | perp_synchronized_clock | 1182 | 715 | 467 | 46.85% |
| 15m | combined_synchronized_clock | 1182 | 702 | 480 | 46.30% |

## Data usability pilots

- Options: 320 captures; usable 7d RR25 in 265, usable 30d RR25 in 86; 241 valid hourly changes.
- Liquidations: 851 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1187}`.
- Exchange stress: 641/641 scheduled records. Capture states: `{"missed": 43, "ok": 598}`. Ratings: `{"low": 598}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
