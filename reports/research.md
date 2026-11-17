# Research evidence

Generated 2026-11-17T08:26Z (input cutoff 2026-11-17T08:15Z). All times are UTC. lab-2.2-2026-09-24; code 6885e925f0d4; commit 28b325e182659b4265ff7be2ef9630f32b654772; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

## At a glance

| Signal | State |
|---|---|
| Workflow | this report was written by the research-lab run at 2026-11-17T08:26Z; whether that run and the collector succeeded is on the repository's Actions tab |
| Data freshness | input cutoff 2026-11-17T08:15Z (11 min before this report); collection health and data age per dataset: [latest.md](latest.md) |
| Research integrity (latest attempt) | 3 not required (bar-based) · 2 passed |
| Evidence maturity | 1 exploratory · 4 under prospective evaluation; no design is supported |
| Publication | 5 valid · 0 BLOCKED · 0 proposal-eligible ([skill_proposals.md](skill_proposals.md)) |

> Workflow success, fresh data and passed integrity checks are not evidence of a trading edge. Intervals are descriptive; decisions are as-of replays by a 6-hourly lab, not live executions.

## Designs

Signals are kept apart: **Data** is the state of this design's inputs (collection health is in [latest.md](latest.md)); **Integrity** is whether the required inputs of this attempt validated (hourly controls: policy conflicts, stored = labelled); **Publication** is whether this attempt may stand as the current result and, if supported, feed a proposal. `—` = not yet computable (not enough data).

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | under prospective evaluation | 10/100 ; 9 | [-65.6 bp, +48.2 bp] | [-73.3 bp, +47.8 bp] | available | not required (bar-based) | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | under prospective evaluation | 11/100 ; 6 | [-130.9 bp, +128.2 bp] | [-130.1 bp, +108.0 bp] | available | passed | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | under prospective evaluation | 2/100 ; 2 | [-142.4 bp, +2.8 bp] | [-145.2 bp, -6.5 bp] | available | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | under prospective evaluation | 18/100 ; 15 | [-16.5 bp, +49.5 bp] | [-16.0 bp, +55.7 bp] | available | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | — | — | available | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - under prospective evaluation
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: 10/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 10/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1239/1238/1238/1237/1238, reanalysis 46/46/46/46/46; 60m* eval 1239/1237/1237/925/1237, reanalysis 46/46/46/28/46; 240m eval 1239/1234/1234/285/1234, reanalysis 46/46/46/11/46; 480m eval 1239/1230/1230/149/1230, reanalysis 46/46/46/6/46
- decision timing: 102 frozen events; lab persisted them 214.7 min (median, max 1060.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 15, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 15, episodes 10, scorable 10, retained 10 in 9 blocks; reference retained 69; test mean -12.3 bp vs reference +0.9 bp; 90% [-41.4 bp, +16.5 bp].
- frozen decisions: {'frozen_used': 141, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- contradictory evidence (1): q99_weak0.5 / prospective / evaluation / 60m: chronological halves disagree (+0.4 bp vs -30.0 bp)
- variants tried in family A-flow: 15

### C1-liquidation-cluster @ ev-eb20553bce1c - under prospective evaluation
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: 11/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 11/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-11-17T08:26Z; 1308 closed hours + 1 partial; 1285 hours with eligible candidates; 1285 selected (1260 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.5 min after the hour (median, range 0.0-57.0)
- selections: 25 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 525964217cdc42e7; equal to the stored selections: True
- labelled controls = stored selections: 1285 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1239/1238/1238/1236/1238, reanalysis 46/46/46/46/46; 60m eval 1239/1238/1238/908/1238, reanalysis 46/46/46/28/46; 240m* eval 1239/1235/1235/284/1235, reanalysis 46/46/46/11/46; 480m eval 1239/1231/1231/149/1231, reanalysis 46/46/46/6/46
- decision timing: 16 frozen events; lab persisted them 274.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 23, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 11; test mean -4.0 bp vs reference +7.1 bp; 90% —.
- prospective/evaluation: test firings 23, episodes 15, scorable 15, retained 11 in 6 blocks; reference retained 284; test mean -31.2 bp vs reference -6.6 bp; 90% [-61.8 bp, +16.3 bp].
- frozen decisions: {'frozen_used': 23, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family C-liquidation: 18

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - under prospective evaluation
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: 2/100 retained test observations before checkpoint 1.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 2/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-11-17T08:26Z; 1328 closed hours + 1 partial; 1305 hours with eligible candidates; 1305 selected (1280 frozen earlier); 24 closed hours without a control (e.g. 12:00: missing collection: no record with required inputs available in this hour); availability 14.0 min after the hour (median, range 0.0-56.2)
- selections: 25 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 ecef39aa7dddef4b; equal to the stored selections: True
- labelled controls = stored selections: 1305 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1239/1238/1238/1236/1238, reanalysis 66/66/66/66/45; 60m eval 1239/1237/1237/945/1237, reanalysis 66/66/66/42/45; 240m eval 1239/1234/1234/289/1234, reanalysis 66/66/66/15/45; 480m* eval 1239/1230/1230/151/1230, reanalysis 66/66/66/8/45
- decision timing: 3 frozen events; lab persisted them 343.1 min (median, max 514.2) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 9, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 8; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 9, episodes 2, scorable 2, retained 2 in 2 blocks; reference retained 151; test mean -81.8 bp vs reference -12.0 bp; 90% [-142.4 bp, +2.8 bp].
- frozen decisions: {'frozen_used': 20, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- contradictory evidence (2): z2 / prospective / evaluation / 240m: 90% interval [-107.3 bp, -4.5 bp] lies on the opposite side of zero
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - under prospective evaluation
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: 18/100 retained test observations before checkpoint 1.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 18/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1239/1238/1238/1237/1238, reanalysis 46/46/46/46/46; 60m* eval 1239/1237/1237/921/1237, reanalysis 46/46/46/28/46; 240m eval 1239/1234/1234/285/1234, reanalysis 46/46/46/11/46; 480m eval 1239/1230/1230/149/1230, reanalysis 46/46/46/6/46
- decision timing: 18 frozen events; lab persisted them 207.3 min (median, max 704.5) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 18, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean — vs reference -12.0 bp; 90% —.
- prospective/evaluation: test firings 18, episodes 18, scorable 18, retained 18 in 15 blocks; reference retained 921; test mean +0.5 bp vs reference -12.3 bp; 90% [-4.3 bp, +31.3 bp].
- frozen decisions: {'frozen_used': 18, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1263/1262/1262/1237/1262, reanalysis 70/70/70/46/70; 60m eval 1263/1261/1261/925/1261, reanalysis 70/70/70/28/70; 240m eval 1263/1258/1258/285/1258, reanalysis 70/70/70/11/70; 480m eval 1263/1254/1254/149/1254, reanalysis 70/70/70/6/70
- decision timing: 154 frozen events; lab persisted them 224.4 min (median, max 1055.4) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean — vs reference —; 90% —.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 147; test mean — vs reference -11.0 bp; 90% —.
- frozen decisions: {'frozen_used': 236, 'revised_since_frozen': 105, 'not_reproduced': 0, 'late_replay': 0, 'new': 3}
- variants tried in family H-deleveraging: 5

