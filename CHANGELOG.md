# Monitor fix, revision 2.17.1 (crypto-desk 12.2, package unchanged) — 2026-09-28

All eight scheduled runs of the range monitor (Sep 26 17:56Z – Sep 27 21:56Z) failed on one line: "actions: range.yml
run 36241307098 ... concluded failure with no record in the repository". That run (the 12:00Z preflight failure)
predates the run log; its verified cause is in `desk/deployments.jsonl`, which the monitor did not read, so it would
have alarmed on every run until the run left GitHub's 20-run list. The range stream itself was healthy: eight
scheduled runs published and were confirmed eligible (Sep 26 16:00Z – Sep 27 20:00Z); hourly scoring ran.

| Change | Tests |
|---|---|
| `desk/range_monitor.py` (monitor-12.2.1): runs recorded in the deployment log are acknowledged in the Actions check (listed under `acknowledged_runs`); a new unrecorded failure still alarms; a due decision whose failure is in the deployment log is reported with that cause instead of "no record". `range-monitor.yml` checks out `desk/deployments.jsonl` | `test_ops.TestMonitor.test_failure_recorded_in_the_deployment_log_is_acknowledged` |

No other module changed; shared skill modules are identical to package 12.2. Evaluation ids unchanged.

