# Phase 65: Shallow Seed and Depth-Curve Refresh - Summary

**Completed:** 2026-04-19  
**Status:** Complete

## What Changed

- Extended `paper_v112.py` with v1.12 evidence refresh suite builders and a runner.
- Added the `paper-refresh` CLI command.
- Generated `artifacts/campaigns/v1.12-evidence-refresh/` with:
  - 10 shallow current-code seed refresh rows.
  - 8 current-code depth refresh rows.
  - Suite definitions and suite results for shallow and depth refreshes.
  - Aggregate JSON/Markdown files.
  - Compact source tables for shallow runs, depth runs, and depth summary rows.
  - A manifest with source locks and reproduction command.
- Added regression tests for suite construction, row shape, and CLI registration.

## Results

- Shallow refresh: 10/10 verifier recovered.
  - Pure blind: 5/5 recovered for seeds 2-6.
  - Scaffolded: 5/5 recovered for seeds 2-6.
- Depth refresh: 4/8 verifier recovered.
  - Depth 2: 2/2 recovered.
  - Depth 3: 2/2 recovered.
  - Depth 4: 0/2 recovered.
  - Depth 5: 0/2 recovered.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_paper_v112.py`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli paper-refresh --output-dir artifacts/campaigns/v1.12-evidence-refresh --overwrite`

## Notes

- Runtime warnings from EML exponential overflow occurred during exact evaluation; the benchmark runner completed and recorded the affected rows honestly.
- Depth 4-5 failures remain visible in the source tables and aggregate evidence.
