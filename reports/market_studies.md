# Market studies

Generated 2026-11-28T12:47:43.918Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 209 | 172 | 172 |
| range | collecting (descriptive) | 209 | 164 | 158 |
| state | collecting (descriptive) | 835 | 405 | 404 |
| paired | collecting (descriptive) | 3340 | 3242 | 3237 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.389828 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00360064 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00086607 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00181495 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.38% | 15.81% | 44.05% | 13.92% | 85.8193 | 1037.29 |
| ordinary/B2_10 | -12.01% | 14.45% | 42.64% | 13.13% | 54.7652 | 836.707 |
| ordinary/VOL_05 | -10.16% | 16.45% | 34.71% | 11.99% | 9.93981 | 98.0562 |
| ordinary/VOL_10 | -9.91% | 16.85% | 36.59% | 11.91% | 6.64144 | 65.5761 |
| stressed/B2_05 | -13.01% | 15.82% | 44.06% | 14.39% | 85.9112 | 1712.8 |
| stressed/B2_10 | -12.41% | 14.43% | 42.65% | 13.45% | 54.8344 | 1268.57 |
| stressed/VOL_05 | -10.23% | 16.44% | 34.72% | 12.02% | 9.94564 | 178.068 |
| stressed/VOL_10 | -9.96% | 16.84% | 36.60% | 11.93% | 6.65005 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.62% | 0.0405021 |
| calibrated | 72.15% | 0.0449961 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3237 | 1821 | 1416 | 48.49% |
| 60m | perp_synchronized_clock | 3237 | 1821 | 1416 | 48.49% |
| 60m | combined_synchronized_clock | 3237 | 1783 | 1454 | 48.85% |
| 15m | perp_original_clock | 3237 | 1821 | 1416 | 48.82% |
| 15m | perp_synchronized_clock | 3237 | 1821 | 1416 | 48.82% |
| 15m | combined_synchronized_clock | 3237 | 1783 | 1454 | 47.84% |

## Data usability pilots

- Options: 834 captures; usable 7d RR25 in 723, usable 30d RR25 in 413; 658 valid hourly changes.
- Liquidations: 2382 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3231}`.
- Exchange stress: 1670/1670 scheduled records. Capture states: `{"missed": 45, "ok": 1625}`. Ratings: `{"low": 1625}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
