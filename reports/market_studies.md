# Market studies

Generated 2026-11-13T01:03:09.984Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 116 | 80 | 80 |
| range | collecting (descriptive) | 116 | 74 | 67 |
| state | collecting (descriptive) | 464 | 310 | 308 |
| paired | collecting (descriptive) | 1853 | 1758 | 1753 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.238072 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00361181 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000496535 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000499144 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 73.13% | 0.0310758 |
| calibrated | 71.64% | 0.0269584 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1753 | 1064 | 689 | 48.40% |
| 60m | perp_synchronized_clock | 1753 | 1064 | 689 | 48.40% |
| 60m | combined_synchronized_clock | 1753 | 1054 | 699 | 48.10% |
| 15m | perp_original_clock | 1753 | 1064 | 689 | 47.37% |
| 15m | perp_synchronized_clock | 1753 | 1064 | 689 | 47.37% |
| 15m | combined_synchronized_clock | 1753 | 1054 | 699 | 46.68% |

## Data usability pilots

- Options: 463 captures; usable 7d RR25 in 385, usable 30d RR25 in 142; 356 valid hourly changes.
- Liquidations: 1272 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1751}`.
- Exchange stress: 927/927 scheduled records. Capture states: `{"missed": 44, "ok": 883}`. Ratings: `{"low": 883}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
