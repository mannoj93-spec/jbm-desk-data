# Market studies

Generated 2026-11-12T20:03:24.505Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 115 | 78 | 78 |
| range | collecting (descriptive) | 115 | 72 | 66 |
| state | collecting (descriptive) | 459 | 308 | 307 |
| paired | collecting (descriptive) | 1833 | 1738 | 1733 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.186419 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0036783 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000696243 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000685228 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -6.17% | 12.82% | 59.23% | 6.48% | 103.741 | 745.871 |
| ordinary/B2_10 | -6.47% | 13.49% | 58.47% | 6.80% | 81.2052 | 688.033 |
| ordinary/VOL_05 | -4.60% | 15.74% | 41.55% | 5.26% | 14.0609 | 78.3691 |
| ordinary/VOL_10 | -4.46% | 14.64% | 42.61% | 5.06% | 11.7826 | 65.5761 |
| stressed/B2_05 | -6.62% | 12.79% | 59.23% | 6.88% | 103.782 | 1212.01 |
| stressed/B2_10 | -6.82% | 13.44% | 58.49% | 7.10% | 81.2406 | 1052.22 |
| stressed/VOL_05 | -4.67% | 15.71% | 41.56% | 5.28% | 14.0698 | 142.3 |
| stressed/VOL_10 | -4.51% | 14.62% | 42.62% | 5.07% | 11.7973 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 72.73% | 0.0309998 |
| calibrated | 71.21% | 0.0268317 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1733 | 1053 | 680 | 48.53% |
| 60m | perp_synchronized_clock | 1733 | 1053 | 680 | 48.53% |
| 60m | combined_synchronized_clock | 1733 | 1044 | 689 | 48.18% |
| 15m | perp_original_clock | 1733 | 1053 | 680 | 47.10% |
| 15m | perp_synchronized_clock | 1733 | 1053 | 680 | 47.10% |
| 15m | combined_synchronized_clock | 1733 | 1044 | 689 | 46.46% |

## Data usability pilots

- Options: 458 captures; usable 7d RR25 in 381, usable 30d RR25 in 142; 353 valid hourly changes.
- Liquidations: 1257 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1731}`.
- Exchange stress: 917/917 scheduled records. Capture states: `{"missed": 44, "ok": 873}`. Ratings: `{"low": 873}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
