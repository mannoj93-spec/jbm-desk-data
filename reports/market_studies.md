# Market studies

Generated 2026-11-18T14:48:00.835Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 149 | 113 | 113 |
| range | collecting (descriptive) | 149 | 106 | 100 |
| state | collecting (descriptive) | 597 | 357 | 354 |
| paired | collecting (descriptive) | 2388 | 2290 | 2285 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0148508 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00414317 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000390926 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000820569 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.16% | 14.51% | 51.76% | 10.57% | 98.6406 | 902.969 |
| ordinary/B2_10 | -10.20% | 14.36% | 50.88% | 10.65% | 72.1218 | 815.177 |
| ordinary/VOL_05 | -8.30% | 16.36% | 38.86% | 9.09% | 13.6763 | 98.0562 |
| ordinary/VOL_10 | -7.73% | 15.24% | 39.76% | 8.49% | 9.14196 | 65.5761 |
| stressed/B2_05 | -10.70% | 14.51% | 51.77% | 11.04% | 98.7086 | 1470.45 |
| stressed/B2_10 | -10.58% | 14.33% | 50.89% | 10.98% | 72.1776 | 1229.59 |
| stressed/VOL_05 | -8.38% | 16.35% | 38.86% | 9.12% | 13.6834 | 178.068 |
| stressed/VOL_10 | -7.78% | 15.23% | 39.77% | 8.50% | 9.15364 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.00% | 0.0341518 |
| calibrated | 65.00% | 0.0322825 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2285 | 1354 | 931 | 48.23% |
| 60m | perp_synchronized_clock | 2285 | 1354 | 931 | 48.23% |
| 60m | combined_synchronized_clock | 2285 | 1332 | 953 | 48.27% |
| 15m | perp_original_clock | 2285 | 1354 | 931 | 47.86% |
| 15m | perp_synchronized_clock | 2285 | 1354 | 931 | 47.86% |
| 15m | combined_synchronized_clock | 2285 | 1332 | 953 | 46.77% |

## Data usability pilots

- Options: 597 captures; usable 7d RR25 in 511, usable 30d RR25 in 267; 466 valid hourly changes.
- Liquidations: 1671 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2283}`.
- Exchange stress: 1194/1194 scheduled records. Capture states: `{"missed": 45, "ok": 1149}`. Ratings: `{"low": 1149}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
