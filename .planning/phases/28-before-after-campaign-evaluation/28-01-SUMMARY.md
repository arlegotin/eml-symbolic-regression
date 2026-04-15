---
phase: 28-before-after-campaign-evaluation
plan: 01
subsystem: diagnostics
tags: [campaigns, comparison, evidence, reports]
requires:
  - phase: 25
    provides: blind optimizer scaffold improvements
  - phase: 26
    provides: warm-start perturbation diagnostics
  - phase: 27
    provides: compiler coverage improvements
provides:
  - v1.4 standard/showcase campaign evidence
  - Before/after comparison report against v1.3 baselines
  - Reproducible diagnostics comparison command
affects: [milestone-audit]
tech-stack:
  added: []
  patterns: [campaign evidence bundles, generated comparison reports]
key-files:
  created:
    - artifacts/campaigns/v1.4-standard/
    - artifacts/campaigns/v1.4-showcase/
    - artifacts/campaigns/v1.4-comparison/
  modified:
    - src/eml_symbolic_regression/diagnostics.py
    - src/eml_symbolic_regression/cli.py
    - tests/test_diagnostics.py
    - tests/test_benchmark_reports.py
    - README.md
key-decisions:
  - "The comparison report uses verifier-owned recovery, unsupported rate, failure rate, losses, and runtime deltas without redefining `recovered`."
  - "Target categories are explicit: blind recovery, Beer-Lambert perturbation, and compiler coverage."
patterns-established:
  - "Campaign directory pairs can be compared with a single `diagnostics compare` command that writes JSON and Markdown."
requirements-completed: [EVAL-01, EVAL-02, EVAL-03, EVAL-04, EVAL-05]
duration: 55 min
completed: 2026-04-15
---

# Phase 28 Plan 01: Before/After Campaign Evaluation Summary

**v1.4 campaign evidence and before/after comparison against v1.3**

## Performance

- **Duration:** 55 min
- **Started:** 2026-04-15T16:25:00Z
- **Completed:** 2026-04-15T16:55:00Z
- **Tasks:** 2
- **Files modified:** 5 source/docs/test files plus generated campaign artifacts

## Accomplishments

- Added `diagnostics compare`, backed by `build_campaign_comparison` and `write_campaign_comparison`, to compare baseline/candidate campaign directory pairs.
- Generated committed v1.4 standard and showcase campaign bundles.
- Generated `artifacts/campaigns/v1.4-comparison/`, with machine-readable JSON and a Markdown report.
- Documented the one-command comparison flow in `README.md`.
- Updated the smoke benchmark aggregate test to reflect that the blind `exp` smoke case now recovers instead of failing.

## Before/After Result

| Category | Verdict | Baseline Recovery | v1.4 Recovery | Unsupported | Failed |
|----------|---------|-------------------|---------------|-------------|--------|
| overall | improved | 18/45 | 27/45 | 9 -> 7 | 18 -> 11 |
| blind_recovery | improved | 3/15 | 10/15 | 0 -> 0 | 12 -> 5 |
| beer_perturbation | unchanged | 15/21 | 15/21 | 0 -> 0 | 6 -> 6 |
| compiler_coverage | improved | 0/9 | 2/9 | 9 -> 7 | 0 -> 0 |

## Task Commits

1. **Phase context and plan** - `5fae1ae`
2. **Campaign comparison code and docs** - `09a3989`
3. **Smoke aggregate test update** - `d94466d`
4. **v1.4 campaign evidence** - `cfe8cbb`

## Files Created/Modified

- `src/eml_symbolic_regression/diagnostics.py` - comparison metrics, verdicts, JSON/Markdown writers.
- `src/eml_symbolic_regression/cli.py` - `diagnostics compare` command.
- `tests/test_diagnostics.py` - comparison behavior coverage.
- `tests/test_benchmark_reports.py` - smoke aggregate expectation for improved blind recovery.
- `README.md` - documented comparison command.
- `artifacts/campaigns/v1.4-standard/` - standard campaign evidence.
- `artifacts/campaigns/v1.4-showcase/` - showcase campaign evidence.
- `artifacts/campaigns/v1.4-comparison/` - before/after comparison evidence.

## Decisions Made

Comparison verdicts are based on recovery, unsupported, and failure rate movement. Loss and runtime deltas are supporting diagnostics and do not redefine verifier-owned recovery.

## Deviations from Plan

The full test suite surfaced a stale smoke aggregate expectation because the blind `exp` smoke run now recovers. The implementation was correct, so the test was updated to assert the improved outcome explicitly.

## Issues Encountered

None blocking.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

All v1.4 phases are complete. The milestone is ready for audit.

---
*Phase: 28-before-after-campaign-evaluation*
*Completed: 2026-04-15*
