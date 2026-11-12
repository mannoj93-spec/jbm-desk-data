# Market studies

Generated 2026-11-12T00:22:15.594Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 110 | 74 | 74 |
| range | collecting (descriptive) | 110 | 68 | 61 |
| state | collecting (descriptive) | 439 | 301 | 300 |
| paired | collecting (descriptive) | 1754 | 1659 | 1653 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0143981 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0040435 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00139119 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 3.781e-05 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| control | 70.49% | 0.0304651 |
| calibrated | 68.85% | 0.0260191 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1653 | 1014 | 639 | 49.01% |
| 60m | perp_synchronized_clock | 1653 | 1014 | 639 | 49.01% |
| 60m | combined_synchronized_clock | 1653 | 1003 | 650 | 48.85% |
| 15m | perp_original_clock | 1653 | 1014 | 639 | 46.94% |
| 15m | perp_synchronized_clock | 1653 | 1014 | 639 | 46.94% |
| 15m | combined_synchronized_clock | 1653 | 1003 | 650 | 46.26% |

## Data usability pilots

- Options: 439 captures; usable 7d RR25 in 365, usable 30d RR25 in 126; 337 valid hourly changes.
- Liquidations: 1197 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1651}`.
- Exchange stress: 877/877 scheduled records. Capture states: `{"missed": 44, "ok": 833}`. Ratings: `{"low": 833}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
