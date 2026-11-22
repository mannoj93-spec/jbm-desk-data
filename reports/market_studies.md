# Market studies

Generated 2026-11-22T23:17:33.447Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 175 | 138 | 138 |
| range | collecting (descriptive) | 175 | 131 | 125 |
| state | collecting (descriptive) | 702 | 375 | 374 |
| paired | collecting (descriptive) | 2806 | 2708 | 2703 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.314455 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.000264578 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00194159 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00120237 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.87% | 16.62% | 47.82% | 13.92% | 88.7421 | 933.517 |
| ordinary/B2_10 | -11.34% | 15.19% | 46.46% | 13.13% | 62.1043 | 815.177 |
| ordinary/VOL_05 | -9.65% | 17.35% | 36.73% | 11.99% | 11.761 | 98.0562 |
| ordinary/VOL_10 | -9.31% | 17.43% | 38.13% | 11.91% | 7.85958 | 65.5761 |
| stressed/B2_05 | -12.42% | 16.62% | 47.82% | 14.39% | 88.8298 | 1525.65 |
| stressed/B2_10 | -11.72% | 15.16% | 46.47% | 13.45% | 62.1705 | 1229.59 |
| stressed/VOL_05 | -9.72% | 17.34% | 36.73% | 12.02% | 11.7676 | 178.068 |
| stressed/VOL_10 | -9.36% | 17.43% | 38.14% | 11.93% | 7.8697 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.60% | 0.0366254 |
| calibrated | 67.20% | 0.0368801 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2703 | 1557 | 1146 | 48.36% |
| 60m | perp_synchronized_clock | 2703 | 1557 | 1146 | 48.36% |
| 60m | combined_synchronized_clock | 2703 | 1529 | 1174 | 48.53% |
| 15m | perp_original_clock | 2703 | 1557 | 1146 | 48.81% |
| 15m | perp_synchronized_clock | 2703 | 1557 | 1146 | 48.81% |
| 15m | combined_synchronized_clock | 2703 | 1529 | 1174 | 47.94% |

## Data usability pilots

- Options: 701 captures; usable 7d RR25 in 598, usable 30d RR25 in 357; 545 valid hourly changes.
- Liquidations: 1983 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2699}`.
- Exchange stress: 1403/1403 scheduled records. Capture states: `{"missed": 45, "ok": 1358}`. Ratings: `{"low": 1358}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
