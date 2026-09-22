#!/usr/bin/env python3
"""runbook.md §G numerical fixtures (package 9.1), as tests. Exit 1 on any failure.

An implementation is `tested` only when it reproduces every fixture. The gross-vs-net
concentration fixture is not here: its snapshot was never stored (§G says so)."""
import math
import sys

import formulas as L

FAILS = []


def check(name, got, want, tol=5e-4):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print(f"{'PASS' if ok else 'FAIL'}  {name:52s} got {got:.6g}  want {want:.6g}")
    if not ok:
        FAILS.append(name)


def check_eq(name, got, want):
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'}  {name:52s} got {got!r}  want {want!r}")
    if not ok:
        FAILS.append(name)


# synthetic index S = OI × (a − b): composition unchanged, S moves with OI alone
check("synthetic index, OI 100", L.synthetic_index(100, 0.60, 0.70), -10)
check("synthetic index, OI 120", L.synthetic_index(120, 0.60, 0.70), -12)
# share from ratio
check("share from ratio r=1.5", L.share_from_ratio(1.5), 0.600)
# size concentration = ratio of odds; the retired p/a is not this ratio
check("size-concentration p0.70 a0.60", L.size_concentration(0.70, 0.60), 1.5556)
check("retired p/a (reference only)", 0.70 / 0.60, 1.1667)
# 0 of 28
check("0/28 one-sided exact upper", L.zero_of_n_upper(28), 0.1016)
check("0/28 two-sided Clopper-Pearson upper", L.zero_of_n_upper(28, two_sided=True), 0.1234, tol=2e-3)
check("0/28 rule of three", L.rule_of_three(28), 0.1071)
# Hyperliquid: 8h formula, hourly cash = ÷8, API field already hourly
f8, h = L.hyperliquid_funding(0.0)
check("HL zero premium F_8h (%)", f8 * 100, 0.01000)
check("HL zero premium hourly (%)", h * 100, 0.00125)
f8, h = L.hyperliquid_funding(0.01)
check("HL doc example P=+1.00% F_8h (%)", f8 * 100, 0.95000)
check("HL doc example hourly (%)", h * 100, 0.11875)
f8, h = L.hyperliquid_funding(-0.0002)
check("HL dead zone P=-0.02% F_8h (%)", f8 * 100, 0.01000)
check("HL dead zone hourly (%)", h * 100, 0.00125)
check_eq("HL dead zone premium identifiable", L.premium_identifiable(f8), False)
# four of four at p81
check("four-of-four at p81: 0.19^4", 0.19 ** 4, 0.00130)
# countdown from verified timestamps (T10's logged 1.6h was 2h17m)
check_eq("countdown 15:43Z -> 18:00Z", L.countdown("2026-09-16T15:43:00Z", "2026-09-16T18:00:00Z"), "2h 17m")
# a range is not a sigma
check("Gaussian E[range]/sigma", L.gaussian_range_over_sigma(), 1.596, tol=1e-3)
# add valuation, toy: four equiprobable paths
toy = [dict(hold_pnl=-2000, hold_liq=True, add_pnl=-1500, add_liq=False),
       dict(hold_pnl=-2000, hold_liq=True, add_pnl=-3000, add_liq=True),
       dict(hold_pnl=1000, hold_liq=False, add_pnl=1000, add_liq=False),
       dict(hold_pnl=-500, hold_liq=False, add_pnl=-500, add_liq=False)]
v = L.add_valuation(10000, 2000, 1000, toy)
check("add toy E[W_hold]", v["E_hold"], 11125)
check("add toy E[W_add]", v["E_add"], 11000)
check("add toy marginal", v["marginal_before_yield"], -125)
check("add toy -C*P(liq|add)", v["minus_C_Pliq"], -250)
check("add toy loss avoided", v["loss_avoided"], 125)
# add valuation, far barrier: exactly zero before yield
far = [dict(hold_pnl=x, hold_liq=False, add_pnl=x, add_liq=False) for x in (-700, -200, 300, 900)]
v = L.add_valuation(10000, 2000, 1000, far, yield_annual=0.04, hours=168)
check("add far barrier marginal before yield", v["marginal_before_yield"], 0.0)
check("add far barrier yield foregone ($)", v["yield_foregone"], 0.767, tol=2e-3)

print(f"\n{len(FAILS)} failed" if FAILS else "\nall fixtures pass")
sys.exit(1 if FAILS else 0)
