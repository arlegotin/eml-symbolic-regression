# Phase 63 Summary

## Implemented

- Added `src/eml_symbolic_regression/paper_package.py`.
- Added CLI command:

```bash
PYTHONPATH=src python -m eml_symbolic_regression.cli paper-package --output-dir artifacts/paper/v1.11 --overwrite
```

- Added tests in `tests/test_paper_package.py`.
- Generated the final v1.11 paper package root:
  - `artifacts/paper/v1.11/manifest.json`,
  - `artifacts/paper/v1.11/source-locks.json`,
  - `artifacts/paper/v1.11/claim-audit.json`,
  - `artifacts/paper/v1.11/claim-audit.md`,
  - `artifacts/paper/v1.11/paper-readiness.md`,
  - `artifacts/paper/v1.11/reproduction.md`,
  - copied `tables/`, `figures/`, `diagnostics/`, `campaigns/`, and `raw-hybrid/` snapshots.

## Audit Outcome

The generated claim audit passed all 7 checks:

- logistic remains unsupported,
- Planck remains unsupported,
- every figure has source JSON/CSV and metadata,
- loss-only recovery remains forbidden,
- regime denominators stay separated,
- current training successes and logistic/Planck probe failures are visible,
- final package inputs have file-level source locks.

## Paper Position

The final package supports a strong verifier-gated hybrid EML paper with honest limits:

- v1.11 current-code training: 8/8 recovered across separated pure-blind, scaffolded, same-AST warm-start, and perturbed-basin regimes.
- Logistic/Planck probes: 0/4 recovered, with 2 unsupported compile rows and 2 failed blind probes.
- Scientific-law support rows: Beer-Lambert, Shockley, Arrhenius, and Michaelis-Menten supported and verified.
- Logistic and Planck motif compression is visible but not promoted.
