# Market studies

Generated 2026-11-15T20:55:57.140Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 133 | 97 | 97 |
| range | collecting (descriptive) | 133 | 91 | 84 |
| state | collecting (descriptive) | 531 | 333 | 332 |
| paired | collecting (descriptive) | 2124 | 2028 | 2023 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0352336 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00392821 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000185683 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -3.08947e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.00% | 15.27% | 54.99% | 10.56% | 104.984 | 873.64 |
| ordinary/B2_10 | -10.07% | 15.19% | 54.35% | 10.65% | 80.1212 | 815.177 |
| ordinary/VOL_05 | -8.16% | 17.33% | 40.46% | 9.09% | 15.216 | 98.0562 |
| ordinary/VOL_10 | -7.55% | 15.97% | 40.93% | 8.49% | 10.1775 | 65.5761 |
| stressed/B2_05 | -10.51% | 15.26% | 55.00% | 11.01% | 105.032 | 1417.53 |
| stressed/B2_10 | -10.46% | 15.14% | 54.36% | 10.98% | 80.1621 | 1229.59 |
| stressed/VOL_05 | -8.23% | 17.31% | 40.47% | 9.12% | 15.2234 | 178.068 |
| stressed/VOL_10 | -7.60% | 15.96% | 40.95% | 8.50% | 10.1904 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 60.71% | 0.0314618 |
| calibrated | 59.52% | 0.0281107 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2023 | 1206 | 817 | 48.42% |
| 60m | perp_synchronized_clock | 2023 | 1206 | 817 | 48.42% |
| 60m | combined_synchronized_clock | 2023 | 1193 | 830 | 48.28% |
| 15m | perp_original_clock | 2023 | 1206 | 817 | 47.43% |
| 15m | perp_synchronized_clock | 2023 | 1206 | 817 | 47.43% |
| 15m | combined_synchronized_clock | 2023 | 1193 | 830 | 46.77% |

## Data usability pilots

- Options: 531 captures; usable 7d RR25 in 451, usable 30d RR25 in 201; 416 valid hourly changes.
- Liquidations: 1473 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2019}`.
- Exchange stress: 1062/1062 scheduled records. Capture states: `{"missed": 44, "ok": 1018}`. Ratings: `{"low": 1018}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
