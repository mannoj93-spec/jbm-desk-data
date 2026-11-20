# Market studies

Generated 2026-11-20T03:33:27.908Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 158 | 122 | 122 |
| range | collecting (descriptive) | 158 | 115 | 109 |
| state | collecting (descriptive) | 634 | 364 | 364 |
| paired | collecting (descriptive) | 2535 | 2437 | 2432 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0177473 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0045236 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00071554 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00077097 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.01% | 14.60% | 50.38% | 11.31% | 93.4236 | 902.969 |
| ordinary/B2_10 | -10.87% | 14.22% | 49.22% | 11.18% | 68.2931 | 815.177 |
| ordinary/VOL_05 | -9.09% | 16.21% | 38.08% | 9.72% | 12.9423 | 98.0562 |
| ordinary/VOL_10 | -8.65% | 15.37% | 39.17% | 9.23% | 8.64948 | 65.5761 |
| stressed/B2_05 | -11.54% | 14.59% | 50.39% | 11.78% | 93.504 | 1470.45 |
| stressed/B2_10 | -11.25% | 14.18% | 49.23% | 11.52% | 68.3541 | 1229.59 |
| stressed/VOL_05 | -9.17% | 16.20% | 38.08% | 9.75% | 12.9492 | 178.068 |
| stressed/VOL_10 | -8.71% | 15.36% | 39.19% | 9.24% | 8.66056 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.81% | 0.0355194 |
| calibrated | 67.89% | 0.0345269 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2432 | 1425 | 1007 | 48.07% |
| 60m | perp_synchronized_clock | 2432 | 1425 | 1007 | 48.07% |
| 60m | combined_synchronized_clock | 2432 | 1403 | 1029 | 48.11% |
| 15m | perp_original_clock | 2432 | 1425 | 1007 | 48.14% |
| 15m | perp_synchronized_clock | 2432 | 1425 | 1007 | 48.14% |
| 15m | combined_synchronized_clock | 2432 | 1403 | 1029 | 47.11% |

## Data usability pilots

- Options: 634 captures; usable 7d RR25 in 533, usable 30d RR25 in 294; 484 valid hourly changes.
- Liquidations: 1782 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2431}`.
- Exchange stress: 1268/1268 scheduled records. Capture states: `{"missed": 45, "ok": 1223}`. Ratings: `{"low": 1223}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
