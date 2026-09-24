# Research evidence

Generated 2026-09-24T22:12Z (input cutoff 2026-09-24T21:54Z); lab-2.2-2026-09-24; code 326991326be8; commit 1c9b920d51b67ae447e69b1038f897304e87212a; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data |
|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-c35cdb2bc9bc | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| account_behavior | B1-underwater-adds @ ev-9cffe8818c14 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liq_exposure | C1-liquidation-cluster @ ev-1e8cf9f4e69a | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| twap_lifecycle | D1-active-twap @ ev-ffa18ae355ef | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liquidity_recovery | E1-liquidity-recovery @ ev-79ea1d99704b | exploratory | 0/100 ; 0 | n/a | n/a | unavailable |
| options_disagreement | F1-options-perp-disagreement @ ev-48a0f80de862 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| cross_asset | G1-alt-stress-propagation @ ev-44a97c2d5259 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| deleveraging | H1-deleveraging-stress @ ev-e76cbdabf3f9 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |

## Per design

### A1-flow-absorption @ ev-c35cdb2bc9bc - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 26/26/26/26/26; 60m* eval 0/0/0/0/0, reanalysis 26/25/25/15/25; 240m eval 0/0/0/0/0, reanalysis 26/22/22/5/22; 480m eval 0/0/0/0/0, reanalysis 26/18/18/3/18
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 2.1 days of stored 1-minute bars; the event threshold needs 7 days of prior windows
- variants tried in family A-flow: 12

### B1-underwater-adds @ ev-9cffe8818c14 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-1): 2026-09-23T20:00Z to 2026-09-24T22:12Z; 26 closed hours + 1 partial; 26 hours with eligible candidates; 26 selected (0 frozen earlier); 0 closed hours without a control; availability 17.9 min after the hour (median, range 0.1-43.5)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 26/26/26/26/26; 60m eval 0/0/0/0/0, reanalysis 26/25/25/15/25; 240m* eval 0/0/0/0/0, reanalysis 26/22/22/5/22; 480m eval 0/0/0/0/0, reanalysis 26/18/18/2/18
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 99 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 12

### C1-liquidation-cluster @ ev-1e8cf9f4e69a - exploratory
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage (hourly-first-available-1): 2026-09-23T20:00Z to 2026-09-24T22:12Z; 26 closed hours + 1 partial; 26 hours with eligible candidates; 26 selected (0 frozen earlier); 0 closed hours without a control; availability 17.9 min after the hour (median, range 0.1-30.5)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 26/26/26/26/26; 60m eval 0/0/0/0/0, reanalysis 26/25/25/15/25; 240m* eval 0/0/0/0/0, reanalysis 26/22/22/5/22; 480m eval 0/0/0/0/0, reanalysis 26/18/18/2/18
- decision timing: 1 frozen events; lab persisted them 1242.0 min (median, max 1242.0) after the assumed decision time (inputs + 60 s); as-of replay, not live execution
- prospective/reanalysis: test firings 1, episodes 1, scorable 1, retained 1 in 1 blocks; reference retained 5; test mean -4.0 bp vs reference -5.9 bp; 90% n/a.
- prospective/evaluation: test firings 1, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 1}
- prospective data: 100 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 12

### D1-active-twap @ ev-ffa18ae355ef - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 240 min (decides status and proposals); secondary 30, 60, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 50/50/50/26/50; 60m eval 0/0/0/0/0, reanalysis 50/49/49/15/49; 240m* eval 0/0/0/0/0, reanalysis 50/46/46/5/46; 480m eval 0/0/0/0/0, reanalysis 50/42/42/3/42
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 5; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 830 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
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

### F1-options-perp-disagreement @ ev-48a0f80de862 - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 480 min (decides status and proposals); secondary 30, 60, 240 min (descriptive only)
- comparison coverage (hourly-first-available-1): 2026-09-23T00:00Z to 2026-09-24T22:12Z; 46 closed hours + 1 partial; 46 hours with eligible candidates; 46 selected (0 frozen earlier); 0 closed hours without a control; availability 17.9 min after the hour (median, range 11.7-28.0)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 46/46/46/46/25; 60m eval 0/0/0/0/0, reanalysis 46/45/45/29/24; 240m eval 0/0/0/0/0, reanalysis 46/42/42/10/21; 480m* eval 0/0/0/0/0, reanalysis 46/38/38/5/17
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 5; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 137 option records (0 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 15

### G1-alt-stress-propagation @ ev-44a97c2d5259 - exploratory
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 60 min (decides status and proposals); secondary 30, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m eval 0/0/0/0/0, reanalysis 26/26/26/26/26; 60m* eval 0/0/0/0/0, reanalysis 26/25/25/15/25; 240m eval 0/0/0/0/0, reanalysis 26/22/22/5/22; 480m eval 0/0/0/0/0, reanalysis 26/18/18/3/18
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 15; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 2.1 days of stored bars; the design needs 14
- variants tried in family G-cross: 12

### H1-deleveraging-stress @ ev-e76cbdabf3f9 - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- horizons: primary 30 min (decides status and proposals); secondary 60, 240, 480 min (descriptive only)
- comparison coverage: hourly controls at each whole-hour bar close whose bar is stored (bar-based; not affected by the collection-time policy)
- controls selected/mature/scorable/retained/baseline-usable (* primary): 30m* eval 0/0/0/0/0, reanalysis 50/50/50/26/50; 60m eval 0/0/0/0/0, reanalysis 50/49/49/15/49; 240m eval 0/0/0/0/0, reanalysis 50/46/46/5/46; 480m eval 0/0/0/0/0, reanalysis 50/42/42/3/42
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 2.8 days of collected OKX liquidation history; the p99 threshold needs 7
- variants tried in family H-deleveraging: 4

