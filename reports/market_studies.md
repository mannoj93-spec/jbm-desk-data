# Market studies

Generated 2026-11-12T02:47:00.686Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 110 | 74 | 74 |
| range | collecting (descriptive) | 110 | 68 | 62 |
| state | collecting (descriptive) | 441 | 302 | 301 |
| paired | collecting (descriptive) | 1764 | 1669 | 1664 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0143981 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00396575 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00133801 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 3.75601e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.12% | 12.71% | 59.99% | 5.64% | 106.158 | 739.372 |
| ordinary/B2_10 | -5.58% | 13.58% | 59.38% | 6.11% | 84.0387 | 688.033 |
| ordinary/VOL_05 | -3.71% | 15.91% | 41.87% | 4.58% | 14.5604 | 78.3691 |
| ordinary/VOL_10 | -3.57% | 14.76% | 42.96% | 4.38% | 12.2014 | 65.5761 |
| stressed/B2_05 | -5.57% | 12.70% | 60.00% | 6.03% | 106.189 | 1200.26 |
| stressed/B2_10 | -5.93% | 13.52% | 59.40% | 6.41% | 84.0674 | 1052.22 |
| stressed/VOL_05 | -3.78% | 15.88% | 41.88% | 4.60% | 14.5695 | 142.3 |
| stressed/VOL_10 | -3.62% | 14.74% | 42.98% | 4.39% | 12.2167 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 70.97% | 0.0305926 |
| calibrated | 69.35% | 0.0262058 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1664 | 1017 | 647 | 48.97% |
| 60m | perp_synchronized_clock | 1664 | 1017 | 647 | 48.97% |
| 60m | combined_synchronized_clock | 1664 | 1006 | 658 | 48.81% |
| 15m | perp_original_clock | 1664 | 1017 | 647 | 46.90% |
| 15m | perp_synchronized_clock | 1664 | 1017 | 647 | 46.90% |
| 15m | combined_synchronized_clock | 1664 | 1006 | 658 | 46.22% |

## Data usability pilots

- Options: 441 captures; usable 7d RR25 in 367, usable 30d RR25 in 128; 339 valid hourly changes.
- Liquidations: 1203 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1659}`.
- Exchange stress: 882/882 scheduled records. Capture states: `{"missed": 44, "ok": 838}`. Ratings: `{"low": 838}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
