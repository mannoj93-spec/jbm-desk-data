# Market studies

Generated 2026-10-30T18:31:48.570Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 36 | 34 | 34 |
| range | collecting (descriptive) | 36 | 28 | 22 |
| state | collecting (descriptive) | 145 | 99 | 96 |
| paired | collecting (descriptive) | 579 | 493 | 488 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.646175 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00818581 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00377429 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00140881 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.35% | 15.77% | 44.18% | 1.73% | 137.237 | 239.455 |
| ordinary/B2_10 | -1.75% | 17.38% | 44.60% | 2.15% | 87.7867 | 153.491 |
| ordinary/VOL_05 | -1.90% | 22.24% | 48.35% | 2.69% | 39.3727 | 68.8516 |
| ordinary/VOL_10 | -1.65% | 20.34% | 47.44% | 2.40% | 29.9402 | 52.2225 |
| stressed/B2_05 | -1.55% | 15.73% | 44.19% | 1.87% | 137.319 | 434.795 |
| stressed/B2_10 | -1.87% | 17.28% | 44.61% | 2.21% | 87.8449 | 278.561 |
| stressed/VOL_05 | -1.96% | 22.19% | 48.37% | 2.69% | 39.3996 | 125.006 |
| stressed/VOL_10 | -1.69% | 20.31% | 47.46% | 2.40% | 29.9796 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 72.73% | 0.032522 |
| calibrated | 72.73% | 0.0260082 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 488 | 295 | 193 | 52.88% |
| 60m | perp_synchronized_clock | 488 | 295 | 193 | 52.88% |
| 60m | combined_synchronized_clock | 488 | 296 | 192 | 53.38% |
| 15m | perp_original_clock | 488 | 295 | 193 | 46.44% |
| 15m | perp_synchronized_clock | 488 | 295 | 193 | 46.44% |
| 15m | combined_synchronized_clock | 488 | 296 | 192 | 46.96% |

## Data usability pilots

- Options: 145 captures; usable 7d RR25 in 122, usable 30d RR25 in 86; 114 valid hourly changes.
- Liquidations: 337 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 493}`.
- Exchange stress: 290/290 scheduled records. Capture states: `{"missed": 39, "ok": 251}`. Ratings: `{"low": 251}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
