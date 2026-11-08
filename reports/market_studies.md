# Market studies

Generated 2026-11-08T14:54:31.050Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 89 | 53 | 53 |
| range | collecting (descriptive) | 89 | 47 | 41 |
| state | collecting (descriptive) | 357 | 259 | 255 |
| paired | collecting (descriptive) | 1428 | 1334 | 1329 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.101007 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00362676 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00178802 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000940557 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.71% | 13.12% | 65.31% | 4.13% | 108.953 | 518.09 |
| ordinary/B2_10 | -4.19% | 14.28% | 64.93% | 4.63% | 88.7909 | 467.869 |
| ordinary/VOL_05 | -2.89% | 17.99% | 43.95% | 3.74% | 17.9182 | 78.3691 |
| ordinary/VOL_10 | -2.74% | 16.55% | 45.31% | 3.54% | 15.0178 | 65.5761 |
| stressed/B2_05 | -4.09% | 13.05% | 65.31% | 4.40% | 108.956 | 904.701 |
| stressed/B2_10 | -4.50% | 14.19% | 64.94% | 4.84% | 88.7903 | 782.71 |
| stressed/VOL_05 | -2.95% | 17.95% | 43.96% | 3.75% | 17.9286 | 142.3 |
| stressed/VOL_10 | -2.80% | 16.53% | 45.33% | 3.54% | 15.0361 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.17% | 0.0286514 |
| calibrated | 70.73% | 0.0229035 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1329 | 821 | 508 | 48.11% |
| 60m | perp_synchronized_clock | 1329 | 821 | 508 | 48.11% |
| 60m | combined_synchronized_clock | 1329 | 817 | 512 | 48.35% |
| 15m | perp_original_clock | 1329 | 821 | 508 | 46.77% |
| 15m | perp_synchronized_clock | 1329 | 821 | 508 | 46.77% |
| 15m | combined_synchronized_clock | 1329 | 817 | 512 | 46.27% |

## Data usability pilots

- Options: 357 captures; usable 7d RR25 in 302, usable 30d RR25 in 86; 278 valid hourly changes.
- Liquidations: 958 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1330}`.
- Exchange stress: 714/714 scheduled records. Capture states: `{"missed": 43, "ok": 671}`. Ratings: `{"low": 671}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
