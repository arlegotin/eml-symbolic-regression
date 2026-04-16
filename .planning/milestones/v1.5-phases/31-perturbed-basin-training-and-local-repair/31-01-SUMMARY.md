---
phase: 31-perturbed-basin-training-and-local-repair
plan: 01
subsystem: benchmark
tags: [eml, proof, basin, perturbation, benchmark]

requires:
  - phase: 29-paper-claim-contract-and-proof-dataset-harness
    provides: proof claim matrix, dataset manifests, benchmark evidence classes
  - phase: 30-bounded-shallow-blind-training-recovery
    provides: scaffolded blind evidence taxonomy kept separate from pure blind evidence
provides:
  - deterministic exact EML basin target inventory
  - first-class perturbed true-tree training runner
  - proof-perturbed-basin and Beer-Lambert probe benchmark suites
  - return_kind/raw_status/repair_status aggregate fields
affects: [phase-31, phase-32, phase-33, proof-reporting, benchmark-suites]

tech-stack:
  added: []
  patterns: [first-class proof runner modes, verifier-owned evidence classification, deterministic target manifests]

key-files:
  created:
    - src/eml_symbolic_regression/basin.py
    - tests/test_basin_targets.py
  modified:
    - src/eml_symbolic_regression/datasets.py
    - src/eml_symbolic_regression/benchmark.py
    - src/eml_symbolic_regression/proof.py
    - src/eml_symbolic_regression/cli.py
    - tests/test_benchmark_contract.py
    - tests/test_benchmark_runner.py
    - tests/test_proof_contract.py

key-decisions:
  - "Perturbed basin evidence uses start_mode='perturbed_tree' and training_mode='perturbed_true_tree_training', not compiler warm-start relabeling."
  - "Same-AST return after declared nonzero perturbation can count as perturbed true-tree recovery only with return_kind preserved separately."
  - "Beer-Lambert 15.0 and 35.0 noise rows are visible probe rows without threshold metadata."

patterns-established:
  - "Basin target specs stay independent from datasets.py to avoid circular imports."
  - "Benchmark evidence class derivation requires perturbed_tree, perturbed_true_tree_training, recovered status, and nonzero perturbation noise."
  - "Aggregate run summaries carry return_kind, raw_status, and repair_status as first-class fields."

requirements-completed: [BASN-01, BASN-02, BASN-05]

duration: 19 min
completed: 2026-04-15
---

# Phase 31 Plan 01: Perturbed True-Tree Suite and Runner Contract Summary

**Deterministic exact EML basin targets and a first-class perturbed true-tree proof runner with bounded and probe suite contracts**

## Performance

- **Duration:** 19 min
- **Started:** 2026-04-15T18:31:56Z
- **Completed:** 2026-04-15T18:50:57Z
- **Tasks:** 3
- **Files modified:** 9

## Accomplishments

- Added `basin.py` with depth-1/2/3 exact EML target specs, explicit split domains, and `fit_perturbed_true_tree()`.
- Exposed the synthetic basin targets through `demo_specs()` and deterministic proof dataset manifests.
- Added `perturbed_tree` benchmark dispatch that records `return_kind`, `raw_status`, `perturbed_true_tree`, and verifier-owned evidence.
- Declared `proof-perturbed-basin` bounded rows and `proof-perturbed-basin-beer-probes` high-noise rows outside the threshold denominator.
- Updated the perturbed-basin claim case inventory and CLI start-mode filters.

## Task Commits

1. **Task 1 RED:** `37100f1` test(31-01): add failing basin target contract tests
2. **Task 1 GREEN:** `98776bf` feat(31-01): add deterministic basin targets
3. **Task 2 RED:** `41daa64` test(31-01): add failing perturbed tree runner tests
4. **Task 2 GREEN:** `ffaaace` feat(31-01): add perturbed true tree runner
5. **Task 3 RED:** `8963b0e` test(31-01): add failing perturbed basin suite tests
6. **Task 3 test fix:** `ec80de7` test(31-01): correct perturbed metadata fixture
7. **Task 3 GREEN:** `52568e9` feat(31-01): declare perturbed basin proof suites

## Files Created/Modified

- `src/eml_symbolic_regression/basin.py` - Basin target specs and perturbed true-tree training wrapper.
- `src/eml_symbolic_regression/datasets.py` - Synthetic basin targets exposed as `DemoSpec` entries.
- `src/eml_symbolic_regression/benchmark.py` - `perturbed_tree` start mode, runner dispatch, evidence classification, and built-in suites.
- `src/eml_symbolic_regression/proof.py` - Concrete perturbed-basin case IDs and same-AST note update.
- `src/eml_symbolic_regression/cli.py` - Benchmark/campaign start-mode filters now accept `perturbed_tree`.
- `tests/test_basin_targets.py` - Target inventory, domain, verifier, and basin runner tests.
- `tests/test_benchmark_contract.py` - Suite expansion, proof metadata, and CLI parser tests.
- `tests/test_benchmark_runner.py` - Artifact and evidence-class tests for perturbed true-tree recovery.
- `tests/test_proof_contract.py` - Claim inventory and note tests.

## Decisions Made

- Kept basin target inventory in `basin.py` without importing `DemoSpec`, so target generation remains usable before dataset registration.
- Used target-expression constants rather than caller budget constants inside `fit_perturbed_true_tree()`, so compiled Beer-Lambert targets keep their exact terminal bank.
- Required nonzero perturbation in proof cases before `perturbed_true_tree_recovered` evidence can be derived.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected RED test override handling**
- **Found during:** Task 3 verification
- **Issue:** The metadata rejection test removed `training_mode` whenever an override omitted that key, so zero-noise and threshold-policy cases exercised the wrong validation path.
- **Fix:** Changed the fixture to remove `training_mode` only when the override explicitly sets it to `None`.
- **Files modified:** `tests/test_benchmark_contract.py`
- **Verification:** `python -m pytest tests/test_benchmark_contract.py::test_perturbed_basin_proof_cases_reject_invalid_metadata -q`
- **Committed in:** `ec80de7`

---

**Total deviations:** 1 auto-fixed (Rule 1).
**Impact on plan:** No scope change; the fix made the planned fail-closed proof metadata tests measure the intended cases.

## Issues Encountered

- The benchmark runner tests and plan-level pytest are slow because they include real training smoke paths.
- Existing `semantics.py:110` overflow warnings still appear in high-noise warm-start coverage; they predate this plan and remained non-failing.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_basin_targets.py tests/test_proof_dataset_manifest.py -q` -> 17 passed.
- `python -m pytest tests/test_basin_targets.py tests/test_benchmark_runner.py tests/test_compiler_warm_start.py tests/test_benchmark_contract.py -q` -> 65 passed, 2 existing warnings.
- `python -m pytest tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_proof_contract.py -q` -> 58 passed, 1 existing warning.
- `python -m pytest tests/test_basin_targets.py tests/test_benchmark_contract.py tests/test_benchmark_runner.py tests/test_proof_contract.py -q` -> 67 passed, 1 existing warning.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli list-benchmarks` -> passed and listed both perturbed-basin suites.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark proof-perturbed-basin --case basin-depth1-perturbed --seed 0 --perturbation-noise 0.05 --output-dir /tmp/eml-phase31-plan01-smoke` -> 1 run, 0 unsupported, 0 failed.

## Next Phase Readiness

Ready for Plan 31-02. The runner now emits raw perturbed-training provenance that local repair can consume without overwriting `return_kind` or `raw_status`.

---
*Phase: 31-perturbed-basin-training-and-local-repair*
*Completed: 2026-04-15*
