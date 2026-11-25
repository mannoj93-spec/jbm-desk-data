# Market studies

Generated 2026-11-25T06:18:54.483Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 189 | 152 | 152 |
| range | collecting (descriptive) | 189 | 145 | 139 |
| state | collecting (descriptive) | 757 | 390 | 389 |
| paired | collecting (descriptive) | 3026 | 2928 | 2923 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.382201 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00117351 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00153665 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00130431 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.16% | 16.21% | 45.93% | 13.92% | 87.8433 | 979.787 |
| ordinary/B2_10 | -11.74% | 14.83% | 44.58% | 13.13% | 57.7806 | 815.177 |
| ordinary/VOL_05 | -10.12% | 16.94% | 35.81% | 11.99% | 10.9363 | 98.0562 |
| ordinary/VOL_10 | -9.87% | 17.17% | 37.44% | 11.91% | 7.30772 | 65.5761 |
| stressed/B2_05 | -12.74% | 16.21% | 45.94% | 14.39% | 87.932 | 1609.25 |
| stressed/B2_10 | -12.13% | 14.80% | 44.59% | 13.45% | 57.8492 | 1229.59 |
| stressed/VOL_05 | -10.20% | 16.93% | 35.82% | 12.02% | 10.9425 | 178.068 |
| stressed/VOL_10 | -9.92% | 17.16% | 37.45% | 11.93% | 7.31715 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.19% | 0.0386627 |
| calibrated | 69.06% | 0.040894 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2923 | 1653 | 1270 | 48.46% |
| 60m | perp_synchronized_clock | 2923 | 1653 | 1270 | 48.46% |
| 60m | combined_synchronized_clock | 2923 | 1628 | 1295 | 48.71% |
| 15m | perp_original_clock | 2923 | 1653 | 1270 | 48.82% |
| 15m | perp_synchronized_clock | 2923 | 1653 | 1270 | 48.82% |
| 15m | combined_synchronized_clock | 2923 | 1628 | 1295 | 47.97% |

## Data usability pilots

- Options: 756 captures; usable 7d RR25 in 652, usable 30d RR25 in 412; 598 valid hourly changes.
- Liquidations: 2148 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2919}`.
- Exchange stress: 1513/1513 scheduled records. Capture states: `{"missed": 45, "ok": 1468}`. Ratings: `{"low": 1468}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
