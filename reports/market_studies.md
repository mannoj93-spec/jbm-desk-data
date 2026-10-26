# Market studies

Generated 2026-10-26T12:46:30.818Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 11 | 9 | 9 |
| range | collecting (descriptive) | 11 | 3 | 0 |
| state | collecting (descriptive) | 43 | 23 | 19 |
| paired | collecting (descriptive) | 172 | 88 | 82 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.09985 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00674077 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00990854 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| 60m | perp_original_clock | 82 | 48 | 34 | 50.00% |
| 60m | perp_synchronized_clock | 82 | 48 | 34 | 50.00% |
| 60m | combined_synchronized_clock | 82 | 49 | 33 | 46.94% |
| 15m | perp_original_clock | 82 | 48 | 34 | 37.50% |
| 15m | perp_synchronized_clock | 82 | 48 | 34 | 37.50% |
| 15m | combined_synchronized_clock | 82 | 49 | 33 | 36.73% |

## Data usability pilots

- Options: 43 captures; usable 7d RR25 in 43, usable 30d RR25 in 43; 42 valid hourly changes.
- Liquidations: 34 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 85}`.
- Exchange stress: 86/86 scheduled records. Capture states: `{"missed": 39, "ok": 47}`. Ratings: `{"low": 47}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
