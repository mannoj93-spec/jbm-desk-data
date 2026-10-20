# O33 v3.1 correction 1 — evidence classes by call type, rule and epoch (prepared in repo 2.30)

`register-2.3.0` decided a result's evidence class from its admission basis and receipt time. A conditional call
registered before the v3.1 effective time and admitted on a quoted receipt was therefore classed **original-rule**,
although O33 v3 defined only lean and containment calls. This correction classifies by call type, admission rule and
epoch (`spec.json`), implemented by `enforcement/desk_register.py` (`register-2.4.0`, the package 12.4.21 copy).

Nothing frozen changes: `../o33-v3.1/` (including its `register-2.3.0` enforcement copy) and `../o33-v3/` keep their
bytes. Results computed before this correction keep their recorded classes; recalculations name this correction and
are reassessments. Effective at the first push of this directory to main, recorded in `effective.json` afterwards.

Verify: `python3 scripts/o33_v31_manifest.py check`.
