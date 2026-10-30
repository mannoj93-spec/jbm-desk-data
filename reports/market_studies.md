# Market studies

Generated 2026-10-30T16:01:55.820Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 36 | 33 | 33 |
| range | collecting (descriptive) | 36 | 27 | 21 |
| state | collecting (descriptive) | 143 | 98 | 94 |
| paired | collecting (descriptive) | 569 | 483 | 478 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.591656 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0058108 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00464693 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00143828 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.40% | 16.00% | 44.52% | 1.73% | 141.27 | 239.455 |
| ordinary/B2_10 | -1.79% | 17.64% | 45.18% | 2.15% | 90.3561 | 153.491 |
| ordinary/VOL_05 | -1.97% | 22.58% | 48.51% | 2.69% | 40.5218 | 68.8516 |
| ordinary/VOL_10 | -1.72% | 20.64% | 47.46% | 2.40% | 30.8161 | 52.2225 |
| stressed/B2_05 | -1.60% | 15.97% | 44.52% | 1.87% | 141.352 | 434.795 |
| stressed/B2_10 | -1.91% | 17.54% | 45.19% | 2.21% | 90.4147 | 278.561 |
| stressed/VOL_05 | -2.02% | 22.53% | 48.53% | 2.69% | 40.5493 | 125.006 |
| stressed/VOL_10 | -1.76% | 20.61% | 47.49% | 2.40% | 30.8566 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 76.19% | 0.0322933 |
| calibrated | 76.19% | 0.0257778 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 478 | 292 | 186 | 52.74% |
| 60m | perp_synchronized_clock | 478 | 292 | 186 | 52.74% |
| 60m | combined_synchronized_clock | 478 | 293 | 185 | 53.24% |
| 15m | perp_original_clock | 478 | 292 | 186 | 46.58% |
| 15m | perp_synchronized_clock | 478 | 292 | 186 | 46.58% |
| 15m | combined_synchronized_clock | 478 | 293 | 185 | 47.10% |

## Data usability pilots

- Options: 142 captures; usable 7d RR25 in 119, usable 30d RR25 in 86; 111 valid hourly changes.
- Liquidations: 331 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 485}`.
- Exchange stress: 285/285 scheduled records. Capture states: `{"missed": 39, "ok": 246}`. Ratings: `{"low": 246}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
