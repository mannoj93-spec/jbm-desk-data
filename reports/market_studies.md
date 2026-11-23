# Market studies

Generated 2026-11-23T18:47:56.838Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 180 | 143 | 143 |
| range | collecting (descriptive) | 180 | 136 | 130 |
| state | collecting (descriptive) | 721 | 378 | 378 |
| paired | collecting (descriptive) | 2884 | 2786 | 2781 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.365238 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000460687 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00189481 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00130349 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.10% | 16.59% | 47.14% | 13.92% | 88.3572 | 949.63 |
| ordinary/B2_10 | -10.69% | 15.13% | 45.76% | 13.13% | 60.4856 | 815.177 |
| ordinary/VOL_05 | -8.89% | 17.27% | 36.39% | 11.99% | 11.4521 | 98.0562 |
| ordinary/VOL_10 | -8.41% | 17.42% | 37.87% | 11.91% | 7.65275 | 65.5761 |
| stressed/B2_05 | -11.66% | 16.60% | 47.14% | 14.39% | 88.4457 | 1554.77 |
| stressed/B2_10 | -11.08% | 15.11% | 45.77% | 13.45% | 60.5529 | 1229.59 |
| stressed/VOL_05 | -8.96% | 17.26% | 36.39% | 12.02% | 11.4585 | 178.068 |
| stressed/VOL_10 | -8.46% | 17.42% | 37.88% | 11.93% | 7.66261 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.15% | 0.037296 |
| calibrated | 67.69% | 0.0382474 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2781 | 1584 | 1197 | 48.36% |
| 60m | perp_synchronized_clock | 2781 | 1584 | 1197 | 48.36% |
| 60m | combined_synchronized_clock | 2781 | 1558 | 1223 | 48.59% |
| 15m | perp_original_clock | 2781 | 1584 | 1197 | 48.93% |
| 15m | perp_synchronized_clock | 2781 | 1584 | 1197 | 48.93% |
| 15m | combined_synchronized_clock | 2781 | 1558 | 1223 | 48.07% |

## Data usability pilots

- Options: 720 captures; usable 7d RR25 in 617, usable 30d RR25 in 376; 564 valid hourly changes.
- Liquidations: 2040 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2775}`.
- Exchange stress: 1442/1442 scheduled records. Capture states: `{"missed": 45, "ok": 1397}`. Ratings: `{"low": 1397}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
