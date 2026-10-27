# Market study operational health

Generated 2026-10-27T04:11:44.916Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 5/5 | 100.0% | 0 |
| range | 5/5 | 100.0% | 0 |
| state | 19/23 | 82.6% | 0 |
| paired | 92/94 | 97.9% | 0 |
| state_v2 | 4/4 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options | 23/23 | 100.0% | 0 |

turnover: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 19 eligible forecasts; 4 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 94/94 closed opportunities recorded; 92 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 4/4 closed opportunities recorded; 4 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 6/6 | 1 |
| range | 6/6 | 1 |
| state | 22/27 | 1 |
| paired | 105/107 | 2 |
| stress | 54/54 | 1 |
| liquidations | 108/108 | 4 |
| options | 27/27 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
None.

Paired study: 142 scored forecasts; 109 unique entries; 41 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 4 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.05.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 28 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 5 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.15 / 16.3.

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4679.5; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4680.0; relative spread median: 0.05555555555555541. Repeated legs and horizons are dependent; missing sizes stay unavailable.
