# Market studies

Generated 2026-11-09T18:31:37.402Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 96 | 60 | 60 |
| range | collecting (descriptive) | 96 | 54 | 48 |
| state | collecting (descriptive) | 385 | 273 | 272 |
| paired | collecting (descriptive) | 1539 | 1445 | 1438 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.109715 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00543906 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000431719 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000912726 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.73% | 13.78% | 64.09% | 5.43% | 111.335 | 693.946 |
| ordinary/B2_10 | -5.23% | 14.80% | 63.58% | 5.95% | 90.5329 | 645.645 |
| ordinary/VOL_05 | -3.27% | 17.38% | 43.17% | 4.35% | 16.6364 | 78.3691 |
| ordinary/VOL_10 | -3.12% | 16.07% | 44.42% | 4.14% | 13.9425 | 65.5761 |
| stressed/B2_05 | -5.15% | 13.75% | 64.10% | 5.78% | 111.339 | 1118.12 |
| stressed/B2_10 | -5.57% | 14.73% | 63.59% | 6.23% | 90.5359 | 990.266 |
| stressed/VOL_05 | -3.33% | 17.34% | 43.18% | 4.36% | 16.6464 | 142.3 |
| stressed/VOL_10 | -3.18% | 16.05% | 44.44% | 4.15% | 13.9597 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 64.58% | 0.027883 |
| calibrated | 60.42% | 0.0225069 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1438 | 890 | 548 | 48.31% |
| 60m | perp_synchronized_clock | 1438 | 890 | 548 | 48.31% |
| 60m | combined_synchronized_clock | 1438 | 881 | 557 | 48.47% |
| 15m | perp_original_clock | 1438 | 890 | 548 | 46.97% |
| 15m | perp_synchronized_clock | 1438 | 890 | 548 | 46.97% |
| 15m | combined_synchronized_clock | 1438 | 881 | 557 | 46.31% |

## Data usability pilots

- Options: 384 captures; usable 7d RR25 in 329, usable 30d RR25 in 86; 305 valid hourly changes.
- Liquidations: 1035 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1435}`.
- Exchange stress: 770/770 scheduled records. Capture states: `{"missed": 43, "ok": 727}`. Ratings: `{"low": 727}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
