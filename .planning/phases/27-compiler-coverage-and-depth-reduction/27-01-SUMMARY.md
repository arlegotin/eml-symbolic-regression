---
phase: 27-compiler-coverage-and-depth-reduction
plan: 01
subsystem: compiler
tags: [sympy, compiler, diagnostics, benchmarks]
requires:
  - phase: 24
    provides: compiler/depth-gate baseline diagnostics
provides:
  - Compiler diagnostic payloads for unsupported paths
  - Lower-depth Shockley compile template
affects: [phase-28]
tech-stack:
  added: []
  patterns: [fail-closed diagnostics, validated lower-depth templates]
key-files:
  created: []
  modified:
    - src/eml_symbolic_regression/compiler.py
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_compiler_warm_start.py
    - tests/test_benchmark_runner.py
key-decisions:
  - "Shockley is the first compiler coverage improvement target because `c*exp(a)-c` has a safe lower-depth EML template."
  - "Damped oscillator `cos` support is explicitly deferred with structured diagnostics."
patterns-established:
  - "Unsupported benchmark compile payloads now include strict error plus relaxed diagnostic metadata when available."
requirements-completed: [COV-01, COV-02, COV-03, COV-04]
duration: 40 min
completed: 2026-04-15
---

# Phase 27 Plan 01: Compiler Coverage Summary

**Compiler diagnostics plus a validated lower-depth Shockley EML template**

## Performance

- **Duration:** 40 min
- **Started:** 2026-04-15T15:45:00Z
- **Completed:** 2026-04-15T16:25:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added `diagnose_compile_expression`, which reports strict unsupported details and relaxed compile metadata/validation when possible.
- Added diagnostic payloads to benchmark compile failures.
- Added a lower-depth `scaled_exp_minus_one_template` for expressions of the form `c*exp(a)-c`.
- Raised default compile depth gates from 12 to 13 so the new Shockley candidate is accepted while deeper formulas remain gated.
- Verified Shockley now compiles to a depth-13, node-35 exact EML AST and passes verifier checks through the real campaign path.

## Task Commits

1. **Phase context and plan** - `dcf1766`
2. **Compiler diagnostics and Shockley template** - `d536cf7`

## Files Created/Modified

- `src/eml_symbolic_regression/compiler.py` - diagnostics helper and lower-depth template.
- `src/eml_symbolic_regression/benchmark.py` - default depth gate and unsupported diagnostic payloads.
- `tests/test_compiler_warm_start.py` - Shockley, Planck diagnostic, and damped oscillator tests.
- `tests/test_benchmark_runner.py` - benchmark path tests for Shockley and unsupported diagnostics.

## Decisions Made

The compiler still fails closed. Shockley moved to verified compiled coverage only because the exact candidate validates against ordinary SymPy evaluation. Damped oscillator remains unsupported because `cos` is outside the current compiler subset.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 28 can compare v1.4 standard/showcase campaigns against v1.3 and should show Shockley moving from unsupported to verified recovered.

---
*Phase: 27-compiler-coverage-and-depth-reduction*
*Completed: 2026-04-15*
