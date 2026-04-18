---
phase: 54-compiler-baseline-locks
verified: 2026-04-18
status: passed
score: 5/5 must-haves verified
---

# Phase 54: Compiler Baseline Locks Verification Report

**Phase Goal:** Maintainers can verify current compiler support and depth anchors before new motif behavior changes.
**Status:** passed

## Goal Achievement

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Logistic relaxed compile diagnostic is locked at depth 27 with no macro hits. | VERIFIED | `test_compile_logistic_archived_relaxed_baseline` asserts strict `depth_exceeded`, relaxed depth `27`, nodes `77`, and hits `[]`. |
| 2 | Planck relaxed compile diagnostic is locked at depth 20 with existing macro hits. | VERIFIED | `test_compile_planck_archived_relaxed_baseline` asserts strict `depth_exceeded`, relaxed depth `20`, nodes `67`, and hits `scaled_exp_minus_one_template` plus `direct_division_template`. |
| 3 | Michaelis-Menten strict support remains depth 12 with `saturation_ratio_template`. | VERIFIED | `test_existing_macro_supported_demos_do_not_regress` asserts strict validation and the expected macro hit, depth, and node count. |
| 4 | Arrhenius strict support remains on `direct_division_template`. | VERIFIED | `test_existing_macro_supported_demos_do_not_regress` asserts strict validation and the expected macro hit. |
| 5 | Shockley strict support remains on `scaled_exp_minus_one_template`. | VERIFIED | `test_existing_macro_supported_demos_do_not_regress` asserts strict validation and the expected macro hit. |

## Automated Checks

| Command | Result |
|---------|--------|
| `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_logistic_archived_relaxed_baseline tests/test_compiler_warm_start.py::test_compile_planck_archived_relaxed_baseline tests/test_compiler_warm_start.py::test_existing_macro_supported_demos_do_not_regress -q` | `3 passed` |
| `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py -q` | `27 passed, 1 warning` |

## Human Verification Required

None.

## Gaps Summary

No gaps found. Phase 54 achieved the baseline lock goal and made no production-code changes.
