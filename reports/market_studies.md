# Market studies

Generated 2026-11-17T22:17:21.472Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 145 | 109 | 109 |
| range | collecting (descriptive) | 145 | 102 | 96 |
| state | collecting (descriptive) | 581 | 349 | 349 |
| paired | collecting (descriptive) | 2322 | 2224 | 2219 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0465613 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00395119 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000399359 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000732312 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.27% | 14.67% | 52.54% | 10.57% | 100.371 | 897.363 |
| ordinary/B2_10 | -10.32% | 14.52% | 51.67% | 10.65% | 73.9709 | 815.177 |
| ordinary/VOL_05 | -8.45% | 16.55% | 39.23% | 9.09% | 14.0316 | 98.0562 |
| ordinary/VOL_10 | -7.90% | 15.36% | 40.03% | 8.49% | 9.38076 | 65.5761 |
| stressed/B2_05 | -10.80% | 14.66% | 52.54% | 11.04% | 100.433 | 1460.41 |
| stressed/B2_10 | -10.71% | 14.48% | 51.69% | 10.98% | 74.0238 | 1229.59 |
| stressed/VOL_05 | -8.53% | 16.53% | 39.23% | 9.12% | 14.0388 | 178.068 |
| stressed/VOL_10 | -7.95% | 15.35% | 40.04% | 8.50% | 9.39272 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.58% | 0.0336147 |
| calibrated | 63.54% | 0.0313029 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2219 | 1316 | 903 | 48.10% |
| 60m | perp_synchronized_clock | 2219 | 1316 | 903 | 48.10% |
| 60m | combined_synchronized_clock | 2219 | 1298 | 921 | 48.15% |
| 15m | perp_original_clock | 2219 | 1316 | 903 | 47.80% |
| 15m | perp_synchronized_clock | 2219 | 1316 | 903 | 47.80% |
| 15m | combined_synchronized_clock | 2219 | 1298 | 921 | 46.84% |

## Data usability pilots

- Options: 581 captures; usable 7d RR25 in 496, usable 30d RR25 in 251; 453 valid hourly changes.
- Liquidations: 1623 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2219}`.
- Exchange stress: 1161/1161 scheduled records. Capture states: `{"missed": 45, "ok": 1116}`. Ratings: `{"low": 1116}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
