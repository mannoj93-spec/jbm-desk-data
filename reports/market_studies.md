# Market studies

Generated 2026-11-17T14:47:27.470Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 143 | 107 | 107 |
| range | collecting (descriptive) | 143 | 100 | 95 |
| state | collecting (descriptive) | 573 | 348 | 346 |
| paired | collecting (descriptive) | 2292 | 2194 | 2189 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.124351 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00389949 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000726375 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000742348 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.89% | 14.76% | 52.91% | 10.56% | 100.701 | 890.73 |
| ordinary/B2_10 | -10.02% | 14.63% | 52.09% | 10.65% | 74.9318 | 815.177 |
| ordinary/VOL_05 | -8.10% | 16.67% | 39.42% | 9.09% | 14.2164 | 98.0562 |
| ordinary/VOL_10 | -7.49% | 15.45% | 40.17% | 8.49% | 9.50498 | 65.5761 |
| stressed/B2_05 | -10.41% | 14.75% | 52.92% | 11.01% | 100.763 | 1448.42 |
| stressed/B2_10 | -10.41% | 14.59% | 52.10% | 10.98% | 74.9831 | 1229.59 |
| stressed/VOL_05 | -8.18% | 16.65% | 39.42% | 9.12% | 14.2236 | 178.068 |
| stressed/VOL_10 | -7.54% | 15.43% | 40.18% | 8.50% | 9.51709 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.21% | 0.0334318 |
| calibrated | 63.16% | 0.0310023 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2189 | 1296 | 893 | 48.15% |
| 60m | perp_synchronized_clock | 2189 | 1296 | 893 | 48.15% |
| 60m | combined_synchronized_clock | 2189 | 1278 | 911 | 48.20% |
| 15m | perp_original_clock | 2189 | 1296 | 893 | 48.07% |
| 15m | perp_synchronized_clock | 2189 | 1296 | 893 | 48.07% |
| 15m | combined_synchronized_clock | 2189 | 1278 | 911 | 47.10% |

## Data usability pilots

- Options: 573 captures; usable 7d RR25 in 493, usable 30d RR25 in 243; 451 valid hourly changes.
- Liquidations: 1599 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2187}`.
- Exchange stress: 1146/1146 scheduled records. Capture states: `{"missed": 45, "ok": 1101}`. Ratings: `{"low": 1101}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
