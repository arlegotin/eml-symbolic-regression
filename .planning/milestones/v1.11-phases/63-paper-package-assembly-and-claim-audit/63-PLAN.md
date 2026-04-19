# Phase 63 Plan: Paper Package Assembly and Claim Audit

## Goal

Assemble the final v1.11 paper evidence package and verify that the visible claims remain claim-safe.

## Scope

- Add a v1.11 package assembler with root manifest and source locks.
- Snapshot paper tables, figures, raw-hybrid scientific-law tables, diagnostics, and current-code training/probe aggregates.
- Write reproduction commands and paper-readiness summary.
- Add an automated claim audit covering:
  - logistic/Planck unsupported status,
  - figure source-table coverage,
  - loss-only recovery prohibition,
  - separated regime denominators,
  - source-lock coverage.
- Add CLI and tests.

## Verification

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_paper_package.py tests/test_raw_hybrid_paper.py tests/test_paper_assets.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-package --output-dir artifacts/paper/v1.11 --overwrite
```
