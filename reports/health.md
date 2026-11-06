# Operational health

Generated 2026-11-06T17:59:58Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule:** stale; last scheduled collector run 2026-11-06T14:03:04Z (236.9 min). Silences over 90 min in the last 72 h: 2026-11-03T17:40:14Z to 2026-11-03T22:34:32Z (294 min); 2026-11-03T22:34:32Z to 2026-11-04T02:38:43Z (244 min); 2026-11-04T02:38:43Z to 2026-11-04T17:53:52Z (915 min); 2026-11-04T17:53:52Z to 2026-11-04T23:33:57Z (340 min); 2026-11-04T23:33:57Z to 2026-11-05T03:40:32Z (247 min); 2026-11-05T03:40:32Z to 2026-11-05T11:35:50Z (475 min); 2026-11-05T11:35:50Z to 2026-11-05T18:56:14Z (440 min); 2026-11-05T18:56:14Z to 2026-11-06T00:04:49Z (309 min); 2026-11-06T00:04:49Z to 2026-11-06T06:02:47Z (358 min); 2026-11-06T06:02:47Z to 2026-11-06T14:03:04Z (480 min); 2026-11-06T14:03:04Z to ongoing (237 min).

**Service continuity:** healthy; last persisted critical success 2026-11-06T17:58:19Z (1.6 min); last automated activity 2026-11-06T17:58:19Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 4, recovery 95; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 17.4 min.

**Range decisions:** 11-05T12:00 failed: failed before forecasting; 11-05T16:00 failed: failed before forecasting; 11-05T20:00 failed: failed before forecasting; 11-06T00:00 failed: failed before forecasting; 11-06T04:00 failed: failed before forecasting; 11-06T08:00 failed: failed before forecasting; 11-06T12:00 failed: failed before forecasting; 11-06T16:00 published.

**PS1 decisions:** 11-05T12:00 no-rebalance; 11-05T16:00 no-rebalance; 11-05T20:00 no-rebalance; 11-06T00:00 no-rebalance; 11-06T04:00 no-rebalance; 11-06T08:00 no-rebalance; 11-06T12:00 no-rebalance; 11-06T16:00 executed.

**PS1 report coverage:** 0.7656 as of 2026-11-06T16:24:10.522Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-06T20:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-06T11:32:39Z: success; last success 2026-11-06T11:32:28Z); range-monitor.yml heartbeat fresh (last run 2026-11-06T16:57:23Z: failure, found a problem: actions: the latest scheduled range.yml run 42213531457 (2026-11-06T11:53:19Z) concluded failure (recorded; the stream has not recovered since); last success 2026-10-31T20:41:40Z); newest scheduled start of any workflow 2026-11-06T16:57:15Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-06T17:57:02Z. Arrivals only: whether each request was sent needs the provider's history.

Recovery service-watch: fresh; passed; last check completion 2026-11-06T17:57:10Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-06T17:58:18Z.