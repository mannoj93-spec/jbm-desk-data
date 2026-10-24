# Market studies

Generated 2026-10-24T17:36:11.945Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | registered; not launched | 0 | 0 | 0 |
| range | registered; not launched | 0 | 0 | 0 |
| state | registered; not launched | 0 | 0 | 0 |
| paired | registered; not launched | 0 | 0 | 0 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | — | — (insufficient blocks) | not launched |
| range | — | — (insufficient blocks) | not launched |
| state | — | — (insufficient blocks) | not launched |
| paired | — | — (insufficient blocks) | not launched |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | — | — | — | — | — | — |
| ordinary/B2_10 | — | — | — | — | — | — |
| ordinary/VOL_05 | — | — | — | — | — | — |
| ordinary/VOL_10 | — | — | — | — | — | — |
| stressed/B2_05 | — | — | — | — | — | — |
| stressed/B2_10 | — | — | — | — | — | — |
| stressed/VOL_05 | — | — | — | — | — | — |
| stressed/VOL_10 | — | — | — | — | — | — |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 0 | 0 | 0 | — |
| 60m | perp_synchronized_clock | 0 | 0 | 0 | — |
| 60m | combined_synchronized_clock | 0 | 0 | 0 | — |
| 15m | perp_original_clock | 0 | 0 | 0 | — |
| 15m | perp_synchronized_clock | 0 | 0 | 0 | — |
| 15m | combined_synchronized_clock | 0 | 0 | 0 | — |

## Data usability pilots

- Options: 0 captures; usable 7d RR25 in 0, usable 30d RR25 in 0; 0 valid hourly changes.
- Liquidations: 0 comparable first/later vintage pairs; 0 direction changes. Capture states: `{}`.
- Exchange stress: 0/0 scheduled records. Capture states: `{}`. Ratings: `{}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
