# Proposed skill changes (2026-09-23T20:25Z)

Generated for human review. Nothing here has been applied to any skill file; the lab never edits skill files. A change is proposed only for a design whose status is **supported** (evaluation episodes at or after registration, minimum count met, intervals excluding zero in the hypothesised direction, both chronological halves agreeing).

**No change is proposed.** No design has reached supported status.

| Design | Status | Why no proposal |
|---|---|---|
| A1-flow-absorption | exploratory | no evaluation episodes yet; no stored 1-minute bars yet (collector 2.7 stores them from deployment) |
| B1-underwater-adds | exploratory | no evaluation episodes yet; 0 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence) |
| C1-liquidation-cluster | exploratory | no evaluation episodes yet; 0 sampled snapshots; the design needs 1344 |
| D1-active-twap | exploratory | no evaluation episodes yet; 0 twapHistory checks, 0 programs observed (0 BTC), 0 qualifying; the design needs 30 active BTC programs |
| E1-liquidity-recovery | exploratory | no evaluation episodes yet; streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector |
| F1-options-perp-disagreement | exploratory | no evaluation episodes yet; 37 option records (0 with a trailing z-score); the design needs 1344 |
| G1-alt-stress-propagation | exploratory | no evaluation episodes yet; 0.0 days of stored bars; the design needs 14 |
| H1-deleveraging-stress | exploratory | no evaluation episodes yet; 1.8 days of collected OKX liquidation history; the p99 threshold needs 7 |

Exploratory reconstructions and pre-registration episodes may be read as hypotheses to watch, never as grounds for a rule. Evaluate a revised skill with `python -m lab.skill_eval` before and after any change a human decides to make.
