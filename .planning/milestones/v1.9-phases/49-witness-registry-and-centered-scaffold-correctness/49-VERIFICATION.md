---
phase: 49-witness-registry-and-centered-scaffold-correctness
verified: 2026-04-17T12:06:23Z
status: passed
score: 9/9 must-haves verified
overrides_applied: 0
---

# Phase 49: Witness Registry and Centered Scaffold Correctness Verification Report

**Phase Goal:** Make scaffold/witness availability explicit by operator family and prevent raw witnesses from contaminating centered-family runs.
**Verified:** 2026-04-17T12:06:23Z
**Status:** passed
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Developer can inspect registered scaffold witnesses and see `exp`, `log`, and `scaled_exp` available only for `raw_eml`. | VERIFIED | `src/eml_symbolic_regression/witnesses.py` defines exactly three `ScaffoldWitness` entries, all with `operator_family="raw_eml"`, and `src/eml_symbolic_regression/__init__.py` exports the registry helpers. `tests/test_benchmark_contract.py::test_scaffold_witness_registry_declares_raw_only_current_witnesses` asserts the public inspection payload. |
| 2 | Raw `exp`, `log`, and `scaled_exp` scaffolds are available for raw EML only unless a same-family witness is explicitly registered. | VERIFIED | `resolve_scaffold_plan()` enables all three kinds for `raw_eml_operator()` and emits `*:centered_family_same_family_witness_missing` exclusions for `CEML_2` and `ZEML_8`; no centered witnesses are registered. Direct Python spot-check returned raw enabled `['exp', 'log', 'scaled_exp']` and centered enabled `[]` with all three exclusions. |
| 3 | Centered benchmark variants remove `exp`, `log`, and `scaled_exp` scaffold initializers before runs are materialized. | VERIFIED | `benchmark._operator_variant_budget()` resolves `base.scaffold_initializers` against `variant.operator_schedule[0]` when present, otherwise `variant.operator_family`, then stores `scaffold_plan.enabled`. Contract tests assert centered family matrix runs have `optimizer.scaffold_initializers == ()`. |
| 4 | Centered benchmark budgets serialize `exp`/`log`/`scaled_exp` exclusions with `centered_family_same_family_witness_missing` reason codes. | VERIFIED | `OptimizerBudget.as_dict()` serializes `scaffold_exclusions`; family matrix tests assert the exact ordered tuple `exp`, `log`, `scaled_exp` with the canonical reason. |
| 5 | Raw benchmark variants preserve the existing raw scaffold defaults. | VERIFIED | `tests/test_benchmark_contract.py` asserts raw shallow and calibration variants keep `("exp", "log", "scaled_exp")` and empty exclusions. |
| 6 | Direct centered `fit_eml_tree()` calls with default scaffolds do not generate `scaffold_exp`, `scaffold_log`, or `scaffold_scaled_exp` attempts. | VERIFIED | `optimize.fit_eml_tree()` computes `scaffold_plan = resolve_scaffold_plan(config.scaffold_initializers, initial_operator)` and uses `effective_config` for `_training_attempts()`. Optimizer cleanup tests assert centered fixed and scheduled runs have empty manifest scaffold initializers and no restart `attempt_kind` starting with `scaffold_`. |
| 7 | Direct raw scaffold helper calls on centered `SoftEMLTree` instances fail closed before mutating slots or embedding expressions. | VERIFIED | `SoftEMLTree._require_scaffold_witness()` calls `scaffold_witness_for(kind, self.operator_family)` before `force_exp`, `force_log`, and `force_scaled_exp` mutate slots. `tests/test_master_tree.py::test_centered_tree_rejects_raw_scaffold_helpers_without_same_family_witness` asserts the exact `EmbeddingError.reason` and unchanged decisions. |
| 8 | Optimizer manifests and benchmark run artifacts expose centered scaffold exclusions with operator-family context. | VERIFIED | `fit_eml_tree()` writes top-level `scaffold_exclusions` and `scaffold_witness_operator`; benchmark artifacts preserve budget exclusions, trained candidate exclusions, metrics, and aggregate rows. Runner tests assert all of those fields for centered smoke runs. |
| 9 | Raw EML scaffold recovery tests still recover `exp` and `scaled_exp` through the existing raw helper paths. | VERIFIED | Raw optimizer and runner tests still assert `scaffold_exp` and `scaffold_scaled_exp` provenance and recovered verifier status for raw runs. Focused pytest passed. |

**Score:** 9/9 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/witnesses.py` | Inspectable scaffold witness registry and resolver. | VERIFIED | Exists, substantive, exports dataclasses, canonical reason, registry inspection, same-family lookup, and ordered scaffold-plan resolution. |
| `src/eml_symbolic_regression/__init__.py` | Top-level registry inspection exports for WIT-01. | VERIFIED | Exports `CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING`, `ScaffoldPlan`, `ScaffoldWitness`, `known_scaffold_kinds`, `list_scaffold_witnesses`, `resolve_scaffold_plan`, and `scaffold_witness_for`. |
| `src/eml_symbolic_regression/benchmark.py` | Registry-backed budget validation, family-variant scaffold filtering, and artifact propagation. | VERIFIED | Uses `known_scaffold_kinds()` for validation, `resolve_scaffold_plan()` for variants, and `_manifest_with_budget_scaffold_exclusions()` plus metrics extraction for artifact visibility. |
| `src/eml_symbolic_regression/optimize.py` | Registry-backed direct optimizer scaffold filtering and manifest exclusions. | VERIFIED | Resolves scaffold plan at `fit_eml_tree()` entry, uses effective config for attempts/training/manifests, serializes `scaffold_exclusions` and `scaffold_witness_operator`, and guards `_apply_scaffold()`. |
| `src/eml_symbolic_regression/master_tree.py` | Fail-closed guard on raw scaffold helper methods. | VERIFIED | GSD artifact matcher flagged missing literal lower-case reason text, but manual verification confirms the file imports `CENTERED_FAMILY_SAME_FAMILY_WITNESS_MISSING` and raises `EmbeddingError` with that canonical value. Tests assert the exact runtime reason. |
| `tests/test_benchmark_contract.py` | Registry inspection, benchmark exclusion, raw-default, continuation, and invalid scaffold tests. | VERIFIED | Focused contract tests passed. |
| `tests/test_optimizer_cleanup.py` | Direct optimizer centered exclusion and raw default regression tests. | VERIFIED | Focused optimizer tests passed. |
| `tests/test_master_tree.py` | Direct helper fail-closed tests plus raw helper regressions. | VERIFIED | Focused master-tree tests passed. |
| `tests/test_benchmark_runner.py` | Run artifact, metrics, aggregate, and raw Beer-Lambert provenance tests. | VERIFIED | Focused runner tests passed. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `benchmark.py` | `witnesses.py` | `OptimizerBudget.validate` uses `known_scaffold_kinds`. | WIRED | GSD key-link check verified pattern; source uses `allowed_scaffolds = set(known_scaffold_kinds())`. |
| `benchmark.py` | `witnesses.py` | `_operator_variant_budget` resolves requested scaffolds against the initial variant operator. | WIRED | GSD key-link check verified pattern; source calls `resolve_scaffold_plan(base.scaffold_initializers, initial_operator)`. |
| `test_benchmark_contract.py` | `witnesses.py` | Direct registry assertions. | WIRED | Tests import and assert `list_scaffold_witnesses`, `known_scaffold_kinds`, `resolve_scaffold_plan`, and `scaffold_witness_for`. |
| `optimize.py` | `witnesses.py` | `fit_eml_tree` resolves direct caller scaffold initializers against the initial training operator. | WIRED | GSD key-link check verified pattern; tests prove centered direct calls emit no scaffold attempts. |
| `master_tree.py` | `witnesses.py` | `force_exp`, `force_log`, and `force_scaled_exp` require a same-family witness before mutation. | WIRED | GSD key-link check verified pattern; runtime test asserts `EmbeddingError.reason` and unchanged decisions. |
| `test_benchmark_runner.py` | `benchmark.py` | Artifact metrics copy budget scaffold exclusions and trained optimizer manifest exclusions. | WIRED | GSD key-link check verified pattern; runner tests assert budget, manifest, metrics, and aggregate fields. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `witnesses.py` | `ScaffoldPlan.enabled`, `ScaffoldPlan.exclusions` | `_SCAFFOLD_WITNESSES` and `EmlOperator.family` via `scaffold_witness_for()`. | Yes - static registry entries are concrete raw witnesses and centered exclusions are computed from actual operator family. | VERIFIED |
| `benchmark.py` | `OptimizerBudget.scaffold_initializers`, `OptimizerBudget.scaffold_exclusions` | `_operator_variant_budget()` resolves base budget through the registry before expanded runs are materialized. | Yes - family matrix tests inspect expanded `BenchmarkRun` budgets. | VERIFIED |
| `optimize.py` | `manifest["config"]["scaffold_initializers"]`, `manifest["scaffold_exclusions"]`, restart `attempt_kind` | `fit_eml_tree()` uses `scaffold_plan.enabled` to build `effective_config` and `_training_attempts()`. | Yes - optimizer tests inspect actual returned manifests. | VERIFIED |
| `master_tree.py` | `EmbeddingError.reason`, tree slot decisions | `_require_scaffold_witness()` resolves against `self.operator_family` before helper mutation. | Yes - master-tree test snapshots decisions before/after and asserts no mutation. | VERIFIED |
| `benchmark.py` | Artifact and aggregate `metrics.scaffold_exclusions` | `_manifest_with_budget_scaffold_exclusions()`, `_extract_run_metrics()`, `_run_summary()`, and `aggregate_evidence()`. | Yes - runner tests execute the benchmark and inspect written artifact JSON plus aggregate rows. | VERIFIED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Focused phase behavior across registry, benchmark, optimizer, helper guards, and runner artifacts. | `python -m pytest tests/test_benchmark_contract.py::test_scaffold_witness_registry_declares_raw_only_current_witnesses tests/test_benchmark_contract.py::test_family_matrix_suites_clone_regimes_with_operator_variants tests/test_benchmark_contract.py::test_v18_family_matrix_expands_scales_and_schedules tests/test_benchmark_contract.py::test_optimizer_budget_parses_and_serializes_constants tests/test_optimizer_cleanup.py::test_optimizer_scaffold_recovers_exp_with_manifest_provenance tests/test_optimizer_cleanup.py::test_optimizer_runs_fixed_centered_family_with_manifest_metadata tests/test_optimizer_cleanup.py::test_optimizer_preserves_centered_schedule_metadata tests/test_master_tree.py::test_force_exp_snaps_to_paper_identity tests/test_master_tree.py::test_force_log_snaps_to_paper_identity tests/test_master_tree.py::test_force_scaled_exp_snaps_to_exact_depth_nine_shape tests/test_master_tree.py::test_centered_tree_rejects_raw_scaffold_helpers_without_same_family_witness tests/test_benchmark_runner.py::test_runner_executes_operator_family_smoke_matrix tests/test_benchmark_runner.py::test_shallow_beer_lambert_blind_run_artifact_exposes_scaled_scaffold_diagnostics -q` | `15 passed, 3 warnings in 118.04s`; warnings are existing numerical runtime warnings from EML semantics tests. | PASS |
| Plan 49-01 artifacts and key links. | `gsd-tools verify artifacts/key-links 49-01-PLAN.md` | Artifacts `3/3` passed; key links `3/3` verified. | PASS |
| Plan 49-02 artifacts and key links. | `gsd-tools verify artifacts/key-links 49-02-PLAN.md` | Key links `3/3` verified. Artifacts `4/5` by literal matcher because `master_tree.py` imports the canonical constant rather than repeating the lower-case reason string; manual and pytest verification passed. | PASS |
| Direct registry behavior. | `python -c '... resolve_scaffold_plan(...) ...'` with `sys.path.insert(0, "src")`. | Raw plan enabled all three scaffolds with no exclusions; centered plan enabled none and emitted all three canonical exclusions. | PASS |
| Deprecated reason removed from source/test contract. | `rg "centered_family_incompatible_raw_witness" src/eml_symbolic_regression/benchmark.py tests/test_benchmark_contract.py src/eml_symbolic_regression/optimize.py src/eml_symbolic_regression/master_tree.py tests/test_optimizer_cleanup.py tests/test_master_tree.py tests/test_benchmark_runner.py` | No matches. | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| WIT-01 | 49-01 | Developer can inspect an explicit witness/initializer registry that declares scaffold availability by operator family. | SATISFIED | `witnesses.py` registry and top-level package exports exist; contract test asserts exact registry payload and raw-only family. |
| WIT-02 | 49-01, 49-02 | Centered families no longer receive raw `exp`, `log`, or `scaled_exp` scaffold attempts unless a tested same-family witness is registered. | SATISFIED | Benchmark variants and direct optimizer entry both call `resolve_scaffold_plan`; centered tests assert empty scaffold initializers and no scaffold restart attempt kinds. |
| WIT-03 | 49-02 | Raw-specific scaffold helpers fail closed or are only reachable through raw-family registry entries. | SATISFIED | `SoftEMLTree._require_scaffold_witness()` guards all three helper methods; test asserts `EmbeddingError.reason == "centered_family_same_family_witness_missing"` before mutation. |
| WIT-04 | 49-01, 49-02 | Benchmark and optimizer artifacts record centered scaffold exclusions with explicit reason codes such as `centered_family_same_family_witness_missing`. | SATISFIED | Optimizer manifests contain `scaffold_exclusions` and `scaffold_witness_operator`; benchmark artifact tests verify budget, trained candidate, metrics, and aggregate rows carry the canonical exclusions. |

All requirement IDs declared in the two PLAN frontmatters are accounted for. `.planning/REQUIREMENTS.md` maps WIT-01 through WIT-04 to Phase 49 and no additional Phase 49 requirement IDs were found.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| N/A | N/A | No blocker anti-patterns found. | N/A | Scan found only benign local list/dict initializers and test assertions for expected empty scaffold lists. The deprecated `centered_family_incompatible_raw_witness` reason is absent from source/test files. |

### Human Verification Required

None. This phase is internal package behavior with deterministic source checks and focused pytest coverage; no visual, real-time, external-service, or manual UX validation is needed.

### Gaps Summary

No gaps found. The phase goal is achieved: scaffold/witness availability is explicit by operator family, centered benchmark and direct optimizer paths no longer receive raw scaffold attempts, direct centered helper calls fail closed, and optimizer/benchmark artifacts expose canonical centered scaffold exclusion reason codes while preserving raw scaffold recovery behavior.

---

_Verified: 2026-04-17T12:06:23Z_
_Verifier: Claude (gsd-verifier)_
