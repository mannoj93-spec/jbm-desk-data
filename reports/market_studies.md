# Market studies

Generated 2026-11-16T15:47:49.205Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 137 | 101 | 101 |
| range | collecting (descriptive) | 137 | 95 | 89 |
| state | collecting (descriptive) | 550 | 339 | 338 |
| paired | collecting (descriptive) | 2200 | 2102 | 2098 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0367064 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00371077 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000983037 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000119161 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.23% | 15.00% | 54.03% | 10.56% | 102.161 | 873.64 |
| ordinary/B2_10 | -10.30% | 14.92% | 53.41% | 10.65% | 77.9618 | 815.177 |
| ordinary/VOL_05 | -8.43% | 17.02% | 40.03% | 9.09% | 14.7996 | 98.0562 |
| ordinary/VOL_10 | -7.88% | 15.71% | 40.62% | 8.49% | 9.89728 | 65.5761 |
| stressed/B2_05 | -10.74% | 14.99% | 54.04% | 11.01% | 102.217 | 1417.53 |
| stressed/B2_10 | -10.69% | 14.87% | 53.42% | 10.98% | 78.0073 | 1229.59 |
| stressed/VOL_05 | -8.51% | 17.00% | 40.03% | 9.12% | 14.807 | 178.068 |
| stressed/VOL_10 | -7.93% | 15.70% | 40.63% | 8.50% | 9.90986 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 61.80% | 0.0323445 |
| calibrated | 60.67% | 0.0292997 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2098 | 1250 | 848 | 48.32% |
| 60m | perp_synchronized_clock | 2098 | 1250 | 848 | 48.32% |
| 60m | combined_synchronized_clock | 2098 | 1238 | 860 | 48.22% |
| 15m | perp_original_clock | 2098 | 1250 | 848 | 47.92% |
| 15m | perp_synchronized_clock | 2098 | 1250 | 848 | 47.92% |
| 15m | combined_synchronized_clock | 2098 | 1238 | 860 | 47.09% |

## Data usability pilots

- Options: 550 captures; usable 7d RR25 in 470, usable 30d RR25 in 220; 431 valid hourly changes.
- Liquidations: 1530 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2095}`.
- Exchange stress: 1100/1100 scheduled records. Capture states: `{"missed": 45, "ok": 1055}`. Ratings: `{"low": 1055}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
