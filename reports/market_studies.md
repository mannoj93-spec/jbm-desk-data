# Market studies

Generated 2026-11-02T14:17:55.340Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 53 | 41 | 41 |
| range | collecting (descriptive) | 53 | 35 | 35 |
| state | collecting (descriptive) | 213 | 154 | 153 |
| paired | collecting (descriptive) | 850 | 762 | 757 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.706197 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000739824 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00255945 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 757 | 475 | 282 | 52.84% |
| 60m | perp_synchronized_clock | 757 | 475 | 282 | 52.84% |
| 60m | combined_synchronized_clock | 757 | 464 | 293 | 53.45% |
| 15m | perp_original_clock | 757 | 475 | 282 | 47.79% |
| 15m | perp_synchronized_clock | 757 | 475 | 282 | 47.79% |
| 15m | combined_synchronized_clock | 757 | 464 | 293 | 48.06% |

## Data usability pilots

- Options: 213 captures; usable 7d RR25 in 190, usable 30d RR25 in 86; 178 valid hourly changes.
- Liquidations: 539 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 58, "ok": 763}`.
- Exchange stress: 425/425 scheduled records. Capture states: `{"missed": 40, "ok": 385}`. Ratings: `{"low": 385}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
