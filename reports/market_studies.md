# Market studies

Generated 2026-11-24T16:20:38.114Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 186 | 149 | 149 |
| range | collecting (descriptive) | 186 | 142 | 135 |
| state | collecting (descriptive) | 743 | 384 | 383 |
| paired | collecting (descriptive) | 2970 | 2872 | 2867 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.387707 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000551001 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00182296 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00126439 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.09% | 16.36% | 46.29% | 13.92% | 89.1591 | 979.787 |
| ordinary/B2_10 | -11.68% | 14.97% | 44.96% | 13.13% | 58.6519 | 815.177 |
| ordinary/VOL_05 | -10.05% | 17.10% | 36.00% | 11.99% | 11.1023 | 98.0562 |
| ordinary/VOL_10 | -9.79% | 17.33% | 37.58% | 11.91% | 7.41865 | 65.5761 |
| stressed/B2_05 | -12.67% | 16.37% | 46.29% | 14.39% | 89.2448 | 1609.25 |
| stressed/B2_10 | -12.06% | 14.94% | 44.97% | 13.45% | 58.7202 | 1229.59 |
| stressed/VOL_05 | -10.12% | 17.09% | 36.01% | 12.02% | 11.1085 | 178.068 |
| stressed/VOL_10 | -9.84% | 17.33% | 37.59% | 11.93% | 7.42822 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.93% | 0.0379656 |
| calibrated | 68.89% | 0.0396394 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2867 | 1628 | 1239 | 48.34% |
| 60m | perp_synchronized_clock | 2867 | 1628 | 1239 | 48.34% |
| 60m | combined_synchronized_clock | 2867 | 1602 | 1265 | 48.56% |
| 15m | perp_original_clock | 2867 | 1628 | 1239 | 48.83% |
| 15m | perp_synchronized_clock | 2867 | 1628 | 1239 | 48.83% |
| 15m | combined_synchronized_clock | 2867 | 1602 | 1265 | 48.00% |

## Data usability pilots

- Options: 742 captures; usable 7d RR25 in 638, usable 30d RR25 in 398; 585 valid hourly changes.
- Liquidations: 2106 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2863}`.
- Exchange stress: 1485/1485 scheduled records. Capture states: `{"missed": 45, "ok": 1440}`. Ratings: `{"low": 1440}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
