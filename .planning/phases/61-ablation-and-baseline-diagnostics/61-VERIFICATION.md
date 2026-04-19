# Phase 61 Verification

## Commands

```bash
PYTHONPATH=src python -m pytest tests/test_paper_diagnostics.py tests/test_verifier_demos_cli.py -q
PYTHONPATH=src python -m eml_symbolic_regression.cli diagnostics paper-ablations --output-dir artifacts/diagnostics/v1.11-paper-ablations
```

## Results

- Paper diagnostics and CLI tests: 13 passed.
- Diagnostics command completed successfully.

## Artifact Checks

`artifacts/diagnostics/v1.11-paper-ablations/manifest.json` reports:

- `motif_depth_deltas`: 6
- `regime_comparison`: 12
- `repair_refit`: 12
- `baseline_diagnostics`: 20

The manifest records source hashes for:

- v1.11 scientific-law table.
- v1.11 paper-training aggregate.
- v1.11 logistic/Planck probe aggregate.
- v1.9 repair summary.

## Claim Checks

- Motif rows are compile-depth diagnostics, not recovery claims.
- Logistic and Planck remain unsupported in motif rows.
- Baseline rows are prediction-only diagnostics and do not enter EML recovery denominators.
