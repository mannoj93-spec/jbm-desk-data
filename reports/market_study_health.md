# Market study operational health

Generated 2026-10-26T04:55:43.763Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 3/5 | 60.0% | 0 |
| range | 1/6 | 16.7% | 0 |
| state | 10/24 | 41.7% | 0 |
| paired | 37/94 | 39.4% | 0 |
| stress | 21/47 | 44.7% | 0 |
| liquidations | 42/88 | 47.7% | 0 |
| options | 23/23 | 100.0% | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- turnover: last-24h operational coverage below 80% (not a research threshold)
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 51 scored forecasts; 35 unique entries; 20 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.
