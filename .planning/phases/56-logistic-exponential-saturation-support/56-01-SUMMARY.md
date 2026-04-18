---
phase: 56-logistic-exponential-saturation-support
plan: 01
subsystem: compiler
tags: [sympy, eml, logistic, macro-diagnostics, pytest]
requirements-completed: [MOTIF-02, LOGI-01, LOGI-02, LOGI-03]
requirements-deferred: [LOGI-04, LOGI-05]
duration: 9min
completed: 2026-04-18
---

# Phase 56 Plan 01: Logistic Exponential-Saturation Support Summary

## Accomplishments

- Added reusable `exponential_saturation_template` for direct `1/(1+c*exp(a))` structures.
- Added support for equivalent ratio structures such as `exp(a)/(exp(a)+c)` and equal-scale variants such as `k*exp(a)/(k*exp(a)+c)` through the same template.
- Reduced logistic relaxed compile depth from archived `27` to `15`, with node count from `77` to `49`.
- Added macro diagnostics showing baseline depth/node count, deltas, macro hit, and validation status.
- Preserved honest strict status: logistic remains unsupported under the unchanged `max_depth=13` strict gate, so warm-start was not attempted or promoted.

## Files Modified

- `src/eml_symbolic_regression/compiler.py` - Added the structural exponential-saturation matcher and exact EML builder.
- `tests/test_compiler_warm_start.py` - Updated logistic baseline lock into an improvement regression and added equivalent-shape coverage.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_compile_logistic_uses_exponential_saturation_template tests/test_compiler_warm_start.py::test_exponential_saturation_template_supports_equivalent_ratio_shape tests/test_compiler_warm_start.py::test_exponential_saturation_template_normalizes_equal_scale_ratio_shape tests/test_compiler_warm_start.py::test_compile_planck_archived_relaxed_baseline tests/test_compiler_warm_start.py::test_existing_macro_supported_demos_do_not_regress -q` -> `5 passed`
- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py -q` -> `33 passed, 1 warning`

## Decisions Made

- Logistic was not promoted to strict support because the exact EML tree is still depth `15`, above the shipped strict gate `13`.
- Logistic warm-start requirements `LOGI-04` and `LOGI-05` remain deferred until strict support exists; Phase 58 should record this as compile diagnostic evidence, not recovery evidence.
- The template does not branch on demo name or exact constants; it matches symbolic exponential-saturation structure.

## Notes

- The warning is the existing high-noise overflow warning in the warm-start failure-mechanism test.
- The macro uses validation to guard the branch-sensitive identity behind `1/(1+c*exp(a))`.
