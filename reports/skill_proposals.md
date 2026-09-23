# Proposed skill changes

Generated 2026-09-23T22:19Z. For human review; nothing here edits a skill file.
A change is proposed only for a design whose CURRENT evaluation version is **supported** under the lab-2.0 promotion rules (data quality, retained observations and dependence blocks, multiplicity-adjusted effect, out-of-sample baseline added value, comparability, stability, at a scheduled look).

**No change is proposed.** No design's current version is supported.

| Design @ version | Status | Why no proposal |
|---|---|---|
| A1-flow-absorption @ ev-834a7e553c0d | exploratory | no evaluation observations yet; 1.1 days of stored 1-minute bars; the event threshold needs 7 days of prior windows |
| B1-underwater-adds @ ev-518c85069dd5 | exploratory | no evaluation observations yet; 7 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence) |
| C1-liquidation-cluster @ ev-533da6a65739 | exploratory | no evaluation observations yet; 8 sampled snapshots; the design needs 1344 |
| D1-active-twap @ ev-e4e1d1a56b1b | exploratory | no evaluation observations yet; 70 twapHistory checks, 200 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs |
| E1-liquidity-recovery @ ev-fa793416754a | exploratory | no evaluation observations yet; streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector |
| F1-options-perp-disagreement @ ev-7c3b32a14a0d | exploratory | no evaluation observations yet; 45 option records (0 with a trailing z-score); the design needs 1344 |
| G1-alt-stress-propagation @ ev-1e11c6123efd | exploratory | no evaluation observations yet; 1.1 days of stored bars; the design needs 14 |
| H1-deleveraging-stress @ ev-c0aa1ade6107 | exploratory | no evaluation observations yet; 1.9 days of collected OKX liquidation history; the p99 threshold needs 7 |

Reanalysis and reconstruction results are hypotheses, never grounds for a rule.
