# Market studies

Generated 2026-11-12T12:47:03.629Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 113 | 77 | 77 |
| range | collecting (descriptive) | 113 | 71 | 64 |
| state | collecting (descriptive) | 451 | 306 | 305 |
| paired | collecting (descriptive) | 1804 | 1709 | 1704 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.111554 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00381754 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000878916 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000806925 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 71.88% | 0.0308109 |
| calibrated | 70.31% | 0.0265369 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1704 | 1037 | 667 | 48.60% |
| 60m | perp_synchronized_clock | 1704 | 1037 | 667 | 48.60% |
| 60m | combined_synchronized_clock | 1704 | 1027 | 677 | 48.20% |
| 15m | perp_original_clock | 1704 | 1037 | 667 | 46.77% |
| 15m | perp_synchronized_clock | 1704 | 1037 | 667 | 46.77% |
| 15m | combined_synchronized_clock | 1704 | 1027 | 677 | 46.06% |

## Data usability pilots

- Options: 451 captures; usable 7d RR25 in 377, usable 30d RR25 in 138; 349 valid hourly changes.
- Liquidations: 1233 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1699}`.
- Exchange stress: 902/902 scheduled records. Capture states: `{"missed": 44, "ok": 858}`. Ratings: `{"low": 858}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
