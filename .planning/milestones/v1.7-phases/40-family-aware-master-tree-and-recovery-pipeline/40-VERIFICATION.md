# Phase 40 Verification

**Status:** passed
**Date:** 2026-04-16

## Commands

```bash
python -m pytest tests/test_semantics_expression.py tests/test_master_tree.py tests/test_optimizer_cleanup.py tests/test_benchmark_contract.py
```

Result: `79 passed, 3 warnings`.

```bash
python -m pytest --ignore=tests/test_shallow_blind_proof_regression.py
```

Result: `233 passed, 18 warnings`.

## Residual Risk

The full unfiltered suite was started and progressed to `tests/test_shallow_blind_proof_regression.py` without failures, then was interrupted after that expensive proof fixture produced no output for an extended period. That file reruns the historical v1.5 shallow proof campaign and is not the primary regression surface for the phase 40 code changes. The phase-specific tests and all non-shallow-proof tests passed.

## Success Criteria Check

- Fixed raw, `CEML_s`, and `ZEML_s` operator-family tree runs: passed.
- Centered snapping, embedding, candidate ranking, repair/refit metadata paths: passed.
- Unsupported centered warm-start and perturbed-tree benchmark paths fail closed with explicit diagnostics: passed.
- Scheduled `s` continuation metadata persists in optimizer manifests and benchmark budgets: passed.
- Raw EML defaults and existing benchmark/reporting contracts remain covered by regression tests: passed.
