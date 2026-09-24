# Research evidence

Generated 2026-09-24T00:50Z (input cutoff 2026-09-24T00:40Z); lab-2.1-2026-09-23; code 9c248ae1aece; commit 5cebff29e7412100732a6b3289fcb74520e944a5; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data |
|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-13f30d25ede6 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| account_behavior | B1-underwater-adds @ ev-36f3bab7e834 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liq_exposure | C1-liquidation-cluster @ ev-448e00c8b90b | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| twap_lifecycle | D1-active-twap @ ev-bf8bdf308173 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liquidity_recovery | E1-liquidity-recovery @ ev-48bc92730cd7 | exploratory | 0/100 ; 0 | n/a | n/a | unavailable |
| options_disagreement | F1-options-perp-disagreement @ ev-f1dbc341200d | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| cross_asset | G1-alt-stress-propagation @ ev-77d34ac5d863 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| deleveraging | H1-deleveraging-stress @ ev-1b9297bc66cb | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |

## Per design

### A1-flow-absorption @ ev-13f30d25ede6 - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1.2 days of stored 1-minute bars; the event threshold needs 7 days of prior windows
- reconstruction/exploratory: test firings 12, episodes 7, scorable 7, retained 6 in 6 blocks; reference retained 93; test mean -35.3 bp vs reference -7.8 bp; 90% [-56.2 bp, -4.8 bp].
- contradictory evidence (1): q95_weak0.5 / reconstruction / exploratory / 60m: chronological halves disagree (+8.2 bp vs -9.6 bp)
- variants tried in family A-flow: 9

### B1-underwater-adds @ ev-36f3bab7e834 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 16 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 9

### C1-liquidation-cluster @ ev-448e00c8b90b - exploratory
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 17 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 9

### D1-active-twap @ ev-bf8bdf308173 - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 1; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 147 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- variants tried in family D-twap: 6

### E1-liquidity-recovery @ ev-48bc92730cd7 - exploratory
After a displayed-depth shock, do slow refills precede larger moves in the depleted side's direction than fast refills? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- variants tried in family E-liquidity: 9

### F1-options-perp-disagreement @ ev-f1dbc341200d - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 2; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 54 option records (0 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 11

### G1-alt-stress-propagation @ ev-77d34ac5d863 - exploratory
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 2; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1.2 days of stored bars; the design needs 14
- reconstruction/exploratory: test firings 52, episodes 49, scorable 49, retained 45 in 34 blocks; reference retained 1437; test mean -18.2 bp vs reference -12.4 bp; 90% [-20.4 bp, +6.9 bp].
- contradictory evidence (2): k2.5 / reconstruction / exploratory / 60m: chronological halves disagree (-7.9 bp vs +0.1 bp)
- variants tried in family G-cross: 9

### H1-deleveraging-stress @ ev-1b9297bc66cb - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- checkpoint 1 pending: 0/100 retained test observations known
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1.9 days of collected OKX liquidation history; the p99 threshold needs 7
- variants tried in family H-deleveraging: 3

