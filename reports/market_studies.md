# Market studies

Generated 2026-11-07T04:46:28.818Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 81 | 45 | 45 |
| range | collecting (descriptive) | 81 | 39 | 35 |
| state | collecting (descriptive) | 323 | 228 | 224 |
| paired | collecting (descriptive) | 1292 | 1198 | 1193 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0337256 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000604592 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00104778 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.70% | 14.01% | 64.23% | 4.07% | 98.7432 | 436.224 |
| ordinary/B2_10 | -4.13% | 15.29% | 63.97% | 4.52% | 79.0976 | 395.988 |
| ordinary/VOL_05 | -2.92% | 19.54% | 44.99% | 3.74% | 19.6472 | 78.3691 |
| ordinary/VOL_10 | -2.77% | 17.96% | 46.49% | 3.54% | 16.4688 | 65.5761 |
| stressed/B2_05 | -4.01% | 13.95% | 64.23% | 4.28% | 98.7566 | 756.422 |
| stressed/B2_10 | -4.38% | 15.20% | 63.98% | 4.67% | 79.1037 | 652.399 |
| stressed/VOL_05 | -2.98% | 19.49% | 45.00% | 3.75% | 19.6582 | 142.3 |
| stressed/VOL_10 | -2.83% | 17.94% | 46.51% | 3.54% | 16.4885 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1193 | 724 | 469 | 48.90% |
| 60m | perp_synchronized_clock | 1193 | 724 | 469 | 48.90% |
| 60m | combined_synchronized_clock | 1193 | 712 | 481 | 49.02% |
| 15m | perp_original_clock | 1193 | 724 | 469 | 46.69% |
| 15m | perp_synchronized_clock | 1193 | 724 | 469 | 46.69% |
| 15m | combined_synchronized_clock | 1193 | 712 | 481 | 46.21% |

## Data usability pilots

- Options: 323 captures; usable 7d RR25 in 268, usable 30d RR25 in 86; 244 valid hourly changes.
- Liquidations: 857 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1195}`.
- Exchange stress: 646/646 scheduled records. Capture states: `{"missed": 43, "ok": 603}`. Ratings: `{"low": 603}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
