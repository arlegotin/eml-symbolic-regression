---
phase: 52-verifier-gated-exact-cleanup-expansion
plan: 02
subsystem: benchmark-runner
tags: [repair, benchmark-suite, candidate-pool, campaign-reporting, pytest]

requires:
  - phase: 52-01
    provides: RepairConfig.expanded_candidate_pool plus repair root/dedup metadata.
provides:
  - Optional benchmark repair config outside optimizer budgets.
  - Built-in `v1.9-repair-evidence` default-vs-expanded near-miss suite.
  - Expanded repair root/dedup metrics in benchmark artifacts and campaign CSVs.
affects: [benchmark-artifacts, campaign-reports, phase-53, raw-hybrid-paper-suite]

tech-stack:
  added: []
  patterns:
    - optional run identity fields separate from optimizer budget hashes
    - focused before/after suite without proof claim metadata
    - row-first/metrics-fallback campaign CSV columns for repair evidence

key-files:
  created:
    - .planning/phases/52-verifier-gated-exact-cleanup-expansion/52-02-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/campaign.py
    - tests/test_benchmark_runner.py
    - tests/test_benchmark_contract.py
    - tests/test_benchmark_reports.py
    - tests/test_campaign.py

key-decisions:
  - "Repair settings are optional benchmark case/run metadata and are not serialized into OptimizerBudget."
  - "`v1.9-repair-evidence` has no claim id, no threshold policy, and `expect_recovery=False`; it measures near-miss repair behavior without changing denominators."
  - "Expanded target-free cleanup config is passed only to cleanup_failed_candidate; perturbed target-aware repair remains the fallback path after a target-free miss."
  - "Repair root/dedup metrics are exposed without relabeling repaired candidates as blind, same-AST, compile-only, or perturbed true-tree recovery."

requirements-completed: [REP-01, REP-02, REP-03, REP-04]

duration: 15min
completed: 2026-04-17T15:32:08Z
---

# Phase 52 Plan 02: Benchmark Repair Evidence Summary

**Benchmark opt-in for expanded verifier-gated cleanup with focused before/after repair evidence**

## Performance

- **Duration:** 15 min
- **Started:** 2026-04-17T15:17:31Z
- **Completed:** 2026-04-17T15:32:08Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Added `BenchmarkRepairConfig` with `preset="expanded_candidate_pool"` and threaded it through `BenchmarkCase`, `BenchmarkRun`, run IDs, suite expansion, and run serialization.
- Routed blind, warm-start, and perturbed-tree target-free cleanup through `_repair_config_for_run(run)`, while keeping target-aware perturbed repair as a fallback after target-free cleanup misses.
- Added built-in `v1.9-repair-evidence` with four focused near-miss cases:
  - `repair-radioactive-blind-default`
  - `repair-radioactive-blind-expanded`
  - `repair-beer-warm-default`
  - `repair-beer-warm-expanded`
- Exposed repair metadata in benchmark metrics: candidate root count, per-root summary count, deduped variant count, accepted candidate id/source, and accepted root source.
- Added campaign run/failure CSV columns for `repair_candidate_root_count`, `repair_deduped_variant_count`, and `repair_accepted_candidate_root_source`.
- Added regression coverage proving selected/fallback optimizer manifests remain intact after repair promotion and repaired rows stay under `repaired_candidate` taxonomy.

## Task Commits

1. **Task 1 RED: benchmark repair config routing coverage** - `aae4be8` (test)
2. **Task 1 GREEN: optional repair config and cleanup routing** - `6bcc6c5` (feat)
3. **Task 2 RED: repair evidence suite contract** - `b2053a2` (test)
4. **Task 2 GREEN: v1.9 repair evidence suite** - `7476e1f` (feat)
5. **Task 3 RED: repair artifact metric coverage** - `a9ccdac` (test)
6. **Task 3 GREEN: repair metrics in reports** - `279cd6c` (feat)

## Files Created/Modified

- `src/eml_symbolic_regression/benchmark.py` - Added optional repair config, run-id participation, cleanup routing, focused suite, and repair metric extraction.
- `src/eml_symbolic_regression/campaign.py` - Added repair root/dedup columns to run and failure CSVs.
- `tests/test_benchmark_contract.py` - Locked optional repair config serialization and the `v1.9-repair-evidence` contract.
- `tests/test_benchmark_runner.py` - Added routing, candidate-pool repair promotion, and perturbed fallback-order regressions.
- `tests/test_benchmark_reports.py` - Locked aggregate taxonomy and expanded repair metric preservation.
- `tests/test_campaign.py` - Locked campaign CSV visibility for repair root/dedup metrics.
- `.planning/phases/52-verifier-gated-exact-cleanup-expansion/52-02-SUMMARY.md` - Captures execution results and GSD metadata.

## Verification

- Task 1 RED: focused command failed before production code with `ImportError: cannot import name 'BenchmarkRepairConfig'`.
- Task 1 GREEN: `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_michaelis_evidence_suite_contains_exact_warm_start_case tests/test_benchmark_runner.py::test_expanded_repair_config_routes_to_target_free_cleanup -q` -> `4 passed`.
- Additional Task 1 serialization check: `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_benchmark_case_and_run_serialize_optional_repair_config tests/test_benchmark_contract.py::test_benchmark_run_id_includes_repair_only_when_declared -q` -> `2 passed`.
- Task 2 RED: focused command failed because `v1.9-repair-evidence` was not registered.
- Task 2 GREEN: `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py::test_builtin_suite_registry_expands_stable_run_ids tests/test_benchmark_contract.py::test_repair_evidence_suite_contains_default_and_expanded_near_miss_pairs tests/test_benchmark_contract.py::test_arrhenius_evidence_suite_contains_exact_warm_start_case tests/test_benchmark_contract.py::test_michaelis_evidence_suite_contains_exact_warm_start_case -q` -> `4 passed`.
- Task 3 RED: focused command failed on missing `repair_candidate_root_count` metric and missing campaign columns.
- Task 3 GREEN: `PYTHONPATH=src python -m pytest tests/test_benchmark_runner.py::test_candidate_pool_cleanup_promotes_artifact_without_mutating_selected_or_fallback tests/test_benchmark_runner.py::test_perturbed_target_aware_repair_still_runs_after_expanded_target_free_miss tests/test_benchmark_reports.py tests/test_campaign.py::test_campaign_tables_preserve_perturbed_repair_status_columns -q` -> `19 passed`.
- Required plan verification: `PYTHONPATH=src python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_benchmark_reports.py tests/test_campaign.py -q` -> `126 passed, 3 warnings in 219.52s`.

## Decisions Made

- Kept repair config out of `OptimizerBudget.as_dict()` so existing no-repair benchmark run IDs remain stable.
- Included repair settings in `BenchmarkRun.run_id` only when a case/run explicitly declares them.
- Kept the repair evidence suite outside proof claims and thresholds because REP-04 asks to measure near-miss behavior, not to assume improvement.
- Added artifact/report visibility for repair metadata without changing `classify_run()` or `evidence_class_for_payload()` taxonomy.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

- A candidate-pool runner fixture initially deduplicated selected and fallback roots because both snapped to the same exact AST. The test fixture was corrected to give the selected fake candidate a distinct failing AST before committing the RED coverage.

## Known Stubs

None introduced. Stub scan found only expected optional defaults, empty collection initializers, existing test assertions for empty scaffold lists, and the pre-existing local variable named `placeholder` in benchmark run-id construction.

## User Setup Required

None.

## Threat Flags

None. The plan introduced no new network endpoints, auth paths, file access patterns, or schema trust boundaries beyond the declared benchmark config and artifact-reporting surfaces.

## Next Phase Readiness

Phase 52-03 can run `v1.9-repair-evidence` and use the new repair root/dedup fields in generated reports. The suite remains intentionally non-claim, and repaired rows stay separate from blind, same-AST, compile-only, and perturbed true-tree recovery.

## Self-Check: PASSED

- Verified created/modified files exist: `src/eml_symbolic_regression/benchmark.py`, `src/eml_symbolic_regression/campaign.py`, `tests/test_benchmark_runner.py`, `tests/test_benchmark_contract.py`, `tests/test_benchmark_reports.py`, `tests/test_campaign.py`, `.planning/phases/52-verifier-gated-exact-cleanup-expansion/52-02-SUMMARY.md`.
- Verified task commits exist in git history: `aae4be8`, `6bcc6c5`, `b2053a2`, `7476e1f`, `a9ccdac`, `279cd6c`.
- Verified no tracked file deletions were introduced by task commits.
- Stub scan found no introduced TODO/FIXME/placeholder stubs or mock-only data paths.

---
*Phase: 52-verifier-gated-exact-cleanup-expansion*
*Completed: 2026-04-17*
