---
phase: 30-bounded-shallow-blind-training-recovery
reviewed: 2026-04-15T16:54:41Z
depth: standard
files_reviewed: 13
files_reviewed_list:
  - src/eml_symbolic_regression/benchmark.py
  - src/eml_symbolic_regression/compiler.py
  - src/eml_symbolic_regression/datasets.py
  - src/eml_symbolic_regression/master_tree.py
  - src/eml_symbolic_regression/optimize.py
  - src/eml_symbolic_regression/proof.py
  - tests/test_benchmark_contract.py
  - tests/test_benchmark_reports.py
  - tests/test_benchmark_runner.py
  - tests/test_master_tree.py
  - tests/test_optimizer_cleanup.py
  - tests/test_shallow_blind_proof_regression.py
  - tests/test_shallow_scaled_exponential_contract.py
findings:
  critical: 1
  warning: 0
  info: 0
  total: 1
status: issues_found
---

# Phase 30: Code Review Report

**Reviewed:** 2026-04-15T16:54:41Z
**Depth:** standard
**Files Reviewed:** 13
**Status:** issues_found

## Summary

Reviewed the Phase 30 benchmark, proof-contract, optimizer, scaled-exponential scaffold, dataset, and regression-test changes. The implementation adds exact scaled-exponential scaffold starts and then counts those runs as `blind_training_recovered`. That breaks the bounded shallow-blind proof contract: a run can satisfy the verifier because the target family and coefficient were injected through the initializer, not because blind training recovered the expression.

## Critical Issues

### CR-01: Scaffolded Exact Starts Are Counted as Blind-Training Proof

**File:** `src/eml_symbolic_regression/benchmark.py:893`

**Issue:** The blind benchmark path constructs `TrainingConfig` without overriding `scaffold_initializers`, so it uses the optimizer default from `src/eml_symbolic_regression/optimize.py:29`. For Phase 30 depth-9 proof cases, `_training_attempts` adds `scaffold_scaled_exp` attempts from the suite-provided coefficient constants (`src/eml_symbolic_regression/optimize.py:135-156`), and `_apply_scaffold` embeds the exact `exp(coefficient * variable)` tree before training (`src/eml_symbolic_regression/optimize.py:197-207`). The recovered artifact is then classified as `blind_training_recovered` solely because the run metadata says `training_mode == "blind_training"` (`src/eml_symbolic_regression/benchmark.py:1279-1280`).

This turns the bounded shallow-blind proof into scaffolded exact-shape verification. The tests also lock in the wrong contract by requiring a non-null scaffold source for proof runs (`tests/test_shallow_blind_proof_regression.py:80`) and by asserting the Beer-Lambert blind proof uses `scaffold_scaled_exp` (`tests/test_benchmark_runner.py:104-112`).

**Fix:**
Disable scaffold initializers for runs that are reported as blind proof, and prevent scaffolded recoveries from being counted as `blind_training_recovered` as a defense-in-depth check.

```python
# src/eml_symbolic_regression/benchmark.py
if run.start_mode == "blind":
    train = splits[0]
    config = TrainingConfig(
        depth=run.optimizer.depth,
        variables=(spec.variable,),
        constants=run.optimizer.constants,
        steps=run.optimizer.steps,
        restarts=run.optimizer.restarts,
        seed=run.seed,
        lr=run.optimizer.lr,
        scaffold_initializers=(),
    )
```

Then update the proof tests to assert blind-proof artifacts are not scaffolded:

```python
candidate = artifact["trained_eml_candidate"]
assert candidate["best_restart"]["attempt_kind"] == "random"
assert candidate["best_restart"]["initialization"] is None
assert artifact["metrics"]["scaffold_source"] is None
```

If scaffolded scaled-exponential recovery is intentional evidence, model it as a separate start mode or training mode and keep it out of the `paper-shallow-blind-recovery` bounded threshold.

---

_Reviewed: 2026-04-15T16:54:41Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
