# Operational health

Generated 2026-10-23T17:14:50Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Source:** healthy; last scheduled collector run 2026-10-23T16:51:02Z (23.8 min). Silences over 90 min in the last 72 h: 2026-10-22T20:31:29Z to 2026-10-22T23:31:34Z (180 min); 2026-10-22T23:31:34Z to 2026-10-23T01:48:45Z (137 min); 2026-10-23T01:48:45Z to 2026-10-23T06:33:19Z (285 min); 2026-10-23T06:33:19Z to 2026-10-23T12:01:03Z (328 min); 2026-10-23T12:01:03Z to 2026-10-23T16:51:02Z (290 min).

**Service continuity:** healthy; last persisted critical success 2026-10-23T17:13:00Z (1.8 min); last automated activity 2026-10-23T17:13:00Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 11, recovery 93; 94 of 95 slot intervals hold an automated critical success (94 hold any automated activity); longest gap between successes 30.1 min.

**Range decisions:** 10-22T08:00 published; 10-22T12:00 published; 10-22T16:00 published; 10-22T20:00 published; 10-23T00:00 published; 10-23T04:00 published; 10-23T08:00 published; 10-23T12:00 published.

**PS1 decisions:** 10-22T12:00 executed; 10-22T16:00 missed: no decision record (run absent); 10-22T20:00 executed; 10-23T00:00 executed; 10-23T04:00 missed: no decision record (run absent); 10-23T08:00 missed: no decision record (run absent); 10-23T12:00 missed: no decision record (run absent); 10-23T16:00 pending.

**PS1 report coverage:** 0.888 as of 2026-10-23T16:42:59.196Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-10-23T20:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-10-23T15:05:57Z: success; last success 2026-10-23T15:05:46Z); range-monitor.yml heartbeat fresh (last run 2026-10-23T14:28:47Z: success; last success 2026-10-23T14:28:34Z); newest scheduled start of any workflow 2026-10-23T16:50:13Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-10-23T17:12:02Z. Arrivals only: whether each request was sent needs the provider's history.
