# Market study operational health

Generated 2026-10-26T01:16:05.789Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
- range: 6 consecutive closed opportunities missed
- paired: 2 consecutive closed opportunities missed

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 3/5 | 60.0% | 1 |
| range | 0/6 | 0.0% | 6 |
| state | 7/23 | 30.4% | 0 |
| paired | 27/93 | 29.0% | 2 |
| stress | 16/47 | 34.0% | 1 |
| liquidations | 26/81 | 32.1% | 0 |
| options | 23/23 | 100.0% | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- turnover: last-24h operational coverage below 80% (not a research threshold)
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 39 scored forecasts; 25 unique entries; 17 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.
