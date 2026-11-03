# Operational health

Generated 2026-11-03T22:59:59Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule:** healthy; last scheduled collector run 2026-11-03T22:34:32Z (25.5 min). Silences over 90 min in the last 72 h: 2026-10-31T20:01:14Z to 2026-10-31T23:18:04Z (197 min); 2026-10-31T23:18:04Z to 2026-11-01T02:18:20Z (180 min); 2026-11-01T02:18:20Z to 2026-11-01T09:19:30Z (421 min); 2026-11-01T09:19:30Z to 2026-11-01T16:06:11Z (407 min); 2026-11-01T16:06:11Z to 2026-11-01T20:27:04Z (261 min); 2026-11-01T20:27:04Z to 2026-11-01T23:49:40Z (203 min); 2026-11-01T23:49:40Z to 2026-11-02T02:48:02Z (178 min); 2026-11-02T02:48:02Z to 2026-11-02T10:03:19Z (435 min); 2026-11-02T10:03:19Z to 2026-11-02T20:09:20Z (606 min); 2026-11-02T20:09:20Z to 2026-11-03T02:22:57Z (374 min); 2026-11-03T02:22:57Z to 2026-11-03T09:56:19Z (453 min); 2026-11-03T09:56:19Z to 2026-11-03T17:40:14Z (464 min); 2026-11-03T17:40:14Z to 2026-11-03T22:34:32Z (294 min).

**Service continuity:** healthy; last persisted critical success 2026-11-03T22:58:14Z (1.8 min); last automated activity 2026-11-03T22:58:14Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 4, recovery 93; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 20.3 min.

**Range decisions:** 11-02T16:00 failed: failed before forecasting; 11-02T20:00 failed: failed before forecasting; 11-03T00:00 failed: failed before forecasting; 11-03T04:00 failed: failed before forecasting; 11-03T08:00 failed: failed before forecasting; 11-03T12:00 failed: failed before forecasting; 11-03T16:00 failed: failed before forecasting; 11-03T20:00 failed: failed before forecasting.

**PS1 decisions:** 11-02T16:00 no-rebalance; 11-02T20:00 no-rebalance; 11-03T00:00 no-rebalance; 11-03T04:00 no-rebalance; 11-03T08:00 no-rebalance; 11-03T12:00 no-rebalance; 11-03T16:00 no-rebalance; 11-03T20:00 no-rebalance.

**PS1 report coverage:** 0.8281 as of 2026-11-03T20:40:43.342Z; due since and not covered: 11-03T20:00 no-rebalance.

**Range availability:** status within expiry (expires 2026-11-04T01:15:00Z); 24h stale; 4h stale; 72h stale.

**Scoring backlog:** none.

**Native scheduled monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-11-03T21:00:14Z: success; last success 2026-11-03T20:59:52Z); range-monitor.yml heartbeat fresh (last run 2026-11-03T20:18:24Z: failure, found a problem: actions: the latest scheduled range.yml run 41701186104 (2026-11-03T19:13:05Z) concluded failure (recorded; the stream has not recovered since); last success 2026-10-31T20:41:40Z); newest scheduled start of any workflow 2026-11-03T22:33:31Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-03T22:57:01Z. Arrivals only: whether each request was sent needs the provider's history.

Recovery service-watch: fresh; passed; last check completion 2026-11-03T22:57:08Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-03T22:57:58Z.