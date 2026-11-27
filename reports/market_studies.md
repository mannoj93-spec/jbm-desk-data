# Market studies

Generated 2026-11-27T19:34:27.804Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 204 | 167 | 167 |
| range | collecting (descriptive) | 204 | 159 | 153 |
| state | collecting (descriptive) | 818 | 402 | 401 |
| paired | collecting (descriptive) | 3271 | 3173 | 3168 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.34869 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00303188 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000750741 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00175584 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.95% | 16.00% | 44.32% | 13.92% | 84.0852 | 1002.09 |
| ordinary/B2_10 | -11.54% | 14.61% | 42.84% | 13.13% | 53.764 | 815.177 |
| ordinary/VOL_05 | -9.88% | 16.68% | 34.97% | 11.99% | 10.1713 | 98.0562 |
| ordinary/VOL_10 | -9.59% | 17.07% | 36.79% | 11.91% | 6.79615 | 65.5761 |
| stressed/B2_05 | -12.55% | 16.00% | 44.33% | 14.39% | 84.1804 | 1649.22 |
| stressed/B2_10 | -11.92% | 14.59% | 42.85% | 13.45% | 53.8338 | 1229.59 |
| stressed/VOL_05 | -9.96% | 16.67% | 34.97% | 12.02% | 10.1772 | 178.068 |
| stressed/VOL_10 | -9.64% | 17.07% | 36.80% | 11.93% | 6.80495 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.63% | 0.0403701 |
| calibrated | 71.24% | 0.0443245 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3168 | 1778 | 1390 | 48.37% |
| 60m | perp_synchronized_clock | 3168 | 1778 | 1390 | 48.37% |
| 60m | combined_synchronized_clock | 3168 | 1741 | 1427 | 48.71% |
| 15m | perp_original_clock | 3168 | 1778 | 1390 | 48.65% |
| 15m | perp_synchronized_clock | 3168 | 1778 | 1390 | 48.65% |
| 15m | combined_synchronized_clock | 3168 | 1741 | 1427 | 47.67% |

## Data usability pilots

- Options: 817 captures; usable 7d RR25 in 706, usable 30d RR25 in 413; 643 valid hourly changes.
- Liquidations: 2331 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3163}`.
- Exchange stress: 1636/1636 scheduled records. Capture states: `{"missed": 45, "ok": 1591}`. Ratings: `{"low": 1591}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
