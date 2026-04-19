# Phase 62 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_paper_assets.py tests/test_verifier_demos_cli.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-assets --output-dir artifacts/paper/v1.11/assets
```

## Results

- Paper asset and CLI regression tests: 13 passed.
- Paper asset generation completed successfully.

## Artifact Checks

`artifacts/paper/v1.11/assets/manifest.json` reports:

- 7 tables,
- 7 figures,
- 7 source locks.

The generated package includes source tables and figure metadata for:

- regime recovery,
- depth degradation,
- scientific-law support,
- motif depth deltas,
- training lifecycle,
- failure taxonomy,
- prediction-only baseline diagnostics.

## Claim Checks

- Every figure has adjacent source-table JSON/CSV and metadata.
- Figure metadata records denominator and claim-boundary text.
- Logistic and Planck remain unsupported in the generated scientific-law support table.
- Baseline diagnostics remain prediction-only and outside EML recovery denominators.
