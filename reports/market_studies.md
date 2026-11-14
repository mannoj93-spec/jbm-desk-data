# Market studies

Generated 2026-11-14T14:32:00.363Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 125 | 89 | 89 |
| range | collecting (descriptive) | 125 | 83 | 77 |
| state | collecting (descriptive) | 501 | 324 | 320 |
| paired | collecting (descriptive) | 2003 | 1908 | 1902 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0989787 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00450326 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000512409 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.000295741 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -8.43% | 14.24% | 56.71% | 8.86% | 105.266 | 807.014 |
| ordinary/B2_10 | -8.52% | 14.36% | 55.95% | 8.92% | 81.7507 | 731.91 |
| ordinary/VOL_05 | -7.06% | 17.02% | 41.19% | 7.82% | 15.0258 | 91.4039 |
| ordinary/VOL_10 | -6.52% | 15.41% | 41.62% | 7.21% | 10.7876 | 65.5761 |
| stressed/B2_05 | -8.92% | 14.22% | 56.71% | 9.30% | 105.31 | 1322.62 |
| stressed/B2_10 | -8.90% | 14.31% | 55.97% | 9.24% | 81.7886 | 1131.69 |
| stressed/VOL_05 | -7.13% | 17.00% | 41.20% | 7.84% | 15.0343 | 165.985 |
| stressed/VOL_10 | -6.57% | 15.39% | 41.64% | 7.23% | 10.8012 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.23% | 0.0319323 |
| calibrated | 64.94% | 0.0282369 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1902 | 1143 | 759 | 49.08% |
| 60m | perp_synchronized_clock | 1902 | 1143 | 759 | 49.08% |
| 60m | combined_synchronized_clock | 1902 | 1132 | 770 | 48.85% |
| 15m | perp_original_clock | 1902 | 1143 | 759 | 47.42% |
| 15m | perp_synchronized_clock | 1902 | 1143 | 759 | 47.42% |
| 15m | combined_synchronized_clock | 1902 | 1132 | 770 | 46.82% |

## Data usability pilots

- Options: 501 captures; usable 7d RR25 in 421, usable 30d RR25 in 171; 390 valid hourly changes.
- Liquidations: 1383 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1899}`.
- Exchange stress: 1002/1002 scheduled records. Capture states: `{"missed": 44, "ok": 958}`. Ratings: `{"low": 958}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
