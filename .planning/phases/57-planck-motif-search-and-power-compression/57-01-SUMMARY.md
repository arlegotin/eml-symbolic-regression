---
phase: 57-planck-motif-search-and-power-compression
plan: 01
subsystem: compiler
tags: [sympy, eml, planck, motif-search, power, pytest]
requirements-completed: [MOTIF-03, MOTIF-04, PLAN-01, PLAN-02, PLAN-03, PLAN-04, PLAN-05]
duration: 8min
completed: 2026-04-18
---

# Phase 57 Plan 01: Planck Motif Search and Power Compression Summary

## Accomplishments

- Added `low_degree_power_template`, which lowers positive integer powers as `exp(n*log(g))` only when the candidate is shorter than repeated multiplication.
- Locked cube shortening: `x**3` now validates at depth `9`, node count `25`, down from depth `16`, node count `33`.
- Preserved square behavior: `x**2` stays on the existing repeated-multiplication path because it is already shorter.
- Added `motif_search.py`, a small bounded validation-record utility for motif candidates, and used it to record cube candidate acceptance over independent samples.
- Reduced Planck relaxed compile depth from archived `20` to `14`, with macro hits `low_degree_power_template`, `scaled_exp_minus_one_template`, and `direct_division_template`.
- Preserved honest Planck status: strict compile still fails at `max_depth=13`, so Planck remains unsupported/stretch and warm-start is not promoted.

## Files Modified

- `src/eml_symbolic_regression/compiler.py` - Added shorter low-degree positive power macro dispatch.
- `src/eml_symbolic_regression/motif_search.py` - Added bounded motif validation record helper.
- `tests/test_compiler_warm_start.py` - Added cube/square power tests, motif-search record assertions, and updated Planck diagnostics.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compiler_fail_closed_negative_cases tests/test_compiler_warm_start.py::test_low_degree_power_template_shortens_cube_but_not_square tests/test_compiler_warm_start.py::test_planck_compile_depth_drops_below_archived_relaxed_diagnostic -q` -> `3 passed`
- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py -q` -> `34 passed, 1 warning`

## Decisions Made

- Planck is not strict-supported because the improved exact EML tree is depth `14`, still above the shipped strict gate `13`.
- Planck warm-start remains blocked by strict compile support; Phase 58 should report this as improved compile diagnostics rather than recovery.
- The square path intentionally does not record `low_degree_power_template` because the candidate is not shorter than the existing compiler output.
- Code review findings were fixed: symbolic integer exponents now return `unsupported_power` diagnostics instead of leaking `TypeError`, and motif-search records count evaluated residual samples.

## Notes

- The warning is the existing high-noise overflow warning in the warm-start failure-mechanism test.
