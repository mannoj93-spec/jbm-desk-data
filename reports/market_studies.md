# Market studies

Generated 2026-10-31T08:01:35.571Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 40 | 37 | 37 |
| range | collecting (descriptive) | 40 | 31 | 25 |
| state | collecting (descriptive) | 159 | 111 | 106 |
| paired | collecting (descriptive) | 633 | 547 | 541 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.666241 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00866761 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00340786 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00138632 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.60% | 15.31% | 43.79% | 1.95% | 137.362 | 302.795 |
| ordinary/B2_10 | -2.01% | 16.76% | 43.78% | 2.36% | 96.1782 | 262.932 |
| ordinary/VOL_05 | -2.10% | 21.52% | 47.92% | 2.93% | 36.3074 | 68.8516 |
| ordinary/VOL_10 | -1.87% | 19.77% | 47.37% | 2.66% | 27.6045 | 52.2225 |
| stressed/B2_05 | -1.81% | 15.28% | 43.80% | 2.09% | 137.447 | 514.703 |
| stressed/B2_10 | -2.16% | 16.68% | 43.79% | 2.45% | 96.2401 | 411.339 |
| stressed/VOL_05 | -2.16% | 21.48% | 47.94% | 2.94% | 36.3325 | 125.006 |
| stressed/VOL_10 | -1.91% | 19.75% | 47.39% | 2.66% | 27.6409 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 76.00% | 0.0332744 |
| calibrated | 72.00% | 0.0267651 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 541 | 326 | 215 | 54.29% |
| 60m | perp_synchronized_clock | 541 | 326 | 215 | 54.29% |
| 60m | combined_synchronized_clock | 541 | 322 | 219 | 54.66% |
| 15m | perp_original_clock | 541 | 326 | 215 | 47.85% |
| 15m | perp_synchronized_clock | 541 | 326 | 215 | 47.85% |
| 15m | combined_synchronized_clock | 541 | 322 | 219 | 47.83% |

## Data usability pilots

- Options: 158 captures; usable 7d RR25 in 135, usable 30d RR25 in 86; 127 valid hourly changes.
- Liquidations: 379 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 549}`.
- Exchange stress: 317/317 scheduled records. Capture states: `{"missed": 39, "ok": 278}`. Ratings: `{"low": 278}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
