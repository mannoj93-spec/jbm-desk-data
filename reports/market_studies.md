# Market studies

Generated 2026-11-20T11:17:32.185Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 160 | 124 | 124 |
| range | collecting (descriptive) | 160 | 117 | 111 |
| state | collecting (descriptive) | 642 | 365 | 364 |
| paired | collecting (descriptive) | 2566 | 2468 | 2463 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.00424193 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00459976 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00071554 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000761267 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.15% | 14.50% | 50.09% | 11.49% | 92.3459 | 902.969 |
| ordinary/B2_10 | -10.97% | 14.12% | 48.87% | 11.33% | 67.5013 | 815.177 |
| ordinary/VOL_05 | -9.22% | 16.09% | 37.91% | 9.89% | 12.7908 | 98.0562 |
| ordinary/VOL_10 | -8.80% | 15.26% | 39.05% | 9.43% | 8.54796 | 65.5761 |
| stressed/B2_05 | -11.67% | 14.49% | 50.10% | 11.96% | 92.4286 | 1470.45 |
| stressed/B2_10 | -11.36% | 14.08% | 48.88% | 11.66% | 67.5632 | 1229.59 |
| stressed/VOL_05 | -9.29% | 16.08% | 37.92% | 9.92% | 12.7976 | 178.068 |
| stressed/VOL_10 | -8.85% | 15.25% | 39.06% | 9.44% | 8.55892 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.37% | 0.035771 |
| calibrated | 68.47% | 0.0349541 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2463 | 1444 | 1019 | 47.92% |
| 60m | perp_synchronized_clock | 2463 | 1444 | 1019 | 47.92% |
| 60m | combined_synchronized_clock | 2463 | 1422 | 1041 | 47.96% |
| 15m | perp_original_clock | 2463 | 1444 | 1019 | 48.34% |
| 15m | perp_synchronized_clock | 2463 | 1444 | 1019 | 48.34% |
| 15m | combined_synchronized_clock | 2463 | 1422 | 1041 | 47.33% |

## Data usability pilots

- Options: 642 captures; usable 7d RR25 in 541, usable 30d RR25 in 300; 490 valid hourly changes.
- Liquidations: 1806 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2463}`.
- Exchange stress: 1283/1283 scheduled records. Capture states: `{"missed": 45, "ok": 1238}`. Ratings: `{"low": 1238}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
