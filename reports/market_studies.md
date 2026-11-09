# Market studies

Generated 2026-11-09T22:47:01.012Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 97 | 61 | 61 |
| range | collecting (descriptive) | 97 | 55 | 49 |
| state | collecting (descriptive) | 389 | 275 | 273 |
| paired | collecting (descriptive) | 1556 | 1462 | 1457 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.100757 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00526679 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000378204 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000900824 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.81% | 13.67% | 63.75% | 5.43% | 110.239 | 693.946 |
| ordinary/B2_10 | -5.31% | 14.67% | 63.24% | 5.95% | 89.646 | 645.645 |
| ordinary/VOL_05 | -3.35% | 17.23% | 43.07% | 4.35% | 16.4692 | 78.3691 |
| ordinary/VOL_10 | -3.21% | 15.93% | 44.31% | 4.14% | 13.8022 | 65.5761 |
| stressed/B2_05 | -5.22% | 13.63% | 63.76% | 5.78% | 110.247 | 1118.12 |
| stressed/B2_10 | -5.65% | 14.60% | 63.26% | 6.23% | 89.6519 | 990.266 |
| stressed/VOL_05 | -3.42% | 17.20% | 43.07% | 4.36% | 16.4791 | 142.3 |
| stressed/VOL_10 | -3.26% | 15.91% | 44.33% | 4.15% | 13.8192 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.31% | 0.0278898 |
| calibrated | 61.22% | 0.0225622 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1457 | 900 | 557 | 48.44% |
| 60m | perp_synchronized_clock | 1457 | 900 | 557 | 48.44% |
| 60m | combined_synchronized_clock | 1457 | 891 | 566 | 48.60% |
| 15m | perp_original_clock | 1457 | 900 | 557 | 47.00% |
| 15m | perp_synchronized_clock | 1457 | 900 | 557 | 47.00% |
| 15m | combined_synchronized_clock | 1457 | 891 | 566 | 46.35% |

## Data usability pilots

- Options: 389 captures; usable 7d RR25 in 334, usable 30d RR25 in 86; 308 valid hourly changes.
- Liquidations: 1047 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1451}`.
- Exchange stress: 778/778 scheduled records. Capture states: `{"missed": 43, "ok": 735}`. Ratings: `{"low": 735}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
