# Market studies

Generated 2026-11-23T03:17:39.482Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 176 | 139 | 139 |
| range | collecting (descriptive) | 176 | 132 | 126 |
| state | collecting (descriptive) | 706 | 377 | 375 |
| paired | collecting (descriptive) | 2822 | 2724 | 2719 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.322891 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.000116679 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00183903 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00126425 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.65% | 16.60% | 47.69% | 13.92% | 88.964 | 939.242 |
| ordinary/B2_10 | -11.15% | 15.17% | 46.31% | 13.13% | 61.7721 | 815.177 |
| ordinary/VOL_05 | -9.43% | 17.33% | 36.65% | 11.99% | 11.6976 | 98.0562 |
| ordinary/VOL_10 | -9.05% | 17.42% | 38.08% | 11.91% | 7.81716 | 65.5761 |
| stressed/B2_05 | -12.21% | 16.61% | 47.69% | 14.39% | 89.0516 | 1536 |
| stressed/B2_10 | -11.54% | 15.15% | 46.32% | 13.45% | 61.8385 | 1229.59 |
| stressed/VOL_05 | -9.50% | 17.32% | 36.66% | 12.02% | 11.7041 | 178.068 |
| stressed/VOL_10 | -9.10% | 17.41% | 38.09% | 11.93% | 7.82722 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.87% | 0.0367392 |
| calibrated | 67.46% | 0.0371377 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2719 | 1560 | 1159 | 48.40% |
| 60m | perp_synchronized_clock | 2719 | 1560 | 1159 | 48.40% |
| 60m | combined_synchronized_clock | 2719 | 1533 | 1186 | 48.60% |
| 15m | perp_original_clock | 2719 | 1560 | 1159 | 48.91% |
| 15m | perp_synchronized_clock | 2719 | 1560 | 1159 | 48.91% |
| 15m | combined_synchronized_clock | 2719 | 1533 | 1186 | 48.01% |

## Data usability pilots

- Options: 705 captures; usable 7d RR25 in 602, usable 30d RR25 in 361; 549 valid hourly changes.
- Liquidations: 1995 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2715}`.
- Exchange stress: 1411/1411 scheduled records. Capture states: `{"missed": 45, "ok": 1366}`. Ratings: `{"low": 1366}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
