# Market studies

Generated 2026-11-08T08:46:29.852Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 88 | 52 | 52 |
| range | collecting (descriptive) | 88 | 46 | 39 |
| state | collecting (descriptive) | 351 | 253 | 251 |
| paired | collecting (descriptive) | 1404 | 1310 | 1305 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.114472 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00398566 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00162132 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000909962 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.76% | 13.23% | 65.18% | 4.13% | 107.91 | 508.442 |
| ordinary/B2_10 | -4.24% | 14.40% | 64.90% | 4.63% | 89.7591 | 467.869 |
| ordinary/VOL_05 | -2.92% | 18.17% | 44.07% | 3.74% | 18.1173 | 78.3691 |
| ordinary/VOL_10 | -2.77% | 16.71% | 45.44% | 3.54% | 15.1849 | 65.5761 |
| stressed/B2_05 | -4.13% | 13.16% | 65.19% | 4.40% | 107.916 | 887.257 |
| stressed/B2_10 | -4.55% | 14.32% | 64.92% | 4.84% | 89.7551 | 782.71 |
| stressed/VOL_05 | -2.98% | 18.13% | 44.08% | 3.75% | 18.1278 | 142.3 |
| stressed/VOL_10 | -2.82% | 16.69% | 45.46% | 3.54% | 15.2033 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 74.36% | 0.0291518 |
| calibrated | 71.79% | 0.0232982 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1305 | 803 | 502 | 48.44% |
| 60m | perp_synchronized_clock | 1305 | 803 | 502 | 48.44% |
| 60m | combined_synchronized_clock | 1305 | 796 | 509 | 48.62% |
| 15m | perp_original_clock | 1305 | 803 | 502 | 46.95% |
| 15m | perp_synchronized_clock | 1305 | 803 | 502 | 46.95% |
| 15m | combined_synchronized_clock | 1305 | 796 | 509 | 46.36% |

## Data usability pilots

- Options: 351 captures; usable 7d RR25 in 296, usable 30d RR25 in 86; 272 valid hourly changes.
- Liquidations: 940 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1306}`.
- Exchange stress: 702/702 scheduled records. Capture states: `{"missed": 43, "ok": 659}`. Ratings: `{"low": 659}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
