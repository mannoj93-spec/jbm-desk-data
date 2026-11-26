# Market studies

Generated 2026-11-26T13:32:58.790Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 197 | 160 | 160 |
| range | collecting (descriptive) | 197 | 152 | 147 |
| state | collecting (descriptive) | 788 | 393 | 391 |
| paired | collecting (descriptive) | 3151 | 3053 | 3048 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.309491 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00225492 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00120981 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.78% | 16.08% | 45.00% | 13.92% | 85.6831 | 990.918 |
| ordinary/B2_10 | -11.34% | 14.71% | 43.61% | 13.13% | 55.5745 | 815.177 |
| ordinary/VOL_05 | -9.65% | 16.80% | 35.34% | 11.99% | 10.5162 | 98.0562 |
| ordinary/VOL_10 | -9.31% | 17.12% | 37.07% | 11.91% | 7.02692 | 65.5761 |
| stressed/B2_05 | -12.37% | 16.09% | 45.00% | 14.39% | 85.7757 | 1629.05 |
| stressed/B2_10 | -11.72% | 14.69% | 43.62% | 13.45% | 55.6439 | 1229.59 |
| stressed/VOL_05 | -9.72% | 16.79% | 35.34% | 12.02% | 10.5222 | 178.068 |
| stressed/VOL_10 | -9.36% | 17.11% | 37.08% | 11.93% | 7.036 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.03% | 0.0396433 |
| calibrated | 70.75% | 0.0428984 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3048 | 1717 | 1331 | 48.11% |
| 60m | perp_synchronized_clock | 3048 | 1717 | 1331 | 48.11% |
| 60m | combined_synchronized_clock | 3048 | 1686 | 1362 | 48.28% |
| 15m | perp_original_clock | 3048 | 1717 | 1331 | 48.51% |
| 15m | perp_synchronized_clock | 3048 | 1717 | 1331 | 48.51% |
| 15m | combined_synchronized_clock | 3048 | 1686 | 1362 | 47.45% |

## Data usability pilots

- Options: 787 captures; usable 7d RR25 in 678, usable 30d RR25 in 413; 620 valid hourly changes.
- Liquidations: 2241 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3043}`.
- Exchange stress: 1576/1576 scheduled records. Capture states: `{"missed": 45, "ok": 1531}`. Ratings: `{"low": 1531}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
