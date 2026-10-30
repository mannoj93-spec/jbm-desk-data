# Market studies

Generated 2026-10-30T06:46:42.212Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 33 | 31 | 31 |
| range | collecting (descriptive) | 33 | 25 | 19 |
| state | collecting (descriptive) | 133 | 91 | 88 |
| paired | collecting (descriptive) | 532 | 446 | 441 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.99387 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.000310774 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00478644 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00085034 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.09% | 16.43% | 45.48% | 1.69% | 144.792 | 230.734 |
| ordinary/B2_10 | -1.54% | 18.19% | 46.42% | 2.15% | 95.9394 | 153.491 |
| ordinary/VOL_05 | -1.55% | 23.21% | 48.84% | 2.69% | 43.0223 | 68.8516 |
| ordinary/VOL_10 | -1.27% | 21.15% | 47.51% | 2.40% | 32.7232 | 52.2225 |
| stressed/B2_05 | -1.28% | 16.38% | 45.48% | 1.82% | 144.872 | 419.251 |
| stressed/B2_10 | -1.67% | 18.09% | 46.43% | 2.21% | 95.9984 | 278.561 |
| stressed/VOL_05 | -1.61% | 23.16% | 48.86% | 2.69% | 43.0511 | 125.006 |
| stressed/VOL_10 | -1.31% | 21.13% | 47.53% | 2.40% | 32.7662 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 84.21% | 0.0323382 |
| calibrated | 84.21% | 0.0258186 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 441 | 267 | 174 | 50.94% |
| 60m | perp_synchronized_clock | 441 | 267 | 174 | 50.94% |
| 60m | combined_synchronized_clock | 441 | 269 | 172 | 51.30% |
| 15m | perp_original_clock | 441 | 267 | 174 | 44.57% |
| 15m | perp_synchronized_clock | 441 | 267 | 174 | 44.57% |
| 15m | combined_synchronized_clock | 441 | 269 | 172 | 44.98% |

## Data usability pilots

- Options: 133 captures; usable 7d RR25 in 110, usable 30d RR25 in 86; 102 valid hourly changes.
- Liquidations: 301 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 445}`.
- Exchange stress: 266/266 scheduled records. Capture states: `{"missed": 39, "ok": 227}`. Ratings: `{"low": 227}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
