# Market studies

Generated 2026-10-28T22:16:26.013Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 25 | 23 | 23 |
| range | collecting (descriptive) | 25 | 17 | 11 |
| state | collecting (descriptive) | 101 | 68 | 65 |
| paired | collecting (descriptive) | 402 | 316 | 310 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.25302 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00648713 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000512225 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000604839 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | 0.03% | 9.55% | 48.29% | 0.84% | 157.11 | 187.429 |
| ordinary/B2_10 | 0.11% | 9.45% | 49.02% | 0.77% | 101.601 | 121.283 |
| ordinary/VOL_05 | 0.48% | 9.57% | 47.77% | 0.67% | 49.036 | 58.5665 |
| ordinary/VOL_10 | 0.44% | 9.42% | 47.52% | 0.67% | 43.7243 | 52.2225 |
| stressed/B2_05 | -0.12% | 9.51% | 48.29% | 0.88% | 157.207 | 340.662 |
| stressed/B2_10 | 0.01% | 9.30% | 49.03% | 0.78% | 101.675 | 220.517 |
| stressed/VOL_05 | 0.43% | 9.48% | 47.79% | 0.67% | 49.0791 | 106.48 |
| stressed/VOL_10 | 0.40% | 9.35% | 47.54% | 0.67% | 43.7815 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 90.91% | 0.0322927 |
| calibrated | 90.91% | 0.0257417 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 310 | 185 | 125 | 48.65% |
| 60m | perp_synchronized_clock | 310 | 185 | 125 | 48.65% |
| 60m | combined_synchronized_clock | 310 | 192 | 118 | 48.96% |
| 15m | perp_original_clock | 310 | 185 | 125 | 46.49% |
| 15m | perp_synchronized_clock | 310 | 185 | 125 | 46.49% |
| 15m | combined_synchronized_clock | 310 | 192 | 118 | 46.88% |

## Data usability pilots

- Options: 101 captures; usable 7d RR25 in 85, usable 30d RR25 in 86; 79 valid hourly changes.
- Liquidations: 205 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 317}`.
- Exchange stress: 201/201 scheduled records. Capture states: `{"missed": 39, "ok": 162}`. Ratings: `{"low": 162}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
