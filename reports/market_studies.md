# Market studies

Generated 2026-10-29T16:03:17.770Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 30 | 27 | 27 |
| range | collecting (descriptive) | 30 | 21 | 15 |
| state | collecting (descriptive) | 119 | 85 | 81 |
| paired | collecting (descriptive) | 473 | 387 | 382 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.897713 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.0064843 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00265089 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00179974 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

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
| 60m | perp_original_clock | 382 | 239 | 143 | 49.79% |
| 60m | perp_synchronized_clock | 382 | 239 | 143 | 49.79% |
| 60m | combined_synchronized_clock | 382 | 240 | 142 | 50.42% |
| 15m | perp_original_clock | 382 | 239 | 143 | 43.93% |
| 15m | perp_synchronized_clock | 382 | 239 | 143 | 43.93% |
| 15m | combined_synchronized_clock | 382 | 240 | 142 | 44.17% |

## Data usability pilots

- Options: 118 captures; usable 7d RR25 in 95, usable 30d RR25 in 86; 87 valid hourly changes.
- Liquidations: 259 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 389}`.
- Exchange stress: 237/237 scheduled records. Capture states: `{"missed": 39, "ok": 198}`. Ratings: `{"low": 198}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
