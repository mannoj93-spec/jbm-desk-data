# Market study operational health

Generated 2026-10-27T16:20:18.178Z. Integrity: ok.

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
| state | 18/23 | 78.3% | 1 |
| paired | 92/94 | 97.9% | 0 |
| state_v2 | 16/16 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options | 18/23 | 78.3% | 5 |

turnover: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 18 eligible forecasts; 5 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 94/94 closed opportunities recorded; 92 eligible forecasts; 2 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 16/16 closed opportunities recorded; 16 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: newer verified success; the current miss alert is cleared. Historical misses remain.

options: newer verified success; the current miss alert is cleared. Historical misses remain.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 9/9 | 1 |
| range | 9/9 | 1 |
| state | 31/39 | 1 |
| paired | 154/156 | 2 |
| stress | 78/78 | 1 |
| liquidations | 156/156 | 4 |
| options | 34/39 | 1 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 5/23 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)

Paired study: 191 scored forecasts; 151 unique entries; 52 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.05.
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 40 forecasts, 8 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.083333333333332 / 31.116666666666667.
- 5: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 17 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 16.3.

Selected rr25_7d legs: 19 usable captures, 76 leg observations. Quote age median (ms): 4600.5; relative spread median: 0.08333333333333337. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4589.5; relative spread median: 0.05555555555555541. Repeated legs and horizons are dependent; missing sizes stay unavailable.
