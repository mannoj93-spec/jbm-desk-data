# Acceptance window 2026-10-06T00:00Z - 2026-10-07T00:00Z

Declared with package 12.4.9 / repo 2.26; evidence cutoff 2026-10-07T02:00Z (window end + 120 min).

## Result of record (unchanged)

`result-acceptance-3.0.0.json` - acceptance-3.0.0 (repo 2.27, on main at evaluation), run by the scheduled check at
2026-10-07T02:22:19Z; Actions evidence retrieved 02:22:35Z (`actions-evidence-3.0.0.json.gz`, the saved
`--save-evidence` file, gzip of sha256 `e24e8e16...c34669`).

- verdict **insufficient** (exit 4); service_verdict **pass**; unattended certification **insufficient evidence**
- collection 95/95 intervals, longest gap 19.7 min; 6/6 range decisions published; 6/6 PS1 decisions executed;
  no lost output; scoring backlog empty; no person or unknown lineage in the critical chain
- reason: 188 critical-chain runs only timer-corroborated - no timer-provider receipt export was supplied

This is the window's result. It is not moved, re-declared or replaced.

## Supplementary corrected-checker audit (repo 2.28, not a replacement)

acceptance-3.0.0 was later shown to have five false-pass modes (repo 2.28 CHANGELOG). To check whether any of them
affected this window, acceptance-3.1.0 evaluated the same window and cutoff offline:

- Actions evidence retrieved 2026-10-07T19:37:35Z, including GitHub's repository activity (push) history for main
  (`actions-evidence-3.1.0.json.gz`, gzip of sha256 `cd05701f...fb21b84`); 406 pushes up to the cutoff used
- repository state: commit `6ce0e82a` (after-commit of the last push at or before the cutoff)
- result `supplementary-acceptance-3.1.0.json`: verdict **insufficient**, service_verdict **pass**, identical numbers
  (95/95, 19.7 min, 6/6, 6/6); 0 records first pushed later than 15 min after their record time; every range
  registration first pushed before its window start; strict validation of all 18 forecasts passed
- same reason: no timer-provider receipts (and the timer job id is not yet pinned in `docs/acceptance/timer.json`)

Conclusion: the original result stands; the corrected checker finds no false pass in this window. Strict unattended
certification remains insufficient - it needs the cron-job.org execution history for the window.

## Replay

```
git clone https://github.com/mannoj93-spec/jbm-desk-data main && cd main   # contains 6ce0e82a
gunzip -k ../actions-evidence-3.1.0.json.gz
python <repo 2.28>/scripts/service_acceptance.py --from 2026-10-06T00:00:00Z --to 2026-10-07T00:00:00Z \
  --now 2026-10-07T20:05:00Z --actions-evidence ../actions-evidence-3.1.0.json --repo .
```

The 3.0.0 result replays with the 2.27 checker and `actions-evidence-3.0.0.json` the same way (committer-time
snapshot; no push history).
