# Proposed skill changes

Generated 2026-09-24T00:00Z. For human review; nothing here edits a skill file.
A change is proposed only for a design whose CURRENT evaluation version is **supported** under the lab-2.1 promotion rules (data quality, retained observations and dependence blocks, multiplicity-adjusted effect, out-of-sample baseline added value, comparability, stability) at a RECORDED checkpoint whose manifest re-verifies; the wording quotes that checkpoint, not later data.

**No change is proposed.** No design's current version is supported by a verified checkpoint.

| Design @ version | Status | Why no proposal |
|---|---|---|
| A1-flow-absorption @ ev-13f30d25ede6 | exploratory | no evaluation observations yet; 1.2 days of stored 1-minute bars; the event threshold needs 7 days of prior windows |
| B1-underwater-adds @ ev-36f3bab7e834 | exploratory | no evaluation observations yet; 14 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence) |
| C1-liquidation-cluster @ ev-448e00c8b90b | exploratory | no evaluation observations yet; 15 sampled snapshots; the design needs 1344 |
| D1-active-twap @ ev-bf8bdf308173 | exploratory | no evaluation observations yet; 129 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs |
| E1-liquidity-recovery @ ev-48bc92730cd7 | exploratory | no evaluation observations yet; streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector |
| F1-options-perp-disagreement @ ev-f1dbc341200d | exploratory | no evaluation observations yet; 52 option records (0 with a trailing z-score); the design needs 1344 |
| G1-alt-stress-propagation @ ev-77d34ac5d863 | exploratory | no evaluation observations yet; 1.2 days of stored bars; the design needs 14 |
| H1-deleveraging-stress @ ev-1b9297bc66cb | exploratory | no evaluation observations yet; 1.9 days of collected OKX liquidation history; the p99 threshold needs 7 |

Reanalysis and reconstruction results are hypotheses, never grounds for a rule.
