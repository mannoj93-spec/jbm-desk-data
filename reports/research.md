# Research evidence

Generated 2026-10-15T07:18Z (input cutoff 2026-10-15T07:15Z). All times are UTC. lab-2.2-2026-09-24; code 7a59e3575684; commit 433780e399ee506820c21810b06bd971c8f47eab; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-10-15T07:18Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-10-15T07:15Z (3 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 5 not required (bar-based) · 3 passed |
| Evidence maturity | 5 exploratory · 3 under prospective evaluation; no design is supported |
| Publication | 8 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 3/100 ; 2 | [-61.2 bp, +87.2 bp] | [-76.7 bp, +88.8 bp] | available | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | — | — | available | passed | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 2/100 ; 1 | — | — | available | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | — | — | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | — | — | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | exploratory | 0/100 ; 0 | — | — | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 8/100 ; 8 | [-18.1 bp, +91.6 bp] | [-20.5 bp, +101.7 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 3/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 3/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 446/445/445/444/445, reanalysis 46/46/46/46/46; 60m* eval 446/444/444/302/444, reanalysis 46/46/46/28/46; 240m eval 446/441/441/103/441, reanalysis 46/46/46/11/46; 480m eval 446/437/437/54/437, reanalysis 46/46/46/6/46
- decision timing: 37 frozen events; lab persisted them 119.0 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 4, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 4, episodes 3, scorable 3, retained 3 in 2 blocks; reference retained 23; test mean -18.4 bp vs reference -8.3 bp; 90% [-52.3 bp, +64.6 bp].
- frozen decisions: {'frozen_used': 50, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 2}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (-49.1 bp vs +61.9 bp)
- variants tried in family A-flow: 15

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-15T07:18Z; 515 closed hours + 1 partial; 481 hours with eligible candidates; 481 selected (474 frozen earlier); 35 closed hours without a control (e.g. 11:00: missing collection: no record with required inputs available in this hour); availability 14.2 min after the hour (median, range 0.0-59.2)
- selections: 7 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 c257e567a8802786; equal to the stored selections: True
- labelled controls = stored selections: 481 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 435/434/434/431/434, reanalysis 46/46/46/45/46; 60m eval 435/433/433/298/433, reanalysis 46/46/46/28/46; 240m* eval 435/430/430/97/430, reanalysis 46/46/46/11/46; 480m eval 435/426/426/51/426, reanalysis 46/46/46/6/46
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family B-accounts: 18

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-15T07:18Z; 515 closed hours + 1 partial; 492 hours with eligible candidates; 492 selected (485 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.2 min after the hour (median, range 0.0-57.0)
- selections: 7 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 912cae13e4a8e73b; equal to the stored selections: True
- labelled controls = stored selections: 492 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 446/445/445/444/445, reanalysis 46/46/46/46/46; 60m eval 446/444/444/307/444, reanalysis 46/46/46/28/46; 240m* eval 446/441/441/102/441, reanalysis 46/46/46/11/46; 480m eval 446/437/437/54/437, reanalysis 46/46/46/6/46
- decision timing: 4 frozen events; lab persisted them 348.4 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 4, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 4, episodes 3, scorable 3, retained 2 in 1 blocks; reference retained 102; test mean -74.7 bp vs reference -15.8 bp; 90% —.
- frozen decisions: {'frozen_used': 4, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 470/469/469/444/469, reanalysis 70/70/70/46/70; 60m eval 470/468/468/302/468, reanalysis 70/70/70/28/70; 240m* eval 470/465/465/103/465, reanalysis 70/70/70/11/70; 480m eval 470/461/461/54/461, reanalysis 70/70/70/6/70
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 103; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 20910 twapHistory checks, 280 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
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

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-10-15T07:18Z; 535 closed hours + 1 partial; 512 hours with eligible candidates; 512 selected (505 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 13.6 min after the hour (median, range 0.0-56.2)
- selections: 7 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 6151f9edf8c937d1; equal to the stored selections: True
- labelled controls = stored selections: 512 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 446/445/445/443/445, reanalysis 66/66/66/66/45; 60m eval 446/444/444/304/444, reanalysis 66/66/66/42/45; 240m eval 446/441/441/103/441, reanalysis 66/66/66/15/45; 480m* eval 446/437/437/54/437, reanalysis 66/66/66/8/45
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 54; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 8/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 8/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 446/445/445/444/445, reanalysis 46/46/46/46/46; 60m* eval 446/444/444/301/444, reanalysis 46/46/46/28/46; 240m eval 446/441/441/103/441, reanalysis 46/46/46/11/46; 480m eval 446/437/437/54/437, reanalysis 46/46/46/6/46
- decision timing: 8 frozen events; lab persisted them 207.3 min (median, max 364.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 8, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 8, episodes 8, scorable 8, retained 8 in 8 blocks; reference retained 301; test mean +8.7 bp vs reference -13.8 bp; 90% [-2.9 bp, +54.9 bp].
- frozen decisions: {'frozen_used': 8, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 470/469/469/444/469, reanalysis 70/70/70/46/70; 60m eval 470/468/468/302/468, reanalysis 70/70/70/28/70; 240m eval 470/465/465/103/465, reanalysis 70/70/70/11/70; 480m eval 470/461/461/54/461, reanalysis 70/70/70/6/70
- decision timing: 53 frozen events; lab persisted them 156.0 min (median, max 629.9) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 52; test mean — vs reference -16.0 bp; 90% —.
- frozen decisions: {'frozen_used': 75, 'revised_since_frozen': 38, 'not_reproduced': 0, 'late_replay': 0, 'new': 3}
- variants tried in family H-deleveraging: 5

