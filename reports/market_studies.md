# Market studies

Generated 2026-11-12T15:02:42.261Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 113 | 77 | 77 |
| range | collecting (descriptive) | 113 | 71 | 65 |
| state | collecting (descriptive) | 454 | 307 | 306 |
| paired | collecting (descriptive) | 1813 | 1718 | 1713 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.111554 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00374685 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000724363 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000693228 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.58% | 12.52% | 59.40% | 5.89% | 104.618 | 745.871 |
| ordinary/B2_10 | -5.97% | 13.34% | 58.69% | 6.31% | 81.8903 | 688.033 |
| ordinary/VOL_05 | -4.11% | 15.63% | 41.63% | 4.77% | 14.1816 | 78.3691 |
| ordinary/VOL_10 | -3.96% | 14.50% | 42.70% | 4.57% | 11.8838 | 65.5761 |
| stressed/B2_05 | -6.03% | 12.50% | 59.41% | 6.29% | 104.656 | 1212.01 |
| stressed/B2_10 | -6.33% | 13.28% | 58.71% | 6.61% | 81.9241 | 1052.22 |
| stressed/VOL_05 | -4.17% | 15.60% | 41.64% | 4.79% | 14.1905 | 142.3 |
| stressed/VOL_10 | -4.02% | 14.49% | 42.71% | 4.58% | 11.8987 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 72.31% | 0.0309038 |
| calibrated | 70.77% | 0.0266836 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1713 | 1041 | 672 | 48.51% |
| 60m | perp_synchronized_clock | 1713 | 1041 | 672 | 48.51% |
| 60m | combined_synchronized_clock | 1713 | 1032 | 681 | 48.16% |
| 15m | perp_original_clock | 1713 | 1041 | 672 | 46.97% |
| 15m | perp_synchronized_clock | 1713 | 1041 | 672 | 46.97% |
| 15m | combined_synchronized_clock | 1713 | 1032 | 681 | 46.32% |

## Data usability pilots

- Options: 453 captures; usable 7d RR25 in 379, usable 30d RR25 in 140; 351 valid hourly changes.
- Liquidations: 1242 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1711}`.
- Exchange stress: 907/907 scheduled records. Capture states: `{"missed": 44, "ok": 863}`. Ratings: `{"low": 863}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
