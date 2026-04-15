---
phase: 26-warm-start-perturbation-robustness
plan: 01
subsystem: warm-start
tags: [warm-start, perturbation, diagnostics, campaigns]
requires:
  - phase: 24
    provides: Beer-Lambert high-perturbation failure baseline
provides:
  - Warm-start diagnosis block in manifests
  - Campaign CSV column for warm-start mechanism
affects: [phase-28]
tech-stack:
  added: []
  patterns: [failure mechanism diagnosis, metric propagation]
key-files:
  created: []
  modified:
    - src/eml_symbolic_regression/warm_start.py
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/campaign.py
    - tests/test_compiler_warm_start.py
    - tests/test_campaign.py
key-decisions:
  - "High-noise failures are explained as mechanisms instead of falling back to the compiled seed."
  - "Warm-start statuses remain unchanged and verifier-owned."
patterns-established:
  - "Warm-start manifest diagnosis fields propagate into benchmark metrics and campaign CSVs."
requirements-completed: [PERT-01, PERT-02, PERT-03, PERT-04]
duration: 30 min
completed: 2026-04-15
---

# Phase 26 Plan 01: Warm-Start Perturbation Summary

**Warm-start failure mechanisms surfaced from perturbation manifests into benchmark and campaign artifacts**

## Performance

- **Duration:** 30 min
- **Started:** 2026-04-15T15:15:00Z
- **Completed:** 2026-04-15T15:45:00Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added a `diagnosis` block to warm-start manifests with status, mechanism, active/changed slot counts, snap margin, losses, and verifier status.
- Added conservative mechanism labels including `active_slot_perturbation`, `snap_instability`, `non_finite_snap`, `verifier_mismatch`, `soft_fit_only`, and successful status labels.
- Propagated `warm_start_mechanism` into benchmark metrics and campaign `runs.csv`.
- Verified a filtered high-noise Beer-Lambert campaign reports `active_slot_perturbation` with changed slots and failed verifier status.

## Task Commits

1. **Phase context and plan** - `b6a94f4`
2. **Warm-start diagnosis implementation** - `a468285`

## Files Created/Modified

- `src/eml_symbolic_regression/warm_start.py` - manifest diagnosis and mechanism classification.
- `src/eml_symbolic_regression/benchmark.py` - metrics propagation.
- `src/eml_symbolic_regression/campaign.py` - CSV column.
- `tests/test_compiler_warm_start.py` - same-AST and high-noise diagnosis tests.
- `tests/test_campaign.py` - campaign CSV column coverage.

## Decisions Made

The phase deliberately narrows the failure mechanism instead of auto-recovering from the original compiled seed. This preserves the claim boundary: same-AST return must still come from the trained snapped tree, not from an unperturbed fallback.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 28 can group Beer-Lambert high-noise failures by `warm_start_mechanism`, and Phase 27 can proceed independently on compiler coverage.

---
*Phase: 26-warm-start-perturbation-robustness*
*Completed: 2026-04-15*
