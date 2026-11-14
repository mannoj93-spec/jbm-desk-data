# Research evidence

Generated 2026-11-14T06:58Z (input cutoff 2026-11-14T06:44Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit 603dd204d9aec17c5be0da94163ff461658ba7d1; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-11-14T06:58Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-11-14T06:44Z (14 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 3 not required (bar-based) · 2 passed |
| Evidence maturity | 1 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 5 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 10/100 ; 9 | [-64.0 bp, +37.0 bp] | [-71.9 bp, +33.9 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 10/100 ; 5 | [-134.1 bp, +18.7 bp] | [-131.9 bp, +20.0 bp] | available | passed | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 18/100 ; 15 | [-18.0 bp, +53.3 bp] | [-18.2 bp, +59.8 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 10/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 10/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1165/1164/1164/1163/1164, reanalysis 46/46/46/46/46; 60m* eval 1165/1164/1164/868/1164, reanalysis 46/46/46/28/46; 240m eval 1165/1161/1161/268/1161, reanalysis 46/46/46/11/46; 480m eval 1165/1157/1157/141/1157, reanalysis 46/46/46/6/46
- decision timing: 100 frozen events; lab persisted them 214.7 min (median, max 610.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 15, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 15, episodes 10, scorable 10, retained 10 in 9 blocks; reference retained 67; test mean -12.3 bp vs reference +1.0 bp; 90% [-40.8 bp, +15.2 bp].
- frozen decisions: {'frozen_used': 139, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (+0.4 bp vs -30.8 bp)
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 10/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 10/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-14T06:58Z; 1234 closed hours + 1 partial; 1211 hours with eligible candidates; 1211 selected (1200 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.6 min after the hour (median, range 0.0-57.0)
- selections: 11 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 f20b00c6e2ca941e; equal to the stored selections: True
- labelled controls = stored selections: 1211 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1165/1165/1165/1163/1165, reanalysis 46/46/46/46/46; 60m eval 1165/1164/1164/848/1164, reanalysis 46/46/46/28/46; 240m* eval 1165/1161/1161/266/1161, reanalysis 46/46/46/11/46; 480m eval 1165/1157/1157/140/1157, reanalysis 46/46/46/6/46
- decision timing: 15 frozen events; lab persisted them 274.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 22, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 22, episodes 14, scorable 14, retained 10 in 5 blocks; reference retained 266; test mean -46.6 bp vs reference -7.5 bp; 90% [-78.7 bp, -10.7 bp].
- frozen decisions: {'frozen_used': 22, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (1): d2_5m / prospective / evaluation / 240m: 90% interval [-78.7 bp, -10.7 bp] lies on the opposite side of zero
- variants tried in family C-liquidation: 18

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - under prospective evaluation
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-11-14T06:58Z; 1254 closed hours + 1 partial; 1231 hours with eligible candidates; 1231 selected (1220 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.0 min after the hour (median, range 0.0-56.2)
- selections: 11 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 adc57c1170d2d4a8; equal to the stored selections: True
- labelled controls = stored selections: 1231 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1165/1164/1164/1162/1164, reanalysis 66/66/66/66/45; 60m eval 1165/1164/1164/882/1164, reanalysis 66/66/66/42/45; 240m eval 1165/1161/1161/271/1161, reanalysis 66/66/66/15/45; 480m* eval 1165/1157/1157/142/1157, reanalysis 66/66/66/8/45
- decision timing: 3 frozen events; lab persisted them 343.1 min (median, max 514.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 142; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 20, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (2): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 18/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 18/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1165/1164/1164/1163/1164, reanalysis 46/46/46/46/46; 60m* eval 1165/1164/1164/862/1164, reanalysis 46/46/46/28/46; 240m eval 1165/1161/1161/267/1161, reanalysis 46/46/46/11/46; 480m eval 1165/1157/1157/140/1157, reanalysis 46/46/46/6/46
- decision timing: 18 frozen events; lab persisted them 207.3 min (median, max 704.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 18, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 18, episodes 18, scorable 18, retained 18 in 15 blocks; reference retained 862; test mean +0.5 bp vs reference -12.3 bp; 90% [-4.6 bp, +31.9 bp].
- frozen decisions: {'frozen_used': 18, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1189/1188/1188/1163/1188, reanalysis 70/70/70/46/70; 60m eval 1189/1188/1188/868/1188, reanalysis 70/70/70/28/70; 240m eval 1189/1185/1185/268/1185, reanalysis 70/70/70/11/70; 480m eval 1189/1181/1181/141/1181, reanalysis 70/70/70/6/70
- decision timing: 144 frozen events; lab persisted them 222.2 min (median, max 918.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 138; test mean — vs reference -9.7 bp; 90% —.
- frozen decisions: {'frozen_used': 221, 'revised_since_frozen': 99, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- variants tried in family H-deleveraging: 5

