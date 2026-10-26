# Market study operational health

Generated 2026-10-26T12:19:34.104Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 4/5 | 80.0% | 0 |
| range | 2/5 | 40.0% | 0 |
| state | 15/23 | 65.2% | 0 |
| paired | 59/93 | 63.4% | 0 |
| stress | 33/47 | 70.2% | 0 |
| liquidations | 64/92 | 69.6% | 0 |
| options | 23/23 | 100.0% | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 81 scored forecasts; 57 unique entries; 26 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.
