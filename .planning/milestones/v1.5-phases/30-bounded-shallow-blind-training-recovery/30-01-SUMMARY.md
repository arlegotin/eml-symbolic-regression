---
phase: 30-bounded-shallow-blind-training-recovery
plan: 01
subsystem: benchmark
tags: [eml, proof-contract, benchmark, datasets, tdd]

requires:
  - phase: 29-paper-claim-contract-and-proof-dataset-harness
    provides: Paper claim, threshold, evidence-class, and proof dataset contracts
provides:
  - Exact scaled-exponential EML shape helper with depth/node/constant evidence
  - Permanent signed/scaled exponential proof targets with deterministic manifests
  - v1.5 shallow proof suite inventory with suite-owned constants and blind-only validation
affects: [30-bounded-shallow-blind-training-recovery, proof-suite, benchmark, datasets]

tech-stack:
  added: []
  patterns:
    - Suite-owned literal coefficient constants in OptimizerBudget
    - Exact shape evidence before proof-suite expansion

key-files:
  created:
    - tests/test_shallow_scaled_exponential_contract.py
  modified:
    - src/eml_symbolic_regression/compiler.py
    - src/eml_symbolic_regression/datasets.py
    - src/eml_symbolic_regression/proof.py
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_benchmark_contract.py

key-decisions:
  - "Scaled exponentials use the current verified depth-9 exp(k*x) EML identity with literal coefficient constants."
  - "The v1.5 shallow proof suite remains blind_training-only and rejects catalog, compile, and warm-start proof cases."

patterns-established:
  - "Proof target additions require DemoSpec provenance, proof dataset manifests, claim case IDs, and suite-declared constants."
  - "Budget constants serialize through format_constant_value and participate in stable run IDs through optimizer.as_dict()."

requirements-completed: [SHAL-01, SHAL-02]

duration: 6min
completed: 2026-04-15
---

# Phase 30 Plan 01: Shallow Proof Contract Lock Summary

**Depth-9 signed/scaled exponential proof contract with permanent targets, claim inventory, and blind-only suite constants**

## Performance

- **Duration:** 6 min
- **Started:** 2026-04-15T14:59:40Z
- **Completed:** 2026-04-15T15:06:29Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- Added `scaled_exponential_expr(variable, coefficient)` as reusable exact EML shape evidence for `exp(coefficient * variable)`.
- Locked verifier-backed evidence for Beer-Lambert, radioactive decay, scaled growth, and fast scaled decay: depth `9`, node count `19`, constants `{1, coefficient}`, and verifier status `recovered`.
- Added permanent `scaled_exp_growth` and `scaled_exp_fast_decay` proof targets with deterministic manifests and Phase 30 provenance.
- Expanded the shallow blind claim and `v1.5-shallow-proof` suite to six cases and 18 blind-training runs over seeds `{0, 1, 2}`.
- Added `OptimizerBudget.constants` parsing, finite validation, stable serialization, and propagation into training configs.
- Added fail-closed validation so `paper-shallow-blind-recovery` cannot be satisfied by catalog, compile, warm-start, or non-bounded threshold cases.

## Task Commits

Each task was committed atomically through TDD RED/GREEN commits:

1. **Task 1: Prove exact scaled-exponential EML bounds before suite lock**
   - `5d66ba7` test: add failing scaled exponential evidence test
   - `82c8088` feat: add scaled exponential EML helper
2. **Task 2: Add permanent signed/scaled proof targets and claim inventory**
   - `420da0e` test: add failing signed scaled inventory tests
   - `23d44f5` feat: add signed scaled proof targets
3. **Task 3: Lock suite-owned constants, depths, seeds, and blind-only proof cases**
   - `3c720a9` test: add failing shallow suite lock tests
   - `4b505c3` feat: lock shallow proof suite constants

## Files Created/Modified

- `src/eml_symbolic_regression/compiler.py` - Added `scaled_exponential_expr` using verified multiplication plus paper `exp(a)` identity.
- `src/eml_symbolic_regression/datasets.py` - Added `scaled_exp_growth` and `scaled_exp_fast_decay` permanent `DemoSpec` targets.
- `src/eml_symbolic_regression/proof.py` - Extended `paper-shallow-blind-recovery` case inventory.
- `src/eml_symbolic_regression/benchmark.py` - Added optimizer constants, blind-only proof validation, and six-case shallow suite contract.
- `tests/test_shallow_scaled_exponential_contract.py` - Added exact shape, provenance, manifest, and verifier tests for scaled exponentials.
- `tests/test_benchmark_contract.py` - Added constants serialization, claim inventory, suite expansion, and fail-closed metadata tests.

## Decisions Made

- The supported signed/scaled variants are exponent-coefficient variants, not amplitude-scaled variants.
- The suite bound for scaled exponentials is explicitly depth `9`, because that is the current verified exact EML representation.
- Literal coefficient constants are suite-owned proof metadata and are supplied to blind training through `OptimizerBudget.constants`.
- Phase 29 proof taxonomy remains intact; this plan only tightens shallow proof validation around blind training.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None. The focused verification passed with four existing `semantics.py` runtime warnings from the EML arithmetic path; these warnings were already present in the exact-shape verifier tests and did not affect recovery status.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_shallow_scaled_exponential_contract.py tests/test_benchmark_contract.py -q` - 31 passed, 4 existing warnings.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli list-claims` - listed all four paper claims, including `paper-shallow-blind-recovery`.

## Known Stubs

None. Stub scan hits were type annotations, empty local accumulator initialization, and the pre-existing local `placeholder` variable used for stable run ID construction.

## Next Phase Readiness

Ready for Plan 30-02. The shallow suite contract is locked, but no optimizer recovery claim was counted in this plan; later Phase 30 work still owns actual blind-training recovery over the six declared cases.

## Self-Check: PASSED

- Confirmed summary and key created/modified files exist.
- Confirmed all six task commits are present in git history.
- Confirmed final verification commands passed.

---
*Phase: 30-bounded-shallow-blind-training-recovery*
*Completed: 2026-04-15*
