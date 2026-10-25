# Market studies

Generated 2026-10-25T00:13:11.032Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 2 | 1 | 1 |
| range | registered; not launched | 2 | 0 | 0 |
| state | collecting (descriptive) | 7 | 4 | 0 |
| paired | collecting (descriptive) | 25 | 11 | 8 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | — | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | — | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | — | — | — | 0.00% | — | — |
| ordinary/B2_10 | — | — | — | 0.00% | — | — |
| ordinary/VOL_05 | — | — | — | 0.00% | — | — |
| ordinary/VOL_10 | — | — | — | 0.00% | — | — |
| stressed/B2_05 | — | — | — | 0.00% | — | — |
| stressed/B2_10 | — | — | — | 0.00% | — | — |
| stressed/VOL_05 | — | — | — | 0.00% | — | — |
| stressed/VOL_10 | — | — | — | 0.00% | — | — |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 8 | 5 | 3 | 60.00% |
| 60m | perp_synchronized_clock | 8 | 5 | 3 | 60.00% |
| 60m | combined_synchronized_clock | 8 | 5 | 3 | 60.00% |
| 15m | perp_original_clock | 8 | 5 | 3 | 60.00% |
| 15m | perp_synchronized_clock | 8 | 5 | 3 | 60.00% |
| 15m | combined_synchronized_clock | 8 | 5 | 3 | 60.00% |

## Data usability pilots

- Options: 7 captures; usable 7d RR25 in 7, usable 30d RR25 in 7; 6 valid hourly changes.
- Liquidations: 3 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 3, "ok": 8}`.
- Exchange stress: 13/13 scheduled records. Capture states: `{"missed": 7, "ok": 6}`. Ratings: `{"low": 6}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
