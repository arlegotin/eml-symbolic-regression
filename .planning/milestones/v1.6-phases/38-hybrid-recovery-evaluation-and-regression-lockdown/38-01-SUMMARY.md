---
phase: 38-hybrid-recovery-evaluation-and-regression-lockdown
plan: 01
subsystem: reporting
tags: [evaluation, reporting, diagnostics, proof, regression]
requires:
  - phase: 34
    provides: "Fallback-safe exact candidate metadata"
  - phase: 35
    provides: "Repair artifacts and taxonomy-preserving run status"
  - phase: 36
    provides: "Refit artifacts and anomaly-rich benchmark metrics"
  - phase: 37
    provides: "Macro-aware compiler diagnostics and expanded Shockley warm-start coverage"
provides:
  - "Explicit regime summaries in campaign and proof reports"
  - "Version-agnostic comparison artifacts with immutable anchor locks"
  - "Regression tests that lock hybrid selection, fallback, and refit reporting fields"
affects: [milestone-audit, reporting-contract, archived-comparisons]
tech-stack:
  added: []
  patterns: ["Hash-locked comparison anchors", "Report-level regime separation backed by aggregate metadata"]
key-files:
  created:
    - .planning/phases/38-hybrid-recovery-evaluation-and-regression-lockdown/38-01-SUMMARY.md
    - .planning/phases/38-hybrid-recovery-evaluation-and-regression-lockdown/38-VERIFICATION.md
    - .planning/v1.6-MILESTONE-AUDIT.md
  modified:
    - src/eml_symbolic_regression/campaign.py
    - src/eml_symbolic_regression/diagnostics.py
    - src/eml_symbolic_regression/proof_campaign.py
    - src/eml_symbolic_regression/cli.py
    - README.md
    - tests/test_proof_campaign.py
    - tests/test_diagnostics.py
    - tests/test_benchmark_reports.py
    - tests/test_campaign.py
key-decisions:
  - "Measured proof thresholds keep the verdict `reported` instead of being collapsed into bounded pass/fail language."
  - "Comparison outputs and proof bundles carry explicit file-hash lock manifests so archived anchors can be audited later."
  - "Hybrid-stage regression locks live at the aggregate/reporting layer, not only in low-level benchmark runner tests."
patterns-established:
  - "Campaign and proof reports now summarize regimes explicitly before narrative interpretation."
  - "Version-agnostic comparison tooling uses the provided directories as source-of-truth instead of hardcoded milestone names."
requirements-completed: [EVAL-01, EVAL-02, EVAL-03, EVAL-04]
duration: not tracked
completed: 2026-04-16
---

# Phase 38 Plan 01: Hybrid Recovery Evaluation and Regression Lockdown Summary

**Regime-aware reporting, immutable comparison anchors, and aggregate-level hybrid regression locks**

## Performance

- **Duration:** not tracked
- **Completed:** 2026-04-16T12:14:20Z
- **Tasks:** 3
- **Files modified:** 9

## Accomplishments

- Added explicit regime summary sections to campaign and proof reports so blind, warm-start, compile-only, catalog, and perturbed-basin evidence are separated at the top level.
- Generalized campaign-comparison output so it no longer assumes `v1.4` versus `v1.3`, and wrote immutable lock manifests for comparison anchors and proof-bundle archived roots.
- Added regression coverage that locks aggregate/report visibility for selected-candidate, fallback-candidate, and refit metadata used to audit weak-dominance behavior.

## Files Created/Modified

- `src/eml_symbolic_regression/campaign.py` - regime summary section in campaign reports.
- `src/eml_symbolic_regression/diagnostics.py` - generic comparison output, lock JSON emission, and anchor-lock markdown sections.
- `src/eml_symbolic_regression/proof_campaign.py` - regime summary, archived anchor locks, proof-bundle lock file, and corrected `reported` verdict handling.
- `src/eml_symbolic_regression/cli.py` - generic diagnostics wording and comparison output default path.
- `README.md` - updated comparison example and proof-bundle lock-manifest documentation.
- `tests/test_proof_campaign.py` - proof-bundle regime summary, anchor-lock, and `reported` verdict regression coverage.
- `tests/test_diagnostics.py` - comparison lock-manifest and generic markdown regression coverage.
- `tests/test_benchmark_reports.py` - aggregate run-row lock for selected/fallback/refit metrics.
- `tests/test_campaign.py` - campaign report regime summary regression coverage.

## Decisions Made

- Kept the actual empirical rerun step separate from the reporting infrastructure: Phase 38 ships the reporting contract and regression locks needed for honest v1.6 evaluation without claiming fresh experimental denominators in the same phase.
- Treated archived anchors as first-class evidence artifacts by hashing comparison inputs and proof-bundle baseline roots.
- Locked hybrid-stage metrics at the aggregate level because weak-dominance claims are only auditable if selected/fallback/refit metadata survives the reporting pipeline.

## Deviations from Plan

- The milestone close-out stopped after a passed audit and updated implementation state. Full archive/tagging was intentionally left as a follow-up because it rewrites the planning root and normally requires an explicit completion step.

## Issues Encountered

- The proof bundle mislabeled measured `reported` thresholds as `bounded`, which blurred measured boundary evidence with bounded proof claims. Correcting the verdict mapping and adding a regime summary table resolved that ambiguity.
- Campaign comparison tooling was already structurally generic, but the wording and default output path were still hardcoded to `v1.4` versus `v1.3`. The final patch generalized both and added lock manifests so later milestone comparisons remain auditable.

## User Setup Required

None.

## Next Phase Readiness

The implementation milestone is complete. The repo is ready for the explicit archive/tagging step that snapshots v1.6 into `.planning/milestones/` and starts the next milestone cleanly.

---
*Phase: 38-hybrid-recovery-evaluation-and-regression-lockdown*
*Completed: 2026-04-16*
