# Market studies

Generated 2026-11-17T03:21:26.639Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 140 | 104 | 104 |
| range | collecting (descriptive) | 140 | 97 | 92 |
| state | collecting (descriptive) | 562 | 344 | 343 |
| paired | collecting (descriptive) | 2246 | 2148 | 2143 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0784263 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00373764 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000508254 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000408306 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.02% | 14.88% | 53.42% | 10.56% | 101.899 | 885.399 |
| ordinary/B2_10 | -10.13% | 14.78% | 52.73% | 10.65% | 76.4185 | 815.177 |
| ordinary/VOL_05 | -8.23% | 16.85% | 39.72% | 9.09% | 14.5025 | 98.0562 |
| ordinary/VOL_10 | -7.63% | 15.59% | 40.39% | 8.49% | 9.6974 | 65.5761 |
| stressed/B2_05 | -10.54% | 14.87% | 53.42% | 11.01% | 101.957 | 1438.78 |
| stressed/B2_10 | -10.52% | 14.74% | 52.74% | 10.98% | 76.4671 | 1229.59 |
| stressed/VOL_05 | -8.30% | 16.83% | 39.72% | 9.12% | 14.5098 | 178.068 |
| stressed/VOL_10 | -7.69% | 15.58% | 40.40% | 8.50% | 9.70974 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 63.04% | 0.0329825 |
| calibrated | 61.96% | 0.0301848 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2143 | 1271 | 872 | 48.31% |
| 60m | perp_synchronized_clock | 2143 | 1271 | 872 | 48.31% |
| 60m | combined_synchronized_clock | 2143 | 1257 | 886 | 48.29% |
| 15m | perp_original_clock | 2143 | 1271 | 872 | 48.07% |
| 15m | perp_synchronized_clock | 2143 | 1271 | 872 | 48.07% |
| 15m | combined_synchronized_clock | 2143 | 1257 | 886 | 47.10% |

## Data usability pilots

- Options: 562 captures; usable 7d RR25 in 482, usable 30d RR25 in 232; 440 valid hourly changes.
- Liquidations: 1566 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2143}`.
- Exchange stress: 1123/1123 scheduled records. Capture states: `{"missed": 45, "ok": 1078}`. Ratings: `{"low": 1078}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
