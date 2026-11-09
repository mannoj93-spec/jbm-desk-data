# Research evidence

Generated 2026-11-09T07:07Z (input cutoff 2026-11-09T07:00Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit 1e017a141a0c81eaaa65ab953491f67f156b3c88; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-11-09T07:07Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-11-09T07:00Z (7 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 5 not required (bar-based) · 3 passed |
| Evidence maturity | 4 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 8 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 9/100 ; 8 | [-76.6 bp, +41.0 bp] | [-85.3 bp, +38.2 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 9/100 ; 4 | [-69.8 bp, +20.7 bp] | [-60.9 bp, +20.7 bp] | available | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | — | — | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | — | — | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 17/100 ; 14 | [-14.5 bp, +53.2 bp] | [-12.7 bp, +59.8 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | — | — | available | passed | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 9/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 9/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1045/1045/1045/1044/1045, reanalysis 46/46/46/46/46; 60m* eval 1045/1044/1044/771/1044, reanalysis 46/46/46/28/46; 240m eval 1045/1041/1041/241/1041, reanalysis 46/46/46/11/46; 480m eval 1045/1037/1037/126/1037, reanalysis 46/46/46/6/46
- decision timing: 91 frozen events; lab persisted them 195.3 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 14, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 14, episodes 9, scorable 9, retained 9 in 8 blocks; reference retained 59; test mean -17.7 bp vs reference -0.1 bp; 90% [-46.4 bp, +12.9 bp].
- frozen decisions: {'frozen_used': 123, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 7}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (+11.9 bp vs -50.0 bp)
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 9/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 9/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-09T07:07Z; 1115 closed hours + 1 partial; 1092 hours with eligible candidates; 1092 selected (1083 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.6 min after the hour (median, range 0.0-57.0)
- selections: 9 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 40f21f6160ac8657; equal to the stored selections: True
- labelled controls = stored selections: 1092 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1046/1045/1045/1044/1045, reanalysis 46/46/46/46/46; 60m eval 1046/1044/1044/760/1044, reanalysis 46/46/46/28/46; 240m* eval 1046/1041/1041/239/1041, reanalysis 46/46/46/11/46; 480m eval 1046/1037/1037/126/1037, reanalysis 46/46/46/6/46
- decision timing: 14 frozen events; lab persisted them 280.9 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 21, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 21, episodes 13, scorable 13, retained 9 in 4 blocks; reference retained 239; test mean -36.5 bp vs reference -9.5 bp; 90% [-58.7 bp, +2.4 bp].
- frozen decisions: {'frozen_used': 21, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1069/1069/1069/1044/1069, reanalysis 70/70/70/46/70; 60m eval 1069/1068/1068/771/1068, reanalysis 70/70/70/28/70; 240m* eval 1069/1065/1065/241/1065, reanalysis 70/70/70/11/70; 480m eval 1069/1061/1061/126/1061, reanalysis 70/70/70/6/70
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 241; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 43175 twapHistory checks, 290 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
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
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-11-09T07:07Z; 1135 closed hours + 1 partial; 1111 hours with eligible candidates; 1111 selected (1103 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.0 min after the hour (median, range 0.0-56.2)
- selections: 8 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 404a186f77f1897d; equal to the stored selections: True
- labelled controls = stored selections: 1111 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1045/1045/1045/1043/1045, reanalysis 66/66/66/66/45; 60m eval 1045/1044/1044/775/1044, reanalysis 66/66/66/42/45; 240m eval 1045/1041/1041/243/1041, reanalysis 66/66/66/15/45; 480m* eval 1045/1037/1037/127/1037, reanalysis 66/66/66/8/45
- decision timing: 3 frozen events; lab persisted them 343.1 min (median, max 514.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 127; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 20, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (2): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 17/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 17/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1045/1045/1045/1044/1045, reanalysis 46/46/46/46/46; 60m* eval 1045/1044/1044/764/1044, reanalysis 46/46/46/28/46; 240m eval 1045/1041/1041/239/1041, reanalysis 46/46/46/11/46; 480m eval 1045/1037/1037/126/1037, reanalysis 46/46/46/6/46
- decision timing: 17 frozen events; lab persisted them 207.1 min (median, max 704.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 17, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 17, episodes 17, scorable 17, retained 17 in 14 blocks; reference retained 764; test mean +3.3 bp vs reference -12.5 bp; 90% [-1.9 bp, +34.9 bp].
- frozen decisions: {'frozen_used': 17, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1069/1069/1069/1044/1069, reanalysis 70/70/70/46/70; 60m eval 1069/1068/1068/771/1068, reanalysis 70/70/70/28/70; 240m eval 1069/1065/1065/241/1065, reanalysis 70/70/70/11/70; 480m eval 1069/1061/1061/126/1061, reanalysis 70/70/70/6/70
- decision timing: 123 frozen events; lab persisted them 197.5 min (median, max 918.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 118; test mean — vs reference -10.0 bp; 90% —.
- frozen decisions: {'frozen_used': 192, 'revised_since_frozen': 92, 'not_reproduced': 0, 'late_replay': 0, 'new': 2}
- variants tried in family H-deleveraging: 5

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-09T07:07Z; 1115 closed hours + 1 partial; 1080 hours with eligible candidates; 1080 selected (1071 frozen earlier); 36 closed hours without a control (e.g. 11:00: missing collection: no record with required inputs available in this hour); availability 14.6 min after the hour (median, range 0.0-59.2)
- selections: 9 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 f0c19c70cdc9149f; equal to the stored selections: True
- labelled controls = stored selections: 1080 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1034/1033/1033/1027/1033, reanalysis 46/46/46/45/46; 60m eval 1034/1032/1032/749/1032, reanalysis 46/46/46/28/46; 240m* eval 1034/1029/1029/234/1029, reanalysis 46/46/46/11/46; 480m eval 1034/1025/1025/123/1025, reanalysis 46/46/46/6/46
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family B-accounts: 18

