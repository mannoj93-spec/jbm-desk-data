# Market study operational health

Generated 2026-10-27T09:32:22.628Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 5/5 | 100.0% | 0 |
| range | 6/6 | 100.0% | 0 |
| state | 19/24 | 79.2% | 1 |
| paired | 91/93 | 97.8% | 0 |
| state_v2 | 10/10 | 100.0% | 0 |
| stress | 46/46 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options | 23/23 | 100.0% | 0 |

turnover: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 24/24 closed opportunities recorded; 19 eligible forecasts; 5 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 91 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 10/10 closed opportunities recorded; 10 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 7/7 | 1 |
| range | 8/8 | 0 |
| state | 27/33 | 0 |
| paired | 126/128 | 3 |
| stress | 64/64 | 2 |
| liquidations | 128/128 | 4 |
| options | 32/32 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 5/24 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 164 scored forecasts; 128 unique entries; 46 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.09166666666667 / 31.05.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 33 forecasts, 6 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 4: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 10 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333336 / 16.3.

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4648.0; relative spread median: 0.0869565217391303. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4650.0; relative spread median: 0.054804804804804756. Repeated legs and horizons are dependent; missing sizes stay unavailable.
