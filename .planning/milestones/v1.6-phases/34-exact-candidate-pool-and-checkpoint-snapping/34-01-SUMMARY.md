---
phase: 34-exact-candidate-pool-and-checkpoint-snapping
plan: 01
subsystem: optimizer
tags: [optimizer, verifier, candidate-pool, hardening, benchmark]
requires:
  - phase: 33
    provides: "Proof-era artifact discipline and the weak-dominance milestone direction"
provides:
  - "Late hardening checkpoint emission for soft EML training"
  - "Verifier-gated exact-candidate selection with explicit legacy fallback"
  - "Blind, warm-start, basin, and CLI artifact provenance for winner/fallback candidates"
affects: [phase-35, phase-36, phase-38, benchmark-artifacts]
tech-stack:
  added: []
  patterns: ["Verifier-gated exact candidate selection with serialized fallback provenance"]
key-files:
  created: []
  modified:
    - src/eml_symbolic_regression/optimize.py
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/cli.py
    - src/eml_symbolic_regression/warm_start.py
    - src/eml_symbolic_regression/basin.py
    - docs/IMPLEMENTATION.md
    - tests/test_optimizer_cleanup.py
    - tests/test_benchmark_runner.py
    - tests/test_verifier_demos_cli.py
key-decisions:
  - "Candidate pooling lives in `fit_eml_tree()` so blind, warm-start, and perturbed-basin flows share one exact-candidate selector."
  - "The legacy single-final-snap selector remains serialized as `fallback_candidate` for weak-dominance comparisons."
  - "Verifier-owned ranking uses extrapolation/high-precision/held-out error ahead of train post-snap loss and complexity."
patterns-established:
  - "Training manifests can expose both selected and legacy candidates without losing prior `best_restart` provenance."
  - "Higher-level training wrappers should reuse optimizer-selected verification rather than re-selecting their own final exact AST."
requirements-completed: [HARD-01, HARD-02, HARD-03, HARD-04]
duration: 17 min
completed: 2026-04-16
---

# Phase 34 Plan 01: Exact Candidate Pool and Checkpoint Snapping Summary

**Late-hardening candidate pooling with verifier-ranked exact selection and legacy fallback provenance across blind, warm-start, basin, and CLI flows**

## Performance

- **Duration:** 17 min
- **Started:** 2026-04-16T10:06:06Z
- **Completed:** 2026-04-16T10:23:15Z
- **Tasks:** 3
- **Files modified:** 9

## Accomplishments

- Added explicit late hardening checkpoints and a retained exact-candidate pool to `fit_eml_tree()`.
- Preserved the old soft-loss-only final snap as `fallback_candidate` while introducing verifier-gated exact-candidate selection.
- Surfaced selected/fallback provenance through benchmark metrics, CLI trained reports, and wrapper manifests, then locked the contract with regression tests.

## Task Commits

The implementation landed as one integrated commit because the selector contract crossed optimizer, wrapper, CLI, and test boundaries:

1. **Tasks 1-3: candidate pool, artifact wiring, and regression coverage** - `9556012` (feat)
2. **Phase context and execution plan** - `7188e3b` (docs)

## Files Created/Modified

- `src/eml_symbolic_regression/optimize.py` - late hardening checkpoint emission, candidate pooling, verifier-aware ranking, and legacy fallback serialization.
- `src/eml_symbolic_regression/benchmark.py` - optimizer budget extensions plus winner/fallback metrics extraction in run artifacts.
- `src/eml_symbolic_regression/cli.py` - demo-level hardening controls and trained-report selection provenance.
- `src/eml_symbolic_regression/warm_start.py` - reuse optimizer-selected verification in warm-start flows.
- `src/eml_symbolic_regression/basin.py` - reuse optimizer-selected verification in perturbed-basin flows.
- `docs/IMPLEMENTATION.md` - candidate-pool and verifier-gated selection contract notes.
- `tests/test_optimizer_cleanup.py` - candidate-pool and fallback provenance regression coverage.
- `tests/test_benchmark_runner.py` - blind benchmark artifact assertions for winner/fallback metadata.
- `tests/test_verifier_demos_cli.py` - CLI trained-report assertions for selection/fallback provenance.

## Decisions Made

- Kept `best_restart` as the legacy soft-loss provenance anchor while letting the shipped exact candidate come from a different restart/checkpoint.
- Stored candidate-pool selection data inside the existing optimizer manifest instead of inventing a disconnected side artifact.
- Let higher-level training wrappers consume `fit.verification` so the exact-candidate choice stays consistent across blind, warm-start, and basin paths.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- A stale `git` lock appeared after an overlapping add/commit attempt. The repository state was clean; rerunning the commit sequence sequentially resolved it.
- `tests/test_benchmark_runner.py` remains a relatively slow slice because verifier-owned candidate ranking now evaluates multiple emitted exact snaps instead of only one final snap.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 35 can now build bounded beam variants and target-free cleanup over serialized low-margin candidate data rather than starting from a single greedy snap.

No blocker remains for the next phase. The only notable cost increase is benchmark-runner runtime due to multi-candidate verification.

---
*Phase: 34-exact-candidate-pool-and-checkpoint-snapping*
*Completed: 2026-04-16*
