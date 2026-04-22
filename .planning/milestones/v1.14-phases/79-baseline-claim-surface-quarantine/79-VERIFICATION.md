# Phase 79 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_baseline_harness.py tests/test_publication_rebuild.py -q
```

Result: `13 passed in 1.60s`

```bash
PYTHONPATH=src python -m compileall -q src/eml_symbolic_regression/baselines.py src/eml_symbolic_regression/publication.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Requirement Coverage

- BASE-01: README and generated baseline report now quarantine baseline rows as diagnostic/future-work context.
- BASE-02: Baseline rows expose dependency, denominator, unsupported reason, adapter launch status, fixed-budget launch status, and main-surface eligibility.
- BASE-03: Missing or unsupported external adapters are labeled as not launched and non-comparison evidence.
- BASE-04: Publication claim audit rejects main-surface baseline comparison claims unless eligible completed external fixed-budget rows exist.

## Residual Risk

- Existing committed v1.13 baseline artifacts are not regenerated in this phase. Phase 81 owns artifact rebuild from the corrected baseline schema.

