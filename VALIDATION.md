# Validation record — desk production fixes, revision 2.17

Validated 2026-09-26 (~13:30–14:10Z) with Python 3.11 and 3.12.3 (container). Earlier blocks below are kept as recorded.

| Check (2.17) | Result |
|---|---|
| Assessed snapshot / base | Assessment of 12.1 / 2.16, overnight snapshot `03ab599`; built on `365ff99` (main moved only by data commits since the 2.16 merge `3ea238b`) |
| Production evidence (verified) | Run 36229141684 (schedule, code `03274ce`, a descendant of `3ea238b`): 08:00Z batch frozen 08:15:19.365Z, confirmed 08:15:21.137Z, window 08:25Z, eligible. Run 36241307098 (schedule, code `79ee0e7`): preflight failed on `TestLiveRecords.test_read_and_replay`, refit/forecast/confirm skipped, only reports committed (`c09c861`); no 12:00Z forecast. Both appended to `desk/deployments.jsonl` |
| Reproductions on 2.16 | 04:30Z and 03:50Z reads return the 08:00Z batch; 00:04Z/01:00Z window accepted; `contract: []` TypeError; old `verify` on 3.12.3: "OUT OF TOLERANCE" at `.rows_file.sha256_uncompressed`, summary max 8.2e-14, exit 0 |
| Same on 2.17 | Reads at 03:50, 04:13:19.581, 04:13:20, 08:05, 08:15:21, 08:15:22, 09:15, 12:25Z give the record available at that instant; strict checks and eligibility as in CHANGELOG 2.17; `verify` PASS, exit 0; injected failures exit 1/2 |
| Regression suite | 535 passed (332 + desk 203), 0 skipped; fixtures 25 |
| Evaluation versions | Identical for all eight designs (`lab/versioning.py`, `365ff99` vs branch) |
| Registered forecasts | All six production RC1D records validate under the 2.17 strict checks and replay; frozen bytes unchanged |
| O21 | Replay zero differences; `verify` 275,016 row values + 218 summary values within 1e-9 (3.11: 0.0; 3.12.3: 1.0e-12), 0 structural, 0 categorical |
| Checksums | `SHA256SUMS` regenerated from its list plus the new code, tests, workflows and fixture |
| Not observed | Any 2.17 scheduled run, the hourly scorer or the monitor running on GitHub, any production score |

