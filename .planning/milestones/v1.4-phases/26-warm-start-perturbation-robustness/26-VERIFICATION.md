---
phase: 26-warm-start-perturbation-robustness
verified: 2026-04-15T15:45:00Z
status: passed
score: 4/4 must-haves verified
---

# Phase 26: Warm-Start Perturbation Robustness Verification Report

**Phase Goal:** Users can improve or precisely explain Beer-Lambert warm-start failures under stronger perturbations.
**Verified:** 2026-04-15T15:45:00Z
**Status:** passed

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Beer-Lambert perturbation manifests include active-slot counts, changed-slot counts, verifier status, and a failure mechanism. | VERIFIED | `warm_start.py` writes `manifest["diagnosis"]` with all required fields. |
| 2 | High-perturbation failures are narrowed to a reproducible mechanism without promoting failed snaps. | VERIFIED | A real filtered standard campaign at noise 35 reported `snapped_but_failed`, mechanism `active_slot_perturbation`, verifier `failed`. |
| 3 | Existing warm-start status taxonomy remains distinct. | VERIFIED | Status assignment logic remains `same_ast_return`, `verified_equivalent_ast`, `snapped_but_failed`, `soft_fit_only`, `failed`. |
| 4 | Literal-constant provenance and verifier-owned recovery semantics remain unchanged. | VERIFIED | No compiler constants or verifier code changed; diagnosis is additive metadata. |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/warm_start.py` | Diagnosis block | EXISTS + SUBSTANTIVE | Adds mechanism classification. |
| `src/eml_symbolic_regression/benchmark.py` | Metrics propagation | EXISTS + SUBSTANTIVE | Adds `warm_start_mechanism`. |
| `src/eml_symbolic_regression/campaign.py` | CSV column | EXISTS + SUBSTANTIVE | Adds `warm_start_mechanism` to `runs.csv`. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| Warm-start manifest | Benchmark metrics | `_extract_run_metrics` | WIRED | Mechanism appears in aggregate rows. |
| Benchmark metrics | Campaign CSV | `_run_csv_row` | WIRED | Mechanism appears in `tables/runs.csv`. |

## Requirements Coverage

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| PERT-01 | SATISFIED | - |
| PERT-02 | SATISFIED | - |
| PERT-03 | SATISFIED | - |
| PERT-04 | SATISFIED | - |

**Coverage:** 4/4 requirements satisfied

## Automated Checks

```bash
python -m pytest tests/test_compiler_warm_start.py tests/test_campaign.py tests/test_benchmark_runner.py -q
```

Result: 21 passed, 2 expected overflow-path warnings.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign standard --case beer-perturbation-sweep --seed 0 --perturbation-noise 35 --output-root /tmp/eml-v1.4-phase26 --label beer-35 --overwrite
```

Result: aggregate and CSV row reported `warm_start_mechanism=active_slot_perturbation`.

## Human Verification Required

None - all verifiable items checked programmatically.

## Gaps Summary

**No gaps found.** Phase goal achieved. Ready to proceed.
