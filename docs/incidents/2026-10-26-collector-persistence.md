# Collector persistence failure during PR #53 merge

[Collector run 40251817627](https://github.com/mannoj93-spec/jbm-desk-data/actions/runs/40251817627)
started at 2026-10-26 00:57 UTC. Collection completed successfully, but main advanced during the run.
The first push was rejected; two 45-second fetch attempts timed out. Persistence ended unconfirmed after
93 seconds. This is a publication failure, not a successful collector interval.

GitHub retained artifact `12620703312`, `collector-recovery-40251817627`, with SHA-256
`5d08d07b7c80b25c3774f5f51b00d530a8dc94c2987f2a56870a12585b1430f3`.
The archive was downloaded and matched that digest before restoration on October 26.
The existing `scripts/restore_failed_run.py` compared its observations against main at
`7037d1a625fe8708fc7ede630e5ca422cf6207a8`.

Seven unique records were preserved under `data/restored/collector-40251817627/`: the run record,
market snapshot, Deribit options capture, OKX insurance capture, and three Hyperliquid account/enrichment/position
records. Twenty-three observations whose identities later runs had already stored were superseded rather than
duplicated. The receipt in `data/restored/receipts.jsonl` records restoration time and individual row hashes.

The restored rows are byte-identical to the archive. They remain outside live data, forecasts, scores, paper
execution, and lab input hashes. Their restoration does not repair on-time coverage or retrospectively rescue
the 01:00 UTC state forecast's stale-depth abstention. Working state and frozen registries from the archive were
not restored. Subsequent successful production runs do not erase this incident.

## Root cause (added in repo 2.30.5, 2026-10-28)

The same signature (push rejected, two 45 s fetch timeouts, unconfirmed after about 93 s) recurred at 13:01 UTC
(run 40327143379, PR #55 merge) and 22:42 UTC (run 40414468575, PR #56 merge). Each run started minutes before a
pull-request merge. The collector's checkout is depth 1; `scripts/commit_push.sh` (repo 2.30) fetched main without a
depth limit. When the new tip is a merge commit whose second parent forks below the shallow boundary, that fetch
downloads the merged branch's ancestry down to the root: reproduced against this repository from the commit before
the PR #53 merge, an unbounded fetch received 1.48 GB and was still running after 150 s, while `--depth=10` finished in
7 s with 14 MB. Ordinary collector-on-collector advances are linear and were unaffected.

Fix: bounded-depth fetches and `rebase --onto <fetched tip> <previous tip>` (repo 2.30.5,
`regression/test_rev2305_persistence.py`, which fails on the 2.30 script). The 13:01 and 22:42 artifacts
(`12653405041`, `12695580365`) are reconciled in their own recovery change.

## Follow-up (repo 2.30.6, 2026-10-29)

PR #59 (the bounded fetch) merged 2026-10-28T23:29:09Z as `cc299cec`. Collector run 40787475302 had started at
23:27:17Z on `04b59c83`, before the merge, so it ran the 2.30 script: its push at 23:30:21Z was rejected because the
merge moved main, and both unbounded fetches timed out - the same signature, one last time. Artifact `12859973279`
(digest `5b803138...`) was restored late: 7 unique rows kept, 24 superseded. In the 22 collector runs after the merge
(to about 12:30Z Oct 29) no push met a moved main, so the fix is merged but not yet observed in production.

