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
