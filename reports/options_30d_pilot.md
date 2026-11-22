# Prospective 30-day options maturity pilot

State: active. Captures: 372/374 closed hours.

Control: nearest eligible expiries within 45 days. Alternate: within 90 days. Both capped at a 35-day span.
Identical frozen leg filters and source capture; no extrapolation. Later books do not alter quote eligibility.

| Horizon | Both usable | Gained | Lost | Neither | Missing capture |
|---|---:|---:|---:|---:|---:|
| 30d | 283 | 86 | 0 | 3 | 2 |

Books: 1344 usable / 1388 attempted / 1476 selected distinct contracts across hours.
Quote sizes, source-to-book lag, spans, value differences and failure reasons: [JSON report](options_30d_pilot.json).

Separate prospective maturity experiment. Compare nearest eligible expiries within 45 versus 90 days, with identical leg filters and a 35-day maximum span in both arms. Repeated captures are dependent; usability is not predictive skill.
