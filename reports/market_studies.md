# Market studies

Generated 2026-11-13T04:03:51.718Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 117 | 80 | 80 |
| range | collecting (descriptive) | 117 | 74 | 68 |
| state | collecting (descriptive) | 467 | 311 | 309 |
| paired | collecting (descriptive) | 1865 | 1770 | 1764 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.238072 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00354726 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000267813 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000496032 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -6.43% | 12.67% | 58.77% | 6.74% | 105.039 | 762.826 |
| ordinary/B2_10 | -6.71% | 13.33% | 58.03% | 7.05% | 79.862 | 688.033 |
| ordinary/VOL_05 | -4.91% | 15.56% | 41.52% | 5.57% | 15.2014 | 86.1552 |
| ordinary/VOL_10 | -4.70% | 14.47% | 42.43% | 5.30% | 11.5842 | 65.5761 |
| stressed/B2_05 | -6.89% | 12.65% | 58.78% | 7.14% | 105.078 | 1242.68 |
| stressed/B2_10 | -7.06% | 13.28% | 58.04% | 7.34% | 79.9002 | 1052.22 |
| stressed/VOL_05 | -4.98% | 15.54% | 41.53% | 5.59% | 15.2107 | 156.448 |
| stressed/VOL_10 | -4.76% | 14.45% | 42.44% | 5.31% | 11.5988 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 73.53% | 0.0311856 |
| calibrated | 72.06% | 0.0271172 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1764 | 1070 | 694 | 48.41% |
| 60m | perp_synchronized_clock | 1764 | 1070 | 694 | 48.41% |
| 60m | combined_synchronized_clock | 1764 | 1060 | 704 | 48.11% |
| 15m | perp_original_clock | 1764 | 1070 | 694 | 47.48% |
| 15m | perp_synchronized_clock | 1764 | 1070 | 694 | 47.48% |
| 15m | combined_synchronized_clock | 1764 | 1060 | 704 | 46.79% |

## Data usability pilots

- Options: 466 captures; usable 7d RR25 in 387, usable 30d RR25 in 144; 358 valid hourly changes.
- Liquidations: 1281 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1763}`.
- Exchange stress: 933/933 scheduled records. Capture states: `{"missed": 44, "ok": 889}`. Ratings: `{"low": 889}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
