# Market studies

Generated 2026-10-26T03:52:22.047Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 8 | 6 | 6 |
| range | registered; not launched | 8 | 0 | 0 |
| state | collecting (descriptive) | 34 | 14 | 11 |
| paired | collecting (descriptive) | 136 | 52 | 47 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.94349 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.00866859 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00664894 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| 60m | perp_original_clock | 47 | 30 | 17 | 50.00% |
| 60m | perp_synchronized_clock | 47 | 30 | 17 | 50.00% |
| 60m | combined_synchronized_clock | 47 | 31 | 16 | 48.39% |
| 15m | perp_original_clock | 47 | 30 | 17 | 43.33% |
| 15m | perp_synchronized_clock | 47 | 30 | 17 | 43.33% |
| 15m | combined_synchronized_clock | 47 | 31 | 16 | 41.94% |

## Data usability pilots

- Options: 34 captures; usable 7d RR25 in 34, usable 30d RR25 in 34; 33 valid hourly changes.
- Liquidations: 14 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 49}`.
- Exchange stress: 68/68 scheduled records. Capture states: `{"missed": 39, "ok": 29}`. Ratings: `{"low": 29}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
