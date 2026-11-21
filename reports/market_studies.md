# Market studies

Generated 2026-11-21T17:32:41.696Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 168 | 131 | 131 |
| range | collecting (descriptive) | 168 | 124 | 118 |
| state | collecting (descriptive) | 672 | 370 | 369 |
| paired | collecting (descriptive) | 2687 | 2589 | 2584 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.233693 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00145566 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.0015057 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000604683 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.20% | 16.54% | 48.85% | 13.92% | 91.5053 | 928.525 |
| ordinary/B2_10 | -11.57% | 15.17% | 47.52% | 13.13% | 64.505 | 815.177 |
| ordinary/VOL_05 | -9.92% | 17.34% | 37.24% | 11.99% | 12.2193 | 98.0562 |
| ordinary/VOL_10 | -9.64% | 17.25% | 38.53% | 11.91% | 8.16613 | 65.5761 |
| stressed/B2_05 | -12.74% | 16.55% | 48.85% | 14.39% | 91.5879 | 1516.64 |
| stressed/B2_10 | -11.96% | 15.14% | 47.53% | 13.45% | 64.5692 | 1229.59 |
| stressed/VOL_05 | -10.00% | 17.33% | 37.25% | 12.02% | 12.226 | 178.068 |
| stressed/VOL_10 | -9.69% | 17.24% | 38.54% | 11.93% | 8.17662 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.10% | 0.0363473 |
| calibrated | 67.80% | 0.036098 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2584 | 1491 | 1093 | 48.22% |
| 60m | perp_synchronized_clock | 2584 | 1491 | 1093 | 48.22% |
| 60m | combined_synchronized_clock | 2584 | 1470 | 1114 | 48.23% |
| 15m | perp_original_clock | 2584 | 1491 | 1093 | 48.76% |
| 15m | perp_synchronized_clock | 2584 | 1491 | 1093 | 48.76% |
| 15m | combined_synchronized_clock | 2584 | 1470 | 1114 | 47.82% |

## Data usability pilots

- Options: 671 captures; usable 7d RR25 in 568, usable 30d RR25 in 327; 515 valid hourly changes.
- Liquidations: 1893 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2579}`.
- Exchange stress: 1344/1344 scheduled records. Capture states: `{"missed": 45, "ok": 1299}`. Ratings: `{"low": 1299}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
