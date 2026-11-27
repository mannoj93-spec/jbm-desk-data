# Market studies

Generated 2026-11-27T16:18:15.760Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 204 | 166 | 166 |
| range | collecting (descriptive) | 204 | 158 | 152 |
| state | collecting (descriptive) | 815 | 401 | 399 |
| paired | collecting (descriptive) | 3258 | 3160 | 3155 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.356269 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00291294 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000882857 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00176307 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.38% | 15.91% | 44.42% | 13.92% | 84.4831 | 1002.09 |
| ordinary/B2_10 | -11.03% | 14.53% | 42.95% | 13.13% | 54.0198 | 815.177 |
| ordinary/VOL_05 | -9.28% | 16.58% | 35.02% | 11.99% | 10.22 | 98.0562 |
| ordinary/VOL_10 | -8.88% | 16.92% | 36.82% | 11.91% | 6.82876 | 65.5761 |
| stressed/B2_05 | -11.99% | 15.92% | 44.43% | 14.39% | 84.5776 | 1649.22 |
| stressed/B2_10 | -11.41% | 14.51% | 42.96% | 13.45% | 54.0895 | 1229.59 |
| stressed/VOL_05 | -9.36% | 16.57% | 35.02% | 12.02% | 10.2259 | 178.068 |
| stressed/VOL_10 | -8.93% | 16.91% | 36.83% | 11.93% | 6.83761 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.42% | 0.0402572 |
| calibrated | 71.05% | 0.0440988 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 3155 | 1775 | 1380 | 48.34% |
| 60m | perp_synchronized_clock | 3155 | 1775 | 1380 | 48.34% |
| 60m | combined_synchronized_clock | 3155 | 1738 | 1417 | 48.68% |
| 15m | perp_original_clock | 3155 | 1775 | 1380 | 48.62% |
| 15m | perp_synchronized_clock | 3155 | 1775 | 1380 | 48.62% |
| 15m | combined_synchronized_clock | 3155 | 1738 | 1417 | 47.64% |

## Data usability pilots

- Options: 814 captures; usable 7d RR25 in 703, usable 30d RR25 in 413; 640 valid hourly changes.
- Liquidations: 2322 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 3151}`.
- Exchange stress: 1629/1629 scheduled records. Capture states: `{"missed": 45, "ok": 1584}`. Ratings: `{"low": 1584}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
