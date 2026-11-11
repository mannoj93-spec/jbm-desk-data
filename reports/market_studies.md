# Market studies

Generated 2026-11-11T06:46:51.808Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 105 | 69 | 69 |
| range | collecting (descriptive) | 105 | 63 | 57 |
| state | collecting (descriptive) | 421 | 293 | 289 |
| paired | collecting (descriptive) | 1684 | 1590 | 1585 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0200884 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00432462 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000749391 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000788644 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.33% | 13.00% | 61.26% | 5.64% | 111.037 | 739.372 |
| ordinary/B2_10 | -5.78% | 13.90% | 60.62% | 6.11% | 87.8876 | 688.033 |
| ordinary/VOL_05 | -3.92% | 16.36% | 42.30% | 4.58% | 15.2405 | 78.3691 |
| ordinary/VOL_10 | -3.77% | 15.16% | 43.44% | 4.38% | 12.7717 | 65.5761 |
| stressed/B2_05 | -5.78% | 12.97% | 61.27% | 6.03% | 111.053 | 1200.26 |
| stressed/B2_10 | -6.13% | 13.83% | 60.63% | 6.41% | 87.906 | 1052.22 |
| stressed/VOL_05 | -3.98% | 16.33% | 42.30% | 4.60% | 15.2499 | 142.3 |
| stressed/VOL_10 | -3.82% | 15.14% | 43.46% | 4.39% | 12.7876 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 68.42% | 0.0297872 |
| calibrated | 66.67% | 0.0250265 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1585 | 976 | 609 | 48.98% |
| 60m | perp_synchronized_clock | 1585 | 976 | 609 | 48.98% |
| 60m | combined_synchronized_clock | 1585 | 964 | 621 | 49.07% |
| 15m | perp_original_clock | 1585 | 976 | 609 | 46.82% |
| 15m | perp_synchronized_clock | 1585 | 976 | 609 | 46.82% |
| 15m | combined_synchronized_clock | 1585 | 964 | 621 | 46.16% |

## Data usability pilots

- Options: 421 captures; usable 7d RR25 in 353, usable 30d RR25 in 108; 326 valid hourly changes.
- Liquidations: 1143 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1579}`.
- Exchange stress: 842/842 scheduled records. Capture states: `{"missed": 43, "ok": 799}`. Ratings: `{"low": 799}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
