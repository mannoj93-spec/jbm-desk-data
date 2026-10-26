# Market studies

Generated 2026-10-26T00:11:27.188Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 8 | 5 | 5 |
| range | registered; not launched | 8 | 0 | 0 |
| state | collecting (descriptive) | 31 | 12 | 10 |
| paired | collecting (descriptive) | 121 | 40 | 38 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 4.68301 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.00877718 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00822368 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.17% | 14.58% | 54.73% | 0.45% | 363.042 | 91.8244 |
| ordinary/B2_10 | 0.27% | 13.41% | 55.63% | 0.39% | 241.493 | 61.0952 |
| ordinary/VOL_05 | 0.23% | 11.47% | 47.56% | 0.33% | 206.463 | 52.2225 |
| ordinary/VOL_10 | 0.23% | 11.47% | 47.56% | 0.33% | 206.463 | 52.2225 |
| stressed/B2_05 | 0.09% | 14.32% | 54.74% | 0.46% | 363.472 | 167.024 |
| stressed/B2_10 | 0.22% | 12.98% | 55.66% | 0.39% | 241.801 | 111.125 |
| stressed/VOL_05 | 0.19% | 11.10% | 47.58% | 0.33% | 206.715 | 94.9864 |
| stressed/VOL_10 | 0.19% | 11.10% | 47.58% | 0.33% | 206.715 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 38 | 28 | 10 | 50.00% |
| 60m | perp_synchronized_clock | 38 | 28 | 10 | 50.00% |
| 60m | combined_synchronized_clock | 38 | 29 | 9 | 48.28% |
| 15m | perp_original_clock | 38 | 28 | 10 | 46.43% |
| 15m | perp_synchronized_clock | 38 | 28 | 10 | 46.43% |
| 15m | combined_synchronized_clock | 38 | 29 | 9 | 44.83% |

## Data usability pilots

- Options: 31 captures; usable 7d RR25 in 31, usable 30d RR25 in 31; 30 valid hourly changes.
- Liquidations: 9 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 37}`.
- Exchange stress: 61/61 scheduled records. Capture states: `{"missed": 38, "ok": 23}`. Ratings: `{"low": 23}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
