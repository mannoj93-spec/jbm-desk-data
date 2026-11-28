# Market studies

Generated 2026-11-28T05:17:57.020Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 207 | 170 | 170 |
| range | collecting (descriptive) | 207 | 162 | 156 |
| state | collecting (descriptive) | 828 | 404 | 402 |
| paired | collecting (descriptive) | 3310 | 3212 | 3207 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.346014 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00337785 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00084154 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00183193 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.90% | 15.87% | 44.09% | 13.92% | 85.9819 | 1031.31 |
| ordinary/B2_10 | -11.50% | 14.49% | 42.64% | 13.13% | 55.2686 | 836.707 |
| ordinary/VOL_05 | -9.87% | 16.54% | 34.81% | 11.99% | 10.0318 | 98.0562 |
| ordinary/VOL_10 | -9.57% | 16.93% | 36.67% | 11.91% | 6.7029 | 65.5761 |
| stressed/B2_05 | -12.53% | 15.87% | 44.10% | 14.39% | 86.0734 | 1701.99 |
| stressed/B2_10 | -11.90% | 14.47% | 42.64% | 13.45% | 55.3376 | 1268.57 |
| stressed/VOL_05 | -9.94% | 16.53% | 34.82% | 12.02% | 10.0376 | 178.068 |
| stressed/VOL_10 | -9.62% | 16.93% | 36.68% | 11.93% | 6.71158 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.23% | 0.0405478 |
| calibrated | 71.79% | 0.0448305 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3207 | 1804 | 1403 | 48.45% |
| 60m | perp_synchronized_clock | 3207 | 1804 | 1403 | 48.45% |
| 60m | combined_synchronized_clock | 3207 | 1766 | 1441 | 48.81% |
| 15m | perp_original_clock | 3207 | 1804 | 1403 | 48.78% |
| 15m | perp_synchronized_clock | 3207 | 1804 | 1403 | 48.78% |
| 15m | combined_synchronized_clock | 3207 | 1766 | 1441 | 47.79% |

## Data usability pilots

- Options: 827 captures; usable 7d RR25 in 716, usable 30d RR25 in 413; 651 valid hourly changes.
- Liquidations: 2361 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3203}`.
- Exchange stress: 1655/1655 scheduled records. Capture states: `{"missed": 45, "ok": 1610}`. Ratings: `{"low": 1610}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
