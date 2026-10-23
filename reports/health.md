# Operational health

Generated 2026-10-23T12:29:48Z by health-1.4.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Source:** healthy; last scheduled collector run 2026-10-23T12:01:03Z (28.8 min). Silences over 90 min in the last 72 h: 2026-10-22T20:31:29Z to 2026-10-22T23:31:34Z (180 min); 2026-10-22T23:31:34Z to 2026-10-23T01:48:45Z (137 min); 2026-10-23T01:48:45Z to 2026-10-23T06:33:19Z (285 min); 2026-10-23T06:33:19Z to 2026-10-23T12:01:03Z (328 min).

**Service continuity:** healthy; last persisted critical success 2026-10-23T12:27:57Z (1.9 min); last automated activity 2026-10-23T12:27:57Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 18, recovery 90; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 20.5 min.

**Range decisions:** 10-22T04:00 published; 10-22T08:00 published; 10-22T12:00 published; 10-22T16:00 published; 10-22T20:00 published; 10-23T00:00 published; 10-23T04:00 published; 10-23T08:00 published.

**PS1 decisions:** 10-22T08:00 executed; 10-22T12:00 executed; 10-22T16:00 missed: no decision record (run absent); 10-22T20:00 executed; 10-23T00:00 executed; 10-23T04:00 missed: no decision record (run absent); 10-23T08:00 missed: no decision record (run absent); 10-23T12:00 pending.

**PS1 report coverage:** 0.8952 as of 2026-10-23T12:18:54.581Z; due since and not covered: none.

**Range availability:** status within expiry (expires 2026-10-23T16:25:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Monitors:** stale (GitHub Actions API, scheduled runs); watchdog.yml heartbeat stale (last run 2026-10-23T10:05:24Z: success; last success 2026-10-23T10:05:15Z); range-monitor.yml heartbeat fresh (last run 2026-10-23T06:34:19Z: success; last success 2026-10-23T06:34:08Z); newest scheduled start of any workflow 2026-10-23T12:01:10Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-10-23T12:27:01Z. Arrivals only: whether each request was sent needs the provider's history.
