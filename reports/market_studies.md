# Market studies

Generated 2026-11-09T14:47:06.976Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 95 | 59 | 59 |
| range | collecting (descriptive) | 95 | 53 | 47 |
| state | collecting (descriptive) | 381 | 273 | 271 |
| paired | collecting (descriptive) | 1524 | 1430 | 1425 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0871516 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00541707 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000502573 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00127193 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.89% | 13.84% | 64.44% | 5.43% | 112.46 | 693.946 |
| ordinary/B2_10 | -5.39% | 14.86% | 63.92% | 5.95% | 91.4425 | 645.645 |
| ordinary/VOL_05 | -3.44% | 17.48% | 43.28% | 4.35% | 16.808 | 78.3691 |
| ordinary/VOL_10 | -3.30% | 16.15% | 44.54% | 4.14% | 14.0864 | 65.5761 |
| stressed/B2_05 | -5.31% | 13.80% | 64.45% | 5.78% | 112.46 | 1118.12 |
| stressed/B2_10 | -5.73% | 14.79% | 63.94% | 6.23% | 91.4424 | 990.266 |
| stressed/VOL_05 | -3.51% | 17.44% | 43.28% | 4.36% | 16.818 | 142.3 |
| stressed/VOL_10 | -3.35% | 16.13% | 44.56% | 4.15% | 14.1037 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 63.83% | 0.0279269 |
| calibrated | 61.70% | 0.0225003 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1425 | 884 | 541 | 48.19% |
| 60m | perp_synchronized_clock | 1425 | 884 | 541 | 48.19% |
| 60m | combined_synchronized_clock | 1425 | 875 | 550 | 48.46% |
| 15m | perp_original_clock | 1425 | 884 | 541 | 46.95% |
| 15m | perp_synchronized_clock | 1425 | 884 | 541 | 46.95% |
| 15m | combined_synchronized_clock | 1425 | 875 | 550 | 46.29% |

## Data usability pilots

- Options: 381 captures; usable 7d RR25 in 326, usable 30d RR25 in 86; 302 valid hourly changes.
- Liquidations: 1023 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1419}`.
- Exchange stress: 762/762 scheduled records. Capture states: `{"missed": 43, "ok": 719}`. Ratings: `{"low": 719}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
