---
phase: 24-baseline-failure-triage-and-diagnostic-harness
plan: 01
subsystem: diagnostics
tags: [campaigns, diagnostics, benchmarks, cli]
requires:
  - phase: 23
    provides: committed v1.3 standard/showcase campaign evidence
provides:
  - Baseline triage reports for v1.3 standard/showcase failures
  - Perturbation-aware run filtering for diagnostic subsets
  - CLI commands for diagnostics triage and focused reruns
affects: [phase-25, phase-26, phase-27, phase-28]
tech-stack:
  added: []
  patterns: [json-first diagnostics, immutable baseline fingerprints, focused campaign filters]
key-files:
  created:
    - src/eml_symbolic_regression/diagnostics.py
    - tests/test_diagnostics.py
    - artifacts/diagnostics/v1.4-baseline/triage.json
    - artifacts/diagnostics/v1.4-baseline/triage.md
    - artifacts/diagnostics/v1.4-baseline/baseline-lock.json
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/campaign.py
    - src/eml_symbolic_regression/cli.py
key-decisions:
  - "Diagnostics reuse existing benchmark/campaign runners instead of creating a separate execution path."
  - "v1.3 baselines are locked by SHA-256 fingerprints and are not mutated."
  - "Beer-Lambert focused reruns use exact perturbation-noise filters."
patterns-established:
  - "Diagnostics reports write JSON plus Markdown plus a lock artifact."
  - "Focused rerun selection is derived from committed aggregate rows."
requirements-completed: [DIAG-01, DIAG-02, DIAG-03, DIAG-04]
duration: 45 min
completed: 2026-04-15
---

# Phase 24 Plan 01: Baseline Diagnostics Summary

**Baseline triage harness with immutable v1.3 fingerprints and focused diagnostic reruns**

## Performance

- **Duration:** 45 min
- **Started:** 2026-04-15T13:55:00Z
- **Completed:** 2026-04-15T14:40:00Z
- **Tasks:** 3
- **Files modified:** 8

## Accomplishments

- Added `RunFilter.perturbation_noises` and wired it through benchmark/campaign CLI filters and campaign reproduction commands.
- Added `diagnostics.py` to load committed campaigns, group failures, write triage artifacts, lock baseline fingerprints, and select focused diagnostic subsets.
- Generated actual v1.4 baseline triage artifacts from `v1.3-standard` and `v1.3-showcase`.
- Added tests covering report/lock output and exact Beer-Lambert perturbation filtering.

## Task Commits

1. **Phase context and plan** - `4f5bcf1`
2. **Diagnostics implementation** - `2cffd80`

## Files Created/Modified

- `src/eml_symbolic_regression/diagnostics.py` - baseline triage, run selection, lock generation, and focused rerun helpers.
- `src/eml_symbolic_regression/benchmark.py` - perturbation-noise-aware `RunFilter`.
- `src/eml_symbolic_regression/campaign.py` - manifest and reproduction command support for `--perturbation-noise`.
- `src/eml_symbolic_regression/cli.py` - diagnostics triage/rerun subcommands and noise filter flags.
- `tests/test_diagnostics.py` - targeted diagnostics tests.
- `artifacts/diagnostics/v1.4-baseline/*` - generated baseline triage and lock artifacts.

## Decisions Made

The diagnostic harness uses committed aggregate rows as the source of truth, then links back to raw run JSON for detailed audit. This keeps v1.3 evidence immutable while still making later v1.4 reruns easy to compare.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

The GSD commit helper could not write `.git/index.lock` under the sandbox, so direct approved `git add`/`git commit` commands were used for metadata and code commits.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 25 can use `artifacts/diagnostics/v1.4-baseline/triage.md` to target blind failures, especially `exp`, `log`, and `radioactive_decay`. Phase 26 can use the Beer-Lambert subset with exact 15.0/35.0 perturbation noise filters. Phase 27 can use the compiler/depth-gate subset.

---
*Phase: 24-baseline-failure-triage-and-diagnostic-harness*
*Completed: 2026-04-15*
