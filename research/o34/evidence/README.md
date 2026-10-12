# O34 v1 evidence bundle (for package crypto-desk 12.4.16)

Separate from the skill ZIP because the skill installer rejects nested archives.

## Contents
- `raw/` — the 38 Binance USD-M BTCUSDT 4h monthly archive files (2023-08 … 2026-09) and their provider `.CHECKSUM` files, re-downloaded 2026-10-12 ~14:45Z from data.binance.vision. Every file's sha256 and provider checksum equal the values recorded by the original run (`studies/o34/inputs_v1.json`).
- `rows_v1.json` — the normalized, validated rows and per-file manifest the original run used (sha256 `63f0c6eaba0aebcd81c91c4c9bf78dec7464ee4db842e00ad274345bd99f1ac6`).
- `replay_raw_output.json`, `replay_rows_output.json` — replay results (0 differences in both modes, 6,942 bars).
- `classify_v1_1_output.json` — the Holm-gated classification (v1.1): "no demonstrated difference", unchanged from v1.

## Replay (offline, from the unzipped skill folder)
```
cd crypto-desk
python3 studies/o34/replay_o34.py --raw /path/to/o34-evidence-v1/raw     # exact provider bytes through jbm_archive validation
python3 studies/o34/replay_o34.py --rows /path/to/o34-evidence-v1/rows_v1.json
python3 studies/o34/classify_v1_1.py
```
Exit 0 = every variant, period and field of `studies/o34/results_v1.json` reproduced. Environment of the original run and of these replays: Python 3.13.16, NumPy 2.5.3 (Linux 6.18). The frozen runner `run_o34.py` (sha256 `107f1fe5…`) is used unchanged.

## What this bundle does not prove
Content hashes show the inputs, code and outputs are the ones recorded. They do not independently prove when the protocol was frozen: that rests on the in-thread message carrying the protocol hash (~13:29Z Oct 12) and the file's local time (13:28:54Z), not on a registry receipt or public commit.
