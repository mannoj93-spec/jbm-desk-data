# Market study operational health

Generated 2026-10-27T17:46:57.125Z. Integrity: ok.

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
| state | 19/24 | 79.2% | 0 |
| paired | 91/93 | 97.8% | 0 |
| state_v2 | 18/18 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 96/96 | 100.0% | 0 |
| options | 18/23 | 78.3% | 0 |

turnover: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 24/24 closed opportunities recorded; 19 eligible forecasts; 5 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 91 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 18/18 closed opportunities recorded; 18 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 10/10 | 0 |
| range | 10/10 | 0 |
| state | 33/41 | 0 |
| paired | 159/161 | 3 |
| stress | 81/81 | 1 |
| liquidations | 164/164 | 0 |
| options | 35/40 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 5/24 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 196 scored forecasts; 155 unique entries; 53 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.05.
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 41 forecasts, 8 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 5: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 18 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.058333333333334 / 16.3.

Selected rr25_7d legs: 19 usable captures, 76 leg observations. Quote age median (ms): 4570.0; relative spread median: 0.08333333333333337. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4529.5; relative spread median: 0.0563492063492062. Repeated legs and horizons are dependent; missing sizes stay unavailable.
