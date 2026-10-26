# Market study operational health

Generated 2026-10-26T06:01:06.856Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 4/6 | 66.7% | 0 |
| range | 1/6 | 16.7% | 0 |
| state | 11/23 | 47.8% | 0 |
| paired | 41/93 | 44.1% | 0 |
| stress | 23/46 | 50.0% | 0 |
| liquidations | 46/86 | 53.5% | 0 |
| options | 22/22 | 100.0% | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- turnover: last-24h operational coverage below 80% (not a research threshold)
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 56 scored forecasts; 38 unique entries; 21 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.
