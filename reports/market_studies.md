# Market studies

Generated 2026-10-28T11:32:24.033Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 22 | 20 | 20 |
| range | collecting (descriptive) | 22 | 14 | 8 |
| state | collecting (descriptive) | 90 | 61 | 56 |
| paired | collecting (descriptive) | 359 | 273 | 268 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.54998 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00642786 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00153483 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00209888 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.27% | 9.47% | 48.76% | 0.84% | 131.551 | 137.08 |
| ordinary/B2_10 | 0.36% | 9.27% | 49.47% | 0.77% | 85.2376 | 88.8705 |
| ordinary/VOL_05 | 0.43% | 8.75% | 47.50% | 0.67% | 50.0644 | 52.2225 |
| ordinary/VOL_10 | 0.43% | 8.75% | 47.50% | 0.67% | 50.0644 | 52.2225 |
| stressed/B2_05 | 0.15% | 9.43% | 48.76% | 0.88% | 131.685 | 249.236 |
| stressed/B2_10 | 0.28% | 9.16% | 49.49% | 0.78% | 85.3472 | 161.642 |
| stressed/VOL_05 | 0.39% | 8.66% | 47.52% | 0.67% | 50.1298 | 94.9864 |
| stressed/VOL_10 | 0.39% | 8.66% | 47.52% | 0.67% | 50.1298 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 87.50% | 0.0326782 |
| calibrated | 87.50% | 0.0261625 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 268 | 167 | 101 | 49.10% |
| 60m | perp_synchronized_clock | 268 | 167 | 101 | 49.10% |
| 60m | combined_synchronized_clock | 268 | 172 | 96 | 48.84% |
| 15m | perp_original_clock | 268 | 167 | 101 | 46.71% |
| 15m | perp_synchronized_clock | 268 | 167 | 101 | 46.71% |
| 15m | combined_synchronized_clock | 268 | 172 | 96 | 45.93% |

## Data usability pilots

- Options: 90 captures; usable 7d RR25 in 81, usable 30d RR25 in 86; 77 valid hourly changes.
- Liquidations: 172 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 273}`.
- Exchange stress: 180/180 scheduled records. Capture states: `{"missed": 39, "ok": 141}`. Ratings: `{"low": 141}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
