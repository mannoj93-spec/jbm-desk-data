# Research feasibility

Generated 2026-10-01T16:15:53Z by feasibility-1.0.0. Read-only: it restates what the lab and the streams recorded and changes no definition. A zero the collection could not observe is marked **not observable**.

## Lab designs

| design | status | eligible days | coverage | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |
|---|---|---|---|---|---|---|---|
| A1-flow-absorption | exploratory | 5.81 | 100% | 6 / 3 | 0 / 100 | absent events | no ETA |
| B1-underwater-adds | exploratory | 5.81 | 100% | 0 / 0 | 0 / 100 | time (warm-up) | no ETA |
| C1-liquidation-cluster | exploratory | 5.81 | 100% | 1 / 1 | 0 / 100 | time (warm-up) | no ETA |
| D1-active-twap | exploratory | 5.81 | 100% | 0 / 0 | 0 / 100 | absent events | no ETA |
| E1-liquidity-recovery | exploratory | 5.81 | 0% | 0 / 0 | 0 / 100 | infrastructure capability | no ETA |
| F1-options-perp-disagreement | exploratory | 5.81 | 100% | 0 / 0 | 0 / 100 | time (warm-up) | no ETA |
| G1-alt-stress-propagation | under prospective evaluation | 5.81 | 100% | 1 / 1 | 1 / 100 | time (warm-up) | no ETA |
| H1-deleveraging-stress | exploratory | 5.81 | 100% | 14 / 9 | 0 / 100 | absent events | no ETA |

Coverage = hourly controls selected in the evaluation phase ÷ hours elapsed since registration.

### A1-flow-absorption (ev-c368833b5ae6)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 60 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): middle response group; windows with missing bars; first 7 days (threshold history)
- Recorded counters: {"events": 6, "late_inputs": 132, "skipped_history": 144, "skipped_missing": 0, "spot_not_yet_available": 2356, "steps": 2500}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5

### B1-underwater-adds (ev-125c86066f05)

- Data: insufficient_data — 708 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): rotating cohort (membership changes); transitions more than 30 minutes apart
- Recorded counters: {"behaviour_counts": {"drawdown:hold": 3929, "drawdown:reduce": 5, "neutral:add": 530, "neutral:flat": 63012, "neutral:hold": 2613, "neutral:reduce": 565, "neutral:reverse": 146}, "snapshots": 708, "transitions": 70800}
- Warm-up: 708 of 1344 snapshot transitions for the fixed cohort; observed 82.65/day → 7.7 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5

### C1-liquidation-cluster (ev-eb20553bce1c)

- Data: insufficient_data — 712 sampled snapshots; the design needs 1344
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 240 min): firings 1, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): sampled accounts only; never market inventory; snapshots without a same-run mark
- Recorded counters: {"snapshots": 712, "with_mark": 712}
- Warm-up: 712 of 1344 sampled snapshots; observed 83.11/day → 7.6 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5

### D1-active-twap (ev-2b023a90293f)

- Data: insufficient_data — 5901 twapHistory checks, 272 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- Zeros: observed zero qualifying events while the detector ran (see capability note)
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): programs first observed after they finished; non-BTC programs
- Recorded counters: {"btc_programs": 2, "btc_programs_not_qualifying": 2, "excluded_non_btc": 270, "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule (first observed after finishing vs below the notional floor)", "programs_observed": 272, "twap_checks": 5901}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5
- Capability: TWAP programs are read by polling each fixed-cohort account's twapHistory every 15 minutes. A program that starts and finishes between polls is first seen finished and excluded, so the collection systematically under-observes short programs. Observing starts needs an event stream (Hyperliquid's websocket user events for the cohort accounts). Not commissioned: the recorded universe (2 BTC programs in 272) suggests qualifying BTC programs are rare even when seen, so a stream would not by itself make D1 feasible; decide after the per-reason counts exist.

### E1-liquidity-recovery (ev-6f279983100b)

- Data: unavailable — streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- Zeros: not observable: the collection cannot see these events
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): shock windows with missing seconds or recorded gaps; Hyperliquid books
- Recorded counters: {"stream_data_dir": null}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5
- Capability: Needs second-scale order-book depth around shocks. The repository's stream/ recorder exists but is not deployed (it needs a persistent host, not GitHub Actions); until then E1 cannot observe a single event and its zero is 'not observable'. Not commissioned here.

### F1-options-perp-disagreement (ev-1c53cfe81c9f)

- Data: insufficient_data — 749 option records (278 with a trailing z-score); the design needs 1344
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 480 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): records before 7 days of z history; panel quotes failing quality checks; events whose rr25_7d quotes are not qualified (regrouped *_ineligible; unknown quality stays unknown)
- Recorded counters: {"quote_policy": "qualified", "records": 749, "with_z": 278}
- Warm-up: 749 of 1344 option records; observed 87.43/day → 6.8 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5

### G1-alt-stress-propagation (ev-5cbc55c34b6d)

- Data: insufficient_data — 8.7 days of stored bars; the design needs 14
- Zeros: design warm-up not complete: events cannot yet qualify
- Test (evaluation phase, primary 60 min): firings 1, episodes 1, scorable 1, retained 1, blocks 1
- Rates per day: test episodes 0.172, retained 0.172
- Exclusions (named in the design): same-minute co-movement is not leadership; windows with missing bars in any of the three assets
- Recorded counters: {"late_inputs": 276, "skipped_missing": 0, "steps": 2500}
- Warm-up: 8.7 of 14 days of stored bars; observed 1.02/day → 5.2 more days at that rate (averaged from the collector start (cadence.json), so an upper bound on the wait if collection began later for this input; warm-up only - it says nothing about event rates after)
- Checkpoint 1: no ETA: 1 retained test observation(s) in 5.8 days; an ETA needs >= 5

### H1-deleveraging-stress (ev-02fcecefd1bf)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): buckets before 7 days of collected liquidation history; other venues' deleveraging data (unavailable)
- Recorded counters: {"buckets": 660, "liquidation_orders": 13439, "stress_rows": 0, "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)", "binance insurance fund"]}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 5.8 days; an ETA needs >= 5

## Desk streams

| stream | limiting factor | detail |
|---|---|---|
| RC1D B2 vs B0 (24h) | time (accumulation) | {"blocks": 0, "checkpoint": {"block": 42, "need_blocks": 10}, "eligible_observation": {"days": 5.51, "from": "2026-09-26T04:00:00Z"}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 25, "rate_per_day": 4.54, "time_to_checkpoint": "~87 d"} |
| RC1D B2 vs B0 (4h) | time (accumulation) | {"blocks": 0, "checkpoint": {"block": 42, "need_blocks": 10}, "eligible_observation": {"days": 5.51, "from": "2026-09-26T04:00:00Z"}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 30, "rate_per_day": 5.44, "time_to_checkpoint": "~72 d"} |
| RC1D B2 vs B0 (72h) | time (accumulation) | {"blocks": 0, "checkpoint": {"block": 42, "need_blocks": 10}, "eligible_observation": {"days": 5.51, "from": "2026-09-26T04:00:00Z"}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 14, "rate_per_day": 2.54, "time_to_checkpoint": "~160 d"} |
| Companion B2 vs B1 (24h) | not started | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 0} |
| Companion B2 vs B1 (4h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 3} |
| Companion B2 vs B1 (72h) | not started | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 0, "paired": 0} |
| PS1 paper sizing | not started | {"note": "no executed decision yet (not before 2026-10-03T00:00:00Z)"} |

Rules: only with >= 5 qualifying observations; 90% Garwood interval on the rate. observed zero (collection capable) is reported separately from not observable. no design, threshold or evaluation version is changed by this report.
