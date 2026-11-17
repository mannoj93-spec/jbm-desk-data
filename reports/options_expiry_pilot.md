# Prospective options expiry pilot

State: active. Captures: 497/498 closed hours.

Control: nearest listed expiries. Alternate: nearest eligible expiries, capped at 14/35-day spans for 7d/30d.
Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.

| Horizon | Both usable | Gained | Lost | Neither | Missing capture |
|---|---:|---:|---:|---:|---:|
| 7d | 419 | 75 | 0 | 3 | 1 |
| 30d | 168 | 17 | 0 | 312 | 1 |

Books: 2552 usable / 2556 attempted / 2708 selected distinct contracts across hours.
Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_expiry_pilot.json).

Repeated horizons and contracts are dependent. A usability gain does not demonstrate predictive skill.
