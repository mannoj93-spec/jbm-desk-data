# Market studies

Generated 2026-11-08T16:19:25.330Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 90 | 54 | 54 |
| range | collecting (descriptive) | 90 | 48 | 41 |
| state | collecting (descriptive) | 359 | 260 | 256 |
| paired | collecting (descriptive) | 1434 | 1340 | 1334 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.138837 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00362676 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00178199 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000937031 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.62% | 13.02% | 65.43% | 4.13% | 107.775 | 518.09 |
| ordinary/B2_10 | -4.11% | 14.17% | 64.96% | 4.63% | 87.8359 | 467.869 |
| ordinary/VOL_05 | -2.85% | 17.83% | 43.84% | 3.74% | 17.722 | 78.3691 |
| ordinary/VOL_10 | -2.70% | 16.40% | 45.18% | 3.54% | 14.8532 | 65.5761 |
| stressed/B2_05 | -4.00% | 12.96% | 65.44% | 4.40% | 107.782 | 904.701 |
| stressed/B2_10 | -4.42% | 14.08% | 64.97% | 4.84% | 87.8385 | 782.71 |
| stressed/VOL_05 | -2.91% | 17.79% | 43.84% | 3.75% | 17.7324 | 142.3 |
| stressed/VOL_10 | -2.76% | 16.38% | 45.19% | 3.54% | 14.8714 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.17% | 0.0286514 |
| calibrated | 70.73% | 0.0229035 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1334 | 825 | 509 | 48.12% |
| 60m | perp_synchronized_clock | 1334 | 825 | 509 | 48.12% |
| 60m | combined_synchronized_clock | 1334 | 821 | 513 | 48.36% |
| 15m | perp_original_clock | 1334 | 825 | 509 | 46.67% |
| 15m | perp_synchronized_clock | 1334 | 825 | 509 | 46.67% |
| 15m | combined_synchronized_clock | 1334 | 821 | 513 | 46.16% |

## Data usability pilots

- Options: 359 captures; usable 7d RR25 in 304, usable 30d RR25 in 86; 280 valid hourly changes.
- Liquidations: 964 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 3, "missed": 66, "ok": 1338}`.
- Exchange stress: 717/717 scheduled records. Capture states: `{"missed": 43, "ok": 674}`. Ratings: `{"low": 674}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
