# Market studies

Generated 2026-11-27T03:02:50.795Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 200 | 163 | 163 |
| range | collecting (descriptive) | 200 | 155 | 149 |
| state | collecting (descriptive) | 802 | 398 | 395 |
| paired | collecting (descriptive) | 3205 | 3107 | 3102 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.293817 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00254655 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00102756 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00159172 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.81% | 15.93% | 44.71% | 13.92% | 85.0832 | 996.551 |
| ordinary/B2_10 | -11.35% | 14.58% | 43.28% | 13.13% | 54.7879 | 815.177 |
| ordinary/VOL_05 | -9.66% | 16.65% | 35.18% | 11.99% | 10.3663 | 98.0562 |
| ordinary/VOL_10 | -9.33% | 16.96% | 36.94% | 11.91% | 6.92671 | 65.5761 |
| stressed/B2_05 | -12.40% | 15.94% | 44.71% | 14.39% | 85.1771 | 1639.22 |
| stressed/B2_10 | -11.74% | 14.56% | 43.29% | 13.45% | 54.8575 | 1229.59 |
| stressed/VOL_05 | -9.74% | 16.64% | 35.18% | 12.02% | 10.3723 | 178.068 |
| stressed/VOL_10 | -9.38% | 16.96% | 36.95% | 11.93% | 6.93567 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.79% | 0.0399218 |
| calibrated | 70.47% | 0.0434157 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3102 | 1745 | 1357 | 48.14% |
| 60m | perp_synchronized_clock | 3102 | 1745 | 1357 | 48.14% |
| 60m | combined_synchronized_clock | 3102 | 1710 | 1392 | 48.42% |
| 15m | perp_original_clock | 3102 | 1745 | 1357 | 48.71% |
| 15m | perp_synchronized_clock | 3102 | 1745 | 1357 | 48.71% |
| 15m | combined_synchronized_clock | 3102 | 1710 | 1392 | 47.60% |

## Data usability pilots

- Options: 800 captures; usable 7d RR25 in 689, usable 30d RR25 in 413; 628 valid hourly changes.
- Liquidations: 2283 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3099}`.
- Exchange stress: 1603/1603 scheduled records. Capture states: `{"missed": 45, "ok": 1558}`. Ratings: `{"low": 1558}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
