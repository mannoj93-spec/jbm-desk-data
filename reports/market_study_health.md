# Market study operational health

Generated 2026-10-26T20:46:44.475Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 5/5 | 100.0% | 0 |
| range | 5/6 | 83.3% | 0 |
| state | 17/24 | 70.8% | 1 |
| paired | 83/93 | 89.2% | 0 |
| stress | 43/47 | 91.5% | 0 |
| liquidations | 88/96 | 91.7% | 0 |
| options | 23/23 | 100.0% | 0 |

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 4/4 | 1 |
| range | 5/5 | 0 |
| state | 15/20 | 0 |
| paired | 77/77 | 3 |
| stress | 39/39 | 1 |
| liquidations | 80/80 | 0 |
| options | 19/19 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 115 scored forecasts; 85 unique entries; 34 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 2 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 20 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4857.0; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4839.0; relative spread median: 0.06250000000000006. Repeated legs and horizons are dependent; missing sizes stay unavailable.
