---
phase: 35-snap-neighborhood-discrete-cleanup
plan: 01
subsystem: optimizer
tags: [cleanup, repair, beam-search, benchmark, fallback]
requires:
  - phase: 34
    provides: "Verifier-gated exact candidate pooling with selected/fallback provenance"
provides:
  - "Replayable low-margin slot alternatives and exact-AST-deduplicated neighborhood expansion"
  - "Target-free local cleanup over failed exact candidates"
  - "Blind, warm-start, and perturbed-basin repair artifacts with fallback preserved"
affects: [phase-36, phase-38, benchmark-artifacts]
tech-stack:
  added: []
  patterns: ["Fallback-preserving target-free cleanup driven by serialized slot alternatives"]
key-files:
  created:
    - .planning/phases/35-snap-neighborhood-discrete-cleanup/35-01-SUMMARY.md
    - .planning/phases/35-snap-neighborhood-discrete-cleanup/35-VERIFICATION.md
  modified:
    - src/eml_symbolic_regression/master_tree.py
    - src/eml_symbolic_regression/optimize.py
    - src/eml_symbolic_regression/repair.py
    - src/eml_symbolic_regression/benchmark.py
    - docs/IMPLEMENTATION.md
    - tests/test_master_tree.py
    - tests/test_repair.py
    - tests/test_benchmark_runner.py
key-decisions:
  - "Replayable slot alternatives are captured at candidate emission time so cleanup can run without the live soft model."
  - "Target-free cleanup promotes a repaired candidate only through verifier-owned ranking and leaves the original selected/fallback manifest untouched."
  - "Perturbed-basin runs try target-free cleanup first but retain the older target-aware repair path as fallback when generic cleanup has no usable neighborhood."
patterns-established:
  - "Exact-candidate manifests can serialize ambiguous slot alternatives for later discrete search."
  - "Benchmark artifacts can append repair reports without mutating the optimizer-selected candidate payload."
requirements-completed: [DISC-01, DISC-02, DISC-03, DISC-04]
duration: 27 min
completed: 2026-04-16
---

# Phase 35 Plan 01: Snap-Neighborhood Discrete Cleanup Summary

**Bounded target-free cleanup over low-margin exact candidates with fallback-preserving benchmark artifacts**

## Performance

- **Duration:** 27 min
- **Started:** 2026-04-16T10:23:15Z
- **Completed:** 2026-04-16T10:50:51Z
- **Tasks:** 3
- **Files modified:** 8

## Accomplishments

- Added replayable active-slot alternatives plus exact-AST-deduplicated snap-neighborhood expansion helpers in `master_tree.py`.
- Serialized slot alternatives into `ExactCandidate`, then used them to build a target-free cleanup stage in `repair.py`.
- Wired cleanup into blind, warm-start, and perturbed-basin benchmark flows while preserving the original selected/fallback candidate manifest and reporting repair provenance in artifacts.

## Task Commits

The implementation landed as one integrated commit because the cleanup contract crossed model replay, repair logic, benchmark artifacts, docs, and tests:

1. **Tasks 1-3: slot alternatives, cleanup integration, docs, and regression coverage** - `bd92f71` (feat)
2. **Phase context and execution plan** - `dce9692` (docs)

## Files Created/Modified

- `src/eml_symbolic_regression/master_tree.py` - replayable active-slot alternatives, slot-map replay helpers, and deduplicated neighborhood expansion.
- `src/eml_symbolic_regression/optimize.py` - exact candidates now retain serialized slot alternatives for later cleanup.
- `src/eml_symbolic_regression/repair.py` - target-free cleanup, richer repair provenance, and verifier-owned repair ranking.
- `src/eml_symbolic_regression/benchmark.py` - blind, warm-start, and perturbed-basin cleanup integration plus repair metrics extraction.
- `docs/IMPLEMENTATION.md` - cleanup-stage and fallback-preserving artifact notes.
- `tests/test_master_tree.py` - slot-alternative and neighborhood-dedup regression coverage.
- `tests/test_repair.py` - target-free cleanup regression coverage.
- `tests/test_benchmark_runner.py` - blind/warm artifact promotion and fallback-preservation coverage.

## Decisions Made

- Stored slot alternatives with each emitted exact candidate instead of reverse-engineering them later from a top-1 snap.
- Kept cleanup as a separate repair artifact so Phase 34 selected/fallback provenance remains auditable even when cleanup wins.
- Preserved the existing perturbed-tree repair as a fallback path so older basin-proof behavior still works when target-free cleanup has no usable neighborhood.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The benchmark runner slice remains relatively slow because repaired runs now verify extra neighborhood candidates in addition to the baseline selected candidate.
- The new neighborhood expansion test initially over-selected an unrelated low-margin slot; tightening the test to the intended two-slot neighborhood resolved the false failure.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 36 can now treat discrete structure as a stable, fallback-preserving substrate for post-snap constant refit and stronger numerical/domain controls.

No blocker remains for the next phase. The main tradeoff introduced here is more verifier work in benchmark slices when cleanup is attempted.

---
*Phase: 35-snap-neighborhood-discrete-cleanup*
*Completed: 2026-04-16*
