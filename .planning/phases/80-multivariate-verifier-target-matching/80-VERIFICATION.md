# Phase 80 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_verify.py tests/test_expanded_datasets.py -q
```

Result: `21 passed in 1.79s`

```bash
PYTHONPATH=src python -m compileall -q src/eml_symbolic_regression/verify.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.

## Requirement Coverage

- VER-01: The fallback no longer uses only the first input variable for target lookup.
- VER-02: The fallback uses a full-row match when `target_mpmath` is absent.
- VER-03: The new regression covers repeated first-coordinate rows with distinct remaining coordinates and targets.
- VER-04: Existing verifier and expanded dataset tests pass.

## Residual Risk

- Full publication artifacts still need regeneration so downstream claim-audit outputs are produced from the corrected verifier. Phase 81 owns that rebuild.

