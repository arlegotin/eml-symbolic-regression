---
phase: 51-reciprocal-and-saturation-compiler-motifs
fixed_at: 2026-04-17T14:30:56Z
review_path: .planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-REVIEW.md
iteration: 1
findings_in_scope: 2
fixed: 2
skipped: 0
status: all_fixed
---

# Phase 51: Code Review Fix Report

**Fixed at:** 2026-04-17T14:30:56Z
**Source review:** `.planning/phases/51-reciprocal-and-saturation-compiler-motifs/51-REVIEW.md`
**Iteration:** 1

**Summary:**
- Findings in scope: 2
- Fixed: 2
- Skipped: 0

## Fixed Issues

### WR-01: Unit-shift helper bypasses constant policy and finite derived-constant checks

**Files modified:** `src/eml_symbolic_regression/compiler.py`, `tests/test_compiler_warm_start.py`
**Commit:** 28fac17
**Applied fix:** `_build_unit_shift()` now derives `exp(-offset)` under suppressed NumPy overflow warnings, rejects non-finite derived constants, rejects basis-only derived constants other than `1`, and returns `None` so reciprocal/saturation callers fall back to the ordinary compiler path. Added regressions for `basis_only` smuggling through `1/(x+1)` and `x/(x+1)`, plus a large negative offset that previously produced an infinite derived constant.

### WR-02: Unit-shift matcher misses explicit unit-coefficient SymPy forms

**Files modified:** `src/eml_symbolic_regression/compiler.py`, `tests/test_compiler_warm_start.py`
**Commit:** e00dc15
**Applied fix:** `_match_unit_shift()` now decomposes non-numeric addends with `as_coeff_Mul()` and accepts only symbol terms whose coefficient simplifies exactly to `1`. Added regressions for `1/(1.0*x + 0.5)` and `2.0*x/(1.0*x + 0.5)` hitting the reciprocal and saturation templates, and for non-unit denominator forms avoiding those templates.

## Verification

**Per-fix checks:**
- WR-01: `python -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ('src/eml_symbolic_regression/compiler.py', 'tests/test_compiler_warm_start.py')]"` passed.
- WR-01: `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_unit_shift_macros_do_not_smuggle_basis_only_constants tests/test_compiler_warm_start.py::test_unit_shift_macro_rejects_nonfinite_derived_constant tests/test_compiler_warm_start.py::test_compile_reciprocal_shift_uses_template tests/test_compiler_warm_start.py::test_compile_michaelis_uses_saturation_ratio_template -q` passed with `4 passed`.
- WR-02: `python -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ('src/eml_symbolic_regression/compiler.py', 'tests/test_compiler_warm_start.py')]"` passed.
- WR-02: `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py::test_explicit_unit_coefficient_reciprocal_shift_uses_template tests/test_compiler_warm_start.py::test_explicit_unit_coefficient_saturation_ratio_uses_template tests/test_compiler_warm_start.py::test_non_unit_coefficient_shift_does_not_use_unit_shift_templates tests/test_compiler_warm_start.py::test_compile_reciprocal_shift_uses_template tests/test_compiler_warm_start.py::test_compile_michaelis_uses_saturation_ratio_template tests/test_compiler_warm_start.py::test_compile_arrhenius_uses_direct_division_template tests/test_compiler_warm_start.py::test_compiler_diagnostics_include_relaxed_depth_metadata -q` passed with `7 passed`.

**Focused Phase 51 suite:**
- `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py -q`
- Result: `108 passed, 4 warnings in 257.19s`.
- Warnings were pre-existing numerical overflow warnings in `semantics.py` and `verify.py` during stress/benchmark paths.

## Skipped Issues

None.

---

_Fixed: 2026-04-17T14:30:56Z_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
