# Market studies

Generated 2026-11-19T07:49:36.680Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 153 | 117 | 117 |
| range | collecting (descriptive) | 153 | 110 | 104 |
| state | collecting (descriptive) | 614 | 363 | 361 |
| paired | collecting (descriptive) | 2456 | 2358 | 2353 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0686108 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00432038 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000618519 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00058436 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 67.31% | 0.0348058 |
| calibrated | 66.35% | 0.0333449 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2353 | 1385 | 968 | 48.09% |
| 60m | perp_synchronized_clock | 2353 | 1385 | 968 | 48.09% |
| 60m | combined_synchronized_clock | 2353 | 1363 | 990 | 48.06% |
| 15m | perp_original_clock | 2353 | 1385 | 968 | 48.16% |
| 15m | perp_synchronized_clock | 2353 | 1385 | 968 | 48.16% |
| 15m | combined_synchronized_clock | 2353 | 1363 | 990 | 47.10% |

## Data usability pilots

- Options: 614 captures; usable 7d RR25 in 521, usable 30d RR25 in 284; 474 valid hourly changes.
- Liquidations: 1722 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2351}`.
- Exchange stress: 1228/1228 scheduled records. Capture states: `{"missed": 45, "ok": 1183}`. Ratings: `{"low": 1183}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
