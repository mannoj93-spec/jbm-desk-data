# Market studies

Generated 2026-11-24T22:03:02.926Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 187 | 150 | 150 |
| range | collecting (descriptive) | 187 | 143 | 137 |
| state | collecting (descriptive) | 749 | 388 | 385 |
| paired | collecting (descriptive) | 2993 | 2895 | 2890 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.38904 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000849213 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00199935 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00125433 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.03% | 16.32% | 46.17% | 13.92% | 88.7129 | 979.787 |
| ordinary/B2_10 | -11.63% | 14.93% | 44.83% | 13.13% | 58.3564 | 815.177 |
| ordinary/VOL_05 | -10.00% | 17.05% | 35.94% | 11.99% | 11.046 | 98.0562 |
| ordinary/VOL_10 | -9.72% | 17.28% | 37.53% | 11.91% | 7.38103 | 65.5761 |
| stressed/B2_05 | -12.62% | 16.32% | 46.17% | 14.39% | 88.7996 | 1609.25 |
| stressed/B2_10 | -12.02% | 14.90% | 44.84% | 13.45% | 58.4248 | 1229.59 |
| stressed/VOL_05 | -10.07% | 17.04% | 35.94% | 12.02% | 11.0522 | 178.068 |
| stressed/VOL_10 | -9.77% | 17.27% | 37.54% | 11.93% | 7.39055 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.42% | 0.0383404 |
| calibrated | 69.34% | 0.0402961 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2890 | 1639 | 1251 | 48.38% |
| 60m | perp_synchronized_clock | 2890 | 1639 | 1251 | 48.38% |
| 60m | combined_synchronized_clock | 2890 | 1613 | 1277 | 48.61% |
| 15m | perp_original_clock | 2890 | 1639 | 1251 | 48.81% |
| 15m | perp_synchronized_clock | 2890 | 1639 | 1251 | 48.81% |
| 15m | combined_synchronized_clock | 2890 | 1613 | 1277 | 47.99% |

## Data usability pilots

- Options: 747 captures; usable 7d RR25 in 643, usable 30d RR25 in 403; 589 valid hourly changes.
- Liquidations: 2124 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2887}`.
- Exchange stress: 1497/1497 scheduled records. Capture states: `{"missed": 45, "ok": 1452}`. Ratings: `{"low": 1452}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
