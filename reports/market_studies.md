# Market studies

Generated 2026-11-06T22:46:41.699Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 79 | 43 | 43 |
| range | collecting (descriptive) | 79 | 37 | 35 |
| state | collecting (descriptive) | 317 | 222 | 220 |
| paired | collecting (descriptive) | 1268 | 1174 | 1169 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0285917 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000144235 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00101583 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.68% | 14.33% | 64.53% | 4.07% | 92.1837 | 401.17 |
| ordinary/B2_10 | -4.10% | 15.64% | 64.36% | 4.52% | 72.0772 | 360.876 |
| ordinary/VOL_05 | -2.94% | 20.00% | 45.29% | 3.74% | 20.1316 | 78.3691 |
| ordinary/VOL_10 | -2.79% | 18.39% | 46.82% | 3.54% | 16.8754 | 65.5761 |
| stressed/B2_05 | -3.97% | 14.28% | 64.53% | 4.26% | 92.202 | 693.104 |
| stressed/B2_10 | -4.33% | 15.55% | 64.37% | 4.64% | 72.0874 | 589.091 |
| stressed/VOL_05 | -3.00% | 19.96% | 45.30% | 3.75% | 20.1427 | 142.3 |
| stressed/VOL_10 | -2.85% | 18.36% | 46.84% | 3.54% | 16.8955 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1169 | 705 | 464 | 49.36% |
| 60m | perp_synchronized_clock | 1169 | 705 | 464 | 49.36% |
| 60m | combined_synchronized_clock | 1169 | 690 | 479 | 49.42% |
| 15m | perp_original_clock | 1169 | 705 | 464 | 46.95% |
| 15m | perp_synchronized_clock | 1169 | 705 | 464 | 46.95% |
| 15m | combined_synchronized_clock | 1169 | 690 | 479 | 46.52% |

## Data usability pilots

- Options: 317 captures; usable 7d RR25 in 262, usable 30d RR25 in 86; 238 valid hourly changes.
- Liquidations: 839 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1171}`.
- Exchange stress: 634/634 scheduled records. Capture states: `{"missed": 43, "ok": 591}`. Ratings: `{"low": 591}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
