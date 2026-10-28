# Market study operational health

Generated 2026-10-28T16:02:05.407Z. Integrity: ok.

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
| state | 19/23 | 82.6% | 2 |
| paired | 93/93 | 100.0% | 0 |
| state_v2 | 23/23 | 100.0% | 0 |
| stress | 46/46 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options capture | 22/22 | 100.0% | 0 |
| options usability rr25_7d | 15/22 | 68.2% | 7 |
| options usability rr25_30d | 15/22 | 68.2% | 7 |

turnover: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 19 eligible forecasts; 4 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 93 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 23/23 closed opportunities recorded; 23 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: newer verified success; the current miss alert is cleared. Historical misses remain.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 15/15 | 0 |
| range | 15/15 | 0 |
| state | 51/63 | 1 |
| paired | 248/250 | 3 |
| stress | 125/125 | 2 |
| liquidations | 252/252 | 4 |
| options | 50/62 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- options rr25_7d: 15/22 closed opportunities usable (<80%; quality warning, not a collection outage)
- options rr25_30d: 15/22 closed opportunities usable (<80%; quality warning, not a collection outage)
- 3 retained source-quality incidents; affected score windows are listed without changing results

Paired study: 286 scored forecasts; 232 unique entries; 72 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 4 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.066666666666666.
- 2: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 64 forecasts, 12 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.075 / 31.116666666666667.
- 7: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 5: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 24 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.05 / 16.15.

Selected rr25_7d legs: 16 usable captures, 64 leg observations. Quote age median (ms): 4931.5; relative spread median: 0.09090909090909097. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 16 usable captures, 64 leg observations. Quote age median (ms): 4929.0; relative spread median: 0.05714285714285699. Repeated legs and horizons are dependent; missing sizes stay unavailable.

State v2 numerical replay: verified, 36 scores reproduced.

## Source quality

Zero trades and a flat last price are a source-quality anomaly, not proof of an exchange outage. Overlapping windows are not independent. Frozen scores and input eligibility remain unchanged.
- binance_klines_1m_BTCUSDT_perp: 36 flat zero-trade minutes; recovered; 26 overlapping score windows (including dependent arms). Incident binance_klines_1m_BTCUSDT_perp-1793059320000; cross-feed differences in bp: {'spot': 27.71648511836311, 'mark': 23.96204444522043}.
- binance_klines_1m_ETHUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_ETHUSDT_perp-1793059320000; cross-feed differences in bp: {}.
- binance_klines_1m_SOLUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_SOLUSDT_perp-1793059320000; cross-feed differences in bp: {}.

Separate options expiry pilot: active. [Prospective feasibility report](options_expiry_pilot.md).
