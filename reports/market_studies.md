# Market studies

Generated 2026-10-30T20:12:55.149Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 37 | 35 | 35 |
| range | collecting (descriptive) | 37 | 29 | 22 |
| state | collecting (descriptive) | 147 | 99 | 97 |
| paired | collecting (descriptive) | 585 | 499 | 494 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.338409 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00818581 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.0041915 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.0013917 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -1.63% | 15.65% | 43.88% | 1.95% | 133.557 | 239.455 |
| ordinary/B2_10 | -1.96% | 17.16% | 44.08% | 2.31% | 85.4428 | 153.491 |
| ordinary/VOL_05 | -2.26% | 22.05% | 48.21% | 2.93% | 38.3242 | 68.8516 |
| ordinary/VOL_10 | -2.04% | 20.23% | 47.42% | 2.66% | 29.141 | 52.2225 |
| stressed/B2_05 | -1.82% | 15.61% | 43.88% | 2.09% | 133.641 | 434.795 |
| stressed/B2_10 | -2.08% | 17.07% | 44.09% | 2.37% | 85.5007 | 278.561 |
| stressed/VOL_05 | -2.32% | 22.00% | 48.22% | 2.94% | 38.3505 | 125.006 |
| stressed/VOL_10 | -2.08% | 20.20% | 47.44% | 2.66% | 29.1794 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 72.73% | 0.032522 |
| calibrated | 72.73% | 0.0260082 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 494 | 300 | 194 | 52.67% |
| 60m | perp_synchronized_clock | 494 | 300 | 194 | 52.67% |
| 60m | combined_synchronized_clock | 494 | 301 | 193 | 53.16% |
| 15m | perp_original_clock | 494 | 300 | 194 | 46.33% |
| 15m | perp_synchronized_clock | 494 | 300 | 194 | 46.33% |
| 15m | combined_synchronized_clock | 494 | 301 | 193 | 46.84% |

## Data usability pilots

- Options: 146 captures; usable 7d RR25 in 123, usable 30d RR25 in 86; 115 valid hourly changes.
- Liquidations: 343 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 501}`.
- Exchange stress: 293/293 scheduled records. Capture states: `{"missed": 39, "ok": 254}`. Ratings: `{"low": 254}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
