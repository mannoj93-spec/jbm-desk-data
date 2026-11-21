# Research evidence

Generated 2026-11-21T07:39Z (input cutoff 2026-11-21T07:30Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit bd7f7a90de8c29b2568d65b09281638d773e4271; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-11-21T07:39Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-11-21T07:30Z (9 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 3 not required (bar-based) · 2 passed |
| Evidence maturity | 1 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 5 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 11/100 ; 10 | [-101.5 bp, +24.6 bp] | [-113.1 bp, +22.3 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 13/100 ; 8 | [-325.6 bp, +74.5 bp] | [-361.7 bp, +96.1 bp] | available | passed | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 19/100 ; 16 | [-18.1 bp, +47.4 bp] | [-16.6 bp, +53.5 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 11/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 11/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1334/1333/1333/1332/1333, reanalysis 46/46/46/46/46; 60m* eval 1334/1333/1333/1007/1333, reanalysis 46/46/46/28/46; 240m eval 1334/1330/1330/308/1330, reanalysis 46/46/46/11/46; 480m eval 1334/1326/1326/161/1326, reanalysis 46/46/46/6/46
- decision timing: 111 frozen events; lab persisted them 220.7 min (median, max 1060.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 16, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 16, episodes 11, scorable 11, retained 11 in 10 blocks; reference retained 76; test mean -25.1 bp vs reference +6.0 bp; 90% [-64.8 bp, +2.7 bp].
- frozen decisions: {'frozen_used': 153, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 13/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 13/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-21T07:39Z; 1403 closed hours + 1 partial; 1380 hours with eligible candidates; 1380 selected (1369 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.4 min after the hour (median, range 0.0-57.0)
- selections: 11 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 8cd4178d85cd18db; equal to the stored selections: True
- labelled controls = stored selections: 1380 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1334/1333/1333/1331/1333, reanalysis 46/46/46/46/46; 60m eval 1334/1333/1333/991/1333, reanalysis 46/46/46/28/46; 240m* eval 1334/1330/1330/307/1330, reanalysis 46/46/46/11/46; 480m eval 1334/1326/1326/160/1326, reanalysis 46/46/46/6/46
- decision timing: 18 frozen events; lab persisted them 280.9 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 25, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 25, episodes 17, scorable 17, retained 13 in 8 blocks; reference retained 307; test mean -63.5 bp vs reference -5.2 bp; 90% [-150.2 bp, +8.9 bp].
- frozen decisions: {'frozen_used': 25, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family C-liquidation: 18

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - under prospective evaluation
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-11-21T07:39Z; 1423 closed hours + 1 partial; 1400 hours with eligible candidates; 1400 selected (1389 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.1 min after the hour (median, range 0.0-56.2)
- selections: 11 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 ac33cd749e1b8e35; equal to the stored selections: True
- labelled controls = stored selections: 1400 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1334/1333/1333/1331/1333, reanalysis 66/66/66/66/45; 60m eval 1334/1333/1333/1032/1333, reanalysis 66/66/66/42/45; 240m eval 1334/1330/1330/313/1330, reanalysis 66/66/66/15/45; 480m* eval 1334/1326/1326/162/1326, reanalysis 66/66/66/8/45
- decision timing: 3 frozen events; lab persisted them 343.1 min (median, max 514.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 162; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 20, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (1): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 19/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 19/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1334/1333/1333/1332/1333, reanalysis 46/46/46/46/46; 60m* eval 1334/1333/1333/1003/1333, reanalysis 46/46/46/28/46; 240m eval 1334/1330/1330/308/1330, reanalysis 46/46/46/11/46; 480m eval 1334/1326/1326/161/1326, reanalysis 46/46/46/6/46
- decision timing: 19 frozen events; lab persisted them 207.3 min (median, max 704.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 19, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 19, episodes 19, scorable 19, retained 19 in 16 blocks; reference retained 1003; test mean -1.7 bp vs reference -12.5 bp; 90% [-5.9 bp, +29.4 bp].
- frozen decisions: {'frozen_used': 19, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1358/1357/1357/1332/1357, reanalysis 70/70/70/46/70; 60m eval 1358/1357/1357/1007/1357, reanalysis 70/70/70/28/70; 240m eval 1358/1354/1354/308/1354, reanalysis 70/70/70/11/70; 480m eval 1358/1350/1350/161/1350, reanalysis 70/70/70/6/70
- decision timing: 167 frozen events; lab persisted them 224.4 min (median, max 1055.4) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 157; test mean — vs reference -10.1 bp; 90% —.
- frozen decisions: {'frozen_used': 248, 'revised_since_frozen': 108, 'not_reproduced': 0, 'late_replay': 0, 'new': 7}
- variants tried in family H-deleveraging: 5

