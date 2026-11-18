# Market studies

Generated 2026-11-18T21:48:12.434Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 151 | 115 | 115 |
| range | collecting (descriptive) | 151 | 108 | 102 |
| state | collecting (descriptive) | 604 | 360 | 358 |
| paired | collecting (descriptive) | 2416 | 2318 | 2312 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.00553983 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00423351 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000605105 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00075692 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.80% | 14.82% | 51.44% | 11.22% | 97.4308 | 902.969 |
| ordinary/B2_10 | -10.70% | 14.50% | 50.49% | 11.12% | 71.234 | 815.177 |
| ordinary/VOL_05 | -8.89% | 16.54% | 38.68% | 9.64% | 13.506 | 98.0562 |
| ordinary/VOL_10 | -8.42% | 15.60% | 39.62% | 9.14% | 9.02762 | 65.5761 |
| stressed/B2_05 | -11.33% | 14.81% | 51.45% | 11.70% | 97.5019 | 1470.45 |
| stressed/B2_10 | -11.08% | 14.47% | 50.50% | 11.45% | 71.2911 | 1229.59 |
| stressed/VOL_05 | -8.97% | 16.53% | 38.68% | 9.67% | 13.513 | 178.068 |
| stressed/VOL_10 | -8.47% | 15.59% | 39.64% | 9.15% | 9.03916 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.0344892 |
| calibrated | 65.69% | 0.0328281 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2312 | 1363 | 949 | 48.28% |
| 60m | perp_synchronized_clock | 2312 | 1363 | 949 | 48.28% |
| 60m | combined_synchronized_clock | 2312 | 1343 | 969 | 48.32% |
| 15m | perp_original_clock | 2312 | 1363 | 949 | 48.06% |
| 15m | perp_synchronized_clock | 2312 | 1363 | 949 | 48.06% |
| 15m | combined_synchronized_clock | 2312 | 1343 | 969 | 46.98% |

## Data usability pilots

- Options: 604 captures; usable 7d RR25 in 513, usable 30d RR25 in 274; 467 valid hourly changes.
- Liquidations: 1692 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2311}`.
- Exchange stress: 1208/1208 scheduled records. Capture states: `{"missed": 45, "ok": 1163}`. Ratings: `{"low": 1163}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
