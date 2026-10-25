# Research evidence

Generated 2026-10-25T11:57Z (input cutoff 2026-10-25T11:44Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit 276aad553a3795875a0f724ef644ce76bde290b9; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-10-25T11:57Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-10-25T11:44Z (13 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 5 not required (bar-based) · 3 passed |
| Evidence maturity | 4 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 8 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 6/100 ; 5 | [-56.3 bp, +66.7 bp] | [-66.5 bp, +70.2 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 7/100 ; 3 | [-68.0 bp, +24.0 bp] | [-57.2 bp, +22.6 bp] | available | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | — | — | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | — | — | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 11/100 ; 10 | [-17.6 bp, +64.5 bp] | [-17.9 bp, +71.1 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | — | — | available | passed | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 6/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 6/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 690/689/689/688/689, reanalysis 46/46/46/46/46; 60m* eval 690/689/689/491/689, reanalysis 46/46/46/28/46; 240m eval 690/686/686/159/686, reanalysis 46/46/46/11/46; 480m eval 690/682/682/84/682, reanalysis 46/46/46/6/46
- decision timing: 65 frozen events; lab persisted them 155.4 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 7, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 7, episodes 6, scorable 6, retained 6 in 5 blocks; reference retained 40; test mean -6.2 bp vs reference -5.9 bp; 90% [-33.2 bp, +43.3 bp].
- frozen decisions: {'frozen_used': 85, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (-14.3 bp vs +13.7 bp)
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 7/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 7/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-25T11:57Z; 759 closed hours + 1 partial; 736 hours with eligible candidates; 736 selected (729 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.4 min after the hour (median, range 0.0-57.0)
- selections: 7 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 195162744ac5dc45; equal to the stored selections: True
- labelled controls = stored selections: 736 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 690/689/689/688/689, reanalysis 46/46/46/46/46; 60m eval 690/689/689/494/689, reanalysis 46/46/46/28/46; 240m* eval 690/686/686/158/686, reanalysis 46/46/46/11/46; 480m eval 690/682/682/84/682, reanalysis 46/46/46/6/46
- decision timing: 11 frozen events; lab persisted them 274.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 17, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 17, episodes 10, scorable 10, retained 7 in 3 blocks; reference retained 158; test mean -29.1 bp vs reference -10.4 bp; 90% [-64.1 bp, +19.5 bp].
- frozen decisions: {'frozen_used': 17, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (1): d2_5m / prospective / evaluation / 240m: chronological halves disagree (-64.9 bp vs +0.1 bp)
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 714/713/713/688/713, reanalysis 70/70/70/46/70; 60m eval 714/713/713/491/713, reanalysis 70/70/70/28/70; 240m* eval 714/710/710/159/710, reanalysis 70/70/70/11/70; 480m eval 714/706/706/84/706, reanalysis 70/70/70/6/70
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 159; test mean — vs reference -12.0 bp; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 31079 twapHistory checks, 283 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
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
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-10-25T11:57Z; 779 closed hours + 1 partial; 756 hours with eligible candidates; 756 selected (749 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 13.7 min after the hour (median, range 0.0-56.2)
- selections: 7 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 d8b40db617d5f336; equal to the stored selections: True
- labelled controls = stored selections: 756 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 690/689/689/687/689, reanalysis 66/66/66/66/45; 60m eval 690/689/689/485/689, reanalysis 66/66/66/42/45; 240m eval 690/686/686/159/686, reanalysis 66/66/66/15/45; 480m* eval 690/682/682/84/682, reanalysis 66/66/66/8/45
- decision timing: 2 frozen events; lab persisted them 343.1 min (median, max 343.1) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 6, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 6, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 84; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 8, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (1): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 11/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 11/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 690/689/689/688/689, reanalysis 46/46/46/46/46; 60m* eval 690/689/689/488/689, reanalysis 46/46/46/28/46; 240m eval 690/686/686/159/686, reanalysis 46/46/46/11/46; 480m eval 690/682/682/84/682, reanalysis 46/46/46/6/46
- decision timing: 11 frozen events; lab persisted them 175.3 min (median, max 364.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 11, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 11, episodes 11, scorable 11, retained 11 in 10 blocks; reference retained 488; test mean +0.4 bp vs reference -12.3 bp; 90% [-6.3 bp, +37.3 bp].
- frozen decisions: {'frozen_used': 10, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- contradictory evidence (1): k3 / prospective / evaluation / 60m: chronological halves disagree (+32.4 bp vs -3.7 bp)
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 714/713/713/688/713, reanalysis 70/70/70/46/70; 60m eval 714/713/713/491/713, reanalysis 70/70/70/28/70; 240m eval 714/710/710/159/710, reanalysis 70/70/70/11/70; 480m eval 714/706/706/84/706, reanalysis 70/70/70/6/70
- decision timing: 82 frozen events; lab persisted them 176.4 min (median, max 918.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 79; test mean — vs reference -10.5 bp; 90% —.
- frozen decisions: {'frozen_used': 123, 'revised_since_frozen': 63, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family H-deleveraging: 5

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-10-25T11:57Z; 759 closed hours + 1 partial; 725 hours with eligible candidates; 725 selected (718 frozen earlier); 35 closed hours without a control (e.g. 11:00: missing collection: no record with required inputs available in this hour); availability 14.4 min after the hour (median, range 0.0-59.2)
- selections: 7 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 431b7343c2483115; equal to the stored selections: True
- labelled controls = stored selections: 725 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 679/678/678/675/678, reanalysis 46/46/46/45/46; 60m eval 679/678/678/485/678, reanalysis 46/46/46/28/46; 240m* eval 679/675/675/153/675, reanalysis 46/46/46/11/46; 480m eval 679/671/671/81/671, reanalysis 46/46/46/6/46
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family B-accounts: 18

