# Market studies

Generated 2026-10-31T12:20:42.356Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 41 | 39 | 39 |
| range | collecting (descriptive) | 41 | 33 | 26 |
| state | collecting (descriptive) | 163 | 113 | 110 |
| paired | collecting (descriptive) | 650 | 564 | 559 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.812637 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00808514 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00218347 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00111807 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.38% | 14.99% | 44.58% | 1.95% | 134.664 | 311.007 |
| ordinary/B2_10 | -1.82% | 16.39% | 44.49% | 2.36% | 98.0988 | 276.217 |
| ordinary/VOL_05 | -1.94% | 20.99% | 47.68% | 2.93% | 34.5129 | 68.8516 |
| ordinary/VOL_10 | -1.69% | 19.30% | 47.33% | 2.66% | 26.2375 | 52.2225 |
| stressed/B2_05 | -1.59% | 14.96% | 44.58% | 2.09% | 134.746 | 529.591 |
| stressed/B2_10 | -1.97% | 16.32% | 44.50% | 2.45% | 98.1557 | 435.443 |
| stressed/VOL_05 | -1.99% | 20.95% | 47.69% | 2.94% | 34.537 | 125.006 |
| stressed/VOL_10 | -1.73% | 19.28% | 47.35% | 2.66% | 26.2721 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 76.92% | 0.0331322 |
| calibrated | 73.08% | 0.0266241 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 559 | 334 | 225 | 53.89% |
| 60m | perp_synchronized_clock | 559 | 334 | 225 | 53.89% |
| 60m | combined_synchronized_clock | 559 | 332 | 227 | 54.22% |
| 15m | perp_original_clock | 559 | 334 | 225 | 47.90% |
| 15m | perp_synchronized_clock | 559 | 334 | 225 | 47.90% |
| 15m | combined_synchronized_clock | 559 | 332 | 227 | 47.89% |

## Data usability pilots

- Options: 163 captures; usable 7d RR25 in 140, usable 30d RR25 in 86; 132 valid hourly changes.
- Liquidations: 391 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 565}`.
- Exchange stress: 325/325 scheduled records. Capture states: `{"missed": 39, "ok": 286}`. Ratings: `{"low": 286}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
