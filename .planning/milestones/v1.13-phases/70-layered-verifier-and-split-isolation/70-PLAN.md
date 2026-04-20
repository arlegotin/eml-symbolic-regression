---
phase: 70
status: planned
created: 2026-04-20
type: execute
wave: 1
files_modified:
  - src/eml_symbolic_regression/verify.py
  - src/eml_symbolic_regression/optimize.py
  - tests/test_verify.py
requirements_addressed:
  - VERIF-01
  - VERIF-02
  - VERIF-03
  - VERIF-04
  - VERIF-05
  - SPLIT-01
  - SPLIT-02
  - SPLIT-03
must_haves:
  truths:
    - "Verifier reports symbolic evidence status when target_sympy is provided or explicitly unsupported otherwise."
    - "Verifier reports dense randomized and adversarial probe statuses."
    - "Verifier reports certificate status, including unsupported labels when interval evidence is unavailable."
    - "Split results and report dictionaries label training, selection, diagnostic, verifier, and final-confirmation roles."
    - "Exact-candidate ranking excludes final-confirmation splits."
---

# Phase 70: Layered Verifier and Split Isolation - Plan

## Objective

Upgrade verifier evidence reporting and selection split isolation while preserving existing verifier statuses and benchmark behavior.

## Tasks

### Task 1: Add Verifier Evidence Layers

<read_first>
- `src/eml_symbolic_regression/verify.py`
- `tests/test_verify.py`
</read_first>

<files>src/eml_symbolic_regression/verify.py</files>

<action>
Extend verifier dataclasses and `verify_candidate` with additive evidence fields: symbolic status, dense randomized status, adversarial status, certificate status, evidence level, metric role counts, and split roles. Add optional `target_sympy`, dense/adversarial probe count, and random seed parameters.
</action>

<acceptance_criteria>
- `VerificationReport.as_dict()` includes `symbolic_status`, `dense_random_status`, `adversarial_status`, `certificate_status`, `evidence_level`, and `metric_roles`.
- Existing callers that omit new parameters continue to work.
</acceptance_criteria>

### Task 2: Enforce Final-Confirmation Isolation In Candidate Ranking

<read_first>
- `src/eml_symbolic_regression/optimize.py`
- `src/eml_symbolic_regression/verify.py`
</read_first>

<files>src/eml_symbolic_regression/optimize.py</files>

<action>
Filter `verification_splits` before candidate ranking so splits with role `final_confirmation` are not used in selection metrics. Preserve final confirmation in the stored verifier report after ranking when those splits are present.
</action>

<acceptance_criteria>
- `_select_exact_candidate` uses selection-allowed splits for `_selection_metrics`.
- A test proves a candidate is not ranked by final-confirmation split errors.
</acceptance_criteria>

### Task 3: Add Focused Tests

<read_first>
- `tests/test_verify.py`
- `tests/test_optimizer_cleanup.py`
</read_first>

<files>tests/test_verify.py</files>

<action>
Add tests for symbolic equivalence pass, unsupported symbolic/certificate labels, dense/adversarial probe status with `target_mpmath`, split role labels, and final-confirmation isolation in candidate selection.
</action>

<acceptance_criteria>
- `PYTHONPATH=src python -m pytest tests/test_verify.py tests/test_optimizer_cleanup.py -q` exits 0.
</acceptance_criteria>

## Verification

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_verify.py tests/test_optimizer_cleanup.py tests/test_benchmark_reports.py -q
```
