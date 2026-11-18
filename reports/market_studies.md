# Market studies

Generated 2026-11-18T17:27:31.814Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 150 | 114 | 114 |
| range | collecting (descriptive) | 150 | 107 | 101 |
| state | collecting (descriptive) | 600 | 358 | 356 |
| paired | collecting (descriptive) | 2398 | 2300 | 2295 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0287034 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00418879 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000308221 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000680828 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.93% | 14.85% | 51.60% | 11.22% | 98.028 | 902.969 |
| ordinary/B2_10 | -10.80% | 14.54% | 50.69% | 11.12% | 71.6727 | 815.177 |
| ordinary/VOL_05 | -9.01% | 16.59% | 38.77% | 9.64% | 13.5901 | 98.0562 |
| ordinary/VOL_10 | -8.56% | 15.64% | 39.69% | 9.14% | 9.08404 | 65.5761 |
| stressed/B2_05 | -11.46% | 14.84% | 51.61% | 11.70% | 98.0976 | 1470.45 |
| stressed/B2_10 | -11.19% | 14.50% | 50.70% | 11.45% | 71.7292 | 1229.59 |
| stressed/VOL_05 | -9.09% | 16.58% | 38.78% | 9.67% | 13.5972 | 178.068 |
| stressed/VOL_10 | -8.62% | 15.63% | 39.70% | 9.15% | 9.09564 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.34% | 0.034341 |
| calibrated | 65.35% | 0.0325769 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2295 | 1356 | 939 | 48.30% |
| 60m | perp_synchronized_clock | 2295 | 1356 | 939 | 48.30% |
| 60m | combined_synchronized_clock | 2295 | 1335 | 960 | 48.31% |
| 15m | perp_original_clock | 2295 | 1356 | 939 | 47.94% |
| 15m | perp_synchronized_clock | 2295 | 1356 | 939 | 47.94% |
| 15m | combined_synchronized_clock | 2295 | 1335 | 960 | 46.82% |

## Data usability pilots

- Options: 600 captures; usable 7d RR25 in 513, usable 30d RR25 in 270; 467 valid hourly changes.
- Liquidations: 1680 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2295}`.
- Exchange stress: 1199/1199 scheduled records. Capture states: `{"missed": 45, "ok": 1154}`. Ratings: `{"low": 1154}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
