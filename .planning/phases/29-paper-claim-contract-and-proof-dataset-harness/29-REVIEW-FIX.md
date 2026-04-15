---
phase: 29-paper-claim-contract-and-proof-dataset-harness
fixed_at: 2026-04-15T14:20:30Z
review_path: .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-REVIEW.md
iteration: 3
findings_in_scope: 6
fixed: 6
skipped: 0
status: all_fixed
---

# Phase 29: Code Review Fix Report

**Fixed at:** 2026-04-15T14:20:30Z
**Source review:** .planning/phases/29-paper-claim-contract-and-proof-dataset-harness/29-REVIEW.md
**Iteration:** 3

**Summary:**
- Findings in scope across auto-fix iterations: 6
- Fixed: 6
- Skipped: 0
- Final re-review: clean

## Fixed Issues

### Iteration 1

#### WR-01: Proof Claim Scope Does Not Match the Built-In Proof Suite

**Files modified:** `src/eml_symbolic_regression/proof.py`, `src/eml_symbolic_regression/benchmark.py`, `tests/test_proof_contract.py`, `tests/test_benchmark_contract.py`
**Commit:** 3759206
**Applied fix:** Aligned the `paper-shallow-blind-recovery` claim scope with the executable `v1.5-shallow-proof` suite and its benchmark case IDs, then added suite/case membership validation for proof-aware benchmark cases.

#### WR-02: Orphan Threshold Metadata Passes Validation Then Crashes the Runner

**Files modified:** `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_contract.py`, `tests/test_benchmark_runner.py`
**Commit:** 1d97f87
**Applied fix:** Rejected `threshold_policy_id` without `claim_id` during benchmark validation and added coverage ensuring malformed proof metadata fails closed before runner execution.

#### WR-03: Proof Dataset Manifests Accept Invalid Sampling Contracts

**Files modified:** `src/eml_symbolic_regression/datasets.py`, `src/eml_symbolic_regression/cli.py`, `tests/test_proof_dataset_manifest.py`, `tests/test_benchmark_runner.py`
**Commit:** ffec8e8
**Applied fix:** Added positive `points` and `tolerance` validation to proof dataset manifest generation and CLI coverage for invalid sampling arguments.

#### WR-04: Campaign Reproduction Command Is Not Shell-Quoted

**Files modified:** `src/eml_symbolic_regression/campaign.py`, `tests/test_campaign.py`
**Commit:** 16c999f
**Applied fix:** Switched campaign reproduction command rendering to shell-safe quoting and added regression coverage for labels/output roots with spaces and shell metacharacters.

### Iteration 2

#### WR-01: String Sequence Fields Are Iterated Character-by-Character

**Files modified:** `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_contract.py`
**Commit:** 6974401
**Applied fix:** Added `_tuple_field()` validation so `seeds`, `perturbation_noise`, and `tags` reject string payloads before iteration/casting.

### Iteration 3

#### WR-01: Unsupported Warm-Start Depth Gates Keep Recovered Claim Status

**Files modified:** `src/eml_symbolic_regression/benchmark.py`, `tests/test_benchmark_reports.py`
**Commit:** 3addce1
**Applied fix:** The warm-start depth gate now overrides the compiled seed verifier `claim_status` to `unsupported` after spreading the compiled payload. Added a regression that compiles a `beer_lambert` warm-start seed with `max_warm_depth` forced below the compiled depth, then verifies the run artifact stays unsupported and aggregate recovery counts remain at zero.

---

_Fixed: 2026-04-15T14:20:30Z_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 3_
