# Market studies

Generated 2026-10-28T17:19:46.161Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 24 | 22 | 22 |
| range | collecting (descriptive) | 24 | 16 | 9 |
| state | collecting (descriptive) | 96 | 65 | 62 |
| paired | collecting (descriptive) | 382 | 296 | 291 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.41086 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00645201 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00081964 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00193299 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.15% | 9.60% | 49.26% | 0.84% | 142.474 | 162.815 |
| ordinary/B2_10 | -0.06% | 9.52% | 50.02% | 0.77% | 77.7199 | 88.8705 |
| ordinary/VOL_05 | 0.07% | 8.90% | 47.52% | 0.67% | 45.6473 | 52.2225 |
| ordinary/VOL_10 | 0.07% | 8.90% | 47.52% | 0.67% | 45.6473 | 52.2225 |
| stressed/B2_05 | -0.28% | 9.59% | 49.27% | 0.88% | 142.596 | 295.979 |
| stressed/B2_10 | -0.14% | 9.41% | 50.04% | 0.78% | 77.8211 | 161.642 |
| stressed/VOL_05 | 0.03% | 8.81% | 47.54% | 0.67% | 45.707 | 94.9864 |
| stressed/VOL_10 | 0.03% | 8.81% | 47.54% | 0.67% | 45.707 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 88.89% | 0.0325896 |
| calibrated | 88.89% | 0.0260595 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 291 | 178 | 113 | 48.88% |
| 60m | perp_synchronized_clock | 291 | 178 | 113 | 48.88% |
| 60m | combined_synchronized_clock | 291 | 183 | 108 | 48.63% |
| 15m | perp_original_clock | 291 | 178 | 113 | 46.63% |
| 15m | perp_synchronized_clock | 291 | 178 | 113 | 46.63% |
| 15m | combined_synchronized_clock | 291 | 183 | 108 | 46.45% |

## Data usability pilots

- Options: 96 captures; usable 7d RR25 in 81, usable 30d RR25 in 86; 77 valid hourly changes.
- Liquidations: 190 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 297}`.
- Exchange stress: 191/191 scheduled records. Capture states: `{"missed": 39, "ok": 152}`. Ratings: `{"low": 152}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
