# Market studies

Generated 2026-10-29T06:31:38.126Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 27 | 25 | 25 |
| range | collecting (descriptive) | 27 | 19 | 13 |
| state | collecting (descriptive) | 109 | 76 | 71 |
| paired | collecting (descriptive) | 435 | 349 | 344 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.924955 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.0064855 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000130754 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000363372 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.62% | 11.20% | 47.71% | 0.95% | 157.285 | 203.444 |
| ordinary/B2_10 | -0.54% | 11.14% | 48.38% | 0.90% | 106.087 | 137.307 |
| ordinary/VOL_05 | -0.36% | 12.62% | 48.21% | 0.88% | 45.213 | 58.5665 |
| ordinary/VOL_10 | -0.30% | 11.89% | 47.54% | 0.79% | 40.3168 | 52.2225 |
| stressed/B2_05 | -0.79% | 11.13% | 47.71% | 1.06% | 157.382 | 369.736 |
| stressed/B2_10 | -0.66% | 11.00% | 48.39% | 0.95% | 106.16 | 249.621 |
| stressed/VOL_05 | -0.40% | 12.55% | 48.23% | 0.88% | 45.253 | 106.48 |
| stressed/VOL_10 | -0.35% | 11.83% | 47.56% | 0.79% | 40.3696 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 92.31% | 0.0322935 |
| calibrated | 92.31% | 0.025754 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 344 | 210 | 134 | 48.57% |
| 60m | perp_synchronized_clock | 344 | 210 | 134 | 48.57% |
| 60m | combined_synchronized_clock | 344 | 216 | 128 | 49.07% |
| 15m | perp_original_clock | 344 | 210 | 134 | 44.76% |
| 15m | perp_synchronized_clock | 344 | 210 | 134 | 44.76% |
| 15m | combined_synchronized_clock | 344 | 216 | 128 | 45.37% |

## Data usability pilots

- Options: 109 captures; usable 7d RR25 in 92, usable 30d RR25 in 86; 86 valid hourly changes.
- Liquidations: 229 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 349}`.
- Exchange stress: 218/218 scheduled records. Capture states: `{"missed": 39, "ok": 179}`. Ratings: `{"low": 179}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
