---
phase: 37-compiler-macro-shortening-and-warm-start-coverage
verified: 2026-04-16T11:58:05Z
status: passed
score: 4/4 must-haves verified
score_verified: 4
score_total: 4
overrides_applied: 0
requirements:
  - id: COMP-01
    status: satisfied
    evidence: "The compiler now exposes an explicit macro layer with `scaled_exp_minus_one_template` and `direct_division_template` before generic lowering."
  - id: COMP-02
    status: satisfied
    evidence: "Compiler metadata and relaxed diagnostics now report macro hits, misses, baseline depth/node counts, and depth/node deltas."
  - id: COMP-03
    status: satisfied
    evidence: "Shockley is recovered through the shipped warm-start path at the new defaults, while Michaelis-Menten and Planck remain fail-closed at the compile gate with relaxed diagnostics preserved."
---

# Phase 37: Compiler Macro Shortening and Warm-Start Coverage Verification Report

**Phase Goal:** Users can warm-start more formulas from shorter exact EML trees without loosening compiler correctness guarantees.
**Verified:** 2026-04-16T11:58:05Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Compiler shortcuts are explicit, traceable macro rules rather than hidden special cases. | VERIFIED | `CompilerConfig.enable_macros`, `CompileMetadata.macro_diagnostics`, and `MACRO_RULES` now make the shortcut layer explicit and serialized. |
| 2 | Macro diagnostics show real shortening wins against the old generic compiler path. | VERIFIED | Shockley reports a positive `scaled_exp_minus_one_template` depth/node delta, Michaelis-Menten reports a positive `direct_division_template` delta, and Planck reports both macros with positive deltas in relaxed diagnostics. |
| 3 | Shipped warm-start coverage expands for at least one previously depth-gated formula. | VERIFIED | `python -m eml_symbolic_regression.cli demo shockley --warm-start-eml --points 24` now returns `compiled_seed=recovered`, `warm_start_attempt=same_ast_return`, and `trained_exact_recovery=recovered` at the shipped defaults. |
| 4 | Unsupported formulas remain fail-closed even when relaxed diagnostics show a shorter exact tree. | VERIFIED | Michaelis-Menten and Planck keep `compiled_seed=unsupported` and `warm_start_attempt=unsupported` at the default compile gate while their relaxed compiler diagnostics remain available for inspection. |

**Score:** 4/4 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Compiler and CLI macro coverage | `python -m pytest tests/test_compiler_warm_start.py -q` | 15 passed, 1 expected numerical warning from overflow-heavy warm-start diagnostics | PASS |
| Benchmark runner Shockley coverage | `python -m pytest tests/test_benchmark_runner.py -q` | 20 passed, 3 expected numerical warnings from existing benchmark overflow probes | PASS |
| Suite and preset contract updates | `python -m pytest tests/test_campaign.py tests/test_benchmark_contract.py -q` | 60 passed | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| COMP-01 | Validated short-macro compiler library before generic lowering | SATISFIED | Explicit macro layer with `scaled_exp_minus_one_template` and `direct_division_template` |
| COMP-02 | Inspectable macro hit/miss and depth/node delta diagnostics | SATISFIED | `macro_diagnostics` in compiler metadata, relaxed diagnostics, and CLI unsupported payloads |
| COMP-03 | Expanded warm-start coverage without weakening fail-closed behavior | SATISFIED | Shockley warm-start recovery at shipped defaults; Michaelis-Menten and Planck remain gated with diagnostics only |

## Gaps Summary

No Phase 37 gaps remain. Phase 38 still needs milestone-wide proof/campaign comparison, regression locks against archived baselines, and final regime-separated reporting.

---

_Verified: 2026-04-16T11:58:05Z_
_Verifier: Codex_
