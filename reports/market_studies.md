# Market studies

Generated 2026-11-23T00:32:49.398Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 176 | 139 | 139 |
| range | collecting (descriptive) | 176 | 132 | 125 |
| state | collecting (descriptive) | 703 | 376 | 374 |
| paired | collecting (descriptive) | 2811 | 2713 | 2708 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.322891 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.000264578 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00194159 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00126939 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.65% | 16.60% | 47.69% | 13.92% | 88.964 | 939.242 |
| ordinary/B2_10 | -11.15% | 15.17% | 46.31% | 13.13% | 61.7721 | 815.177 |
| ordinary/VOL_05 | -9.43% | 17.33% | 36.65% | 11.99% | 11.6976 | 98.0562 |
| ordinary/VOL_10 | -9.05% | 17.42% | 38.08% | 11.91% | 7.81716 | 65.5761 |
| stressed/B2_05 | -12.21% | 16.61% | 47.69% | 14.39% | 89.0516 | 1536 |
| stressed/B2_10 | -11.54% | 15.15% | 46.32% | 13.45% | 61.8385 | 1229.59 |
| stressed/VOL_05 | -9.50% | 17.32% | 36.66% | 12.02% | 11.7041 | 178.068 |
| stressed/VOL_10 | -9.10% | 17.41% | 38.09% | 11.93% | 7.82722 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.60% | 0.0366254 |
| calibrated | 67.20% | 0.0368801 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2708 | 1559 | 1149 | 48.36% |
| 60m | perp_synchronized_clock | 2708 | 1559 | 1149 | 48.36% |
| 60m | combined_synchronized_clock | 2708 | 1532 | 1176 | 48.56% |
| 15m | perp_original_clock | 2708 | 1559 | 1149 | 48.88% |
| 15m | perp_synchronized_clock | 2708 | 1559 | 1149 | 48.88% |
| 15m | combined_synchronized_clock | 2708 | 1532 | 1176 | 47.98% |

## Data usability pilots

- Options: 702 captures; usable 7d RR25 in 599, usable 30d RR25 in 358; 546 valid hourly changes.
- Liquidations: 1986 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2703}`.
- Exchange stress: 1406/1406 scheduled records. Capture states: `{"missed": 45, "ok": 1361}`. Ratings: `{"low": 1361}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
