---
phase: 92
plan: 92-01
status: complete
completed: 2026-04-22
---

# Plan 92-01 Summary: v1.16 ablation and paper-figure assets

## What Changed

- Added `write_v116_ablation_assets` with deterministic table, figure, failure-example, manifest, and source-lock outputs.
- Added the `geml-v116-ablations` CLI command.
- Generated `artifacts/paper/v1.16-geml/ablations/` from the source-locked pilot campaign, budget ladder, and v1.16 paper package.

## Package Result

- Decision: `inconclusive`
- Paper claim allowed: `false`
- Ablation rows: 12
- Failure-example rows: 7
- Figures: family recovery, loss before/after snap, branch anomalies, runtime, representative curves
- Source locks: all required inputs locked

## Verification

- `python -m pytest tests/test_paper_v116.py -q` passed with 11 tests.
- `PYTHONPATH=src python -m eml_symbolic_regression.cli geml-v116-ablations --campaign-dir artifacts/campaigns/v1.16-geml-pilot --budget-ladder-dir artifacts/campaigns/v1.16-geml-budget-ladder --package-dir artifacts/paper/v1.16-geml --output-dir artifacts/paper/v1.16-geml/ablations --overwrite` completed successfully.

## Key Files

- `src/eml_symbolic_regression/paper_v116.py`
- `src/eml_symbolic_regression/cli.py`
- `tests/test_paper_v116.py`
- `artifacts/paper/v1.16-geml/ablations/`
