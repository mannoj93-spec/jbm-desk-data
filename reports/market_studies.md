# Market studies

Generated 2026-11-13T05:47:08.101Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 117 | 81 | 81 |
| range | collecting (descriptive) | 117 | 75 | 69 |
| state | collecting (descriptive) | 468 | 312 | 310 |
| paired | collecting (descriptive) | 1872 | 1777 | 1771 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.147102 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00367776 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -6.05735e-05 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000317617 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -7.58% | 14.03% | 58.58% | 7.88% | 104.19 | 762.826 |
| ordinary/B2_10 | -7.74% | 14.36% | 57.81% | 8.07% | 79.2169 | 688.033 |
| ordinary/VOL_05 | -6.17% | 16.89% | 41.50% | 6.82% | 15.0766 | 86.1552 |
| ordinary/VOL_10 | -5.73% | 15.39% | 42.34% | 6.32% | 11.489 | 65.5761 |
| stressed/B2_05 | -8.03% | 14.00% | 58.59% | 8.29% | 104.231 | 1242.68 |
| stressed/B2_10 | -8.09% | 14.30% | 57.82% | 8.37% | 79.2565 | 1052.22 |
| stressed/VOL_05 | -6.24% | 16.87% | 41.51% | 6.84% | 15.086 | 156.448 |
| stressed/VOL_10 | -5.78% | 15.37% | 42.35% | 6.34% | 11.5034 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 72.46% | 0.0312477 |
| calibrated | 71.01% | 0.0272271 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1771 | 1074 | 697 | 48.42% |
| 60m | perp_synchronized_clock | 1771 | 1074 | 697 | 48.42% |
| 60m | combined_synchronized_clock | 1771 | 1063 | 708 | 48.17% |
| 15m | perp_original_clock | 1771 | 1074 | 697 | 47.67% |
| 15m | perp_synchronized_clock | 1771 | 1074 | 697 | 47.67% |
| 15m | combined_synchronized_clock | 1771 | 1063 | 708 | 46.94% |

## Data usability pilots

- Options: 468 captures; usable 7d RR25 in 389, usable 30d RR25 in 144; 359 valid hourly changes.
- Liquidations: 1284 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1767}`.
- Exchange stress: 936/936 scheduled records. Capture states: `{"missed": 44, "ok": 892}`. Ratings: `{"low": 892}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
