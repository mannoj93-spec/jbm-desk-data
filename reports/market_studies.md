# Market studies

Generated 2026-11-10T22:32:02.396Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 103 | 67 | 67 |
| range | collecting (descriptive) | 103 | 61 | 55 |
| state | collecting (descriptive) | 413 | 288 | 288 |
| paired | collecting (descriptive) | 1651 | 1557 | 1552 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0715569 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00448051 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000668428 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000926224 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.29% | 13.19% | 61.80% | 5.62% | 112.025 | 733.902 |
| ordinary/B2_10 | -5.71% | 14.11% | 61.15% | 6.07% | 86.7934 | 656.413 |
| ordinary/VOL_05 | -3.88% | 16.61% | 42.48% | 4.58% | 15.5286 | 78.3691 |
| ordinary/VOL_10 | -3.73% | 15.39% | 43.65% | 4.38% | 13.0133 | 65.5761 |
| stressed/B2_05 | -5.73% | 13.17% | 61.81% | 6.01% | 112.035 | 1190.42 |
| stressed/B2_10 | -6.05% | 14.04% | 61.16% | 6.36% | 86.8103 | 1009.79 |
| stressed/VOL_05 | -3.94% | 16.57% | 42.49% | 4.60% | 15.5381 | 142.3 |
| stressed/VOL_10 | -3.79% | 15.37% | 43.67% | 4.39% | 13.0295 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.27% | 0.0293495 |
| calibrated | 65.45% | 0.0244143 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1552 | 957 | 595 | 48.90% |
| 60m | perp_synchronized_clock | 1552 | 957 | 595 | 48.90% |
| 60m | combined_synchronized_clock | 1552 | 946 | 606 | 49.05% |
| 15m | perp_original_clock | 1552 | 957 | 595 | 47.13% |
| 15m | perp_synchronized_clock | 1552 | 957 | 595 | 47.13% |
| 15m | combined_synchronized_clock | 1552 | 946 | 606 | 46.51% |

## Data usability pilots

- Options: 413 captures; usable 7d RR25 in 345, usable 30d RR25 in 100; 318 valid hourly changes.
- Liquidations: 1119 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1547}`.
- Exchange stress: 826/826 scheduled records. Capture states: `{"missed": 43, "ok": 783}`. Ratings: `{"low": 783}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
