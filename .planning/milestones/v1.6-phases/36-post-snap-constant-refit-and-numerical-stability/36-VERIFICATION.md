---
phase: 36-post-snap-constant-refit-and-numerical-stability
verified: 2026-04-16T11:24:38Z
status: passed
score: 4/4 must-haves verified
score_verified: 4
score_total: 4
overrides_applied: 0
requirements:
  - id: REFI-01
    status: satisfied
    evidence: "Exact Expr trees now expose stable constant paths and can rebuild frozen structures after literal-only refit."
  - id: REFI-02
    status: satisfied
    evidence: "Benchmark artifacts record pre-refit and post-refit candidates and accept post-refit only when verifier-owned ranking improves or matches the fallback."
  - id: STAB-01
    status: satisfied
    evidence: "Anomaly stats now distinguish exp overflow/clamp pressure from log small-magnitude, non-positive-real, branch-cut, and non-finite input stress."
  - id: STAB-02
    status: satisfied
    evidence: "Training configs can enable log-safety penalties without changing faithful post-snap verification semantics."
---

# Phase 36: Post-Snap Constant Refit and Numerical Stability Verification Report

**Phase Goal:** Users can improve structurally correct snapped candidates through post-snap coefficient refit while getting better training diagnostics for domain and numerical failures.
**Verified:** 2026-04-16T11:24:38Z
**Status:** passed

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Frozen exact trees can expose literal constants without changing discrete structure. | VERIFIED | `Expr.constant_occurrences()` and `Expr.with_constant_updates()` provide stable constant-path enumeration and exact-tree rebuilding. |
| 2 | Benchmark artifacts preserve both pre-refit and post-refit exact candidates with fallback-safe acceptance. | VERIFIED | Benchmark blind, warm-start, and perturbed-basin payloads now include a `refit` section with pre/post candidates, constant diffs, and the selected candidate decision. |
| 3 | Training diagnostics expose exp and log stress separately. | VERIFIED | `AnomalyStats` now records `exp_overflow_count`, `clamp_count`, `log_small_magnitude_count`, `log_non_positive_real_count`, `log_branch_cut_count`, and `log_non_finite_input_count`. |
| 4 | Optional log-safety controls are training-only. | VERIFIED | `TrainingSemanticsConfig` and `TrainingConfig` add log-safety penalties to training loss while `verify_candidate()` still evaluates canonical exact expressions. |

**Score:** 4/4 truths verified

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Phase 36 regression slice | `python -m pytest tests/test_semantics_expression.py tests/test_benchmark_runner.py tests/test_compiler_warm_start.py tests/test_basin_targets.py -q` | 48 passed, 4 expected numerical warnings from existing overflow-heavy diagnostics | PASS |

## Requirements Coverage

| Requirement | Description | Status | Evidence |
|-------------|-------------|--------|----------|
| REFI-01 | Frozen snapped trees expose literal constants for post-snap refit | SATISFIED | `expression.py` constant paths and override-aware torch evaluation |
| REFI-02 | Pre-refit and post-refit artifacts are preserved with fallback-safe acceptance | SATISFIED | `benchmark.py` `refit` payload and verifier-owned ranking comparison |
| STAB-01 | Training diagnostics expose exp/log domain and numerical failures clearly | SATISFIED | Expanded `AnomalyStats` plus metric extraction in benchmark artifacts |
| STAB-02 | Positive-domain-safe controls can be enabled during training without affecting faithful verification | SATISFIED | Training-only log-safety penalty flow through `TrainingConfig` and `TrainingSemanticsConfig` |

## Gaps Summary

No Phase 36 gaps remain. Compiler macro shortening, warm-start coverage expansion, and milestone-wide regression/evaluation lockdown remain Phase 37 and Phase 38 work.

---

_Verified: 2026-04-16T11:24:38Z_
_Verifier: Codex_
