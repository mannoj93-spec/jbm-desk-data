"""Crypto-desk range forecaster (desk/, package 12.1): runs the desk's own offline suites here so the
Regression and numerical fixtures workflow covers them on every push."""
import importlib
import sys
import unittest
from pathlib import Path

DESK = Path(__file__).resolve().parents[1] / "desk"
MODULES = ("test_jbm_measure", "test_jbm_archive", "test_range_model", "test_range_contract", "test_range_job",
           "test_hardening", "test_release")


def load_tests(loader, tests, pattern):
    if str(DESK) not in sys.path:
        sys.path.insert(0, str(DESK))
    suite = unittest.TestSuite()
    for name in MODULES:
        suite.addTests(loader.loadTestsFromModule(importlib.import_module(name)))
    return suite
