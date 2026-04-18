---
phase: 56-logistic-exponential-saturation-support
reviewed: 2026-04-18T11:11:49Z
depth: quick
files_reviewed: 2
files_reviewed_list:
  - src/eml_symbolic_regression/compiler.py
  - tests/test_compiler_warm_start.py
findings:
  critical: 0
  warning: 1
  info: 0
  total: 1
status: issues_found
---

# Phase 56: Code Review Report

**Reviewed:** 2026-04-18T11:11:49Z
**Depth:** quick
**Files Reviewed:** 2
**Status:** issues_found

## Summary

Quick review covered the Phase 56 compiler and warm-start test changes. The generic quick-depth scans found no hardcoded secrets, dangerous eval/exec usage, debug artifacts, or empty catches. The focused check found one exponential saturation matching gap: the new equivalent-ratio branch is still hardcoded to a unit-scaled exponential numerator and denominator, so an algebraically equivalent nonzero equal-scale ratio falls back to the deeper generic division path and remains strict-unsupported.

Targeted verification run: `python -m pytest tests/test_compiler_warm_start.py -q` passed with 32 tests and 1 existing runtime warning from overflow in `semantics.py`.

## Warnings

### WR-01: Equivalent Ratio Matching Hardcodes Unit Exponential Scale

**File:** `src/eml_symbolic_regression/compiler.py:431`

**Issue:** `_match_exponential_saturation()` only accepts the ratio form when the numerator exponential scale is exactly `1.0`, and `_match_exp_plus_constant()` also rejects denominator exponential scales other than `1.0`. This covers `exp(a)/(exp(a)+c)` but rejects `k*exp(a)/(k*exp(a)+c)` even though, for finite nonzero `k`, it is the same unit-saturation family: `1/(1+(c/k)*exp(-a))`. That is a formula/constant hardcoding risk in the new Phase 56 matcher. A quick probe with `2*exp(1.3*x)/(2*exp(1.3*x)+3)` produced strict `depth_exceeded` and relaxed `direct_division_template` instead of using `exponential_saturation_template`.

**Fix:** Preserve the denominator exponential scale from `_match_exp_plus_constant()`, require it to match the numerator scale for the unit-asymptote ratio case, and normalize the constant by that scale.

```python
def _match_exp_plus_constant(self, expr: sp.Expr) -> tuple[sp.Expr, complex, complex] | None:
    ...
    exp_scale, exponent = exp_terms[0]
    return exponent, exp_scale, constant_terms[0]

# In _match_exponential_saturation()
denominator_arg, denominator_scale, constant = denominator_match
if sp.simplify(numerator_arg - denominator_arg) != 0:
    return None
scale_delta = abs(numerator_scale - denominator_scale)
scale_limit = 1e-12 * max(1.0, abs(numerator_scale), abs(denominator_scale))
if scale_delta > scale_limit:
    return None
return _ExponentialSaturation(
    exponent=-denominator_arg,
    coefficient=constant / denominator_scale,
)
```

Add a regression test beside `test_exponential_saturation_template_supports_equivalent_ratio_shape()` for `2*exp(1.3*x)/(2*exp(1.3*x)+3)` and assert it hits `exponential_saturation_template` at the intended depth.

---

_Reviewed: 2026-04-18T11:11:49Z_
_Reviewer: Codex (gsd-code-reviewer)_
_Depth: quick_
