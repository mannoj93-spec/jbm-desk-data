# Market studies

Generated 2026-11-14T22:32:16.201Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 127 | 91 | 91 |
| range | collecting (descriptive) | 127 | 85 | 79 |
| state | collecting (descriptive) | 509 | 325 | 324 |
| paired | collecting (descriptive) | 2035 | 1940 | 1935 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0839546 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00475874 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000687926 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000129199 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.55% | 15.17% | 56.46% | 9.85% | 107.678 | 831.149 |
| ordinary/B2_10 | -9.47% | 14.98% | 55.73% | 9.79% | 80.5566 | 731.91 |
| ordinary/VOL_05 | -7.82% | 17.24% | 41.06% | 8.46% | 14.8039 | 91.4039 |
| ordinary/VOL_10 | -7.23% | 15.63% | 41.45% | 7.82% | 10.6273 | 65.5761 |
| stressed/B2_05 | -10.05% | 15.17% | 56.47% | 10.30% | 107.717 | 1366.26 |
| stressed/B2_10 | -9.84% | 14.94% | 55.74% | 10.11% | 80.5972 | 1131.69 |
| stressed/VOL_05 | -7.89% | 17.22% | 41.07% | 8.48% | 14.8124 | 165.985 |
| stressed/VOL_10 | -7.28% | 15.62% | 41.46% | 7.83% | 10.6407 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.56% | 0.0317592 |
| calibrated | 63.29% | 0.0281319 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1935 | 1154 | 781 | 48.87% |
| 60m | perp_synchronized_clock | 1935 | 1154 | 781 | 48.87% |
| 60m | combined_synchronized_clock | 1935 | 1142 | 793 | 48.69% |
| 15m | perp_original_clock | 1935 | 1154 | 781 | 47.31% |
| 15m | perp_synchronized_clock | 1935 | 1154 | 781 | 47.31% |
| 15m | combined_synchronized_clock | 1935 | 1142 | 793 | 46.67% |

## Data usability pilots

- Options: 509 captures; usable 7d RR25 in 429, usable 30d RR25 in 179; 398 valid hourly changes.
- Liquidations: 1407 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1931}`.
- Exchange stress: 1018/1018 scheduled records. Capture states: `{"missed": 44, "ok": 974}`. Ratings: `{"low": 974}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
