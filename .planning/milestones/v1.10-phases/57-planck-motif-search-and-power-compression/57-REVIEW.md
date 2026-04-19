---
phase: 57-planck-motif-search-and-power-compression
reviewed: 2026-04-18T11:24:55Z
depth: quick
files_reviewed: 3
files_reviewed_list:
  - src/eml_symbolic_regression/compiler.py
  - src/eml_symbolic_regression/motif_search.py
  - tests/test_compiler_warm_start.py
findings:
  critical: 0
  warning: 1
  info: 1
  total: 2
status: issues_found
---

# Phase 57: Code Review Report

**Reviewed:** 2026-04-18T11:24:55Z
**Depth:** quick
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Quick review covered the requested Phase 57 files with the configured grep-style checks plus targeted scans around `low_degree_power_template`, validation-backed motif records, square no-regression behavior, and Planck unsupported reporting. No hardcoded secrets, dangerous calls, debug artifacts, empty catches, or commented-out code patterns were found.

One crash path was found in power handling, and one motif-record metadata issue can weaken validation evidence.

## Warnings

### WR-01: Symbolic Integer Powers Can Crash Instead Of Returning Unsupported Diagnostics

**File:** `src/eml_symbolic_regression/compiler.py:535`
**Issue:** `_compile_low_degree_power` checks `exponent.is_integer` and then immediately calls `int(exponent)`. In SymPy, an assumption-qualified symbol such as `n = Symbol("n", integer=True)` has `is_integer == True` but cannot be converted with `int(n)`. Compiling or diagnosing `x**n` therefore raises a raw `TypeError` instead of returning `None` from the macro path and eventually reporting `CompileReason.UNSUPPORTED_POWER`. The same guard pattern exists in `_compile_power`, so both paths should reject non-literal integer exponents before conversion.
**Fix:**
```python
def _compile_low_degree_power(self, expr: sp.Pow) -> Expr | None:
    base, exponent = expr.args
    if not exponent.is_Integer:
        return None
    power = int(exponent)
    ...

def _compile_power(self, expr: sp.Pow) -> Expr:
    base, exponent = expr.args
    if not exponent.is_Integer:
        raise UnsupportedExpression(CompileReason.UNSUPPORTED_POWER, expr, "only literal integer powers are supported")
    power = int(exponent)
    ...
```

## Info

### IN-01: Motif Record Sample Count Can Misreport Broadcast Or Constant Validations

**File:** `src/eml_symbolic_regression/motif_search.py:76`
**Issue:** `validate_motif_candidate` records `sample_count` from `values[0].size`. That is accurate for the current one-variable tests, but it misreports validation evidence for constant motifs, scalar-first multi-variable inputs, or broadcasted input shapes. Since these records are meant to back motif-search claims, `sample_count` should reflect the evaluated residual shape.
**Fix:** Compute it from the validation result:
```python
sample_count=int(np.size(residual))
```

---

_Reviewed: 2026-04-18T11:24:55Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: quick_
