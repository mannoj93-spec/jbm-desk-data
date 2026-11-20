# Market studies

Generated 2026-11-20T00:20:50.227Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 158 | 122 | 122 |
| range | collecting (descriptive) | 158 | 115 | 108 |
| state | collecting (descriptive) | 631 | 364 | 364 |
| paired | collecting (descriptive) | 2522 | 2424 | 2419 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0177473 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00448446 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00071554 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000697602 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.01% | 14.60% | 50.38% | 11.31% | 93.4236 | 902.969 |
| ordinary/B2_10 | -10.87% | 14.22% | 49.22% | 11.18% | 68.2931 | 815.177 |
| ordinary/VOL_05 | -9.09% | 16.21% | 38.08% | 9.72% | 12.9423 | 98.0562 |
| ordinary/VOL_10 | -8.65% | 15.37% | 39.17% | 9.23% | 8.64948 | 65.5761 |
| stressed/B2_05 | -11.54% | 14.59% | 50.39% | 11.78% | 93.504 | 1470.45 |
| stressed/B2_10 | -11.25% | 14.18% | 49.23% | 11.52% | 68.3541 | 1229.59 |
| stressed/VOL_05 | -9.17% | 16.20% | 38.08% | 9.75% | 12.9492 | 178.068 |
| stressed/VOL_10 | -8.71% | 15.36% | 39.19% | 9.24% | 8.66056 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.52% | 0.0353719 |
| calibrated | 67.59% | 0.0342892 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2419 | 1419 | 1000 | 47.92% |
| 60m | perp_synchronized_clock | 2419 | 1419 | 1000 | 47.92% |
| 60m | combined_synchronized_clock | 2419 | 1396 | 1023 | 47.92% |
| 15m | perp_original_clock | 2419 | 1419 | 1000 | 48.06% |
| 15m | perp_synchronized_clock | 2419 | 1419 | 1000 | 48.06% |
| 15m | combined_synchronized_clock | 2419 | 1396 | 1023 | 46.99% |

## Data usability pilots

- Options: 631 captures; usable 7d RR25 in 530, usable 30d RR25 in 293; 482 valid hourly changes.
- Liquidations: 1773 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2419}`.
- Exchange stress: 1261/1261 scheduled records. Capture states: `{"missed": 45, "ok": 1216}`. Ratings: `{"low": 1216}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
