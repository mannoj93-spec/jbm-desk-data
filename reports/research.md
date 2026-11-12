# Research evidence

Generated 2026-11-12T20:24Z (input cutoff 2026-11-12T20:15Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit b89040f3e55aaf2424315c34375dd3d10de1f7c5; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-11-12T20:24Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-11-12T20:15Z (9 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 3 not required (bar-based) · 2 passed |
| Evidence maturity | 1 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 5 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 10/100 ; 9 | [-70.5 bp, +43.3 bp] | [-79.4 bp, +41.2 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 10/100 ; 5 | [-131.1 bp, +19.3 bp] | [-133.3 bp, +20.2 bp] | available | passed | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 18/100 ; 15 | [-14.5 bp, +51.0 bp] | [-14.0 bp, +57.1 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 10/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 10/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1131/1130/1130/1129/1130, reanalysis 46/46/46/46/46; 60m* eval 1131/1129/1129/836/1129, reanalysis 46/46/46/28/46; 240m eval 1131/1126/1126/260/1126, reanalysis 46/46/46/11/46; 480m eval 1131/1122/1122/136/1122, reanalysis 46/46/46/6/46
- decision timing: 96 frozen events; lab persisted them 214.0 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 15, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 15, episodes 10, scorable 10, retained 10 in 9 blocks; reference retained 63; test mean -12.3 bp vs reference +0.7 bp; 90% [-41.6 bp, +15.3 bp].
- frozen decisions: {'frozen_used': 134, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 2}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (+2.9 bp vs -33.7 bp)
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 10/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 10/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-12T20:24Z; 1200 closed hours + 1 partial; 1177 hours with eligible candidates; 1177 selected (1164 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.6 min after the hour (median, range 0.0-57.0)
- selections: 13 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 a420b920ec9699be; equal to the stored selections: True
- labelled controls = stored selections: 1177 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1131/1130/1130/1128/1130, reanalysis 46/46/46/46/46; 60m eval 1131/1130/1130/821/1130, reanalysis 46/46/46/28/46; 240m* eval 1131/1127/1127/258/1127, reanalysis 46/46/46/11/46; 480m eval 1131/1123/1123/136/1123, reanalysis 46/46/46/6/46
- decision timing: 15 frozen events; lab persisted them 274.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 22, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 22, episodes 14, scorable 14, retained 10 in 5 blocks; reference retained 258; test mean -46.6 bp vs reference -8.7 bp; 90% [-77.5 bp, -9.7 bp].
- frozen decisions: {'frozen_used': 22, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (1): d2_5m / prospective / evaluation / 240m: 90% interval [-77.5 bp, -9.7 bp] lies on the opposite side of zero
- variants tried in family C-liquidation: 18

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - under prospective evaluation
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-11-12T20:24Z; 1220 closed hours + 1 partial; 1197 hours with eligible candidates; 1197 selected (1184 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.0 min after the hour (median, range 0.0-56.2)
- selections: 13 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 4d3f98fe040a3040; equal to the stored selections: True
- labelled controls = stored selections: 1197 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1131/1130/1130/1128/1130, reanalysis 66/66/66/66/45; 60m eval 1131/1129/1129/850/1129, reanalysis 66/66/66/42/45; 240m eval 1131/1126/1126/263/1126, reanalysis 66/66/66/15/45; 480m* eval 1131/1122/1122/137/1122, reanalysis 66/66/66/8/45
- decision timing: 3 frozen events; lab persisted them 343.1 min (median, max 514.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 137; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 20, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (2): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 18/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 18/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1131/1130/1130/1129/1130, reanalysis 46/46/46/46/46; 60m* eval 1131/1129/1129/830/1129, reanalysis 46/46/46/28/46; 240m eval 1131/1126/1126/259/1126, reanalysis 46/46/46/11/46; 480m eval 1131/1122/1122/136/1122, reanalysis 46/46/46/6/46
- decision timing: 18 frozen events; lab persisted them 207.3 min (median, max 704.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 18, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 18, episodes 18, scorable 18, retained 18 in 15 blocks; reference retained 830; test mean +0.5 bp vs reference -12.3 bp; 90% [-4.7 bp, +32.0 bp].
- frozen decisions: {'frozen_used': 18, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1155/1154/1154/1129/1154, reanalysis 70/70/70/46/70; 60m eval 1155/1153/1153/836/1153, reanalysis 70/70/70/28/70; 240m eval 1155/1150/1150/260/1150, reanalysis 70/70/70/11/70; 480m eval 1155/1146/1146/136/1146, reanalysis 70/70/70/6/70
- decision timing: 134 frozen events; lab persisted them 222.2 min (median, max 918.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 129; test mean — vs reference -9.0 bp; 90% —.
- frozen decisions: {'frozen_used': 204, 'revised_since_frozen': 94, 'not_reproduced': 0, 'late_replay': 0, 'new': 2}
- variants tried in family H-deleveraging: 5

