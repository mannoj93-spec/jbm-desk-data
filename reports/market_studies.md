# Market studies

Generated 2026-11-16T10:34:25.675Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 136 | 100 | 100 |
| range | collecting (descriptive) | 136 | 94 | 88 |
| state | collecting (descriptive) | 545 | 337 | 335 |
| paired | collecting (descriptive) | 2179 | 2083 | 2078 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.035176 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.003726 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000554556 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000210539 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.05% | 15.07% | 54.27% | 10.56% | 102.854 | 873.64 |
| ordinary/B2_10 | -10.12% | 14.98% | 53.64% | 10.65% | 78.4923 | 815.177 |
| ordinary/VOL_05 | -8.22% | 17.09% | 40.13% | 9.09% | 14.9019 | 98.0562 |
| ordinary/VOL_10 | -7.62% | 15.76% | 40.69% | 8.49% | 9.96607 | 65.5761 |
| stressed/B2_05 | -10.56% | 15.06% | 54.28% | 11.01% | 102.909 | 1417.53 |
| stressed/B2_10 | -10.51% | 14.94% | 53.65% | 10.98% | 78.5368 | 1229.59 |
| stressed/VOL_05 | -8.29% | 17.07% | 40.14% | 9.12% | 14.9092 | 178.068 |
| stressed/VOL_10 | -7.67% | 15.74% | 40.71% | 8.50% | 9.97872 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 61.36% | 0.0321003 |
| calibrated | 60.23% | 0.0289939 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2078 | 1236 | 842 | 48.22% |
| 60m | perp_synchronized_clock | 2078 | 1236 | 842 | 48.22% |
| 60m | combined_synchronized_clock | 2078 | 1225 | 853 | 48.16% |
| 15m | perp_original_clock | 2078 | 1236 | 842 | 47.65% |
| 15m | perp_synchronized_clock | 2078 | 1236 | 842 | 47.65% |
| 15m | combined_synchronized_clock | 2078 | 1225 | 853 | 46.86% |

## Data usability pilots

- Options: 545 captures; usable 7d RR25 in 465, usable 30d RR25 in 215; 426 valid hourly changes.
- Liquidations: 1515 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2075}`.
- Exchange stress: 1090/1090 scheduled records. Capture states: `{"missed": 44, "ok": 1046}`. Ratings: `{"low": 1046}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
