# Market studies

Generated 2026-11-15T16:22:14.713Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 132 | 96 | 96 |
| range | collecting (descriptive) | 132 | 90 | 83 |
| state | collecting (descriptive) | 527 | 332 | 328 |
| paired | collecting (descriptive) | 2106 | 2010 | 2005 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0362721 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00408631 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000245104 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000187032 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.07% | 15.34% | 55.24% | 10.56% | 105.712 | 873.64 |
| ordinary/B2_10 | -10.14% | 15.25% | 54.59% | 10.65% | 80.6779 | 815.177 |
| ordinary/VOL_05 | -8.24% | 17.41% | 40.57% | 9.09% | 15.3233 | 98.0562 |
| ordinary/VOL_10 | -7.65% | 16.03% | 41.02% | 8.49% | 10.2498 | 65.5761 |
| stressed/B2_05 | -10.58% | 15.33% | 55.25% | 11.01% | 105.757 | 1417.53 |
| stressed/B2_10 | -10.53% | 15.20% | 54.61% | 10.98% | 80.7175 | 1229.59 |
| stressed/VOL_05 | -8.31% | 17.39% | 40.58% | 9.12% | 15.3308 | 178.068 |
| stressed/VOL_10 | -7.70% | 16.02% | 41.03% | 8.50% | 10.2628 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 61.45% | 0.0314167 |
| calibrated | 60.24% | 0.028013 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2005 | 1195 | 810 | 48.62% |
| 60m | perp_synchronized_clock | 2005 | 1195 | 810 | 48.62% |
| 60m | combined_synchronized_clock | 2005 | 1181 | 824 | 48.52% |
| 15m | perp_original_clock | 2005 | 1195 | 810 | 47.28% |
| 15m | perp_synchronized_clock | 2005 | 1195 | 810 | 47.28% |
| 15m | combined_synchronized_clock | 2005 | 1181 | 824 | 46.66% |

## Data usability pilots

- Options: 527 captures; usable 7d RR25 in 447, usable 30d RR25 in 197; 412 valid hourly changes.
- Liquidations: 1461 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2003}`.
- Exchange stress: 1053/1053 scheduled records. Capture states: `{"missed": 44, "ok": 1009}`. Ratings: `{"low": 1009}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
