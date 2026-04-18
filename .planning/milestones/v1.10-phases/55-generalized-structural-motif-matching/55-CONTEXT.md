---
phase: 55-generalized-structural-motif-matching
status: discussed
mode: autonomous-smart-discuss
created: 2026-04-18
requirements: [MOTIF-01, MOTIF-05, MOTIF-06]
---

# Phase 55 Context: Generalized Structural Motif Matching

## Goal

Generalize reciprocal and saturation motif matching so it can operate on validated compilable subexpressions, not just raw variables, while preserving fail-closed behavior and diagnostic visibility.

## Locked Defaults

- No compiler support gate changes: default strict max depth remains `13` and max nodes remains `256`.
- Existing Phase 54 baseline locks must remain passing.
- Existing exact unit-shift behavior remains valid:
  - `1/(x+0.5)` -> `reciprocal_shift_template`, depth `10`, nodes `25`.
  - `2*x/(x+0.5)` -> `saturation_ratio_template`, depth `12`, nodes `41`.
- Non-unit shifted denominators such as `1/(2*x+0.5)` and `2*x/(2*x+0.5)` must not use the unit-shift templates.

## Implementation Decisions

- Replace the `_UnitShift` raw-variable assumption with a structural base-expression match for `g + b`, where `g` is one non-numeric term with coefficient `1`.
- Compile `g` through the normal compiler and then build `g+b` with the existing EML identity `eml(log(g), exp(-b))`, keeping branch safety behind validation.
- Generalize saturation matching to numerator `c*g` over denominator `g+b`; the numerator base and denominator base must be structurally equivalent.
- Do not call broad algebraic normalizers as the primary recognizer. Matching remains direct SymPy structure with small equivalence checks only between the numerator base and denominator base.
- Add macro diagnostic validation fields so validated macro paths are visibly distinct from unvalidated compile-only metadata.
- Rejected variants should fail closed by returning `None` from macro matchers or by raising the existing `UnsupportedExpression` reason from the normal compiler path.

## Existing Code Insights

### Reusable Assets

- `compiler.py` already has `_match_unit_shift`, `_build_unit_shift`, `_compile_reciprocal_shift`, and `_compile_saturation_ratio`.
- `_macro_diagnostics()` already reports hits, misses, baseline depth/node count, and depth/node deltas.
- `compile_and_validate()` is the correct place to stamp validated macro metadata because it owns the validation result.

### Established Patterns

- Macro rules are structural and validation-gated by tests calling `compile_and_validate()`.
- Tests assert macro hits exactly and use relaxed diagnostics for unsupported stretch cases.
- Fail-closed tests should inspect macro hits under relaxed compile when strict compile fails.

### Integration Points

- Phase 56 will build logistic exponential-saturation support on this generalized `g+b` capability.
- Phase 57 can reuse the same pattern for power-compressed Planck subexpressions.

## Deferred Ideas

- Do not add logistic-specific exponential-saturation macro logic in Phase 55. That belongs to Phase 56.
- Do not add generic power compression in Phase 55. That belongs to Phase 57.

## Threat Model

- **Overbroad matching**: A broad symbolic normalization could silently match unintended formulas. Mitigation: direct structural `g+b` and `c*g/(g+b)` only.
- **Branch errors**: `eml(log(g), exp(-b))` relies on principal branch behavior. Mitigation: accept through `compile_and_validate()` and fail closed on validation errors.
- **Regression**: Existing raw-variable motifs could change depth/node counts. Mitigation: keep Phase 54 and existing macro tests passing.
