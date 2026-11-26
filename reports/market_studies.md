# Market studies

Generated 2026-11-26T01:32:46.913Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 194 | 157 | 157 |
| range | collecting (descriptive) | 194 | 149 | 144 |
| state | collecting (descriptive) | 776 | 391 | 391 |
| paired | collecting (descriptive) | 3103 | 3005 | 2999 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.320277 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00186485 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00122958 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.67% | 16.23% | 45.34% | 13.92% | 86.3928 | 985.599 |
| ordinary/B2_10 | -11.25% | 14.85% | 43.97% | 13.13% | 56.3947 | 815.177 |
| ordinary/VOL_05 | -9.54% | 16.96% | 35.51% | 11.99% | 10.6724 | 98.0562 |
| ordinary/VOL_10 | -9.18% | 17.28% | 37.20% | 11.91% | 7.13147 | 65.5761 |
| stressed/B2_05 | -12.26% | 16.24% | 45.34% | 14.39% | 86.4838 | 1619.74 |
| stressed/B2_10 | -11.63% | 14.83% | 43.97% | 13.45% | 56.4639 | 1229.59 |
| stressed/VOL_05 | -9.61% | 16.95% | 35.51% | 12.02% | 10.6786 | 178.068 |
| stressed/VOL_10 | -9.23% | 17.27% | 37.21% | 11.93% | 7.14069 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.36% | 0.0393223 |
| calibrated | 70.14% | 0.0422082 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2999 | 1689 | 1310 | 48.19% |
| 60m | perp_synchronized_clock | 2999 | 1689 | 1310 | 48.19% |
| 60m | combined_synchronized_clock | 2999 | 1658 | 1341 | 48.37% |
| 15m | perp_original_clock | 2999 | 1689 | 1310 | 48.61% |
| 15m | perp_synchronized_clock | 2999 | 1689 | 1310 | 48.61% |
| 15m | combined_synchronized_clock | 2999 | 1658 | 1341 | 47.59% |

## Data usability pilots

- Options: 775 captures; usable 7d RR25 in 666, usable 30d RR25 in 413; 608 valid hourly changes.
- Liquidations: 2205 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2995}`.
- Exchange stress: 1552/1552 scheduled records. Capture states: `{"missed": 45, "ok": 1507}`. Ratings: `{"low": 1507}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
