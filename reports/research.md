# Research evidence (2026-09-23T20:25Z)

Lab lab-1.0-2026-09-23; code b352c8c6f65f; commit d155cbaf5e1675124cd95322a72cb921ff06f83d; cost model costs-1 (assumed fees - see VALIDATION.md). Descriptive intervals only; no result here is described as significant or profitable.

| Module | Design | Status | Prospective eval episodes | Primary diff (90%) | Data state |
|---|---|---|---|---|---|
| flow_absorption | A1-flow-absorption (60m) | exploratory | 0/100 | n/a | insufficient_data |
| account_behavior | B1-underwater-adds (240m) | exploratory | 0/100 | n/a | insufficient_data |
| liq_exposure | C1-liquidation-cluster (240m) | exploratory | 0/100 | n/a | insufficient_data |
| twap_lifecycle | D1-active-twap (240m) | exploratory | 0/100 | n/a | insufficient_data |
| liquidity_recovery | E1-liquidity-recovery (30m) | exploratory | 0/100 | n/a | unavailable |
| options_disagreement | F1-options-perp-disagreement (480m) | exploratory | 0/100 | n/a | insufficient_data |
| cross_asset | G1-alt-stress-propagation (60m) | exploratory | 0/100 | n/a | insufficient_data |
| deleveraging | H1-deleveraging-stress (30m) | exploratory | 0/100 | n/a | insufficient_data |

## Per design

### A1-flow-absorption - exploratory
Do weak-response heavy-flow windows differ from strong-response ones in subsequent flow-direction net return? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: no stored 1-minute bars yet (collector 2.7 stores them from deployment)
- reconstruction/exploratory: 6 test vs 93 reference independent episodes over 41 days; test mean -35.3 bp, reference mean -7.1 bp, diff 90% [-56.2 bp, -6.1 bp].
- contradictory evidence: 1 item(s), e.g. q95_weak0.5 / reconstruction / exploratory / 60m: the two chronological halves disagree in sign (+8.7 bp vs -7.1 bp)
- variants tested in family A-flow: 3

### B1-underwater-adds - exploratory
Do fixed-cohort BTC additions under drawdown differ from additions in profit in subsequent return in the added direction? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: 0 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence)
- variants tested in family B-accounts: 3

### C1-liquidation-cluster - exploratory
When sampled long liquidation exposure within 2% of mark is large, does BTC fall more than at scheduled times? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: 0 sampled snapshots; the design needs 1344
- variants tested in family C-liquidation: 3

### D1-active-twap - exploratory
After an active BTC TWAP of a fixed-cohort account is first observed, do returns in its direction exceed scheduled entries with the same direction mix? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: 0 twapHistory checks, 0 programs observed (0 BTC), 0 qualifying; the design needs 30 active BTC programs
- variants tested in family D-twap: 2

### E1-liquidity-recovery - exploratory
After a displayed-depth shock, do slow refills precede larger moves in the depleted side's direction than fast refills? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector
- variants tested in family E-liquidity: 3

### F1-options-perp-disagreement - exploratory
When 7-day risk reversal and perp funding disagree at extremes, does BTC follow the options side more than scheduled entries do? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: 37 option records (0 with a trailing z-score); the design needs 1344
- variants tested in family F-options: 3

### G1-alt-stress-propagation - exploratory
After an ETH/SOL 5-minute shock with BTC calm, does BTC follow the alt more than scheduled entries do? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: 0.0 days of stored bars; the design needs 14
- reconstruction/exploratory: 44 test vs 1437 reference independent episodes over 60 days; test mean -19.3 bp, reference mean -12.3 bp, diff 90% [-22.8 bp, +5.7 bp].
- contradictory evidence: 1 item(s), e.g. k4 / reconstruction / exploratory / 60m: the two chronological halves disagree in sign (+11.2 bp vs -7.1 bp)
- variants tested in family G-cross: 3

### H1-deleveraging-stress - exploratory
Do OKX liquidation bursts accompanied by insurance-fund loss or ADL rows continue further than plain bursts? Status reason: no evaluation episodes yet.
- prospective/exploratory: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective/evaluation: 0 test vs 0 reference independent episodes over 0 days; test mean n/a, reference mean n/a, diff 90% n/a.
- prospective data: 1.8 days of collected OKX liquidation history; the p99 threshold needs 7; no OKX insurance-fund rows stored yet (collector 2.7)
- variants tested in family H-deleveraging: 1

