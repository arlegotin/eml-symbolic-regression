---
phase: 27-compiler-coverage-and-depth-reduction
verified: 2026-04-15T16:25:00Z
status: passed
score: 4/4 must-haves verified
---

# Phase 27: Compiler Coverage and Depth Reduction Verification Report

**Phase Goal:** Users can move at least one v1.3 unsupported/depth-gated FOR_DEMO formula closer to verified EML coverage while preserving fail-closed compiler behavior.
**Verified:** 2026-04-15T16:25:00Z
**Status:** passed

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Compiler diagnostics expose strict unsupported reason plus relaxed depth, node count, rule trace, and validation when available. | VERIFIED | `diagnose_compile_expression` returns strict errors and relaxed metadata; Planck test checks relaxed depth and trace. |
| 2 | Shockley moves from v1.3 depth-gated unsupported to a verified compiled EML AST under the v1.4 default gate. | VERIFIED | Real filtered campaign reports `shockley-compile` as `recovered`, compiled depth 13, node count 35. |
| 3 | Damped oscillator remains explicitly unsupported for `cos` with tests documenting the deferred path. | VERIFIED | Damped diagnostic test asserts strict and relaxed `unsupported_operator`. |
| 4 | Unsupported formulas continue to emit structured reasons and diagnostics instead of invalid ASTs. | VERIFIED | Benchmark unsupported payloads include `compiled_eml.reason` and `compiled_eml.diagnostic`. |

**Score:** 4/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/eml_symbolic_regression/compiler.py` | Diagnostics and template | EXISTS + SUBSTANTIVE | Adds `diagnose_compile_expression` and `scaled_exp_minus_one_template`. |
| `src/eml_symbolic_regression/benchmark.py` | Diagnostic payloads | EXISTS + SUBSTANTIVE | Unsupported compile runs include diagnostics. |
| `tests/test_compiler_warm_start.py` | Compiler tests | EXISTS + SUBSTANTIVE | Covers Shockley, Planck, and damped oscillator. |
| `tests/test_benchmark_runner.py` | Benchmark path tests | EXISTS + SUBSTANTIVE | Covers Shockley campaign run and unsupported diagnostics. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| Compiler failure | Benchmark artifact | `diagnose_compile_expression` in `_compile_demo` | WIRED | Unsupported payload includes diagnostics. |
| Shockley template | Validation | `compile_and_validate` | WIRED | Accepted only after validation passes. |

## Requirements Coverage

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| COV-01 | SATISFIED | - |
| COV-02 | SATISFIED | - |
| COV-03 | SATISFIED | - |
| COV-04 | SATISFIED | - |

**Coverage:** 4/4 requirements satisfied

## Automated Checks

```bash
python -m pytest tests/test_compiler_warm_start.py tests/test_benchmark_runner.py tests/test_campaign.py -q
```

Result: 25 passed, 2 expected overflow-path warnings.

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli campaign standard --case shockley-compile --output-root /tmp/eml-v1.4-phase27 --label shockley --overwrite
```

Result: `recovered`, compiled depth 13, trace includes `scaled_exp_minus_one_template`.

## Human Verification Required

None - all verifiable items checked programmatically.

## Gaps Summary

**No gaps found.** Phase goal achieved. Ready to proceed.
