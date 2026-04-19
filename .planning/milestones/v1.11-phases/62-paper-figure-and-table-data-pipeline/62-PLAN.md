# Phase 62 Plan: Paper Figure and Table Data Pipeline

## Goal

Generate deterministic, plot-ready paper assets from the v1.11 locked evidence artifacts.

## Scope

- Add a paper asset generator that reads existing source-locked artifacts rather than recomputing claim logic.
- Emit source tables and SVG figures for:
  - regime recovery,
  - depth degradation,
  - scientific-law support,
  - motif depth deltas,
  - training lifecycle,
  - failure taxonomy,
  - prediction-only baseline diagnostics.
- Attach figure metadata with source table paths, denominators, included statuses, and claim boundaries.
- Add CLI and tests for representative generation.

## Constraints

- Do not merge blind, warm-start, perturbed, compile-only, and probe evidence into a single discovery claim.
- Logistic and Planck remain unsupported unless upstream source artifacts say otherwise.
- Baseline diagnostics are prediction-only and must remain outside EML recovery denominators.
- Figures must be reproducible from committed artifact fields.

## Verification

Run:

```bash
PYTHONPATH=src python -m pytest tests/test_paper_assets.py tests/test_verifier_demos_cli.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-assets --output-dir artifacts/paper/v1.11/assets
```
