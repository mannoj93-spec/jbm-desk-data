# Research evidence

Generated 2026-10-07T00:58Z (input cutoff 2026-10-07T00:56Z). All times are UTC. lab-2.2-2026-09-24; code 7a59e3575684; commit a3492b4ef2cfd47a2a26788af7262b7ac325ffbb; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-10-07T00:58Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-10-07T00:56Z (2 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 5 not required (bar-based) · 3 passed |
| Evidence maturity | 5 exploratory · 3 under prospective evaluation; no design is supported |
| Publication | 8 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 2/100 ; 1 | — | — | available | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | — | — | insufficient_data | passed | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 2/100 ; 1 | — | — | insufficient_data | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | — | — | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | — | — | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | exploratory | 0/100 ; 0 | — | — | insufficient_data | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 4/100 ; 4 | [-14.2 bp, +135.1 bp] | [-11.3 bp, +146.9 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 247/247/247/246/247, reanalysis 46/46/46/46/46; 60m* eval 247/246/246/164/246, reanalysis 46/46/46/28/46; 240m eval 247/243/243/58/243, reanalysis 46/46/46/11/46; 480m eval 247/239/239/31/239, reanalysis 46/46/46/6/46
- decision timing: 16 frozen events; lab persisted them 139.8 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 2, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 2, episodes 2, scorable 2, retained 2 in 1 blocks; reference retained 11; test mean -48.8 bp vs reference -3.4 bp; 90% —.
- frozen decisions: {'frozen_used': 24, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- reconstruction/exploratory: test firings 15, episodes 9, scorable 9, retained 8 in 7 blocks; reference retained 91; test mean -38.7 bp vs reference -4.8 bp; 90% [-56.8 bp, -11.7 bp].
- contradictory evidence (1): q95_weak0.5 / reconstruction / exploratory / 60m: chronological halves disagree (+11.5 bp vs -9.8 bp)
- variants tried in family A-flow: 15

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-07T00:58Z; 316 closed hours + 1 partial; 282 hours with eligible candidates; 282 selected (276 frozen earlier); 35 closed hours without a control (e.g. 11:00: missing collection: no record with required inputs available in this hour); availability 16.3 min after the hour (median, range 0.0-59.2)
- selections: 6 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 ed07308273fa03e7; equal to the stored selections: True
- labelled controls = stored selections: 282 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 236/236/236/233/236, reanalysis 46/46/46/45/46; 60m eval 236/235/235/158/235, reanalysis 46/46/46/28/46; 240m* eval 236/232/232/53/232, reanalysis 46/46/46/11/46; 480m eval 236/228/228/28/228, reanalysis 46/46/46/6/46
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1202 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 18

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-07T00:58Z; 316 closed hours + 1 partial; 293 hours with eligible candidates; 293 selected (287 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 16.3 min after the hour (median, range 0.0-57.0)
- selections: 6 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 b0c32186a9099d7e; equal to the stored selections: True
- labelled controls = stored selections: 293 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 247/247/247/246/247, reanalysis 46/46/46/46/46; 60m eval 247/246/246/167/246, reanalysis 46/46/46/28/46; 240m* eval 247/243/243/58/243, reanalysis 46/46/46/11/46; 480m eval 247/239/239/31/239, reanalysis 46/46/46/6/46
- decision timing: 4 frozen events; lab persisted them 348.4 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 4, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 4, episodes 3, scorable 3, retained 2 in 1 blocks; reference retained 58; test mean -74.7 bp vs reference -11.2 bp; 90% —.
- frozen decisions: {'frozen_used': 4, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1221 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 271/271/271/246/271, reanalysis 70/70/70/46/70; 60m eval 271/270/270/164/270, reanalysis 70/70/70/28/70; 240m* eval 271/267/267/58/267, reanalysis 70/70/70/11/70; 480m eval 271/263/263/31/263, reanalysis 70/70/70/6/70
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 58; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 10155 twapHistory checks, 277 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
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
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-10-07T00:58Z; 336 closed hours + 1 partial; 313 hours with eligible candidates; 313 selected (307 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 16.1 min after the hour (median, range 0.0-56.2)
- selections: 6 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 65244feb25645259; equal to the stored selections: True
- labelled controls = stored selections: 313 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 247/247/247/246/247, reanalysis 66/66/66/66/45; 60m eval 247/246/246/165/246, reanalysis 66/66/66/42/45; 240m eval 247/243/243/58/243, reanalysis 66/66/66/15/45; 480m* eval 247/239/239/31/239, reanalysis 66/66/66/8/45
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 31; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1258 option records (770 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 4/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 4/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 247/247/247/246/247, reanalysis 46/46/46/46/46; 60m* eval 247/246/246/165/246, reanalysis 46/46/46/28/46; 240m eval 247/243/243/58/243, reanalysis 46/46/46/11/46; 480m eval 247/239/239/31/239, reanalysis 46/46/46/6/46
- decision timing: 4 frozen events; lab persisted them 175.3 min (median, max 207.3) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 4, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 4, episodes 4, scorable 4, retained 4 in 4 blocks; reference retained 165; test mean +16.9 bp vs reference -13.2 bp; 90% [-8.8 bp, +89.7 bp].
- frozen decisions: {'frozen_used': 4, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- reconstruction/exploratory: test firings 49, episodes 46, scorable 46, retained 42 in 33 blocks; reference retained 1437; test mean -14.5 bp vs reference -12.3 bp; 90% [-19.9 bp, +11.2 bp].
- contradictory evidence (3): k3 / prospective / evaluation / 60m: chronological halves disagree (-1.0 bp vs +40.5 bp)
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 271/271/271/246/271, reanalysis 70/70/70/46/70; 60m eval 271/270/270/164/270, reanalysis 70/70/70/28/70; 240m eval 271/267/267/58/267, reanalysis 70/70/70/11/70; 480m eval 271/263/263/31/263, reanalysis 70/70/70/6/70
- decision timing: 25 frozen events; lab persisted them 155.9 min (median, max 629.9) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 24; test mean — vs reference -14.9 bp; 90% —.
- frozen decisions: {'frozen_used': 39, 'revised_since_frozen': 16, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family H-deleveraging: 5

