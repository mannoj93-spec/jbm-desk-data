# Research feasibility

Generated 2026-11-12T16:44:27Z by feasibility-1.3.0; source cutoff 2026-11-12T07:40Z. Read-only: it restates what the lab and the streams recorded and changes no definition. A zero the collection could not observe is marked **not observable**.

## Lab designs

| design | status | capability | calendar days | observable days | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |
|---|---|---|---|---|---|---|---|---|
| A1-flow-absorption | under prospective evaluation | observable | 47.59 | 46.58 | 134 / 94 | 10 / 100 | time (accumulation) | ~419 d (90%: 247–773 d) |
| B1-underwater-adds | exploratory | observable | 46.56 | 45.0 | 0 / 0 | 0 / 100 | absent events; parked | no ETA |
| C1-liquidation-cluster | under prospective evaluation | observable | 47.59 | 46.58 | 22 / 15 | 10 / 100 | time (accumulation) | ~419 d (90%: 247–773 d) |
| D1-active-twap | exploratory | observable | 46.56 | 46.54 | 0 / 0 | 0 / 100 | absent events; parked | no ETA |
| E1-liquidity-recovery | exploratory | not observable | 46.56 | unavailable | 0 / 0 | 0 / 100 | infrastructure capability; parked | no ETA |
| F1-options-perp-disagreement | under prospective evaluation | observable | 47.59 | 46.58 | 20 / 3 | 2 / 100 | time (accumulation) | no ETA |
| G1-alt-stress-propagation | under prospective evaluation | observable | 47.59 | 46.58 | 18 / 18 | 18 / 100 | time (accumulation) | ~212 d (90%: 143–328 d) |
| H1-deleveraging-stress | exploratory | observable | 47.59 | 47.58 | 204 / 132 | 0 / 100 | absent events | no ETA |

Observable days = hours with a selected hourly control (the lab's coverage count) ÷ 24; calendar days are shown for reference only and never divide a count.

### A1-flow-absorption (ev-c368833b5ae6)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 15, episodes 10, scorable 10, retained 10, blocks 9
- Rates per observable day: test episodes 0.215, retained 0.215
- Exclusions (named in the design): middle response group; windows with missing bars; first 7 days (threshold history)
- Recorded counters: {"events": 134, "late_inputs": 439, "skipped_history": 144, "skipped_missing": 0, "spot_not_yet_available": 14389, "steps": 14533}

### B1-underwater-adds (ev-125c86066f05)

- **Parked** 2026-11-11 by operator: zero test episodes in 45.0 observable days (reports/feasibility.md, 2026-11-11), and 2,126.8 of the lab's 2,353.5 seconds in run 42976436886; the lab step reached 48.75 minutes against a 50-minute job limit on 2026-11-10. Not run by the scheduled lab; the figures below are as of its last run (2026-11-11T07:02Z).
- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): rotating cohort (membership changes); transitions more than 30 minutes apart
- Recorded counters: {"behaviour_counts": {"drawdown:add": 8, "drawdown:hold": 22561, "drawdown:reduce": 6, "gain:add": 1, "gain:close": 1, "gain:hold": 5309, "gain:reduce": 18, "neutral:add": 3494, "neutral:close": 1, "neutral:flat": 472476, "neutral:hold": 22943, "neutral:open": 2, "neutral:reduce": 3662, "neutral:reverse": 910}, "snapshots": 5314, "transitions": 531392}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 45.0 observable days; an ETA needs >= 5

### C1-liquidation-cluster (ev-eb20553bce1c)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 240 min): firings 22, episodes 14, scorable 14, retained 10, blocks 5
- Rates per observable day: test episodes 0.301, retained 0.215
- Exclusions (named in the design): sampled accounts only; never market inventory; snapshots without a same-run mark
- Recorded counters: {"snapshots": 5443, "with_mark": 5442}

### D1-active-twap (ev-2b023a90293f)

- **Parked** 2026-11-11 by operator: zero test episodes in about 45 observable days (reports/feasibility.md, 2026-11-11). Not run by the scheduled lab; the figures below are as of its last run (2026-11-11T07:02Z).
- Data: insufficient_data — 44796 twapHistory checks, 291 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- Zeros: observed zero qualifying events while the detector ran (see capability note)
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): programs first observed after they finished; non-BTC programs
- Recorded counters: {"btc_programs": 2, "btc_programs_not_qualifying": 2, "excluded_non_btc": 289, "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule (first observed after finishing vs below the notional floor)", "programs_observed": 291, "twap_checks": 44796}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 46.5 observable days; an ETA needs >= 5
- Capability: TWAP programs are read by polling each fixed-cohort account's twapHistory every 15 minutes. A program that starts and finishes between polls is first seen finished and excluded, so the collection systematically under-observes short programs. Observing starts needs an event stream (Hyperliquid's websocket user events for the cohort accounts). Not commissioned. Per-reason counts (research_tools/d1_diagnostics.py, Oct 19 2026): 282 programs, 280 not BTC, the 2 BTC programs first seen already finished, none rejected on notional - universe scarcity dominates, so a stream could at most recover those two against a design that needs 30 (the Oct 8 figure was 2 BTC in 272).

### E1-liquidity-recovery (ev-6f279983100b)

- **Parked** 2026-11-11 by operator: not observable: the collection cannot see these events without the streaming host, which the operator has not commissioned. Not run by the scheduled lab; the figures below are as of its last run (2026-11-11T07:02Z).
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
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 480 min): firings 9, episodes 2, scorable 2, retained 2, blocks 2
- Rates per observable day: test episodes 0.043, retained 0.043
- Exclusions (named in the design): records before 7 days of z history; panel quotes failing quality checks; events whose rr25_7d quotes are not qualified (regrouped *_ineligible; unknown quality stays unknown)
- Recorded counters: {"quote_policy": "qualified", "records": 5475, "with_z": 4977}
- Checkpoint 1: no ETA: 2 retained test observation(s) in 46.6 observable days; an ETA needs >= 5

### G1-alt-stress-propagation (ev-5cbc55c34b6d)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 18, episodes 18, scorable 18, retained 18, blocks 15
- Rates per observable day: test episodes 0.386, retained 0.386
- Exclusions (named in the design): same-minute co-movement is not leadership; windows with missing bars in any of the three assets
- Recorded counters: {"late_inputs": 583, "skipped_missing": 0, "steps": 14533}

### H1-deleveraging-stress (ev-02fcecefd1bf)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): buckets before 7 days of collected liquidation history; other venues' deleveraging data (unavailable)
- Recorded counters: {"buckets": 3694, "liquidation_orders": 86222, "stress_rows": 0, "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)", "binance insurance fund"]}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 47.6 observable days; an ETA needs >= 5

## Desk streams

| stream | limiting factor | detail |
|---|---|---|
| RC1D B2 vs B0 (24h) | time (accumulation) | {"blocks": 5, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 47.53, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 235, "rate_per_day": 4.94, "time_to_checkpoint": "~37 d"} |
| RC1D B2 vs B0 (4h) | time (accumulation) | {"blocks": 5, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 47.53, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 240, "rate_per_day": 5.05, "time_to_checkpoint": "~36 d"} |
| RC1D B2 vs B0 (72h) | time (accumulation) | {"blocks": 5, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 47.53, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 223, "rate_per_day": 4.69, "time_to_checkpoint": "~42 d"} |
| Companion B2 vs B1 (24h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 33, "paired": 175} |
| Companion B2 vs B1 (4h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 38, "paired": 175} |
| Companion B2 vs B1 (72h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 23, "paired": 173} |
| PS1 paper sizing | infrastructure capability | {"checkpoint": {}, "coverage": 0.7878, "intervals": 192, "outcomes": {"executed": 193, "missed: no run": 6, "missed: stale: processed after close + max_delay": 8, "no-rebalance: forecast unavailable": 38}} |

Rules: only with >= 5 qualifying observations; 90% Garwood interval on the rate. observed zero (collection capable) is reported separately from not observable; an unobservable rate is null, never 0.0. no design, threshold or evaluation version is changed by this report.
