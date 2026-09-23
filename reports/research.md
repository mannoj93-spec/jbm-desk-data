# Research evidence

Generated 2026-09-23T22:19Z (input cutoff 2026-09-23T22:17Z); lab-2.0-2026-09-23; code 4b73a8f63a8f; commit 87268f312b8f17f6e10a127157069af69a64920d; cost model costs-1 (assumed fees). Refreshed by the Research lab workflow every 6 hours; anything older is stale.

Descriptive intervals only. Decisions are as-of replays by a 6-hourly lab, not live executions.

| Module | Design @ version | Status | Evaluation retained / blocks (primary h) | Adjusted diff | Baseline residual diff (adj.) | Data |
|---|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption @ ev-834a7e553c0d | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| account_behavior | B1-underwater-adds @ ev-518c85069dd5 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liq_exposure | C1-liquidation-cluster @ ev-533da6a65739 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| twap_lifecycle | D1-active-twap @ ev-e4e1d1a56b1b | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| liquidity_recovery | E1-liquidity-recovery @ ev-fa793416754a | exploratory | 0/100 ; 0 | n/a | n/a | unavailable |
| options_disagreement | F1-options-perp-disagreement @ ev-7c3b32a14a0d | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| cross_asset | G1-alt-stress-propagation @ ev-1e11c6123efd | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |
| deleveraging | H1-deleveraging-stress @ ev-c0aa1ade6107 | exploratory | 0/100 ; 0 | n/a | n/a | insufficient_data |

## Per design

### A1-flow-absorption @ ev-834a7e553c0d - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1.1 days of stored 1-minute bars; the event threshold needs 7 days of prior windows
- reconstruction/exploratory: test firings 13, episodes 7, scorable 7, retained 6 in 6 blocks; reference retained 93; test mean -35.3 bp vs reference -7.1 bp; 90% [-56.9 bp, -5.7 bp].
- contradictory evidence (1): q95_weak0.5 / reconstruction / exploratory / 60m: chronological halves disagree (+11.8 bp vs -10.8 bp)
- variants tried in family A-flow: 6

### B1-underwater-adds @ ev-518c85069dd5 - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 7 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tried in family B-accounts: 6

### C1-liquidation-cluster @ ev-533da6a65739 - exploratory
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 8 sampled snapshots; the design needs 1344
- variants tried in family C-liquidation: 6

### D1-active-twap @ ev-e4e1d1a56b1b - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 70 twapHistory checks, 200 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs
- variants tried in family D-twap: 4

### E1-liquidity-recovery @ ev-fa793416754a - exploratory
After a displayed-depth shock, do slow refills precede larger moves in the depleted side's direction than fast refills? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- variants tried in family E-liquidity: 6

### F1-options-perp-disagreement @ ev-7c3b32a14a0d - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 1; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 45 option records (0 with a trailing z-score); the design needs 1344
- variants tried in family F-options: 7

### G1-alt-stress-propagation @ ev-1e11c6123efd - exploratory
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 1; test mean n/a vs reference -12.0 bp; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1.1 days of stored bars; the design needs 14
- reconstruction/exploratory: test firings 51, episodes 48, scorable 48, retained 44 in 33 blocks; reference retained 1437; test mean -19.3 bp vs reference -12.3 bp; 90% [-23.4 bp, +5.7 bp].
- contradictory evidence (1): k4 / reconstruction / exploratory / 60m: chronological halves disagree (+11.3 bp vs -7.1 bp)
- variants tried in family G-cross: 6

### H1-deleveraging-stress @ ev-c0aa1ade6107 - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status: no evaluation observations yet.
- prospective/reanalysis: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- prospective/evaluation: test firings 0, episodes 0, scorable 0, retained 0 in 0 blocks; reference retained 0; test mean n/a vs reference n/a; 90% n/a.
- frozen decisions: {'frozen_used': 0, 'revised_since_frozen': 0, 'not_reproduced': 0, 'late_replay': 0, 'new': 0}
- prospective data: 1.9 days of collected OKX liquidation history; the p99 threshold needs 7
- variants tried in family H-deleveraging: 2

