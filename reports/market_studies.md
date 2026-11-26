# Market studies

Generated 2026-11-26T18:03:12.029Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 198 | 161 | 161 |
| range | collecting (descriptive) | 198 | 153 | 147 |
| state | collecting (descriptive) | 793 | 393 | 393 |
| paired | collecting (descriptive) | 3169 | 3071 | 3066 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.308643 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00225492 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00115848 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00120271 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.79% | 16.03% | 44.89% | 13.92% | 85.2798 | 990.918 |
| ordinary/B2_10 | -11.35% | 14.67% | 43.50% | 13.13% | 55.3111 | 815.177 |
| ordinary/VOL_05 | -9.66% | 16.75% | 35.29% | 11.99% | 10.466 | 98.0562 |
| ordinary/VOL_10 | -9.33% | 17.06% | 37.03% | 11.91% | 6.99336 | 65.5761 |
| stressed/B2_05 | -12.39% | 16.04% | 44.90% | 14.39% | 85.3733 | 1629.05 |
| stressed/B2_10 | -11.74% | 14.65% | 43.51% | 13.45% | 55.3806 | 1229.59 |
| stressed/VOL_05 | -9.74% | 16.74% | 35.29% | 12.02% | 10.472 | 178.068 |
| stressed/VOL_10 | -9.38% | 17.06% | 37.04% | 11.93% | 7.00241 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.03% | 0.0396433 |
| calibrated | 70.75% | 0.0428984 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3066 | 1724 | 1342 | 48.03% |
| 60m | perp_synchronized_clock | 3066 | 1724 | 1342 | 48.03% |
| 60m | combined_synchronized_clock | 3066 | 1693 | 1373 | 48.20% |
| 15m | perp_original_clock | 3066 | 1724 | 1342 | 48.55% |
| 15m | perp_synchronized_clock | 3066 | 1724 | 1342 | 48.55% |
| 15m | combined_synchronized_clock | 3066 | 1693 | 1373 | 47.49% |

## Data usability pilots

- Options: 791 captures; usable 7d RR25 in 681, usable 30d RR25 in 413; 623 valid hourly changes.
- Liquidations: 2256 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3063}`.
- Exchange stress: 1585/1585 scheduled records. Capture states: `{"missed": 45, "ok": 1540}`. Ratings: `{"low": 1540}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
