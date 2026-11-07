# Market studies

Generated 2026-11-07T15:20:04.544Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 83 | 47 | 47 |
| range | collecting (descriptive) | 83 | 41 | 35 |
| state | collecting (descriptive) | 334 | 239 | 234 |
| paired | collecting (descriptive) | 1334 | 1240 | 1235 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.139891 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00100207 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.001417 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.59% | 13.85% | 64.42% | 4.07% | 98.4568 | 444.383 |
| ordinary/B2_10 | -4.06% | 15.08% | 64.12% | 4.52% | 80.3442 | 408.474 |
| ordinary/VOL_05 | -2.86% | 19.13% | 44.72% | 3.74% | 19.1856 | 78.3691 |
| ordinary/VOL_10 | -2.72% | 17.59% | 46.17% | 3.54% | 16.0814 | 65.5761 |
| stressed/B2_05 | -3.91% | 13.79% | 64.43% | 4.28% | 98.4721 | 771.187 |
| stressed/B2_10 | -4.32% | 15.01% | 64.14% | 4.67% | 80.3485 | 675.012 |
| stressed/VOL_05 | -2.93% | 19.09% | 44.72% | 3.75% | 19.1965 | 142.3 |
| stressed/VOL_10 | -2.77% | 17.57% | 46.19% | 3.54% | 16.1007 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1235 | 752 | 483 | 48.94% |
| 60m | perp_synchronized_clock | 1235 | 752 | 483 | 48.94% |
| 60m | combined_synchronized_clock | 1235 | 740 | 495 | 49.19% |
| 15m | perp_original_clock | 1235 | 752 | 483 | 46.81% |
| 15m | perp_synchronized_clock | 1235 | 752 | 483 | 46.81% |
| 15m | combined_synchronized_clock | 1235 | 740 | 495 | 46.22% |

## Data usability pilots

- Options: 334 captures; usable 7d RR25 in 279, usable 30d RR25 in 86; 255 valid hourly changes.
- Liquidations: 890 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1239}`.
- Exchange stress: 667/667 scheduled records. Capture states: `{"missed": 43, "ok": 624}`. Ratings: `{"low": 624}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
