# Market studies

Generated 2026-10-28T03:01:23.138Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 20 | 18 | 18 |
| range | collecting (descriptive) | 20 | 12 | 6 |
| state | collecting (descriptive) | 82 | 53 | 48 |
| paired | collecting (descriptive) | 325 | 239 | 234 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.947885 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00635542 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00066962 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0045406 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.02% | 9.86% | 48.76% | 0.84% | 137.459 | 129.407 |
| ordinary/B2_10 | 0.07% | 9.58% | 48.81% | 0.77% | 94.3471 | 88.8705 |
| ordinary/VOL_05 | 0.18% | 9.11% | 47.49% | 0.67% | 55.4188 | 52.2225 |
| ordinary/VOL_10 | 0.18% | 9.11% | 47.49% | 0.67% | 55.4188 | 52.2225 |
| stressed/B2_05 | -0.09% | 9.81% | 48.77% | 0.88% | 137.607 | 235.296 |
| stressed/B2_10 | -0.01% | 9.44% | 48.83% | 0.78% | 94.4665 | 161.642 |
| stressed/VOL_05 | 0.14% | 9.00% | 47.51% | 0.67% | 55.491 | 94.9864 |
| stressed/VOL_10 | 0.14% | 9.00% | 47.51% | 0.67% | 55.491 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 83.33% | 0.0329508 |
| calibrated | 83.33% | 0.0264782 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 234 | 146 | 88 | 50.00% |
| 60m | perp_synchronized_clock | 234 | 146 | 88 | 50.00% |
| 60m | combined_synchronized_clock | 234 | 151 | 83 | 49.01% |
| 15m | perp_original_clock | 234 | 146 | 88 | 47.95% |
| 15m | perp_synchronized_clock | 234 | 146 | 88 | 47.95% |
| 15m | combined_synchronized_clock | 234 | 151 | 83 | 47.68% |

## Data usability pilots

- Options: 81 captures; usable 7d RR25 in 76, usable 30d RR25 in 81; 72 valid hourly changes.
- Liquidations: 148 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 241}`.
- Exchange stress: 163/163 scheduled records. Capture states: `{"missed": 39, "ok": 124}`. Ratings: `{"low": 124}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
