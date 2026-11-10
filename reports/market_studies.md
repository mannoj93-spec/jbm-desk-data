# Market studies

Generated 2026-11-10T10:32:11.958Z. Paper research only. Missing outcomes are never zero.

| Study | Status | Scheduled | On-time published | Scored / executed |
|---|---|---:|---:|---:|
| turnover | collecting (descriptive) | 100 | 64 | 64 |
| range | collecting (descriptive) | 100 | 58 | 52 |
| state | collecting (descriptive) | 401 | 284 | 280 |
| paired | collecting (descriptive) | 1603 | 1509 | 1504 |

## Primary comparisons

Turnover: higher is better. Range and probability scores: lower is better. A dash means unavailable, not zero.

| Study | Paired difference | 90% block interval | First verified launch |
|---|---:|---|---|
| turnover | -0.0995687 | — (insufficient blocks) | 2026-10-24T21:12:42.213Z |
| range | 0.00486312 | — (insufficient blocks) | 2026-10-26T04:19:34.052Z |
| state | -0.000234726 | — (insufficient blocks) | 2026-10-24T21:12:41.518Z |
| paired | -0.00049867 | — (insufficient blocks) | 2026-10-24T18:31:17.940Z |

## Turnover accounts

Returns, costs and turnover below cover closed intervals. Each latest trade opens a still-pending interval.

| Scenario / arm | Net return | Annualized risk | Exposure | Drawdown | Annual turnover | Costs (USDT) |
|---|---:|---:|---:|---:|---:|---:|
| ordinary/B2_05 | -4.86% | 13.40% | 62.76% | 5.43% | 107.055 | 693.946 |
| ordinary/B2_10 | -5.36% | 14.38% | 62.27% | 5.95% | 87.0698 | 645.645 |
| ordinary/VOL_05 | -3.40% | 16.87% | 42.77% | 4.35% | 15.9843 | 78.3691 |
| ordinary/VOL_10 | -3.26% | 15.61% | 43.97% | 4.14% | 13.3955 | 65.5761 |
| stressed/B2_05 | -5.27% | 13.37% | 62.77% | 5.78% | 107.074 | 1118.12 |
| stressed/B2_10 | -5.69% | 14.31% | 62.28% | 6.23% | 87.0836 | 990.266 |
| stressed/VOL_05 | -3.47% | 16.84% | 42.78% | 4.36% | 15.994 | 142.3 |
| stressed/VOL_10 | -3.31% | 15.59% | 43.99% | 4.15% | 13.4121 | 119.284 |

## Range calibration

| Arm | 80% interval coverage | Mean interval width (ln H/L) |
|---|---:|---:|
| control | 67.31% | 0.0285525 |
| calibrated | 63.46% | 0.0234324 |

## Paired-flow direction checks

Conditional hit rates exclude neutral signals. Scored and neutral counts stay visible; scheduled coverage is above.

| Horizon | Arm | Scored | Directional | Neutral | Conditional hit rate |
|---|---|---:|---:|---:|---:|
| 60m | perp_original_clock | 1504 | 927 | 577 | 48.54% |
| 60m | perp_synchronized_clock | 1504 | 927 | 577 | 48.54% |
| 60m | combined_synchronized_clock | 1504 | 915 | 589 | 48.52% |
| 15m | perp_original_clock | 1504 | 927 | 577 | 47.03% |
| 15m | perp_synchronized_clock | 1504 | 927 | 577 | 47.03% |
| 15m | combined_synchronized_clock | 1504 | 915 | 589 | 46.34% |

## Data usability pilots

- Options: 401 captures; usable 7d RR25 in 343, usable 30d RR25 in 88; 317 valid hourly changes.
- Liquidations: 1083 comparable first/later vintage pairs; 0 direction changes. Capture states: `{"coverage-unknown": 10, "missed": 66, "ok": 1499}`.
- Exchange stress: 802/802 scheduled records. Capture states: `{"missed": 43, "ok": 759}`. Ratings: `{"low": 759}`.

These pilots measure availability and revisions; they are not predictive evidence. Unknown source coverage is never zero activity.

The JSON companion retains all exclusions, model comparisons, clock comparisons, insurance variation and per-expiry detail.
A registration is not a launch. Launch dates require verified on-time forecasts or a verified paper execution.
No study is promoted automatically. See [the frozen rules and checkpoints](../docs/MARKET_STUDIES.md).
