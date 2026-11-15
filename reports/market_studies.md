# Market studies

Generated 2026-11-15T19:32:17.227Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 132 | 96 | 96 |
| range | collecting (descriptive) | 132 | 90 | 84 |
| state | collecting (descriptive) | 530 | 332 | 330 |
| paired | collecting (descriptive) | 2119 | 2023 | 2018 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0362721 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00392821 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000863859 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -3.09713e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.07% | 15.34% | 55.24% | 10.56% | 105.712 | 873.64 |
| ordinary/B2_10 | -10.14% | 15.25% | 54.59% | 10.65% | 80.6779 | 815.177 |
| ordinary/VOL_05 | -8.24% | 17.41% | 40.57% | 9.09% | 15.3233 | 98.0562 |
| ordinary/VOL_10 | -7.65% | 16.03% | 41.02% | 8.49% | 10.2498 | 65.5761 |
| stressed/B2_05 | -10.58% | 15.33% | 55.25% | 11.01% | 105.757 | 1417.53 |
| stressed/B2_10 | -10.53% | 15.20% | 54.61% | 10.98% | 80.7175 | 1229.59 |
| stressed/VOL_05 | -8.31% | 17.39% | 40.58% | 9.12% | 15.3308 | 178.068 |
| stressed/VOL_10 | -7.70% | 16.02% | 41.03% | 8.50% | 10.2628 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 60.71% | 0.0314618 |
| calibrated | 59.52% | 0.0281107 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2018 | 1202 | 816 | 48.50% |
| 60m | perp_synchronized_clock | 2018 | 1202 | 816 | 48.50% |
| 60m | combined_synchronized_clock | 2018 | 1189 | 829 | 48.36% |
| 15m | perp_original_clock | 2018 | 1202 | 816 | 47.42% |
| 15m | perp_synchronized_clock | 2018 | 1202 | 816 | 47.42% |
| 15m | combined_synchronized_clock | 2018 | 1189 | 829 | 46.76% |

## Data usability pilots

- Options: 530 captures; usable 7d RR25 in 450, usable 30d RR25 in 200; 415 valid hourly changes.
- Liquidations: 1470 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2015}`.
- Exchange stress: 1060/1060 scheduled records. Capture states: `{"missed": 44, "ok": 1016}`. Ratings: `{"low": 1016}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
