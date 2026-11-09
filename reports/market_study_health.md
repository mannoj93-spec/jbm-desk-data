# Market study operational health

Generated 2026-11-09T08:19:54.439Z. Integrity: ok.

Operational diagnostics only; frozen study results and launch clocks are unchanged.
Rolling 24-hour counts include closed deadlines plus five minutes for persistence. Pending outcomes are separate.

Paused: False

## Alerts
None.
- v1 verification: ok
- state_v2 verification: ok
- options_expiry verification: ok
- options_30d verification: ok
- immediate_books verification: ok
- source_quality verification: ok
- report_freshness verification: ok
- v1 published report: fresh; last successful refresh: 2026-11-09T08:19:41.093Z
- state_v2 published report: fresh; last successful refresh: 2026-11-09T08:19:47.081Z
- options_expiry published report: fresh; last successful refresh: 2026-11-09T08:19:47.533Z
- options_30d published report: fresh; last successful refresh: 2026-11-09T08:19:53.185Z

## Coverage

| Program | Successful / due | Coverage | Consecutive misses |
|---|---:|---:|---:|
| turnover | 5/5 | 100.0% | 0 |
| range | 5/5 | 100.0% | 0 |
| state | 17/23 | 73.9% | 1 |
| paired | 93/93 | 100.0% | 0 |
| state_v2 | 23/23 | 100.0% | 0 |
| stress | 47/47 | 100.0% | 0 |
| liquidations | 85/92 | 92.4% | 0 |
| options capture | 23/23 | 100.0% | 0 |
| options usability rr25_7d | 23/23 | 100.0% | 0 |
| options usability rr25_30d | 0/23 | 0.0% | 23 |

turnover: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

range: 5/5 closed opportunities recorded; 5 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state: 23/23 closed opportunities recorded; 17 eligible forecasts; 6 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

paired: 93/93 closed opportunities recorded; 93 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

state_v2: 23/23 closed opportunities recorded; 23 eligible forecasts; 0 abstentions. Abstention rate uses recorded closed opportunities; scheduled research denominators are unchanged.

## Since recovery deployment

Study recovery deployment (PR #53), 2026-10-26T00:58:03Z; commit `d03301c59ec95502e716faf06502c875298a2866`.
Fixed operational comparison by opportunity time, not a reset of research history.

| Program | Successful / closed | Additional successes awaiting closure |
|---|---:|---:|
| turnover | 51/85 | 1 |
| range | 51/85 | 1 |
| state | 258/343 | 0 |
| paired | 1361/1371 | 3 |
| stress | 682/686 | 1 |
| liquidations | 1354/1372 | 4 |
| options | 50/343 | 0 |

## Diagnostics

Training readiness, per-opportunity reasons and source confirmations, publication delays, pending/overdue scores, per-vintage collection, paired unique-entry sensitivity and options quality are in [the JSON report](market_study_health.json).

Warnings:
- state: 6/23 recorded closed opportunities abstained in 24h (>20%; operational warning only)
- state: last-24h operational coverage below 80% (not a research threshold)
- options rr25_30d: 0/23 closed opportunities usable (<80%; quality warning, not a collection outage)
- 3 retained source-quality incidents; affected score windows are listed without changing results

Paired study: 1399 scored forecasts; 1217 unique entries; 321 windows in the largest disjoint subset. These are not independent-sample counts.
Sensitivity only: average within each shared entry, then across entries. Overlapping windows remain dependent; no new primary, interval or support claim. Equal minute entry clocks cannot establish a subminute execution or latency advantage.

State depth (last_24h): 24 forecasts, 7 abstentions; 0 unavailable depth ages. Median/max age in minutes: 16.025 / 31.0.
- 2: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 5: flow_per_depth: stale-depth: measured 30 min before T (limit 30)

State depth (since_deployment): 344 forecasts, 85 abstentions; 2 unavailable depth ages. Median/max age in minutes: 16.05 / 45.85.
- 21: flow_per_depth: stale-depth: measured 31 min before T (limit 30)
- 61: flow_per_depth: stale-depth: measured 30 min before T (limit 30)
- 1: ret_15m_bp: stale-inputs: latest perp bar closed 47 min before T
- 1: rv_1h_bp: incomplete-or-stale
- 1: flow_per_depth: stale-inputs: latest perp bar closed 47 min before T
- 1: d_oi_1h_pct: stale-oi: newest usable OI stamp 55 min before T (limit 45)
- 1: oi_x_ret: stale-oi: newest usable OI stamp 55 min before T (limit 45)
- 1: flow_per_depth: stale-depth: measured 45 min before T (limit 30)
- 1: flow_per_depth: stale-depth: measured 40 min before T (limit 30)

State depth (state_v2_last_24h): 24 forecasts, 0 abstentions; 0 unavailable depth ages. Median/max age in minutes: 15.958333333333332 / 25.666666666666668.

Selected rr25_7d legs: 24 usable captures, 96 leg observations. Quote age median (ms): 4955.0; relative spread median: 0.08695652173913052. Repeated legs and horizons are dependent; missing sizes stay unavailable.

Selected rr25_30d legs: 0 usable captures, 0 leg observations. Quote age median (ms): None; relative spread median: None. Repeated legs and horizons are dependent; missing sizes stay unavailable.

State v2 numerical replay: verified, 312 scores reproduced.

State v2 evidence: 312/1680 scored observations for the frozen minimum interval threshold; 1/10 block equivalents. Scheduled review: 2027-04-25T00:00:00.000Z. Block equivalents are not independent samples. Frozen interval and review rules; no automatic promotion.

Immediate selected books: 192 usable / 192 attempted / 192 selected in 24h; median/p90 source lag (ms): 469.0 / 682.
Immediate collector diagnostic, separate from both prospective pilots. Missing and budget-skipped captures are explicit; later sizes never replace original quotes.

## Source quality

Zero trades and a flat last price are a source-quality anomaly, not proof of an exchange outage. Overlapping windows are not independent. Frozen scores and input eligibility remain unchanged.
- binance_klines_1m_BTCUSDT_perp: 36 flat zero-trade minutes; recovered; 26 overlapping score windows (including dependent arms). Incident binance_klines_1m_BTCUSDT_perp-1793059320000; cross-feed differences in bp: {'spot': 27.71648511836311, 'mark': 23.96204444522043}.
- binance_klines_1m_ETHUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_ETHUSDT_perp-1793059320000; cross-feed differences in bp: {}.
- binance_klines_1m_SOLUSDT_perp: 36 flat zero-trade minutes; recovered; 0 overlapping score windows (including dependent arms). Incident binance_klines_1m_SOLUSDT_perp-1793059320000; cross-feed differences in bp: {}.

Separate options expiry pilot: active. [Prospective feasibility report](options_expiry_pilot.md).

Separate 30-day maturity pilot: active. [Report](options_30d_pilot.md).
