# Market studies

Generated 2026-10-26T01:46:09.046Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 8 | 6 | 6 |
| range | registered; not launched | 8 | 0 | 0 |
| state | collecting (descriptive) | 32 | 12 | 10 |
| paired | collecting (descriptive) | 128 | 44 | 40 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.94349 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.00877718 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0078125 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.38% | 15.32% | 54.12% | 0.71% | 260.313 | 91.8244 |
| ordinary/B2_10 | -0.31% | 15.15% | 55.66% | 0.65% | 173.13 | 61.0952 |
| ordinary/VOL_05 | -0.26% | 12.95% | 47.58% | 0.56% | 148.022 | 52.2225 |
| ordinary/VOL_10 | -0.26% | 12.95% | 47.58% | 0.56% | 148.022 | 52.2225 |
| stressed/B2_05 | -0.46% | 14.89% | 54.13% | 0.73% | 260.639 | 167.024 |
| stressed/B2_10 | -0.36% | 14.69% | 55.68% | 0.65% | 173.355 | 111.125 |
| stressed/VOL_05 | -0.31% | 12.55% | 47.60% | 0.56% | 148.206 | 94.9864 |
| stressed/VOL_10 | -0.31% | 12.55% | 47.60% | 0.56% | 148.206 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 40 | 29 | 11 | 48.28% |
| 60m | perp_synchronized_clock | 40 | 29 | 11 | 48.28% |
| 60m | combined_synchronized_clock | 40 | 30 | 10 | 46.67% |
| 15m | perp_original_clock | 40 | 29 | 11 | 44.83% |
| 15m | perp_synchronized_clock | 40 | 29 | 11 | 44.83% |
| 15m | combined_synchronized_clock | 40 | 30 | 10 | 43.33% |

## Data usability pilots

- Options: 32 captures; usable 7d RR25 in 32, usable 30d RR25 in 32; 31 valid hourly changes.
- Liquidations: 11 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 41}`.
- Exchange stress: 64/64 scheduled records. Capture states: `{"missed": 39, "ok": 25}`. Ratings: `{"low": 25}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
