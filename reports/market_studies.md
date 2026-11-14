# Market studies

Generated 2026-11-14T17:32:14.979Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 126 | 90 | 90 |
| range | collecting (descriptive) | 126 | 84 | 78 |
| state | collecting (descriptive) | 504 | 324 | 323 |
| paired | collecting (descriptive) | 2015 | 1920 | 1915 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0509603 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00463264 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000798718 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000293734 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.53% | 15.26% | 56.64% | 9.83% | 106.159 | 817.162 |
| ordinary/B2_10 | -9.46% | 15.06% | 55.84% | 9.78% | 81.1453 | 731.91 |
| ordinary/VOL_05 | -7.81% | 17.33% | 41.13% | 8.45% | 14.9135 | 91.4039 |
| ordinary/VOL_10 | -7.23% | 15.72% | 41.54% | 7.81% | 10.7065 | 65.5761 |
| stressed/B2_05 | -10.02% | 15.25% | 56.65% | 10.27% | 106.202 | 1340.97 |
| stressed/B2_10 | -9.84% | 15.02% | 55.85% | 10.11% | 81.1847 | 1131.69 |
| stressed/VOL_05 | -7.88% | 17.31% | 41.13% | 8.48% | 14.922 | 165.985 |
| stressed/VOL_10 | -7.28% | 15.71% | 41.55% | 7.82% | 10.72 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.38% | 0.0318828 |
| calibrated | 64.10% | 0.0282218 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1915 | 1145 | 770 | 49.00% |
| 60m | perp_synchronized_clock | 1915 | 1145 | 770 | 49.00% |
| 60m | combined_synchronized_clock | 1915 | 1134 | 781 | 48.77% |
| 15m | perp_original_clock | 1915 | 1145 | 770 | 47.34% |
| 15m | perp_synchronized_clock | 1915 | 1145 | 770 | 47.34% |
| 15m | combined_synchronized_clock | 1915 | 1134 | 781 | 46.74% |

## Data usability pilots

- Options: 504 captures; usable 7d RR25 in 424, usable 30d RR25 in 174; 393 valid hourly changes.
- Liquidations: 1392 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1911}`.
- Exchange stress: 1008/1008 scheduled records. Capture states: `{"missed": 44, "ok": 964}`. Ratings: `{"low": 964}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
