---
phase: 29-paper-claim-contract-and-proof-dataset-harness
reviewed: 2026-04-15T13:58:15Z
depth: standard
files_reviewed: 11
files_reviewed_list:
  - src/eml_symbolic_regression/proof.py
  - src/eml_symbolic_regression/datasets.py
  - src/eml_symbolic_regression/benchmark.py
  - src/eml_symbolic_regression/cli.py
  - src/eml_symbolic_regression/campaign.py
  - tests/test_proof_contract.py
  - tests/test_proof_dataset_manifest.py
  - tests/test_benchmark_contract.py
  - tests/test_benchmark_runner.py
  - tests/test_benchmark_reports.py
  - tests/test_campaign.py
findings:
  critical: 0
  warning: 4
  info: 0
  total: 4
status: issues_found
---

# Phase 29: Code Review Report

**Reviewed:** 2026-04-15T13:58:15Z
**Depth:** standard
**Files Reviewed:** 11
**Status:** issues_found

## Summary

Reviewed the proof contract, deterministic proof dataset manifest, benchmark expansion/execution, CLI entry points, campaign reporting, and related tests. The main risks are data-contract issues: proof suite scope can drift from the claim matrix, malformed proof metadata can pass validation and crash execution before an artifact is written, and the proof dataset manifest can be generated with invalid parameters.

## Warnings

### WR-01: Proof Claim Scope Does Not Match the Built-In Proof Suite

**File:** `src/eml_symbolic_regression/proof.py:240-241`
**Issue:** `paper-shallow-blind-recovery` declares `suite_ids=("proof-shallow-blind",)` and case scope `("exp", "log", "radioactive_decay", "scaled_exponential_family")`, but the executable proof suite is `v1.5-shallow-proof` and includes `beer_lambert` instead of `scaled_exponential_family` (`src/eml_symbolic_regression/benchmark.py:700-707`). Because suite validation only checks the threshold policy, aggregate thresholds can count evidence for cases the claim does not declare and omit cases it does declare.
**Fix:**
```python
# Pick one stable contract key. If case_ids are benchmark case IDs:
suite_ids=("v1.5-shallow-proof",),
case_ids=(
    "shallow-exp-blind",
    "shallow-log-blind",
    "shallow-radioactive-decay-blind",
    "shallow-beer-lambert-blind",
),

# Then validate this in BenchmarkSuite.validate():
if case.claim_id is not None:
    claim = paper_claim(case.claim_id)
    if self.id not in claim.suite_ids:
        raise BenchmarkValidationError("invalid_proof_contract", "claim does not declare this suite", path=f"cases[{index}].claim_id")
    if claim.case_ids and case.id not in claim.case_ids:
        raise BenchmarkValidationError("invalid_proof_contract", "claim does not declare this case", path=f"cases[{index}].id")
```

### WR-02: Orphan Threshold Metadata Passes Validation Then Crashes the Runner

**File:** `src/eml_symbolic_regression/benchmark.py:229`
**Issue:** `_validate_proof_contract()` returns immediately when `claim_id` is absent, so a suite case can provide `threshold_policy_id` without a claim and still pass `suite.validate()`. If the policy ID is invalid, `_base_run_payload()` later calls `threshold_policy()` before `execute_benchmark_run()` enters its `try` block (`src/eml_symbolic_regression/benchmark.py:742-759`), aborting the whole benchmark instead of producing an `execution_error` artifact.
**Fix:**
```python
if self.claim_id is None:
    if self.threshold_policy_id is not None:
        raise BenchmarkValidationError(
            "invalid_proof_contract",
            "threshold_policy_id requires claim_id",
            path=f"{path}.threshold_policy_id",
        )
    return
```

Also consider moving `_base_run_payload(run)` inside the `try` block or writing a minimal error artifact if payload construction fails.

### WR-03: Proof Dataset Manifests Accept Invalid Sampling Contracts

**File:** `src/eml_symbolic_regression/datasets.py:212`
**Issue:** `proof_dataset_manifest()` does not validate `points` or `tolerance`. The CLI can write a manifest with `points=0`, which produces an empty train split, and a negative tolerance, which downstream proof/benchmark contracts treat as invalid elsewhere. That creates proof dataset artifacts that look schema-valid but cannot be trusted.
**Fix:**
```python
def proof_dataset_manifest(formula_id: str, *, points: int = 80, seed: int = 0, tolerance: float = 1e-8) -> dict[str, Any]:
    points = int(points)
    tolerance = float(tolerance)
    if points <= 0:
        raise ValueError("points must be positive")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    ...
```

Add CLI and unit coverage for `--points 0` and negative `--tolerance`.

### WR-04: Campaign Reproduction Command Is Not Shell-Quoted

**File:** `src/eml_symbolic_regression/campaign.py:457`
**Issue:** `_reproduction_command()` concatenates arguments with `" ".join(parts)`. Labels, output roots, and filter values containing spaces or shell metacharacters produce a broken command; a label such as `ok; echo injected` is rendered as an extra shell command in the report. The code does not execute this string, but the report explicitly tells users to run it, so it is a copy/paste command-injection risk and a reproducibility bug.
**Fix:**
```python
import shlex

...
return shlex.join(parts)
```

Keep the current simple-command tests and add a case with spaces or metacharacters in `--label` and `--output-root`.

---

_Reviewed: 2026-04-15T13:58:15Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
