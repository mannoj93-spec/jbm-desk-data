# Market study operational health

Generated 2026-10-31T10:17:01.821Z. Integrity: ok.

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
| state | 19/23 | 82.6% | 0 |
| paired | 93/93 | 100.0% | 0 |
| state_v2 | 23/23 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options capture | 23/23 | 100.0% | 0 |
| options usability rr25_7d | 23/23 | 100.0% | 0 |
| options usability rr25_30d | 0/23 | 0.0% | 23 |

turnover: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 19 eligible forecasts; 4 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 93 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 23/23 closed opportunities recorded; 23 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 32/32 | 0 |
| range | 32/32 | 0 |
| state | 100/129 | 0 |
| paired | 513/515 | 3 |
| stress | 258/258 | 1 |
| liquidations | 516/516 | 4 |
| options | 50/129 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- options rr25_30d: 0/23 closed opportunities usable (<80%; quality warning, not a collection outage)
- 3 retained source-quality incidents; affected score windows are listed without changing results

Paired study: 551 scored forecasts; 453 unique entries; 131 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.0 / 31.016666666666666.
- 4: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 130 forecasts, 30 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.116666666666667.
- 11: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 19: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 24 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 15.966666666666667 / 16.133333333333333.

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4907.0; relative spread median: 0.06451612903225812. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 0 usable captures, 0 leg observations. Quote age median (ms): None; relative spread median: None. Repeated legs and horizons are dependent; missing sizes stay unavailable.

State v2 numerical replay: verified, 102 scores reproduced.

## Source quality

Zero trades and a flat last price are a source-quality anomaly, not proof of an exchange outage. Overlapping windows are not independent. Frozen scores and input eligibility remain unchanged.
- binance_klines_1m_BTCUSDT_perp: 36 flat zero-trade minutes; recovered; 26 overlapping score windows (including dependent arms). Incident binance_klines_1m_BTCUSDT_perp-1793059320000; cross-feed differences in bp: {'spot': 27.71648511836311, 'mark': 23.96204444522043}.
- binance_klines_1m_ETHUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_ETHUSDT_perp-1793059320000; cross-feed differences in bp: {}.
- binance_klines_1m_SOLUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_SOLUSDT_perp-1793059320000; cross-feed differences in bp: {}.

Separate options expiry pilot: active. [Prospective feasibility report](options_expiry_pilot.md).
