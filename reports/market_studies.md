# Market studies

Generated 2026-10-30T03:49:00.792Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 32 | 30 | 30 |
| range | collecting (descriptive) | 32 | 24 | 18 |
| state | collecting (descriptive) | 130 | 89 | 87 |
| paired | collecting (descriptive) | 520 | 434 | 428 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.818795 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00289758 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00389853 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000876168 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.36% | 16.48% | 46.14% | 1.69% | 145.452 | 224.563 |
| ordinary/B2_10 | -1.80% | 18.30% | 47.11% | 2.15% | 88.886 | 137.307 |
| ordinary/VOL_05 | -2.01% | 23.16% | 49.03% | 2.69% | 37.8704 | 58.5665 |
| ordinary/VOL_10 | -1.78% | 20.93% | 47.54% | 2.40% | 33.768 | 52.2225 |
| stressed/B2_05 | -1.54% | 16.44% | 46.14% | 1.82% | 145.534 | 408.054 |
| stressed/B2_10 | -1.92% | 18.21% | 47.12% | 2.21% | 88.9552 | 249.621 |
| stressed/VOL_05 | -2.06% | 23.12% | 49.05% | 2.69% | 37.9043 | 106.48 |
| stressed/VOL_10 | -1.83% | 20.90% | 47.56% | 2.40% | 33.8124 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 88.89% | 0.0321734 |
| calibrated | 88.89% | 0.0256513 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 428 | 260 | 168 | 50.77% |
| 60m | perp_synchronized_clock | 428 | 260 | 168 | 50.77% |
| 60m | combined_synchronized_clock | 428 | 262 | 166 | 51.15% |
| 15m | perp_original_clock | 428 | 260 | 168 | 45.00% |
| 15m | perp_synchronized_clock | 428 | 260 | 168 | 45.00% |
| 15m | combined_synchronized_clock | 428 | 262 | 166 | 45.42% |

## Data usability pilots

- Options: 130 captures; usable 7d RR25 in 107, usable 30d RR25 in 86; 99 valid hourly changes.
- Liquidations: 292 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 433}`.
- Exchange stress: 260/260 scheduled records. Capture states: `{"missed": 39, "ok": 221}`. Ratings: `{"low": 221}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
