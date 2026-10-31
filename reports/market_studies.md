# Market studies

Generated 2026-10-31T09:16:23.585Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 40 | 38 | 38 |
| range | collecting (descriptive) | 40 | 32 | 26 |
| state | collecting (descriptive) | 160 | 112 | 107 |
| paired | collecting (descriptive) | 638 | 552 | 547 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.734098 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00808514 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00323243 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000799817 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.43% | 15.18% | 44.19% | 1.95% | 138.09 | 311.007 |
| ordinary/B2_10 | -1.86% | 16.60% | 43.99% | 2.36% | 93.7333 | 262.932 |
| ordinary/VOL_05 | -1.98% | 21.27% | 47.80% | 2.93% | 35.3859 | 68.8516 |
| ordinary/VOL_10 | -1.73% | 19.55% | 47.35% | 2.66% | 26.9025 | 52.2225 |
| stressed/B2_05 | -1.65% | 15.15% | 44.20% | 2.09% | 138.171 | 529.591 |
| stressed/B2_10 | -2.01% | 16.53% | 44.00% | 2.45% | 93.7953 | 411.339 |
| stressed/VOL_05 | -2.04% | 21.22% | 47.81% | 2.94% | 35.4105 | 125.006 |
| stressed/VOL_10 | -1.78% | 19.53% | 47.37% | 2.66% | 26.938 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 76.92% | 0.0331322 |
| calibrated | 73.08% | 0.0266241 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 547 | 328 | 219 | 54.27% |
| 60m | perp_synchronized_clock | 547 | 328 | 219 | 54.27% |
| 60m | combined_synchronized_clock | 547 | 325 | 222 | 54.46% |
| 15m | perp_original_clock | 547 | 328 | 219 | 47.87% |
| 15m | perp_synchronized_clock | 547 | 328 | 219 | 47.87% |
| 15m | combined_synchronized_clock | 547 | 325 | 222 | 47.69% |

## Data usability pilots

- Options: 160 captures; usable 7d RR25 in 137, usable 30d RR25 in 86; 129 valid hourly changes.
- Liquidations: 382 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 553}`.
- Exchange stress: 319/319 scheduled records. Capture states: `{"missed": 39, "ok": 280}`. Ratings: `{"low": 280}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
