# Research feasibility

Generated 2026-10-17T01:22:11Z by feasibility-1.2.0; source cutoff 2026-10-16T19:07Z. Read-only: it restates what the lab and the streams recorded and changes no definition. A zero the collection could not observe is marked **not observable**.

## Lab designs

| design | status | capability | calendar days | observable days | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |
|---|---|---|---|---|---|---|---|---|
| A1-flow-absorption | under prospective evaluation | observable | 21.07 | 20.04 | 55 / 40 | 3 / 100 | time (accumulation) | no ETA |
| B1-underwater-adds | exploratory | observable | 21.07 | 19.58 | 0 / 0 | 0 / 100 | absent events | no ETA |
| C1-liquidation-cluster | under prospective evaluation | observable | 21.07 | 20.04 | 14 / 8 | 5 / 100 | time (accumulation) | ~381 d (90%: 181–966 d) |
| D1-active-twap | exploratory | observable | 21.07 | 21.04 | 0 / 0 | 0 / 100 | absent events | no ETA |
| E1-liquidity-recovery | exploratory | not observable | 21.07 | unavailable | 0 / 0 | 0 / 100 | infrastructure capability | no ETA |
| F1-options-perp-disagreement | exploratory | observable | 21.07 | 20.04 | 0 / 0 | 0 / 100 | absent events | no ETA |
| G1-alt-stress-propagation | under prospective evaluation | observable | 21.07 | 20.04 | 8 / 8 | 8 / 100 | time (accumulation) | ~230 d (90%: 128–463 d) |
| H1-deleveraging-stress | exploratory | observable | 21.07 | 21.04 | 87 / 60 | 0 / 100 | absent events | no ETA |

Observable days = hours with a selected hourly control (the lab's coverage count) ÷ 24; calendar days are shown for reference only and never divide a count.

### A1-flow-absorption (ev-c368833b5ae6)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 4, episodes 3, scorable 3, retained 3, blocks 2
- Rates per observable day: test episodes 0.15, retained 0.15
- Exclusions (named in the design): middle response group; windows with missing bars; first 7 days (threshold history)
- Recorded counters: {"events": 55, "late_inputs": 437, "skipped_history": 144, "skipped_missing": 0, "spot_not_yet_available": 6748, "steps": 6892}
- Checkpoint 1: no ETA: 3 retained test observation(s) in 20.0 observable days; an ETA needs >= 5

### B1-underwater-adds (ev-125c86066f05)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): rotating cohort (membership changes); transitions more than 30 minutes apart
- Recorded counters: {"behaviour_counts": {"drawdown:hold": 14060, "drawdown:reduce": 5, "gain:hold": 861, "gain:reduce": 2, "neutral:add": 1745, "neutral:flat": 237714, "neutral:hold": 10426, "neutral:reduce": 1830, "neutral:reverse": 451}, "snapshots": 2671, "transitions": 267094}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 19.6 observable days; an ETA needs >= 5

### C1-liquidation-cluster (ev-eb20553bce1c)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 240 min): firings 14, episodes 7, scorable 7, retained 5, blocks 2
- Rates per observable day: test episodes 0.349, retained 0.249
- Exclusions (named in the design): sampled accounts only; never market inventory; snapshots without a same-run mark
- Recorded counters: {"snapshots": 2690, "with_mark": 2689}

### D1-active-twap (ev-2b023a90293f)

- Data: insufficient_data — 22529 twapHistory checks, 281 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- Zeros: observed zero qualifying events while the detector ran (see capability note)
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): programs first observed after they finished; non-BTC programs
- Recorded counters: {"btc_programs": 2, "btc_programs_not_qualifying": 2, "excluded_non_btc": 279, "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule (first observed after finishing vs below the notional floor)", "programs_observed": 281, "twap_checks": 22529}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 21.0 observable days; an ETA needs >= 5
- Capability: TWAP programs are read by polling each fixed-cohort account's twapHistory every 15 minutes. A program that starts and finishes between polls is first seen finished and excluded, so the collection systematically under-observes short programs. Observing starts needs an event stream (Hyperliquid's websocket user events for the cohort accounts). Not commissioned: the recorded universe (2 BTC programs in 272) suggests qualifying BTC programs are rare even when seen, so a stream would not by itself make D1 feasible; decide after the per-reason counts exist.

### E1-liquidity-recovery (ev-6f279983100b)

- Data: unavailable — streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- Zeros: not observable: the collection cannot see these events
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes unavailable, retained unavailable (not observable)
- Exclusions (named in the design): shock windows with missing seconds or recorded gaps; Hyperliquid books
- Recorded counters: {"stream_data_dir": null}
- Checkpoint 1: no ETA: not observable
- Capability: Needs second-scale order-book depth around shocks. The repository's stream/ recorder exists but is not deployed (it needs a persistent host, not GitHub Actions); until then E1 cannot observe a single event and its zero is 'not observable'. Not commissioned here.

### F1-options-perp-disagreement (ev-1c53cfe81c9f)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 480 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): records before 7 days of z history; panel quotes failing quality checks; events whose rr25_7d quotes are not qualified (regrouped *_ineligible; unknown quality stays unknown)
- Recorded counters: {"quote_policy": "qualified", "records": 2724, "with_z": 2236}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 20.0 observable days; an ETA needs >= 5

### G1-alt-stress-propagation (ev-5cbc55c34b6d)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 8, episodes 8, scorable 8, retained 8, blocks 8
- Rates per observable day: test episodes 0.399, retained 0.399
- Exclusions (named in the design): same-minute co-movement is not leadership; windows with missing bars in any of the three assets
- Recorded counters: {"late_inputs": 581, "skipped_missing": 0, "steps": 6892}

### H1-deleveraging-stress (ev-02fcecefd1bf)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): buckets before 7 days of collected liquidation history; other venues' deleveraging data (unavailable)
- Recorded counters: {"buckets": 1789, "liquidation_orders": 39157, "stress_rows": 0, "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)", "binance insurance fund"]}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 21.0 observable days; an ETA needs >= 5

## Desk streams

| stream | limiting factor | detail |
|---|---|---|
| RC1D B2 vs B0 (24h) | time (accumulation) | {"blocks": 2, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 20.89, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 110, "rate_per_day": 5.27, "time_to_checkpoint": "~59 d"} |
| RC1D B2 vs B0 (4h) | time (accumulation) | {"blocks": 2, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 20.89, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 115, "rate_per_day": 5.5, "time_to_checkpoint": "~55 d"} |
| RC1D B2 vs B0 (72h) | time (accumulation) | {"blocks": 2, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 20.89, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 98, "rate_per_day": 4.69, "time_to_checkpoint": "~69 d"} |
| Companion B2 vs B1 (24h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 83} |
| Companion B2 vs B1 (4h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 88} |
| Companion B2 vs B1 (72h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 71} |
| PS1 paper sizing | time (accumulation) | {"checkpoint": {}, "coverage": 0.9059, "intervals": 76, "outcomes": {"executed": 77, "missed: stale: processed after close + max_delay": 8}} |

Rules: only with >= 5 qualifying observations; 90% Garwood interval on the rate. observed zero (collection capable) is reported separately from not observable; an unobservable rate is null, never 0.0. no design, threshold or evaluation version is changed by this report.
