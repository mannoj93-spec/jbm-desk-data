# Market studies

Generated 2026-11-10T20:02:19.153Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 103 | 66 | 66 |
| range | collecting (descriptive) | 103 | 60 | 54 |
| state | collecting (descriptive) | 411 | 288 | 287 |
| paired | collecting (descriptive) | 1641 | 1547 | 1541 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 0.0650591 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00459552 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000687495 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.000811162 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -5.31% | 13.28% | 62.13% | 5.62% | 111.414 | 725.653 |
| ordinary/B2_10 | -5.74% | 14.21% | 61.55% | 6.07% | 87.6038 | 656.413 |
| ordinary/VOL_05 | -3.92% | 16.73% | 42.58% | 4.58% | 15.6766 | 78.3691 |
| ordinary/VOL_10 | -3.78% | 15.50% | 43.76% | 4.38% | 13.1375 | 65.5761 |
| stressed/B2_05 | -5.75% | 13.26% | 62.14% | 6.01% | 111.423 | 1175.49 |
| stressed/B2_10 | -6.08% | 14.14% | 61.56% | 6.36% | 87.6184 | 1009.79 |
| stressed/VOL_05 | -3.98% | 16.70% | 42.58% | 4.60% | 15.6862 | 142.3 |
| stressed/VOL_10 | -3.83% | 15.48% | 43.77% | 4.39% | 13.1537 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.67% | 0.0290652 |
| calibrated | 64.81% | 0.0240707 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1541 | 951 | 590 | 48.79% |
| 60m | perp_synchronized_clock | 1541 | 951 | 590 | 48.79% |
| 60m | combined_synchronized_clock | 1541 | 939 | 602 | 48.88% |
| 15m | perp_original_clock | 1541 | 951 | 590 | 47.21% |
| 15m | perp_synchronized_clock | 1541 | 951 | 590 | 47.21% |
| 15m | combined_synchronized_clock | 1541 | 939 | 602 | 46.54% |

## Data usability pilots

- Options: 410 captures; usable 7d RR25 in 343, usable 30d RR25 in 97; 317 valid hourly changes.
- Liquidations: 1113 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1539}`.
- Exchange stress: 821/821 scheduled records. Capture states: `{"missed": 43, "ok": 778}`. Ratings: `{"low": 778}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
