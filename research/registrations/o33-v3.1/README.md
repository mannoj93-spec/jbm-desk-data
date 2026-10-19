# O33 v3.1 — amendment record (prepared in repo 2.29)

O33 v3.1 changes **which calls are admitted and how conditionals are handled**; it does not change any v3 estimator,
constant, cohort rule, cost or claim threshold (`spec.json` lists what changed and what did not). The frozen v3
artifacts in `../o33-v3/` are untouched.

**Effective time.** The first push of this directory to `main` — read from the merge commit (GitHub activity API) and
recorded in `effective.json` after the merge. The 12.4.19 package implemented these rules on Oct 19 2026 without a
published record, so that earlier timing cannot be established and is not claimed. Calls registered before the
effective time are reported as original-rule corrections or retrospective reassessments, never as prospective v3.1.

**Identity.** `manifest.json` pins the sha256 of `spec.json`, the enforcement wrapper (`enforcement/desk_register.py`,
register-2.3.0), the shared evidence contract (`enforcement/desk_evidence.py`, evidence-1.0.0, byte-identical to
`research_tools/evidence_contract.py`) and the frozen v3 files it depends on. Private call records are not published.

**Results** are reported per population (all admitted, quote-only, order-record-only), each recomputed from
eligibility through de-duplication, with the conditional funnel beside any conditional score
(`desk_register.score_v31`). Outcome names: the conditional plain grade is the invalidation-path grade; a unit's `d`
is the terminal-close, drift-adjusted return.

Verify: `python3 scripts/o33_v31_manifest.py check`.
