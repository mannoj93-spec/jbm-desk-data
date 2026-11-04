# Operational health

Generated 2026-11-04T22:29:49Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule:** stale; last scheduled collector run 2026-11-04T17:53:52Z (275.9 min). Silences over 90 min in the last 72 h: 2026-11-01T20:27:04Z to 2026-11-01T23:49:40Z (203 min); 2026-11-01T23:49:40Z to 2026-11-02T02:48:02Z (178 min); 2026-11-02T02:48:02Z to 2026-11-02T10:03:19Z (435 min); 2026-11-02T10:03:19Z to 2026-11-02T20:09:20Z (606 min); 2026-11-02T20:09:20Z to 2026-11-03T02:22:57Z (374 min); 2026-11-03T02:22:57Z to 2026-11-03T09:56:19Z (453 min); 2026-11-03T09:56:19Z to 2026-11-03T17:40:14Z (464 min); 2026-11-03T17:40:14Z to 2026-11-03T22:34:32Z (294 min); 2026-11-03T22:34:32Z to 2026-11-04T02:38:43Z (244 min); 2026-11-04T02:38:43Z to 2026-11-04T17:53:52Z (915 min); 2026-11-04T17:53:52Z to ongoing (276 min).

**Service continuity:** healthy; last persisted critical success 2026-11-04T22:28:17Z (1.5 min); last automated activity 2026-11-04T22:28:17Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 3, recovery 88; 89 of 95 slot intervals hold an automated critical success (89 hold any automated activity); longest gap between successes 50.5 min.

**Range decisions:** 11-03T16:00 failed: failed before forecasting; 11-03T20:00 failed: failed before forecasting; 11-04T00:00 failed: failed before forecasting; 11-04T04:00 failed: failed before forecasting; 11-04T08:00 failed: failed before forecasting; 11-04T12:00 failed: failed before forecasting; 11-04T16:00 failed: failed before forecasting; 11-04T20:00 failed: failed before forecasting.

**PS1 decisions:** 11-03T16:00 no-rebalance; 11-03T20:00 no-rebalance; 11-04T00:00 no-rebalance; 11-04T04:00 no-rebalance; 11-04T08:00 no-rebalance; 11-04T12:00 no-rebalance; 11-04T16:00 no-rebalance; 11-04T20:00 no-rebalance.

**PS1 report coverage:** 0.803 as of 2026-11-04T20:37:51.654Z; due since and not covered: 11-04T20:00 no-rebalance.

**Range availability:** status within expiry (expires 2026-11-05T01:15:00Z); 24h stale; 4h stale; 72h stale.

**Scoring backlog:** none.

**Native scheduled monitors:** fresh (GitHub Actions API, scheduled runs); watchdog.yml heartbeat fresh (last run 2026-11-04T22:14:18Z: success; last success 2026-11-04T22:14:07Z); range-monitor.yml heartbeat fresh (last run 2026-11-04T17:46:34Z: failure, found a problem: actions: the latest scheduled range.yml run 41824745295 (2026-11-04T11:54:33Z) concluded failure (recorded; the stream has not recovered since); last success 2026-10-31T20:41:40Z); newest scheduled start of any workflow 2026-11-04T22:14:07Z.

**External timer (primary trigger):** gaps; 94 of 96 opportunities on time in 24 h, 0 delayed, absent 2026-11-04T09:42:00Z, 2026-11-04T15:12:00Z; last arrival 2026-11-04T22:27:02Z. Arrivals only: whether each request was sent needs the provider's history.

Recovery service-watch: fresh; passed; last check completion 2026-11-04T22:27:10Z.
Recovery study-watch: fresh; check failed; last check completion 2026-11-04T22:28:03Z.