# Market study operational health

Generated 2026-10-27T14:01:25.601Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
- options: consecutive capture opportunities missed or unusable

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 6/6 | 100.0% | 0 |
| range | 6/6 | 100.0% | 0 |
| state | 18/23 | 78.3% | 0 |
| paired | 91/93 | 97.8% | 0 |
| state_v2 | 14/14 | 100.0% | 0 |
| stress | 46/46 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options | 20/22 | 90.9% | 2 |

turnover: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 18 eligible forecasts; 5 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 91 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 14/14 closed opportunities recorded; 14 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 9/9 | 0 |
| range | 9/9 | 0 |
| state | 30/37 | 1 |
| paired | 144/146 | 3 |
| stress | 73/73 | 2 |
| liquidations | 148/148 | 4 |
| options | 34/36 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 5/23 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 181 scored forecasts; 143 unique entries; 50 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.05.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 38 forecasts, 7 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 5: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 15 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 16.3.

Selected rr25_7d legs: 21 usable captures, 84 leg observations. Quote age median (ms): 4600.5; relative spread median: 0.0833333333333334. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4642.0; relative spread median: 0.054054054054054106. Repeated legs and horizons are dependent; missing sizes stay unavailable.
