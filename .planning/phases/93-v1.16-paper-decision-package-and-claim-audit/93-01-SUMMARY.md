---
phase: 93
plan: 93-01
status: complete
completed: 2026-04-22
---

# Plan 93-01 Summary: final v1.16 decision package

## What Changed

- Added `write_v116_final_decision_package` with final decision, final claim audit, source-lock, manifest, and README outputs.
- Added the `geml-v116-final` CLI command.
- Generated `artifacts/paper/v1.16-geml/final-decision/` and `artifacts/paper/v1.16-geml/README.md`.

## Package Result

- Final decision: `inconclusive`
- Paper claim allowed: `false`
- Final claim audit: `passed`
- Source locks: `source_locks_ok` is `true`
- README guidance: updated to match the inconclusive decision

## Verification

- `python -m pytest tests/test_paper_v116.py -q` passed with 13 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v116-final --campaign-dir artifacts/campaigns/v1.16-geml-pilot --budget-ladder-dir artifacts/campaigns/v1.16-geml-budget-ladder --package-dir artifacts/paper/v1.16-geml --ablation-dir artifacts/paper/v1.16-geml/ablations --output-dir artifacts/paper/v1.16-geml/final-decision --overwrite` completed with final claim audit `passed`.

## Key Files

- `src/eml_symbolic_regression/paper_v116.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_paper_v116.py`
- `artifacts/paper/v1.16-geml/final-decision/`
- `artifacts/paper/v1.16-geml/README.md`
