# Market studies

Generated 2026-11-28T10:17:58.607Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 208 | 171 | 171 |
| range | collecting (descriptive) | 208 | 163 | 157 |
| state | collecting (descriptive) | 833 | 404 | 404 |
| paired | collecting (descriptive) | 3330 | 3232 | 3227 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.361532 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00348996 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00086607 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00182058 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.18% | 15.85% | 44.09% | 13.92% | 85.5937 | 1031.31 |
| ordinary/B2_10 | -11.78% | 14.48% | 42.64% | 13.13% | 55.0177 | 836.707 |
| ordinary/VOL_05 | -10.02% | 16.50% | 34.76% | 11.99% | 9.98596 | 98.0562 |
| ordinary/VOL_10 | -9.75% | 16.89% | 36.63% | 11.91% | 6.67228 | 65.5761 |
| stressed/B2_05 | -12.80% | 15.85% | 44.09% | 14.39% | 85.6861 | 1701.99 |
| stressed/B2_10 | -12.18% | 14.45% | 42.65% | 13.45% | 55.0867 | 1268.57 |
| stressed/VOL_05 | -10.10% | 16.49% | 34.77% | 12.02% | 9.99181 | 178.068 |
| stressed/VOL_10 | -9.80% | 16.89% | 36.64% | 11.93% | 6.68093 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.43% | 0.0405372 |
| calibrated | 71.97% | 0.0449262 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3227 | 1815 | 1412 | 48.43% |
| 60m | perp_synchronized_clock | 3227 | 1815 | 1412 | 48.43% |
| 60m | combined_synchronized_clock | 3227 | 1777 | 1450 | 48.79% |
| 15m | perp_original_clock | 3227 | 1815 | 1412 | 48.76% |
| 15m | perp_synchronized_clock | 3227 | 1815 | 1412 | 48.76% |
| 15m | combined_synchronized_clock | 3227 | 1777 | 1450 | 47.78% |

## Data usability pilots

- Options: 832 captures; usable 7d RR25 in 721, usable 30d RR25 in 413; 656 valid hourly changes.
- Liquidations: 2376 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3223}`.
- Exchange stress: 1665/1665 scheduled records. Capture states: `{"missed": 45, "ok": 1620}`. Ratings: `{"low": 1620}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
