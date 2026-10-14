# O34 — close-basis exits against the R-09 stop alone (crypto-desk 12.4.14–12.4.16)

Retained here on **2026-10-12** (repo 2.28.2). The commit date is the date these files reached this repository. It is
**not** evidence of when the protocol was frozen (see Chronology).

## Question and result

Does an exit on a 4H close 0.7 entry-σ beyond entry (B), placed inside the R-09 2σ stop, change the net outcome
compared with the R-09 stop alone (A)? BTCUSDT USD-M perpetual 4H bars from 2023-08 to 2026-09 (6,942 bars, 38
monthly provider files). Both directions are tested at every eligible close. The study has nine (k, H) variants with a
Holm family on validation. The primary variant is k = 0.7, H = 6 bars.

| period | decision times | mean D = B − A (bp) | 95% interval (bp) | p (two-sided) |
|---|---|---|---|---|
| validation | 2,185 | −0.469 | [−2.839, +1.854] | 0.706 (Holm 1.0) |
| holdout | 2,185 | +0.103 | [−2.418, +2.632] | 0.934 |

Classification: **no demonstrated difference**. v1 recorded this result, and the v1.1 Holm-gated rule gives the same
one. The outcome excludes funding. The bootstrap is a stationary block bootstrap. Quantile uncertainty was not
estimated. The study covers unconditioned entries at every close, not the desk's discretionary entries.

## Files

| file | role | sha256 |
|---|---|---|
| `protocol.json` | v1 protocol, frozen — **not published here** (see below) | `8b7fb0f1dc295b8aaed11bd746e7672f6a2304213ffd37df7178727ed3adc2c4` (`protocol.sha256`) |
| `run_o34.py` | v1 runner, written after the freeze, unchanged | `107f1fe5e9a5237599faba00749c3d9b27d5da5f1dcfde1fda7dc510b4e3ddfb` |
| `results_v1.json` | v1 results, unchanged | `5efc7d92921ad7152e12d2816e84776788833fbe98a6e39397ddb658b7e955eb` |
| `inputs_v1.json` | the 38 input files: URLs, sha256 values, provider checksums (12.4.16) | `81c85e9e1571adea1f2018e904158bb251372986bc47dae533c8749c70f1434d` |
| `erratum_v1_1.json` | v1.1 erratum: v1's filing branch ignored the declared Holm gate (12.4.16) | `c2847b4a38d257f64677d0d6a9add01774454e4c01c3354db0c351de59a66aba` |
| `classify_v1_1.py` | Holm-gated classification, o34-classify-1.1.0 (12.4.16) | `e8a339f5eb1c2c3571b8cd12a4bf6f94986c230396f9fe47d4d3d0cb9091461f` |
| `replay_o34.py` | offline replay against `results_v1.json` (12.4.16) | `cb413cbcd4e8ef3bb7d59d8338c78f66299da45418e0f451bc823e83b70edd41` |
| `evidence/` | the O34 evidence bundle v1 (`o34-evidence-v1.zip`, sha256 `5649aec2…`): `raw/` (exact provider bytes), replay and classification outputs, its own README | — |
| `evidence/rows_v1.json.gz` | gzip of the normalized rows; `gunzip` restores the file the replay checks | uncompressed `63f0c6eaba0aebcd81c91c4c9bf78dec7464ee4db842e00ad274345bd99f1ac6` |

These files are byte-identical to `studies/o34/` in the crypto-desk 12.4.16 package (`crypto-desk-12.4.16.zip`, sha256
`b2a1e857…`). That package also holds the tests (`test_o34_exits.py`, `test_o34_v1_1.py`), which are not copied here.

**Why `protocol.json` is withheld.** This repository is public. The protocol's `why` and `operator_decision` fields
record the operator's own positions and their dollar results. Under the desk's policy, private operating records stay
out of the public repository. Only the protocol's hash is published here. The file stays in the skill package. The
operator can publish it later as-is; its hash cannot change.

## Replay (offline)

First copy `protocol.json` from the 12.4.16 package into this folder and check it against `protocol.sha256`. Then
run, from the repository root:

```
(cd research/o34 && sha256sum -c protocol.sha256)              # after placing the private protocol.json there
PYTHONPATH=desk python3 research/o34/replay_o34.py --raw research/o34/evidence/raw
gunzip -k research/o34/evidence/rows_v1.json.gz
PYTHONPATH=desk python3 research/o34/replay_o34.py --rows research/o34/evidence/rows_v1.json
python3 research/o34/classify_v1_1.py
```

Exit 0 means every variant, period and field of `results_v1.json` was reproduced. Both commands were run from this
layout on 2026-10-12 (Python 3.13.16, NumPy 2.5.3): `--raw` gave 0 differences and `--rows` gave 0 differences, over
6,942 bars. `desk/jbm_archive.py`, `desk/jbm_measure.py` and `desk/range_contract.py` were byte-identical to the
package's copies. **Do not run `run_o34.py` as a script.** Its `__main__` rewrites `results_v1.json`. `replay_o34.py`
calls `run()` instead, which writes nothing.

## Chronology (what the hashes do and do not show)

- Protocol file local time: 2026-10-12 13:28:54Z. Its sha256 was sent to the operator in the thread at about 13:29Z,
  before the run.
- v1 run: 13:30:54Z (`results_v1.json` `run_utc`).
- 12.4.16 additions (inputs record, erratum, classifier, replay): about 14:45Z.
- This repository: committed 2026-10-12, after all of the above.

The content hashes show that these inputs, this code and these outputs are the recorded ones. They do not
independently prove the freeze time. That rests on the thread message and the local file time, not on a registry
receipt or an earlier public commit.
