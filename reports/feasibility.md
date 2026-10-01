# Research feasibility

Generated 2026-10-01T20:59:44Z by feasibility-1.0.0. Read-only: it restates what the lab and the streams recorded and changes no definition. A zero the collection could not observe is marked **not observable**.

## Lab designs

| design | status | eligible days | coverage | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |
|---|---|---|---|---|---|---|---|
| A1-flow-absorption | exploratory | 6.05 | 100% | 7 / 4 | 0 / 100 | absent events | no ETA |
| B1-underwater-adds | exploratory | 6.05 | 100% | 0 / 0 | 0 / 100 | time (warm-up) | no ETA |
| C1-liquidation-cluster | exploratory | 6.05 | 100% | 1 / 1 | 0 / 100 | time (warm-up) | no ETA |
| D1-active-twap | exploratory | 6.05 | 100% | 0 / 0 | 0 / 100 | absent events | no ETA |
| E1-liquidity-recovery | exploratory | 6.05 | 0% | 0 / 0 | 0 / 100 | infrastructure capability | no ETA |
| F1-options-perp-disagreement | exploratory | 6.05 | 100% | 0 / 0 | 0 / 100 | time (warm-up) | no ETA |
| G1-alt-stress-propagation | under prospective evaluation | 6.05 | 100% | 1 / 1 | 1 / 100 | time (warm-up) | no ETA |
| H1-deleveraging-stress | exploratory | 6.05 | 100% | 18 / 10 | 0 / 100 | absent events | no ETA |

Coverage = hourly controls selected in the evaluation phase ÷ hours elapsed since registration.

### A1-flow-absorption (ev-c368833b5ae6)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 60 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): middle response group; windows with missing bars; first 7 days (threshold history)
- Recorded counters: {"events": 7, "late_inputs": 132, "skipped_history": 144, "skipped_missing": 0, "spot_not_yet_available": 2426, "steps": 2570}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5

### B1-underwater-adds (ev-125c86066f05)

- Data: insufficient_data — 729 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): rotating cohort (membership changes); transitions more than 30 minutes apart
- Recorded counters: {"behaviour_counts": {"drawdown:hold": 4067, "drawdown:reduce": 5, "neutral:add": 548, "neutral:flat": 64881, "neutral:hold": 2654, "neutral:reduce": 594, "neutral:reverse": 151}, "snapshots": 729, "transitions": 72900}
- Warm-up: 729 of 1344 snapshot transitions for the fixed cohort; observed 82.7/day → 7.4 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5

### C1-liquidation-cluster (ev-eb20553bce1c)

- Data: insufficient_data — 733 sampled snapshots; the design needs 1344
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 240 min): firings 1, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): sampled accounts only; never market inventory; snapshots without a same-run mark
- Recorded counters: {"snapshots": 733, "with_mark": 733}
- Warm-up: 733 of 1344 sampled snapshots; observed 83.16/day → 7.3 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5

### D1-active-twap (ev-2b023a90293f)

- Data: insufficient_data — 6066 twapHistory checks, 275 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- Zeros: observed zero qualifying events while the detector ran (see capability note)
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): programs first observed after they finished; non-BTC programs
- Recorded counters: {"btc_programs": 2, "btc_programs_not_qualifying": 2, "excluded_non_btc": 273, "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule (first observed after finishing vs below the notional floor)", "programs_observed": 275, "twap_checks": 6066}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5
- Capability: TWAP programs are read by polling each fixed-cohort account's twapHistory every 15 minutes. A program that starts and finishes between polls is first seen finished and excluded, so the collection systematically under-observes short programs. Observing starts needs an event stream (Hyperliquid's websocket user events for the cohort accounts). Not commissioned: the recorded universe (2 BTC programs in 272) suggests qualifying BTC programs are rare even when seen, so a stream would not by itself make D1 feasible; decide after the per-reason counts exist.

### E1-liquidity-recovery (ev-6f279983100b)

- Data: unavailable — streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- Zeros: not observable: the collection cannot see these events
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): shock windows with missing seconds or recorded gaps; Hyperliquid books
- Recorded counters: {"stream_data_dir": null}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5
- Capability: Needs second-scale order-book depth around shocks. The repository's stream/ recorder exists but is not deployed (it needs a persistent host, not GitHub Actions); until then E1 cannot observe a single event and its zero is 'not observable'. Not commissioned here.

### F1-options-perp-disagreement (ev-1c53cfe81c9f)

- Data: insufficient_data — 770 option records (299 with a trailing z-score); the design needs 1344
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 480 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): records before 7 days of z history; panel quotes failing quality checks; events whose rr25_7d quotes are not qualified (regrouped *_ineligible; unknown quality stays unknown)
- Recorded counters: {"quote_policy": "qualified", "records": 770, "with_z": 299}
- Warm-up: 770 of 1344 option records; observed 87.36/day → 6.6 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5

### G1-alt-stress-propagation (ev-5cbc55c34b6d)

- Data: insufficient_data — 9.0 days of stored bars; the design needs 14
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 60 min): firings 1, episodes 1, scorable 1, retained 1, blocks 1
- Rates per day: test episodes 0.165, retained 0.165
- Exclusions (named in the design): same-minute co-movement is not leadership; windows with missing bars in any of the three assets
- Recorded counters: {"late_inputs": 276, "skipped_missing": 0, "steps": 2570}
- Warm-up: 9 of 14 days of stored bars; observed 1.02/day → 4.9 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 1 retained test observation(s) in 6.1 days; an ETA needs >= 5

### H1-deleveraging-stress (ev-02fcecefd1bf)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): buckets before 7 days of collected liquidation history; other venues' deleveraging data (unavailable)
- Recorded counters: {"buckets": 690, "liquidation_orders": 14036, "stress_rows": 0, "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)", "binance insurance fund"]}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 6.1 days; an ETA needs >= 5

## Desk streams

| stream | limiting factor | detail |
|---|---|---|
| RC1D B2 vs B0 (24h) | time (accumulation) | {"blocks": 0, "checkpoint": {"block": 42, "need_blocks": 10}, "eligible_observation": {"days": 5.71, "from": "2026-09-26T04:00:00Z"}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 27, "rate_per_day": 4.73, "time_to_checkpoint": "~83 d"} |
| RC1D B2 vs B0 (4h) | time (accumulation) | {"blocks": 0, "checkpoint": {"block": 42, "need_blocks": 10}, "eligible_observation": {"days": 5.71, "from": "2026-09-26T04:00:00Z"}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 32, "rate_per_day": 5.61, "time_to_checkpoint": "~69 d"} |
| RC1D B2 vs B0 (72h) | time (accumulation) | {"blocks": 0, "checkpoint": {"block": 42, "need_blocks": 10}, "eligible_observation": {"days": 5.71, "from": "2026-09-26T04:00:00Z"}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 16, "rate_per_day": 2.8, "time_to_checkpoint": "~144 d"} |
| Companion B2 vs B1 (24h) | not started | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 0} |
| Companion B2 vs B1 (4h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 5} |
| Companion B2 vs B1 (72h) | not started | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 0} |
| PS1 paper sizing | not started | {"note": "no executed decision yet (not before 2026-10-03T00:00:00Z)"} |

Rules: only with >= 5 qualifying observations; 90% Garwood interval on the rate. observed zero (collection capable) is reported separately from not observable. no design, threshold or evaluation version is changed by this report.
