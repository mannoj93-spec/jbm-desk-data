# Market studies

Generated 2026-10-27T19:02:04.647Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 18 | 16 | 16 |
| range | collecting (descriptive) | 18 | 10 | 4 |
| state | collecting (descriptive) | 74 | 46 | 43 |
| paired | collecting (descriptive) | 293 | 207 | 202 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.12235 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00626232 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00099112 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0108292 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 75.00% | 0.0330439 |
| calibrated | 75.00% | 0.0266059 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 202 | 126 | 76 | 51.59% |
| 60m | perp_synchronized_clock | 202 | 126 | 76 | 51.59% |
| 60m | combined_synchronized_clock | 202 | 133 | 69 | 48.87% |
| 15m | perp_original_clock | 202 | 126 | 76 | 46.03% |
| 15m | perp_synchronized_clock | 202 | 126 | 76 | 46.03% |
| 15m | combined_synchronized_clock | 202 | 133 | 69 | 44.36% |

## Data usability pilots

- Options: 73 captures; usable 7d RR25 in 68, usable 30d RR25 in 73; 64 valid hourly changes.
- Liquidations: 124 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 209}`.
- Exchange stress: 147/147 scheduled records. Capture states: `{"missed": 39, "ok": 108}`. Ratings: `{"low": 108}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
