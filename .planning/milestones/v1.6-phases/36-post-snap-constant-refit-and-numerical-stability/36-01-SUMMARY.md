---
phase: 36-post-snap-constant-refit-and-numerical-stability
plan: 01
subsystem: optimizer
tags: [refit, numerics, anomalies, benchmark, fallback]
requires:
  - phase: 35
    provides: "Fallback-preserving exact candidate and cleanup artifacts"
provides:
  - "Frozen exact-expression literal refit over snapped candidates"
  - "Fallback-preserving pre/post refit benchmark artifacts"
  - "Expanded exp/log anomaly diagnostics and training-only log-safety penalties"
affects: [phase-37, phase-38, benchmark-artifacts]
tech-stack:
  added: []
  patterns: ["Path-stable literal refit over exact ASTs with verifier-owned acceptance"]
key-files:
  created:
    - .planning/phases/36-post-snap-constant-refit-and-numerical-stability/36-01-SUMMARY.md
    - .planning/phases/36-post-snap-constant-refit-and-numerical-stability/36-VERIFICATION.md
  modified:
    - src/eml_symbolic_regression/expression.py
    - src/eml_symbolic_regression/semantics.py
    - src/eml_symbolic_regression/master_tree.py
    - src/eml_symbolic_regression/optimize.py
    - src/eml_symbolic_regression/benchmark.py
    - docs/IMPLEMENTATION.md
    - tests/test_semantics_expression.py
    - tests/test_benchmark_runner.py
key-decisions:
  - "Post-snap refit operates on frozen exact Expr trees, and originally real literal constants stay on the real axis during refit."
  - "Benchmark artifacts keep both pre-refit and post-refit candidates, and promotion is gated by the same verifier-owned ranking priorities used for exact candidate selection."
  - "Numerical controls remain training-only: anomaly stats expose exp/log stress and optional log-safety penalties without changing faithful post-snap verification semantics."
patterns-established:
  - "Exact AST leaves can expose stable constant paths for later numerical optimization without mutating discrete structure."
  - "Run artifacts can append refit and anomaly reports without overwriting the optimizer-selected selected/fallback candidate manifest."
requirements-completed: [REFI-01, REFI-02, STAB-01, STAB-02]
duration: not tracked
completed: 2026-04-16
---

# Phase 36 Plan 01: Post-Snap Constant Refit and Numerical Stability Summary

**Frozen exact-expression constant refit, fallback-preserving artifact wiring, and richer exp/log anomaly diagnostics**

## Performance

- **Duration:** not tracked
- **Completed:** 2026-04-16T11:24:38Z
- **Tasks:** 3
- **Files modified:** 8

## Accomplishments

- Added path-stable literal constant enumeration, override-aware exact-expression torch evaluation, and exact-tree rebuilding helpers so snapped candidates can be refit without changing discrete structure.
- Expanded anomaly stats to distinguish `exp` clamp/overflow pressure from `log` small-magnitude, non-positive-real, branch-cut, and non-finite input stress, plus optional training-only log-safety penalties.
- Wired benchmark blind, warm-start, and perturbed-basin flows to preserve pre-refit and post-refit candidates, keep fallback semantics intact, and surface refit/anomaly metadata in run metrics and docs.

## Files Created/Modified

- `src/eml_symbolic_regression/expression.py` - stable constant-path enumeration, exact-tree rebuilding, and override-aware exact torch evaluation.
- `src/eml_symbolic_regression/semantics.py` - richer anomaly counters, training penalty tracking, and optional log-safety controls.
- `src/eml_symbolic_regression/master_tree.py` - training semantics config plumbing for anomaly-aware forward passes.
- `src/eml_symbolic_regression/optimize.py` - training config support for numerical controls and refit settings.
- `src/eml_symbolic_regression/benchmark.py` - post-snap refit execution, artifact serialization, and run metric extraction.
- `docs/IMPLEMENTATION.md` - refit and anomaly-reporting contract updates.
- `tests/test_semantics_expression.py` - constant-path and anomaly-telemetry regression coverage.
- `tests/test_benchmark_runner.py` - post-snap refit artifact and literal-update regression coverage.

## Decisions Made

- Kept real literals real during refit to avoid spurious tiny imaginary coefficients in ordinary real-domain demos.
- Reused verifier-owned ranking priorities for refit acceptance instead of inventing a separate promotion rule.
- Surfaced anomaly diagnostics from both soft training and exact-expression refit through the existing benchmark artifact path.

## Deviations from Plan

- The old plan named `tests/test_semantics.py`, but the active repo test surface is `tests/test_semantics_expression.py`; phase verification was anchored to the current file layout instead of the stale plan reference.

## Issues Encountered

- A first pass at refit allowed real literals to drift into tiny complex coefficients, which weakened verifier outcomes on real-valued demos. Constraining originally real literals to real-only parameters resolved that issue while preserving complex support where needed.

## User Setup Required

None.

## Next Phase Readiness

Phase 37 can now build compiler shortcuts against a stronger post-snap pipeline: exact candidates already preserve fallback provenance, cleanup can rescue discrete near misses, and refit/anomaly metadata is available for warm-start and campaign diagnostics.

---
*Phase: 36-post-snap-constant-refit-and-numerical-stability*
*Completed: 2026-04-16*
