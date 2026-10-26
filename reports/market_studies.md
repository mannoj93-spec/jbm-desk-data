# Market studies

Generated 2026-10-26T19:17:13.328Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 12 | 10 | 10 |
| range | collecting (descriptive) | 12 | 4 | 0 |
| state | collecting (descriptive) | 50 | 27 | 24 |
| paired | collecting (descriptive) | 198 | 114 | 109 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.10651 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00372871 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.00573394 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.24% | 11.48% | 51.68% | 0.73% | 180.24 | 97.5299 |
| ordinary/B2_10 | -0.19% | 11.22% | 52.07% | 0.68% | 138.508 | 74.9863 |
| ordinary/VOL_05 | -0.12% | 9.82% | 47.52% | 0.57% | 96.4493 | 52.2225 |
| ordinary/VOL_10 | -0.12% | 9.82% | 47.52% | 0.57% | 96.4493 | 52.2225 |
| stressed/B2_05 | -0.32% | 11.25% | 51.69% | 0.75% | 180.473 | 177.395 |
| stressed/B2_10 | -0.25% | 10.95% | 52.09% | 0.69% | 138.695 | 136.413 |
| stressed/VOL_05 | -0.16% | 9.60% | 47.54% | 0.57% | 96.5729 | 94.9864 |
| stressed/VOL_10 | -0.16% | 9.60% | 47.54% | 0.57% | 96.5729 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 109 | 62 | 47 | 50.00% |
| 60m | perp_synchronized_clock | 109 | 62 | 47 | 50.00% |
| 60m | combined_synchronized_clock | 109 | 64 | 45 | 48.44% |
| 15m | perp_original_clock | 109 | 62 | 47 | 41.94% |
| 15m | perp_synchronized_clock | 109 | 62 | 47 | 41.94% |
| 15m | combined_synchronized_clock | 109 | 64 | 45 | 42.19% |

## Data usability pilots

- Options: 50 captures; usable 7d RR25 in 50, usable 30d RR25 in 50; 47 valid hourly changes.
- Liquidations: 52 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 113}`.
- Exchange stress: 99/99 scheduled records. Capture states: `{"missed": 39, "ok": 60}`. Ratings: `{"low": 60}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
