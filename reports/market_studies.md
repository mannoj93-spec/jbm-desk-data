# Market studies

Generated 2026-11-11T00:22:03.167Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 104 | 68 | 68 |
| range | collecting (descriptive) | 104 | 62 | 55 |
| state | collecting (descriptive) | 415 | 289 | 288 |
| paired | collecting (descriptive) | 1658 | 1564 | 1559 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0143541 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00448051 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000668428 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000801796 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.27% | 13.09% | 61.53% | 5.62% | 112.058 | 739.372 |
| ordinary/B2_10 | -5.72% | 14.00% | 60.88% | 6.07% | 88.6924 | 688.033 |
| ordinary/VOL_05 | -3.86% | 16.49% | 42.39% | 4.58% | 15.3829 | 78.3691 |
| ordinary/VOL_10 | -3.72% | 15.27% | 43.55% | 4.38% | 12.8912 | 65.5761 |
| stressed/B2_05 | -5.72% | 13.07% | 61.53% | 6.01% | 112.069 | 1200.26 |
| stressed/B2_10 | -6.08% | 13.94% | 60.89% | 6.36% | 88.7084 | 1052.22 |
| stressed/VOL_05 | -3.92% | 16.45% | 42.40% | 4.60% | 15.3924 | 142.3 |
| stressed/VOL_10 | -3.77% | 15.26% | 43.56% | 4.39% | 12.9072 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.27% | 0.0293495 |
| calibrated | 65.45% | 0.0244143 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1559 | 962 | 597 | 48.96% |
| 60m | perp_synchronized_clock | 1559 | 962 | 597 | 48.96% |
| 60m | combined_synchronized_clock | 1559 | 950 | 609 | 49.05% |
| 15m | perp_original_clock | 1559 | 962 | 597 | 47.09% |
| 15m | perp_synchronized_clock | 1559 | 962 | 597 | 47.09% |
| 15m | combined_synchronized_clock | 1559 | 950 | 609 | 46.42% |

## Data usability pilots

- Options: 415 captures; usable 7d RR25 in 347, usable 30d RR25 in 102; 320 valid hourly changes.
- Liquidations: 1125 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1555}`.
- Exchange stress: 829/829 scheduled records. Capture states: `{"missed": 43, "ok": 786}`. Ratings: `{"low": 786}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
