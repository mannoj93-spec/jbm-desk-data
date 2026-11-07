# Market studies

Generated 2026-11-07T08:48:21.083Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 82 | 46 | 46 |
| range | collecting (descriptive) | 82 | 40 | 35 |
| state | collecting (descriptive) | 327 | 232 | 228 |
| paired | collecting (descriptive) | 1308 | 1214 | 1209 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.107934 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00480849 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000488061 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00155087 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.47% | 14.00% | 64.32% | 4.07% | 99.6132 | 444.383 |
| ordinary/B2_10 | -3.92% | 15.24% | 63.97% | 4.52% | 78.1767 | 395.988 |
| ordinary/VOL_05 | -2.81% | 19.34% | 44.85% | 3.74% | 19.4137 | 78.3691 |
| ordinary/VOL_10 | -2.66% | 17.79% | 46.33% | 3.54% | 16.2728 | 65.5761 |
| stressed/B2_05 | -3.79% | 13.94% | 64.33% | 4.28% | 99.6247 | 771.187 |
| stressed/B2_10 | -4.17% | 15.16% | 63.99% | 4.67% | 78.1855 | 652.399 |
| stressed/VOL_05 | -2.87% | 19.30% | 44.86% | 3.75% | 19.4246 | 142.3 |
| stressed/VOL_10 | -2.71% | 17.77% | 46.35% | 3.54% | 16.2923 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 77.14% | 0.0302886 |
| calibrated | 74.29% | 0.0242299 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1209 | 736 | 473 | 48.78% |
| 60m | perp_synchronized_clock | 1209 | 736 | 473 | 48.78% |
| 60m | combined_synchronized_clock | 1209 | 722 | 487 | 49.03% |
| 15m | perp_original_clock | 1209 | 736 | 473 | 46.47% |
| 15m | perp_synchronized_clock | 1209 | 736 | 473 | 46.47% |
| 15m | combined_synchronized_clock | 1209 | 722 | 487 | 46.12% |

## Data usability pilots

- Options: 327 captures; usable 7d RR25 in 272, usable 30d RR25 in 86; 248 valid hourly changes.
- Liquidations: 869 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1211}`.
- Exchange stress: 654/654 scheduled records. Capture states: `{"missed": 43, "ok": 611}`. Ratings: `{"low": 611}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
