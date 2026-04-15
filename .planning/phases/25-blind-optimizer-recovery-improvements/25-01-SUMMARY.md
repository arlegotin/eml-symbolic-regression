---
phase: 25-blind-optimizer-recovery-improvements
plan: 01
subsystem: optimizer
tags: [pytorch, optimizer, diagnostics, benchmarks]
requires:
  - phase: 24
    provides: locked v1.3 blind failure baselines
provides:
  - Generic paper-primitive scaffold attempts for blind training
  - Blind failure mechanism classifier
  - Blind baseline/candidate comparison helper
affects: [phase-28]
tech-stack:
  added: []
  patterns: [scaffold provenance, verifier-owned comparison]
key-files:
  created: []
  modified:
    - src/eml_symbolic_regression/optimize.py
    - src/eml_symbolic_regression/diagnostics.py
    - tests/test_optimizer_cleanup.py
    - tests/test_diagnostics.py
key-decisions:
  - "Scaffold attempts are generic paper primitives and are not formula-specific target injection."
  - "External initializer paths skip scaffolds so compiler warm starts remain isolated."
  - "Blind diagnostics classify remaining failures without changing recovery semantics."
patterns-established:
  - "Optimizer attempts record `attempt_kind`, `random_restart`, and initialization provenance."
requirements-completed: [BLIND-01, BLIND-02, BLIND-03, BLIND-04]
duration: 35 min
completed: 2026-04-15
---

# Phase 25 Plan 01: Blind Optimizer Improvements Summary

**Generic `exp`/`log` primitive scaffolds for blind training plus verifier-owned blind comparison diagnostics**

## Performance

- **Duration:** 35 min
- **Started:** 2026-04-15T14:40:00Z
- **Completed:** 2026-04-15T15:15:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added `TrainingConfig.scaffold_initializers`, defaulting to `("exp", "log")`.
- Added legal scaffold attempts for `exp(variable)` and `log(variable)` when no external initializer is supplied.
- Preserved random restart seed behavior and warm-start/custom initializer isolation.
- Added `classify_blind_failure` and `compare_blind_runs` to compare baseline/candidate blind rows using verifier-owned statuses.
- Verified a real CLI smoke campaign for `exp-blind` now recovers with `scaffold_exp` manifest provenance.

## Task Commits

1. **Phase context and plan** - `954ec1b`
2. **Optimizer scaffolds and diagnostics** - `4814455`

## Files Created/Modified

- `src/eml_symbolic_regression/optimize.py` - scaffold-aware training attempts.
- `src/eml_symbolic_regression/diagnostics.py` - blind failure classifier and comparison helper.
- `tests/test_optimizer_cleanup.py` - scaffold recovery and initializer isolation tests.
- `tests/test_diagnostics.py` - blind classifier and delta comparison tests.

## Decisions Made

The selected default improves shallow blind behavior by trying paper primitives generically. It does not inject target formulas or constants, and it does not alter `verify_candidate` or `claim_status` promotion rules.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

One test initially assumed every restart log had an initialization object. Random restarts intentionally keep `initialization: None`, so the test was corrected to handle that manifest shape.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 26 can proceed independently. Phase 28 should expect `exp` and `log` blind rows to improve where the generic scaffold exactly matches a paper primitive; radioactive decay may remain a blind failure because its literal coefficient is still not provided to the blind terminal bank.

---
*Phase: 25-blind-optimizer-recovery-improvements*
*Completed: 2026-04-15*
