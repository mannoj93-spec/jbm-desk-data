# Prospective options expiry pilot

State: active. Captures: 621/623 closed hours.

Control: nearest listed expiries. Alternate: nearest eligible expiries, capped at 14/35-day spans for 7d/30d.
Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.

| Horizon | Both usable | Gained | Lost | Neither | Missing capture |
|---|---:|---:|---:|---:|---:|
| 7d | 523 | 93 | 0 | 5 | 2 |
| 30d | 278 | 29 | 0 | 314 | 2 |

Books: 3326 usable / 3484 attempted / 3684 selected distinct contracts across hours.
Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_expiry_pilot.json).

Repeated horizons and contracts are dependent. A usability gain does not demonstrate predictive skill.
