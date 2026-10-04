# Research evidence

Generated 2026-10-04T01:13Z (input cutoff 2026-10-04T00:15Z). All times are UTC. lab-2.2-2026-09-24; code 7a59e3575684; commit 4adb6932f38dd35daecfa1ba19d858cb2bf88af9; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-10-04T01:13Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-10-04T00:15Z (58 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 5 not required (bar-based) · 3 passed |
| Evidence maturity | 6 exploratory · 2 under prospective evaluation; no design is supported |
| Publication | 8 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | — | — | insufficient_data | passed | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 2/100 ; 1 | — | — | insufficient_data | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | — | — | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | — | — | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | exploratory | 0/100 ; 0 | — | — | insufficient_data | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 3/100 ; 3 | [-2.9 bp, +135.0 bp] | [-1.0 bp, +147.0 bp] | insufficient_data | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 192/191/191/191/191, reanalysis 46/46/46/46/46; 60m* eval 192/191/191/121/191, reanalysis 46/46/46/28/46; 240m eval 192/191/191/43/191, reanalysis 46/46/46/11/46; 480m eval 192/188/188/23/188, reanalysis 46/46/46/6/46
- decision timing: 9 frozen events; lab persisted them 92.4 min (median, max 301.0) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 7; test mean — vs reference -14.6 bp; 90% —.
- frozen decisions: {'frozen_used': 14, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family A-flow: 15

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-04T01:13Z; 245 closed hours + 1 partial; 231 hours with eligible candidates; 231 selected (231 frozen earlier); 14 closed hours without a control (e.g. 11:00: missing collection: no record with required inputs available in this hour); availability 16.8 min after the hour (median, range 0.0-53.3)
- controls used: sha256 d2152246a560f2e8; equal to the stored selections: True
- labelled controls = stored selections: 231 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 185/185/185/183/185, reanalysis 46/46/46/45/46; 60m eval 185/185/185/122/185, reanalysis 46/46/46/28/46; 240m* eval 185/185/185/42/185, reanalysis 46/46/46/11/46; 480m eval 185/185/185/22/185, reanalysis 46/46/46/6/46
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 875 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 18

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-04T01:13Z; 245 closed hours + 1 partial; 238 hours with eligible candidates; 238 selected (234 frozen earlier); 7 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 16.8 min after the hour (median, range 0.0-57.0)
- selections: 4 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 eca48cc4b7e0643e; equal to the stored selections: True
- labelled controls = stored selections: 238 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 192/191/191/191/191, reanalysis 46/46/46/46/46; 60m eval 192/191/191/126/191, reanalysis 46/46/46/28/46; 240m* eval 192/191/191/43/191, reanalysis 46/46/46/11/46; 480m eval 192/188/188/23/188, reanalysis 46/46/46/6/46
- decision timing: 4 frozen events; lab persisted them 348.4 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 4, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 4, episodes 3, scorable 3, retained 2 in 1 blocks; reference retained 43; test mean -74.7 bp vs reference -12.5 bp; 90% —.
- frozen decisions: {'frozen_used': 4, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 888 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 199/193/193/191/193, reanalysis 70/70/70/46/70; 60m eval 199/193/193/121/193, reanalysis 70/70/70/28/70; 240m* eval 199/193/193/43/193, reanalysis 70/70/70/11/70; 480m eval 199/190/190/23/190, reanalysis 70/70/70/6/70
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 43; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 7381 twapHistory checks, 276 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
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
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-10-04T01:13Z; 265 closed hours + 1 partial; 258 hours with eligible candidates; 258 selected (254 frozen earlier); 7 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 16.8 min after the hour (median, range 0.0-56.2)
- selections: 4 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 1a38f798cb1828c7; equal to the stored selections: True
- labelled controls = stored selections: 258 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 192/191/191/191/191, reanalysis 66/66/66/66/45; 60m eval 192/191/191/126/191, reanalysis 66/66/66/42/45; 240m eval 192/191/191/43/191, reanalysis 66/66/66/15/45; 480m* eval 192/188/188/23/188, reanalysis 66/66/66/8/45
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 23; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 925 option records (454 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 3/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 3/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 192/191/191/191/191, reanalysis 46/46/46/46/46; 60m* eval 192/191/191/122/191, reanalysis 46/46/46/28/46; 240m eval 192/191/191/43/191, reanalysis 46/46/46/11/46; 480m eval 192/188/188/23/188, reanalysis 46/46/46/6/46
- decision timing: 3 frozen events; lab persisted them 175.3 min (median, max 207.3) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 3, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 3, episodes 3, scorable 3, retained 3 in 3 blocks; reference retained 122; test mean +31.2 bp vs reference -12.9 bp; 90% [-1.7 bp, +133.6 bp].
- frozen decisions: {'frozen_used': 3, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 11.2 days of stored bars; the design needs 14
- contradictory evidence (1): k3 / prospective / evaluation / 60m: chronological halves disagree (-0.5 bp vs +66.3 bp)
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 199/193/193/191/193, reanalysis 70/70/70/46/70; 60m eval 199/193/193/121/193, reanalysis 70/70/70/28/70; 240m eval 199/193/193/43/193, reanalysis 70/70/70/11/70; 480m eval 199/190/190/23/190, reanalysis 70/70/70/6/70
- decision timing: 17 frozen events; lab persisted them 155.9 min (median, max 297.1) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 17; test mean — vs reference -10.6 bp; 90% —.
- frozen decisions: {'frozen_used': 27, 'revised_since_frozen': 13, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family H-deleveraging: 5

