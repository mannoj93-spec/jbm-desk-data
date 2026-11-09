# Market studies

Generated 2026-11-09T04:02:03.164Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 93 | 56 | 56 |
| range | collecting (descriptive) | 93 | 50 | 44 |
| state | collecting (descriptive) | 371 | 268 | 266 |
| paired | collecting (descriptive) | 1481 | 1387 | 1382 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0694743 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00387703 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00136857 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000994935 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.67% | 13.96% | 65.54% | 4.98% | 108.251 | 530.495 |
| ordinary/B2_10 | -5.15% | 15.03% | 65.01% | 5.49% | 85.9872 | 467.869 |
| ordinary/VOL_05 | -3.38% | 17.71% | 43.61% | 4.05% | 17.3427 | 78.3691 |
| ordinary/VOL_10 | -3.23% | 16.33% | 44.92% | 3.84% | 14.535 | 65.5761 |
| stressed/B2_05 | -5.06% | 13.91% | 65.55% | 5.32% | 108.26 | 927.169 |
| stressed/B2_10 | -5.46% | 14.94% | 65.02% | 5.74% | 85.9956 | 782.71 |
| stressed/VOL_05 | -3.44% | 17.67% | 43.62% | 4.06% | 17.3529 | 142.3 |
| stressed/VOL_10 | -3.29% | 16.31% | 44.94% | 3.85% | 14.5528 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.18% | 0.0281905 |
| calibrated | 65.91% | 0.0225987 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1382 | 860 | 522 | 48.02% |
| 60m | perp_synchronized_clock | 1382 | 860 | 522 | 48.02% |
| 60m | combined_synchronized_clock | 1382 | 854 | 528 | 48.24% |
| 15m | perp_original_clock | 1382 | 860 | 522 | 46.74% |
| 15m | perp_synchronized_clock | 1382 | 860 | 522 | 46.74% |
| 15m | combined_synchronized_clock | 1382 | 854 | 528 | 46.14% |

## Data usability pilots

- Options: 370 captures; usable 7d RR25 in 315, usable 30d RR25 in 86; 291 valid hourly changes.
- Liquidations: 993 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1379}`.
- Exchange stress: 741/741 scheduled records. Capture states: `{"missed": 43, "ok": 698}`. Ratings: `{"low": 698}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
