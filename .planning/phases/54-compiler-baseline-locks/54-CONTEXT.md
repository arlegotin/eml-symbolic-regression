---
phase: 54-compiler-baseline-locks
status: discussed
mode: autonomous-smart-discuss
created: 2026-04-18
requirements: [BASE-01, BASE-02, BASE-03, BASE-04, BASE-05]
---

# Phase 54 Context: Compiler Baseline Locks

## Goal

Lock archived compiler baselines for logistic, Planck, Michaelis-Menten, Arrhenius, and Shockley before introducing new motif behavior.

## Locked Defaults

- Default strict compiler gate remains `CompilerConfig(max_depth=13, max_nodes=256)`.
- Logistic currently strict-fails with `depth_exceeded`; relaxed diagnostics compile at depth `27`, node count `77`, and no macro hits.
- Planck currently strict-fails with `depth_exceeded`; relaxed diagnostics compile at depth `20`, node count `67`, and macro hits `scaled_exp_minus_one_template` plus `direct_division_template`.
- Michaelis-Menten currently strict-compiles at depth `12`, node count `41`, with `saturation_ratio_template`.
- Arrhenius currently strict-compiles at depth `7` with `direct_division_template`.
- Shockley currently strict-compiles with `scaled_exp_minus_one_template`.

## Implementation Decisions

- This phase is a test-only regression lock. No compiler behavior should change.
- Exact archived depths are asserted for logistic, Planck, and Michaelis-Menten because later phases claim improvement relative to these values.
- Existing supported wins must be asserted by macro hits, not just by successful compilation.
- Baseline tests should live in `tests/test_compiler_warm_start.py`, next to the current compiler and warm-start macro tests.
- Use current demo definitions from `datasets.py`; do not create duplicate formula fixtures.

## Existing Code Insights

### Reusable Assets

- `diagnose_compile_expression()` already reports strict and relaxed diagnostics with metadata.
- `compile_and_validate()` already validates strict compile paths against sampled demo splits.
- `get_demo()` provides the logistic, Planck, Michaelis-Menten, Arrhenius, and Shockley symbolic candidates and domains.

### Established Patterns

- Compiler regression tests use `CompilerConfig(variables=(spec.variable,), max_depth=13, max_nodes=256)`.
- Demo split inputs come from `spec.make_splits(points=..., seed=0)`.
- Macro assertions inspect `metadata.macro_diagnostics["hits"]`.

### Integration Points

- Phase 55 and later motif changes will update these baseline locks only when a test intentionally changes from archived baseline to improved current behavior.

## Deferred Ideas

None. Phase 54 is intentionally limited to baseline tests.

## Threat Model

- **Regression masking**: Later motif changes could accidentally break existing wins unless this phase asserts exact macro hits and depths.
- **Claim drift**: Logistic or Planck improvement claims need explicit pre-change anchors.
- **Gate drift**: Tests must assert the shipped strict gate remains unchanged.
