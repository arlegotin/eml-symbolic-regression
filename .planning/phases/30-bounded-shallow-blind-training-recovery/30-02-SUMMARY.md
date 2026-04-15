---
phase: 30-bounded-shallow-blind-training-recovery
plan: 02
subsystem: optimizer
tags: [eml, pytorch, proof-suite, blind-training, diagnostics]

requires:
  - phase: 30-bounded-shallow-blind-training-recovery
    provides: Plan 30-01 scaled-exponential expression helper, proof targets, and suite-owned constants
provides:
  - SoftEMLTree scaled-exponential scaffold embedding through the existing snap path
  - Blind optimizer scaled-exponential scaffold attempts over suite-owned finite non-unit constants
  - Proof artifact diagnostics for scaffold source, strategy, coefficient, losses, snap confidence, active nodes, and verifier status
affects: [30-bounded-shallow-blind-training-recovery, v1.5-shallow-proof, benchmark-artifacts]

tech-stack:
  added: []
  patterns:
    - Formula-family scaffold attempts stay inside fit_eml_tree and still train, snap, and verify
    - Benchmark metrics derive scaffold provenance from serialized optimizer manifests

key-files:
  created:
    - .planning/phases/30-bounded-shallow-blind-training-recovery/30-02-SUMMARY.md
  modified:
    - src/eml_symbolic_regression/master_tree.py
    - src/eml_symbolic_regression/optimize.py
    - src/eml_symbolic_regression/benchmark.py
    - tests/test_master_tree.py
    - tests/test_optimizer_cleanup.py
    - tests/test_benchmark_runner.py

key-decisions:
  - "Scaled-exp scaffolds are emitted only at depth >= 9 and only for finite non-unit constants declared by the training config."
  - "The scaffold is recorded as optimizer initialization provenance, not as a compiler warm-start, catalog route, or compile-only shortcut."
  - "Artifact metrics expose scaffold source, strategy, and coefficient from the winning optimizer manifest."

patterns-established:
  - "SoftEMLTree.force_scaled_exp embeds compiler.scaled_exponential_expr through embed_expr and returns EmbeddingResult diagnostics."
  - "TrainingConfig defaults now include scaled_exp after exp/log, with no-op behavior when no eligible constants exist."
  - "Proof artifact diagnostics are extracted from trained_eml_candidate.best_restart.initialization."

requirements-completed: [SHAL-02, SHAL-03]

duration: 16min
completed: 2026-04-15
---

# Phase 30 Plan 02: Scaled-Exponential Blind Recovery Summary

**Blind scaled-exponential scaffold recovery with verifier-owned proof artifacts and serialized scaffold diagnostics**

## Performance

- **Duration:** 16 min
- **Started:** 2026-04-15T15:07:00Z
- **Completed:** 2026-04-15T15:22:35Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments

- Added `SoftEMLTree.force_scaled_exp(variable, coefficient, strength=30.0)` using the existing `scaled_exponential_expr` and `embed_expr` machinery.
- Added scaled-exponential blind scaffold attempts for each variable and each suite-declared finite non-unit constant when `depth >= 9`.
- Verified direct blind `fit_eml_tree` recovery for `radioactive_decay`, `beer_lambert`, and `scaled_exp_growth` without compiler warm-starts, catalog candidates, or compile-only evidence.
- Extended benchmark metrics so proof artifacts expose scaffold source, strategy, coefficient, losses, snap margin, active node count, verifier status, and derived evidence class.
- Confirmed filtered `v1.5-shallow-proof` Beer-Lambert seed 0 recovers through the CLI with `blind_training_recovered` evidence.

## Task Commits

Each task was committed atomically through TDD RED/GREEN commits:

1. **Task 1: Add exact scaled-exp tree scaffold support**
   - `cdfe12b` test: add failing scaled-exp scaffold tests
   - `42e6a91` feat: add scaled-exp scaffold embedder
2. **Task 2: Add blind scaled-exp scaffold attempts and recovery tests**
   - `8a18d83` test: add failing scaled-exp optimizer tests
   - `c3f3c61` feat: add scaled-exp optimizer scaffolds
3. **Task 3: Propagate constants and diagnostics into proof run artifacts**
   - `93393de` test: add failing proof artifact scaffold diagnostics
   - `f14941a` feat: expose scaffold diagnostics in artifacts

## Files Created/Modified

- `src/eml_symbolic_regression/master_tree.py` - Added `force_scaled_exp()` returning `EmbeddingResult` from the existing expression embedding path.
- `src/eml_symbolic_regression/optimize.py` - Added `"scaled_exp"` default scaffolds, depth/constant gating, and optimizer initialization provenance.
- `src/eml_symbolic_regression/benchmark.py` - Added scaffold source, strategy, and coefficient to extracted run metrics.
- `tests/test_master_tree.py` - Covered exact scaled-exp snap evaluation, depth, node count, snap margin, and missing-constant behavior.
- `tests/test_optimizer_cleanup.py` - Covered verifier recovery and manifest provenance for scaled-exp blind training.
- `tests/test_benchmark_runner.py` - Covered filtered Beer-Lambert proof artifact diagnostics and evidence class.

## Decisions Made

- Scaled-exp attempts skip unit constants because generic `exp` already covers `exp(1*x)` and the plan targeted signed/scaled coefficient variants.
- The optimizer manifest serializes coefficients with `format_constant_value()` and records the matching `constant_label()` for auditability.
- Benchmark metrics report scaffold provenance only from the winning trained candidate manifest, keeping evidence classification derived from verifier status and training mode.

## Deviations from Plan

None - plan executed exactly as written.

**Total deviations:** 0 auto-fixed.
**Impact on plan:** No scope creep; implementation stayed inside plan-owned files.

## Issues Encountered

None. The focused proof artifact test and CLI smoke are intentionally slow because they execute the real depth-9 Beer-Lambert proof run.

## User Setup Required

None - no external service configuration required.

## Verification

- `python -m pytest tests/test_master_tree.py -q` - 6 passed, 1 existing `semantics.py` warning.
- `python -m pytest tests/test_optimizer_cleanup.py tests/test_master_tree.py -q` - 12 passed, 1 existing `semantics.py` warning.
- `python -m pytest tests/test_benchmark_runner.py tests/test_optimizer_cleanup.py -q` - 20 passed, 1 existing `semantics.py` warning.
- `python -m pytest tests/test_master_tree.py tests/test_optimizer_cleanup.py tests/test_benchmark_runner.py -q` - 26 passed, 2 existing `semantics.py` warnings.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli benchmark v1.5-shallow-proof --case shallow-beer-lambert-blind --seed 0 --output-dir /tmp/eml-phase30-plan02-smoke` - 1 run, 0 unsupported, 0 failed; aggregate recovery rate 1.000.

## Proof Smoke Artifact

- Suite result: `/tmp/eml-phase30-plan02-smoke/v1.5-shallow-proof/suite-result.json`
- Aggregate report: `/tmp/eml-phase30-plan02-smoke/v1.5-shallow-proof/aggregate.md`
- Beer-Lambert artifact status: `recovered`
- Evidence class: `blind_training_recovered`
- Metrics: `scaffold_source=scaffold_scaled_exp`, `scaffold_strategy=paper_scaled_exponential_family`, `scaffold_coefficient=-0.8`, `snap_active_node_count=19`, `snap_min_margin=1.0`, `verifier_status=recovered`

## Next Phase Readiness

Ready for Plan 30-03. The scaled-exponential recovery path and diagnostic surface are wired into benchmark artifacts; Plan 30-03 can now run the full shallow proof regression gate and aggregate guardrails.

## Self-Check: PASSED

- Confirmed all plan-owned code and test files were modified.
- Confirmed `force_scaled_exp|scaffold_scaled_exp` links exist between optimizer and master tree.
- Confirmed filtered proof CLI smoke recovered Beer-Lambert with verifier-owned `blind_training_recovered` evidence.
- Confirmed `STATE.md`, `ROADMAP.md`, and requirements state were not updated by this executor run.

---
*Phase: 30-bounded-shallow-blind-training-recovery*
*Completed: 2026-04-15*
