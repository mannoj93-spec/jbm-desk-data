# Market studies

Generated 2026-10-27T06:02:06.063Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 15 | 13 | 13 |
| range | collecting (descriptive) | 15 | 7 | 1 |
| state | collecting (descriptive) | 61 | 37 | 32 |
| paired | collecting (descriptive) | 241 | 155 | 150 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.65401 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00643804 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00283408 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0125 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.51% | 10.71% | 49.11% | 0.84% | 172.446 | 118.904 |
| ordinary/B2_10 | -0.42% | 10.53% | 50.08% | 0.77% | 108.697 | 74.9863 |
| ordinary/VOL_05 | -0.37% | 9.72% | 47.50% | 0.67% | 75.6805 | 52.2225 |
| ordinary/VOL_10 | -0.37% | 9.72% | 47.50% | 0.67% | 75.6805 | 52.2225 |
| stressed/B2_05 | -0.61% | 10.57% | 49.12% | 0.88% | 172.628 | 216.219 |
| stressed/B2_10 | -0.48% | 10.30% | 50.09% | 0.78% | 108.848 | 136.413 |
| stressed/VOL_05 | -0.42% | 9.54% | 47.52% | 0.67% | 75.7783 | 94.9864 |
| stressed/VOL_10 | -0.42% | 9.54% | 47.52% | 0.67% | 75.7783 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 100.00% | 0.0326025 |
| calibrated | 100.00% | 0.0261645 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 150 | 85 | 65 | 50.59% |
| 60m | perp_synchronized_clock | 150 | 85 | 65 | 50.59% |
| 60m | combined_synchronized_clock | 150 | 91 | 59 | 47.25% |
| 15m | perp_original_clock | 150 | 85 | 65 | 41.18% |
| 15m | perp_synchronized_clock | 150 | 85 | 65 | 41.18% |
| 15m | combined_synchronized_clock | 150 | 91 | 59 | 39.56% |

## Data usability pilots

- Options: 60 captures; usable 7d RR25 in 60, usable 30d RR25 in 60; 57 valid hourly changes.
- Liquidations: 85 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 157}`.
- Exchange stress: 121/121 scheduled records. Capture states: `{"missed": 39, "ok": 82}`. Ratings: `{"low": 82}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
