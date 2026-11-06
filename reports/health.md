# Operational health

Generated 2026-11-06T23:15:01Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule:** stale; last scheduled collector run 2026-11-06T20:23:52Z (171.1 min). Silences over 90 min in the last 72 h: 2026-11-03T22:34:32Z to 2026-11-04T02:38:43Z (244 min); 2026-11-04T02:38:43Z to 2026-11-04T17:53:52Z (915 min); 2026-11-04T17:53:52Z to 2026-11-04T23:33:57Z (340 min); 2026-11-04T23:33:57Z to 2026-11-05T03:40:32Z (247 min); 2026-11-05T03:40:32Z to 2026-11-05T11:35:50Z (475 min); 2026-11-05T11:35:50Z to 2026-11-05T18:56:14Z (440 min); 2026-11-05T18:56:14Z to 2026-11-06T00:04:49Z (309 min); 2026-11-06T00:04:49Z to 2026-11-06T06:02:47Z (358 min); 2026-11-06T06:02:47Z to 2026-11-06T14:03:04Z (480 min); 2026-11-06T14:03:04Z to 2026-11-06T20:23:52Z (381 min); 2026-11-06T20:23:52Z to ongoing (171 min).

**Service continuity:** healthy; last persisted critical success 2026-11-06T23:13:13Z (1.8 min); last automated activity 2026-11-06T23:13:13Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 4, recovery 95; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 19.5 min.

**Range decisions:** 11-05T16:00 failed: failed before forecasting; 11-05T20:00 failed: failed before forecasting; 11-06T00:00 failed: failed before forecasting; 11-06T04:00 failed: failed before forecasting; 11-06T08:00 failed: failed before forecasting; 11-06T12:00 failed: failed before forecasting; 11-06T16:00 published; 11-06T20:00 published.

**PS1 decisions:** 11-05T16:00 no-rebalance; 11-05T20:00 no-rebalance; 11-06T00:00 no-rebalance; 11-06T04:00 no-rebalance; 11-06T08:00 no-rebalance; 11-06T12:00 no-rebalance; 11-06T16:00 executed; 11-06T20:00 executed.

**PS1 report coverage:** 0.7667 as of 2026-11-06T20:22:51.318Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-07T00:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-06T18:30:10Z: success; last success 2026-11-06T18:29:58Z); range-monitor.yml heartbeat fresh (last run 2026-11-06T22:26:00Z: failure, found a problem: runs: decision 2026-11-06T12:00:00Z: run 42217778524 produced no attempt (refit failure); last success 2026-10-31T20:41:40Z); newest scheduled start of any workflow 2026-11-06T22:25:52Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-06T23:12:02Z. Arrivals only: whether each request was sent needs the provider's history.

Recovery service-watch: fresh; passed; last check completion 2026-11-06T23:12:09Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-06T23:13:05Z.