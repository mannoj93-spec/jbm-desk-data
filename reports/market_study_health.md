# Market study operational health

Generated 2026-10-27T15:46:27.388Z. Integrity: ok.

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
| state | 18/24 | 75.0% | 1 |
| paired | 91/93 | 97.8% | 0 |
| state_v2 | 16/16 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 96/96 | 100.0% | 0 |
| options | 19/23 | 82.6% | 4 |

turnover: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 24/24 closed opportunities recorded; 18 eligible forecasts; 6 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 91 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 16/16 closed opportunities recorded; 16 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 9/9 | 0 |
| range | 9/9 | 0 |
| state | 31/39 | 0 |
| paired | 151/153 | 3 |
| stress | 77/77 | 1 |
| liquidations | 156/156 | 0 |
| options | 34/38 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 6/24 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 189 scored forecasts; 149 unique entries; 52 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 6 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.075 / 31.05.
- 3: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 39 forecasts, 8 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 5: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 16 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 16.3.

Selected rr25_7d legs: 19 usable captures, 76 leg observations. Quote age median (ms): 4600.5; relative spread median: 0.08333333333333337. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4589.5; relative spread median: 0.054054054054054106. Repeated legs and horizons are dependent; missing sizes stay unavailable.
