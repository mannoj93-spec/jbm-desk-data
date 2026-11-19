# Market studies

Generated 2026-11-19T01:02:25.650Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 152 | 116 | 116 |
| range | collecting (descriptive) | 152 | 109 | 103 |
| state | collecting (descriptive) | 608 | 360 | 360 |
| paired | collecting (descriptive) | 2429 | 2331 | 2326 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.00257471 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00427737 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000620748 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000591144 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.83% | 14.76% | 51.28% | 11.22% | 96.8398 | 902.969 |
| ordinary/B2_10 | -10.73% | 14.44% | 50.30% | 11.12% | 70.8 | 815.177 |
| ordinary/VOL_05 | -8.93% | 16.47% | 38.59% | 9.64% | 13.4227 | 98.0562 |
| ordinary/VOL_10 | -8.46% | 15.53% | 39.56% | 9.14% | 8.97181 | 65.5761 |
| stressed/B2_05 | -11.36% | 14.75% | 51.29% | 11.70% | 96.9124 | 1470.45 |
| stressed/B2_10 | -11.11% | 14.40% | 50.31% | 11.45% | 70.8577 | 1229.59 |
| stressed/VOL_05 | -9.00% | 16.46% | 38.59% | 9.67% | 13.4298 | 178.068 |
| stressed/VOL_10 | -8.51% | 15.52% | 39.57% | 9.15% | 8.98328 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.99% | 0.0346624 |
| calibrated | 66.02% | 0.0331024 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2326 | 1372 | 954 | 48.25% |
| 60m | perp_synchronized_clock | 2326 | 1372 | 954 | 48.25% |
| 60m | combined_synchronized_clock | 2326 | 1350 | 976 | 48.22% |
| 15m | perp_original_clock | 2326 | 1372 | 954 | 48.10% |
| 15m | perp_synchronized_clock | 2326 | 1372 | 954 | 48.10% |
| 15m | combined_synchronized_clock | 2326 | 1350 | 976 | 47.04% |

## Data usability pilots

- Options: 607 captures; usable 7d RR25 in 514, usable 30d RR25 in 277; 467 valid hourly changes.
- Liquidations: 1704 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2327}`.
- Exchange stress: 1215/1215 scheduled records. Capture states: `{"missed": 45, "ok": 1170}`. Ratings: `{"low": 1170}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
