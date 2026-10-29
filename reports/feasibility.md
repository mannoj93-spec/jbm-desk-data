# Research feasibility

Generated 2026-10-29T04:54:56Z by feasibility-1.2.1; source cutoff 2026-10-28T22:49Z. Read-only: it restates what the lab and the streams recorded and changes no definition. A zero the collection could not observe is marked **not observable**.

## Lab designs

| design | status | capability | calendar days | observable days | raw / episodes (prospective) | test retained / need | limiting factor | time to checkpoint 1 |
|---|---|---|---|---|---|---|---|---|
| A1-flow-absorption | under prospective evaluation | observable | 33.22 | 32.21 | 89 / 68 | 6 / 100 | time (accumulation) | ~505 d (90%: 256–1159 d) |
| B1-underwater-adds | exploratory | observable | 33.22 | 31.75 | 0 / 0 | 0 / 100 | absent events | no ETA |
| C1-liquidation-cluster | under prospective evaluation | observable | 33.22 | 32.21 | 17 / 11 | 7 / 100 | time (accumulation) | ~428 d (90%: 228–912 d) |
| D1-active-twap | exploratory | observable | 33.22 | 33.21 | 0 / 0 | 0 / 100 | absent events | no ETA |
| E1-liquidity-recovery | exploratory | not observable | 33.22 | unavailable | 0 / 0 | 0 / 100 | infrastructure capability | no ETA |
| F1-options-perp-disagreement | under prospective evaluation | observable | 33.22 | 32.21 | 8 / 2 | 2 / 100 | time (accumulation) | no ETA |
| G1-alt-stress-propagation | under prospective evaluation | observable | 33.22 | 32.21 | 11 / 11 | 11 / 100 | time (accumulation) | ~261 d (90%: 157–465 d) |
| H1-deleveraging-stress | exploratory | observable | 33.22 | 33.21 | 134 / 90 | 0 / 100 | absent events | no ETA |

Observable days = hours with a selected hourly control (the lab's coverage count) ÷ 24; calendar days are shown for reference only and never divide a count.

### A1-flow-absorption (ev-c368833b5ae6)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 7, episodes 6, scorable 6, retained 6, blocks 5
- Rates per observable day: test episodes 0.186, retained 0.186
- Exclusions (named in the design): middle response group; windows with missing bars; first 7 days (threshold history)
- Recorded counters: {"events": 89, "late_inputs": 437, "skipped_history": 144, "skipped_missing": 0, "spot_not_yet_available": 10250, "steps": 10394}

### B1-underwater-adds (ev-125c86066f05)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): rotating cohort (membership changes); transitions more than 30 minutes apart
- Recorded counters: {"behaviour_counts": {"drawdown:add": 2, "drawdown:hold": 19737, "drawdown:reduce": 6, "gain:hold": 1998, "gain:reduce": 4, "neutral:add": 2598, "neutral:flat": 358487, "neutral:hold": 16529, "neutral:reduce": 2730, "neutral:reverse": 703}, "snapshots": 4028, "transitions": 402794}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 31.8 observable days; an ETA needs >= 5

### C1-liquidation-cluster (ev-eb20553bce1c)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 240 min): firings 17, episodes 10, scorable 10, retained 7, blocks 3
- Rates per observable day: test episodes 0.31, retained 0.217
- Exclusions (named in the design): sampled accounts only; never market inventory; snapshots without a same-run mark
- Recorded counters: {"snapshots": 4049, "with_mark": 4048}

### D1-active-twap (ev-2b023a90293f)

- Data: insufficient_data — 33912 twapHistory checks, 285 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- Zeros: observed zero qualifying events while the detector ran (see capability note)
- Test (evaluation phase, primary 240 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): programs first observed after they finished; non-BTC programs
- Recorded counters: {"btc_programs": 2, "btc_programs_not_qualifying": 2, "excluded_non_btc": 283, "per_reason_note": "lab-2.2 does not record which of the BTC programs failed which rule (first observed after finishing vs below the notional floor)", "programs_observed": 285, "twap_checks": 33912}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 33.2 observable days; an ETA needs >= 5
- Capability: TWAP programs are read by polling each fixed-cohort account's twapHistory every 15 minutes. A program that starts and finishes between polls is first seen finished and excluded, so the collection systematically under-observes short programs. Observing starts needs an event stream (Hyperliquid's websocket user events for the cohort accounts). Not commissioned. Per-reason counts (research_tools/d1_diagnostics.py, Oct 19 2026): 282 programs, 280 not BTC, the 2 BTC programs first seen already finished, none rejected on notional - universe scarcity dominates, so a stream could at most recover those two against a design that needs 30 (the Oct 8 figure was 2 BTC in 272).

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
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 480 min): firings 6, episodes 2, scorable 2, retained 2, blocks 2
- Rates per observable day: test episodes 0.062, retained 0.062
- Exclusions (named in the design): records before 7 days of z history; panel quotes failing quality checks; events whose rr25_7d quotes are not qualified (regrouped *_ineligible; unknown quality stays unknown)
- Recorded counters: {"quote_policy": "qualified", "records": 4083, "with_z": 3594}
- Checkpoint 1: no ETA: 2 retained test observation(s) in 32.2 observable days; an ETA needs >= 5

### G1-alt-stress-propagation (ev-5cbc55c34b6d)

- Data: available
- Zeros: events occur; evidence accumulates with time
- Test (evaluation phase, primary 60 min): firings 11, episodes 11, scorable 11, retained 11, blocks 10
- Rates per observable day: test episodes 0.342, retained 0.342
- Exclusions (named in the design): same-minute co-movement is not leadership; windows with missing bars in any of the three assets
- Recorded counters: {"late_inputs": 581, "skipped_missing": 0, "steps": 10394}

### H1-deleveraging-stress (ev-02fcecefd1bf)

- Data: available
- Zeros: observed zero test episodes with data available
- Test (evaluation phase, primary 30 min): firings 0, episodes 0, scorable 0, retained 0, blocks 0
- Rates per observable day: test episodes 0.0, retained 0.0
- Exclusions (named in the design): buckets before 7 days of collected liquidation history; other venues' deleveraging data (unavailable)
- Recorded counters: {"buckets": 2570, "liquidation_orders": 54687, "stress_rows": 0, "unavailable_sources": ["bybit (HTTP 403 here)", "deribit liquidation flag (1h public delay)", "binance insurance fund"]}
- Checkpoint 1: no ETA: 0 retained test observation(s) in 33.2 observable days; an ETA needs >= 5

## Desk streams

| stream | limiting factor | detail |
|---|---|---|
| RC1D B2 vs B0 (24h) | time (accumulation) | {"blocks": 4, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 33.04, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 182, "rate_per_day": 5.51, "time_to_checkpoint": "~43 d"} |
| RC1D B2 vs B0 (4h) | time (accumulation) | {"blocks": 4, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 33.04, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 187, "rate_per_day": 5.66, "time_to_checkpoint": "~41 d"} |
| RC1D B2 vs B0 (72h) | time (accumulation) | {"blocks": 4, "calendar_exposure": {"basis": "calendar days since the stream start (one window per 4H decision)", "days": 33.04, "from": "2026-09-26T04:00:00Z"}, "checkpoint": {"block": 42, "need_blocks": 10}, "note": "one scored window per 4H decision when scoring keeps up; deterministic accumulation", "paired_scored": 170, "rate_per_day": 5.15, "time_to_checkpoint": "~49 d"} |
| Companion B2 vs B1 (24h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 8, "paired": 147} |
| Companion B2 vs B1 (4h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 9, "paired": 151} |
| Companion B2 vs B1 (72h) | time (accumulation) | {"checkpoint": {"block": 42, "need_blocks": 10}, "late": 0, "missing": 7, "paired": 136} |
| PS1 paper sizing | time (accumulation) | {"checkpoint": {}, "coverage": 0.9051, "intervals": 142, "outcomes": {"executed": 143, "missed: no run": 6, "missed: stale: processed after close + max_delay": 8, "no-rebalance: forecast unavailable": 1}} |

Rules: only with >= 5 qualifying observations; 90% Garwood interval on the rate. observed zero (collection capable) is reported separately from not observable; an unobservable rate is null, never 0.0. no design, threshold or evaluation version is changed by this report.
