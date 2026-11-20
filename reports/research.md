# Research evidence

Generated 2026-11-20T07:42Z (input cutoff 2026-11-20T07:30Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit 53b5581e8580b9b3539a7f09084adc3c6c966494; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-11-20T07:42Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-11-20T07:30Z (12 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 3 not required (bar-based) · 2 passed |
| Evidence maturity | 1 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 5 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 11/100 ; 10 | [-100.5 bp, +30.1 bp] | [-109.5 bp, +27.0 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 12/100 ; 7 | [-95.8 bp, +114.0 bp] | [-120.9 bp, +122.1 bp] | available | passed | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 19/100 ; 16 | [-19.0 bp, +47.3 bp] | [-18.8 bp, +53.3 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 11/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 11/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1310/1309/1309/1308/1309, reanalysis 46/46/46/46/46; 60m* eval 1310/1309/1309/987/1309, reanalysis 46/46/46/28/46; 240m eval 1310/1306/1306/302/1306, reanalysis 46/46/46/11/46; 480m eval 1310/1302/1302/158/1302, reanalysis 46/46/46/6/46
- decision timing: 108 frozen events; lab persisted them 220.7 min (median, max 1060.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 16, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 16, episodes 11, scorable 11, retained 11 in 10 blocks; reference retained 73; test mean -25.1 bp vs reference +3.1 bp; 90% [-60.7 bp, +6.2 bp].
- frozen decisions: {'frozen_used': 149, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 12/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 12/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-20T07:42Z; 1379 closed hours + 1 partial; 1356 hours with eligible candidates; 1356 selected (1345 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.4 min after the hour (median, range 0.0-57.0)
- selections: 11 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 d0e492301ac3564e; equal to the stored selections: True
- labelled controls = stored selections: 1356 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1310/1309/1309/1307/1309, reanalysis 46/46/46/46/46; 60m eval 1310/1309/1309/969/1309, reanalysis 46/46/46/28/46; 240m* eval 1310/1306/1306/301/1306, reanalysis 46/46/46/11/46; 480m eval 1310/1302/1302/158/1302, reanalysis 46/46/46/6/46
- decision timing: 17 frozen events; lab persisted them 274.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 24, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 24, episodes 16, scorable 16, retained 12 in 7 blocks; reference retained 301; test mean -21.9 bp vs reference -5.7 bp; 90% [-51.7 bp, +28.3 bp].
- frozen decisions: {'frozen_used': 24, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family C-liquidation: 18

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - under prospective evaluation
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-11-20T07:42Z; 1399 closed hours + 1 partial; 1376 hours with eligible candidates; 1376 selected (1365 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.1 min after the hour (median, range 0.0-56.2)
- selections: 11 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 a6bdd1275707fef2; equal to the stored selections: True
- labelled controls = stored selections: 1376 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1310/1309/1309/1307/1309, reanalysis 66/66/66/66/45; 60m eval 1310/1309/1309/1012/1309, reanalysis 66/66/66/42/45; 240m eval 1310/1306/1306/307/1306, reanalysis 66/66/66/15/45; 480m* eval 1310/1302/1302/159/1302, reanalysis 66/66/66/8/45
- decision timing: 3 frozen events; lab persisted them 343.1 min (median, max 514.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 159; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 20, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (1): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 19/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 19/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1310/1309/1309/1308/1309, reanalysis 46/46/46/46/46; 60m* eval 1310/1309/1309/983/1309, reanalysis 46/46/46/28/46; 240m eval 1310/1306/1306/302/1306, reanalysis 46/46/46/11/46; 480m eval 1310/1302/1302/158/1302, reanalysis 46/46/46/6/46
- decision timing: 19 frozen events; lab persisted them 207.3 min (median, max 704.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 19, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 19, episodes 19, scorable 19, retained 19 in 16 blocks; reference retained 983; test mean -1.7 bp vs reference -12.4 bp; 90% [-6.2 bp, +29.5 bp].
- frozen decisions: {'frozen_used': 19, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1334/1333/1333/1308/1333, reanalysis 70/70/70/46/70; 60m eval 1334/1333/1333/987/1333, reanalysis 70/70/70/28/70; 240m eval 1334/1330/1330/302/1330, reanalysis 70/70/70/11/70; 480m eval 1334/1326/1326/158/1326, reanalysis 70/70/70/6/70
- decision timing: 157 frozen events; lab persisted them 224.4 min (median, max 1055.4) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 150; test mean — vs reference -11.9 bp; 90% —.
- frozen decisions: {'frozen_used': 241, 'revised_since_frozen': 106, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- variants tried in family H-deleveraging: 5

