# Market studies

Generated 2026-10-30T10:31:39.400Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 34 | 32 | 32 |
| range | collecting (descriptive) | 34 | 26 | 20 |
| state | collecting (descriptive) | 137 | 93 | 90 |
| paired | collecting (descriptive) | 547 | 461 | 456 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.96077 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00319829 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00504052 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000822368 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.14% | 16.15% | 44.87% | 1.69% | 140.432 | 230.734 |
| ordinary/B2_10 | -1.59% | 17.88% | 45.78% | 2.15% | 93.0651 | 153.491 |
| ordinary/VOL_05 | -1.64% | 22.82% | 48.67% | 2.69% | 41.7348 | 68.8516 |
| ordinary/VOL_10 | -1.36% | 20.80% | 47.49% | 2.40% | 31.7412 | 52.2225 |
| stressed/B2_05 | -1.33% | 16.11% | 44.87% | 1.82% | 140.513 | 419.251 |
| stressed/B2_10 | -1.72% | 17.79% | 45.79% | 2.21% | 93.124 | 278.561 |
| stressed/VOL_05 | -1.69% | 22.77% | 48.69% | 2.69% | 41.763 | 125.006 |
| stressed/VOL_10 | -1.40% | 20.77% | 47.51% | 2.40% | 31.7829 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 80.00% | 0.0323479 |
| calibrated | 80.00% | 0.0258305 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 456 | 278 | 178 | 51.80% |
| 60m | perp_synchronized_clock | 456 | 278 | 178 | 51.80% |
| 60m | combined_synchronized_clock | 456 | 280 | 176 | 52.14% |
| 15m | perp_original_clock | 456 | 278 | 178 | 46.04% |
| 15m | perp_synchronized_clock | 456 | 278 | 178 | 46.04% |
| 15m | combined_synchronized_clock | 456 | 280 | 176 | 46.43% |

## Data usability pilots

- Options: 137 captures; usable 7d RR25 in 114, usable 30d RR25 in 86; 106 valid hourly changes.
- Liquidations: 313 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 461}`.
- Exchange stress: 274/274 scheduled records. Capture states: `{"missed": 39, "ok": 235}`. Ratings: `{"low": 235}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
