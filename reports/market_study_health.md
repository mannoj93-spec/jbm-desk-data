# Market study operational health

Generated 2026-10-26T17:01:18.421Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 4/5 | 80.0% | 0 |
| range | 4/6 | 66.7% | 0 |
| state | 16/23 | 69.6% | 1 |
| paired | 73/93 | 78.5% | 0 |
| stress | 38/46 | 82.6% | 0 |
| liquidations | 76/92 | 82.6% | 0 |
| options | 22/22 | 100.0% | 0 |

state: newer verified success; the current miss alert is cleared. Historical misses remain.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 3/3 | 1 |
| range | 4/4 | 0 |
| state | 13/16 | 1 |
| paired | 62/62 | 3 |
| stress | 31/31 | 2 |
| liquidations | 64/64 | 4 |
| options | 15/15 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 100 scored forecasts; 73 unique entries; 31 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 3 abstentions; 4 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.116666666666667.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 17 forecasts, 3 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4743.5; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4740.0; relative spread median: 0.06451612903225812. Repeated legs and horizons are dependent; missing sizes stay unavailable.
