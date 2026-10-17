# Research evidence

Generated 2026-10-17T19:01Z (input cutoff 2026-10-17T18:59Z). All times are UTC. lab-2.2-2026-09-24; code 7a59e3575684; commit 9d7423124b9ffa211056ba263a133a81a9e81284; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-10-17T19:01Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-10-17T18:59Z (2 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 5 not required (bar-based) · 3 passed |
| Evidence maturity | 4 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 8 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 4/100 ; 3 | [-60.0 bp, +80.2 bp] | [-72.4 bp, +82.4 bp] | available | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | — | — | available | passed | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 7/100 ; 3 | [-68.0 bp, +23.6 bp] | [-56.9 bp, +24.2 bp] | available | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | — | — | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | — | — | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 1/100 ; 1 | — | — | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 9/100 ; 9 | [-14.4 bp, +77.4 bp] | [-14.5 bp, +87.0 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 4/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 4/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 505/505/505/504/505, reanalysis 46/46/46/46/46; 60m* eval 505/504/504/345/504, reanalysis 46/46/46/28/46; 240m eval 505/501/501/116/501, reanalysis 46/46/46/11/46; 480m eval 505/497/497/62/497, reanalysis 46/46/46/6/46
- decision timing: 42 frozen events; lab persisted them 118.7 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 5, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 5, episodes 4, scorable 4, retained 4 in 3 blocks; reference retained 26; test mean -8.4 bp vs reference -13.3 bp; 90% [-41.2 bp, +61.1 bp].
- frozen decisions: {'frozen_used': 56, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (-49.1 bp vs +58.9 bp)
- variants tried in family A-flow: 15

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-17T19:01Z; 575 closed hours + 1 partial; 540 hours with eligible candidates; 540 selected (535 frozen earlier); 35 closed hours without a control (e.g. 11:00: missing collection: no record with required inputs available in this hour); availability 14.2 min after the hour (median, range 0.0-59.2)
- selections: 5 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 bf3f18bcdbf44c01; equal to the stored selections: True
- labelled controls = stored selections: 540 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 494/494/494/491/494, reanalysis 46/46/46/45/46; 60m eval 494/493/493/341/493, reanalysis 46/46/46/28/46; 240m* eval 494/490/490/110/490, reanalysis 46/46/46/11/46; 480m eval 494/486/486/59/486, reanalysis 46/46/46/6/46
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family B-accounts: 18

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 7/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 7/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-17T19:01Z; 575 closed hours + 1 partial; 551 hours with eligible candidates; 551 selected (546 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.2 min after the hour (median, range 0.0-57.0)
- selections: 5 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 ddca1d3a43c0faa1; equal to the stored selections: True
- labelled controls = stored selections: 551 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 505/505/505/504/505, reanalysis 46/46/46/46/46; 60m eval 505/504/504/350/504, reanalysis 46/46/46/28/46; 240m* eval 505/501/501/115/501, reanalysis 46/46/46/11/46; 480m eval 505/497/497/62/497, reanalysis 46/46/46/6/46
- decision timing: 11 frozen events; lab persisted them 274.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 17, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 17, episodes 10, scorable 10, retained 7 in 3 blocks; reference retained 115; test mean -29.1 bp vs reference -10.3 bp; 90% [-64.0 bp, +19.1 bp].
- frozen decisions: {'frozen_used': 16, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 529/529/529/504/529, reanalysis 70/70/70/46/70; 60m eval 529/528/528/345/528, reanalysis 70/70/70/28/70; 240m* eval 529/525/525/116/525, reanalysis 70/70/70/11/70; 480m eval 529/521/521/62/521, reanalysis 70/70/70/6/70
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 116; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 23548 twapHistory checks, 281 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- variants tried in family D-twap: 10

### E1-liquidity-recovery @ ev-6f279983100b - exploratory
After a displayed-depth shock, do slow refills precede larger moves in the depleted side's direction than fast refills? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 60m eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 240m eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 480m eval 0/0/0/0/0, reanalysis 0/0/0/0/0
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- variants tried in family E-liquidity: 15

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - under prospective evaluation
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 1/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 1/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-10-17T19:01Z; 595 closed hours + 1 partial; 571 hours with eligible candidates; 571 selected (566 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 13.6 min after the hour (median, range 0.0-56.2)
- selections: 5 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 b8b138eecf82ed55; equal to the stored selections: True
- labelled controls = stored selections: 571 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 505/505/505/503/505, reanalysis 66/66/66/66/45; 60m eval 505/504/504/346/504, reanalysis 66/66/66/42/45; 240m eval 505/501/501/116/501, reanalysis 66/66/66/15/45; 480m* eval 505/497/497/62/497, reanalysis 66/66/66/8/45
- decision timing: 1 frozen events; lab persisted them 343.1 min (median, max 343.1) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 2, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 2, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 62; test mean -9.2 bp vs reference -5.1 bp; 90% —.
- frozen decisions: {'frozen_used': 2, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 9/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 9/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 505/505/505/504/505, reanalysis 46/46/46/46/46; 60m* eval 505/504/504/344/504, reanalysis 46/46/46/28/46; 240m eval 505/501/501/116/501, reanalysis 46/46/46/11/46; 480m eval 505/497/497/62/497, reanalysis 46/46/46/6/46
- decision timing: 9 frozen events; lab persisted them 175.3 min (median, max 364.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 9, scorable 9, retained 9 in 9 blocks; reference retained 344; test mean +6.8 bp vs reference -12.9 bp; 90% [-3.0 bp, +46.8 bp].
- frozen decisions: {'frozen_used': 9, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 529/529/529/504/529, reanalysis 70/70/70/46/70; 60m eval 529/528/528/345/528, reanalysis 70/70/70/28/70; 240m eval 529/525/525/116/525, reanalysis 70/70/70/11/70; 480m eval 529/521/521/62/521, reanalysis 70/70/70/6/70
- decision timing: 60 frozen events; lab persisted them 156.0 min (median, max 629.9) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 58; test mean — vs reference -12.7 bp; 90% —.
- frozen decisions: {'frozen_used': 87, 'revised_since_frozen': 45, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family H-deleveraging: 5

