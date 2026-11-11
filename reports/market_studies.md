# Market studies

Generated 2026-11-11T12:46:57.561Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 107 | 71 | 71 |
| range | collecting (descriptive) | 107 | 65 | 58 |
| state | collecting (descriptive) | 427 | 297 | 294 |
| paired | collecting (descriptive) | 1708 | 1614 | 1609 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0073078 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00425071 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00119503 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000466128 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 68.97% | 0.0299309 |
| calibrated | 67.24% | 0.0252529 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1609 | 989 | 620 | 49.04% |
| 60m | perp_synchronized_clock | 1609 | 989 | 620 | 49.04% |
| 60m | combined_synchronized_clock | 1609 | 977 | 632 | 49.03% |
| 15m | perp_original_clock | 1609 | 989 | 620 | 47.12% |
| 15m | perp_synchronized_clock | 1609 | 989 | 620 | 47.12% |
| 15m | combined_synchronized_clock | 1609 | 977 | 632 | 46.37% |

## Data usability pilots

- Options: 427 captures; usable 7d RR25 in 359, usable 30d RR25 in 114; 332 valid hourly changes.
- Liquidations: 1161 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1603}`.
- Exchange stress: 854/854 scheduled records. Capture states: `{"missed": 43, "ok": 811}`. Ratings: `{"low": 811}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
