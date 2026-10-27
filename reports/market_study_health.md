# Market study operational health

Generated 2026-10-27T00:19:54.489Z. Integrity: ok.

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
| state | 18/23 | 78.3% | 0 |
| paired | 91/93 | 97.8% | 0 |
| state_v2 | 0/0 | — | 0 |
| stress | 46/47 | 97.9% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options | 23/23 | 100.0% | 0 |

turnover: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 18 eligible forecasts; 5 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 91 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 0/0 closed opportunities recorded; 0 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 5/5 | 1 |
| range | 5/5 | 1 |
| state | 18/23 | 1 |
| paired | 91/91 | 2 |
| stress | 46/46 | 1 |
| liquidations | 92/92 | 4 |
| options | 23/23 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 5/23 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 129 scored forecasts; 97 unique entries; 37 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 1 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.1 / 16.1.

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4736.5; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4736.0; relative spread median: 0.0606617647058824. Repeated legs and horizons are dependent; missing sizes stay unavailable.
