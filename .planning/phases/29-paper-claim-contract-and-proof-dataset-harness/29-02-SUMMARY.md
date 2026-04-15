---
phase: 29-paper-claim-contract-and-proof-dataset-harness
plan: 02
subsystem: proof-benchmark-contract
tags: [python, pytest, benchmark, proof-contract, evidence]

# Dependency graph
requires:
  - phase: 29-paper-claim-contract-and-proof-dataset-harness
    provides: Plan 01 proof claim, threshold, evidence-class, training-mode, and dataset manifest contracts
provides:
  - Proof-aware benchmark case/run metadata with fail-closed validation
  - Run artifacts with claim, threshold, training mode, evidence class, dataset manifest, budget, and provenance fields
  - Aggregate evidence-class counts and claim threshold summaries
affects: [phase-30-shallow-proof, phase-31-perturbed-basin, phase-32-depth-curve, phase-33-proof-report]

# Tech tracking
tech-stack:
  added: []
  patterns: [proof metadata propagation, derived evidence classes, claim-policy threshold aggregation]

key-files:
  created:
    - .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-02-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_benchmark_contract.py
    - tests/test_benchmark_runner.py
    - tests/test_benchmark_reports.py

key-decisions:
  - "Benchmark evidence classes are derived after execution and cannot be supplied by suite JSON."
  - "Runtime warm-start statuses are normalized to the existing Plan 01 proof vocabulary (`same_ast`, `verified_equivalent`) for threshold policy compatibility."
  - "STATE.md, ROADMAP.md, and REQUIREMENTS.md were not updated because the sequential orchestrator owns final phase state updates."

patterns-established:
  - "Proof contract validation wraps ProofContractError as BenchmarkValidationError(reason='invalid_proof_contract')."
  - "Aggregate threshold rows are grouped by (claim_id, threshold_policy_id) and use ThresholdPolicy.allowed_evidence_classes."

requirements-completed: [CLAIM-01, CLAIM-02, CLAIM-03, CLAIM-04]

# Metrics
duration: 10m 22s
completed: 2026-04-15
---

# Phase 29 Plan 02: Benchmark Proof Contract Summary

**Proof-aware benchmark suites, run artifacts, and aggregate threshold reports wired to the Plan 01 claim contract**

## Performance

- **Duration:** 10m 22s
- **Started:** 2026-04-15T13:31:06Z
- **Completed:** 2026-04-15T13:41:28Z
- **Tasks:** 3 TDD tasks
- **Files modified:** 4 implementation/test files plus this summary

## Accomplishments

- Extended `BenchmarkCase` and `BenchmarkRun` with proof metadata, default training-mode resolution, run-id hashing for proof fields, and fail-closed validation for unknown claims, thresholds, incompatible training modes, and caller-supplied evidence classes.
- Added the built-in `v1.5-shallow-proof` suite over existing `exp`, `log`, `radioactive_decay`, and `beer_lambert` formulas with fixed seeds, bounded threshold metadata, and blind-training tags.
- Added run artifact proof fields: `claim_id`, `claim_class`, `training_mode`, `evidence_class`, `threshold`, compact `dataset`, detailed `dataset_manifest`, `budget`, and formula `provenance`.
- Added derived evidence-class mapping for catalog, compile-only, blind training, compiler warm-start, perturbed true-tree reserved fixtures, repaired candidates, unsupported, failed, snapped, and soft-fit outcomes.
- Extended aggregate reports with `counts.evidence_classes`, `groups.evidence_class`, threshold summaries, and Markdown evidence/threshold tables.

## Task Commits

Each TDD task was committed atomically:

1. **Task 1 RED: benchmark proof contract tests** - `56251b4` (test)
2. **Task 1 GREEN: benchmark proof contracts** - `28f9ba4` (feat)
3. **Task 2 RED: artifact proof field tests** - `1bdb5c3` (test)
4. **Task 2 GREEN: proof fields in run artifacts** - `2dd2d58` (feat)
5. **Task 3 RED: proof aggregate tests** - `344d3cc` (test)
6. **Task 3 GREEN: aggregate evidence thresholds** - `ec20378` (feat)

**Plan metadata:** this summary file is committed separately as `docs(29-02): complete benchmark proof contract plan`.

## Files Created/Modified

- `src/eml_symbolic_regression/benchmark.py` - Proof metadata validation, suite expansion, artifact fields, derived evidence classes, aggregate evidence-class counts, and threshold summaries.
- `tests/test_benchmark_contract.py` - Proof metadata serialization, fail-closed validation, and `v1.5-shallow-proof` suite tests.
- `tests/test_benchmark_runner.py` - Run artifact proof schema and derived evidence-class tests.
- `tests/test_benchmark_reports.py` - Evidence-class aggregate and threshold policy tests.
- `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-02-SUMMARY.md` - Plan execution summary.

## Decisions Made

- Kept legacy benchmark suites valid without claim/threshold fields, while still resolving training mode on expanded runs and artifacts.
- Kept evidence classes derived from final payload status and training mode; suite JSON can no longer spoof `evidence_class`.
- Used Plan 01 `ThresholdPolicy.allowed_evidence_classes` as the threshold pass set, so bounded proof rows do not count catalog or compile-only verification as training proof.
- Left orchestrator-owned `STATE.md`, `ROADMAP.md`, and `REQUIREMENTS.md` untouched.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Aligned warm-start evidence names with Plan 01 proof vocabulary**
- **Found during:** Task 2 and Task 3
- **Issue:** The plan text described warm-start evidence classes as `same_ast_return` and `verified_equivalent_ast`, while Plan 01 registered threshold policies use `same_ast` and `verified_equivalent`.
- **Fix:** `evidence_class_for_payload()` maps runtime statuses `same_ast_return` and `verified_equivalent_ast` into the registered Plan 01 evidence-class values before threshold aggregation.
- **Files modified:** `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_runner.py`, `tests/test_benchmark_reports.py`
- **Verification:** `python -m pytest tests/test_benchmark_runner.py tests/test_benchmark_reports.py -q`
- **Committed in:** `2dd2d58`, `ec20378`

---

**Total deviations:** 1 auto-fixed (1 blocking compatibility issue)
**Impact on plan:** Preserves Wave 1 proof contract compatibility and keeps threshold summaries policy-driven. No scope expansion.

## Issues Encountered

- Measured depth-curve tests were adjusted to match Plan 01 policy semantics: failed outcomes are allowed measured evidence, and the threshold row reports status `reported` rather than failing the claim.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_benchmark_contract.py -q` - passed, 13 tests.
- `python -m pytest tests/test_benchmark_runner.py -q` - passed, 8 tests, 1 existing overflow warning from `semantics.py`.
- `python -m pytest tests/test_benchmark_reports.py -q` - passed, 6 tests.
- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py -q` - passed, 27 tests, 1 existing overflow warning from `semantics.py`.
- Acceptance `rg` checks for proof metadata, artifact fields, evidence classes, and thresholds all returned matches.

## Known Stubs

None. Stub scan found only implementation accumulator variables and the local `placeholder` run object used for stable artifact path construction; no TODO/FIXME/placeholder text or hardcoded empty UI/data stubs were introduced.

## Threat Flags

None. The trust boundaries in the plan were addressed inside existing benchmark suite validation, run artifact generation, and aggregate reporting; no new network endpoints, auth paths, file access patterns, or schema trust boundaries were introduced beyond the planned local JSON artifact surface.

## Next Phase Readiness

Phase 30 can run bounded shallow proof suites and consume artifacts that already expose claim, threshold, dataset manifest, training mode, and evidence-class metadata. Phase 33 can use aggregate threshold rows directly for proof reporting.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-02-SUMMARY.md`.
- Modified files exist: `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`, and `tests/test_benchmark_reports.py`.
- Task commits found in git history by message: `56251b4`, `28f9ba4`, `1bdb5c3`, `2dd2d58`, `344d3cc`, `ec20378`.
- Stub scan found no actionable stubs in created/modified files.

---
*Phase: 29-paper-claim-contract-and-proof-dataset-harness*
*Completed: 2026-04-15*
