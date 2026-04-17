---
phase: 49-witness-registry-and-centered-scaffold-correctness
plan: 01
subsystem: benchmark
tags: [witness-registry, scaffolds, operator-family, benchmark-contracts, pytest]

requires: []
provides:
  - Raw-only scaffold witness registry for exp, log, and scaled_exp.
  - Registry-backed benchmark budget validation and family-variant scaffold filtering.
  - Focused benchmark contract tests for raw defaults and centered scaffold exclusions.
affects: [benchmark-suite-expansion, optimizer-budget-validation, centered-family-evidence, phase-49-plan-02]

tech-stack:
  added: []
  patterns:
    - Immutable dataclass registry for scaffold witness availability.
    - Initial-operator scaffold filtering for fixed and scheduled centered-family variants.

key-files:
  created:
    - src/eml_symbolic_regression/witnesses.py
  modified:
    - src/eml_symbolic_regression/__init__.py
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_benchmark_contract.py

key-decisions:
  - "Current exp, log, and scaled_exp scaffold witnesses are registered only for raw_eml."
  - "Centered benchmark variants serialize exp/log/scaled_exp exclusions with centered_family_same_family_witness_missing."
  - "Continuation benchmark variants resolve scaffold availability against the first scheduled operator."

patterns-established:
  - "Scaffold availability is resolved through witnesses.resolve_scaffold_plan instead of per-call-site conditionals."
  - "Benchmark budgets preserve raw scaffold defaults while centered-family clones store ordered missing-witness exclusions."

requirements-completed: [WIT-01, WIT-02, WIT-04]

duration: 4 min
completed: 2026-04-17
---

# Phase 49 Plan 01: Witness Registry and Benchmark Scaffold Routing Summary

**Raw-only scaffold witness registry with benchmark budget filtering that removes raw exp/log/scaled_exp scaffolds from centered-family variants.**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-17T11:29:10Z
- **Completed:** 2026-04-17T11:33:44Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Added `src/eml_symbolic_regression/witnesses.py` with frozen `ScaffoldWitness` and `ScaffoldPlan` contracts, ordered registry inspection, same-family lookup, and scaffold plan resolution.
- Exported witness registry helpers and the canonical `centered_family_same_family_witness_missing` reason from the package API.
- Replaced benchmark scaffold validation and family-variant filtering with registry-backed logic, including first-scheduled-operator handling for ZEML continuation rows.
- Added TDD contract coverage proving raw defaults remain available and centered benchmark budgets serialize ordered exp/log/scaled_exp missing-witness exclusions.

## Task Commits

Each task was committed atomically through RED/GREEN TDD commits:

1. **Task 1: Add raw-only scaffold witness registry** - `7a0f8b3` (test), `e003a67` (feat)
2. **Task 2: Route benchmark budgets through witness availability** - `240e05a` (test), `46a4c0c` (feat)

**Plan metadata:** recorded in the final docs commit.

## Files Created/Modified

- `src/eml_symbolic_regression/witnesses.py` - Raw-only scaffold witness registry and resolver.
- `src/eml_symbolic_regression/__init__.py` - Top-level exports for registry inspection helpers.
- `src/eml_symbolic_regression/benchmark.py` - Registry-backed scaffold validation and family-variant budget filtering.
- `tests/test_benchmark_contract.py` - Registry inspection, raw-default, centered-exclusion, and continuation-schedule contract tests.

## Decisions Made

- Kept the registry static and stdlib-only; future centered witnesses must be added explicitly as same-family registry entries.
- Kept `scaffold_exclusions` as ordered `kind:reason` strings for budget serialization compatibility.
- Used `operator_schedule[0]` for scaffold availability because benchmark scaffolds are materialized at initialization time.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## Verification

- `python -m pytest tests/test_benchmark_contract.py::test_scaffold_witness_registry_declares_raw_only_current_witnesses tests/test_benchmark_contract.py::test_family_matrix_suites_clone_regimes_with_operator_variants tests/test_benchmark_contract.py::test_v18_family_matrix_expands_scales_and_schedules tests/test_benchmark_contract.py::test_optimizer_budget_parses_and_serializes_constants -q` - passed (`4 passed`).
- `rg "CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING" src/eml_symbolic_regression/witnesses.py` - passed.
- `rg "ScaffoldWitness\\(\"exp\", \"raw_eml\", \"scaffold_exp\", 1" src/eml_symbolic_regression/witnesses.py` - passed, with matching raw log and scaled_exp entries verified.
- `rg "centered_family_incompatible_raw_witness" src/eml_symbolic_regression/benchmark.py tests/test_benchmark_contract.py` - passed with no matches.

## Known Stubs

None. Stub scan matches were local accumulator initializers and pre-existing optional field defaults, not placeholder data paths.

## Self-Check: PASSED

- Created file exists: `src/eml_symbolic_regression/witnesses.py`.
- Summary file exists: `.planning/phases/49-witness-registry-and-centered-scaffold-correctness/49-01-SUMMARY.md`.
- Task commits exist: `7a0f8b3`, `e003a67`, `240e05a`, `46a4c0c`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 49-02 can now close the direct optimizer/helper bypass path using the registry API created here. Benchmark-side WIT-02/WIT-04 coverage is in place; optimizer manifests and raw helper guards remain the next plan's scope.

---
*Phase: 49-witness-registry-and-centered-scaffold-correctness*
*Completed: 2026-04-17*
