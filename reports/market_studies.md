# Market studies

Generated 2026-11-13T20:19:52.984Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 121 | 85 | 85 |
| range | collecting (descriptive) | 121 | 79 | 72 |
| state | collecting (descriptive) | 483 | 313 | 313 |
| paired | collecting (descriptive) | 1930 | 1835 | 1830 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.165195 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.0040475 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00014947 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000307377 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -7.48% | 13.89% | 57.37% | 8.02% | 105.939 | 791.943 |
| ordinary/B2_10 | -7.66% | 14.25% | 56.68% | 8.24% | 79.6308 | 704.79 |
| ordinary/VOL_05 | -6.13% | 16.95% | 41.41% | 7.08% | 14.6036 | 86.1552 |
| ordinary/VOL_10 | -5.69% | 15.35% | 41.98% | 6.53% | 11.1266 | 65.5761 |
| stressed/B2_05 | -7.96% | 13.87% | 57.38% | 8.44% | 105.978 | 1295.35 |
| stressed/B2_10 | -8.02% | 14.20% | 56.69% | 8.53% | 79.6686 | 1082.57 |
| stressed/VOL_05 | -6.19% | 16.92% | 41.42% | 7.10% | 14.6127 | 156.448 |
| stressed/VOL_10 | -5.75% | 15.34% | 41.99% | 6.54% | 11.1407 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 69.44% | 0.0315437 |
| calibrated | 68.06% | 0.0276582 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1830 | 1104 | 726 | 48.64% |
| 60m | perp_synchronized_clock | 1830 | 1104 | 726 | 48.64% |
| 60m | combined_synchronized_clock | 1830 | 1093 | 737 | 48.40% |
| 15m | perp_original_clock | 1830 | 1104 | 726 | 47.74% |
| 15m | perp_synchronized_clock | 1830 | 1104 | 726 | 47.74% |
| 15m | combined_synchronized_clock | 1830 | 1093 | 737 | 47.03% |

## Data usability pilots

- Options: 483 captures; usable 7d RR25 in 403, usable 30d RR25 in 153; 372 valid hourly changes.
- Liquidations: 1329 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1827}`.
- Exchange stress: 965/965 scheduled records. Capture states: `{"missed": 44, "ok": 921}`. Ratings: `{"low": 921}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
