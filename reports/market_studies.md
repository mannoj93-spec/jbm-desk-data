# Market studies

Generated 2026-10-26T07:01:13.626Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 9 | 7 | 7 |
| range | collecting (descriptive) | 9 | 1 | 0 |
| state | collecting (descriptive) | 38 | 18 | 13 |
| paired | collecting (descriptive) | 149 | 65 | 60 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 2.15666 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00823802 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0135417 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.39% | 13.72% | 53.43% | 0.72% | 249.51 | 97.5299 |
| ordinary/B2_10 | -0.31% | 13.56% | 55.64% | 0.66% | 156.229 | 61.0952 |
| ordinary/VOL_05 | -0.27% | 11.59% | 47.56% | 0.56% | 133.557 | 52.2225 |
| ordinary/VOL_10 | -0.27% | 11.59% | 47.56% | 0.56% | 133.557 | 52.2225 |
| stressed/B2_05 | -0.47% | 13.34% | 53.44% | 0.74% | 249.81 | 177.395 |
| stressed/B2_10 | -0.36% | 13.16% | 55.66% | 0.66% | 156.434 | 111.125 |
| stressed/VOL_05 | -0.31% | 11.25% | 47.58% | 0.56% | 133.724 | 94.9864 |
| stressed/VOL_10 | -0.31% | 11.25% | 47.58% | 0.56% | 133.724 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 60 | 34 | 26 | 52.94% |
| 60m | perp_synchronized_clock | 60 | 34 | 26 | 52.94% |
| 60m | combined_synchronized_clock | 60 | 35 | 25 | 48.57% |
| 15m | perp_original_clock | 60 | 34 | 26 | 41.18% |
| 15m | perp_synchronized_clock | 60 | 34 | 26 | 41.18% |
| 15m | combined_synchronized_clock | 60 | 35 | 25 | 40.00% |

## Data usability pilots

- Options: 37 captures; usable 7d RR25 in 37, usable 30d RR25 in 37; 36 valid hourly changes.
- Liquidations: 22 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 65}`.
- Exchange stress: 75/75 scheduled records. Capture states: `{"missed": 39, "ok": 36}`. Ratings: `{"low": 36}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
