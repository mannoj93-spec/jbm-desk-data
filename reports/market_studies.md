# Market studies

Generated 2026-10-25T04:50:22.038Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 3 | 3 | 3 |
| range | registered; not launched | 3 | 0 | 0 |
| state | collecting (descriptive) | 11 | 5 | 4 |
| paired | collecting (descriptive) | 44 | 17 | 13 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 62.1115 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.0228892 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.33% | 4.14% | 53.02% | 0.00% | 703.415 | 67.4545 |
| ordinary/B2_10 | 0.35% | 3.49% | 55.63% | 0.00% | 637.101 | 61.0952 |
| ordinary/VOL_05 | 0.30% | 2.99% | 47.55% | 0.00% | 544.672 | 52.2225 |
| ordinary/VOL_10 | 0.30% | 2.99% | 47.55% | 0.00% | 544.672 | 52.2225 |
| stressed/B2_05 | 0.28% | 2.80% | 53.04% | 0.00% | 704.391 | 122.732 |
| stressed/B2_10 | 0.30% | 1.95% | 55.66% | 0.00% | 637.834 | 111.125 |
| stressed/VOL_05 | 0.26% | 1.67% | 47.57% | 0.00% | 545.279 | 94.9864 |
| stressed/VOL_10 | 0.26% | 1.67% | 47.57% | 0.00% | 545.279 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 13 | 9 | 4 | 44.44% |
| 60m | perp_synchronized_clock | 13 | 9 | 4 | 44.44% |
| 60m | combined_synchronized_clock | 13 | 9 | 4 | 44.44% |
| 15m | perp_original_clock | 13 | 9 | 4 | 44.44% |
| 15m | perp_synchronized_clock | 13 | 9 | 4 | 44.44% |
| 15m | combined_synchronized_clock | 13 | 9 | 4 | 44.44% |

## Data usability pilots

- Options: 11 captures; usable 7d RR25 in 11, usable 30d RR25 in 11; 10 valid hourly changes.
- Liquidations: 4 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 12, "ok": 11}`.
- Exchange stress: 22/22 scheduled records. Capture states: `{"missed": 13, "ok": 9}`. Ratings: `{"low": 9}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
