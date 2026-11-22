# Market studies

Generated 2026-11-22T14:47:21.598Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 173 | 136 | 136 |
| range | collecting (descriptive) | 173 | 129 | 123 |
| state | collecting (descriptive) | 693 | 374 | 373 |
| paired | collecting (descriptive) | 2772 | 2674 | 2669 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.289063 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.000411166 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00189999 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00103035 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.64% | 16.74% | 48.14% | 13.92% | 89.077 | 928.525 |
| ordinary/B2_10 | -11.09% | 15.29% | 46.75% | 13.13% | 62.7744 | 815.177 |
| ordinary/VOL_05 | -9.36% | 17.47% | 36.87% | 11.99% | 11.889 | 98.0562 |
| ordinary/VOL_10 | -8.97% | 17.54% | 38.24% | 11.91% | 7.94525 | 65.5761 |
| stressed/B2_05 | -12.18% | 16.74% | 48.15% | 14.39% | 89.1646 | 1516.64 |
| stressed/B2_10 | -11.48% | 15.27% | 46.76% | 13.45% | 62.84 | 1229.59 |
| stressed/VOL_05 | -9.43% | 17.46% | 36.87% | 12.02% | 11.8956 | 178.068 |
| stressed/VOL_10 | -9.02% | 17.54% | 38.25% | 11.93% | 7.95547 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.04% | 0.0364042 |
| calibrated | 66.67% | 0.0365207 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2669 | 1538 | 1131 | 48.31% |
| 60m | perp_synchronized_clock | 2669 | 1538 | 1131 | 48.31% |
| 60m | combined_synchronized_clock | 2669 | 1510 | 1159 | 48.41% |
| 15m | perp_original_clock | 2669 | 1538 | 1131 | 48.89% |
| 15m | perp_synchronized_clock | 2669 | 1538 | 1131 | 48.89% |
| 15m | combined_synchronized_clock | 2669 | 1510 | 1159 | 48.01% |

## Data usability pilots

- Options: 692 captures; usable 7d RR25 in 589, usable 30d RR25 in 348; 536 valid hourly changes.
- Liquidations: 1956 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2663}`.
- Exchange stress: 1386/1386 scheduled records. Capture states: `{"missed": 45, "ok": 1341}`. Ratings: `{"low": 1341}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
