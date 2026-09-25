# Research evidence

Generated 2026-09-25T15:41Z (input cutoff 2026-09-25T15:31Z); lab-2.2-2026-09-24; code 44c2f35d533a; commit 84dd74af109d51a84f1049a18e52d4a31916321c; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data |
|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c35cdb2bc9bc | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| account_behavior | B1-underwater-adds @ ev-5db159f025fd | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liq_exposure | C1-liquidation-cluster @ ev-2ace4c5a6647 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| twap_lifecycle | D1-active-twap @ ev-ffa18ae355ef | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liquidity_recovery | E1-liquidity-recovery @ ev-79ea1d99704b | exploratory | 0/100 ; 0 | n/a | n/a | unavailable |
| options_disagreement | F1-options-perp-disagreement @ ev-33998e4f9082 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| cross_asset | G1-alt-stress-propagation @ ev-44a97c2d5259 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| deleveraging | H1-deleveraging-stress @ ev-e76cbdabf3f9 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |

## Per design

### A1-flow-absorption @ ev-c35cdb2bc9bc - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 18/17/17/17/17, reanalysis 26/26/26/26/26; 60m* eval 18/17/17/11/17, reanalysis 26/26/26/15/26; 240m eval 18/14/14/3/14, reanalysis 26/26/26/6/26; 480m eval 18/10/10/2/10, reanalysis 26/26/26/3/26
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 2.8 days of stored 1-minute bars; the event threshold needs 7 days of prior windows
- variants tried in family A-flow: 12

### B1-underwater-adds @ ev-5db159f025fd - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-09-25T15:41Z; 43 closed hours + 1 partial; 44 hours with eligible candidates; 44 selected (0 frozen earlier); 0 closed hours without a control; availability 17.7 min after the hour (median, range 0.1-48.1)
- selections: 44 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 51c1016dc4aca936; equal to the stored selections: True
- labelled controls = stored selections: 44 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 44/43/43/42/43; 60m eval 0/0/0/0/0, reanalysis 44/43/43/26/43; 240m* eval 0/0/0/0/0, reanalysis 44/40/40/9/40; 480m eval 0/0/0/0/0, reanalysis 44/36/36/4/36
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 165 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 15

### C1-liquidation-cluster @ ev-2ace4c5a6647 - exploratory
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T20:00Z to 2026-09-25T15:41Z; 43 closed hours + 1 partial; 44 hours with eligible candidates; 44 selected (0 frozen earlier); 0 closed hours without a control; availability 17.7 min after the hour (median, range 0.1-30.5)
- selections: 44 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 f0b0e284907acad2; equal to the stored selections: True
- labelled controls = stored selections: 44 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 44/43/43/43/43; 60m eval 0/0/0/0/0, reanalysis 44/43/43/26/43; 240m* eval 0/0/0/0/0, reanalysis 44/40/40/9/40; 480m eval 0/0/0/0/0, reanalysis 44/36/36/4/36
- decision timing: 1 frozen events; lab persisted them 2291.1 min (median, max 2291.1) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 1, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 9; test mean -4.0 bp vs reference +4.0 bp; 90% n/a.
- prospective/evaluation: test firings 1, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- prospective data: 167 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 15

### D1-active-twap @ ev-ffa18ae355ef - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 18/17/17/17/17, reanalysis 50/50/50/26/50; 60m eval 18/17/17/11/17, reanalysis 50/50/50/15/50; 240m* eval 18/14/14/3/14, reanalysis 50/50/50/6/50; 480m eval 18/10/10/2/10, reanalysis 50/50/50/3/50
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 6; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 3; test mean n/a vs reference -12.0 bp; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1371 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- variants tried in family D-twap: 8

### E1-liquidity-recovery @ ev-79ea1d99704b - exploratory
After a displayed-depth shock, do slow refills precede larger moves in the depleted side's direction than fast refills? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 60m eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 240m eval 0/0/0/0/0, reanalysis 0/0/0/0/0; 480m eval 0/0/0/0/0, reanalysis 0/0/0/0/0
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- variants tried in family E-liquidity: 12

### F1-options-perp-disagreement @ ev-33998e4f9082 - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-2): 2026-09-23T00:00Z to 2026-09-25T15:41Z; 63 closed hours + 1 partial; 64 hours with eligible candidates; 64 selected (0 frozen earlier); 0 closed hours without a control; availability 17.6 min after the hour (median, range 11.7-28.0)
- selections: 64 accepted this run, 0 proposals superseded by stored winners, 0 hours pending processing (decision after the cutoff), 0 stored records withheld at this cutoff
- controls used: sha256 bf382bc34b19fed9; equal to the stored selections: True
- labelled controls = stored selections: 64 checked, 0 mismatches
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 64/63/63/63/42; 60m eval 0/0/0/0/0, reanalysis 64/63/63/40/42; 240m eval 0/0/0/0/0, reanalysis 64/60/60/14/39; 480m* eval 0/0/0/0/0, reanalysis 64/56/56/7/35
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 7; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 204 option records (0 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 19

### G1-alt-stress-propagation @ ev-44a97c2d5259 - exploratory
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 18/17/17/17/17, reanalysis 26/26/26/26/26; 60m* eval 18/17/17/11/17, reanalysis 26/26/26/15/26; 240m eval 18/14/14/3/14, reanalysis 26/26/26/6/26; 480m eval 18/10/10/2/10, reanalysis 26/26/26/3/26
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 15; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 11; test mean n/a vs reference -12.0 bp; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 2.8 days of stored bars; the design needs 14
- variants tried in family G-cross: 12

### H1-deleveraging-stress @ ev-e76cbdabf3f9 - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 18/17/17/17/17, reanalysis 50/50/50/26/50; 60m eval 18/17/17/11/17, reanalysis 50/50/50/15/50; 240m eval 18/14/14/3/14, reanalysis 50/50/50/6/50; 480m eval 18/10/10/2/10, reanalysis 50/50/50/3/50
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 3.6 days of collected OKX liquidation history; the p99 threshold needs 7
- variants tried in family H-deleveraging: 4

