---
phase: 30-bounded-shallow-blind-training-recovery
review_path: .planning/phases/30-bounded-shallow-blind-training-recovery/30-REVIEW.md
fixed: 1
skipped: 0
findings_in_scope: 1
status: all_fixed
iteration: 1
---

# Phase 30: Code Review Fix Report

## Summary

Fixed CR-01 by separating scaffolded blind-training recoveries from pure blind-training recoveries.

The fix does not disable scaffold initializers. Instead, recovered blind runs whose best optimizer attempt is a scaffold now receive the evidence class `scaffolded_blind_training_recovered` and classification `scaffolded_blind_recovery`. The `paper-shallow-blind-recovery` threshold still counts only `blind_training_recovered`, so exact scaffold starts can no longer satisfy the shallow-blind proof target.

## Fixes Applied

### CR-01: Scaffolded Exact Starts Are Counted as Blind-Training Proof

**Status:** fixed

**Commit:** `f7d3ad0 fix(30): distinguish scaffolded blind evidence`

**Changes:**
- Added `scaffolded_blind_training_recovered` to the proof evidence taxonomy.
- Derived scaffolded evidence from `trained_eml_candidate.best_restart.attempt_kind`.
- Kept scaffolded evidence out of the `paper-shallow-blind-recovery` counted evidence set.
- Updated regression tests so the v1.5 shallow suite can recover with scaffolds while the pure blind threshold correctly fails.

## Verification

- `python -m pytest tests/test_proof_contract.py tests/test_benchmark_reports.py tests/test_benchmark_runner.py -q` -> 26 passed, 1 existing `semantics.py:110` warning.
- `python -m pytest tests/test_shallow_blind_proof_regression.py -q` -> 2 passed in 19m21s.

## Residual Blocker

Phase 30 no longer satisfies SHAL-02 as written. The implementation can recover the declared shallow suite through paper-grounded scaffold initializers, but those runs are not pure random-initialized blind recovery under the paper/NORTH_STAR definition.

Next planning decision: either narrow the Phase 30 blind proof suite to targets that recover from random initialization, or reframe the scaled-exponential result as a separate scaffolded-training proof claim.
