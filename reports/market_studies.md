# Market studies

Generated 2026-11-25T20:03:45.941Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 193 | 155 | 155 |
| range | collecting (descriptive) | 193 | 147 | 142 |
| state | collecting (descriptive) | 771 | 391 | 391 |
| paired | collecting (descriptive) | 3081 | 2983 | 2978 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.367991 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00159471 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00129582 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00130121 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.46% | 16.06% | 45.58% | 13.92% | 86.5407 | 979.787 |
| ordinary/B2_10 | -12.00% | 14.69% | 44.20% | 13.13% | 56.9179 | 815.177 |
| ordinary/VOL_05 | -10.43% | 16.79% | 35.62% | 11.99% | 10.7721 | 98.0562 |
| ordinary/VOL_10 | -10.23% | 17.02% | 37.29% | 11.91% | 7.19804 | 65.5761 |
| stressed/B2_05 | -13.04% | 16.07% | 45.58% | 14.39% | 86.632 | 1609.25 |
| stressed/B2_10 | -12.39% | 14.67% | 44.21% | 13.45% | 56.9869 | 1229.59 |
| stressed/VOL_05 | -10.50% | 16.78% | 35.63% | 12.02% | 10.7782 | 178.068 |
| stressed/VOL_10 | -10.28% | 17.01% | 37.30% | 11.93% | 7.20734 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.90% | 0.0390949 |
| calibrated | 69.72% | 0.041725 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2978 | 1677 | 1301 | 48.36% |
| 60m | perp_synchronized_clock | 2978 | 1677 | 1301 | 48.36% |
| 60m | combined_synchronized_clock | 2978 | 1647 | 1331 | 48.57% |
| 15m | perp_original_clock | 2978 | 1677 | 1301 | 48.54% |
| 15m | perp_synchronized_clock | 2978 | 1677 | 1301 | 48.54% |
| 15m | combined_synchronized_clock | 2978 | 1647 | 1331 | 47.60% |

## Data usability pilots

- Options: 769 captures; usable 7d RR25 in 661, usable 30d RR25 in 413; 607 valid hourly changes.
- Liquidations: 2190 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2975}`.
- Exchange stress: 1541/1541 scheduled records. Capture states: `{"missed": 45, "ok": 1496}`. Ratings: `{"low": 1496}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
