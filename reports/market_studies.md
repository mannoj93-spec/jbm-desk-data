# Market studies

Generated 2026-11-19T04:19:44.218Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 153 | 117 | 117 |
| range | collecting (descriptive) | 153 | 110 | 103 |
| state | collecting (descriptive) | 611 | 361 | 360 |
| paired | collecting (descriptive) | 2442 | 2344 | 2339 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0686108 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00427737 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000620748 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000587858 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.58% | 14.77% | 51.13% | 11.22% | 96.2574 | 902.969 |
| ordinary/B2_10 | -10.53% | 14.44% | 50.12% | 11.12% | 70.3722 | 815.177 |
| ordinary/VOL_05 | -8.69% | 16.46% | 38.50% | 9.64% | 13.3408 | 98.0562 |
| ordinary/VOL_10 | -8.18% | 15.54% | 39.49% | 9.14% | 8.91682 | 65.5761 |
| stressed/B2_05 | -11.11% | 14.77% | 51.13% | 11.70% | 96.3314 | 1470.45 |
| stressed/B2_10 | -10.91% | 14.40% | 50.13% | 11.45% | 70.4305 | 1229.59 |
| stressed/VOL_05 | -8.77% | 16.44% | 38.50% | 9.67% | 13.3478 | 178.068 |
| stressed/VOL_10 | -8.23% | 15.53% | 39.50% | 9.15% | 8.92822 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.99% | 0.0346624 |
| calibrated | 66.02% | 0.0331024 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2339 | 1377 | 962 | 48.15% |
| 60m | perp_synchronized_clock | 2339 | 1377 | 962 | 48.15% |
| 60m | combined_synchronized_clock | 2339 | 1355 | 984 | 48.12% |
| 15m | perp_original_clock | 2339 | 1377 | 962 | 48.08% |
| 15m | perp_synchronized_clock | 2339 | 1377 | 962 | 48.08% |
| 15m | combined_synchronized_clock | 2339 | 1355 | 984 | 47.01% |

## Data usability pilots

- Options: 611 captures; usable 7d RR25 in 518, usable 30d RR25 in 281; 471 valid hourly changes.
- Liquidations: 1713 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2339}`.
- Exchange stress: 1221/1221 scheduled records. Capture states: `{"missed": 45, "ok": 1176}`. Ratings: `{"low": 1176}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
