# Market studies

Generated 2026-10-29T02:32:34.455Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 26 | 24 | 24 |
| range | collecting (descriptive) | 26 | 18 | 12 |
| state | collecting (descriptive) | 105 | 72 | 67 |
| paired | collecting (descriptive) | 419 | 333 | 328 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.23299 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00648625 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000956273 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000381098 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.05% | 9.33% | 47.99% | 0.84% | 163.647 | 203.444 |
| ordinary/B2_10 | 0.13% | 9.24% | 48.69% | 0.77% | 110.378 | 137.307 |
| ordinary/VOL_05 | 0.53% | 9.36% | 48.00% | 0.67% | 47.0485 | 58.5665 |
| ordinary/VOL_10 | 0.49% | 9.21% | 47.53% | 0.67% | 41.9528 | 52.2225 |
| stressed/B2_05 | -0.11% | 9.30% | 47.99% | 0.88% | 163.742 | 369.736 |
| stressed/B2_10 | 0.02% | 9.09% | 48.70% | 0.78% | 110.452 | 249.621 |
| stressed/VOL_05 | 0.48% | 9.27% | 48.02% | 0.67% | 47.09 | 106.48 |
| stressed/VOL_10 | 0.45% | 9.14% | 47.55% | 0.67% | 42.0078 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 91.67% | 0.0323133 |
| calibrated | 91.67% | 0.0257685 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 328 | 200 | 128 | 47.50% |
| 60m | perp_synchronized_clock | 328 | 200 | 128 | 47.50% |
| 60m | combined_synchronized_clock | 328 | 206 | 122 | 48.06% |
| 15m | perp_original_clock | 328 | 200 | 128 | 45.50% |
| 15m | perp_synchronized_clock | 328 | 200 | 128 | 45.50% |
| 15m | combined_synchronized_clock | 328 | 206 | 122 | 46.12% |

## Data usability pilots

- Options: 105 captures; usable 7d RR25 in 89, usable 30d RR25 in 86; 83 valid hourly changes.
- Liquidations: 217 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 333}`.
- Exchange stress: 210/210 scheduled records. Capture states: `{"missed": 39, "ok": 171}`. Ratings: `{"low": 171}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
