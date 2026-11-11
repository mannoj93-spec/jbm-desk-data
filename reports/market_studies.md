# Market studies

Generated 2026-11-11T18:32:07.451Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 108 | 72 | 72 |
| range | collecting (descriptive) | 108 | 66 | 60 |
| state | collecting (descriptive) | 433 | 300 | 298 |
| paired | collecting (descriptive) | 1731 | 1637 | 1632 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0214572 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00411027 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00140127 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000268076 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.00% | 12.83% | 60.48% | 5.64% | 108.044 | 739.372 |
| ordinary/B2_10 | -5.46% | 13.71% | 59.86% | 6.11% | 85.527 | 688.033 |
| ordinary/VOL_05 | -3.59% | 16.08% | 42.03% | 4.58% | 14.8232 | 78.3691 |
| ordinary/VOL_10 | -3.45% | 14.91% | 43.15% | 4.38% | 12.4218 | 65.5761 |
| stressed/B2_05 | -5.45% | 12.81% | 60.49% | 6.03% | 108.07 | 1200.26 |
| stressed/B2_10 | -5.81% | 13.65% | 59.87% | 6.41% | 85.5519 | 1052.22 |
| stressed/VOL_05 | -3.66% | 16.05% | 42.04% | 4.60% | 14.8324 | 142.3 |
| stressed/VOL_10 | -3.50% | 14.90% | 43.16% | 4.39% | 12.4373 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 70.00% | 0.0303136 |
| calibrated | 68.33% | 0.0257928 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1632 | 1005 | 627 | 48.96% |
| 60m | perp_synchronized_clock | 1632 | 1005 | 627 | 48.96% |
| 60m | combined_synchronized_clock | 1632 | 994 | 638 | 48.89% |
| 15m | perp_original_clock | 1632 | 1005 | 627 | 46.87% |
| 15m | perp_synchronized_clock | 1632 | 1005 | 627 | 46.87% |
| 15m | combined_synchronized_clock | 1632 | 994 | 638 | 46.18% |

## Data usability pilots

- Options: 433 captures; usable 7d RR25 in 363, usable 30d RR25 in 120; 336 valid hourly changes.
- Liquidations: 1179 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1627}`.
- Exchange stress: 866/866 scheduled records. Capture states: `{"missed": 43, "ok": 823}`. Ratings: `{"low": 823}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
