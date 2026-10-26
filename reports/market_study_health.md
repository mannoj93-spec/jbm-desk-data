# Market study operational health

Generated 2026-10-26T16:21:51.710Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 4/5 | 80.0% | 0 |
| range | 3/5 | 60.0% | 0 |
| state | 17/23 | 73.9% | 0 |
| paired | 72/94 | 76.6% | 0 |
| stress | 38/47 | 80.9% | 0 |
| liquidations | 76/92 | 82.6% | 0 |
| options | 23/23 | 100.0% | 0 |

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 3/3 | 1 |
| range | 3/3 | 1 |
| state | 13/15 | 0 |
| paired | 60/60 | 2 |
| stress | 30/30 | 1 |
| liquidations | 60/60 | 4 |
| options | 15/15 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 97 scored forecasts; 70 unique entries; 30 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 3 abstentions; 4 unavailable depth ages. Median/max age in minutes: 16.1 / 31.116666666666667.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 16 forecasts, 3 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.116666666666667.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4743.5; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4740.0; relative spread median: 0.06451612903225812. Repeated legs and horizons are dependent; missing sizes stay unavailable.
