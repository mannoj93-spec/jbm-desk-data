# Market studies

Generated 2026-11-18T04:03:37.407Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 147 | 110 | 110 |
| range | collecting (descriptive) | 147 | 103 | 97 |
| state | collecting (descriptive) | 587 | 352 | 349 |
| paired | collecting (descriptive) | 2345 | 2247 | 2242 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0468161 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00400067 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000399359 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000724799 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.98% | 14.71% | 52.33% | 10.57% | 99.7359 | 897.363 |
| ordinary/B2_10 | -10.03% | 14.56% | 51.47% | 10.65% | 73.5021 | 815.177 |
| ordinary/VOL_05 | -8.11% | 16.58% | 39.13% | 9.09% | 13.9415 | 98.0562 |
| ordinary/VOL_10 | -7.50% | 15.45% | 39.96% | 8.49% | 9.32024 | 65.5761 |
| stressed/B2_05 | -10.50% | 14.70% | 52.33% | 11.04% | 99.8004 | 1460.41 |
| stressed/B2_10 | -10.42% | 14.52% | 51.48% | 10.98% | 73.5557 | 1229.59 |
| stressed/VOL_05 | -8.19% | 16.57% | 39.14% | 9.12% | 13.9487 | 178.068 |
| stressed/VOL_10 | -7.55% | 15.44% | 39.97% | 8.50% | 9.33213 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.95% | 0.0337447 |
| calibrated | 63.92% | 0.0315469 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2242 | 1332 | 910 | 48.27% |
| 60m | perp_synchronized_clock | 2242 | 1332 | 910 | 48.27% |
| 60m | combined_synchronized_clock | 2242 | 1314 | 928 | 48.33% |
| 15m | perp_original_clock | 2242 | 1332 | 910 | 47.90% |
| 15m | perp_synchronized_clock | 2242 | 1332 | 910 | 47.90% |
| 15m | combined_synchronized_clock | 2242 | 1314 | 928 | 46.96% |

## Data usability pilots

- Options: 586 captures; usable 7d RR25 in 500, usable 30d RR25 in 256; 456 valid hourly changes.
- Liquidations: 1641 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2243}`.
- Exchange stress: 1173/1173 scheduled records. Capture states: `{"missed": 45, "ok": 1128}`. Ratings: `{"low": 1128}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
