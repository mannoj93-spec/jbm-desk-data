# Proposed skill changes

Generated 2026-09-25T18:53Z (UTC). For human review; nothing here edits a skill file. A proposal is a conditional base rate for a person to consider, not evidence of a trading edge.

A change is proposed only for a design whose CURRENT evaluation version is **supported** under the lab-2.1+ promotion rules (data quality, retained observations and dependence blocks, multiplicity-adjusted effect, out-of-sample baseline added value, comparability, stability) at a RECORDED checkpoint whose manifest re-verifies; the wording quotes that checkpoint, not later data. Only the primary horizon, fixed in the design before any data, decides checkpoints, status and skill proposals; secondary horizons are descriptive and cannot override a failed primary or trigger a proposal on their own.

## Result

**No change is proposed.** No design's current version is supported by a verified checkpoint.

## Why each design has no proposal

| Design @ version | Status | Why no proposal |
|---|---|---|
| A1-flow-absorption @ ev-c368833b5ae6 | exploratory | no evaluation observations yet; 3.0 days of stored 1-minute bars; the event threshold needs 7 days of prior windows |
| B1-underwater-adds @ ev-125c86066f05 | exploratory | no evaluation observations yet; 178 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence) |
| C1-liquidation-cluster @ ev-eb20553bce1c | exploratory | no evaluation observations yet; 180 sampled snapshots; the design needs 1344 |
| D1-active-twap @ ev-2b023a90293f | exploratory | no evaluation observations yet; 1486 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs |
| E1-liquidity-recovery @ ev-6f279983100b | exploratory | no evaluation observations yet; streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector |
| F1-options-perp-disagreement @ ev-1c53cfe81c9f | exploratory | no evaluation observations yet; 217 option records (0 with a trailing z-score); the design needs 1344 |
| G1-alt-stress-propagation @ ev-5cbc55c34b6d | exploratory | no evaluation observations yet; 3.0 days of stored bars; the design needs 14 |
| H1-deleveraging-stress @ ev-02fcecefd1bf | exploratory | no evaluation observations yet; 3.7 days of collected OKX liquidation history; the p99 threshold needs 7 |

Reanalysis and reconstruction results are hypotheses, never grounds for a rule.
