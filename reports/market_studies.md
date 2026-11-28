# Market studies

Generated 2026-11-28T16:54:24.062Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 210 | 173 | 173 |
| range | collecting (descriptive) | 210 | 165 | 158 |
| state | collecting (descriptive) | 839 | 406 | 405 |
| paired | collecting (descriptive) | 3356 | 3258 | 3253 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.367148 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00360064 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00120929 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00180603 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -12.29% | 15.77% | 44.02% | 13.92% | 85.4451 | 1037.29 |
| ordinary/B2_10 | -11.90% | 14.42% | 42.64% | 13.13% | 54.5251 | 836.707 |
| ordinary/VOL_05 | -10.10% | 16.41% | 34.66% | 11.99% | 9.89586 | 98.0562 |
| ordinary/VOL_10 | -9.84% | 16.81% | 36.55% | 11.91% | 6.61208 | 65.5761 |
| stressed/B2_05 | -12.92% | 15.78% | 44.02% | 14.39% | 85.5378 | 1712.8 |
| stressed/B2_10 | -12.30% | 14.40% | 42.65% | 13.45% | 54.5944 | 1268.57 |
| stressed/VOL_05 | -10.17% | 16.40% | 34.67% | 12.02% | 9.90167 | 178.068 |
| stressed/VOL_10 | -9.89% | 16.80% | 36.56% | 11.93% | 6.62065 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.62% | 0.0405021 |
| calibrated | 72.15% | 0.0449961 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3253 | 1831 | 1422 | 48.55% |
| 60m | perp_synchronized_clock | 3253 | 1831 | 1422 | 48.55% |
| 60m | combined_synchronized_clock | 3253 | 1793 | 1460 | 48.91% |
| 15m | perp_original_clock | 3253 | 1831 | 1422 | 48.77% |
| 15m | perp_synchronized_clock | 3253 | 1831 | 1422 | 48.77% |
| 15m | combined_synchronized_clock | 3253 | 1793 | 1460 | 47.80% |

## Data usability pilots

- Options: 838 captures; usable 7d RR25 in 727, usable 30d RR25 in 413; 662 valid hourly changes.
- Liquidations: 2394 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3247}`.
- Exchange stress: 1678/1678 scheduled records. Capture states: `{"missed": 45, "ok": 1633}`. Ratings: `{"low": 1633}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
