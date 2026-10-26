# Market study operational health

Generated 2026-10-26T21:52:45.839Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 6/6 | 100.0% | 0 |
| range | 5/6 | 83.3% | 0 |
| state | 18/24 | 75.0% | 0 |
| paired | 86/94 | 91.5% | 0 |
| stress | 44/47 | 93.6% | 0 |
| liquidations | 92/96 | 95.8% | 0 |
| options | 23/23 | 100.0% | 0 |

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 5/5 | 0 |
| range | 5/5 | 0 |
| state | 16/21 | 0 |
| paired | 82/82 | 2 |
| stress | 41/41 | 1 |
| liquidations | 84/84 | 0 |
| options | 20/20 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 118 scored forecasts; 88 unique entries; 35 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 1 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 21 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4857.0; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4839.0; relative spread median: 0.06250000000000006. Repeated legs and horizons are dependent; missing sizes stay unavailable.
