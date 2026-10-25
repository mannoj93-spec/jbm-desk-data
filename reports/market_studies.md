# Market studies

Generated 2026-10-25T03:46:51.454Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 2 | 2 | 2 |
| range | registered; not launched | 2 | 0 | 0 |
| state | collecting (descriptive) | 10 | 5 | 3 |
| paired | collecting (descriptive) | 40 | 15 | 13 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | — | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | — | — (insufficient blocks) | not launched |
| state | -0.0243697 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.24% | — | 55.57% | 0.00% | 1164.86 | 61.0952 |
| ordinary/B2_10 | 0.24% | — | 55.57% | 0.00% | 1164.86 | 61.0952 |
| ordinary/VOL_05 | 0.21% | — | 47.49% | 0.00% | 995.688 | 52.2225 |
| ordinary/VOL_10 | 0.21% | — | 47.49% | 0.00% | 995.688 | 52.2225 |
| stressed/B2_05 | 0.19% | — | 55.59% | 0.00% | 1165.91 | 111.125 |
| stressed/B2_10 | 0.19% | — | 55.59% | 0.00% | 1165.91 | 111.125 |
| stressed/VOL_05 | 0.16% | — | 47.51% | 0.00% | 996.584 | 94.9864 |
| stressed/VOL_10 | 0.16% | — | 47.51% | 0.00% | 996.584 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | — | — |
| calibrated | — | — |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 13 | 9 | 4 | 44.44% |
| 60m | perp_synchronized_clock | 13 | 9 | 4 | 44.44% |
| 60m | combined_synchronized_clock | 13 | 9 | 4 | 44.44% |
| 15m | perp_original_clock | 13 | 9 | 4 | 44.44% |
| 15m | perp_synchronized_clock | 13 | 9 | 4 | 44.44% |
| 15m | combined_synchronized_clock | 13 | 9 | 4 | 44.44% |

## Data usability pilots

- Options: 10 captures; usable 7d RR25 in 10, usable 30d RR25 in 10; 9 valid hourly changes.
- Liquidations: 4 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 9, "ok": 11}`.
- Exchange stress: 20/20 scheduled records. Capture states: `{"missed": 12, "ok": 8}`. Ratings: `{"low": 8}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
