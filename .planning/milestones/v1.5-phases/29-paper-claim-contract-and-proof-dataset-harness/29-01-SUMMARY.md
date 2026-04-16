---
phase: 29-paper-claim-contract-and-proof-dataset-harness
plan: 01
subsystem: proof-contract
tags: [python, dataclasses, pytest, datasets, provenance]

# Dependency graph
requires:
  - phase: 29-paper-claim-contract-and-proof-dataset-harness
    provides: Phase 29 context and research decisions D-01 through D-07
provides:
  - Stable paper claim matrix and threshold policy registry
  - Deterministic proof dataset manifests with provenance and split signatures
  - Fast proof contract and dataset manifest tests
affects: [phase-30-shallow-proof, phase-31-perturbed-basin, phase-32-depth-curve, phase-33-proof-report]

# Tech tracking
tech-stack:
  added: []
  patterns: [frozen dataclass contracts, fail-closed validation errors, deterministic SHA-256 manifest digests]

key-files:
  created:
    - src/eml_symbolic_regression/proof.py
    - tests/test_proof_contract.py
    - tests/test_proof_dataset_manifest.py
    - .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-01-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/datasets.py

key-decisions:
  - "Bounded 100% proof policies allow only verifier-owned training evidence classes, not catalog or compile-only verification."
  - "Dataset manifests hash generated split input and target bytes while omitting raw array payloads."
  - "STATE.md, ROADMAP.md, and REQUIREMENTS.md were not updated because the sequential orchestrator owns final phase state updates."

patterns-established:
  - "Proof contracts use frozen dataclasses with as_dict() and fail-closed ProofContractError."
  - "Proof dataset manifests are computed from DemoSpec.make_splits() and include a digest over the manifest excluding manifest_sha256."

requirements-completed: [CLAIM-01, CLAIM-02, CLAIM-04]

# Metrics
duration: 5m 25s
completed: 2026-04-15
---

# Phase 29 Plan 01: Paper Claim Contract and Proof Dataset Harness Summary

**Stable paper claim contracts and deterministic proof dataset manifests with provenance, split signatures, and bounded threshold policies**

## Performance

- **Duration:** 5m 25s
- **Started:** 2026-04-15T13:23:02Z
- **Completed:** 2026-04-15T13:28:27Z
- **Tasks:** 2
- **Files modified:** 4 implementation/test files plus this summary

## Accomplishments

- Added `src/eml_symbolic_regression/proof.py` with stable paper claim IDs, explicit threshold policies, evidence/training vocabularies, and fail-closed validation helpers.
- Extended `DemoSpec` with formula provenance fields and added `proof_dataset_manifest()` for deterministic split metadata, SHA-256 split signatures, and manifest digests.
- Added fast pytest coverage for claim stability, bounded threshold semantics, dataset determinism, seed-sensitive signatures, source provenance, and raw-array omission.

## Task Commits

Each TDD task was committed atomically:

1. **Task 1 RED: proof claim/threshold tests** - `4cc204d` (test)
2. **Task 1 GREEN: proof claim contracts** - `30b42d7` (feat)
3. **Task 2 RED: proof dataset manifest tests** - `98a33ea` (test)
4. **Task 2 GREEN: dataset manifests and provenance** - `2594cf4` (feat)

**Plan metadata:** this summary file is committed separately as `docs(29-01): complete proof contract plan`.

## Files Created/Modified

- `src/eml_symbolic_regression/proof.py` - Paper claim matrix, threshold policies, evidence/training vocabularies, and validation helpers.
- `src/eml_symbolic_regression/datasets.py` - Demo provenance fields, `formula_provenance()`, split hashing, and `proof_dataset_manifest()`.
- `tests/test_proof_contract.py` - Stable claim ID, threshold policy, and fail-closed validation tests.
- `tests/test_proof_dataset_manifest.py` - Determinism, seed-difference, provenance, split metadata, and no-raw-array tests.

## Decisions Made

- Kept `bounded_100_percent` separate from `measured_depth_curve` and `contract_context`; only the bounded policy has `required_rate=1.0`.
- Kept catalog verification and compile-only verification as distinct classes outside the bounded training-proof allowed evidence set.
- Used deterministic SHA-256 signatures over generated split input/target bytes plus dtype and shape metadata, while excluding raw arrays from manifests.
- Left final `STATE.md`, `ROADMAP.md`, and `REQUIREMENTS.md` updates to the orchestrator, per the sequential executor prompt.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0 auto-fixed
**Impact on plan:** No scope changes.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_proof_contract.py -q` - passed, 5 tests.
- `python -m pytest tests/test_proof_dataset_manifest.py -q` - passed, 5 tests.
- `python -m pytest tests/test_proof_contract.py tests/test_proof_dataset_manifest.py -q` - passed, 10 tests.
- `python -m pytest tests/test_benchmark_contract.py tests/test_verifier_demos_cli.py -q` - passed, 11 tests.

## Known Stubs

None.

## Next Phase Readiness

Phase 30 can now attach shallow blind recovery suites to stable claim IDs and `bounded_100_percent` thresholds. Later proof reports can cite deterministic proof dataset manifests without persisting bulky raw arrays.

## Self-Check: PASSED

- Created files exist: `src/eml_symbolic_regression/proof.py`, `tests/test_proof_contract.py`, `tests/test_proof_dataset_manifest.py`, and this summary.
- Modified file exists: `src/eml_symbolic_regression/datasets.py`.
- Task commits found in git history: `4cc204d`, `30b42d7`, `98a33ea`, `2594cf4`.
- Stub scan found no TODO, FIXME, placeholder, coming soon, not available, or hardcoded empty UI payload patterns in created/modified files.

---
*Phase: 29-paper-claim-contract-and-proof-dataset-harness*
*Completed: 2026-04-15*
