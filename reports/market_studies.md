# Market studies

Generated 2026-11-16T03:32:13.772Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 134 | 98 | 98 |
| range | collecting (descriptive) | 134 | 92 | 86 |
| state | collecting (descriptive) | 538 | 335 | 334 |
| paired | collecting (descriptive) | 2151 | 2055 | 2050 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0339862 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00375752 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000262438 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00027439 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.91% | 15.22% | 54.75% | 10.56% | 104.265 | 873.64 |
| ordinary/B2_10 | -9.98% | 15.14% | 54.11% | 10.65% | 79.5717 | 815.177 |
| ordinary/VOL_05 | -8.05% | 17.26% | 40.35% | 9.09% | 15.11 | 98.0562 |
| ordinary/VOL_10 | -7.43% | 15.91% | 40.85% | 8.49% | 10.1062 | 65.5761 |
| stressed/B2_05 | -10.42% | 15.21% | 54.76% | 11.01% | 104.316 | 1417.53 |
| stressed/B2_10 | -10.37% | 15.09% | 54.12% | 10.98% | 79.6138 | 1229.59 |
| stressed/VOL_05 | -8.13% | 17.24% | 40.36% | 9.12% | 15.1174 | 178.068 |
| stressed/VOL_10 | -7.48% | 15.90% | 40.87% | 8.50% | 10.119 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 60.47% | 0.0316973 |
| calibrated | 59.30% | 0.0284635 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2050 | 1221 | 829 | 48.16% |
| 60m | perp_synchronized_clock | 2050 | 1221 | 829 | 48.16% |
| 60m | combined_synchronized_clock | 2050 | 1208 | 842 | 48.10% |
| 15m | perp_original_clock | 2050 | 1221 | 829 | 47.34% |
| 15m | perp_synchronized_clock | 2050 | 1221 | 829 | 47.34% |
| 15m | combined_synchronized_clock | 2050 | 1208 | 842 | 46.61% |

## Data usability pilots

- Options: 538 captures; usable 7d RR25 in 458, usable 30d RR25 in 208; 422 valid hourly changes.
- Liquidations: 1494 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2047}`.
- Exchange stress: 1076/1076 scheduled records. Capture states: `{"missed": 44, "ok": 1032}`. Ratings: `{"low": 1032}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
