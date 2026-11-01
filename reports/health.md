# Operational health

Generated 2026-11-01T16:07:49Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule:** healthy; last scheduled collector run 2026-11-01T16:06:11Z (1.6 min). Silences over 90 min in the last 72 h: 2026-10-29T14:24:32Z to 2026-10-29T19:50:07Z (326 min); 2026-10-29T19:50:07Z to 2026-10-29T23:38:04Z (228 min); 2026-10-29T23:38:04Z to 2026-10-30T03:04:04Z (206 min); 2026-10-30T03:04:04Z to 2026-10-30T09:49:24Z (405 min); 2026-10-30T09:49:24Z to 2026-10-30T16:21:17Z (392 min); 2026-10-30T16:21:17Z to 2026-10-30T20:50:19Z (269 min); 2026-10-30T20:50:19Z to 2026-10-31T00:09:43Z (199 min); 2026-10-31T00:09:43Z to 2026-10-31T05:49:57Z (340 min); 2026-10-31T05:49:57Z to 2026-10-31T11:18:26Z (328 min); 2026-10-31T11:18:26Z to 2026-10-31T16:08:42Z (290 min); 2026-10-31T16:08:42Z to 2026-10-31T20:01:14Z (233 min); 2026-10-31T20:01:14Z to 2026-10-31T23:18:04Z (197 min); 2026-10-31T23:18:04Z to 2026-11-01T02:18:20Z (180 min); 2026-11-01T02:18:20Z to 2026-11-01T09:19:30Z (421 min); 2026-11-01T09:19:30Z to 2026-11-01T16:06:11Z (407 min).

**Service continuity:** healthy; last persisted critical success 2026-11-01T16:06:11Z (1.6 min); last automated activity 2026-11-01T16:06:11Z (critical success, native-schedule). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 6, recovery 91; 92 of 95 slot intervals hold an automated critical success (92 hold any automated activity); longest gap between successes 66.4 min.

**Range decisions:** 10-31T08:00 published; 10-31T12:00 published; 10-31T16:00 published; 10-31T20:00 published; 11-01T00:00 failed: failed before forecasting; 11-01T04:00 failed: failed before forecasting; 11-01T08:00 failed: failed before forecasting; 11-01T12:00 failed: failed before forecasting.

**PS1 decisions:** 10-31T12:00 executed; 10-31T16:00 executed; 10-31T20:00 executed; 11-01T00:00 no-rebalance; 11-01T04:00 no-rebalance; 11-01T08:00 no-rebalance; 11-01T12:00 no-rebalance; 11-01T16:00 pending.

**PS1 report coverage:** 0.8933 as of 2026-11-01T15:32:57.916Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-11-01T17:15:00Z); 24h stale; 4h stale; 72h stale.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-01T09:20:47Z: success; last success 2026-11-01T09:20:39Z); range-monitor.yml heartbeat fresh (last run 2026-11-01T09:12:25Z: failure, found a problem: actions: the latest scheduled range.yml run 41274842438 (2026-11-01T04:54:09Z) concluded failure (recorded; the stream has not recovered since); last success 2026-10-31T20:41:40Z); newest scheduled start of any workflow 2026-11-01T16:05:21Z.

**External timer (primary trigger):** gaps; 93 of 97 opportunities on time in 24 h, 0 delayed, absent 2026-11-01T08:12:00Z, 2026-11-01T08:27:00Z, 2026-11-01T08:42:00Z, 2026-11-01T08:57:00Z; last arrival 2026-11-01T15:57:02Z. Arrivals only: whether each request was sent needs the provider's history.

Recovery service-watch: fresh; passed; last check completion 2026-11-01T15:57:11Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-01T15:57:57Z.