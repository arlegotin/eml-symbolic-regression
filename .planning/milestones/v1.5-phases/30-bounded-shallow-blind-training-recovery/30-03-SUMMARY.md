---
phase: 30-bounded-shallow-blind-training-recovery
plan: 03
subsystem: benchmarking
tags: [eml, proof-suite, regression-tests, threshold-aggregation, diagnostics]

requires:
  - phase: 30-bounded-shallow-blind-training-recovery
    provides: Plan 30-01 proof suite contract and Plan 30-02 blind scaled-exponential recovery scaffolds
provides:
  - End-to-end full-suite shallow blind proof regression gate
  - Claim-specific threshold counting for paper-shallow-blind-recovery
  - Aggregate diagnostics guardrails for every proof run summary
affects: [30-bounded-shallow-blind-training-recovery, v1.5-shallow-proof, benchmark-aggregation]

tech-stack:
  added: []
  patterns:
    - Full proof-suite regression tests use module-scoped benchmark fixtures to avoid duplicate 18-run execution per pytest invocation
    - Shared bounded_100_percent policy remains unchanged while claim-specific counting enforces stricter shallow proof evidence

key-files:
  created:
    - tests/test_shallow_blind_proof_regression.py
    - .planning/phases/30-bounded-shallow-blind-training-recovery/30-03-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_benchmark_reports.py
    - tests/test_shallow_blind_proof_regression.py

key-decisions:
  - "paper-shallow-blind-recovery threshold summaries count only blind_training_recovered as passing evidence."
  - "The shared bounded_100_percent threshold policy was not loosened or redefined."
  - "The full v1.5-shallow-proof regression gate runs the declared suite without case or seed filters."

patterns-established:
  - "Proof regression tests inspect both in-memory aggregate rows and per-run JSON artifacts."
  - "Synthetic aggregate tests exercise non-blind evidence classes to keep SHAL-02 counting fail-closed."

requirements-completed: [SHAL-02, SHAL-03, SHAL-04]

duration: 1h 24m
completed: 2026-04-15
---

# Phase 30 Plan 03: Bounded Shallow Proof Regression Summary

**Full shallow blind proof regression gate with strict blind-only threshold counting and artifact diagnostics**

## Performance

- **Duration:** 1h 24m
- **Started:** 2026-04-15T15:26:00Z
- **Completed:** 2026-04-15T16:50:00Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added an end-to-end regression test that executes the full declared `v1.5-shallow-proof` suite without filters and asserts all 18 runs recover through `blind_training_recovered`.
- Added artifact checks that reject compile-only, catalog, warm-start, same-AST, and catalog-style verification payloads for the shallow proof gate.
- Added aggregate threshold assertions for `paper-shallow-blind-recovery`: 18 eligible, 18 passed, 0 failed, rate 1.0, evidence classes exactly `{"blind_training_recovered": 18}`.
- Added diagnostic checks requiring every aggregate run summary to expose best loss, post-snap loss, snap margin, active node count, scaffold source, and verifier status.
- Tightened `_threshold_summary()` so the shallow blind claim counts only `blind_training_recovered`, while leaving the shared `bounded_100_percent` policy definition intact.
- Added synthetic guardrails showing compile-only, catalog, compiler warm-start, repaired, verified-equivalent, same-AST, and soft-fit evidence fail the shallow bounded target when mixed into this claim.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add end-to-end bounded shallow proof regression**
   - `e01f146` test(30-03): add shallow blind proof regression gate
2. **Task 2: Tighten aggregate and diagnostic guardrails**
   - `54e7b91` test(30-03): add failing shallow threshold guardrails
   - `03d1799` feat(30-03): count only blind evidence for shallow proof

## Files Created/Modified

- `tests/test_shallow_blind_proof_regression.py` - Full `v1.5-shallow-proof` regression tests for declared runs, artifacts, aggregate threshold status, and diagnostics.
- `src/eml_symbolic_regression/benchmark.py` - Added a narrow claim-specific counted-evidence override for `paper-shallow-blind-recovery`.
- `tests/test_benchmark_reports.py` - Added synthetic shallow-claim aggregation guardrails for non-blind and non-proof evidence classes.
- `.planning/phases/30-bounded-shallow-blind-training-recovery/30-03-SUMMARY.md` - Plan outcome summary.

## Decisions Made

- Kept `threshold_policies()["bounded_100_percent"]` unchanged to preserve Phase 29 and future Phase 31 semantics.
- Scoped the stricter counting rule to `paper-shallow-blind-recovery` because D-01 requires this claim to count only proof-aware blind training.
- Used a module-scoped pytest fixture for the full proof suite so the two regression tests share one 18-run benchmark execution within a single pytest process.

## Deviations from Plan

### Auto-fixed Issues

None.

---

**Total deviations:** 0 auto-fixed.
**Impact on plan:** No scope creep; implementation stayed inside the plan-owned files.

## Issues Encountered

- The Task 1 TDD check did not produce a RED failure because Plans 30-01 and 30-02 had already made the full shallow proof suite recover. The test was still committed as the Task 1 regression gate after `python -m pytest tests/test_shallow_blind_proof_regression.py -q` passed.
- Runtime is substantial: every full `v1.5-shallow-proof` execution took roughly 19-22 minutes on this machine.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_shallow_blind_proof_regression.py -q` - 1 passed in 1170.72s (0:19:30).
- `python -m pytest tests/test_benchmark_reports.py::test_shallow_bounded_threshold_counts_only_blind_training_recovery -q` - RED check failed before the benchmark fix with `threshold["passed"] == 4`, expected `1`.
- `python -m pytest tests/test_benchmark_reports.py::test_shallow_bounded_threshold_counts_only_blind_training_recovery -q` - 1 passed in 0.91s after the benchmark fix.
- `python -m pytest tests/test_shallow_blind_proof_regression.py tests/test_benchmark_reports.py -q` - 9 passed in 1164.88s (0:19:24).
- `python -m pytest tests/test_shallow_scaled_exponential_contract.py tests/test_master_tree.py tests/test_optimizer_cleanup.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py tests/test_shallow_blind_proof_regression.py -q` - 66 passed, 6 existing `semantics.py:110` warnings in 1317.92s (0:21:57).
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.5-shallow-proof --output-dir /tmp/eml-phase30-proof-regression` - 18 runs, 0 unsupported, 0 failed.

## Proof CLI Artifact

- Suite result: `/tmp/eml-phase30-proof-regression/v1.5-shallow-proof/suite-result.json`
- Aggregate report: `/tmp/eml-phase30-proof-regression/v1.5-shallow-proof/aggregate.md`
- Aggregate JSON: `/tmp/eml-phase30-proof-regression/v1.5-shallow-proof/aggregate.json`
- Threshold row: `paper-shallow-blind-recovery`, policy `bounded_100_percent`, eligible 18, passed 18, failed 0, rate 1.0, status `passed`.
- Evidence classes: `{"blind_training_recovered": 18}`.

## Next Phase Readiness

Plan 30-03 is complete. The orchestrator can now update Phase 30 state, roadmap progress, and requirement status, then proceed to Phase 30 review/verification.

## Self-Check: PASSED

- Confirmed all plan-owned implementation and test files were modified.
- Confirmed the final worktree was clean before adding this summary.
- Confirmed `STATE.md`, `ROADMAP.md`, and requirements state were not updated by this executor run.

---
*Phase: 30-bounded-shallow-blind-training-recovery*
*Completed: 2026-04-15*
