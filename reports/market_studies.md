# Market studies

Generated 2026-11-18T06:47:14.929Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 147 | 111 | 111 |
| range | collecting (descriptive) | 147 | 104 | 98 |
| state | collecting (descriptive) | 589 | 352 | 351 |
| paired | collecting (descriptive) | 2356 | 2258 | 2253 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0465747 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00404914 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.000349597 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000998668 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -10.04% | 14.64% | 52.12% | 10.57% | 99.1034 | 897.363 |
| ordinary/B2_10 | -10.10% | 14.49% | 51.27% | 10.65% | 73.0349 | 815.177 |
| ordinary/VOL_05 | -8.19% | 16.51% | 39.04% | 9.09% | 13.8517 | 98.0562 |
| ordinary/VOL_10 | -7.59% | 15.38% | 39.89% | 8.49% | 9.25987 | 65.5761 |
| stressed/B2_05 | -10.57% | 14.64% | 52.13% | 11.04% | 99.1696 | 1460.41 |
| stressed/B2_10 | -10.49% | 14.46% | 51.28% | 10.98% | 73.0893 | 1229.59 |
| stressed/VOL_05 | -8.26% | 16.49% | 39.05% | 9.12% | 13.8589 | 178.068 |
| stressed/VOL_10 | -7.64% | 15.37% | 39.90% | 8.50% | 9.27169 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 65.31% | 0.0338796 |
| calibrated | 64.29% | 0.0317935 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2253 | 1338 | 915 | 48.21% |
| 60m | perp_synchronized_clock | 2253 | 1338 | 915 | 48.21% |
| 60m | combined_synchronized_clock | 2253 | 1318 | 935 | 48.33% |
| 15m | perp_original_clock | 2253 | 1338 | 915 | 47.91% |
| 15m | perp_synchronized_clock | 2253 | 1338 | 915 | 47.91% |
| 15m | combined_synchronized_clock | 2253 | 1318 | 935 | 46.89% |

## Data usability pilots

- Options: 589 captures; usable 7d RR25 in 503, usable 30d RR25 in 259; 459 valid hourly changes.
- Liquidations: 1647 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 2251}`.
- Exchange stress: 1178/1178 scheduled records. Capture states: `{"missed": 45, "ok": 1133}`. Ratings: `{"low": 1133}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
