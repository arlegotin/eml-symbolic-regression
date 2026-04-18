---
phase: 54-compiler-baseline-locks
plan: 01
subsystem: compiler-tests
tags: [compiler, regression, macro-diagnostics, pytest]
requirements-completed: [BASE-01, BASE-02, BASE-03, BASE-04, BASE-05]
duration: 2min
completed: 2026-04-18
---

# Phase 54 Plan 01: Compiler Baseline Locks Summary

## Accomplishments

- Added a logistic archived relaxed diagnostic regression: strict unsupported by `depth_exceeded`, relaxed depth `27`, node count `77`, and no macro hits.
- Strengthened the Planck archived relaxed diagnostic regression: strict unsupported by `depth_exceeded`, relaxed depth `20`, node count `67`, and macro hits `scaled_exp_minus_one_template` plus `direct_division_template`.
- Added a combined no-regression test for existing strict-supported macro wins: Shockley, Arrhenius, and Michaelis-Menten.
- Confirmed default strict compiler gates remain `max_depth=13` and `max_nodes=256`.

## Files Modified

- `tests/test_compiler_warm_start.py` - Baseline-lock tests for logistic, Planck, and existing supported macro demos.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_logistic_archived_relaxed_baseline tests/test_compiler_warm_start.py::test_compile_planck_archived_relaxed_baseline tests/test_compiler_warm_start.py::test_existing_macro_supported_demos_do_not_regress -q` -> `3 passed`
- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py -q` -> `27 passed, 1 warning`

## Notes

- The warning is the pre-existing overflow warning in `test_high_noise_warm_start_records_failure_mechanism`; it is unrelated to the Phase 54 baseline-lock changes.
- No production compiler behavior changed in this phase.
