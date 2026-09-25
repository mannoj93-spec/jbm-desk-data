# Research evidence

Generated 2026-09-25T18:47Z (input cutoff 2026-09-25T18:46Z); lab-2.2-2026-09-24; code 200239d3de0f; commit 1334078866cb98c85d2a494dda9914bd836d976a; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.

Three separate signals: **collection health** is the collector's (reports/latest.md; the Data column is the state of this design's inputs); **research integrity** is whether the design's required inputs (hourly controls: policy conflicts, stored = labelled) validated in this attempt; **publication** is whether this attempt's evaluation may stand as the current result and, if supported, feed a proposal. A blocked attempt names the last valid result instead of presenting it as current.

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data | Integrity | Publication |
|---|---|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c368833b5ae6 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | not required (bar-based) | valid |
| account_behavior | B1-underwater-adds @ ev-125c86066f05 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | passed | valid |
| liq_exposure | C1-liquidation-cluster @ ev-eb20553bce1c | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | passed | valid |
| twap_lifecycle | D1-active-twap @ ev-2b023a90293f | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | not required (bar-based) | valid |
| liquidity_recovery | E1-liquidity-recovery @ ev-6f279983100b | exploratory | 0/100 ; 0 | n/a | n/a | unavailable | not required (bar-based) | valid |
| options_disagreement | F1-options-perp-disagreement @ ev-1c53cfe81c9f | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | passed | valid |
| cross_asset | G1-alt-stress-propagation @ ev-5cbc55c34b6d | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | not required (bar-based) | valid |
| deleveraging | H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data | not required (bar-based) | valid |

## Per design

### A1-flow-absorption @ ev-c368833b5ae6 - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1/0/0/0/0, reanalysis 46/46/46/46/46; 60m* eval 1/0/0/0/0, reanalysis 46/46/46/28/46; 240m eval 1/0/0/0/0, reanalysis 46/43/43/10/43; 480m eval 1/0/0/0/0, reanalysis 46/39/39/5/39
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 3.0 days of stored 1-minute bars; the event threshold needs 7 days of prior windows
- variants tried in family A-flow: 15

### B1-underwater-adds @ ev-125c86066f05 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-09-25T18:47Z; 46 closed hours + 1 partial; 47 hours with eligible candidates; 47 selected (46 frozen earlier); 0 closed hours without a control; availability 17.7 min after the hour (median, range 0.1-48.1)
- selections: 1 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 6e7dfd88230460ee; equal to the stored selections: True
- labelled controls = stored selections: 47 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1/0/0/0/0, reanalysis 46/46/46/45/46; 60m eval 1/0/0/0/0, reanalysis 46/46/46/28/46; 240m* eval 1/0/0/0/0, reanalysis 46/43/43/10/43; 480m eval 1/0/0/0/0, reanalysis 46/39/39/5/39
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 178 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 18

### C1-liquidation-cluster @ ev-eb20553bce1c - exploratory
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-09-25T18:47Z; 46 closed hours + 1 partial; 47 hours with eligible candidates; 47 selected (46 frozen earlier); 0 closed hours without a control; availability 17.7 min after the hour (median, range 0.1-30.5)
- selections: 1 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 1e7882dda8237f6a; equal to the stored selections: True
- labelled controls = stored selections: 47 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1/0/0/0/0, reanalysis 46/46/46/46/46; 60m eval 1/0/0/0/0, reanalysis 46/46/46/28/46; 240m* eval 1/0/0/0/0, reanalysis 46/43/43/10/43; 480m eval 1/0/0/0/0, reanalysis 46/39/39/5/39
- decision timing: 1 frozen events; lab persisted them 2402.7 min (median, max 2402.7) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 1, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 10; test mean -4.0 bp vs reference +5.6 bp; 90% n/a.
- prospective/evaluation: test firings 1, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 1, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 180 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 18

### D1-active-twap @ ev-2b023a90293f - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1/0/0/0/0, reanalysis 70/70/70/46/70; 60m eval 1/0/0/0/0, reanalysis 70/70/70/28/70; 240m* eval 1/0/0/0/0, reanalysis 70/67/67/10/67; 480m eval 1/0/0/0/0, reanalysis 70/63/63/5/63
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 10; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1486 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- variants tried in family D-twap: 10

### E1-liquidity-recovery @ ev-6f279983100b - exploratory
After a displayed-depth shock, do slow refills precede larger moves in the depleted side's direction than fast refills? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 60m eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 240m eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 480m eval 0/0/0/0/0, reanalysis 0/0/0/0/0
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- variants tried in family E-liquidity: 15

### F1-options-perp-disagreement @ ev-1c53cfe81c9f - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: no evaluation observations yet.
- research integrity: passed; publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-09-25T18:47Z; 66 closed hours + 1 partial; 67 hours with eligible candidates; 67 selected (66 frozen earlier); 0 closed hours without a control; availability 17.6 min after the hour (median, range 11.7-28.0)
- selections: 1 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 28043de0321a0875; equal to the stored selections: True
- labelled controls = stored selections: 67 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1/0/0/0/0, reanalysis 66/66/66/66/45; 60m eval 1/0/0/0/0, reanalysis 66/66/66/42/45; 240m eval 1/0/0/0/0, reanalysis 66/63/63/14/42; 480m* eval 1/0/0/0/0, reanalysis 66/59/59/7/38
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 7; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 217 option records (0 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 23

### G1-alt-stress-propagation @ ev-5cbc55c34b6d - exploratory
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 1/0/0/0/0, reanalysis 46/46/46/46/46; 60m* eval 1/0/0/0/0, reanalysis 46/46/46/28/46; 240m eval 1/0/0/0/0, reanalysis 46/43/43/10/43; 480m eval 1/0/0/0/0, reanalysis 46/39/39/5/39
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 28; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 3.0 days of stored bars; the design needs 14
- variants tried in family G-cross: 15

### H1-deleveraging-stress @ ev-02fcecefd1bf - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- research integrity: not required (bar-based); publication: valid
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 1/0/0/0/0, reanalysis 70/70/70/46/70; 60m eval 1/0/0/0/0, reanalysis 70/70/70/28/70; 240m eval 1/0/0/0/0, reanalysis 70/67/67/10/67; 480m eval 1/0/0/0/0, reanalysis 70/63/63/5/63
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 3.7 days of collected OKX liquidation history; the p99 threshold needs 7
- variants tried in family H-deleveraging: 5

