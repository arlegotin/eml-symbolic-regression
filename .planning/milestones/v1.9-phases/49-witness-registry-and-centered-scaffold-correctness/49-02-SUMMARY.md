---
phase: 49-witness-registry-and-centered-scaffold-correctness
plan: 02
subsystem: optimizer
tags: [witness-registry, scaffolds, operator-family, benchmark-artifacts, pytest]

requires:
  - phase: 49-01
    provides: Raw-only scaffold witness registry and benchmark budget filtering.
provides:
  - Direct optimizer scaffold filtering through the witness registry.
  - Fail-closed raw scaffold helper guards for centered-family trees.
  - Centered scaffold exclusion visibility in optimizer manifests, run artifacts, metrics, and aggregate summaries.
affects: [optimizer-attempt-generation, master-tree-scaffolds, benchmark-run-artifacts, phase-50]

tech-stack:
  added: []
  patterns:
    - Resolve optimizer scaffold availability against the initial training operator.
    - Annotate benchmark trained-candidate manifests with budget-level scaffold exclusions.

key-files:
  created: []
  modified:
    - src/eml_symbolic_regression/optimize.py
    - src/eml_symbolic_regression/master_tree.py
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_optimizer_cleanup.py
    - tests/test_master_tree.py
    - tests/test_benchmark_runner.py

key-decisions:
  - "Direct optimizer calls use the initial training operator, not the final hardening operator, to resolve scaffold witness availability."
  - "Centered raw scaffold helper calls fail with EmbeddingError reason centered_family_same_family_witness_missing before slot mutation or embedding."
  - "Benchmark artifacts copy budget scaffold exclusions into trained optimizer manifests when benchmark filtering has already removed the raw scaffold requests."

patterns-established:
  - "Use witnesses.resolve_scaffold_plan at optimizer entry boundaries before training attempts are generated."
  - "Keep raw scaffold recovery paths active while centered-family runs serialize ordered exp/log/scaled_exp exclusions."

requirements-completed: [WIT-02, WIT-03, WIT-04]

duration: 13 min
completed: 2026-04-17
---

# Phase 49 Plan 02: Direct Optimizer and Helper Scaffold Guard Summary

**Registry-backed optimizer and helper guards that block raw exp/log/scaled_exp scaffolds under centered operators while preserving raw scaffold recovery artifacts.**

## Performance

- **Duration:** 13 min
- **Started:** 2026-04-17T11:37:42Z
- **Completed:** 2026-04-17T11:50:18Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- Routed direct `fit_eml_tree()` scaffold defaults through `resolve_scaffold_plan()` using the initial training operator, including scheduled `ZEML_8 -> ZEML_4` runs.
- Added top-level optimizer manifest fields for `scaffold_exclusions` and `scaffold_witness_operator`, with effective configs showing centered scaffold initializers removed.
- Added `SoftEMLTree._require_scaffold_witness()` so `force_exp`, `force_log`, and `force_scaled_exp` fail closed on centered trees before mutation, depth checks, or embedding.
- Extended benchmark runner coverage so centered exclusions survive budgets, trained optimizer manifests, extracted metrics, and aggregate rows while raw Beer-Lambert still records `scaffold_scaled_exp` recovery provenance.

## Task Commits

Each task was committed atomically through TDD commits:

1. **Task 1: Filter direct optimizer scaffolds and serialize exclusions** - `d6ee1c1` (test), `7540b0f` (feat)
2. **Task 2: Guard raw scaffold helper methods** - `e210c09` (test), `b68585d` (feat)
3. **Task 3: Prove scaffold exclusion reason codes survive run artifacts** - `d172cc7` (test), `3030165` (fix)

**Plan metadata:** recorded in the final docs commit.

## Files Created/Modified

- `src/eml_symbolic_regression/optimize.py` - Direct optimizer scaffold plan resolution, manifest exclusion serialization, and scaffold dispatch guard.
- `src/eml_symbolic_regression/master_tree.py` - Raw scaffold helper witness guard with structured `EmbeddingError`.
- `src/eml_symbolic_regression/benchmark.py` - Benchmark trained-candidate manifest annotation with budget scaffold exclusions.
- `tests/test_optimizer_cleanup.py` - Direct optimizer raw default, centered fixed-family, and centered schedule regression coverage.
- `tests/test_master_tree.py` - Centered helper fail-closed coverage for exp, log, and scaled_exp.
- `tests/test_benchmark_runner.py` - Run artifact, metrics, aggregate, and raw Beer-Lambert provenance coverage.

## Decisions Made

- Kept scaffold availability tied to the initial training operator because scaffolds are applied before schedule progression and final hardening.
- Kept optimizer manifests JSON-style for `scaffold_initializers` so in-memory and artifact assertions use the same list shape.
- Preserved verifier-owned status and evidence-class logic; only scaffold attempt availability and reason-code visibility changed.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Propagated benchmark budget exclusions into trained optimizer manifests**
- **Found during:** Task 3 (artifact RED test)
- **Issue:** Centered benchmark budgets and metrics carried scaffold exclusions, but nested optimizer manifests showed `[]` because benchmark filtering removed scaffold requests before calling `fit_eml_tree()`.
- **Fix:** Added `_manifest_with_budget_scaffold_exclusions()` and used it for blind and perturbed-tree trained-candidate payloads.
- **Files modified:** `src/eml_symbolic_regression/benchmark.py`
- **Verification:** `python -m pytest tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix tests/test_benchmark_runner.py::test_shallow_beer_lambert_blind_run_artifact_exposes_scaled_scaffold_diagnostics -q`
- **Committed in:** `3030165`

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** The fix was required for WIT-04 artifact truthfulness and did not change verifier status, evidence classes, or recovery thresholds.

## Issues Encountered

- The old centered optimizer test still assumed a cheap centered run would snap to the scaffold-derived exact expression. After raw scaffolds were correctly filtered, that assertion no longer matched the plan's centered-negative contract, so the test now focuses on operator metadata, exclusion serialization, and absence of scaffold attempts.

## Verification

- `python -m pytest tests/test_optimizer_cleanup.py::test_optimizer_scaffold_recovers_exp_with_manifest_provenance tests/test_optimizer_cleanup.py::test_optimizer_runs_fixed_centered_family_with_manifest_metadata tests/test_optimizer_cleanup.py::test_optimizer_preserves_centered_schedule_metadata tests/test_master_tree.py::test_centered_tree_rejects_raw_scaffold_helpers_without_same_family_witness tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix tests/test_benchmark_runner.py::test_shallow_beer_lambert_blind_run_artifact_exposes_scaled_scaffold_diagnostics -q` - passed (`8 passed`, 2 warnings from centered `log1p` runtime diagnostics).
- `rg "resolve_scaffold_plan" src/eml_symbolic_regression/optimize.py` - passed.
- `rg "\"scaffold_exclusions\"" src/eml_symbolic_regression/optimize.py` - passed.
- `rg "_require_scaffold_witness" src/eml_symbolic_regression/master_tree.py` - passed.
- `rg "centered_family_same_family_seed_missing" tests/test_benchmark_runner.py` - passed, preserving existing seed-gate assertions.

## Known Stubs

None. Stub scan found only a pre-existing local `placeholder` variable in benchmark suite expansion code, not placeholder data or UI behavior.

## Threat Flags

None. The plan touched optimizer/helper trust boundaries and artifact serialization already covered by the phase threat model; it introduced no new network, auth, file-access, or schema trust boundary.

## Self-Check: PASSED

- Summary file exists: `.planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-02-SUMMARY.md`.
- Key modified files exist: `src/eml_symbolic_regression/optimize.py`, `src/eml_symbolic_regression/master_tree.py`, and `src/eml_symbolic_regression/benchmark.py`.
- Task commits exist: `d6ee1c1`, `7540b0f`, `e210c09`, `b68585d`, `d172cc7`, `3030165`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 49 now satisfies WIT-02, WIT-03, and WIT-04 end to end. Centered families remain paused until true same-family witnesses are constructed; raw scaffolded recovery and Beer-Lambert artifact provenance remain intact for the raw-hybrid work in Phase 50.

---
*Phase: 49-witness-registry-and-centered-scaffold-correctness*
*Completed: 2026-04-17*
