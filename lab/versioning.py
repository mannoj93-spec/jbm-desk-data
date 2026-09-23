"""Evaluation-version identity (lab-2.0).

A prospective clock belongs to an EVALUATION VERSION, not to a design file alone. The version id is
a hash over everything that decides what an event, a label or a verdict means:
  design          the design JSON bytes (question, variants, groups, horizons, criteria)
  common          semantic code shared by every design: lab/asof.py, lab/common.py, lab/data.py,
                  lab/events.py, lab/outcomes.py (labels and cost model), lab/stats.py,
                  lab/baseline.py (baseline methodology), lab/experiments.py (evaluation rules),
                  lab/hlevidence.py (evidence attribution)
  module          the design's detector/feature module
  data            the collector constants the module's inputs depend on (sampling policy, schema
                  and field lists), named per module in DATA_DEPENDENCIES
Code is hashed SEMANTICALLY: the Python AST with docstrings removed (comments are not in the AST),
so documentation and comment edits do not start a new version, while any change to logic,
constants or conventions does. Data files are never part of the identity, so ordinary data
commits never reset a clock. Reports, evidence writers and the CLI (lab/evidence.py, lab/run.py,
lab/skill_eval.py) are presentation and are deliberately excluded.
"""
import ast
import hashlib
import json
from pathlib import Path

COMMON = ("lab/asof.py", "lab/common.py", "lab/data.py", "lab/events.py", "lab/outcomes.py", "lab/stats.py",
          "lab/baseline.py", "lab/experiments.py", "lab/hlevidence.py")
MODULE_FILES = {"flow_absorption": "lab/modules/flow_absorption.py", "account_behavior": "lab/modules/accounts.py",
                "liq_exposure": "lab/modules/liq_exposure.py", "twap_lifecycle": "lab/modules/twap.py",
                "liquidity_recovery": "lab/modules/liquidity.py",
                "options_disagreement": "lab/modules/options_disagreement.py",
                "cross_asset": "lab/modules/cross_asset.py", "deleveraging": "lab/modules/deleveraging.py"}
_PRICES = [("schema.py", "PRICE_SERIES"), ("schema.py", "KLINE_FIELDS"), ("enrich.py", None)]
_HL = [("hlsample.py", "POLICY_DOC"), ("hlsample.py", "ACCOUNT_FIELDS"), ("hlsample.py", "POSITION_FIELDS"),
       ("hlsample.py", "FILL_FIELDS"), ("hlsample.py", "FIXED_N"), ("hlsample.py", "ROTATING_N")]
DATA_DEPENDENCIES = {
    "flow_absorption": _PRICES,
    "cross_asset": _PRICES,
    "account_behavior": _HL + _PRICES,
    "liq_exposure": _HL + _PRICES,
    "twap_lifecycle": _HL + _PRICES,
    "options_disagreement": [("optionsbook.py", "SCHEMA"), ("optionsbook.py", "ROW_FIELDS"),
                             ("optionsbook.py", "PANEL_FIELDS"), ("optionsbook.py", "PANEL_TARGET_DAYS")] + _PRICES,
    "deleveraging": [("enrich.py", None)] + _PRICES,
    "liquidity_recovery": [("stream/books.py", None), ("stream/service.py", "Recorder")] + _PRICES,
}


def _strip_docstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree


def semantic_hash(path, name=None):
    """sha256 of the docstring-free AST of a file, or of one top-level definition in it."""
    p = Path(path)
    if not p.exists():
        return None
    tree = _strip_docstrings(ast.parse(p.read_text()))
    if name is not None:
        nodes = [n for n in tree.body
                 if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name)
                 or (isinstance(n, ast.Assign) and any(getattr(t, "id", None) == name for t in n.targets))]
        if not nodes:
            return None
        tree = ast.Module(body=nodes, type_ignores=[])
    return hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest()


def components(base, design):
    base = Path(base)
    comp = {"design": design["_sha256"]}
    for rel in COMMON:
        comp[rel] = semantic_hash(base / rel)
    mod = MODULE_FILES.get(design["module"])
    comp[mod or f"unknown module {design['module']}"] = semantic_hash(base / mod) if mod else None
    for rel, name in DATA_DEPENDENCIES.get(design["module"], []):
        comp[f"{rel}:{name or '*'}"] = semantic_hash(base / rel, name)
    return comp


def version_id(comp):
    return "ev-" + hashlib.sha256(json.dumps(comp, sort_keys=True).encode()).hexdigest()[:12]
