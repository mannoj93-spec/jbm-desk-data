# Market studies

Generated 2026-11-09T09:17:06.725Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 94 | 58 | 58 |
| range | collecting (descriptive) | 94 | 52 | 46 |
| state | collecting (descriptive) | 376 | 270 | 268 |
| paired | collecting (descriptive) | 1502 | 1408 | 1403 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0532976 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00492604 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00106663 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00106914 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.11% | 13.84% | 64.81% | 5.43% | 113.601 | 693.946 |
| ordinary/B2_10 | -5.61% | 14.88% | 64.28% | 5.95% | 92.3654 | 645.645 |
| ordinary/VOL_05 | -3.68% | 17.54% | 43.39% | 4.35% | 16.9822 | 78.3691 |
| ordinary/VOL_10 | -3.53% | 16.20% | 44.67% | 4.14% | 14.2326 | 65.5761 |
| stressed/B2_05 | -5.52% | 13.80% | 64.81% | 5.78% | 113.596 | 1118.12 |
| stressed/B2_10 | -5.95% | 14.80% | 64.29% | 6.23% | 92.362 | 990.266 |
| stressed/VOL_05 | -3.74% | 17.51% | 43.39% | 4.36% | 16.9923 | 142.3 |
| stressed/VOL_10 | -3.59% | 16.18% | 44.69% | 4.15% | 14.25 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.22% | 0.0280022 |
| calibrated | 63.04% | 0.0225229 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1403 | 872 | 531 | 48.17% |
| 60m | perp_synchronized_clock | 1403 | 872 | 531 | 48.17% |
| 60m | combined_synchronized_clock | 1403 | 864 | 539 | 48.38% |
| 15m | perp_original_clock | 1403 | 872 | 531 | 46.67% |
| 15m | perp_synchronized_clock | 1403 | 872 | 531 | 46.67% |
| 15m | combined_synchronized_clock | 1403 | 864 | 539 | 45.95% |

## Data usability pilots

- Options: 376 captures; usable 7d RR25 in 321, usable 30d RR25 in 86; 297 valid hourly changes.
- Liquidations: 1008 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1399}`.
- Exchange stress: 751/751 scheduled records. Capture states: `{"missed": 43, "ok": 708}`. Ratings: `{"low": 708}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
