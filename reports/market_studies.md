# Market studies

Generated 2026-10-29T14:03:04.198Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 29 | 27 | 27 |
| range | collecting (descriptive) | 29 | 21 | 15 |
| state | collecting (descriptive) | 117 | 84 | 79 |
| paired | collecting (descriptive) | 465 | 379 | 374 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.897713 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.0064843 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00244298 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00183824 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.53% | 10.78% | 47.19% | 0.95% | 146.015 | 203.444 |
| ordinary/B2_10 | -0.45% | 10.72% | 47.81% | 0.90% | 98.4845 | 137.307 |
| ordinary/VOL_05 | -0.23% | 12.15% | 48.57% | 0.88% | 41.9693 | 58.5665 |
| ordinary/VOL_10 | -0.19% | 11.43% | 47.53% | 0.79% | 37.4229 | 52.2225 |
| stressed/B2_05 | -0.69% | 10.72% | 47.19% | 1.06% | 146.113 | 369.736 |
| stressed/B2_10 | -0.56% | 10.59% | 47.82% | 0.95% | 98.5565 | 249.621 |
| stressed/VOL_05 | -0.28% | 12.08% | 48.59% | 0.88% | 42.0066 | 106.48 |
| stressed/VOL_10 | -0.24% | 11.38% | 47.55% | 0.79% | 37.4719 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 93.33% | 0.0320994 |
| calibrated | 93.33% | 0.0255683 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 374 | 234 | 140 | 49.15% |
| 60m | perp_synchronized_clock | 374 | 234 | 140 | 49.15% |
| 60m | combined_synchronized_clock | 374 | 235 | 139 | 49.79% |
| 15m | perp_original_clock | 374 | 234 | 140 | 43.59% |
| 15m | perp_synchronized_clock | 374 | 234 | 140 | 43.59% |
| 15m | combined_synchronized_clock | 374 | 235 | 139 | 43.83% |

## Data usability pilots

- Options: 116 captures; usable 7d RR25 in 94, usable 30d RR25 in 86; 87 valid hourly changes.
- Liquidations: 253 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 381}`.
- Exchange stress: 233/233 scheduled records. Capture states: `{"missed": 39, "ok": 194}`. Ratings: `{"low": 194}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
