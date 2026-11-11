# Market studies

Generated 2026-11-11T16:03:19.417Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 108 | 71 | 71 |
| range | collecting (descriptive) | 108 | 65 | 59 |
| state | collecting (descriptive) | 431 | 298 | 296 |
| paired | collecting (descriptive) | 1721 | 1627 | 1622 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0073078 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0041793 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00117014 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000269729 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.12% | 12.89% | 60.73% | 5.64% | 109.031 | 739.372 |
| ordinary/B2_10 | -5.57% | 13.77% | 60.11% | 6.11% | 86.3056 | 688.033 |
| ordinary/VOL_05 | -3.71% | 16.18% | 42.12% | 4.58% | 14.9607 | 78.3691 |
| ordinary/VOL_10 | -3.56% | 15.00% | 43.24% | 4.38% | 12.5371 | 65.5761 |
| stressed/B2_05 | -5.57% | 12.87% | 60.74% | 6.03% | 109.054 | 1200.26 |
| stressed/B2_10 | -5.93% | 13.71% | 60.12% | 6.41% | 86.3284 | 1052.22 |
| stressed/VOL_05 | -3.77% | 16.14% | 42.13% | 4.60% | 14.97 | 142.3 |
| stressed/VOL_10 | -3.62% | 14.98% | 43.26% | 4.39% | 12.5527 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.49% | 0.0301015 |
| calibrated | 67.80% | 0.0255034 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1622 | 997 | 625 | 49.05% |
| 60m | perp_synchronized_clock | 1622 | 997 | 625 | 49.05% |
| 60m | combined_synchronized_clock | 1622 | 986 | 636 | 48.99% |
| 15m | perp_original_clock | 1622 | 997 | 625 | 46.94% |
| 15m | perp_synchronized_clock | 1622 | 997 | 625 | 46.94% |
| 15m | combined_synchronized_clock | 1622 | 986 | 636 | 46.25% |

## Data usability pilots

- Options: 430 captures; usable 7d RR25 in 362, usable 30d RR25 in 117; 335 valid hourly changes.
- Liquidations: 1173 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1619}`.
- Exchange stress: 861/861 scheduled records. Capture states: `{"missed": 43, "ok": 818}`. Ratings: `{"low": 818}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
