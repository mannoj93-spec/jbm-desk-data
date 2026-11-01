# Market studies

Generated 2026-11-01T07:16:19.524Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 45 | 41 | 41 |
| range | collecting (descriptive) | 45 | 35 | 31 |
| state | collecting (descriptive) | 182 | 130 | 125 |
| paired | collecting (descriptive) | 726 | 640 | 635 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.706197 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00591753 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -1.09765e-05 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00216535 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.35% | 14.61% | 45.76% | 1.95% | 135.327 | 325.746 |
| ordinary/B2_10 | -1.78% | 15.98% | 45.44% | 2.36% | 93.459 | 276.217 |
| ordinary/VOL_05 | -1.91% | 20.46% | 47.45% | 2.93% | 32.8836 | 68.8516 |
| ordinary/VOL_10 | -1.66% | 18.81% | 47.29% | 2.66% | 24.9964 | 52.2225 |
| stressed/B2_05 | -1.58% | 14.58% | 45.76% | 2.09% | 135.408 | 556.325 |
| stressed/B2_10 | -1.93% | 15.91% | 45.45% | 2.45% | 93.5168 | 435.443 |
| stressed/VOL_05 | -1.97% | 20.42% | 47.47% | 2.94% | 32.9067 | 125.006 |
| stressed/VOL_10 | -1.70% | 18.79% | 47.31% | 2.66% | 25.0294 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.42% | 0.031432 |
| calibrated | 74.19% | 0.0250951 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 635 | 389 | 246 | 52.70% |
| 60m | perp_synchronized_clock | 635 | 389 | 246 | 52.70% |
| 60m | combined_synchronized_clock | 635 | 383 | 252 | 53.26% |
| 15m | perp_original_clock | 635 | 389 | 246 | 47.30% |
| 15m | perp_synchronized_clock | 635 | 389 | 246 | 47.30% |
| 15m | combined_synchronized_clock | 635 | 383 | 252 | 48.04% |

## Data usability pilots

- Options: 182 captures; usable 7d RR25 in 159, usable 30d RR25 in 86; 149 valid hourly changes.
- Liquidations: 447 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 1, "missed": 58, "ok": 640}`.
- Exchange stress: 363/363 scheduled records. Capture states: `{"missed": 39, "ok": 324}`. Ratings: `{"low": 324}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
