# Market studies

Generated 2026-10-27T21:46:27.049Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 19 | 17 | 17 |
| range | collecting (descriptive) | 19 | 11 | 5 |
| state | collecting (descriptive) | 76 | 47 | 45 |
| paired | collecting (descriptive) | 304 | 218 | 213 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.05652 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00629747 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000992158 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00792254 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.03% | 10.18% | 48.38% | 0.84% | 133.377 | 118.904 |
| ordinary/B2_10 | 0.08% | 9.89% | 48.43% | 0.77% | 84.0658 | 74.9863 |
| ordinary/VOL_05 | 0.19% | 9.40% | 47.48% | 0.67% | 58.5251 | 52.2225 |
| ordinary/VOL_10 | 0.19% | 9.40% | 47.48% | 0.67% | 58.5251 | 52.2225 |
| stressed/B2_05 | -0.07% | 10.13% | 48.38% | 0.88% | 133.528 | 216.219 |
| stressed/B2_10 | 0.02% | 9.75% | 48.44% | 0.78% | 84.1848 | 136.413 |
| stressed/VOL_05 | 0.14% | 9.29% | 47.50% | 0.67% | 58.6013 | 94.9864 |
| stressed/VOL_10 | 0.14% | 9.29% | 47.50% | 0.67% | 58.6013 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 80.00% | 0.0331598 |
| calibrated | 80.00% | 0.0267218 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 213 | 132 | 81 | 50.76% |
| 60m | perp_synchronized_clock | 213 | 132 | 81 | 50.76% |
| 60m | combined_synchronized_clock | 213 | 139 | 74 | 48.92% |
| 15m | perp_original_clock | 213 | 132 | 81 | 46.21% |
| 15m | perp_synchronized_clock | 213 | 132 | 81 | 46.21% |
| 15m | combined_synchronized_clock | 213 | 139 | 74 | 45.32% |

## Data usability pilots

- Options: 76 captures; usable 7d RR25 in 71, usable 30d RR25 in 76; 67 valid hourly changes.
- Liquidations: 130 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 217}`.
- Exchange stress: 152/152 scheduled records. Capture states: `{"missed": 39, "ok": 113}`. Ratings: `{"low": 113}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
