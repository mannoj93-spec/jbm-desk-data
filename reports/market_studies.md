# Market studies

Generated 2026-10-27T16:01:39.796Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 18 | 15 | 15 |
| range | collecting (descriptive) | 18 | 9 | 3 |
| state | collecting (descriptive) | 71 | 44 | 40 |
| paired | collecting (descriptive) | 281 | 195 | 190 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.4271 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00643804 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00383427 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0108553 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.37% | 10.04% | 48.69% | 0.84% | 150.325 | 118.904 |
| ordinary/B2_10 | -0.29% | 9.85% | 49.13% | 0.77% | 94.7494 | 74.9863 |
| ordinary/VOL_05 | -0.23% | 9.12% | 47.48% | 0.67% | 65.9669 | 52.2225 |
| ordinary/VOL_10 | -0.23% | 9.12% | 47.48% | 0.67% | 65.9669 | 52.2225 |
| stressed/B2_05 | -0.46% | 9.94% | 48.69% | 0.88% | 150.491 | 216.219 |
| stressed/B2_10 | -0.35% | 9.65% | 49.15% | 0.78% | 94.8823 | 136.413 |
| stressed/VOL_05 | -0.27% | 8.97% | 47.50% | 0.67% | 66.0525 | 94.9864 |
| stressed/VOL_10 | -0.27% | 8.97% | 47.50% | 0.67% | 66.0525 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 100.00% | 0.0323007 |
| calibrated | 100.00% | 0.0258626 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 190 | 117 | 73 | 52.99% |
| 60m | perp_synchronized_clock | 190 | 117 | 73 | 52.99% |
| 60m | combined_synchronized_clock | 190 | 122 | 68 | 50.00% |
| 15m | perp_original_clock | 190 | 117 | 73 | 47.01% |
| 15m | perp_synchronized_clock | 190 | 117 | 73 | 47.01% |
| 15m | combined_synchronized_clock | 190 | 122 | 68 | 45.08% |

## Data usability pilots

- Options: 70 captures; usable 7d RR25 in 65, usable 30d RR25 in 70; 62 valid hourly changes.
- Liquidations: 115 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 197}`.
- Exchange stress: 141/141 scheduled records. Capture states: `{"missed": 39, "ok": 102}`. Ratings: `{"low": 102}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
