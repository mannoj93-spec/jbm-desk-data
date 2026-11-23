# Market studies

Generated 2026-11-23T08:02:43.851Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 178 | 140 | 140 |
| range | collecting (descriptive) | 178 | 133 | 127 |
| state | collecting (descriptive) | 711 | 377 | 377 |
| paired | collecting (descriptive) | 2841 | 2743 | 2738 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.326467 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 2.88907e-05 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00198816 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00125548 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -11.60% | 16.55% | 47.56% | 13.92% | 88.4985 | 939.242 |
| ordinary/B2_10 | -11.11% | 15.12% | 46.17% | 13.13% | 61.446 | 815.177 |
| ordinary/VOL_05 | -9.38% | 17.27% | 36.59% | 11.99% | 11.6354 | 98.0562 |
| ordinary/VOL_10 | -8.99% | 17.37% | 38.03% | 11.91% | 7.77549 | 65.5761 |
| stressed/B2_05 | -12.15% | 16.56% | 47.57% | 14.39% | 88.587 | 1536 |
| stressed/B2_10 | -11.49% | 15.10% | 46.18% | 13.45% | 61.5127 | 1229.59 |
| stressed/VOL_05 | -9.45% | 17.26% | 36.59% | 12.02% | 11.6419 | 178.068 |
| stressed/VOL_10 | -9.04% | 17.36% | 38.04% | 11.93% | 7.7855 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 66.14% | 0.0368791 |
| calibrated | 67.72% | 0.0374191 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 2738 | 1565 | 1173 | 48.37% |
| 60m | perp_synchronized_clock | 2738 | 1565 | 1173 | 48.37% |
| 60m | combined_synchronized_clock | 2738 | 1538 | 1200 | 48.57% |
| 15m | perp_original_clock | 2738 | 1565 | 1173 | 48.95% |
| 15m | perp_synchronized_clock | 2738 | 1565 | 1173 | 48.95% |
| 15m | combined_synchronized_clock | 2738 | 1538 | 1200 | 48.05% |

## Data usability pilots

- Options: 709 captures; usable 7d RR25 in 606, usable 30d RR25 in 365; 553 valid hourly changes.
- Liquidations: 2010 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 14, "missed": 66, "ok": 2735}`.
- Exchange stress: 1421/1421 scheduled records. Capture states: `{"missed": 45, "ok": 1376}`. Ratings: `{"low": 1376}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
