# Market studies

Generated 2026-11-07T16:46:40.007Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 84 | 48 | 48 |
| range | collecting (descriptive) | 84 | 42 | 36 |
| state | collecting (descriptive) | 335 | 240 | 236 |
| paired | collecting (descriptive) | 1340 | 1246 | 1240 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.129338 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00459879 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.00133121 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.0015625 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -3.81% | 13.76% | 64.52% | 4.13% | 97.3189 | 444.383 |
| ordinary/B2_10 | -4.29% | 14.98% | 64.27% | 4.63% | 79.4216 | 408.474 |
| ordinary/VOL_05 | -2.97% | 18.93% | 44.58% | 3.74% | 18.9611 | 78.3691 |
| ordinary/VOL_10 | -2.82% | 17.41% | 46.02% | 3.54% | 15.8929 | 65.5761 |
| stressed/B2_05 | -4.13% | 13.70% | 64.52% | 4.40% | 97.3376 | 771.187 |
| stressed/B2_10 | -4.55% | 14.90% | 64.28% | 4.84% | 79.4286 | 675.012 |
| stressed/VOL_05 | -3.03% | 18.88% | 44.59% | 3.75% | 18.9719 | 142.3 |
| stressed/VOL_10 | -2.88% | 17.38% | 46.04% | 3.54% | 15.9121 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 75.00% | 0.0301162 |
| calibrated | 72.22% | 0.0241027 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1240 | 753 | 487 | 48.87% |
| 60m | perp_synchronized_clock | 1240 | 753 | 487 | 48.87% |
| 60m | combined_synchronized_clock | 1240 | 742 | 498 | 49.19% |
| 15m | perp_original_clock | 1240 | 753 | 487 | 46.88% |
| 15m | perp_synchronized_clock | 1240 | 753 | 487 | 46.88% |
| 15m | combined_synchronized_clock | 1240 | 742 | 498 | 46.36% |

## Data usability pilots

- Options: 335 captures; usable 7d RR25 in 280, usable 30d RR25 in 86; 256 valid hourly changes.
- Liquidations: 893 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 2, "missed": 66, "ok": 1243}`.
- Exchange stress: 670/670 scheduled records. Capture states: `{"missed": 43, "ok": 627}`. Ratings: `{"low": 627}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
