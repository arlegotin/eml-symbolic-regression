# Phase 61 Plan: Ablation and Baseline Diagnostics

## Goal

Add low-hanging diagnostics that explain which hybrid pieces matter without changing recovery denominators.

## Scope

- Derive motif-depth deltas from locked scientific-law run artifacts.
- Derive regime comparisons from the v1.11 training/probe aggregates.
- Surface repair/refit/candidate-pool diagnostics from existing repair evidence and probe artifacts.
- Add scoped local prediction-only baseline diagnostics using NumPy.
- Keep baselines separate from EML verifier-owned recovery.

## Tasks

1. Add a paper diagnostics module that reads locked campaign/package sources and writes JSON/CSV/Markdown outputs.
2. Add a CLI entry point under `diagnostics`.
3. Generate `artifacts/diagnostics/v1.11-paper-ablations/`.
4. Add tests for schema, current logistic/Planck motif rows, regime separation, and baseline limitation labels.
5. Run targeted tests and the diagnostics command.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_paper_diagnostics.py tests/test_verifier_demos_cli.py -q`
- `PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics paper-ablations --output-dir artifacts/diagnostics/v1.11-paper-ablations`

## Constraints

- Diagnostic baselines are prediction-only and do not enter EML recovery denominators.
- Motif rows report compile-depth/node deltas only; they do not promote unsupported laws.
- Ablation rows must list source artifacts and changed variables.
