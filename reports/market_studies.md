# Market studies

Generated 2026-11-15T04:20:22.822Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 129 | 93 | 93 |
| range | collecting (descriptive) | 129 | 87 | 80 |
| state | collecting (descriptive) | 515 | 325 | 325 |
| paired | collecting (descriptive) | 2058 | 1962 | 1957 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0412058 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00458433 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000548584 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -3.19366e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -9.96% | 15.23% | 56.02% | 10.37% | 107.955 | 873.64 |
| ordinary/B2_10 | -10.03% | 15.15% | 55.35% | 10.42% | 82.3942 | 815.177 |
| ordinary/VOL_05 | -8.11% | 17.28% | 40.92% | 8.96% | 14.5905 | 91.4039 |
| ordinary/VOL_10 | -7.50% | 15.68% | 41.27% | 8.29% | 10.473 | 65.5761 |
| stressed/B2_05 | -10.47% | 15.22% | 56.02% | 10.81% | 107.993 | 1417.53 |
| stressed/B2_10 | -10.42% | 15.09% | 55.36% | 10.74% | 82.4297 | 1229.59 |
| stressed/VOL_05 | -8.18% | 17.26% | 40.93% | 8.98% | 14.5989 | 165.985 |
| stressed/VOL_10 | -7.55% | 15.67% | 41.29% | 8.30% | 10.4863 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 63.75% | 0.0316321 |
| calibrated | 62.50% | 0.0280628 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1957 | 1164 | 793 | 48.88% |
| 60m | perp_synchronized_clock | 1957 | 1164 | 793 | 48.88% |
| 60m | combined_synchronized_clock | 1957 | 1151 | 806 | 48.74% |
| 15m | perp_original_clock | 1957 | 1164 | 793 | 47.34% |
| 15m | perp_synchronized_clock | 1957 | 1164 | 793 | 47.34% |
| 15m | combined_synchronized_clock | 1957 | 1151 | 806 | 46.74% |

## Data usability pilots

- Options: 515 captures; usable 7d RR25 in 435, usable 30d RR25 in 185; 402 valid hourly changes.
- Liquidations: 1425 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1955}`.
- Exchange stress: 1029/1029 scheduled records. Capture states: `{"missed": 44, "ok": 985}`. Ratings: `{"low": 985}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
