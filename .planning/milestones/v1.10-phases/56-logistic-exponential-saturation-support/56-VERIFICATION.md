---
phase: 56-logistic-exponential-saturation-support
verified: 2026-04-18
status: passed
score: 4/5 must-haves verified
deferred:
  - LOGI-04
  - LOGI-05
---

# Phase 56: Logistic Exponential-Saturation Support Verification Report

**Phase Goal:** Logistic-like laws can compile shorter through a structural exponential-saturation motif and receive honest warm-start evidence when strict support passes.
**Status:** passed

## Goal Achievement

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Compiler recognizes logistic-like `1/(1+c*exp(a))` structurally. | VERIFIED | `test_compile_logistic_uses_exponential_saturation_template` reports `exponential_saturation_template`. |
| 2 | Logistic relaxed compile depth is materially lower than archived depth 27. | VERIFIED | Logistic relaxed depth is now `15`, node count `49`, with baseline depth `27`, baseline nodes `77`, depth delta `12`, and node delta `28`. |
| 3 | Logistic compile diagnostics include the new macro hit. | VERIFIED | Macro diagnostics hits are exactly `["exponential_saturation_template"]`. |
| 4 | Logistic remains strict-unsupported if unchanged depth 13 gate does not pass. | VERIFIED | Diagnostic status remains `unsupported` with strict reason `depth_exceeded`. |
| 5 | Logistic warm-start evidence exists if strict support passes. | DEFERRED | Strict support did not pass; no warm-start was attempted or promoted. This is the intended fail-closed behavior. |

## Automated Checks

| Command | Result |
|---------|--------|
| Focused logistic and regression command from `56-01-SUMMARY.md` | `5 passed` |
| `PYTHONPATH=src python -m pytest tests/test_compiler_warm_start.py -q` | `33 passed, 1 warning` |

## Human Verification Required

None.

## Gaps Summary

No blocking gaps. Logistic has a structural macro-backed compile improvement but remains unsupported for strict warm-start promotion under the shipped gate.
