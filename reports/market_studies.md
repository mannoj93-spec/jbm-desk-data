# Market studies

Generated 2026-11-09T06:01:40.724Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 93 | 57 | 57 |
| range | collecting (descriptive) | 93 | 51 | 45 |
| state | collecting (descriptive) | 373 | 270 | 267 |
| paired | collecting (descriptive) | 1489 | 1395 | 1390 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.082331 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00441319 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.0012189 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00107914 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.77% | 13.83% | 65.17% | 5.08% | 114.774 | 693.946 |
| ordinary/B2_10 | -5.26% | 14.89% | 64.64% | 5.60% | 93.3135 | 645.645 |
| ordinary/VOL_05 | -3.31% | 17.56% | 43.50% | 4.05% | 17.1614 | 78.3691 |
| ordinary/VOL_10 | -3.16% | 16.20% | 44.79% | 3.84% | 14.3829 | 65.5761 |
| stressed/B2_05 | -5.18% | 13.79% | 65.18% | 5.44% | 114.764 | 1118.12 |
| stressed/B2_10 | -5.60% | 14.82% | 64.66% | 5.88% | 93.3067 | 990.266 |
| stressed/VOL_05 | -3.37% | 17.53% | 43.50% | 4.06% | 17.1716 | 142.3 |
| stressed/VOL_10 | -3.21% | 16.18% | 44.81% | 3.85% | 14.4005 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.0280942 |
| calibrated | 64.44% | 0.0225598 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1390 | 867 | 523 | 48.10% |
| 60m | perp_synchronized_clock | 1390 | 867 | 523 | 48.10% |
| 60m | combined_synchronized_clock | 1390 | 859 | 531 | 48.31% |
| 15m | perp_original_clock | 1390 | 867 | 523 | 46.71% |
| 15m | perp_synchronized_clock | 1390 | 867 | 523 | 46.71% |
| 15m | combined_synchronized_clock | 1390 | 859 | 531 | 45.98% |

## Data usability pilots

- Options: 372 captures; usable 7d RR25 in 317, usable 30d RR25 in 86; 293 valid hourly changes.
- Liquidations: 999 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1387}`.
- Exchange stress: 745/745 scheduled records. Capture states: `{"missed": 43, "ok": 702}`. Ratings: `{"low": 702}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
