# Market studies

Generated 2026-11-21T20:02:36.150Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 169 | 131 | 131 |
| range | collecting (descriptive) | 169 | 124 | 119 |
| state | collecting (descriptive) | 675 | 370 | 370 |
| paired | collecting (descriptive) | 2697 | 2599 | 2594 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.233693 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000771599 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00154758 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00065054 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.20% | 16.54% | 48.85% | 13.92% | 91.5053 | 928.525 |
| ordinary/B2_10 | -11.57% | 15.17% | 47.52% | 13.13% | 64.505 | 815.177 |
| ordinary/VOL_05 | -9.92% | 17.34% | 37.24% | 11.99% | 12.2193 | 98.0562 |
| ordinary/VOL_10 | -9.64% | 17.25% | 38.53% | 11.91% | 8.16613 | 65.5761 |
| stressed/B2_05 | -12.74% | 16.55% | 48.85% | 14.39% | 91.5879 | 1516.64 |
| stressed/B2_10 | -11.96% | 15.14% | 47.53% | 13.45% | 64.5692 | 1229.59 |
| stressed/VOL_05 | -10.00% | 17.33% | 37.25% | 12.02% | 12.226 | 178.068 |
| stressed/VOL_10 | -9.69% | 17.24% | 38.54% | 11.93% | 8.17662 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.55% | 0.0363527 |
| calibrated | 67.23% | 0.0361789 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2594 | 1498 | 1096 | 48.20% |
| 60m | perp_synchronized_clock | 2594 | 1498 | 1096 | 48.20% |
| 60m | combined_synchronized_clock | 2594 | 1475 | 1119 | 48.20% |
| 15m | perp_original_clock | 2594 | 1498 | 1096 | 48.80% |
| 15m | perp_synchronized_clock | 2594 | 1498 | 1096 | 48.80% |
| 15m | combined_synchronized_clock | 2594 | 1475 | 1119 | 47.86% |

## Data usability pilots

- Options: 673 captures; usable 7d RR25 in 570, usable 30d RR25 in 329; 517 valid hourly changes.
- Liquidations: 1902 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2591}`.
- Exchange stress: 1349/1349 scheduled records. Capture states: `{"missed": 45, "ok": 1304}`. Ratings: `{"low": 1304}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
