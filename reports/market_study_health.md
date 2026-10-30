# Market study operational health

Generated 2026-10-30T02:47:06.230Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
- state: 2 consecutive closed opportunities missed

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 6/6 | 100.0% | 0 |
| range | 6/6 | 100.0% | 0 |
| state | 16/24 | 66.7% | 2 |
| paired | 93/93 | 100.0% | 0 |
| state_v2 | 24/24 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 96/96 | 100.0% | 0 |
| options capture | 23/23 | 100.0% | 0 |
| options usability rr25_7d | 16/23 | 69.6% | 0 |
| options usability rr25_30d | 0/23 | 0.0% | 23 |

turnover: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 6/6 closed opportunities recorded; 6 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 24/24 closed opportunities recorded; 16 eligible forecasts; 8 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 93 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 24/24 closed opportunities recorded; 24 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 24/24 | 0 |
| range | 24/24 | 0 |
| state | 76/98 | 0 |
| paired | 387/389 | 3 |
| stress | 195/195 | 1 |
| liquidations | 392/392 | 0 |
| options | 50/97 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 8/24 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)
- options rr25_7d: 16/23 closed opportunities usable (<80%; quality warning, not a collection outage)
- options rr25_30d: 0/23 closed opportunities usable (<80%; quality warning, not a collection outage)
- 3 retained source-quality incidents; affected score windows are listed without changing results

Paired study: 425 scored forecasts; 351 unique entries; 103 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 8 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.1.
- 6: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)

State depth (since_deployment): 98 forecasts, 22 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.116666666666667.
- 9: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 13: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (state_v2_last_24h): 24 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 15.991666666666667 / 16.1.

Selected rr25_7d legs: 17 usable captures, 68 leg observations. Quote age median (ms): 5652.0; relative spread median: 0.09523809523809516. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 0 usable captures, 0 leg observations. Quote age median (ms): None; relative spread median: None. Repeated legs and horizons are dependent; missing sizes stay unavailable.

State v2 numerical replay: verified, 71 scores reproduced.

## Source quality

Zero trades and a flat last price are a source-quality anomaly, not proof of an exchange outage. Overlapping windows are not independent. Frozen scores and input eligibility remain unchanged.
- binance_klines_1m_BTCUSDT_perp: 36 flat zero-trade minutes; recovered; 26 overlapping score windows (including dependent arms). Incident binance_klines_1m_BTCUSDT_perp-1793059320000; cross-feed differences in bp: {'spot': 27.71648511836311, 'mark': 23.96204444522043}.
- binance_klines_1m_ETHUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_ETHUSDT_perp-1793059320000; cross-feed differences in bp: {}.
- binance_klines_1m_SOLUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_SOLUSDT_perp-1793059320000; cross-feed differences in bp: {}.

Separate options expiry pilot: active. [Prospective feasibility report](options_expiry_pilot.md).
