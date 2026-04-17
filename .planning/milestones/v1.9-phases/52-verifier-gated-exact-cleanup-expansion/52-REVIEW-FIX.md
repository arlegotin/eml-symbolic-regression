---
phase: 52-verifier-gated-exact-cleanup-expansion
fixed: 2026-04-17T15:58:00Z
review: 52-REVIEW.md
findings_fixed: 1
status: complete
---

# Phase 52 Review Fixes

## Fixed Findings

### WR-01: Per-root dedup counts can be credited to the wrong candidate root

**Status:** Fixed

`cleanup_failed_candidate()` now records raw per-root variant counts during generation, then computes per-root dedup ownership after the final global dedup map is stable. If a later root replaces an earlier duplicate variant, the winning root now owns the deduped count used in `variants_by_candidate_root`.

Regression coverage was added in `tests/test_repair.py` with a selected root and fallback root that generate the same repaired AST while the fallback root wins the dedup ranking due to a better probability gap. The test asserts the fallback owns at least one deduped variant and that per-root dedup counts sum to the global deduped count.

## Verification

```bash
PYTHONPATH=src python -m pytest tests/test_repair.py -q
```

Result: `17 passed, 7 warnings in 0.88s`

```bash
PYTHONPATH=src python -m pytest tests/test_repair.py tests/test_benchmark_runner.py::test_candidate_pool_cleanup_promotes_artifact_without_mutating_selected_or_fallback -q
```

Result: `18 passed, 7 warnings in 1.64s`

Warnings are the existing NumPy divide-by-zero warnings from EML semantics paths.
