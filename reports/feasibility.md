# Research feasibility

Generated 2026-10-06T04:22:34Z by feasibility-1.1.0; source cutoff 2026-10-06T00:55Z. Read-only: it restates what the lab and the streams recorded and changes no definition. A zero the collection could not observe is marked **not observable**.

## Lab designs

| design | status | capability | calendar days | observable days | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |
|---|---|---|---|---|---|---|---|---|
| A1-flow-absorption | under prospective evaluation | observable | 10.31 | 9.29 | 24 / 16 | 2 / 100 | time (accumulation) | no ETA |
| B1-underwater-adds | exploratory | observable | 10.31 | 8.83 | 0 / 0 | 0 / 100 | time (warm-up) | no ETA |
| C1-liquidation-cluster | under prospective evaluation | observable | 10.31 | 9.29 | 4 / 4 | 2 / 100 | time (warm-up) | no ETA |
| D1-active-twap | exploratory | observable | 10.31 | 10.29 | 0 / 0 | 0 / 100 | absent events | no ETA |
| E1-liquidity-recovery | exploratory | not observable | 10.31 | unavailable | 0 / 0 | 0 / 100 | infrastructure capability | no ETA |
| F1-options-perp-disagreement | exploratory | observable | 10.31 | 9.29 | 0 / 0 | 0 / 100 | time (warm-up) | no ETA |
| G1-alt-stress-propagation | under prospective evaluation | observable | 10.31 | 9.29 | 4 / 4 | 4 / 100 | time (warm-up) | no ETA |
| H1-deleveraging-stress | exploratory | observable | 10.31 | 10.29 | 38 / 24 | 0 / 100 | absent events | no ETA |

Observable days = hours with a selected hourly control (the lab's coverage count) ÷ 24; calendar days are shown for reference only and never divide a count.

### A1-flow-absorption (ev-c368833b5ae6)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 2, episodes 2, scorable 2, retained 2, blocks 1
- Rates per observable day: test episodes 0.215, retained 0.215
- Exclusions (named in the design): middle response group; windows with missing bars; first 7 days (threshold history)
- Recorded counters: {"events": 24, "late_inputs": 437, "skipped_history": 144, "skipped_missing": 0, "spot_not_yet_available": 3652, "steps": 3796}
- Checkpoint 1: no ETA: 2 retained test observation(s) in 9.3 observable days; an ETA needs >= 5

### B1-underwater-adds (ev-125c86066f05)

- Data: insufficient_data — 1028 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- Zeros: warm-up not complete per the lab (1028 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)); no retained test observation yet
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes unavailable, retained unavailable (warm-up incomplete per the lab; a zero here is not an observed rate)
- Exclusions (named in the design): rotating cohort (membership changes); transitions more than 30 minutes apart
- Recorded counters: {"behaviour_counts": {"drawdown:hold": 6176, "drawdown:reduce": 5, "neutral:add": 768, "neutral:flat": 91492, "neutral:hold": 3329, "neutral:reduce": 830, "neutral:reverse": 200}, "snapshots": 1028, "transitions": 102800}
- Warm-up: 1028 of 1344 snapshot transitions for the fixed cohort; observed 78.67/day → 4.0 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 8.8 observable days; an ETA needs >= 5

### C1-liquidation-cluster (ev-eb20553bce1c)

- Data: insufficient_data — 1047 sampled snapshots; the design needs 1344
- Zeros: warm-up not complete per the lab (1047 sampled snapshots; the design needs 1344); 2 retained test observation(s) in 1 block(s) are already recorded
- Test (evaluation phase, primary 240 min): firings 4, episodes 3, scorable 3, retained 2, blocks 1
- Rates per observable day: test episodes 0.323, retained 0.215
- Exclusions (named in the design): sampled accounts only; never market inventory; snapshots without a same-run mark
- Recorded counters: {"snapshots": 1047, "with_mark": 1047}
- Warm-up: 1047 of 1344 sampled snapshots; observed 80.13/day → 3.7 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 2 retained test observation(s) in 9.3 observable days; an ETA needs >= 5

### D1-active-twap (ev-2b023a90293f)

- Data: insufficient_data — 8685 twapHistory checks, 277 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- Zeros: observed zero qualifying events while the detector ran (see capability note)
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): programs first observed after they finished; non-BTC programs
- Recorded counters: {"btc_programs": 2, "btc_programs_not_qualifying": 2, "excluded_non_btc": 275, "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule (first observed after finishing vs below the notional floor)", "programs_observed": 277, "twap_checks": 8685}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 10.3 observable days; an ETA needs >= 5
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

- Data: insufficient_data — 1084 option records (613 with a trailing z-score); the design needs 1344
- Zeros: warm-up not complete per the lab (1084 option records (613 with a trailing z-score); the design needs 1344); no retained test observation yet
- Test (evaluation phase, primary 480 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes unavailable, retained unavailable (warm-up incomplete per the lab; a zero here is not an observed rate)
- Exclusions (named in the design): records before 7 days of z history; panel quotes failing quality checks; events whose rr25_7d quotes are not qualified (regrouped *_ineligible; unknown quality stays unknown)
- Recorded counters: {"quote_policy": "qualified", "records": 1084, "with_z": 613}
- Warm-up: 1084 of 1344 option records; observed 82.96/day → 3.1 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 9.3 observable days; an ETA needs >= 5

### G1-alt-stress-propagation (ev-5cbc55c34b6d)

- Data: insufficient_data — 13.2 days of stored bars; the design needs 14
- Zeros: warm-up not complete per the lab (13.2 days of stored bars; the design needs 14); 4 retained test observation(s) in 4 block(s) are already recorded
- Test (evaluation phase, primary 60 min): firings 4, episodes 4, scorable 4, retained 4, blocks 4
- Rates per observable day: test episodes 0.43, retained 0.43
- Exclusions (named in the design): same-minute co-movement is not leadership; windows with missing bars in any of the three assets
- Recorded counters: {"late_inputs": 581, "skipped_missing": 0, "steps": 3796}
- Warm-up: 13.2 of 14 days of stored bars; observed 1.01/day → 0.8 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 4 retained test observation(s) in 9.3 observable days; an ETA needs >= 5

### H1-deleveraging-stress (ev-02fcecefd1bf)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): buckets before 7 days of collected liquidation history; other venues' deleveraging data (unavailable)
- Recorded counters: {"buckets": 944, "liquidation_orders": 19540, "stress_rows": 0, "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)", "binance insurance fund"]}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 10.3 observable days; an ETA needs >= 5

## Desk streams

| stream | limiting factor | detail |
|---|---|---|
| RC1D B2 vs B0 (24h) | time (accumulation) | {"blocks": 1, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 10.02, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 45, "rate_per_day": 4.49, "time_to_checkpoint": "~83 d"} |
| RC1D B2 vs B0 (4h) | time (accumulation) | {"blocks": 1, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 10.02, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 49, "rate_per_day": 4.89, "time_to_checkpoint": "~76 d"} |
| RC1D B2 vs B0 (72h) | time (accumulation) | {"blocks": 0, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 10.02, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 40, "rate_per_day": 3.99, "time_to_checkpoint": "~95 d"} |
| Companion B2 vs B1 (24h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 18} |
| Companion B2 vs B1 (4h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 22} |
| Companion B2 vs B1 (72h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 13} |
| PS1 paper sizing | time (accumulation) | {"checkpoint": {}, "coverage": 0.6, "intervals": 11, "outcomes": {"executed": 12, "missed: stale: processed after close + max_delay": 8}} |

Rules: only with >= 5 qualifying observations; 90% Garwood interval on the rate. observed zero (collection capable) is reported separately from not observable; an unobservable rate is null, never 0.0. no design, threshold or evaluation version is changed by this report.
