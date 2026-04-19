# Phase 66: Paper-Facing Figures, Captions, and Negative Results - Summary

**Completed:** 2026-04-19  
**Status:** Complete

## What Changed

- Extended `paper_v112.py` with paper-facing artifact generation.
- Added the `paper-figures` CLI command.
- Generated under `artifacts/paper/v1.11/draft/`:
  - `figure-captions.md`
  - `table-captions.md`
  - `tables/motif-library-evolution.json`
  - `tables/motif-library-evolution.csv`
  - `tables/motif-library-evolution.md`
  - `tables/logistic-planck-negative-results.json`
  - `tables/logistic-planck-negative-results.csv`
  - `tables/logistic-planck-negative-results.md`
  - `figures/pipeline.svg`
  - `figures/pipeline.metadata.json`
  - `paper-facing-manifest.json`
- Added tests for motif evolution, negative-result rows, generated assets, and CLI wiring.

## Results

- Motif evolution table includes Arrhenius, Logistic diagnostic, Michaelis-Menten, Planck diagnostic, and Shockley.
- Logistic remains `promotion: no` with relaxed motif depth 15 and strict gate 13.
- Planck remains `promotion: no` with v1.11 diagnostic convention 24 -> 14 and strict gate 13.
- The pipeline figure documents data -> soft complete EML tree -> snap -> candidate pool/repair/refit -> verifier.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_paper_v112.py`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli paper-figures --output-dir artifacts/paper/v1.11/draft`

## Notes

- Planck caption/table text explicitly records the depth-convention caveat instead of hiding it.
- Captions preserve regime separation and do not promote unsupported diagnostics.
