# Market studies

Generated 2026-10-27T16:21:26.825Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 18 | 16 | 16 |
| range | collecting (descriptive) | 18 | 10 | 3 |
| state | collecting (descriptive) | 71 | 44 | 40 |
| paired | collecting (descriptive) | 282 | 196 | 191 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.12235 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00643804 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00383427 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0107984 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.06% | 10.48% | 48.52% | 0.84% | 141.34 | 118.904 |
| ordinary/B2_10 | -0.00% | 10.19% | 48.75% | 0.77% | 89.0846 | 74.9863 |
| ordinary/VOL_05 | 0.09% | 9.68% | 47.47% | 0.67% | 62.0215 | 52.2225 |
| ordinary/VOL_10 | 0.09% | 9.68% | 47.47% | 0.67% | 62.0215 | 52.2225 |
| stressed/B2_05 | -0.15% | 10.42% | 48.52% | 0.88% | 141.498 | 216.219 |
| stressed/B2_10 | -0.06% | 10.04% | 48.77% | 0.78% | 89.2102 | 136.413 |
| stressed/VOL_05 | 0.05% | 9.56% | 47.49% | 0.67% | 62.1021 | 94.9864 |
| stressed/VOL_10 | 0.05% | 9.56% | 47.49% | 0.67% | 62.1021 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 100.00% | 0.0323007 |
| calibrated | 100.00% | 0.0258626 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 191 | 117 | 74 | 52.99% |
| 60m | perp_synchronized_clock | 191 | 117 | 74 | 52.99% |
| 60m | combined_synchronized_clock | 191 | 122 | 69 | 50.00% |
| 15m | perp_original_clock | 191 | 117 | 74 | 47.01% |
| 15m | perp_synchronized_clock | 191 | 117 | 74 | 47.01% |
| 15m | combined_synchronized_clock | 191 | 122 | 69 | 45.08% |

## Data usability pilots

- Options: 71 captures; usable 7d RR25 in 66, usable 30d RR25 in 71; 62 valid hourly changes.
- Liquidations: 115 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 197}`.
- Exchange stress: 141/141 scheduled records. Capture states: `{"missed": 39, "ok": 102}`. Ratings: `{"low": 102}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
