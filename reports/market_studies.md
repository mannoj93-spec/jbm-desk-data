# Market studies

Generated 2026-11-13T07:48:20.401Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 117 | 81 | 81 |
| range | collecting (descriptive) | 117 | 75 | 69 |
| state | collecting (descriptive) | 470 | 312 | 311 |
| paired | collecting (descriptive) | 1880 | 1785 | 1780 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.147102 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00367776 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000112411 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000316011 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| 60m | perp_original_clock | 1780 | 1080 | 700 | 48.43% |
| 60m | perp_synchronized_clock | 1780 | 1080 | 700 | 48.43% |
| 60m | combined_synchronized_clock | 1780 | 1069 | 711 | 48.18% |
| 15m | perp_original_clock | 1780 | 1080 | 700 | 47.50% |
| 15m | perp_synchronized_clock | 1780 | 1080 | 700 | 47.50% |
| 15m | combined_synchronized_clock | 1780 | 1069 | 711 | 46.77% |

## Data usability pilots

- Options: 470 captures; usable 7d RR25 in 390, usable 30d RR25 in 144; 360 valid hourly changes.
- Liquidations: 1290 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1775}`.
- Exchange stress: 940/940 scheduled records. Capture states: `{"missed": 44, "ok": 896}`. Ratings: `{"low": 896}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
