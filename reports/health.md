# Operational health

Generated 2026-11-11T19:45:05Z by health-1.5.0 (runner UTC clock at the check (time.time)). this report is written by the collector run; older than 90 min means no collector run has persisted a newer report - the scheduler may have been silent, the run may not have executed (no runner), may have failed, or may have failed to persist; its contents are not current.

**Native collector schedule (secondary trigger):** last scheduled collector run 2026-11-11T18:03:41Z (101.4 min); 12 silence(s) over 90 min in the last 72 h, longest 631 min. Native starts per closed day: 2026-11-08 5 of 100 automated runs; 2026-11-09 3 of 96 automated runs; 2026-11-10 4 of 97 automated runs. Each silence is in reports/health.json; incidents carry one summary row per day.

**Service continuity:** healthy; last persisted critical success 2026-11-11T19:43:18Z (1.8 min); last automated activity 2026-11-11T19:43:18Z (critical success, recovery). 45-min acceptance target met now. Last 24 h: 96 slots; runs by source native-schedule 4, recovery 94; 95 of 95 slot intervals hold an automated critical success (95 hold any automated activity); longest gap between successes 18.5 min.

**Range decisions:** 11-10T12:00 published; 11-10T16:00 published; 11-10T20:00 published; 11-11T00:00 published; 11-11T04:00 published; 11-11T08:00 published; 11-11T12:00 published; 11-11T16:00 published.

**PS1 decisions:** 11-10T12:00 executed; 11-10T16:00 executed; 11-10T20:00 executed; 11-11T00:00 executed; 11-11T04:00 executed; 11-11T08:00 executed; 11-11T12:00 executed; 11-11T16:00 no-rebalance.

**PS1 report coverage:** 0.7824 as of 2026-11-11T16:41:04.370Z; due since and not covered: 11-11T16:00 no-rebalance.

**Range availability:** status within expiry (expires 2026-11-11T20:30:00Z); 24h valid-current; 4h valid-current; 72h valid-current.

**Scoring backlog:** none.

**Native scheduled monitors:** fresh (GitHub Actions API, scheduled runs); watchdog.yml heartbeat fresh (last run 2026-11-11T18:42:50Z: success; last success 2026-11-11T18:42:40Z); range-monitor.yml heartbeat fresh (last run 2026-11-11T17:28:42Z: success; last success 2026-11-11T17:28:32Z); range-readiness.yml heartbeat fresh (last run 2026-11-11T02:14:02Z: success; last success 2026-11-11T02:12:59Z); newest scheduled start of any workflow 2026-11-11T18:42:40Z.

**External timer (primary trigger):** arriving; 96 of 96 opportunities on time in 24 h, 0 delayed, absent none; last arrival 2026-11-11T19:42:02Z. Arrivals only: whether each request was sent needs the provider's history.

**External timer token:** expiry not recorded - record token.expires_utc in docs/acceptance/timer.json; an expired token stops the primary trigger.

**Record integrity:** no malformed lines in the files read.

Recovery service-watch: fresh; passed; last check completion 2026-11-11T19:42:10Z.
Recovery study-watch: fresh; passed; last check completion 2026-11-11T19:43:17Z.