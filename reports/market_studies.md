# Market studies

Generated 2026-11-08T03:31:41.905Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 86 | 50 | 50 |
| range | collecting (descriptive) | 86 | 44 | 38 |
| state | collecting (descriptive) | 346 | 250 | 245 |
| paired | collecting (descriptive) | 1383 | 1289 | 1284 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.113575 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00418759 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00161259 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.0014116 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.80% | 13.48% | 65.13% | 4.13% | 102.117 | 473.81 |
| ordinary/B2_10 | -4.27% | 14.68% | 64.85% | 4.63% | 83.5745 | 433.404 |
| ordinary/VOL_05 | -2.95% | 18.53% | 44.32% | 3.74% | 18.5297 | 78.3691 |
| ordinary/VOL_10 | -2.80% | 17.04% | 45.72% | 3.54% | 15.5309 | 65.5761 |
| stressed/B2_05 | -4.14% | 13.42% | 65.14% | 4.40% | 102.134 | 824.509 |
| stressed/B2_10 | -4.56% | 14.60% | 64.86% | 4.84% | 83.5803 | 720.219 |
| stressed/VOL_05 | -3.01% | 18.49% | 44.33% | 3.75% | 18.5404 | 142.3 |
| stressed/VOL_10 | -2.86% | 17.02% | 45.74% | 3.54% | 15.5497 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.68% | 0.0294718 |
| calibrated | 71.05% | 0.0235613 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1284 | 788 | 496 | 48.73% |
| 60m | perp_synchronized_clock | 1284 | 788 | 496 | 48.73% |
| 60m | combined_synchronized_clock | 1284 | 779 | 505 | 49.04% |
| 15m | perp_original_clock | 1284 | 788 | 496 | 47.21% |
| 15m | perp_synchronized_clock | 1284 | 788 | 496 | 47.21% |
| 15m | combined_synchronized_clock | 1284 | 779 | 505 | 46.73% |

## Data usability pilots

- Options: 346 captures; usable 7d RR25 in 291, usable 30d RR25 in 86; 267 valid hourly changes.
- Liquidations: 925 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1286}`.
- Exchange stress: 692/692 scheduled records. Capture states: `{"missed": 43, "ok": 649}`. Ratings: `{"low": 649}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
