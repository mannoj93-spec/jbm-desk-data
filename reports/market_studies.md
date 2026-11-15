# Market studies

Generated 2026-11-15T00:47:08.575Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 128 | 92 | 92 |
| range | collecting (descriptive) | 128 | 86 | 79 |
| state | collecting (descriptive) | 511 | 325 | 324 |
| paired | collecting (descriptive) | 2044 | 1949 | 1944 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0282228 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00475874 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000687926 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -3.21502e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.07% | 15.29% | 56.29% | 10.37% | 106.912 | 831.149 |
| ordinary/B2_10 | -10.10% | 15.21% | 55.61% | 10.42% | 79.9803 | 731.91 |
| ordinary/VOL_05 | -8.32% | 17.31% | 40.99% | 8.96% | 14.6967 | 91.4039 |
| ordinary/VOL_10 | -7.71% | 15.71% | 41.36% | 8.29% | 10.5498 | 65.5761 |
| stressed/B2_05 | -10.57% | 15.27% | 56.29% | 10.81% | 106.953 | 1366.26 |
| stressed/B2_10 | -10.47% | 15.16% | 55.63% | 10.74% | 80.0223 | 1131.69 |
| stressed/VOL_05 | -8.39% | 17.29% | 41.00% | 8.98% | 14.7051 | 165.985 |
| stressed/VOL_10 | -7.76% | 15.69% | 41.38% | 8.30% | 10.5631 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.56% | 0.0317592 |
| calibrated | 63.29% | 0.0281319 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1944 | 1157 | 787 | 48.83% |
| 60m | perp_synchronized_clock | 1944 | 1157 | 787 | 48.83% |
| 60m | combined_synchronized_clock | 1944 | 1144 | 800 | 48.69% |
| 15m | perp_original_clock | 1944 | 1157 | 787 | 47.28% |
| 15m | perp_synchronized_clock | 1944 | 1157 | 787 | 47.28% |
| 15m | combined_synchronized_clock | 1944 | 1144 | 800 | 46.68% |

## Data usability pilots

- Options: 511 captures; usable 7d RR25 in 431, usable 30d RR25 in 181; 400 valid hourly changes.
- Liquidations: 1413 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1939}`.
- Exchange stress: 1022/1022 scheduled records. Capture states: `{"missed": 44, "ok": 978}`. Ratings: `{"low": 978}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
