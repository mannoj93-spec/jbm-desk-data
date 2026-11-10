# Market studies

Generated 2026-11-10T06:01:57.564Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 99 | 63 | 63 |
| range | collecting (descriptive) | 99 | 57 | 51 |
| state | collecting (descriptive) | 397 | 281 | 276 |
| paired | collecting (descriptive) | 1585 | 1491 | 1486 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0967902 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0049924 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000112768 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000504711 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.88% | 13.51% | 63.09% | 5.43% | 108.093 | 693.946 |
| ordinary/B2_10 | -5.38% | 14.49% | 62.59% | 5.95% | 87.9098 | 645.645 |
| ordinary/VOL_05 | -3.43% | 17.00% | 42.87% | 4.35% | 16.1423 | 78.3691 |
| ordinary/VOL_10 | -3.28% | 15.73% | 44.08% | 4.14% | 13.528 | 65.5761 |
| stressed/B2_05 | -5.30% | 13.47% | 63.09% | 5.78% | 108.109 | 1118.12 |
| stressed/B2_10 | -5.72% | 14.42% | 62.60% | 6.23% | 87.9211 | 990.266 |
| stressed/VOL_05 | -3.49% | 16.97% | 42.87% | 4.36% | 16.152 | 142.3 |
| stressed/VOL_10 | -3.34% | 15.71% | 44.10% | 4.15% | 13.5447 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.028322 |
| calibrated | 62.75% | 0.0231354 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1486 | 913 | 573 | 48.74% |
| 60m | perp_synchronized_clock | 1486 | 913 | 573 | 48.74% |
| 60m | combined_synchronized_clock | 1486 | 901 | 585 | 48.72% |
| 15m | perp_original_clock | 1486 | 913 | 573 | 47.10% |
| 15m | perp_synchronized_clock | 1486 | 913 | 573 | 47.10% |
| 15m | combined_synchronized_clock | 1486 | 901 | 585 | 46.39% |

## Data usability pilots

- Options: 396 captures; usable 7d RR25 in 341, usable 30d RR25 in 86; 315 valid hourly changes.
- Liquidations: 1071 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1483}`.
- Exchange stress: 793/793 scheduled records. Capture states: `{"missed": 43, "ok": 750}`. Ratings: `{"low": 750}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
