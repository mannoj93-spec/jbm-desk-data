# Acceptance window 2026-10-07T00:00Z - 2026-10-08T00:00Z

Declared 2026-10-05T21:10Z with repo 2.27 (`docs/acceptance/2026-10-07.json`). The evidence cutoff is
2026-10-08T02:00Z (window end + 120 min) and the earliest evaluation time was 02:15Z. The declaration was amended
append-only on Oct 7 at 20:10Z (repo 2.28). Under the amendment, the declared checker acceptance-3.0.0 gives the result
of record and acceptance-3.1.0 audits the same window and cutoff. **The window is credited as a pass only if both
pass.**

## When this was evaluated

The window was **first evaluated on 2026-10-12 at about 19:05Z (repo 2.28.2)**, 4 days and 17 hours after its earliest
evaluation time. Nothing had been computed or recorded for it before then. The window, the cutoff, the targets and the
declared checker are as declared. Evaluating late changes only the time at which the Actions metadata was read. The
repository is still read as of the cutoff.

## Result of record — acceptance-3.0.0 (declared)

File: `result-acceptance-3.0.0.json`.

- **Checker.** `scripts/service_acceptance.py` at the 2.27 merge `f242b90e` (sha256 `f3da7d26…`). It ran from a
  checkout of that commit with `--commit f13b35bc` (main at evaluation). Its repository snapshot is the last
  first-parent commit with committer time at or before the cutoff: `eace196b` (01:59:37Z). That is 3.0.0's own
  method: committer time, not push time.
- **Actions evidence.** Fetched by 3.0.0 itself and saved as `actions-evidence-3.0.0.json.gz` (gzip of
  `actions-evidence/1`, sha256 `07dd6d97…`; normalized hash in the result `b054e603…`). It holds 796 runs, complete,
  retrieved 19:05:00Z. The run's `--now` was set at launch (19:04:42Z), 18 s before the retrieval finished.
- **Timer receipts.** `docs/acceptance/receipts/2026-10-07-cron-job-org.json` (sha256 `d1f54b15…`). It covers only
  10:12Z-22:27Z, because the provider console keeps about 50 executions.
- **Verdict: insufficient (exit 4).**
  - service_verdict: **pass**
  - unattended certification: **insufficient evidence**
  - reason: 92 critical-chain runs are only timer-corroborated (outside the receipt export's coverage)
- **Numbers:**
  - collection: 94 of 95 intervals (one empty interval allowed of 2), longest gap 25.7 min
  - strict (verified and timer-receipt starts only): 90 of 95, longest gap 26.6 min
  - decisions: 6 of 6 range decisions published; 6 of 6 PS1 decisions executed (chain verified: 23 executions)
  - collector runs: 171, of which 167 persisted-success and 4 yielded with valid receipts; no lost output
  - scoring backlog: empty
  - no person and no unknown lineage in the critical chain
- **The empty interval** is 15:07-15:22Z (15:02:00 → 15:27:42). It follows the 15:12Z external-timer opportunity,
  which received an HTTP 500 from GitHub (`docs/incidents/2026-10-07-external-timer-gaps.md`). It counts against the
  window, as the declaration requires.

## Supplementary audits (not replacements)

3.1.0 and 3.2.0 read the repository at `eace196b`, the after-commit of the last push to main at or before 02:00Z
(pushed 01:59:40Z). Each used 415 pushes from GitHub's activity API. 3.0.0 reached the same commit by committer time.

**Evidence.** `actions-evidence-3.1.0.json.gz` (gzip of `actions-evidence/2` with push history, sha256 `752b3ad7…`;
normalized `ae466501…`): 796 runs and 1,600 pushes, complete, retrieved 19:03:32Z. The 3.2.0 checker fetched it. Its
fetch code (`fetch_evidence`, `fetch_pushes`, `complete_evidence`) is unchanged from 3.1.0.

| checker | code | verdict | service | collection | late records | PS1 | range |
|---|---|---|---|---|---|---|---|
| 3.0.0 (record) | `f3da7d26…` @ f242b90e | insufficient | pass | 94/95, 25.7 min | — (no push history) | 6/6 executed | 6/6 published |
| 3.1.0 (amendment) | `79a1ceb8…` (main f13b35bc; identical to the 2.28 merge's; timer pinned) | insufficient | pass | 94/95, 25.7 min | 0 | 6/6 executed | 6/6 published |
| 3.2.0 (content crediting) | `5ed60ce6…` (repo 2.28.2) | insufficient | pass | 94/95, 25.7 min | 0 | 6/6 executed | 6/6 published |

- **Receipts.** 3.1.0 and 3.2.0 validated the receipt export (47 accepted executions, nothing rejected). 3.0.0 does not
  validate receipts. The initiation counts are identical across the three checkers: 96 verified, 35 timer-receipt and
  36 timer-corroborated collector records.
- **3.1.0 vs 3.2.0.** Every field is identical except the availability label, which now reads "content first pushed".
  No collector record and no PS1 execution received content after its first push.

## Conclusion

The window is **not credited as a pass**. Every service target was met under all three checkers. Strict unattended
certification is not established: the receipt export covers about half of the window, and the rest is
timer-corroborated only. No checker finds a false pass. The 3.2.0 crediting fix changes nothing in this window.

## Replay

```
git clone https://github.com/mannoj93-spec/jbm-desk-data main && cd main          # contains eace196b and f13b35bc
gunzip -k docs/acceptance/results/2026-10-07/actions-evidence-3.1.0.json.gz
python scripts/service_acceptance.py --from 2026-10-07T00:00:00Z --to 2026-10-08T00:00:00Z --now <iso> \
  --actions-evidence docs/acceptance/results/2026-10-07/actions-evidence-3.1.0.json \
  --timer-receipts docs/acceptance/receipts/2026-10-07-cron-job-org.json --repo .
```

The local clone must contain **every** pushed commit named in the evidence, including those after the cutoff. If it
does not, availability reads "unestablished" (fail-safe: insufficient, never pass). For 3.0.0, run
`scripts/service_acceptance.py` from a checkout of `f242b90e` with `--actions-evidence <3.0.0 file>` and
`--commit f13b35bc`.
