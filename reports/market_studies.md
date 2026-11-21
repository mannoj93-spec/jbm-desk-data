# Market studies

Generated 2026-11-21T21:39:12.466Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 169 | 132 | 132 |
| range | collecting (descriptive) | 169 | 125 | 119 |
| state | collecting (descriptive) | 676 | 370 | 370 |
| paired | collecting (descriptive) | 2703 | 2605 | 2600 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.243344 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000771599 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00154758 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000649038 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.04% | 16.51% | 48.70% | 13.92% | 91.0056 | 928.525 |
| ordinary/B2_10 | -11.44% | 15.14% | 47.36% | 13.13% | 64.1488 | 815.177 |
| ordinary/VOL_05 | -9.77% | 17.30% | 37.17% | 11.99% | 12.1513 | 98.0562 |
| ordinary/VOL_10 | -9.45% | 17.22% | 38.47% | 11.91% | 8.12065 | 65.5761 |
| stressed/B2_05 | -12.58% | 16.52% | 48.71% | 14.39% | 91.0892 | 1516.64 |
| stressed/B2_10 | -11.82% | 15.11% | 47.37% | 13.45% | 64.2132 | 1229.59 |
| stressed/VOL_05 | -9.84% | 17.29% | 37.17% | 12.02% | 12.158 | 178.068 |
| stressed/VOL_10 | -9.50% | 17.21% | 38.48% | 11.93% | 8.13108 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.55% | 0.0363527 |
| calibrated | 67.23% | 0.0361789 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2600 | 1499 | 1101 | 48.23% |
| 60m | perp_synchronized_clock | 2600 | 1499 | 1101 | 48.23% |
| 60m | combined_synchronized_clock | 2600 | 1476 | 1124 | 48.24% |
| 15m | perp_original_clock | 2600 | 1499 | 1101 | 48.83% |
| 15m | perp_synchronized_clock | 2600 | 1499 | 1101 | 48.83% |
| 15m | combined_synchronized_clock | 2600 | 1476 | 1124 | 47.90% |

## Data usability pilots

- Options: 675 captures; usable 7d RR25 in 572, usable 30d RR25 in 331; 519 valid hourly changes.
- Liquidations: 1905 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2595}`.
- Exchange stress: 1352/1352 scheduled records. Capture states: `{"missed": 45, "ok": 1307}`. Ratings: `{"low": 1307}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
