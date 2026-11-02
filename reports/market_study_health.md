# Market study operational health

Generated 2026-11-02T12:01:49.633Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
- turnover: 5 consecutive closed opportunities missed
- range: 5 consecutive closed opportunities missed
- state: 3 consecutive closed opportunities missed

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 0/5 | 0.0% | 5 |
| range | 0/5 | 0.0% | 5 |
| state | 19/23 | 82.6% | 3 |
| paired | 93/93 | 100.0% | 0 |
| state_v2 | 23/23 | 100.0% | 0 |
| stress | 46/46 | 100.0% | 0 |
| liquidations | 92/92 | 100.0% | 0 |
| options capture | 22/22 | 100.0% | 0 |
| options usability rr25_7d | 22/22 | 100.0% | 0 |
| options usability rr25_30d | 0/22 | 0.0% | 22 |

turnover: 5/5 closed opportunities recorded; 0 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 5/5 closed opportunities recorded; 0 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 19 eligible forecasts; 4 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 93 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 23/23 closed opportunities recorded; 23 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 35/44 | 0 |
| range | 35/44 | 0 |
| state | 141/179 | 0 |
| paired | 710/714 | 3 |
| stress | 356/357 | 2 |
| liquidations | 715/716 | 4 |
| options | 50/178 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- turnover: last-24h operational coverage below 80% (not a research threshold)
- range: last-24h operational coverage below 80% (not a research threshold)
- options rr25_30d: 0/22 closed opportunities usable (<80%; quality warning, not a collection outage)
- 3 retained source-quality incidents; affected score windows are listed without changing results

Paired study: 748 scored forecasts; 625 unique entries; 176 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim.

State depth (last_24h): 24 forecasts, 5 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.033333333333335.
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 3: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 180 forecasts, 39 abstentions; 1 unavailable depth ages. Median/max age in minutes: 16.066666666666666 / 31.15.
- 15: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 23: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 1: ret_15m_bp: stale-inputs: latest perp bar closed 47 min before T
- 1: rv_1h_bp: incomplete-or-stale
- 1: flow_per_depth: stale-inputs: latest perp bar closed 47 min before T
- 1: d_oi_1h_pct: stale-oi: newest usable OI stamp 55 min before T (limit 45)
- 1: oi_x_ret: stale-oi: newest usable OI stamp 55 min before T (limit 45)

State depth (state_v2_last_24h): 24 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.033333333333335 / 16.116666666666667.

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4172.0; relative spread median: 0.08333333333333341. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 0 usable captures, 0 leg observations. Quote age median (ms): None; relative spread median: None. Repeated legs and horizons are dependent; missing sizes stay unavailable.

State v2 numerical replay: verified, 151 scores reproduced.

## Source quality

Zero trades and a flat last price are a source-quality anomaly, not proof of an exchange outage. Overlapping windows are not independent. Frozen scores and input eligibility remain unchanged.
- binance_klines_1m_BTCUSDT_perp: 36 flat zero-trade minutes; recovered; 26 overlapping score windows (including dependent arms). Incident binance_klines_1m_BTCUSDT_perp-1793059320000; cross-feed differences in bp: {'spot': 27.71648511836311, 'mark': 23.96204444522043}.
- binance_klines_1m_ETHUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_ETHUSDT_perp-1793059320000; cross-feed differences in bp: {}.
- binance_klines_1m_SOLUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_SOLUSDT_perp-1793059320000; cross-feed differences in bp: {}.

Separate options expiry pilot: active. [Prospective feasibility report](options_expiry_pilot.md).
