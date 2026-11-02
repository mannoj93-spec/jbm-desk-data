# Operational health

Generated 2026-11-02T08:15:17Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule:** stale; last scheduled collector run 2026-11-02T02:48:02Z (327.3 min). Silences over 90 min in the last 72 h: 2026-10-30T03:04:04Z to 2026-10-30T09:49:24Z (405 min); 2026-10-30T09:49:24Z to 2026-10-30T16:21:17Z (392 min); 2026-10-30T16:21:17Z to 2026-10-30T20:50:19Z (269 min); 2026-10-30T20:50:19Z to 2026-10-31T00:09:43Z (199 min); 2026-10-31T00:09:43Z to 2026-10-31T05:49:57Z (340 min); 2026-10-31T05:49:57Z to 2026-10-31T11:18:26Z (328 min); 2026-10-31T11:18:26Z to 2026-10-31T16:08:42Z (290 min); 2026-10-31T16:08:42Z to 2026-10-31T20:01:14Z (233 min); 2026-10-31T20:01:14Z to 2026-10-31T23:18:04Z (197 min); 2026-10-31T23:18:04Z to 2026-11-01T02:18:20Z (180 min); 2026-11-01T02:18:20Z to 2026-11-01T09:19:30Z (421 min); 2026-11-01T09:19:30Z to 2026-11-01T16:06:11Z (407 min); 2026-11-01T16:06:11Z to 2026-11-01T20:27:04Z (261 min); 2026-11-01T20:27:04Z to 2026-11-01T23:49:40Z (203 min); 2026-11-01T23:49:40Z to 2026-11-02T02:48:02Z (178 min); 2026-11-02T02:48:02Z to ongoing (327 min).

**Service continuity:** healthy; last persisted critical success 2026-11-02T08:13:24Z (1.9 min); last automated activity 2026-11-02T08:13:24Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 5, recovery 91; 92 of 95 slot intervals hold an automated critical success (92 hold any automated activity); longest gap between successes 64.2 min.

**Range decisions:** 11-01T00:00 failed: failed before forecasting; 11-01T04:00 failed: failed before forecasting; 11-01T08:00 failed: failed before forecasting; 11-01T12:00 failed: failed before forecasting; 11-01T16:00 failed: failed before forecasting; 11-01T20:00 failed: failed before forecasting; 11-02T00:00 failed: failed before forecasting; 11-02T04:00 failed: failed before forecasting.

**PS1 decisions:** 11-01T04:00 no-rebalance; 11-01T08:00 no-rebalance; 11-01T12:00 no-rebalance; 11-01T16:00 no-rebalance; 11-01T20:00 no-rebalance; 11-02T00:00 no-rebalance; 11-02T04:00 no-rebalance; 11-02T08:00 pending.

**PS1 report coverage:** 0.8736 as of 2026-11-02T06:56:27.517Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-02T09:15:00Z); 24h stale; 4h stale; 72h stale.

**Scoring backlog:** none.

**Native scheduled monitors:** fresh (GitHub Actions API, scheduled runs); watchdog.yml heartbeat fresh (last run 2026-11-02T06:54:37Z: success; last success 2026-11-02T06:54:27Z); range-monitor.yml heartbeat fresh (last run 2026-11-02T01:03:45Z: failure, found a problem: actions: the latest scheduled range.yml run 41346185976 (2026-11-01T20:18:38Z) concluded failure (recorded; the stream has not recovered since); last success 2026-10-31T20:41:40Z); newest scheduled start of any workflow 2026-11-02T06:54:55Z.

**External timer (primary trigger):** gaps; 92 of 96 opportunities on time in 24 h, 0 delayed, absent 2026-11-01T08:12:00Z, 2026-11-01T08:27:00Z, 2026-11-01T08:42:00Z, 2026-11-01T08:57:00Z; last arrival 2026-11-02T08:12:02Z. Arrivals only: whether each request was sent needs the provider's history.

Recovery service-watch: fresh; passed; last check completion 2026-11-02T08:12:22Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-02T08:13:06Z.