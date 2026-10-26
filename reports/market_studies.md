# Market studies

Generated 2026-10-26T15:01:32.656Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 11 | 9 | 9 |
| range | collecting (descriptive) | 11 | 3 | 0 |
| state | collecting (descriptive) | 46 | 25 | 21 |
| paired | collecting (descriptive) | 181 | 97 | 92 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.09985 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00353277 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00883152 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.21% | 12.27% | 52.14% | 0.73% | 198.699 | 97.5299 |
| ordinary/B2_10 | -0.16% | 12.00% | 53.01% | 0.68% | 152.691 | 74.9863 |
| ordinary/VOL_05 | -0.08% | 10.49% | 47.52% | 0.57% | 106.335 | 52.2225 |
| ordinary/VOL_10 | -0.08% | 10.49% | 47.52% | 0.57% | 106.335 | 52.2225 |
| stressed/B2_05 | -0.29% | 12.03% | 52.15% | 0.75% | 198.951 | 177.395 |
| stressed/B2_10 | -0.22% | 11.70% | 53.03% | 0.69% | 152.895 | 136.413 |
| stressed/VOL_05 | -0.13% | 10.25% | 47.54% | 0.57% | 106.471 | 94.9864 |
| stressed/VOL_10 | -0.13% | 10.25% | 47.54% | 0.57% | 106.471 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 92 | 52 | 40 | 50.00% |
| 60m | perp_synchronized_clock | 92 | 52 | 40 | 50.00% |
| 60m | combined_synchronized_clock | 92 | 53 | 39 | 47.17% |
| 15m | perp_original_clock | 92 | 52 | 40 | 36.54% |
| 15m | perp_synchronized_clock | 92 | 52 | 40 | 36.54% |
| 15m | combined_synchronized_clock | 92 | 53 | 39 | 35.85% |

## Data usability pilots

- Options: 45 captures; usable 7d RR25 in 45, usable 30d RR25 in 45; 43 valid hourly changes.
- Liquidations: 41 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 97}`.
- Exchange stress: 91/91 scheduled records. Capture states: `{"missed": 39, "ok": 52}`. Ratings: `{"low": 52}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
