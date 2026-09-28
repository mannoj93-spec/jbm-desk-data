# Validation record — monitor fix, revision 2.17.1

Validated 2026-09-28 ~00:30Z (Python 3.11, container). Earlier blocks below are kept as recorded.

| Check (2.17.1) | Result |
|---|---|
| Production evidence (verified) | Range stream monitor runs #1–#8 (Sep 26 17:56Z – Sep 27 21:56Z) all failed; run #8 (36353516254) annotation: "actions: range.yml run 36241307098 (2026-09-26T12:14:41Z) concluded failure with no record in the repository". Range forecasts: 8 scheduled runs Sep 26 16:00Z – Sep 27 20:00Z, all `published` in `state/range_runs.jsonl`, all confirmed eligible; no integrity failures |
| Reproduction | Monitor on the Sep 27 21:56Z repository with that run in the Actions list: the same single error. Without the Actions list: no problems (the repository checks were healthy) |
| Same on 2.17.1 | CI-like sparse checkout (with `desk/deployments.jsonl`): no problems at 21:56Z; `acknowledged_runs` = [36241307098]; a new unrecorded failed run still alarms; a due decision inside the lookback whose failure is in the deployment log is reported with that cause |
| Regression suite | 536 passed (desk 204), 0 skipped; fixtures 25; evaluation ids identical |

