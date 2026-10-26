# Market study operational health

Generated 2026-10-26T11:01:19.713Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 4/6 | 66.7% | 0 |
| range | 2/6 | 33.3% | 0 |
| state | 15/23 | 65.2% | 0 |
| paired | 56/93 | 60.2% | 0 |
| stress | 31/46 | 67.4% | 0 |
| liquidations | 63/91 | 69.2% | 0 |
| options | 22/22 | 100.0% | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- turnover: last-24h operational coverage below 80% (not a research threshold)
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 76 scored forecasts; 54 unique entries; 25 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.
