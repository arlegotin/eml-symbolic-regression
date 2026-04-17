---
phase: 51-reciprocal-and-saturation-compiler-motifs
reviewed: 2026-04-17T14:20:34Z
depth: standard
files_reviewed: 11
files_reviewed_list:
  - src/eml_symbolic_regression/compiler.py
  - src/eml_symbolic_regression/benchmark.py
  - tests/test_compiler_warm_start.py
  - tests/test_benchmark_contract.py
  - tests/test_benchmark_runner.py
  - README.md
  - docs/IMPLEMENTATION.md
  - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/suite-result.json
  - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.json
  - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/aggregate.md
  - artifacts/campaigns/v1.9-michaelis-evidence/v1.9-michaelis-evidence/v1-9-michaelis-evidence-michaelis-warm-a67d8ccfb108.json
findings:
  critical: 0
  warning: 2
  info: 0
  total: 2
status: issues_found
---

# Phase 51: Code Review Report

**Reviewed:** 2026-04-17T14:20:34Z
**Depth:** standard
**Files Reviewed:** 11
**Status:** issues_found

## Summary

Reviewed the Phase 51 compiler motifs, focused Michaelis benchmark suite, runner tests, docs, and generated evidence artifacts. The implementation preserves the strict default gates (`CompilerConfig.max_depth == 13`, `max_nodes == 256`, benchmark `max_compile_depth == 13`, `max_compile_nodes == 256`), keeps the Michaelis suite focused to one warm-start case, and classifies the generated artifact as same-AST compiler warm-start evidence (`same_ast_return`, verifier `recovered`, evidence class `same_ast`) rather than blind discovery. Arrhenius still uses `direct_division_template`, and Planck remains stretch/unsupported under the warm-start gate.

The issues found are both in the new reusable unit-shift helper. They do not invalidate the checked Michaelis artifact path, but they are real compiler contract edge cases and should be fixed before relying on the motifs as general reusable compiler infrastructure.

Verification run:

```bash
PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py -q
```

Result: `103 passed, 4 warnings`.

## Warnings

### WR-01: Unit-shift helper bypasses constant policy and finite derived-constant checks

**File:** `src/eml_symbolic_regression/compiler.py:298`

**Issue:** `_build_unit_shift()` always emits `Const(np.exp(-match.offset))`. That derived literal is not validated against `CompilerConfig.constant_policy` and is not checked for finiteness. As a result, `compile_sympy_expression(1/(x + 1), CompilerConfig(constant_policy="basis_only", ...))` and `compile_sympy_expression(x/(x + 1), CompilerConfig(constant_policy="basis_only", ...))` currently succeed through the new macros while adding `0.36787944117144233` to the constant catalog, even though `basis_only` is documented and enforced elsewhere as allowing only literal `1`. A large finite offset can also synthesize `inf` via `np.exp(-offset)` before validation catches the resulting behavior.

This is a correctness and evidence-integrity issue: a basis-only compile can silently become a literal-constant compile through the new motif path.

**Fix:** Make the unit-shift builder fail closed or fall back to the generic compiler path unless the derived constant is finite and allowed by the configured constant policy.

```python
def _build_unit_shift(self, match: _UnitShift) -> Expr | None:
    derived = complex(np.exp(-match.offset))
    if not (np.isfinite(derived.real) and np.isfinite(derived.imag)):
        return None
    if self.config.constant_policy == "basis_only" and abs(derived - 1.0) > 1e-12:
        return None
    self.assumptions.append("unit shift x+b compiled as eml(log(x), exp(-b)) behind validation")
    return Eml(log_of(Var(match.variable)), Const(derived))
```

Then have `_compile_reciprocal_shift()` and `_compile_saturation_ratio()` return `None` when `_build_unit_shift()` returns `None`, so the ordinary compiler path enforces the policy. Add regression tests for `basis_only` inputs such as `1/(x + 1)` and `x/(x + 1)`, and for a large finite offset that would otherwise produce a non-finite derived constant.

### WR-02: Unit-shift matcher misses explicit unit-coefficient SymPy forms

**File:** `src/eml_symbolic_regression/compiler.py:283`

**Issue:** `_match_unit_shift()` only treats a term as the variable term when `isinstance(term, sp.Symbol)`. Structurally equivalent SymPy expressions such as `1.0*x + 0.5` produce a `Mul` term, not a bare `Symbol`, so the new `reciprocal_shift_template` and `saturation_ratio_template` do not fire. For example, the equivalent expression `2.0*x/(1.0*x + 0.5)` currently fails the strict gate with `depth_exceeded`, and the relaxed diagnostic falls back to `direct_division_template` instead of `saturation_ratio_template`.

This weakens the "reusable structural SymPy match" requirement: the motif works for the exact canonical `x + b` shape but misses a common unit-coefficient representation produced by floating-point SymPy expressions or normalization.

**Fix:** Decompose each non-numeric addend with `as_coeff_Mul()` and accept exactly unit coefficient forms while still rejecting non-unit shifts like `2*x + b`.

```python
def _match_unit_shift(self, expr: sp.Expr) -> _UnitShift | None:
    if not isinstance(expr, sp.Add):
        return None

    symbol_terms: list[sp.Symbol] = []
    numeric_terms: list[sp.Expr] = []
    for term in expr.args:
        if term.is_number:
            numeric_terms.append(term)
            continue
        coeff, rest = term.as_coeff_Mul()
        if isinstance(rest, sp.Symbol) and sp.simplify(coeff - 1) == 0:
            symbol_terms.append(rest)
            continue
        return None

    if len(symbol_terms) != 1 or len(numeric_terms) != 1:
        return None
    return _UnitShift(
        variable=self._variable_name(symbol_terms[0]),
        offset=self._constant_value(numeric_terms[0]),
    )
```

Add tests for `1/(1.0*x + 0.5)` and `2.0*x/(1.0*x + 0.5)` that assert the reciprocal-only case hits `reciprocal_shift_template` and the Michaelis-equivalent top-level ratio hits `saturation_ratio_template` within the unchanged strict gate.

---

_Reviewed: 2026-04-17T14:20:34Z_
_Reviewer: Codex (gsd-code-reviewer)_
_Depth: standard_
