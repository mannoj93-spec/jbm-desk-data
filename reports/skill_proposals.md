# Proposed skill changes

Generated 2026-09-25T12:51Z. For human review; nothing here edits a skill file.
A change is proposed only for a design whose CURRENT evaluation version is **supported** under the lab-2.1+ promotion rules (data quality, retained observations and dependence blocks, multiplicity-adjusted effect, out-of-sample baseline added value, comparability, stability) at a RECORDED checkpoint whose manifest re-verifies; the wording quotes that checkpoint, not later data. Only the primary horizon, fixed in the design before any data, decides checkpoints, status and skill proposals; secondary horizons are descriptive and cannot override a failed primary or trigger a proposal on their own.

**No change is proposed.** No design's current version is supported by a verified checkpoint.

| Design @ version | Status | Why no proposal |
|---|---|---|
| A1-flow-absorption @ ev-c35cdb2bc9bc | exploratory | no evaluation observations yet; 2.7 days of stored 1-minute bars; the event threshold needs 7 days of prior windows |
| B1-underwater-adds @ ev-9cffe8818c14 | exploratory | no evaluation observations yet; 154 snapshot transitions for the fixed cohort; the design needs 1344 (about two weeks at 15-minute cadence) |
| C1-liquidation-cluster @ ev-1e8cf9f4e69a | exploratory | no evaluation observations yet; 156 sampled snapshots; the design needs 1344 |
| D1-active-twap @ ev-ffa18ae355ef | exploratory | no evaluation observations yet; 1290 twapHistory checks, 265 programs observed (2 BTC), 0 qualifying; the design needs 30 active BTC programs |
| E1-liquidity-recovery @ ev-79ea1d99704b | exploratory | no evaluation observations yet; streaming service not deployed or its data not mounted (STREAM_DATA_DIR); second-scale depth is not observable by the 15-minute collector |
| F1-options-perp-disagreement @ ev-48a0f80de862 | exploratory | no evaluation observations yet; 193 option records (0 with a trailing z-score); the design needs 1344 |
| G1-alt-stress-propagation @ ev-44a97c2d5259 | exploratory | no evaluation observations yet; 2.7 days of stored bars; the design needs 14 |
| H1-deleveraging-stress @ ev-e76cbdabf3f9 | exploratory | no evaluation observations yet; 3.5 days of collected OKX liquidation history; the p99 threshold needs 7 |

Reanalysis and reconstruction results are hypotheses, never grounds for a rule.
