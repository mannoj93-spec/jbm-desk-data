# Market studies

Generated 2026-11-10T04:02:01.730Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 99 | 62 | 62 |
| range | collecting (descriptive) | 99 | 56 | 50 |
| state | collecting (descriptive) | 395 | 279 | 276 |
| paired | collecting (descriptive) | 1577 | 1483 | 1478 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.115125 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00512685 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000112768 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000507442 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.70% | 13.59% | 63.41% | 5.43% | 109.149 | 693.946 |
| ordinary/B2_10 | -5.20% | 14.59% | 62.91% | 5.95% | 88.7642 | 645.645 |
| ordinary/VOL_05 | -3.23% | 17.12% | 42.96% | 4.35% | 16.3031 | 78.3691 |
| ordinary/VOL_10 | -3.09% | 15.83% | 44.19% | 4.14% | 13.6629 | 65.5761 |
| stressed/B2_05 | -5.11% | 13.56% | 63.42% | 5.78% | 109.161 | 1118.12 |
| stressed/B2_10 | -5.54% | 14.52% | 62.92% | 6.23% | 88.7729 | 990.266 |
| stressed/VOL_05 | -3.30% | 17.08% | 42.97% | 4.36% | 16.313 | 142.3 |
| stressed/VOL_10 | -3.14% | 15.81% | 44.21% | 4.15% | 13.6798 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.00% | 0.0281358 |
| calibrated | 62.00% | 0.0228801 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1478 | 909 | 569 | 48.73% |
| 60m | perp_synchronized_clock | 1478 | 909 | 569 | 48.73% |
| 60m | combined_synchronized_clock | 1478 | 897 | 581 | 48.72% |
| 15m | perp_original_clock | 1478 | 909 | 569 | 47.19% |
| 15m | perp_synchronized_clock | 1478 | 909 | 569 | 47.19% |
| 15m | combined_synchronized_clock | 1478 | 897 | 581 | 46.49% |

## Data usability pilots

- Options: 394 captures; usable 7d RR25 in 339, usable 30d RR25 in 86; 313 valid hourly changes.
- Liquidations: 1065 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1475}`.
- Exchange stress: 789/789 scheduled records. Capture states: `{"missed": 43, "ok": 746}`. Ratings: `{"low": 746}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
