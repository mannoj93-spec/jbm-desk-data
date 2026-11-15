# Market studies

Generated 2026-11-15T10:16:49.328Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 130 | 94 | 94 |
| range | collecting (descriptive) | 130 | 88 | 82 |
| state | collecting (descriptive) | 521 | 328 | 325 |
| paired | collecting (descriptive) | 2082 | 1986 | 1981 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0434174 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00424827 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000548584 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000189298 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.26% | 15.20% | 55.76% | 10.56% | 107.198 | 873.64 |
| ordinary/B2_10 | -10.33% | 15.11% | 55.10% | 10.65% | 81.815 | 815.177 |
| ordinary/VOL_05 | -8.46% | 17.25% | 40.81% | 9.09% | 15.5428 | 98.0562 |
| ordinary/VOL_10 | -7.91% | 15.71% | 41.19% | 8.49% | 10.3976 | 65.5761 |
| stressed/B2_05 | -10.77% | 15.18% | 55.76% | 11.01% | 107.239 | 1417.53 |
| stressed/B2_10 | -10.72% | 15.06% | 55.11% | 10.98% | 81.852 | 1229.59 |
| stressed/VOL_05 | -8.54% | 17.24% | 40.81% | 9.12% | 15.5503 | 178.068 |
| stressed/VOL_10 | -7.96% | 15.69% | 41.20% | 8.50% | 10.4108 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 62.20% | 0.0314809 |
| calibrated | 60.98% | 0.0280234 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1981 | 1183 | 798 | 48.77% |
| 60m | perp_synchronized_clock | 1981 | 1183 | 798 | 48.77% |
| 60m | combined_synchronized_clock | 1981 | 1169 | 812 | 48.67% |
| 15m | perp_original_clock | 1981 | 1183 | 798 | 47.42% |
| 15m | perp_synchronized_clock | 1981 | 1183 | 798 | 47.42% |
| 15m | combined_synchronized_clock | 1981 | 1169 | 812 | 46.79% |

## Data usability pilots

- Options: 521 captures; usable 7d RR25 in 441, usable 30d RR25 in 191; 406 valid hourly changes.
- Liquidations: 1443 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1979}`.
- Exchange stress: 1041/1041 scheduled records. Capture states: `{"missed": 44, "ok": 997}`. Ratings: `{"low": 997}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
