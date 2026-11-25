# Market studies

Generated 2026-11-25T01:47:45.167Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 188 | 151 | 151 |
| range | collecting (descriptive) | 188 | 144 | 138 |
| state | collecting (descriptive) | 752 | 389 | 388 |
| paired | collecting (descriptive) | 3008 | 2910 | 2904 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.385225 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000996033 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00163037 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00135589 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.11% | 16.26% | 46.05% | 13.92% | 88.2775 | 979.787 |
| ordinary/B2_10 | -11.70% | 14.88% | 44.71% | 13.13% | 58.0681 | 815.177 |
| ordinary/VOL_05 | -10.07% | 17.00% | 35.88% | 11.99% | 10.991 | 98.0562 |
| ordinary/VOL_10 | -9.81% | 17.22% | 37.48% | 11.91% | 7.34431 | 65.5761 |
| stressed/B2_05 | -12.69% | 16.27% | 46.05% | 14.39% | 88.3652 | 1609.25 |
| stressed/B2_10 | -12.08% | 14.85% | 44.72% | 13.45% | 58.1366 | 1229.59 |
| stressed/VOL_05 | -10.14% | 16.99% | 35.88% | 12.02% | 10.9973 | 178.068 |
| stressed/VOL_10 | -9.86% | 17.22% | 37.49% | 11.93% | 7.35379 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.0384631 |
| calibrated | 69.57% | 0.0405576 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2904 | 1646 | 1258 | 48.42% |
| 60m | perp_synchronized_clock | 2904 | 1646 | 1258 | 48.42% |
| 60m | combined_synchronized_clock | 2904 | 1619 | 1285 | 48.67% |
| 15m | perp_original_clock | 2904 | 1646 | 1258 | 48.78% |
| 15m | perp_synchronized_clock | 2904 | 1646 | 1258 | 48.78% |
| 15m | combined_synchronized_clock | 2904 | 1619 | 1285 | 47.99% |

## Data usability pilots

- Options: 751 captures; usable 7d RR25 in 647, usable 30d RR25 in 407; 593 valid hourly changes.
- Liquidations: 2133 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2899}`.
- Exchange stress: 1504/1504 scheduled records. Capture states: `{"missed": 45, "ok": 1459}`. Ratings: `{"low": 1459}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
