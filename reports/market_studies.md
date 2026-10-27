# Market studies

Generated 2026-10-27T09:16:30.610Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 16 | 14 | 14 |
| range | collecting (descriptive) | 16 | 8 | 1 |
| state | collecting (descriptive) | 64 | 39 | 35 |
| paired | collecting (descriptive) | 254 | 168 | 163 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | 1.56202 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | -0.00643804 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | 0.00456419 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | 0.0115031 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -0.47% | 10.31% | 48.88% | 0.84% | 160.423 | 118.904 |
| ordinary/B2_10 | -0.38% | 10.12% | 49.56% | 0.77% | 101.116 | 74.9863 |
| ordinary/VOL_05 | -0.33% | 9.35% | 47.49% | 0.67% | 70.4009 | 52.2225 |
| ordinary/VOL_10 | -0.33% | 9.35% | 47.49% | 0.67% | 70.4009 | 52.2225 |
| stressed/B2_05 | -0.56% | 10.18% | 48.88% | 0.88% | 160.597 | 216.219 |
| stressed/B2_10 | -0.45% | 9.91% | 49.58% | 0.78% | 101.257 | 136.413 |
| stressed/VOL_05 | -0.37% | 9.18% | 47.51% | 0.67% | 70.4921 | 94.9864 |
| stressed/VOL_10 | -0.37% | 9.18% | 47.51% | 0.67% | 70.4921 | 94.9864 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 100.00% | 0.0326025 |
| calibrated | 100.00% | 0.0261645 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 163 | 96 | 67 | 51.04% |
| 60m | perp_synchronized_clock | 163 | 96 | 67 | 51.04% |
| 60m | combined_synchronized_clock | 163 | 102 | 61 | 48.04% |
| 15m | perp_original_clock | 163 | 96 | 67 | 43.75% |
| 15m | perp_synchronized_clock | 163 | 96 | 67 | 43.75% |
| 15m | combined_synchronized_clock | 163 | 102 | 61 | 42.16% |

## Data usability pilots

- Options: 64 captures; usable 7d RR25 in 64, usable 30d RR25 in 64; 61 valid hourly changes.
- Liquidations: 94 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"missed": 58, "ok": 169}`.
- Exchange stress: 127/127 scheduled records. Capture states: `{"missed": 39, "ok": 88}`. Ratings: `{"low": 88}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
