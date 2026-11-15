# Market studies

Generated 2026-11-15T14:17:15.550Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 131 | 95 | 95 |
| range | collecting (descriptive) | 131 | 89 | 83 |
| state | collecting (descriptive) | 525 | 330 | 327 |
| paired | collecting (descriptive) | 2098 | 2002 | 1997 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0342557 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00408631 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000137869 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000187782 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.80% | 15.38% | 55.50% | 10.56% | 106.448 | 873.64 |
| ordinary/B2_10 | -9.87% | 15.30% | 54.84% | 10.65% | 81.2409 | 815.177 |
| ordinary/VOL_05 | -7.92% | 17.45% | 40.69% | 9.09% | 15.4321 | 98.0562 |
| ordinary/VOL_10 | -7.28% | 16.03% | 41.10% | 8.49% | 10.3231 | 65.5761 |
| stressed/B2_05 | -10.31% | 15.37% | 55.50% | 11.01% | 106.491 | 1417.53 |
| stressed/B2_10 | -10.26% | 15.25% | 54.85% | 10.98% | 81.2793 | 1229.59 |
| stressed/VOL_05 | -8.00% | 17.43% | 40.69% | 9.12% | 15.4395 | 178.068 |
| stressed/VOL_10 | -7.33% | 16.02% | 41.11% | 8.50% | 10.3362 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 61.45% | 0.0314167 |
| calibrated | 60.24% | 0.028013 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1997 | 1189 | 808 | 48.53% |
| 60m | perp_synchronized_clock | 1997 | 1189 | 808 | 48.53% |
| 60m | combined_synchronized_clock | 1997 | 1175 | 822 | 48.43% |
| 15m | perp_original_clock | 1997 | 1189 | 808 | 47.35% |
| 15m | perp_synchronized_clock | 1997 | 1189 | 808 | 47.35% |
| 15m | combined_synchronized_clock | 1997 | 1175 | 822 | 46.72% |

## Data usability pilots

- Options: 525 captures; usable 7d RR25 in 445, usable 30d RR25 in 195; 410 valid hourly changes.
- Liquidations: 1455 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1995}`.
- Exchange stress: 1049/1049 scheduled records. Capture states: `{"missed": 44, "ok": 1005}`. Ratings: `{"low": 1005}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
