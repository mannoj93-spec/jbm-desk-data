# Market study operational health

Generated 2026-10-27T23:01:25.423Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 6/6 | 100.0% | 0 |
| range | 6/6 | 100.0% | 0 |
| state | 18/23 | 78.3% | 0 |
| paired | 91/93 | 97.8% | 0 |
| state_v2 | 23/23 | 100.0% | 0 |
| stress | 46/46 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options | 17/22 | 77.3% | 0 |

turnover: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 18 eligible forecasts; 5 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 91 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 23/23 closed opportunities recorded; 23 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 11/11 | 0 |
| range | 11/11 | 0 |
| state | 36/46 | 1 |
| paired | 180/182 | 3 |
| stress | 91/91 | 2 |
| liquidations | 184/184 | 4 |
| options | 40/45 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 5/23 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 218 scored forecasts; 174 unique entries; 58 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.0.
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 47 forecasts, 10 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.116666666666667.
- 6: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 4: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 24 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.025 / 16.3.

Selected rr25_7d legs: 19 usable captures, 76 leg observations. Quote age median (ms): 4600.5; relative spread median: 0.0833333333333334. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4598.5; relative spread median: 0.05555555555555541. Repeated legs and horizons are dependent; missing sizes stay unavailable.
