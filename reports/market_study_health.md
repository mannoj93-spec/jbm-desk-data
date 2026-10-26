# Market study operational health

Generated 2026-10-26T13:07:38.475Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 4/5 | 80.0% | 0 |
| range | 3/6 | 50.0% | 0 |
| state | 16/23 | 69.6% | 0 |
| paired | 63/94 | 67.0% | 0 |
| stress | 35/47 | 74.5% | 0 |
| liquidations | 68/92 | 73.9% | 0 |
| options | 23/23 | 100.0% | 0 |

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 2/2 | 1 |
| range | 3/3 | 0 |
| state | 11/12 | 0 |
| paired | 47/47 | 2 |
| stress | 24/24 | 1 |
| liquidations | 48/48 | 4 |
| options | 12/12 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- range: last-24h operational coverage below 80% (not a research threshold)
- state: last-24h operational coverage below 80% (not a research threshold)
- paired: last-24h operational coverage below 80% (not a research threshold)

Paired study: 82 scored forecasts; 58 unique entries; 27 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 2 abstentions; 6 unavailable depth ages. Median/max age in minutes: 16.1 / 31.116666666666667.
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 13 forecasts, 2 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.1 / 31.116666666666667.
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4696.5; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4696.0; relative spread median: 0.06451612903225812. Repeated legs and horizons are dependent; missing sizes stay unavailable.
